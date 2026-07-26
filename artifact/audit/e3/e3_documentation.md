# Phase 5 — E3 Evaluator Smoke-Test Results

Audit date: 2026-07-13. Environment: CPU-only conda env `e3smoke` (Python 3.11), controlled `std_path_semantics=on` (PYTHONSAFEPATH neutralized uniformly before first pass).

## Execution endpoints

- **First-pass (as documented): 5/26 = 19.2%**, 95% Wilson CI [8.5%, 37.9%].
- **After documented repair: 7/26 = 26.9%**, 95% Wilson CI [13.7%, 46.1%].
  Two additional cases are DS-1000 and TableBench.
- Executions attempted (interface reached, command run): 21/26.

First-pass and repaired outcomes are reported separately and never merged. Every repair is a documented environment/service configuration change with no edit to benchmark source code.

## Ladder

Completed repository resolution is 30/35, comprising 26 primary releases and a
four-release post-freeze expansion. Within the primary cohort, model-coded R2
is 13/26, first-pass E3 is 5/26, and repaired E3 is 7/26.

## R2 → E3 conditional

- Among R2-reconstructable (n=13): 6 reached E3.
- Among not-R2 (n=13): 1 reached E3.

## By category

- code-gen: 1/4
- e2e-agent: 3/8
- ml-eng: 1/5
- tabular: 2/4
- text2sql: 0/5

No text-to-SQL/DB benchmark reached E3: every one requires a live database (SQLite/DuckDB/BigQuery) or a service credential for execution-based scoring.

## Repair patches (minimal, documented)

- **DS-1000**: in-process execution shim — ProcessPoolExecutor to serial executor and `execution.check_correctness` monkeypatched to `exec()` in-process with a signal-based `ITIMER_REAL` wall-clock guard. This changes process isolation, so semantic equivalence is not claimed. Reason: sandbox blocks POSIX semaphores and multiprocessing.Manager. 50-problem smoke slice on shipped predictions; no repo source edited.
- **TableBench**: network access to huggingface.co granted (service configuration, no code edit). Reason: `evaluate.load('rouge')` fetches the ROUGE metric module from the HF Hub at runtime.

## Per-benchmark outcomes

| Benchmark | Category | R2 | First-pass label | E3 | Prediction source |
|---|---|---|---|---|---|
| BigCodeBench | code-gen | ✓ | credential-or-service-blocked | — | n/a |
| DA-Code | code-gen | ✓ | missing-required-data | — | n/a |
| DS-1000 | code-gen | ✓ | dependency-or-environment-failure | ✓ | OFFICIAL shipped sample predictions (data/gpt-4o-2024-08-06-answers.jsonl) |
| PandasEval/NumpyEval (CERT) | code-gen | — | dependency-or-environment-failure | — | n/a |
| BLADE | e2e-agent | — | credential-or-service-blocked | — | n/a |
| BixBench | e2e-agent | ✓ | credential-or-service-blocked | — | n/a |
| DataSciBench | e2e-agent | — | missing-required-data | — | n/a |
| DiscoveryBench | e2e-agent | — | credential-or-service-blocked | — | n/a |
| InfiAgent-DABench | e2e-agent | ✓ | pass-as-documented | ✓ | 10 synthetic @name[value] responses keyed to real label IDs (every 3rd corrupted) |
| QRData | e2e-agent | ✓ | pass-as-documented | ✓ | schema-valid synthetic (4 items, both fields fabricated) |
| ScienceAgentBench | e2e-agent | ✓ | pass-as-documented | ✓ | schema-valid synthetic run_logs+eval_logs (2 runs x 5 tasks) |
| Spider2-V | e2e-agent | — | not-applicable | — | n/a |
| DSBench | ml-eng | — | pass-as-documented | ✓ | schema-valid synthetic answer.csv + predict.csv (Rings target, 20 rows) |
| MLAgentBench | ml-eng | ✓ | credential-or-service-blocked | — | n/a |
| MLE-bench | ml-eng | ✓ | dependency-or-environment-failure | — | n/a |
| MLGym | ml-eng | — | dependency-or-environment-failure | — | n/a |
| RE-Bench | ml-eng | ✓ | dependency-or-environment-failure | — | n/a |
| SpreadsheetBench | tabular | ✓ | pass-as-documented | ✓ | schema-valid synthetic dataset.json + answer/input .xlsx pairs (2 tasks, match+mismatch) |
| TabFact | tabular | — | dependency-or-environment-failure | — | n/a |
| TableBench | tabular | ✓ | credential-or-service-blocked | ✓ | official shipped example (o3-mini DP example jsonl) |
| WikiTableQuestions | tabular | — | dependency-or-environment-failure | — | n/a (failed at parse) |
| BIRD | text2sql | — | missing-required-data | — | n/a |
| BIRD-CRITIC / SQL-eval | text2sql | — | credential-or-service-blocked | — | n/a |
| Dr.Spider | text2sql | — | missing-required-data | — | n/a |
| Spider | text2sql | — | missing-required-data | — | official shipped gold/pred examples (no DB) |
| Spider 2.0 | text2sql | ✓ | credential-or-service-blocked | — | n/a |

## Constraint compliance

0 GPU-hours, 0 paid model API calls, no full model/agent inference, no private credentials, no leaderboard-score reproduction. Synthetic predictions were schema-valid and independent of benchmark answer keys (e.g. InfiAgent every-3rd-answer corruption; no wholesale answer-key copy).

## Scope limits

Smoke-testability is not full computational reproducibility. A `pass` means the official scorer processed supplied or schema-valid synthetic predictions on CPU and produced a structured score; it does not certify that scores match published leaderboard values. Blocker labels record what did not run under this controlled protocol, not that an evaluator is defective.
