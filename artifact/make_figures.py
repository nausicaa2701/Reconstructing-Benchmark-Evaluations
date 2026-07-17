#!/usr/bin/env python3
"""
Regenerate the data-driven main-paper figures from the frozen analysis dataset.
Plain matplotlib (no external style dependency) so a fresh clone can run it.

    python artifact/make_figures.py            # writes *_repro.png into figures/

These are faithful regenerations of the quantitative figures from
analysis/master_outcomes.csv + analysis/phase6_stats.json. The styled paper
versions (identical data) are the committed fig_*.png / .pdf. Raster output is
not byte-reproducible across matplotlib/font versions, so figures are verified
by data content, not file hash.
"""
import json, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "artifact")
FIG = os.path.join(A, "figures")

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0, 0.0)
    p = k/n; d = 1+z*z/n
    c = (p+z*z/(2*n))/d; h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return p, max(0, c-h), min(1, c+h)

def main():
    df = pd.read_csv(os.path.join(A, "analysis", "master_outcomes.csv"))
    N = len(df)

    # Fig A: screening outcome plus conditional audit endpoints.
    rows = [("Official repository resolved", 30, 35),
            ("R2 Reconstructable (model-coded)", int(df.R2_reconstructable.sum()), N),
            ("E3 as documented", int(df.E3_first_pass.sum()), N),
            ("E3 after documented repair", int(df.E3_smoke_testable.sum()), N)]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for i, (lab, k, n) in enumerate(rows):
        p, lo, hi = wilson(k, n); y = len(rows)-i
        ax.plot([lo*100, hi*100], [y, y], color="#4C72B0", lw=2, zorder=1)
        ax.scatter([p*100], [y], s=90, color="#4C72B0", zorder=2)
        ax.text(hi*100+2, y, f"{k}/{n}", va="center", fontsize=10)
    ax.set_yticks([len(rows)-i for i in range(len(rows))])
    ax.set_yticklabels([r[0] for r in rows]); ax.set_xlim(0, 112)
    ax.set_xlabel("Percent of releases (95% Wilson CI)")
    ax.set_title("Screening and conditional audit outcomes")
    ax.grid(axis="x", ls=":", alpha=.4); fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_endpoints_forest_repro.png"), dpi=150); plt.close(fig)

    # Fig B: E3 by category
    g = df.groupby("category")
    cats = sorted(g.groups); e3 = [int(g.get_group(c).E3_smoke_testable.sum()) for c in cats]
    ns = [len(g.get_group(c)) for c in cats]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    y = np.arange(len(cats))
    ax.barh(y, ns, color="#DDDDDD", label="not E3")
    ax.barh(y, e3, color="#55A868", label="E3")
    for i, (k, n) in enumerate(zip(e3, ns)): ax.text(n+.1, i, f"{k}/{n}", va="center", fontsize=10)
    ax.set_yticks(y); ax.set_yticklabels(cats); ax.set_xlabel("Releases reaching E3")
    ax.set_title("E3 by benchmark category"); ax.legend(loc="lower right"); fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_e3_by_category_repro.png"), dpi=150); plt.close(fig)

    # Fig C: deterministic three-provider aggregate for the six coded criteria.
    panel = pd.read_csv(os.path.join(
        A, "audit", "model_panel_v1", "analysis", "aggregated_model_judgments.csv"
    ))
    criteria = [
        "Input/expected-output schema", "Metric definition",
        "Evaluator implementation available", "Grading rules & tie-breaking",
        "Predictions->aggregate-score mapping", "Sample predictions / trajectories",
    ]
    short = ["I/O schema", "Metric", "Evaluator", "Grading", "Pred.→score", "Samples"]
    labels = [
        "not-documented", "access-blocked", "claimed-but-not-verifiable",
        "partially-documented", "documented-and-verifiable", "not-applicable",
    ]
    colors = ["#B23A48", "#7A5195", "#D97941", "#E9C46A", "#2A9D8F", "#6C757D"]
    label_to_int = {label: i for i, label in enumerate(labels)}
    pivot = panel.pivot(index="benchmark", columns="criterion", values="aggregated_label")
    pivot = pivot.loc[sorted(pivot.index), criteria]
    matrix = pivot.apply(lambda column: column.map(label_to_int)).to_numpy()
    fig, ax = plt.subplots(figsize=(5.3, 7.0))
    ax.imshow(matrix, aspect="auto", cmap=ListedColormap(colors), vmin=-.5, vmax=5.5)
    ax.set_xticks(range(len(short)), short, rotation=38, ha="right", fontsize=8)
    ax.set_yticks(range(len(pivot.index)), pivot.index, fontsize=7)
    ax.axvline(4.5, color="#222222", linestyle="--", linewidth=1)
    ax.set_xticks(np.arange(-.5, len(short), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(pivot.index), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=.55)
    ax.tick_params(which="minor", bottom=False, left=False)
    legend_labels = ["Missing", "Blocked", "Claimed", "Partial", "Verifiable", "N/A"]
    ax.legend(
        handles=[Patch(facecolor=color, label=label) for color, label in zip(colors, legend_labels)],
        loc="upper center", bbox_to_anchor=(.5, -0.105), ncol=3, frameon=False, fontsize=7,
    )
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_r2_labels.png"), dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "fig_r2_labels.pdf"), bbox_inches="tight")
    plt.close(fig)

    # Fig D: blocker counts from the panel aggregate and frozen execution outcomes.
    stats = json.load(open(os.path.join(A, "analysis", "phase6_stats.json")))
    r2_blocks = stats["RQ5_failure_patterns"]["R2_blocking_criteria"]
    e3_blocks = stats["RQ5_failure_patterns"]["E3_blocker_taxonomy"]
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.5))
    for ax, values, title, color in [
        (axes[0], r2_blocks, "R2 documentation blockers", "#B23A48"),
        (axes[1], e3_blocks, "First-pass execution blockers", "#457B9D"),
    ]:
        items = sorted(values.items(), key=lambda item: item[1])
        names = [name.replace("Predictions->aggregate-score mapping", "Predictions→score mapping")
                 .replace("Evaluator implementation available", "Evaluator implementation")
                 .replace("credential-or-service-blocked", "Credentials/services")
                 .replace("dependency-or-environment-failure", "Dependencies/environment")
                 .replace("missing-required-data", "Missing required data")
                 .replace("not-applicable", "Not applicable") for name, _ in items]
        counts = [value for _, value in items]
        y = np.arange(len(items))
        ax.barh(y, counts, color=color)
        ax.set_yticks(y, names, fontsize=7)
        ax.set_xlim(0, max(counts) + 1.5)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="x", linestyle=":", alpha=.35)
        for index, count in enumerate(counts):
            ax.text(count + .15, index, str(count), va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_failure_patterns.png"), dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "fig_failure_patterns.pdf"), bbox_inches="tight")
    plt.close(fig)

    print("regenerated: endpoint/category checks and panel R2/failure figures")
    print(f"E3 first-pass = {int(df.E3_first_pass.sum())}/{N}; "
          f"after repair = {int(df.E3_smoke_testable.sum())}/{N}; "
          f"R2 = {int(df.R2_reconstructable.sum())}/{N}")

if __name__ == "__main__":
    main()
