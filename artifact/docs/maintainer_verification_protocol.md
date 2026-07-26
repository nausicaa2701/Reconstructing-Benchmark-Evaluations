# Maintainer Verification and Dispute Protocol

## Purpose

Every *not-documented* and *claimed-but-not-verifiable* label in this audit
rests on an author-conducted search of public artifacts. Missing evidence is
not evidence of absence, and the people best placed to falsify such a label are
the release's own maintainers. This protocol turns that into a measured
quantity: a confirmation rate, a dispute rate, and a corrected false-omission
rate.

## What is sent

For each of the 26 releases, one notification containing only:

1. the frozen commit and audit date;
2. the criteria coded *not-documented*, *claimed-but-not-verifiable*, or
   *partially-documented*, with the exact searched locations and search terms;
3. the first-pass execution label and the exact command and log;
4. a request to confirm, dispute, or correct each item;
5. a statement that the audit assesses public evaluation reconstructability,
   not benchmark quality or author competence, and that responses will be
   published verbatim alongside the label they concern.

Nothing is asked of maintainers beyond a per-item verdict. No embargo is
requested and no response is required.

## Response coding

Each item receives exactly one outcome:

- **confirmed** — the maintainer agrees the evidence is not public at the
  frozen commit.
- **disputed-with-pointer** — the maintainer identifies public evidence we
  missed. This is a **false omission** and the label is corrected.
- **disputed-without-pointer** — the maintainer disagrees but supplies no
  locatable public evidence. The label stands and the dispute is published.
- **out-of-scope** — the maintainer points to evidence published after the
  frozen commit. The label stands for the frozen commit and the update is
  recorded in the correction log.
- **no-response** — recorded as such; never coerced into agreement.

## Reported quantities

- confirmation rate = confirmed / (confirmed + disputed + out-of-scope)
- dispute rate = (disputed-with-pointer + disputed-without-pointer) / responded
- **false-omission rate** = disputed-with-pointer / all missing-evidence labels
  sent. This is the quantity that bounds the validity of our search procedure
  and is the single most informative number this protocol produces.
- response rate = responded / contacted

## Handling of corrections

A false omission triggers: correction of the cell, a dated entry in
`corrections.csv`, recomputation of every affected aggregate, and publication
of both the original and corrected label. Frozen records are never silently
rewritten; see `maintenance_policy.md`.

## Ethics

Contact is by the public channel the release itself designates (repository
issue tracker or the correspondence address in its paper). No individual is
named in the paper as the source of a dispute unless they ask to be. Responses
are published verbatim only with permission; otherwise only the coded outcome
is published.

## Status

The notification set is prepared and the response ledger schema is fixed
(`maintainer_responses.csv`). No release has been contacted yet, so the paper
reports no confirmation or dispute rate and states this absence explicitly as
a limitation rather than implying validation.
