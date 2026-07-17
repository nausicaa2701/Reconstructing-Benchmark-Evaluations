#!/usr/bin/env python3
"""Export a complete, secret-scanned panel run as a release artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from common import HERE, ROOT, WORK

PROVIDERS = ["openai", "anthropic", "gemini"]
SECRET_PATTERNS = [
    re.compile(rb"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(rb"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(rb"AIza[A-Za-z0-9_-]{20,}"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_complete(run_dirs: dict[str, Path]) -> None:
    for provider in PROVIDERS:
        count = len(list((run_dirs[provider] / "normalized" / provider).glob("B*.json")))
        if count != 26:
            raise SystemExit(f"{provider}: expected 26 normalized packets, found {count}")


def scan(path: Path) -> None:
    for file in path.rglob("*"):
        if not file.is_file():
            continue
        payload = file.read_bytes()
        if any(pattern.search(payload) for pattern in SECRET_PATTERNS):
            raise SystemExit(f"Potential API key found in release file: {file}")


def copy_provider(source: Path, target: Path, provider: str) -> None:
    shutil.copytree(source / "raw" / provider, target / "raw" / provider)
    shutil.copytree(
        source / "normalized" / provider,
        target / "normalized" / provider,
    )


def copy_run_metadata(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / "run_manifest.json", target / "run_manifest.json")
    shutil.copy2(source / "usage.jsonl", target / "usage.jsonl")
    errors = source / "errors.jsonl"
    if errors.exists():
        shutil.copy2(errors, target / "errors.jsonl")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="panel-v1")
    parser.add_argument("--gemini-run-id", default=None)
    parser.add_argument("--repeat-run-id", default=None)
    parser.add_argument("--gemini-repeat-run-id", default=None)
    parser.add_argument("--superseded-partial-run-id", default=None)
    parser.add_argument(
        "--output-dir", type=Path,
        default=ROOT / "artifact/audit/model_panel_v1",
    )
    args = parser.parse_args()
    run_dir = WORK / "runs" / args.run_id
    run_dirs = {provider: run_dir for provider in PROVIDERS}
    if args.gemini_run_id:
        run_dirs["gemini"] = WORK / "runs" / args.gemini_run_id
    assert_complete(run_dirs)
    if args.output_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing release: {args.output_dir}")
    args.output_dir.mkdir(parents=True)
    for name in ["config.json", "config.production.json", "judge_output_schema.json", "prompt.txt"]:
        shutil.copy2(HERE / name, args.output_dir / name)
    shutil.copy2(HERE / "config.json", args.output_dir / "config.repeat.json")
    for name in ["packet_manifest.json", "private_benchmark_map.json"]:
        shutil.copy2(WORK / name, args.output_dir / name)
    shutil.copytree(WORK / "packets", args.output_dir / "packets")
    for provider in PROVIDERS:
        copy_provider(run_dirs[provider], args.output_dir, provider)
    manifests = args.output_dir / "run_manifests"
    usage = args.output_dir / "usage"
    manifests.mkdir()
    usage.mkdir()
    for run_id, source in sorted({path.name: path for path in run_dirs.values()}.items()):
        shutil.copy2(source / "run_manifest.json", manifests / f"{run_id}.json")
        shutil.copy2(source / "usage.jsonl", usage / f"{run_id}.jsonl")
        errors = source / "errors.jsonl"
        if errors.exists():
            shutil.copy2(errors, usage / f"{run_id}.errors.jsonl")
    repeat_dirs = None
    if args.repeat_run_id or args.gemini_repeat_run_id:
        if not (args.repeat_run_id and args.gemini_repeat_run_id):
            raise SystemExit("Both repeat run IDs are required together")
        repeat = WORK / "runs" / args.repeat_run_id
        gemini_repeat = WORK / "runs" / args.gemini_repeat_run_id
        repeat_dirs = {"openai": repeat, "anthropic": repeat, "gemini": gemini_repeat}
        repeat_target = args.output_dir / "repeatability"
        for provider in PROVIDERS:
            expected = len(list((repeat_dirs[provider] / "normalized" / provider).glob("B*.json")))
            if expected != 6:
                raise SystemExit(f"repeat {provider}: expected 6 packets, found {expected}")
            copy_provider(repeat_dirs[provider], repeat_target, provider)
        for source in sorted(set(repeat_dirs.values())):
            copy_run_metadata(source, repeat_target / "runs" / source.name)

    history = args.output_dir / "protocol_history"
    medium_raw = run_dir / "raw" / "gemini"
    if medium_raw.exists():
        pilot = history / "excluded_gemini_default_thinking_pilot"
        shutil.copytree(medium_raw, pilot / "raw")
        medium_normalized = run_dir / "normalized" / "gemini"
        if medium_normalized.exists():
            shutil.copytree(medium_normalized, pilot / "normalized")
    if args.superseded_partial_run_id:
        partial = WORK / "runs" / args.superseded_partial_run_id
        partial_target = history / "superseded_partial_repeat" / partial.name
        shutil.copytree(partial / "raw", partial_target / "raw")
        shutil.copytree(partial / "normalized", partial_target / "normalized")
        copy_run_metadata(partial, partial_target)

    release_protocol = {
        "production_runs": {provider: path.name for provider, path in run_dirs.items()},
        "repeatability_runs": (
            {provider: path.name for provider, path in repeat_dirs.items()}
            if repeat_dirs else None
        ),
        "excluded_pilot": {
            "run": args.run_id,
            "provider": "gemini",
            "reason": "Default-thinking preflight was excluded wholesale after structured output truncation; production reran all 26 packets with low thinking.",
        },
        "superseded_partial_repeat": args.superseded_partial_run_id,
        "operational_amendment": "Repeat request timeout increased from 180s to 600s; model, prompt, schema, packets, and inference settings were unchanged.",
        "config_snapshots": {
            "production_and_gemini_repeat": "config.production.json",
            "openai_anthropic_repeat": "config.repeat.json",
        },
    }
    (args.output_dir / "RELEASE_PROTOCOL.json").write_text(
        json.dumps(release_protocol, indent=2) + "\n"
    )
    analysis = WORK / "analysis"
    if analysis.exists():
        shutil.copytree(analysis, args.output_dir / "analysis")
    scan(args.output_dir)
    hashes = {
        str(path.relative_to(args.output_dir)): digest(path)
        for path in sorted(args.output_dir.rglob("*")) if path.is_file()
    }
    (args.output_dir / "RELEASE_HASHES.json").write_text(
        json.dumps(hashes, indent=2) + "\n"
    )
    print(json.dumps({"output_dir": str(args.output_dir), "files": len(hashes)}, indent=2))


if __name__ == "__main__":
    main()
