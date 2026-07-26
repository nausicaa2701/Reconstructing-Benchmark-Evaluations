#!/usr/bin/env python3
"""Assemble the 156-cell human gold set and score the model panel against it.

Gold label for a cell = the two raters' shared label where they agree, and the
third coder's adjudicated label where they do not. This is the reference set
R1 asked for: it lets model-panel accuracy be estimated over all 156 cells
rather than only over the 93 the raters found easy enough to agree on.

Run after a human adjudicator has filled adjudicated_label in
adjudication_form.csv. Refuses to run on an incomplete or invalid form.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[0] / "audit"
ALLOWED = {
    "documented-and-verifiable", "partially-documented",
    "claimed-but-not-verifiable", "not-documented", "not-applicable",
    "access-blocked",
}
R2_CRITERIA = [
    "Input/expected-output schema", "Metric definition",
    "Grading rules & tie-breaking", "Predictions->aggregate-score mapping",
    "Evaluator implementation available",
]
R2_PASS = {"documented-and-verifiable", "partially-documented", "not-applicable"}
KEYS = ["benchmark", "criterion"]


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [float(centre - half), float(centre + half)]


def load_raters():
    frames = []
    for coder in ("A", "B"):
        f = pd.read_csv(HERE / "assignments" / f"coder_{coder}.csv", keep_default_na=False)
        frames.append(f[KEYS + ["label"]].rename(columns={"label": f"label_{coder}"}))
    return frames[0].merge(frames[1], on=KEYS, validate="one_to_one")


def load_model():
    wide = pd.read_csv(AUDIT / "adjudicated" / "r2_final_labels.csv", keep_default_na=False)
    criteria = [c for c in wide.columns
                if c not in ("benchmark", "category", "R2_reconstructable", "n_ok_of_5")]
    return wide.melt(id_vars="benchmark", value_vars=criteria,
                     var_name="criterion", value_name="label_M")


def load_adjudication():
    path = HERE / "adjudication_form.csv"
    if not path.exists():
        raise SystemExit("adjudication_form.csv missing; run build_adjudication_packet.py")
    adj = pd.read_csv(path, keep_default_na=False)
    blank = adj[adj.adjudicated_label.str.strip() == ""]
    if len(blank):
        raise SystemExit(
            f"{len(blank)}/{len(adj)} items still unadjudicated "
            f"(first: {blank.iloc[0].item_id}). The gold set needs all 63.")
    bad = set(adj.adjudicated_label) - ALLOWED
    if bad:
        raise SystemExit(f"invalid adjudicated labels: {sorted(bad)}")
    if (adj.adjudication_pointer.str.strip() == "").any():
        raise SystemExit("every adjudicated cell needs an evidence pointer")
    return adj[KEYS + ["adjudicated_label"]]


def main():
    merged = load_raters().merge(load_model(), on=KEYS, how="left", validate="one_to_one")
    adj = load_adjudication()
    merged = merged.merge(adj, on=KEYS, how="left")
    agree = merged.label_A == merged.label_B
    merged["gold"] = np.where(agree, merged.label_A, merged.adjudicated_label.fillna(""))
    if (merged.gold == "").any():
        raise SystemExit("some disagreed cells have no adjudicated label")

    n = len(merged)
    exact = int((merged.label_M == merged.gold).sum())
    binary = int((merged.label_M.isin(R2_PASS) == merged.gold.isin(R2_PASS)).sum())
    out = {
        "cells": n,
        "gold_from_rater_agreement": int(agree.sum()),
        "gold_from_adjudication": int((~agree).sum()),
        "model_exact_accuracy": exact / n,
        "model_exact_accuracy_ci95": wilson(exact, n),
        "model_binary_accuracy": binary / n,
        "model_binary_accuracy_ci95": wilson(binary, n),
    }

    # Per-label recall and precision against the full gold set.
    per_label = {}
    for label in sorted(set(merged.gold)):
        g = merged[merged.gold == label]
        m = merged[merged.label_M == label]
        per_label[label] = {
            "gold_n": int(len(g)),
            "recall": float((g.label_M == label).mean()),
            "predicted_n": int(len(m)),
            "precision": float((m.gold == label).mean()) if len(m) else None,
        }
    out["per_label"] = per_label

    # How much the easy-cell restriction had inflated the estimate.
    easy = merged[agree]
    out["model_exact_accuracy_on_agreed_cells_only"] = float(
        (easy.label_M == easy.gold).mean())
    hard = merged[~agree]
    out["model_exact_accuracy_on_adjudicated_cells_only"] = float(
        (hard.label_M == hard.gold).mean())

    # Corpus R2 recomputed under the human gold set.
    primary = merged[merged.criterion.isin(R2_CRITERIA)]
    gold_r2 = primary.assign(ok=primary.gold.isin(R2_PASS)).groupby("benchmark").ok.all()
    model_r2 = primary.assign(ok=primary.label_M.isin(R2_PASS)).groupby("benchmark").ok.all()
    out["R2_under_human_gold"] = int(gold_r2.sum())
    out["R2_under_model_panel"] = int(model_r2.sum())
    out["R2_benchmark_level_agreement"] = float((gold_r2 == model_r2).mean())
    out["benchmarks"] = int(len(gold_r2))

    pd.crosstab(merged.gold, merged.label_M).to_csv(HERE / "model_vs_gold_confusion.csv")
    merged[KEYS + ["label_A", "label_B", "gold", "label_M"]].to_csv(
        HERE / "human_gold_set.csv", index=False)
    (HERE / "gold_set_stats.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
