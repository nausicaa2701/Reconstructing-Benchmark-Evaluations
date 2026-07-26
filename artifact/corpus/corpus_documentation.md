# Benchmark Corpus (Phase 2)

**Audit date:** 2026-07-13
**Unit of analysis:** one benchmark release at a frozen repository commit.

## Screening eligibility

A candidate enters the screening frame if the first two conditions hold:

1. It targets at least one data-science task in scope (DS code generation,
   text-to-SQL / database agents, tabular / spreadsheet analysis, ML
   experimentation / engineering, or end-to-end data-science agents).
2. It has a public paper or technical report (A0 candidate) **or** a public
   evaluator repository that is the primary release vehicle.
Repository resolution is a measured screening outcome, not a topical
eligibility condition.

## Repository-resolved audit cohort

Of 35 candidates, 26 had an official repository resolved and frozen before the
primary outcomes were known. These form the primary cohort. A completed
post-freeze rescreen resolved four additional official repositories and applied
the full A1/R2/E3 protocol to them. They are reported as an expansion
sensitivity rather than retroactively entering the primary cohort. Five
candidates remain unresolved and are not interpreted as true artifact absences.

## Freeze protocol

For every included release the frozen commit is the `HEAD` of the default branch
resolved with `git ls-remote https://github.com/<owner>/<repo> HEAD` on the
audit date (Git protocol, not the REST API, so no rate-limit truncation).
arXiv identifiers were confirmed by fetching each candidate id and matching the
returned title exactly, because relevance search returned wrong papers for
several homonymous titles (BIRD, Spider, TableBench, WikiTableQuestions,
MLE-bench, QRData were corrected this way).

## Composition

26 releases: 4 DS code-generation, 5 text-to-SQL/DB, 4 tabular/spreadsheet,
5 ML-experimentation/engineering, 8 end-to-end DS agents. Every stratum meets
the >=4 minimum, and the total exceeds the >=20 Go/No-Go threshold.

## Notes on specific entries

- **BIRD-CRITIC / SQL-eval** (`defog-ai/sql-eval`): a SQL-evaluation tool
  repository with no single dedicated arXiv paper; retained as a text-to-SQL
  evaluator release with `arxiv_id` left null and the condition recorded.
- **PandasEval/NumpyEval** are released inside the CERT repository
  (`microsoft/PyCodeGPT`, arXiv:2206.06888); the release is frozen at that repo.
- Display names follow each project's own capitalization.

## Files

- `corpus_frozen.csv` — the frozen corpus (benchmark, category, arxiv_id, repo,
  frozen_commit, repo_url, audit_date, paper_note).
- `corpus_excluded.csv` — candidates outside the initial repository-resolved cohort.
- `rescreening_ledger.csv` — post-freeze candidate links and required actions.
- `rescreened_release_coding.json` — criterion evidence and E3 decisions for
  the four-release expansion.
- `prisma_counts.json` — identification/inclusion counts.
