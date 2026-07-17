# Phase 6 — Statistics, Robustness, and Case Studies

**Audit date:** 2026-07-13 | **Screening frame:** 35 candidates | **Conditional audit cohort:** N = 26 repository-resolved releases. See the 2026-07-14 protocol amendment.

## Research questions and outcomes

### RQ1 — Screening and conditional accessibility
Completed repository resolution was 30/35 (85.7%): 26 primary frozen releases
plus four post-freeze expansion releases. Within the primary cohort,
A0 and A1 were 26/26 by construction and artifact-class presence was uneven:
sample predictions 13/26 and container recipes 7/26. These conditional rates
must not be generalized to all eligible benchmarks.

### RQ2 — Reconstructability
Under the three-provider majority rule, model-coded R2 = 13/26; the strict rule
gives 1/26 and unanimous permissive agreement gives 7/26. Because nominal
inter-model reliability missed its pre-specified gate, R2 is descriptive.

### RQ3 — Executability
First-pass E3 is 5/26 (19.2% [8.5%, 37.9%]). Two more cases pass only after
documented interventions, giving 7/26 after repair. The dated amendment treats
first-pass as the least discretionary estimate and repaired E3 as sensitivity.

### RQ4 — Claim–evidence concordance
14/26 READMEs frame a runnable evaluation (explicit reproducibility language or a concrete one-command evaluation invocation). Of those 14, **2 (14.3%, CI [4.0%, 39.9%]) produced a score under the CPU-only, no-inference protocol**; the other 12 are framed-runnable but gated by an external dependency not surfaced in the runnable framing — dependency/environment (6), credential/service such as an LLM API or live database (4), missing required data (1), or not-applicable environment coupling (1). We report this as a gap between how evaluation is framed publicly and what runs under a controlled independent protocol; we do not infer that any claim is false, only that the framed procedure did not run unassisted here.

### RQ5 — Failure patterns
**Reconstruction (R2)** is most often blocked by grading and tie-breaking rules
(11/26), followed by predictions→aggregate-score mapping (7), evaluator
availability (4), metric definition (2), and I/O schema (1). A release may be
blocked on multiple criteria.

**Execution (E3)** failure mechanisms vary by category: text-to-SQL is blocked by missing databases (missing-required-data 3/5, credential/service 2/5); ml-engineering by dependency/environment coupling to model weights and heavy stacks (3/5); e2e-agents by credential/service gating (LLM/cloud) (3/8). The single most common first-pass blocker overall is credential-or-service dependency (7/19 non-E3).

## Robustness checks
- **Model-panel sensitivity (R2).** Majority permissive: 13/26; strict: 1/26;
  unanimous permissive: 7/26. Leave-one-judge-out pessimistic counts are 7--10
  and optimistic counts are 14--17. R2 remains descriptive.
- **Excluding service/access-blocked releases (E3).** All: 7/26 (26.9%). Excluding credential/service- and access-blocked releases: 6/18 (33.3% [16.3%, 56.3%]). The primary conclusion is unchanged in direction.
- **First-pass vs repaired execution** are reported separately throughout (5 as-documented + 2 after minimal repair).
- **Category association (exploratory).** text-to-SQL vs rest × E3: Fisher exact p = 0.278 (0/5 vs 7/21). R2 vs E3: Fisher exact p = 0.073, odds ratio ≈ 10.3 — reconstructable releases reach E3 far more often (6/13 vs 1/13), though not significant at α = 0.05 with N = 26. Reported as exploratory; no causal interpretation.

## Case studies (mechanism, not judgment)

**1. Reconstructable and smoke-testable as documented — ScienceAgentBench** (commit 72220ee8). The public `calculate_metrics.py` aggregator consumes schema-valid run/eval logs and emits Success Rate, CodeBERTScore, Valid Program Rate, and Cost. On schema-valid synthetic logs (2 runs × 5 tasks) it ran first-pass (EXIT 0) and returned SR 0.80, CodeBERTScore 0.73, Valid Program Rate 1.0. We smoke-tested the *aggregator*; the upstream CodeBERT/program-execution scorer was not exercised. Mechanism: the score-composition step is public, self-contained, and dependency-light.

**2. Succeeds only after a documented repair — DS-1000** (commit b39aab71). The first pass failed because the sandbox blocks semaphores required by `ProcessPoolExecutor`. The repair used serial in-process execution and a signal timeout on a 50-problem slice, producing a mean pandas score of 0.48. Because process isolation changed, semantic equivalence is not claimed; this case appears only in the repaired sensitivity result.

**3. Blocked by a missing external artifact — Spider** (commit b7b5b8c8). Spider ships gold/predicted SQL examples and `tables.json`, and its `evaluation.py` is public. Even in exact-match mode the evaluator calls `get_schema(db)` per row (line 505), which reads a per-database SQLite file; the SQLite databases are a large, separately distributed artifact not present in the repository clone. The evaluator therefore did not produce a score under our protocol — classified missing-required-data. Mechanism: the scorer's control flow is coupled to a bulk data artifact distributed outside the code repository. We did not find this dependency flagged as a prerequisite in the runnable framing.

## Deliverables
- `artifact/analysis/master_outcomes.csv` — one row per release with all A0/A1/R2/E3 outcomes and component-presence flags.
- `artifact/analysis/phase6_stats.json` — all RQ proportions, CIs, bootstrap, robustness, and exploratory tests.
- `artifact/analysis/claim_evidence_concordance.csv` — RQ4 per-release claim codes vs observed evidence.
- `artifact/audit/model_panel_v1/` — prompts, packets, raw judgments,
  deterministic aggregation, repeatability, protocol history, and hashes.
- `artifact/figures/fig_endpoints_forest.{png,pdf}` — RQ1–RQ3 endpoint forest plot with Wilson CIs.
- `artifact/figures/fig_failure_patterns.{png,pdf}` — RQ4 concordance and RQ5 failure patterns.
