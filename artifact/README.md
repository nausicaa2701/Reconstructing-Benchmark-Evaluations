# Public-Artifact Audit of Foundation-Model Benchmarks for Data Science

Evidence dataset and analysis pipeline for the paper
*"Auditing Public Evaluation Specifications and Scorer Smoke-Testability:
A Public-Artifact Audit of Foundation-Model Benchmarks for Data Science"*
(KDD 2027 Datasets and Benchmarks Track).

**Stable archive DOI (all versions):** [10.5281/zenodo.21617012](https://doi.org/10.5281/zenodo.21617012)

**Artifact version:** v1.1.3

**Primary audit date:** 2026-07-13 · **Expansion audit:** 2026-07-16 ·
**Screening frame:** 35 candidates · **Primary cohort:** 26 frozen releases ·
**Post-freeze expansion:** 4 releases ·
**Codebook:** v1.0.0 (sha256 `aa57e2b3...`)

## What this artifact contains

This artifact releases the complete evidence chain behind every audit decision, so that
each reported result can be traced from the paper back to its source. It is engineered to
meet a higher public-reproducibility standard than the artifacts it audits.

The central question: *given only a benchmark paper and its public materials, can an
independent researcher reconstruct the evaluation protocol and run its evaluator without
foundation-model inference?* Repository resolution is reported for the full
screening frame. R2 and E3 are conditional on the repository-resolved cohort.

## Headline results

| Outcome | Result | 95% CI |
|---|---|---|
| Official repository resolved | 30/35 (85.7%) | [70.6%, 93.7%] |
| R2 Reconstructable (permissive) | 13/26 (50%) | [32.1%, 67.9%] |
| **E3 as documented** | **5/26 (19.2%)** | **[8.5%, 37.9%]** |
| E3 after documented repair | 7/26 (26.9%) | [13.7%, 46.1%] |

E3 above is the frozen **portable-environment** endpoint. A targeted
official-environment diagnostic subsequently rebuilt all seven releases whose
portable failure had been labelled dependency/environment: 4 ran, while 3
stopped on corrected data-access or privileged-runtime blockers. None of the
seven original environment attributions survived. This was a selected
failure-label diagnostic, not an official-environment audit of the full cohort.

### Authoritative evaluator-correctness ladder

`execution/fixtures/evaluation_levels.csv` is the source of truth for all
L1/L2/L3 counts. It distinguishes the seven releases producing a score in the
portable protocol from the ten producing a score in any tested environment.
Levels are cumulative: L3 implies L2, and L2 implies L1.

| Scope | L1 invoked | L2 fixture-matched | L3 published-score reproduced |
|---|---:|---:|---:|
| Portable protocol | 7/26 | 4/7 | 1/7 |
| Any tested environment | 10/26 | 5/10 | 1/10 |

The mutually exclusive highest-level counts over the ten releases are
L1-only=5, L2=4, and L3=1. `validate_evaluation_levels.py` cross-checks the
table against frozen E3 outcomes, official-environment results, fixture status,
the cumulative hierarchy, and every evidence path.

The declared 30-release expansion sensitivity gives R2 16/30, first-pass E3
8/30, and repaired E3 10/30. Primary outcomes remain tied to the frozen
26-release cohort because the additional repositories were found after those
outcomes were known.

## Repository layout

```
artifact/
  README.md              this file
  LICENSE                CC-BY-4.0 (our evidence data + code)
  CITATION.cff           citation metadata
  reproduce.py           single-command reproduction interface
  OUTPUT_HASHES.json     sha256 of released main-paper outputs
  environment/           frozen environment specs (analysis + e3smoke)
  schema/                codebook v1.0.0, audit-record + dataset JSON schemas
  corpus/                candidate registry, inclusion/exclusion, frozen manifest
  audit/
    raw_labels/          A1 scan and superseded two-model R2 provenance
    adjudicated/         adjudicated A0/A1 and superseded R2 provenance
    model_panel_v1/      released three-provider R2 panel + repeatability study
    evidence/            per-release evidence bundles, artifact-scan detail
    e3/                  E3 outcomes, per-record detail, execution log bundle
  execution/
    manifests/           one manifest per attempted smoke test (commit, cmd, label)
    logs/                raw first-pass / repair-pass logs
    patches/             minimal-repair scripts (bounded runner, DS-1000 shim)
    containers/          (reserved; smoke tests ran in conda env e3smoke)
  analysis/              master analysis dataset, RQ stats, concordance
  figures/               all paper figures (.png + .pdf)
  tables/                all paper tables (.csv + .tex)
  docs/                  research contract, novelty positioning,
                         maintainer verification + corpus maintenance policy
  human_validation/      blinded two-rater R2 coding instrument (not yet executed)
  execution/fixtures/    authoritative L1/L2/L3 table, fixtures, and validator
  environment/           frozen envs + per-release official-environment specs
  MANIFEST.sha256        sha256 of every released file
  MANIFEST.json          release version, paper PDF hash, frozen vs living layer
```

## Validation status (read this before citing a number)

| Layer | Status |
|---|---|
| A1 accessibility | measured |
| R2 model-panel coding | measured; reliability gate missed |
| R2 human criterion validation | completed; two raters, all 156 cells; reliability gate missed |
| E3 L1 invocation (portable env) | measured: 5/26 first-pass, 7/26 after repair |
| E3 L1 invocation (any tested env) | measured: 10/26 |
| E3 L2 golden-fixture match | measured: 5/10 cumulatively; 4 have L2 as highest level |
| E3 L3 published-score reproduction | measured: 1/10 (DS-1000) |
| E3-official diagnostic | completed for all 7 portable environment-labelled failures; 4 pass |
| Maintainer confirmation / dispute | protocol released, **no release contacted** |

Anything marked *not executed* is released as a runnable instrument with a
pre-registered analysis, so that its result cannot be chosen after seeing the
data. No paper claim rests on it.

## Frozen vs living layers

`corpus/`, `audit/`, `execution/logs/`, and `execution/manifests/` are
**append-only** and reproduce every number in the paper. Corrections, maintainer
responses, human labels, official-environment runs, and re-audits accumulate in
the dated living layer and never rewrite the frozen record. See
`docs/maintenance_policy.md`.

## Reproduction

From the repository root, in an environment with `numpy scipy pandas matplotlib`:

```bash
python artifact/reproduce.py --check       # validate schema, recompute stats, verify hashes
python artifact/reproduce.py --regenerate  # regenerate headline outputs and hashes
```

`--check` validates the master dataset, recomputes conditional R2/E3 statistics,
checks the 30/35 completed screening yield, validates both the primary and
expanded datasets, verifies released output hashes, and validates the
authoritative L1/L2/L3 table.

To regenerate the data-driven figures from the frozen dataset:

```bash
python artifact/analysis/build_extended_analysis.py  # blocker taxonomies, artifact-presence
                                                     # association, lineage robustness
python artifact/make_tex_figures.py                  # writes figures/fig_*.tex (paper figures)
python artifact/make_figures.py                      # optional: fig_*_repro.png cross-checks
```

The paper's figures are native TikZ/pgfplots sources (`figures/fig_*.tex`) generated from the
frozen data and `\input` by the manuscript, so they are exactly reproducible, diffable, and update
by rerunning the generator after any data change. Shared styling lives in `figures/figstyle.tex`;
`fig_instrument_structure.tex` is a hand-maintained schematic. The legacy matplotlib script is kept
as an independent cross-check of the same values; its raster output is verified by data content,
not file hash.

Evaluator smoke tests are replayed separately -- see `execution/README.md` -- because they depend on
heterogeneous external artifacts. Each attempted benchmark has a manifest (frozen commit + command +
label) under `execution/manifests/`.

## Evidence and provenance

Every audit decision records: benchmark + release id, frozen commit, source URL/path, file/line
pointer, access date, evidence note, raw judgment, deterministic aggregate, and disagreement or
repair explanation. The final R2 panel (`audit/model_panel_v1/`), superseded
model-coding provenance, and analysis-ready dataset (`analysis/master_outcomes.csv`)
are kept separate.

## Reliability

R2 was coded independently by three model providers and two blinded human
raters, none of whom saw another coder's work. Model-panel nominal alpha is
0.471 (95% CI [0.373, 0.548]); human-human alpha is 0.432 (clustered 95% CI
[0.299, 0.556]). Across all five coders, none of the ten pairs reaches the
pre-specified 0.80 gate (pairwise alpha 0.371--0.503), and 63/156 human-coded
cells required adjudication. R2 therefore remains descriptive rather than
validated ground truth. The two completed rater files, their uncollapsed
disagreements, adjudication, five-coder statistics, model prompts, packets, raw
responses, and line-level evidence are released.

## Redistribution and licenses

We do **not** redistribute third-party benchmark data or code. The corpus manifest
(`corpus/corpus_frozen.csv`) records each release's owner, repository, frozen commit, and license so
that any third-party artifact can be retrieved at its exact audited state. Our own evidence data,
analysis code, tables, and figures are released under CC-BY-4.0 (see `LICENSE`).

## Scope note

These outcomes measure public evaluation reconstructability at a frozen commit
and date. Cohort rates are conditional on repository resolution and are not a
universal ranking or population prevalence estimate.
