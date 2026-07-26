#!/usr/bin/env python3
"""Lineage-clustered bootstrap intervals for the primary endpoints.

Wilson intervals treat the 26 releases as independent, which the shared
Spider / BIRD / DS-1000-CERT lineages violate. This resamples whole lineages
(the cluster bootstrap) so the interval reflects the 21 independent lineages
rather than 26 exchangeable releases. Wilson is retained in the paper as a
conditional descriptive summary; these are the intervals of record.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FAMILIES = {
    "spider": ["Spider", "Spider 2.0", "Spider2-V", "Dr.Spider"],
    "bird": ["BIRD", "BIRD-CRITIC / SQL-eval"],
    "ds1000-cert": ["DS-1000", "PandasEval/NumpyEval (CERT)"],
}
B = 20000
SEED = 42


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (float(centre - half), float(centre + half))


def cluster_bootstrap(values, clusters, rng, b=B):
    """Percentile bootstrap over resampled clusters, weighting each release
    equally within the resampled corpus (the estimand is the release-level
    proportion, so cluster sizes carry through)."""
    groups = {c: values[clusters == c] for c in pd.unique(clusters)}
    names = np.array(list(groups))
    draws = np.empty(b)
    for i in range(b):
        picked = rng.choice(names, size=len(names), replace=True)
        pooled = np.concatenate([groups[c] for c in picked])
        draws[i] = pooled.mean()
    return draws


def main():
    df = pd.read_csv(HERE / "master_outcomes.csv")
    fam = {b: f for f, bs in FAMILIES.items() for b in bs}
    df = df.assign(family=df.benchmark.map(fam).fillna(df.benchmark))

    endpoints = {
        "R2_permissive": df.R2_reconstructable.astype(float).to_numpy(),
        "E3_first_pass": df.E3_first_pass.astype(bool).astype(float).to_numpy(),
        "E3_after_repair": df.E3_smoke_testable.astype(bool).astype(float).to_numpy()
        if "E3_smoke_testable" in df else None,
    }
    clusters = df.family.to_numpy()
    rng = np.random.default_rng(SEED)

    out = {
        "n_releases": int(len(df)),
        "n_lineages": int(df.family.nunique()),
        "bootstrap_draws": B,
        "seed": SEED,
        "endpoints": {},
    }
    for name, values in endpoints.items():
        if values is None:
            continue
        k, n = int(values.sum()), len(values)
        draws = cluster_bootstrap(values, clusters, rng)
        out["endpoints"][name] = {
            "count": k,
            "n": n,
            "point": k / n,
            "wilson95": list(wilson(k, n)),
            "cluster_bootstrap95": [float(np.percentile(draws, 2.5)),
                                    float(np.percentile(draws, 97.5))],
            "cluster_bootstrap_se": float(draws.std(ddof=1)),
        }
    (HERE / "cluster_bootstrap_ci.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
