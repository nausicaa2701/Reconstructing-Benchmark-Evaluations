# Corpus Maintenance and Correction Policy

## The problem this solves

The audit is anchored to commits frozen on 2026-07-13. Those repositories keep
moving: an evaluator that was undocumented then may be documented now, and a
link that resolved then may be dead now. A point-in-time audit that is silently
edited to track those changes stops being a frozen record; one that is never
updated stops being useful. This policy separates the two.

## Two layers, one immutable

**Layer 1 — the frozen record.** Corpus registry, evidence packets, model
judgments, execution logs, patches, and the analysis that produced the paper's
numbers. This layer is **append-only**. It is never edited after the release
tag that accompanies the paper. Any error in it is handled by a correction
entry, never by rewriting the file.

**Layer 2 — the living record.** Re-audits at later commits, maintainer
responses, corrections, and any label superseded by newer evidence. This layer
changes; every change is dated and points at the Layer 1 record it supersedes.

A reader can always reconstruct exactly what the paper claimed, and separately
see what is true today.

## Versioning

Semantic release tags on the artifact repository:

- `vX.0.0` — a new audit round (new freeze date, re-audited cohort). The prior
  round remains published and citable.
- `vX.Y.0` — new evidence added to the living layer: maintainer responses,
  human-validation labels, official-environment runs, golden-fixture results.
  No Layer 1 file changes.
- `vX.Y.Z` — a correction. Requires a `corrections.csv` entry.

The tag accompanying this paper is frozen at submission and archived with a
DOI. Every number in the paper is reproducible from that tag alone.

## Correction procedure

1. Anyone may file a correction through the repository issue tracker; the
   maintainer verification protocol is the structured path for release authors.
2. A correction is accepted only with a locatable pointer to public evidence at
   the frozen commit. Evidence published after the freeze is recorded as a
   post-freeze update, not a correction.
3. An accepted correction adds a row to `corrections.csv` recording the
   original value, the corrected value, the trigger, the affected aggregates,
   and the release tag it supersedes.
4. Affected aggregates are recomputed and republished with both the original
   and corrected figures visible. Headline numbers are never quietly changed.
5. Corrections that would change a number printed in the paper are additionally
   listed in a `PAPER_ERRATA.md` at the repository root.

## Disputes we do not accept

A dispute without a pointer to public evidence at the frozen commit does not
change a label. It is published verbatim next to the label it concerns, and the
disagreement stands on the record. We do not adjudicate a maintainer's
recollection against our search; we publish both.

## Re-audit cadence

A re-audit round is triggered by whichever comes first: 18 months since the
last freeze, or a corrected false-omission rate above 10% in the maintainer
verification protocol, which would indicate that the search procedure itself
needs revision rather than individual labels.

## Deprecation

No round is ever deleted. If a round's methodology is superseded, its README
gains a deprecation notice naming the superseding tag; the data stays
downloadable and citable at its DOI.
