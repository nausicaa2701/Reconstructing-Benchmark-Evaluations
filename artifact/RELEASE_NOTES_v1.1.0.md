# Artifact v1.1.0 Release Notes

Release date: 2026-07-27
DOI: [10.5281/zenodo.21617013](https://doi.org/10.5281/zenodo.21617013)

## What changed

- Added the completed two-rater human validation, adjudication, and five-coder
  reliability result to the top-level artifact documentation.
- Added machine-readable results for the targeted seven-release
  official-environment diagnostic.
- Added `execution/fixtures/evaluation_levels.csv`, the authoritative
  per-release L1/L2/L3 accounting over all 26 releases.
- Defined L1/L2/L3 cumulatively while retaining a mutually exclusive
  `highest_level` field.
- Added an automated validator that cross-checks portable outcomes,
  official-environment outcomes, fixture status, hierarchy, counts, and
  evidence paths.
- Integrated evaluation-level validation into `artifact/reproduce.py --check`.
- Updated the citation metadata to the current paper title and DOI.

## Counts fixed by the source-of-truth table

- Portable protocol: cumulative L1/L2/L3 = 7/4/1.
- Targeted official-environment diagnostic: 7 tested, 4 pass.
- Union over all tested environments: cumulative L1/L2/L3 = 10/5/1.
- Mutually exclusive highest levels among the ten L1 releases:
  L1-only=5, L2=4, L3=1.

## What did not change

This release does not rewrite the frozen audit:

- primary cohort: 26 releases;
- repository resolution: 30/35;
- descriptive model-panel R2: 13/26;
- portable E3 first pass: 5/26;
- portable E3 after repair: 7/26.

The official-environment runs, golden fixtures, and human validation remain
dated follow-up layers with their provenance preserved.

## Verification

```bash
python artifact/execution/fixtures/verify_golden_fixtures.py
python artifact/execution/fixtures/validate_evaluation_levels.py
python artifact/reproduce.py --check
python tools/build_release_manifest.py --verify
```
