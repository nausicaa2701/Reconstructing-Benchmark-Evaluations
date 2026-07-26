# Evaluator Smoke-Test Replay

The E3 smoke tests are replayed separately from `reproduce.py` because they depend on
heterogeneous external artifacts (each benchmark's own repository at a frozen commit).

## Controlled environment

All smoke tests ran in a single conda environment, `e3smoke` (Python 3.11):

- spec: `../environment/e3smoke_pip_freeze.txt`
- CPU only, 0 GPU-hours, 0 paid model API calls, no private credentials.

## Per-benchmark manifests

`manifests/INDEX.json` lists all 26 releases with their E3 outcome. Each *attempted*
benchmark has a manifest `manifests/<Benchmark>.json` recording:

- frozen commit,
- prediction source (official sample predictions or schema-valid synthetic),
- first-pass label + runtime + log path,
- repair-pass label + patch (only when a minimal repair was applied),
- final E3 status.

## Two-pass protocol

1. **First pass** follows official instructions with no code modification. Its label and
   log are recorded under `first_pass`.
2. **Minimal-repair pass** (only where applied) is recorded separately under `repair_pass`
   with the exact patch. First-pass and repaired outcomes are never merged.

Repairs applied in this study (see `patches/`):

- **run_bounded.py** -- bounded runner wrapper (time cap + exit/runtime trailers); applied
  uniformly as controlled-environment configuration, not a benchmark fix.
- **ds1000_launcher2.py** -- DS-1000 in-process execution shim: replaces `ProcessPoolExecutor`
  (blocked by sandbox semaphore limits) with serial execution and a signal-based ITIMER timeout
  that preserves exact pass/fail semantics; 50-problem smoke slice. No repo edit.
- **TableBench** -- network access to huggingface.co for `evaluate.load('rouge')` (service
  configuration, no code edit).

## Path redaction

Raw logs are released verbatim except that machine-specific absolute path prefixes have been
replaced with portable placeholders (`$WORKSPACE`, `$CONDA`, `$REPO`, `$HOME`). No other log
content was altered; exit codes, runtimes, tracebacks, and scores are unchanged.

## Reaching E3 (7/26)

pass-as-documented: QRData, InfiAgent-DABench, DSBench, ScienceAgentBench, SpreadsheetBench.
pass-after-minimal-repair: DS-1000, TableBench.

## Not reaching E3 (19/26)

Blockers are labeled with the frozen execution-label vocabulary: credential-or-service-blocked,
dependency-or-environment-failure, missing-required-data, not-applicable. See each manifest and
`../audit/e3/e3_records_detail.json` for the per-release detail.
