# Reviewer Red-Team Report (Phase 9)

> **Historical review, updated on 2026-07-17.** The original review below
> predates completed re-screening and the heterogeneous three-provider panel.
> The mechanical submission gate now passes; R2 remains explicitly descriptive
> because nominal inter-model alpha is below 0.80.

**Audit date:** 2026-07-13
**Manuscript:** Reconstructing Benchmark Evaluations: A Public-Artifact Audit of
Foundation-Model Benchmarks for Data Science
**Reviewer instruments:** three independent mock reviews from distinct
perspectives (benchmark/evaluation researcher; reproducibility/statistics
researcher; skeptical KDD Datasets & Benchmarks reviewer), each scoring the full
manuscript against the Phase 9 review questions.

## Scores

| Reviewer role | Score (/10) | Novelty clear | Survey/checklist objection survivable |
|---|---|---|---|
| Benchmark & evaluation researcher | 6 | yes | yes |
| Reproducibility & statistics researcher | 6 | yes | yes |
| Skeptical KDD reviewer | 5 | yes | yes |
| **Median** | **6** | — | — |

Target: median mock-review score >= ~6/10 — **met**. No reviewer raised a
**fatal** objection. Concern census: 11 major, 7 minor, 3 editorial (across
reviewers, with substantial overlap; consolidated to 14 distinct themes in the
resolution table).

## Acceptance criteria (Phase 9)

- **No unresolved fatal objection about novelty, selection bias, validity, or
  overclaiming.** Met — zero fatal concerns; all three reviewers judged novelty
  clear and the survey/checklist objection survivable.
- **Every major concern has a documented response.** Met — see
  `resolution_table.json`; each of the five recurring major themes maps to an
  acknowledged limitation, a pre-specified mitigation, or a text fix.
- **Independent reviewers describe the central contribution consistently.**
  Met — all three summaries independently describe the same three-level
  audit (accessibility / reconstructability / CPU-only executability) over 26
  frozen releases with a released evidence trail.
- **Median mock-review score >= ~6/10.** Met (median 6).
- **Artifact passes independent reproduction testing.** Met earlier — a
  fresh-clone run regenerated all main tables and figures from the frozen
  dataset (Phase 7).
- **Survives the "merely a survey/checklist" objection.** Met — unanimous.

## Recurring major concerns and disposition

1. **LLM coding below the 0.80 nominal reliability target, no human ground
   truth** (all three reviewers). Disposition: R2 is secondary/descriptive;
   majority, strict, unanimous, leave-one-out, pairwise, and repeatability
   analyses plus every raw judgment are released. No ground-truth claim is made.
2. **Same model family -> possible correlated blind spots** (stats reviewer).
   Mitigated with independently operated OpenAI, Anthropic, and Google judges;
   correlated training-data blind spots remain acknowledged in Limitations.
3. **Minimal-repair discretion moves the primary endpoint (5 -> 7 / 26)**
   (two reviewers). The revised paper makes first-pass the least discretionary
   estimate and repaired E3 a sensitivity analysis; every patch is released.
4. **Small N, sparse category cells, OR ≈ 10.3 may be over-read** (all three).
   Already mitigated: category comparisons and the association are labeled
   exploratory with non-significant p-values inline; a new benchmark-family
   pseudo-replication caveat was added to Limitations.
5. **Single-pass corpus screening -> selection bias** (skeptical reviewer).
   Acknowledged; exclusion framed as inability to resolve the official artifact
   in this pass. This disposition was inadequate and is superseded by the
   35-candidate screening frame, 30/35 completed resolution yield, and a declared
   26-release primary cohort plus four-release post-freeze sensitivity.

## Text changes made in response

- **Table 3 caption** now defines the `R2 crit`, `R2`, `E3 fp`, `E3 rep`, and
  `E3` columns (was undefined — minor concern, benchmark reviewer).
- **Limitations** gained a *Shared benchmark lineage* paragraph noting the
  Spider / BIRD / DS-1000–CERT families and the resulting partial
  pseudo-replication relative to exchangeable-unit intervals (major concern,
  stats reviewer).
- **Results / reliability** now states the nominal alpha is the pre-specified
  primary metric and the ordinal alpha and Gwet AC1 are post-hoc
  characterizations, not a re-choice of endpoint (editorial concern, stats
  reviewer — "metric shopping").
- **QRData case study** runtime corrected to 0.04 s to match the frozen
  execution manifest.

## Deferred to camera-ready

- Persistent artifact identifier / DOI in the manuscript body (kept neutral for
  single-blind review; availability statement already present).

## Gate outcome

**CONDITIONAL PASS.** Screening, static evidence, CPU execution, panel release,
repeatability, reproduction, and build gates pass. The failed nominal R2
reliability gate is retained as a disclosed limitation, not relabeled as human
reliability or validated measurement.
