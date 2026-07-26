#!/usr/bin/env python3
"""Print a pseudonymous evidence packet for a human rater.

    python artifact/human_validation/show_packet.py PKT-07
    python artifact/human_validation/show_packet.py PKT-07 --file eval/eval.py

Output is line-numbered so a rater can cite `eval/eval.py:120-134` as an
evidence pointer, exactly as the model judges were required to do.  The
release name is never printed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # packets contain non-cp1252 characters
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
BUNDLES = ROOT / "artifact/audit/evidence/r2_evidence_bundles.json"
KEY = Path(__file__).resolve().parent / "packet_key.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet_id")
    parser.add_argument("--file", default=None,
                        help="show one file; omit to list the packet contents")
    parser.add_argument("--readme", action="store_true", help="show the README")
    args = parser.parse_args()

    key = json.loads(KEY.read_text(encoding="utf-8"))
    name = key.get(args.packet_id.upper())
    if name is None:
        raise SystemExit(f"unknown packet {args.packet_id}; run build_rater_forms.py first")
    bundle = json.loads(BUNDLES.read_text(encoding="utf-8"))[name]
    files = bundle.get("eval_files") or {}

    print(f"packet {args.packet_id.upper()}  commit {bundle.get('commit', '')}")
    if args.readme or (args.file and args.file == bundle.get("readme_path")):
        body = bundle.get("readme") or bundle.get("readme_text") or ""
        show(bundle.get("readme_path", "README.md"), body)
        return
    if args.file:
        if args.file not in files:
            raise SystemExit(f"not in packet: {args.file}\navailable: {sorted(files)}")
        show(args.file, files[args.file])
        return
    print(f"  readme: {bundle.get('readme_path', '(none)')}   (--readme to view)")
    print("  evaluation files (--file <path> to view):")
    for path in sorted(files):
        print(f"    {path}  ({len(files[path].splitlines())} lines)")


def show(path: str, body: str) -> None:
    print(f"\n===== {path} =====")
    for number, line in enumerate(body.splitlines(), 1):
        print(f"{number:5d} | {line}")


if __name__ == "__main__":
    main()
