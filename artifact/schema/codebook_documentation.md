# Audit Instrument / Codebook (Phase 3)

**Version:** 1.0.0 — frozen (see `codebook_v1.json` field `frozen_sha256`).
**Frozen on audit date:** 2026-07-13.

The codebook is frozen *before* any label is assigned. Its SHA-256 is recorded so
that any later change is detectable; inclusion criteria, labels, and outcome
logic are not silently changed after observing results.

## Label set (6)

| Label | Meaning |
|---|---|
| documented-and-verifiable | Stated in an official source **and** independently confirmable in a public artifact. |
| partially-documented | Some consequential parts present; a bounded, non-trivial gap remains. |
| claimed-but-not-verifiable | Officially asserted but the referenced artifact is unreachable or lacks the detail. |
| not-documented | Not stated and not present in inspected artifacts; record locations + search terms. |
| not-applicable | Criterion does not apply to this task type. |
| access-blocked | Referenced artifact exists but is gated, so content cannot be verified publicly. |

The label set deliberately distinguishes *missing* (`not-documented`) from
*claimed-but-unverifiable* from *access-blocked*, matching the project rule that
these are different conditions.

## Criteria (25) in 5 groups

Identity/Provenance, Task/Data, Prompt/Run, Evaluation, Environment. Each
criterion carries an inherited / adapted / new status (see
`criterion_crosswalk.csv`): 8 inherited, 10 adapted, 7 new.

## Release-level outcome derivation

- **A0 Described** — a public paper/report defines the benchmark.
- **A1 Accessible** — core referenced artifacts are publicly reachable; no
  `claimed-but-not-verifiable` or `access-blocked` on core artifact-linkage criteria.
- **R2 Reconstructable** — the six consequential evaluation criteria (input/output
  schema, metric definition, evaluator implementation available, grading rules,
  predictions→score mapping, sample predictions) are `documented-and-verifiable`
  or `partially-documented` with a bounded gap — never `not-documented` or
  `claimed-but-not-verifiable`.
- **E3 Smoke-testable** — decided by the execution protocol (Phase 5), not by
  coding; the evaluator must run in the CPU sandbox on supplied or schema-valid
  synthetic predictions.

The outcomes are ordered as reporting levels, not a global quality score.

## Primary vs exploratory

The six R2-determining criteria are the **primary** outcomes for reliability
(target Krippendorff alpha >= 0.80). The remaining 19 criteria are exploratory
(target >= 0.67). Reliability is computed with Krippendorff's alpha (nominal)
and Gwet's AC1 as a prevalence-robust sensitivity check.

## Evidence requirements (every non-trivial cell)

benchmark, frozen commit, source URL/path, pointer (page/section/file/line),
access date, evidence quote/note, raw coder label, adjudicated label,
disagreement/repair note. For `not-documented`, also the artifact locations and
search terms inspected. Machine schema: `audit_record_schema.json`.

## Source priority

official paper/appendix > official supplementary > official repository >
official dataset/model-hub page > official docs/site > official leaderboard docs.
Third-party implementations provide context only and never establish that the
official release is reconstructable.
