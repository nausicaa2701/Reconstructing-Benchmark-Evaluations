#!/usr/bin/env python3
"""
Reproduction interface for:
  "Auditing Public Evaluation Specifications and Scorer Smoke-Testability:
   A Public-Artifact Audit of Foundation-Model Benchmarks for Data Science"
   (KDD 2027 D&B Track)

Usage (from repository root, analysis environment; numpy/scipy/pandas/matplotlib + jsonschema):
    python artifact/reproduce.py --check      # validate schema, recompute stats, verify hashes
    python artifact/reproduce.py --regenerate # also rewrite tables/figures from frozen data

The evaluator SMOKE TESTS are replayed separately (see artifact/execution/README.md);
they involve heterogeneous external artifacts and are not part of this single command.
"""
import argparse, csv, json, os, subprocess, sys, hashlib
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "artifact")

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0, 0.0)
    p = k/n; d = 1+z*z/n
    c = (p+z*z/(2*n))/d; h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return p, max(0, c-h), min(1, c+h)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()

def canonical_json_hash(path):
    value = json.load(open(path))
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()

def validate_schema():
    master = os.path.join(A, "analysis", "master_outcomes.csv")
    df = pd.read_csv(master)
    assert len(df) == 26, f"expected 26 rows, got {len(df)}"
    cats = {"code-gen","text2sql","tabular","ml-eng","e2e-agent"}
    assert set(df["category"]) <= cats, f"unexpected category: {set(df['category'])-cats}"
    labels = {"pass-as-documented","pass-after-minimal-repair","missing-evaluator","missing-required-data",
              "access-or-license-blocked","credential-or-service-blocked","dependency-or-environment-failure",
              "resource-cap-exceeded","unsupported-output-schema","not-applicable"}
    assert set(df["first_pass_label"]) <= labels, "unexpected first_pass_label"
    for c in ["A0_described","A1_accessible","R2_reconstructable","E3_first_pass","E3_after_repair","E3_smoke_testable"]:
        assert set(df[c].unique()) <= {0,1}, f"{c} not binary"
    assert (df["n_ok_of_5"].between(0,5)).all(), "n_ok_of_5 out of range"
    # consistency: E3_smoke_testable == E3_first_pass OR E3_after_repair
    assert (df["E3_smoke_testable"] == ((df["E3_first_pass"]|df["E3_after_repair"]))).all(), "E3 inconsistency"
    print("[schema] OK: 26 rows, categories/labels/binaries valid, E3 consistent")
    registry = pd.read_csv(os.path.join(A, "corpus", "candidate_registry.csv"))
    assert len(registry) == 35, f"expected 35 screening candidates, got {len(registry)}"
    assert (registry.screening_status == "repository_resolved_audit_cohort").sum() == 26
    assert (registry.screening_status == "post_freeze_resolved_extension").sum() == 4
    resolved_statuses = {"repository_resolved_audit_cohort", "post_freeze_resolved_extension"}
    assert registry.screening_status.isin(resolved_statuses).sum() == 30
    print("[screening] OK: 35 candidates, 26 primary + 4 post-freeze extension + 5 unresolved")
    return df

