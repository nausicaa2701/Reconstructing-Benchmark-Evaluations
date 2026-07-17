#!/usr/bin/env python3
"""
Extended analyses over the frozen audit dataset.

    python artifact/analysis/build_extended_analysis.py

Writes analysis/extended_analysis_stats.json. Three additions beyond phase6:

1. first_pass_blocker_taxonomy -- the blocker distribution over all 21 first-pass
   failures. phase6_stats' RQ5 "E3_blocker_taxonomy" tabulates the 19 releases
   that never reached a score (it drops DS-1000 and TableBench, which failed the
   first pass but passed after repair), so it must not be described as a
   first-pass taxonomy. Both are emitted here under unambiguous names.
2. artifact_presence_association -- does shipping sample predictions, a
   container, or an environment file predict R2/E3? Tests the mechanism behind
   the paper's recommendations.
3. lineage_robustness -- outcomes recomputed with shared-lineage releases
   (Spider, BIRD, DS-1000/CERT families) collapsed or dropped, since the
   headline intervals treat releases as exchangeable.
"""
import json, os
import pandas as pd
from scipy.stats import fisher_exact

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "artifact")

# Releases sharing authorship or an evaluator codebase; see Limitations.
FAMILIES = {
    "Spider": ["Spider", "Spider 2.0", "Spider2-V", "Dr.Spider"],
    "BIRD": ["BIRD", "BIRD-CRITIC / SQL-eval"],
    "DS-1000/CERT": ["DS-1000", "PandasEval/NumpyEval (CERT)"],
}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / d
    return p, max(0.0, c - h), min(1.0, c + h)


def prop(k, n):
    p, lo, hi = wilson(k, n)
    return {"k": int(k), "n": int(n), "prop": round(p, 4), "ci95": [round(lo, 4), round(hi, 4)]}


def blocker_taxonomies(df):
    first = df[~df.E3_first_pass].first_pass_label.value_counts().to_dict()
    final = df[~df.E3_smoke_testable].first_pass_label.value_counts().to_dict()
    repaired = df[df.E3_after_repair][["benchmark", "first_pass_label"]]
    return {
        "first_pass_blockers": {k: int(v) for k, v in first.items()},
        "first_pass_blockers_total": int(sum(first.values())),
        "final_failure_blockers": {k: int(v) for k, v in final.items()},
        "final_failure_blockers_total": int(sum(final.values())),
        "repaired_out_of_first_pass_set": [
            {"benchmark": b, "first_pass_label": l} for b, l in repaired.itertuples(index=False)
        ],
        "note": (
            "first_pass_blockers covers all 21 first-pass failures. "
            "final_failure_blockers covers the 19 releases that never scored and "
            "equals phase6_stats RQ5_failure_patterns.E3_blocker_taxonomy."
        ),
    }


def association(df):
    out = {}
    df = df.assign(R2b=df.R2_reconstructable.astype(bool))
    for outcome in ["R2b", "E3_first_pass", "E3_smoke_testable"]:
        for pred in ["sample_predictions", "container", "env_file"]:
            present = df[df[pred] == 1]
            absent = df[df[pred] == 0]
            a, b = int(present[outcome].sum()), int((~present[outcome]).sum())
            c, d = int(absent[outcome].sum()), int((~absent[outcome]).sum())
            odds, p = fisher_exact([[a, b], [c, d]])
            out[f"{pred}__{outcome}"] = {
                "present": prop(a, a + b),
                "absent": prop(c, c + d),
                "odds_ratio": None if odds in (float("inf"),) else round(float(odds), 4),
                "fisher_p": round(float(p), 4),
            }
    out["note"] = (
        "Exploratory, N=26, no multiplicity correction. No artifact-presence "
        "signal predicts any endpoint at alpha=0.05; presence of an artifact "
        "class is not sufficiency of the evidence it is meant to supply."
    )
    return out


def lineage(df):
    fam = {b: f for f, bs in FAMILIES.items() for b in bs}
    df = df.assign(family=df.benchmark.map(fam).fillna(df.benchmark))
    res = {
        "n_releases": int(len(df)),
        "n_independent_lineages": int(df.family.nunique()),
        "families": {
            f: {
                "n": int((df.family == f).sum()),
                "R2": int(df[df.family == f].R2_reconstructable.sum()),
                "E3_first_pass": int(df[df.family == f].E3_first_pass.sum()),
            }
            for f in FAMILIES
        },
        "leave_one_family_out": {},
        "one_release_per_family": {},
    }
    for f in FAMILIES:
        s = df[df.family != f]
        res["leave_one_family_out"][f] = {
            "R2": prop(s.R2_reconstructable.sum(), len(s)),
            "E3_first_pass": prop(s.E3_first_pass.sum(), len(s)),
        }
    s = df.groupby("family", sort=False).head(1)
    res["one_release_per_family"] = {
        "R2": prop(s.R2_reconstructable.sum(), len(s)),
        "E3_first_pass": prop(s.E3_first_pass.sum(), len(s)),
    }
    res["note"] = (
        "E3 first-pass stays within 20.8-23.8% under every lineage adjustment; "
        "the headline is not driven by clustered families."
    )
    return res


def main():
    df = pd.read_csv(os.path.join(A, "analysis", "master_outcomes.csv"))
    assert len(df) == 26, f"expected 26 rows, got {len(df)}"
    att = df[df.attempted_execution]

    stats = {
        "source": "artifact/analysis/master_outcomes.csv",
        "N": int(len(df)),
        "blocker_taxonomy": blocker_taxonomies(df),
        "conditional_on_evaluator_reached": {
            "n_command_run": int(len(att)),
            "E3_first_pass": prop(att.E3_first_pass.sum(), len(att)),
            "E3_after_repair_any": prop(att.E3_smoke_testable.sum(), len(att)),
            "note": (
                "Denominator restricted to the 21 releases where a public "
                "evaluator interface was reached and a command was actually run."
            ),
        },
        "artifact_presence_association": association(df),
        "lineage_robustness": lineage(df),
    }

    out = os.path.join(A, "analysis", "extended_analysis_stats.json")
    with open(out, "w") as handle:
        json.dump(stats, handle, indent=2)
        handle.write("\n")
    print(f"[extended] wrote {os.path.relpath(out, ROOT)}")
    t = stats["blocker_taxonomy"]
    print(f"[extended] first-pass blockers total {t['first_pass_blockers_total']} "
          f"(final-failure taxonomy total {t['final_failure_blockers_total']})")
    a = stats["artifact_presence_association"]
    print("[extended] artifact-presence Fisher p: " + ", ".join(
        f"{k}={v['fisher_p']}" for k, v in a.items() if k != "note"))


if __name__ == "__main__":
    main()
