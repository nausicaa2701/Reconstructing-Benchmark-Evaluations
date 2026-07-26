#!/usr/bin/env python3
"""Build identical, line-addressable evidence packets for all model judges."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from common import ROOT, WORK, canonical_hash

SOURCE = ROOT / "artifact/audit/evidence/r2_evidence_bundles.json"


def numbered(text: str) -> tuple[str, int]:
    lines = text.splitlines() or [""]
    return "\n".join(f"L{i:05d}: {line}" for i, line in enumerate(lines, 1)), len(lines)


def make_source(source_id: str, path: str, content: str) -> dict:
    rendered, count = numbered(content)
    return {
        "source_id": source_id,
        "path": path,
        "sha256": hashlib.sha256(content.encode()).hexdigest(),
        "line_count": count,
        "numbered_content": rendered,
    }


def build(output_dir: Path) -> dict:
    bundles = json.loads(SOURCE.read_text())
    packets_dir = output_dir / "packets"
    packets_dir.mkdir(parents=True, exist_ok=True)
    private_map, manifest = {}, []
    for index, benchmark in enumerate(sorted(bundles), 1):
        bundle = bundles[benchmark]
        packet_id = f"B{index:03d}"
        sources = [make_source("E001", bundle["readme_path"], bundle["readme"])]
        for source_index, (path, content) in enumerate(sorted(bundle["eval_files"].items()), 2):
            sources.append(make_source(f"E{source_index:03d}", path, content))
        core = {
            "packet_id": packet_id,
            "frozen_commit": bundle["commit"],
            "sources": sources,
        }
        packet = {**core, "packet_sha256": canonical_hash(core)}
        path = packets_dir / f"{packet_id}.json"
        path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
        try:
            manifest_path = path.relative_to(ROOT)
        except ValueError:
            manifest_path = path
        private_map[packet_id] = {
            "benchmark": benchmark,
            "repository": bundle["repo"],
            "frozen_commit": bundle["commit"],
        }
        manifest.append({
            "packet_id": packet_id,
            "packet_sha256": packet["packet_sha256"],
            "source_count": len(sources),
            "path": str(manifest_path),
        })
    (output_dir / "packet_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    (output_dir / "private_benchmark_map.json").write_text(
        json.dumps(private_map, indent=2, ensure_ascii=False) + "\n"
    )
    return {"packets": len(manifest), "output_dir": str(output_dir)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=WORK)
    args = parser.parse_args()
    print(json.dumps(build(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
