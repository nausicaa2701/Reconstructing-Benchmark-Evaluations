# Automated Public-Artifact Accessibility Audit — A0 / A1 (Phase 4a)

**Audit date:** 2026-07-13. **Cohort:** 26 repository-resolved frozen releases
from a 35-candidate screening frame.

## Method

1. **Reachability probe.** Every paper URL (`arxiv.org/abs/<id>`) and repository
   URL was fetched over HTTP; status and final (post-redirect) URL recorded.
   All 51 targets returned HTTP 200.
2. **Repository scan.** Each repository was cloned at its frozen commit with a
   blobless, depth-1 filter (`--filter=blob:none --depth 1`), and its file tree
   was scanned with path heuristics for six artifact classes: evaluator code,
   dataset/data (including compressed archives), sample predictions,
   environment/dependency files, container files, and license.

The scan is a **presence detector over public file paths**, not a semantic
judgment; ambiguous cells are re-examined by the reconstructability coding pass
(Phase 4b). Two detection gaps were found and fixed during validation:
compressed data archives (`data.tar.gz`, e.g. Dr.Spider) and preprocess/predict
scripts acting as evaluators were initially missed and added to the patterns.

## Results

- **A0 Described:** 26 / 26. Every release has a public paper or, for the
  repository-primary SQL-eval tool, a public technical README.
- **A1 Accessible:** 26 / 26. Every repository is publicly reachable at its
  frozen commit and exposes at least an evaluator or dataset artifact.

Artifact-class presence rates across the 26 repositories:

| Artifact class | Present |
|---|---|
| Evaluator code | 100% |
| Dataset / data | 96% |
| Environment / dependency file | 81% |
| Sample predictions | 50% |
| Container file | 27% |
| License | 88% |

**Interpretation.** Conditional on repository resolution, papers and repositories
are reachable and expose core artifacts. This 26/26 result is structural and
must not be generalized to all 35 candidates. Completed repository resolution
was 30/35; four post-freeze releases are reported separately as an expansion
sensitivity. Sample predictions (50%) and container files (27%) are sparse in
the primary cohort.
These classes directly affect downstream reconstructability and smoke testing.

## Evidence files

- `raw_labels/a1_artifact_scan.csv` — per-benchmark presence flags + file counts.
- `evidence/a1_scan_detail.json` — up to 12 matched paths per artifact class per
  benchmark (the concrete evidence pointers).
- `adjudicated/a0_a1_outcomes.csv` — derived A0/A1 outcomes with the supporting
  detection flags.
