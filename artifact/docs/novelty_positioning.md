# Novelty and Positioning (Phase 1)

Initial framework metadata is stored in
`artifact/data/comparison_frameworks_metadata.json`. A 2026-07-14 update adds
full-text checks for the closest works; novelty claims must not be based on
abstracts alone.

## Closest-work correction

The initial search missed *ReproEvalCard*, published at ACL 2026
(doi:10.18653/v1/2026.acl-short.22). It audits 55 LLM-pipeline papers and then
proposes a reporting standard. The corrected comparison also treats Rollout
Cards as an empirical repository audit with re-grading, not merely a card
template, and adds Auto Benchmark Audit (arXiv:2605.26079), which executes
task-level audits across 168 benchmarks.

## The novelty matrix

`novelty_matrix.csv` compares the closest prior works plus this study. Coding legend: `yes` =
capability is a core, exercised component; `partial` = touched but not central or
only via self-report; `no` = not present.

Key observations after the correction:

- **BetterBench** (arXiv:2411.12990) assesses 24 AI benchmarks against 46
  best-practice items across the benchmark lifecycle, reports a human-checked
  assessment, and releases a living repository — but its unit is a checklist over
  documentation/usability; it does **not** clone repositories at a frozen commit
  or execute evaluators.
- **BenchmarkCards** (arXiv:2410.12974) standardizes benchmark documentation and
  validates it with user studies; it is a documentation schema, not a
  claim–evidence audit or an execution study.
- **MEQA** (arXiv:2504.14039) meta-evaluates QA benchmarks with human and LLM
  judges and produces quantifiable scores; domain is QA/cybersecurity and it does
  not execute benchmark evaluators.
- **ReproEvalCard** audits evaluation-critical reporting artifacts but does not
  execute third-party benchmark scorers.
- **Rollout Cards** audits 50 repositories and re-grades preserved outputs; its
  unit is the rollout record and reporting rule rather than scorer availability.
- **Auto Benchmark Audit** executes automated task-level checks and validates
  issues with experts; its object is task correctness rather than release-level
  public scorer reconstructability.
- **REPRO-Bench** executes and inspects repositories, but its unit is a
  social-science paper and its purpose is to benchmark AI agents' reproducibility
  assessment, not to audit FM benchmark evaluators for data science.

We no longer claim that repository inspection or execution is new in isolation.
The narrower contribution is evidence-linked, release-level measurement of
public scorer reconstruction and invocation for data-science workflows, with
frozen commits and separate as-documented versus repaired outcomes.

## Criterion crosswalk

`criterion_crosswalk.csv` classifies all 25 audit criteria: 8 **inherited**
(same meaning as Datasheets / Model Cards / standard ML reporting), 10
**adapted** (modified for data-science or agentic evaluation), and 7 **new**
(not represented in the selected prior frameworks and justified by a specific
reconstruction/execution failure mode: frozen evaluator commit, agent scaffold,
evaluator-implementation presence, sample predictions/trajectories,
predictions→score mapping, container/env file, required services & credentials).

## "Why not just use BetterBench?" (two sentences)

BetterBench scores *documentation and usability best practices* from what a
benchmark reports about itself; it neither freezes a repository commit as
evidence nor attempts to run the evaluator. Our study instead independently
verifies that referenced artifacts are reachable, reconstructs the evaluation
specification from repository-level evidence, and **executes each public
evaluator in a controlled CPU-only environment**, separating unassisted from
minimally repaired execution — capabilities a documentation checklist cannot
provide.

## Contributions that are not implemented by the closest prior work

1. **Controlled CPU-only scorer invocation** with separate as-documented and
   repaired outcomes, released logs, and frozen release-level evidence.
2. **Claim–evidence concordance** comparing explicit paper artifact-availability
   claims against independently observed public evidence at the release level.

Both are additional to (not just a domain restriction of) documentation audits.
Domain restriction alone is explicitly *not* claimed as the novelty.
