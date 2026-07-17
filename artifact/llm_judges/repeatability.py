#!/usr/bin/env python3
"""Compare a preselected repeated sample with the frozen primary panel run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import CRITERIA, PERMISSIVE_PASS, WORK, read_json

PROVIDERS = ["openai", "anthropic", "gemini"]
DEFAULT_SAMPLE = ["B001", "B004", "B008", "B009", "B021", "B024"]


def labels(run_dir: Path, provider: str, packet: str) -> dict[str, str]:
    payload = read_json(run_dir / "normalized" / provider / f"{packet}.json")
    return {row["criterion"]: row["label"] for row in payload["judgment"]["decisions"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-run", default="panel-v1")
    parser.add_argument("--repeat-run", default="panel-v1-repeat")
    parser.add_argument("--gemini-base-run", default=None)
    parser.add_argument("--gemini-repeat-run", default=None)
    parser.add_argument("--packets", nargs="+", default=DEFAULT_SAMPLE)
    args = parser.parse_args()
    base, repeat = WORK / "runs" / args.base_run, WORK / "runs" / args.repeat_run
    base_runs = {provider: base for provider in PROVIDERS}
    repeat_runs = {provider: repeat for provider in PROVIDERS}
    if args.gemini_base_run:
        base_runs["gemini"] = WORK / "runs" / args.gemini_base_run
    if args.gemini_repeat_run:
        repeat_runs["gemini"] = WORK / "runs" / args.gemini_repeat_run
    per_provider, all_exact, all_binary = {}, 0, 0
    total = len(args.packets) * len(PROVIDERS) * len(CRITERIA)
    for provider in PROVIDERS:
        exact = binary = 0
        for packet in args.packets:
            first = labels(base_runs[provider], provider, packet)
            second = labels(repeat_runs[provider], provider, packet)
            for criterion in CRITERIA:
                exact += first[criterion] == second[criterion]
                binary += (first[criterion] in PERMISSIVE_PASS) == (second[criterion] in PERMISSIVE_PASS)
        cells = len(args.packets) * len(CRITERIA)
        per_provider[provider] = {
            "cells": cells,
            "exact_repeatability": exact / cells,
            "binary_repeatability": binary / cells,
        }
        all_exact += exact
        all_binary += binary
    result = {
        "preselected_packets": args.packets,
        "base_runs": {provider: path.name for provider, path in base_runs.items()},
        "repeat_runs": {provider: path.name for provider, path in repeat_runs.items()},
        "cells": total,
        "overall_exact_repeatability": all_exact / total,
        "overall_binary_repeatability": all_binary / total,
        "per_provider": per_provider,
    }
    output = WORK / "analysis" / "model_panel_repeatability.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
