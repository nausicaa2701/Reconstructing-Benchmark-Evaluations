# Human Validation of R2 Coding

This directory contains the completed, replayable blinded human-validation
workflow, the two frozen rater submissions, adjudication records, and derived
reliability analyses.

## Roles

- Two coders independently label all 26 releases on the same six criteria.
- Coders must not inspect model labels or discuss decisions before freezing.
- An adjudicator reviews only disagreements after both files are frozen.
- A coder must not serve as adjudicator.

## Allowed labels

`documented-and-verifiable`, `partially-documented`,
`claimed-but-not-verifiable`, `not-documented`, `not-applicable`, and
`access-blocked`.

Use `artifact/schema/codebook_v1.json` and inspect the frozen evidence bundle
named in each assignment. Record a concrete file, section, or URL pointer and a
short factual note for every label. Do not read
`artifact/audit/raw_labels/r2_coder_labels.csv` or adjudicated labels until both
human files are frozen and hashed.

## Workflow

```bash
python artifact/human_validation/prepare_assignments.py   # shuffled item order per coder
python artifact/human_validation/build_rater_forms.py     # rater_form_A.md, rater_form_B.md
# Send rater_form_{A,B}.md to the two raters. They fill them in independently.
python artifact/human_validation/ingest_rater_forms.py    # validate + merge into the CSVs
python artifact/human_validation/analyze_labels.py        # agreement, alpha, disagreements
```

Raters read evidence with:

```bash
python artifact/human_validation/show_packet.py PKT-07              # list packet contents
python artifact/human_validation/show_packet.py PKT-07 --readme     # line-numbered README
python artifact/human_validation/show_packet.py PKT-07 --file eval/eval.py
```

`ingest_rater_forms.py` refuses any submission with a blank label, an invalid
label, a missing evidence pointer, an unanswered item, or an unknown item, and
writes `frozen_submissions.json` with a SHA-256 of each completed sheet. That
hash is what "frozen" means: adjudication and unsealing happen only after it
exists for both raters.

## Blinding

`packet_key.json` maps packet IDs back to release names. **Do not send it to
the raters and do not open it yourself while coding is in progress.** It is
generated locally by `build_rater_forms.py` and is only unsealed after both
submissions are hashed. Packet contents may still reveal a release's identity
(a README often names its own repository); that is acceptable and matches what
the model judges saw. What must not leak is any label, ours or the other
rater's.

The analysis refuses blank or invalid labels, checks complete one-to-one
coverage, computes agreement and nominal Krippendorff alpha, bootstraps by
benchmark, derives coder-specific permissive R2, and writes disagreements for
adjudication.

## Acceptance gate

- 156/156 cells completed by each coder with evidence pointers.
- Nominal Krippendorff alpha at least 0.80 for the six primary criteria.
- Fewer than 15% of cells require adjudication.
- Adjudication is completed without consulting model labels.
- Human-coded R2 replaces model-coded R2 in the paper and generated artifacts.

## Completed outcome

Both raters completed all 156 cells with evidence pointers, but the reliability
gate failed: exact agreement was 59.6%, nominal Krippendorff alpha was 0.432
(clustered 95% CI [0.299, 0.556]), and 63/156 cells required adjudication.
Across the two humans and three model coders, none of the ten coder pairs
reached alpha 0.80. The six-way R2 instrument is therefore released as a
negative validation result and is not presented as validated ground truth.

Authoritative outputs:

- `frozen_submissions.json`: hashes of both completed submissions;
- `human_reliability_stats.json` and `human_diagnostics.json`: two-rater result;
- `five_coder_reliability.json`: all ten coder pairs;
- `human_gold_set.csv` and `gold_set_stats.json`: adjudicated descriptive set;
- `human_disagreements_for_adjudication.csv`: all 63 uncollapsed disagreements.

The proposed binary artifact-anchored replacement has not been prospectively
validated and is described as a proposed remedy, not as a measured result.
