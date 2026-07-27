#!/usr/bin/env python3
"""Build a complete, verifiable manifest of the released artifact tree.

Writes artifact/MANIFEST.sha256 (one `sha256  path` line per file, sorted) and
artifact/MANIFEST.json (path, size, sha256, plus release metadata).  Run this
immediately before tagging a release; the tag, the manifest, and the archived
DOI must all describe the same bytes.

    python tools/build_release_manifest.py --version v1.0.0 --paper-sha256 <hash>
    python tools/build_release_manifest.py --verify
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
SKIP_DIRS = {"__pycache__", "work", ".git"}
SKIP_NAMES = {
    "MANIFEST.sha256",
    "MANIFEST.json",
    ".DS_Store",
    ".env",
    "_merged_rater_a_labels.json",  # local merge scratch; never release
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def released_files() -> list[Path]:
    files = []
    for path in sorted(ARTIFACT.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES or SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return files


def build(version: str, paper_sha256: str | None) -> dict:
    entries = []
    for path in released_files():
        entries.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        })
    lines = [f"{entry['sha256']}  {entry['path']}" for entry in entries]
    (ARTIFACT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest = {
        "release_version": version,
        "built": date.today().isoformat(),
        "paper_pdf_sha256": paper_sha256,
        "n_files": len(entries),
        "total_bytes": sum(entry["bytes"] for entry in entries),
        "license": "CC-BY-4.0 for original contributions; see artifact/LICENSE",
        "regeneration": "python artifact/reproduce.py",
        "frozen_layer": "corpus/, audit/, execution/logs/, execution/manifests/",
        "living_layer": "docs/corrections.csv, docs/maintainer_responses.csv, human_validation/, environment/official_env_specs/",
        "files": entries,
    }
    (ARTIFACT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                            encoding="utf-8")
    return manifest


def verify() -> int:
    manifest = json.loads((ARTIFACT / "MANIFEST.json").read_text(encoding="utf-8"))
    recorded = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    current = {path.relative_to(ROOT).as_posix(): digest(path) for path in released_files()}
    added = sorted(set(current) - set(recorded))
    removed = sorted(set(recorded) - set(current))
    changed = sorted(p for p in set(recorded) & set(current) if recorded[p] != current[p])
    print(json.dumps({"release_version": manifest["release_version"], "added": added,
                      "removed": removed, "changed": changed}, indent=2))
    return 1 if (added or removed or changed) else 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v1.0.0")
    parser.add_argument("--paper-sha256", default=None)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        raise SystemExit(verify())
    manifest = build(args.version, args.paper_sha256)
    print(json.dumps({k: v for k, v in manifest.items() if k != "files"}, indent=2))


if __name__ == "__main__":
    main()