def validate_model_panel():
    panel = os.path.join(A, "audit", "model_panel_v1")
    analysis = os.path.join(panel, "analysis")
    raw = pd.read_csv(os.path.join(analysis, "raw_model_judgments.csv"))
    aggregate = pd.read_csv(os.path.join(analysis, "aggregated_model_judgments.csv"))
    r2 = pd.read_csv(os.path.join(analysis, "model_panel_r2.csv"))
    stats = json.load(open(os.path.join(analysis, "model_panel_stats.json")))
    repeat = json.load(open(os.path.join(analysis, "model_panel_repeatability.json")))
    production_config = os.path.join(panel, "config.production.json")
    repeat_config = os.path.join(panel, "config.repeat.json")
    assert len(raw) == 468 and len(aggregate) == 156 and len(r2) == 26
    assert set(raw.provider) == {"openai", "anthropic", "gemini"}
    assert stats["r2_majority_permissive"] == 13
    assert stats["r2_majority_strict"] == 1
    assert stats["r2_unanimous_permissive"] == 7
    assert repeat["cells"] == 108
    assert abs(repeat["overall_binary_repeatability"] - 0.9351851851851852) < 1e-12
    production_hash = canonical_json_hash(production_config)
    repeat_hash = canonical_json_hash(repeat_config)
    for run_id in ["panel-v1", "panel-v1-gemini-low"]:
        manifest = json.load(open(os.path.join(panel, "run_manifests", f"{run_id}.json")))
        assert manifest["config_sha256"] == production_hash
    for run_id in ["panel-v1-repeat-t600"]:
        manifest = json.load(open(os.path.join(panel, "repeatability", "runs", run_id, "run_manifest.json")))
        assert manifest["config_sha256"] == repeat_hash
    gemini_repeat_manifest = json.load(open(os.path.join(
        panel, "repeatability", "runs", "panel-v1-repeat-gemini-low", "run_manifest.json"
    )))
    assert gemini_repeat_manifest["config_sha256"] == production_hash
    release_hashes = json.load(open(os.path.join(panel, "RELEASE_HASHES.json")))
    for rel, expected in release_hashes.items():
        assert sha256(os.path.join(panel, rel)) == expected, f"model-panel hash mismatch: {rel}"
    print("[model-panel] OK: 468 raw decisions, 156 cells, R2=13/26 majority, "
          "1/26 strict, 7/26 unanimous; binary repeatability=93.5%")

def validate_evaluation_levels():
    validator = os.path.join(
        A, "execution", "fixtures", "validate_evaluation_levels.py"
    )
    subprocess.run([sys.executable, validator], check=True)

def compute_stats(df):
    N = 26
    def line(k): p,lo,hi = wilson(k,N); return {"k":int(k),"n":N,"prop":round(p,4),"ci":[round(lo,4),round(hi,4)]}
    stats = {"repository_resolution": {"k": 30, "n": 35, "prop": round(30/35, 4),
              "ci": [round(x, 4) for x in wilson(30, 35)[1:]]},
             "A0_conditional":line(df.A0_described.sum()),"A1_conditional":line(df.A1_accessible.sum()),
             "R2":line(df.R2_reconstructable.sum()),
             "E3_any":line(df.E3_smoke_testable.sum()),"E3_first_pass":line(df.E3_first_pass.sum())}
    rng = np.random.default_rng(42)
    v = df.E3_smoke_testable.astype(int).values
    boot = [rng.choice(v, size=N, replace=True).mean() for _ in range(10000)]
    stats["E3_bootstrap_ci95"] = [round(np.percentile(boot,2.5),4), round(np.percentile(boot,97.5),4)]
    stats["E3_by_category"] = {c:{"e3":int(g.E3_smoke_testable.sum()),"n":len(g)} for c,g in df.groupby("category")}
    return stats

def check_stats(stats):
    ref = json.load(open(os.path.join(A,"analysis","phase6_stats.json")))
    assert stats["E3_any"]["k"] == ref["RQ3_executability"]["E3_any"]["k"], "E3 count mismatch vs frozen"
    assert abs(stats["E3_any"]["prop"] - ref["RQ3_executability"]["E3_any"]["prop"]) < 1e-6, "E3 prop mismatch"
    assert stats["R2"]["k"] == ref["RQ2_reconstructability"]["R2_permissive_frozen"]["k"], "R2 mismatch"
    print(f"[stats] OK: repo=30/35, primary E3-first={stats['E3_first_pass']['k']}/26, "
          f"E3-repaired={stats['E3_any']['k']}/26, R2={stats['R2']['k']}/26")
    expanded = pd.read_csv(os.path.join(A, "analysis", "expanded_sensitivity_outcomes.csv"))
    assert len(expanded) == 30
    assert int(expanded.R2_reconstructable.sum()) == 16
    assert int(expanded.E3_first_pass.sum()) == 8
    assert int(expanded.E3_smoke_testable.sum()) == 10
    print("[expansion] OK: R2=16/30, E3-first=8/30, E3-repaired=10/30")

