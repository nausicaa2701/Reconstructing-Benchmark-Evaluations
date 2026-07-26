#!/usr/bin/env python3
"""Validate completed human labels and compute benchmark-level reliability."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ALLOWED = {
    "documented-and-verifiable", "partially-documented",
    "claimed-but-not-verifiable", "not-documented", "not-applicable",
    "access-blocked",
}
R2_CRITERIA = {
    "Input/expected-output schema", "Metric definition",
    "Grading rules & tie-breaking", "Predictions->aggregate-score mapping",
    "Evaluator implementation available",
}
R2_PASS = {"documented-and-verifiable", "partially-documented", "not-applicable"}


def nominal_alpha(a, b):
    values = pd.concat([a, b], ignore_index=True)
    frequencies = values.value_counts().to_numpy(dtype=float)
    expected = 1.0 - np.sum(frequencies * (frequencies - 1)) / (len(values) * (len(values) - 1))
    observed = np.mean(a.to_numpy() != b.to_numpy())
    return 1.0 if expected == 0 else 1.0 - observed / expected


def load(coder):
    path = HERE / "assignments" / f"coder_{coder}.csv"
    frame = pd.read_csv(path, keep_default_na=False)
    if len(frame) != 156:
        raise SystemExit(f"{path}: expected 156 rows, found {len(frame)}")
    invalid = set(frame.label) - ALLOWED
    if invalid:
        raise SystemExit(f"{path}: blank or invalid labels: {sorted(invalid)}")
    if (frame.evidence_pointer.str.strip() == "").any():
        raise SystemExit(f"{path}: every row needs an evidence_pointer")
    return frame


def r2_count(frame):
    primary = frame[frame.criterion.isin(R2_CRITERIA)]
    status = primary.assign(ok=primary.label.isin(R2_PASS)).groupby("benchmark").ok.all()
    return int(status.sum())


def main():
    a, b = load("A"), load("B")
    keys = ["benchmark", "criterion", "frozen_commit"]
    merged = a.merge(b, on=keys, suffixes=("_A", "_B"), validate="one_to_one")
    if len(merged) != 156:
        raise SystemExit("coder files do not cover identical benchmark-criterion cells")
    agreement = float((merged.label_A == merged.label_B).mean())
    alpha = nominal_alpha(merged.label_A, merged.label_B)
    rng = np.random.default_rng(42)
    benchmarks = merged.benchmark.unique()
    boot = []
    for _ in range(10000):
        sampled = rng.choice(benchmarks, size=len(benchmarks), replace=True)
        cells = pd.concat([merged[merged.benchmark == name] for name in sampled], ignore_index=True)
        boot.append(nominal_alpha(cells.label_A, cells.label_B))
    disagreements = merged[merged.label_A != merged.label_B].copy()
    disagreements["adjudicated_label"] = ""
    disagreements["adjudication_pointer"] = ""
    disagreements["adjudication_note"] = ""
    disagreements.to_csv(HERE / "human_disagreements_for_adjudication.csv", index=False)
    result = {
        "cells": len(merged),
        "agreement": agreement,
        "krippendorff_alpha_nominal": alpha,
        "benchmark_bootstrap_ci95": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
        "disagreements": len(disagreements),
        "disagreement_rate": len(disagreements) / len(merged),
        "coder_A_R2_permissive": r2_count(a),
        "coder_B_R2_permissive": r2_count(b),
        "passes_alpha_gate": bool(alpha >= 0.80),
        "passes_adjudication_rate_gate": bool(len(disagreements) / len(merged) < 0.15),
    }
    (HERE / "human_reliability_stats.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
