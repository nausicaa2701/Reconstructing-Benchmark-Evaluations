#!/usr/bin/env python3
"""Emit one official-environment build spec per release that reached execution.

Reads the frozen execution manifests and writes, for each in-scope release, a
skeleton spec recording the frozen commit, the authoritative setup file to be
discovered on re-clone, and the E3-official / E3-portable outcome pair to be
filled in.  Nothing here executes a scorer; see official_env_protocol.md.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFESTS = ROOT / "artifact" / "execution" / "manifests"
OUT = Path(__file__).resolve().parent / "official_env_specs"


def main() -> None:
    index = json.loads((MANIFESTS / "INDEX.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    written, skipped = [], []
    for path in sorted(MANIFESTS.glob("*.json")):
        if path.name == "INDEX.json":
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        spec = {
            "benchmark": manifest["benchmark"],
            "frozen_commit": manifest["frozen_commit"],
            "portable_first_pass_label": manifest["first_pass"]["label"],
            "portable_repair_label": (manifest.get("repair_pass") or {}).get("label"),
            "authoritative_setup_file": None,
            "base_image": None,
            "build_commands": [],
            "resolved_packages_digest": None,
            "E3_official_first_pass": None,
            "E3_official_after_repair": None,
            "E3_portable_first_pass": manifest["first_pass"]["label"] == "pass-as-documented",
            "under_specified_base": None,
            "environment_contract_findings": [],
            "status": "pending-execution",
        }
        (OUT / f"{manifest['benchmark'].replace('/', '_')}.json").write_text(
            json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        written.append(manifest["benchmark"])
    for entry in index if isinstance(index, list) else index.get("releases", []):
        name = entry.get("benchmark") if isinstance(entry, dict) else entry
        if name and name not in written:
            skipped.append(name)
    print(json.dumps({"specs_written": len(written),
                      "out_of_scope_no_invocable_interface": sorted(skipped)},
                     indent=2))


if __name__ == "__main__":
    main()
