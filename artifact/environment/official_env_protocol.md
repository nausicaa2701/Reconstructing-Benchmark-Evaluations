# Per-Release Official-Environment Baseline (E3-official)

## Why this exists

The frozen audit measured E3 in one shared environment (conda `e3smoke`,
Python 3.11.15, CPU-only). That design confounds two different things: a
release whose evaluator is genuinely not runnable, and a release whose
evaluator is runnable under its own documented environment but not under ours.
Two of the seven first-pass dependency-or-environment failures (DS-1000,
MLE-bench) are known to be of the second kind or plausibly so.

This protocol adds a second, primary-facing endpoint:

- **E3-official** — the evaluator is invoked in a clean environment built
  *only* from the release's own documented setup instructions at the frozen
  commit.
- **E3-portable** — the evaluator is invoked in the shared `e3smoke`
  environment. This is what the frozen audit reports.

E3-official measures the release. E3-portable measures the release *and* our
provisioning, and becomes an explicitly labelled portability endpoint rather
than the headline.

## Environment construction rules

1. Start from a clean container per release. No packages carried over from a
   previous release, no packages from `e3smoke`.
2. Base image is chosen by the release's own documentation. If it names an OS,
   Python version, CUDA version, or base image, use it. If it names none, use
   `python:3.11-slim` and record that the release under-specifies its base.
3. Install exactly what the release's documented path installs, in the
   documented order: `environment.yml`, `requirements.txt`, `pyproject.toml`,
   `setup.py`, `Dockerfile`, or the README's literal commands. Record which
   file was authoritative.
4. No auditor-chosen package may be added at this stage. A missing transitive
   dependency is a finding, not a provisioning task.
5. `PYTHONSAFEPATH` and other sandbox normalisations applied in the frozen
   audit are **not** applied here; if the documented path requires a different
   host contract, record it as an environment-contract finding.
6. Network access follows the frozen audit's rule: package indexes and the
   release's own documented downloads are allowed; credentialed or gated
   services remain blockers and are never circumvented.
7. Record the resulting image digest, the full resolved package set, wall-clock
   build time, and every command.

## Outcome labels

Each release receives a pair `(E3-official, E3-portable)` with the same
first-pass / after-repair split used in the frozen audit. Four combinations
carry distinct meaning:

| official | portable | reading |
| --- | --- | --- |
| pass | pass | evaluator runs; environment-independent within our range |
| pass | fail | our shared environment caused the failure; the frozen audit under-reports this release |
| fail | pass | the documented environment is broken but the scorer is portable |
| fail | fail | the failure is a property of the release under both contracts |

Only the `pass/fail` row would change the frozen audit's interpretation, and
DS-1000 and MLE-bench are the two releases we expect to land there.

## Scope of the baseline

All 21 releases that reached an executable command are in scope. The five that
never presented an invocable interface are out of scope: no documented
environment can be built for an evaluator that does not exist in the artifacts.

## Reporting rule

E3-official and E3-portable are reported as separate columns and never merged.
Until the per-release runs are complete, the paper reports E3-portable only and
labels it as such; no release is claimed to pass or fail E3-official on the
basis of the shared-environment result.

## Status

Environment specifications are generated from the frozen manifests by
`build_official_env_specs.py`. The execution of these environments requires
re-cloning each release at its frozen commit and is not yet complete; the
paper states this explicitly rather than reporting the shared-environment
result as an as-documented outcome.