def write_headline_table(stats):
    rows = [
        ("Official repository resolved", 30, 35, stats["repository_resolution"]),
        ("R2 Reconstructable (permissive)", stats["R2"]["k"], 26, stats["R2"]),
        ("R2 Reconstructable (strict)", 1, 26, {"prop": 1/26, "ci": wilson(1, 26)[1:]}),
        ("E3 as documented", stats["E3_first_pass"]["k"], 26, stats["E3_first_pass"]),
        ("E3 after documented repair", stats["E3_any"]["k"], 26, stats["E3_any"]),
    ]
    csv_path = os.path.join(A, "tables", "table1_endpoints.csv")
    with open(csv_path, "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["Outcome", "k", "n", "Proportion", "95% CI"])
        for label, k, n, values in rows:
            lo, hi = values["ci"]
            writer.writerow([label, k, n, f"{100*values['prop']:.1f}%", f"[{100*lo:.1f}%, {100*hi:.1f}%]"])
    tex_path = os.path.join(A, "tables", "table1_endpoints.tex")
    with open(tex_path, "w") as handle:
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write("\\caption{Screening and conditional audit outcomes (Wilson 95\\% intervals).}\n")
        handle.write("\\label{tab:endpoints}\n\\footnotesize\n\\begin{tabular}{@{}lrrrr@{}}\n")
        handle.write("\\toprule\nOutcome & k & n & Proportion & 95\\% CI \\\\\n\\midrule\n")
        for label, k, n, values in rows:
            lo, hi = values["ci"]
            handle.write(f"{label} & {k} & {n} & {100*values['prop']:.1f}\\% & "
                         f"[{100*lo:.1f}\\%, {100*hi:.1f}\\%] \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")
    print("[tables] regenerated table1_endpoints.csv/.tex")

def check_hashes():
    manifest_path = os.path.join(A, "OUTPUT_HASHES.json")
    if not os.path.exists(manifest_path):
        print("[hashes] no OUTPUT_HASHES.json (run --regenerate first to create it)"); return
    ref = json.load(open(manifest_path)); ok=0; bad=[]
    for rel, h in ref.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p): bad.append((rel,"MISSING")); continue
        if sha256(p) != h: bad.append((rel,"HASH_DIFF"))
        else: ok += 1
    if bad:
        print(f"[hashes] {ok} match, {len(bad)} differ:"); [print("  ",r,s) for r,s in bad]
    else:
        print(f"[hashes] OK: all {ok} released outputs match recorded hashes")

def write_hashes():
    targets = ["artifact/tables/table1_endpoints.csv","artifact/tables/table2_by_category.csv",
               "artifact/tables/table3_per_benchmark.csv","artifact/analysis/master_outcomes.csv",
               "artifact/analysis/phase6_stats.json",
               "artifact/analysis/expanded_sensitivity_outcomes.csv",
               "artifact/analysis/expanded_sensitivity_stats.json",
               "artifact/audit/model_panel_v1/analysis/model_panel_stats.json",
               "artifact/audit/model_panel_v1/analysis/model_panel_repeatability.json",
               "artifact/audit/model_panel_v1/RELEASE_PROTOCOL.json"]
    ref = {t: sha256(os.path.join(ROOT,t)) for t in targets if os.path.exists(os.path.join(ROOT,t))}
    json.dump(ref, open(os.path.join(A,"OUTPUT_HASHES.json"),"w"), indent=2)
    print(f"[hashes] wrote OUTPUT_HASHES.json for {len(ref)} released outputs")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--regenerate", action="store_true")
    args = ap.parse_args()
    if not (args.check or args.regenerate): args.check = True
    df = validate_schema()
    validate_model_panel()
    validate_evaluation_levels()
    stats = compute_stats(df)
    check_stats(stats)
    if args.regenerate:
        write_headline_table(stats)
        subprocess.run([sys.executable, os.path.join(A, "make_figures.py")], check=True)
        # extended analyses (blocker taxonomies, artifact-presence association,
        # lineage robustness) feed the TeX figures, so they run first
        subprocess.run([sys.executable,
                        os.path.join(A, "analysis", "build_extended_analysis.py")], check=True)
        subprocess.run([sys.executable, os.path.join(A, "make_tex_figures.py")], check=True)
        write_hashes()
    else:
        check_hashes()
    print("\nReproduction complete. E3 as documented = {}/26; after repair = {}/26."
          .format(int(df.E3_first_pass.sum()), int(df.E3_smoke_testable.sum())))

if __name__ == "__main__":
    main()
