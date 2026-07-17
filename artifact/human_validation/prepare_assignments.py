#!/usr/bin/env python3
"""Create independently ordered R2 assignment sheets without model labels."""
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifact"
OUT = Path(__file__).resolve().parent / "assignments"
CRITERIA = [
    "Input/expected-output schema",
    "Metric definition",
    "Grading rules & tie-breaking",
    "Predictions->aggregate-score mapping",
    "Evaluator implementation available",
    "Sample predictions / trajectories",
]


def write_assignment(coder, seed, benchmarks, bundles):
    rows = [(benchmark, criterion) for benchmark in benchmarks for criterion in CRITERIA]
    random.Random(seed).shuffle(rows)
    path = OUT / f"coder_{coder}.csv"
    if path.exists():
        with path.open(newline="", encoding="utf-8") as existing:
            if any(row.get("label", "").strip() for row in csv.DictReader(existing)):
                raise SystemExit(f"refusing to overwrite completed labels in {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        fields = ["assignment_id", "benchmark", "criterion", "frozen_commit",
                  "evidence_bundle", "label", "evidence_pointer", "evidence_note"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, (benchmark, criterion) in enumerate(rows, 1):
            writer.writerow({
                "assignment_id": f"H{coder}-{index:03d}",
                "benchmark": benchmark,
                "criterion": criterion,
                "frozen_commit": bundles[benchmark]["commit"],
                "evidence_bundle": "artifact/audit/evidence/r2_evidence_bundles.json",
                "label": "",
                "evidence_pointer": "",
                "evidence_note": "",
            })
    return path


def main():
    bundles = json.loads((ARTIFACT / "audit/evidence/r2_evidence_bundles.json").read_text())
    benchmarks = sorted(bundles)
    if len(benchmarks) != 26:
        raise SystemExit(f"expected 26 evidence bundles, found {len(benchmarks)}")
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [write_assignment("A", 1729, benchmarks, bundles),
             write_assignment("B", 7919, benchmarks, bundles)]
    print("wrote " + ", ".join(str(path.relative_to(ROOT)) for path in paths))


if __name__ == "__main__":
    main()
