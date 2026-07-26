# Research Contract (Frozen)

**Project:** Reconstructing Benchmark Evaluations: A Public-Artifact Audit of Foundation-Model Benchmarks for Data Science
**Target venue:** KDD 2027 Datasets and Benchmarks Track
**Contract frozen:** before full-corpus coding (Phase 0 gate); see the dated
post-freeze amendment in `protocol_amendment_2026-07-14.md`.
**Status of REAL-C:** demoted from headline contribution to a *secondary diagnostic taxonomy*; no overall REAL-C score is computed.

## 1. Central question

Given only a benchmark paper and its public supplementary materials, repositories, datasets, documentation, and leaderboards, can an independent researcher reconstruct the benchmark's evaluation protocol and run its evaluator **without performing foundation-model inference**?

## 2. Primary outcome (pre-specified)

The original endpoint was the proportion of included benchmark releases that
reach **E3 (Smoke-testable)** under the pre-specified CPU-only protocol. The
dated amendment promotes first-pass E3 as the least discretionary estimate and
treats repaired E3 as sensitivity analysis.

Secondary outcomes: A1 accessibility rate, R2 reconstructability rate, pass-after-repair rate, and claim–evidence disagreement rate.

## 3. Release-level operational outcomes

| Level | Name | Operational requirement |
|---|---|---|
| A0 | Described | A public paper or technical report defines the benchmark. |
| A1 | Accessible | Core referenced artifacts are publicly reachable under their stated access conditions. |
| R2 | Reconstructable | Consequential components of the evaluation specification can be instantiated without unsupported guesses. |
| E3 | Smoke-testable | The evaluator produces a score or structured result from supplied or schema-valid synthetic predictions in the controlled CPU environment. |

These levels measure **public evaluation reproducibility**. They are explicitly **not** a universal ranking of benchmark quality.

## 4. Operational definitions (frozen; Section 2.5 of plan)

- **Public artifact:** a resource available without personal requests, privileged credentials, paid model access, or private organizational access.
- **Evaluation specification:** task definition, inputs, expected outputs, dataset version/split, prompts/scaffold, model/run configuration, environment, metric, evaluator, and grading behavior needed to understand how a reported result was produced.
- **Reconstructable:** the public artifacts provide enough information to instantiate the evaluation specification without guessing consequential details.
- **Evaluator:** the code or formally specified process mapping benchmark predictions or trajectories to scores or structured evaluation outputs.
- **Smoke-testable:** the evaluator can process supplied or schema-valid synthetic predictions in a controlled CPU environment and produce a score or structured result.
- **Full reproduction:** re-executing the complete model or agent evaluation and recovering reported results. **Out of scope.**

## 5. Non-goals (must be stated in the paper)

The study does **not**: reproduce complete leaderboard results; rerun foundation models or agents; judge whether one benchmark is globally better than another; infer undocumented author intentions; treat missing documentation as proof a procedure was not performed; measure model capability, quality, or safety; or claim full computational reproducibility from an evaluator smoke test.

## 6. Unit of analysis

A **benchmark release**, defined by: a canonical paper/technical report; an identifiable public release date; a repository/dataset/documentation site when available; a frozen repository commit and dataset version when available; and an audit date. Distinct major versions with materially different task definitions, data, or evaluators count as separate releases; minor repository updates do not.

## 7. Hard resource constraints (part of the scientific design)

0 GPU-hours; 0 paid model API calls; no private credentials; no full model/agent inference; CPU-only evaluator smoke tests; deterministic analysis scripts where possible; a documented per-benchmark time and download budget.

## 8. Language discipline

- "We did not find public evidence of X" — never "the authors did not perform X."
- "The evaluator did not run under our controlled protocol" — never "the evaluator is broken."
- "Publicly reconstructable" — never "reproducible" when full reproduction was not tested.
- The word **first** is used only if a documented systematic search establishes it. (It is not used.)
- "Benchmark quality" is never used as a synonym for public reconstructability.

## 9. Coding integrity commitments

Every non-trivial audit decision carries: benchmark+release id, frozen commit/version when available, source URL/path, page/section/line/file pointer, access date, evidence quotation or factual note, raw coder label, adjudicated label when applicable, and disagreement/repair explanation. `not-documented` decisions record the locations inspected and search terms used. Raw independent labels are preserved before adjudication. Checklist cells from the same benchmark are never treated as independent samples.
