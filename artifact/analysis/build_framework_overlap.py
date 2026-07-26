#!/usr/bin/env python3
"""Scope-coverage overlap between this instrument and the closest frameworks.

For every blocker instance actually observed in the frozen 26-release cohort
(R2 criterion failures plus first-pass execution failures), we ask whether the
blocker falls inside the published reporting scope of each comparison
framework.  This is a coverage analysis over *our* observations, not a re-run
of the other instruments; the mapping and its justification per blocker class
live in artifact/data/framework_scope_map.csv and are auditable independently
of the counts produced here.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "artifact"
R2_CRITERIA = [
    "Input/expected-output schema",
    "Metric definition",
    "Evaluator implementation available",
    "Grading rules & tie-breaking",
    "Predictions->aggregate-score mapping",
]
PASS = {"documented-and-verifiable", "partially-documented", "not-applicable"}
EXEC_BLOCKERS = {
    "credential-or-service-blocked",
    "dependency-or-environment-failure",
    "missing-required-data",
}
FRAMEWORKS = ["BetterBench", "BenchmarkCards", "ReproEvalCard", "Rollout Cards",
              "Auto Benchmark Audit"]
SHORT = {"BetterBench": "BetterBench", "BenchmarkCards": "B.Cards",
         "ReproEvalCard": "ReproEvalCard", "Rollout Cards": "Rollout",
         "Auto Benchmark Audit": "ABA"}


def observed_blockers() -> pd.DataFrame:
    panel = pd.read_csv(A / "audit/model_panel_v1/analysis/aggregated_model_judgments.csv")
    r2 = panel[panel.criterion.isin(R2_CRITERIA)]
    rows = [
        {"benchmark": row.benchmark, "blocker": row.criterion, "kind": "R2"}
        for row in r2.itertuples(index=False)
        if row.aggregated_label not in PASS
    ]
    master = pd.read_csv(A / "analysis/master_outcomes.csv")
    rows += [
        {"benchmark": row.benchmark, "blocker": row.first_pass_label, "kind": "E3"}
        for row in master.itertuples(index=False)
        if row.first_pass_label in EXEC_BLOCKERS
    ]
    return pd.DataFrame(rows)


def main() -> None:
    blockers = observed_blockers()
    scope = pd.read_csv(A / "data/framework_scope_map.csv")
    missing = set(blockers.blocker) - set(scope.blocker)
    if missing:
        raise SystemExit(f"unmapped blocker classes: {sorted(missing)}")

    merged = blockers.merge(scope, on="blocker", how="left")
    merged.to_csv(A / "analysis/framework_overlap_instances.csv", index=False,
                  lineterminator="\n")

    total = len(blockers)
    summary = []
    for framework in FRAMEWORKS:
        sub = merged[merged.framework == framework]
        counts = sub.covered.value_counts()
        full = int(counts.get("yes", 0))
        part = int(counts.get("partial", 0))
        none = int(counts.get("no", 0))
        summary.append({
            "framework": framework, "n_blocker_instances": total,
            "in_scope": full, "partial_scope": part, "out_of_scope": none,
            "out_of_scope_pct": round(100 * none / total, 1),
        })
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(A / "analysis/framework_overlap_summary.csv", index=False,
                      lineterminator="\n")

    lines = [
        "\\begin{table}[t]", "\\centering",
        "\\caption{Scope-coverage overlap on the blocker instances actually",
        "observed in the frozen 26-release cohort ($n$ blocker instances:",
        f"{total}). For each instance we ask whether the blocker class lies",
        "inside the published reporting scope of the comparison framework;",
        "cells and justifications are released in",
        "\\texttt{framework\\_scope\\_map.csv}. This is a coverage comparison over",
        "our observations, not a re-execution of the other instruments.}",
        "\\label{tab:overlap}", "\\begin{tabular}{lrrr}", "\\toprule",
        "Framework & In scope & Partial & Out of scope \\\\", "\\midrule",
    ]
    for row in summary_df.itertuples(index=False):
        lines.append(
            f"{SHORT[row.framework]} & {row.in_scope} & {row.partial_scope} & "
            f"{row.out_of_scope} ({row.out_of_scope_pct}\\%) \\\\")
    lines += [
        "\\bottomrule", "\\end{tabular}", "\\end{table}",
    ]
    # Our own instrument is deliberately omitted: the blocker classes are
    # defined by this instrument, so its coverage is 45/45 by construction and
    # carries no information.
    (A / "tables/table4_framework_overlap.tex").write_text("\n".join(lines) + "\n")

    print(json.dumps({"n_blocker_instances": total,
                      "by_kind": blockers.kind.value_counts().to_dict(),
                      "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
