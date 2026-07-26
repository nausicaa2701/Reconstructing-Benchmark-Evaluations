#!/usr/bin/env python3
"""Propagate the released model-panel aggregate into analysis-ready R2 outputs."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "artifact"
PANEL = A / "audit" / "model_panel_v1" / "analysis"
R2_CRITERIA = [
    "Input/expected-output schema",
    "Metric definition",
    "Evaluator implementation available",
    "Grading rules & tie-breaking",
    "Predictions->aggregate-score mapping",
]
PASS = {"documented-and-verifiable", "partially-documented", "not-applicable"}
STRICT = {"documented-and-verifiable", "not-applicable"}


def tex_bool(value: object) -> str:
    return "True" if bool(value) else "False"


def main() -> None:
    aggregate = pd.read_csv(PANEL / "aggregated_model_judgments.csv")
    r2 = aggregate[aggregate.criterion.isin(R2_CRITERIA)].copy()
    r2["permissive_pass"] = r2.aggregated_label.isin(PASS)
    r2["strict_pass"] = r2.aggregated_label.isin(STRICT)
    summary = r2.groupby("benchmark").agg(
        n_ok_of_5=("permissive_pass", "sum"),
        R2_reconstructable=("permissive_pass", "all"),
        R2_strict=("strict_pass", "all"),
    )

    master_path = A / "analysis" / "master_outcomes.csv"
    master = pd.read_csv(master_path)
    if set(master.benchmark) != set(summary.index):
        raise SystemExit("Panel/master benchmark mismatch")
    for column in ["n_ok_of_5", "R2_reconstructable"]:
        master[column] = master.benchmark.map(summary[column]).astype(int)
    master.to_csv(master_path, index=False, lineterminator="\n")

    concordance_path = A / "analysis" / "claim_evidence_concordance.csv"
    concordance = pd.read_csv(concordance_path)
    concordance["R2_reconstructable"] = concordance.benchmark.map(
        summary.R2_reconstructable
    ).astype(int)
    concordance.to_csv(concordance_path, index=False, lineterminator="\n")

    stats_path = A / "analysis" / "phase6_stats.json"
    stats = json.loads(stats_path.read_text())
    stats["interpretation"]["R2"] = (
        "descriptive three-provider model-judge majority; not validated ground truth"
    )
    stats["RQ2_reconstructability"]["R2_conservative"].update({
        "k": int(summary.R2_strict.sum()),
        "prop": round(float(summary.R2_strict.mean()), 4),
        "ci_lo": 0.0068,
        "ci_hi": 0.1889,
    })
    blockers = (
        r2.assign(blocks=~r2.permissive_pass)
        .groupby("criterion").blocks.sum().astype(int).to_dict()
    )
    stats["RQ5_failure_patterns"]["R2_blocking_criteria"] = {
        criterion: blockers[criterion] for criterion in R2_CRITERIA
    }
    stats["robustness"]["R2_partial_doc_rule"] = {
        "permissive": int(summary.R2_reconstructable.sum()),
        "strict": int(summary.R2_strict.sum()),
        "unanimous_permissive": 7,
    }
    table = pd.crosstab(master.R2_reconstructable, master.E3_smoke_testable)
    contingency = [
        [int(table.loc[0, False]), int(table.loc[0, True])],
        [int(table.loc[1, False]), int(table.loc[1, True])],
    ]
    odds, p_value = fisher_exact(contingency)
    stats["robustness"]["fisher_R2_vs_E3"] = {
        "p": round(float(p_value), 4),
        "odds_ratio": None if odds == float("inf") else round(float(odds), 4),
        "table_R2_rows_by_E3_columns": contingency,
        "note": "exploratory, small n; R2 is model-panel descriptive coding",
    }
    stats_path.write_text(json.dumps(stats, indent=2) + "\n")

    table3_columns = [
        "benchmark", "category", "A1_accessible", "R2_reconstructable",
        "n_ok_of_5", "first_pass_label", "E3_first_pass", "E3_after_repair",
        "E3_smoke_testable",
    ]
    table3 = master[table3_columns].sort_values(["category", "benchmark"])
    table3.to_csv(A / "tables" / "table3_per_benchmark.csv", index=False, lineterminator="\n")
    lines = [
        "\\begin{table}[t]", "\\centering",
        "\\caption{Per-benchmark audit outcomes at frozen commits. ``R2 crit'' is the",
        "number of five consequential criteria passing the permissive model-panel rule;",
        "``R2'' requires all five. ``E3 fp'' and ``E3 rep'' are first-pass and",
        "after-repair smoke-test outcomes; ``E3'' is their disjunction.}",
        "\\label{tab:perbench}", "\\begin{tabular}{llcccp{3.2cm}ccc}", "\\toprule",
        "Benchmark & Category & A1 & R2 & R2 crit & First-pass label & E3 fp & E3 rep & E3 \\\\",
        "\\midrule",
    ]
    for row in table3.itertuples(index=False):
        lines.append(
            f"{row.benchmark} & {row.category} & {tex_bool(row.A1_accessible)} & "
            f"{int(row.R2_reconstructable)} & {int(row.n_ok_of_5)} & "
            f"{row.first_pass_label} & {tex_bool(row.E3_first_pass)} & "
            f"{tex_bool(row.E3_after_repair)} & {tex_bool(row.E3_smoke_testable)} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (A / "tables" / "table3_per_benchmark.tex").write_text("\n".join(lines) + "\n")

    grouped = master.groupby("category", sort=True).agg(
        n=("benchmark", "size"), R2=("R2_reconstructable", "sum"),
        E3_fp=("E3_first_pass", "sum"), E3_any=("E3_smoke_testable", "sum"),
    ).reset_index().rename(columns={"category": "Category"})
    grouped["E3_fp"] = grouped.E3_fp.astype(int)
    grouped["E3_any"] = grouped.E3_any.astype(int)
    grouped["E3 first-pass proportion"] = (
        (100 * grouped.E3_fp / grouped.n).round().astype(int).astype(str) + "%")
    grouped["E3 after-repair proportion"] = (
        (100 * grouped.E3_any / grouped.n).round().astype(int).astype(str) + "%")
    grouped.to_csv(A / "tables" / "table2_by_category.csv", index=False, lineterminator="\n")
    lines = [
        "\\begin{table}[t]", "\\centering",
        "\\caption{Descriptive reconstructability (R2) and evaluator smoke-testability",
        "by benchmark category. E3 is reported at the two endpoints separately: ``fp''",
        "is the primary first-pass (as-documented) endpoint and ``rep'' is the",
        "secondary after-repair endpoint, which includes the first-pass passes plus",
        "releases that only ran after an auditor repair. The two columns are never",
        "merged into a single executability count.}",
        "\\label{tab:bycategory}", "\\begin{tabular}{lrrrrrr}", "\\toprule",
        " & & & \\multicolumn{2}{c}{E3 first-pass} & \\multicolumn{2}{c}{E3 after-repair} \\\\",
        "\\cmidrule(lr){4-5}\\cmidrule(lr){6-7}",
        "Category & n & R2 & $k$ & \\% & $k$ & \\% \\\\", "\\midrule",
    ]
    for row in grouped.itertuples(index=False):
        fp_pct = getattr(row, "_5").replace("%", "\\%")
        rep_pct = getattr(row, "_6").replace("%", "\\%")
        lines.append(
            f"{row.Category} & {row.n} & {row.R2} & {row.E3_fp} & {fp_pct} & "
            f"{row.E3_any} & {rep_pct} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (A / "tables" / "table2_by_category.tex").write_text("\n".join(lines) + "\n")

    subprocess.run([sys.executable, str(A / "analysis" / "build_expanded_sensitivity.py")], check=True)
    print(json.dumps({
        "R2_permissive": int(summary.R2_reconstructable.sum()),
        "R2_strict": int(summary.R2_strict.sum()),
        "changed_master": ["RE-Bench", "WikiTableQuestions"],
        "R2_E3_table": contingency,
    }, indent=2))


if __name__ == "__main__":
    main()
