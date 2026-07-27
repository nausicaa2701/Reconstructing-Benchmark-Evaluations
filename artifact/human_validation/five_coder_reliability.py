#!/usr/bin/env python3
"""Reliability across all five independent coders, and adjudicator diagnostics.

Two questions this answers without any new data collection:

1. Is the codability failure a property of our two human raters, or of the
   codebook? We hold labels from five coders who never saw each other's work:
   three model judges from different providers and two blinded human raters.
   Pairwise agreement over all ten pairs, and a five-coder Krippendorff alpha,
   test whether any pair of coders reaches the pre-registered gate.

2. Is the single adjudicator a hidden point of failure? We cannot measure a
   lone adjudicator against a second one, but we can test the two failure modes
   that would matter: positional bias (did they systematically favour whichever
   rater was shown first, given that presentation order was randomised?) and
   deference (did they only ever pick one of the two offered labels, or did the
   evidence sometimes support a third?).
"""
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[0] / "audit"
KEYS = ["benchmark", "criterion"]
R2_PASS = {"documented-and-verifiable", "partially-documented", "not-applicable"}
GATE = 0.80


def nominal_alpha_pair(a, b):
    values = pd.concat([pd.Series(a), pd.Series(b)], ignore_index=True)
    freq = values.value_counts().to_numpy(dtype=float)
    expected = 1.0 - np.sum(freq * (freq - 1)) / (len(values) * (len(values) - 1))
    observed = np.mean(np.asarray(a) != np.asarray(b))
    return 1.0 if expected == 0 else 1.0 - observed / expected


def nominal_alpha_many(frame):
    """Krippendorff's nominal alpha for m coders x n units, no missing data."""
    units = frame.to_numpy()
    n_units, m = units.shape
    labels = sorted({v for row in units for v in row})
    index = {lab: i for i, lab in enumerate(labels)}
    counts = np.zeros((n_units, len(labels)))
    for u, row in enumerate(units):
        for v in row:
            counts[u, index[v]] += 1
    n_u = counts.sum(axis=1)
    # observed disagreement
    do_num = sum((counts[u] * (n_u[u] - counts[u])).sum() / (n_u[u] - 1)
                 for u in range(n_units))
    n_total = n_u.sum()
    do = do_num / n_total
    # expected disagreement
    col = counts.sum(axis=0)
    de = (n_total ** 2 - (col ** 2).sum()) / (n_total * (n_total - 1))
    return 1.0 - do / de


def load_coders():
    frames = {}
    for coder in ("A", "B"):
        f = pd.read_csv(HERE / "assignments" / f"coder_{coder}.csv", keep_default_na=False)
        frames[f"human_{coder}"] = f.set_index(KEYS).label
    raw = pd.read_csv(AUDIT / "model_panel_v1" / "analysis" / "raw_model_judgments.csv",
                      keep_default_na=False)
    for provider, block in raw.groupby("provider"):
        frames[f"model_{provider}"] = block.set_index(KEYS).label
    return pd.DataFrame(frames).dropna()


def adjudicator_diagnostics():
    form = pd.read_csv(HERE / "adjudication_form.csv", keep_default_na=False)
    key = json.loads((HERE / "adjudication_key.json").read_text())
    chose = Counter()
    by_rater = Counter()
    for _, row in form.iterrows():
        label = row.adjudicated_label.strip()
        if label == row.option_1_label:
            chose["option_1"] += 1
            by_rater[key[row.item_id]["option_1_is_rater"]] += 1
        elif label == row.option_2_label:
            chose["option_2"] += 1
            by_rater[key[row.item_id]["option_2_is_rater"]] += 1
        else:
            chose["third_label"] += 1
    n = len(form)
    # Binomial two-sided test for positional preference among the cells where a
    # side was chosen; presentation order was randomised, so 0.5 is the null.
    sided = chose["option_1"] + chose["option_2"]
    k = chose["option_1"]
    from math import comb
    tail = sum(comb(sided, i) for i in range(0, min(k, sided - k) + 1)) / 2 ** sided
    p_two_sided = min(1.0, 2 * tail)
    return {
        "n_adjudicated": int(n),
        "chose_option_shown_first": int(chose["option_1"]),
        "chose_option_shown_second": int(chose["option_2"]),
        "positional_binomial_p": float(p_two_sided),
        "chose_a_third_label_neither_rater_gave": int(chose["third_label"]),
        "third_label_rate": float(chose["third_label"] / n),
        "sided_with_rater_A": int(by_rater.get("A", 0)),
        "sided_with_rater_B": int(by_rater.get("B", 0)),
    }


def main():
    coders = load_coders()
    names = list(coders.columns)
    out = {"cells": int(len(coders)), "coders": names}

    pairs = {}
    for x, y in combinations(names, 2):
        pairs[f"{x} vs {y}"] = {
            "exact_agreement": float((coders[x] == coders[y]).mean()),
            "alpha": float(nominal_alpha_pair(coders[x], coders[y])),
            "binary_agreement": float(
                (coders[x].isin(R2_PASS) == coders[y].isin(R2_PASS)).mean()),
        }
    out["pairwise"] = pairs
    alphas = [v["alpha"] for v in pairs.values()]
    out["n_pairs"] = len(pairs)
    out["pairs_reaching_gate"] = int(sum(a >= GATE for a in alphas))
    out["alpha_range"] = [float(min(alphas)), float(max(alphas))]
    out["best_pair"] = max(pairs, key=lambda k: pairs[k]["alpha"])

    out["five_coder_alpha"] = float(nominal_alpha_many(coders))
    binary = coders.apply(lambda c: c.isin(R2_PASS).map({True: "pass", False: "fail"}))
    out["five_coder_alpha_binary"] = float(nominal_alpha_many(binary))

    # Is the failure concentrated in the graded criteria, across all five coders?
    per_criterion = {}
    for criterion, block in coders.groupby(level="criterion"):
        per_criterion[criterion] = float(nominal_alpha_many(block))
    out["five_coder_alpha_by_criterion"] = per_criterion

    # Cross-panel: do human-human pairs differ from model-model pairs?
    def mean_of(pred):
        vals = [v["alpha"] for k, v in pairs.items() if pred(k)]
        return float(np.mean(vals)) if vals else None
    out["mean_alpha_human_human"] = mean_of(lambda k: k.count("human") == 2)
    out["mean_alpha_model_model"] = mean_of(lambda k: k.count("model") == 2)
    out["mean_alpha_cross"] = mean_of(lambda k: k.count("human") == 1)

    out["adjudicator"] = adjudicator_diagnostics()

    (HERE / "five_coder_reliability.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
