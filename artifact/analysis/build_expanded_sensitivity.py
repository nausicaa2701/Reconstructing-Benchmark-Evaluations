#!/usr/bin/env python3
"""Build the 30-release post-freeze expansion sensitivity without changing the primary cohort."""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifact"


def main():
    primary = pd.read_csv(ARTIFACT / "analysis" / "master_outcomes.csv")
    coding = json.loads((ARTIFACT / "corpus" / "rescreened_release_coding.json").read_text())
    rows = []
    for release in coding["releases"]:
        criteria = release["criteria"]
        pass_labels = {"documented-and-verifiable", "partially-documented", "not-applicable"}
        primary_names = [
            "Input/expected-output schema", "Metric definition",
            "Grading rules & tie-breaking", "Predictions->aggregate-score mapping",
            "Evaluator implementation available",
        ]
        n_ok = sum(criteria[name]["label"] in pass_labels for name in primary_names)
        e3 = release["e3"]
        flags = release["artifact_flags"]
        rows.append({
            "benchmark": release["benchmark"], "category": release["category"],
            "arxiv_id": release["arxiv_id"], "frozen_commit": release["frozen_commit"],
            "A0_described": True, "A1_accessible": True,
            "R2_reconstructable": int(n_ok == 5), "n_ok_of_5": n_ok,
            "attempted_execution": e3["attempted"], "first_pass_label": e3["first_pass_label"],
            "E3_first_pass": e3["first_pass"], "E3_after_repair": e3["after_repair"],
            "E3_smoke_testable": e3["first_pass"] or e3["after_repair"],
            "evaluator": flags["evaluator"], "dataset": flags["dataset"],
            "sample_predictions": flags["sample_predictions"], "env_file": flags["environment"],
            "container": flags["container"], "license": flags["license"],
            "analysis_set": "post-freeze-extension",
        })
    primary = primary.assign(analysis_set="primary-frozen")
    expanded = pd.concat([primary, pd.DataFrame(rows)], ignore_index=True)
    expanded.to_csv(ARTIFACT / "analysis" / "expanded_sensitivity_outcomes.csv", index=False, lineterminator="\n")
    stats = {
        "audit_date": coding["audit_date"], "primary_n": len(primary), "extension_n": len(rows),
        "expanded_n": len(expanded), "repository_resolution": {"k": 30, "n": 35},
        "R2_permissive": {"k": int(expanded.R2_reconstructable.sum()), "n": len(expanded)},
        "E3_first_pass": {"k": int(expanded.E3_first_pass.sum()), "n": len(expanded)},
        "E3_after_repair": {"k": int(expanded.E3_smoke_testable.sum()), "n": len(expanded)},
        "interpretation": "Post-freeze expansion sensitivity; primary estimates remain the pre-specified 26-release cohort."
    }
    (ARTIFACT / "analysis" / "expanded_sensitivity_stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
