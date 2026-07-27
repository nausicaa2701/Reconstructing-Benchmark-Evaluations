# Evaluator-Level Accounting

This note fixes the denominator and hierarchy for every L1/L2/L3 statement.
The machine-readable source of truth is
`artifact/execution/fixtures/evaluation_levels.csv`; this note is explanatory.

## Definitions

- **L1 invoked:** an official scorer accepted the supplied input, exited
  successfully, and emitted or wrote a score in at least one tested environment.
- **L2 fixture-matched:** the emitted value matched an expected value obtained
  independently of that audit execution.
- **L3 published-score reproduced:** the scorer reproduced an author-published
  value for a released prediction set.

The summary uses cumulative levels: L3 implies L2, and L2 implies L1. The
`highest_level` column is the mutually exclusive representation.

## Two denominators

The frozen portable protocol and the later official-environment diagnostic
answer different questions:

| Scope | L1 | cumulative L2 | cumulative L3 |
|---|---:|---:|---:|
| Portable protocol, all 26 releases | 7 | 4 | 1 |
| Union of all tested environments, all 26 releases | 10 | 5 | 1 |
| Conditional on the 10 releases reaching L1 anywhere | 10/10 | 5/10 | 1/10 |

The three additional L1 releases in the union are CERT, MLGym, and
WikiTableQuestions. They ran only in the targeted official-environment
diagnostic. WikiTableQuestions also reaches L2.

## Mutually exclusive highest levels

Among the ten releases that reach L1 in any environment:

- five are L1-only: CERT, InfiAgent-DABench, MLGym, ScienceAgentBench, TableBench;
- four have L2 as their highest level: DSBench, QRData, SpreadsheetBench,
  WikiTableQuestions;
- one reaches L3: DS-1000.

DS-1000 counts in cumulative L2 because the release's published score supplies
an expected value independent of the audit execution.

## Canonical artifact-facing wording

> Seven releases produced a score in the shared portable environment. Rebuilding
> the documented environment for the seven failures initially attributed to
> dependencies or environment added three distinct score-producing releases,
> so ten of 26 produced a score in at least one tested environment. Five of
> those ten matched an independently established expected value, including
> DS-1000, which reproduced an author-published score.

Do not use “three L2” without qualifying it as “three non-L3 portable releases.”
For a cumulative correctness ladder, the portable count is L1/L2/L3 = 7/4/1
and the any-tested-environment count is 10/5/1.

## Automated checks

Run:

```bash
python artifact/execution/fixtures/validate_evaluation_levels.py
python artifact/reproduce.py --check
```

The validator checks cohort identity, portable E3 fields, official-environment
selection and outcomes, hierarchy, highest-level labels, expected counts, and
the existence of every evidence path.
