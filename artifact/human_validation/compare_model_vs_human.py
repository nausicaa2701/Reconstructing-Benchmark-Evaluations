#!/usr/bin/env python3
"""Human-panel diagnostics and model-vs-human comparison.

Run after ingest_rater_forms.py and analyze_labels.py. Produces:
  human_diagnostics.json          per-criterion agreement, boundary confusion
  model_vs_human_confusion.csv    model final label x human label counts
"""
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[0] / "audit"
R2_CRITERIA = [
    "Input/expected-output schema", "Metric definition",
    "Grading rules & tie-breaking", "Predictions->aggregate-score mapping",
    "Evaluator implementation available",
]
R2_PASS = {"documented-and-verifiable", "partially-documented", "not-applicable"}
KEYS = ["benchmark", "criterion"]


def nominal_alpha(a, b):
    values = pd.concat([a, b], ignore_index=True)
    freq = values.value_counts().to_numpy(dtype=float)
    expected = 1.0 - np.sum(freq * (freq - 1)) / (len(values) * (len(values) - 1))
    observed = np.mean(np.asarray(a) != np.asarray(b))
    return 1.0 if expected == 0 else 1.0 - observed / expected


def load_human(coder):
    frame = pd.read_csv(HERE / "assignments" / f"coder_{coder}.csv", keep_default_na=False)
    return frame[KEYS + ["label"]].rename(columns={"label": f"label_{coder}"})


def load_model():
    wide = pd.read_csv(AUDIT / "adjudicated" / "r2_final_labels.csv", keep_default_na=False)
    criteria = [c for c in wide.columns if c not in ("benchmark", "category", "R2_reconstructable", "n_ok_of_5")]
    long = wide.melt(id_vars="benchmark", value_vars=criteria,
                     var_name="criterion", value_name="label_M")
    return long


def r2_from_long(frame, column):
    primary = frame[frame.criterion.isin(R2_CRITERIA)]
    ok = primary.assign(ok=primary[column].isin(R2_PASS)).groupby("benchmark").ok.all()
    return int(ok.sum()), int(len(ok))


def main():
    merged = load_human("A").merge(load_human("B"), on=KEYS, validate="one_to_one")
    merged = merged.merge(load_model(), on=KEYS, how="left", validate="one_to_one")
    if merged.label_M.eq("").any() or merged.label_M.isna().any():
        raise SystemExit("model labels missing for some cells")

    out = {"cells": len(merged)}

    # 1. Human-human agreement at the permissive binary boundary.
    bin_a = merged.label_A.isin(R2_PASS)
    bin_b = merged.label_B.isin(R2_PASS)
    out["human_binary_agreement"] = float((bin_a == bin_b).mean())
    out["human_binary_alpha"] = float(nominal_alpha(bin_a.astype(str), bin_b.astype(str)))

    # 2. Where the disagreement sits, per criterion.
    per_criterion = {}
    for criterion, block in merged.groupby("criterion"):
        per_criterion[criterion] = {
            "n": int(len(block)),
            "exact_agreement": float((block.label_A == block.label_B).mean()),
            "binary_agreement": float(
                (block.label_A.isin(R2_PASS) == block.label_B.isin(R2_PASS)).mean()),
        }
    out["per_criterion"] = per_criterion

    # 3. Which label boundaries generate the disagreements.
    pairs = Counter()
    for a, b in zip(merged.label_A, merged.label_B):
        if a != b:
            pairs[" | ".join(sorted((a, b)))] += 1
    out["disagreement_boundaries"] = dict(pairs.most_common())
    total = sum(pairs.values())
    out["disagreements"] = total
    partial_share = sum(v for k, v in pairs.items() if "partially-documented" in k)
    out["share_of_disagreements_touching_partially_documented"] = partial_share / total

    # 4. Benchmark-level R2 under each coder and under the model panel.
    r2 = {}
    for name, column in (("coder_A", "label_A"), ("coder_B", "label_B"), ("model_panel", "label_M")):
        count, denom = r2_from_long(merged, column)
        r2[name] = {"permissive_R2": count, "of": denom}
    # Human consensus: pass only where both coders pass every criterion.
    consensus = merged.assign(ok=merged.label_A.isin(R2_PASS) & merged.label_B.isin(R2_PASS))
    strictboth = consensus[consensus.criterion.isin(R2_CRITERIA)].groupby("benchmark").ok.all()
    r2["human_both_agree_pass"] = {"permissive_R2": int(strictboth.sum()), "of": int(len(strictboth))}
    either = merged.assign(ok=merged.label_A.isin(R2_PASS) | merged.label_B.isin(R2_PASS))
    eitherb = either[either.criterion.isin(R2_CRITERIA)].groupby("benchmark").ok.all()
    r2["human_either_passes"] = {"permissive_R2": int(eitherb.sum()), "of": int(len(eitherb))}
    out["R2_counts"] = r2

    # 5. Model vs each human coder.
    for coder in ("A", "B"):
        column = f"label_{coder}"
        out[f"model_vs_{coder}"] = {
            "exact_agreement": float((merged.label_M == merged[column]).mean()),
            "binary_agreement": float(
                (merged.label_M.isin(R2_PASS) == merged[column].isin(R2_PASS)).mean()),
            "alpha_nominal": float(nominal_alpha(merged.label_M, merged[column])),
        }
    # Model vs the cells where the two humans already agree: the only cells
    # where a human reference exists without adjudication.
    stable = merged[merged.label_A == merged.label_B]
    out["human_stable_cells"] = int(len(stable))
    out["model_accuracy_on_human_stable_cells"] = float((stable.label_M == stable.label_A).mean())
    out["model_binary_accuracy_on_human_stable_cells"] = float(
        (stable.label_M.isin(R2_PASS) == stable.label_A.isin(R2_PASS)).mean())
    per_label = {}
    for label, block in stable.groupby("label_A"):
        per_label[label] = {"n": int(len(block)),
                            "model_recall": float((block.label_M == label).mean())}
    out["model_recall_on_human_stable_cells_by_label"] = per_label

    confusion = pd.crosstab(stable.label_A, stable.label_M)
    confusion.to_csv(HERE / "model_vs_human_confusion.csv")

    (HERE / "human_diagnostics.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
