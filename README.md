<div align="center">

# Auditing Public Evaluation Specifications and Scorer Smoke-Testability

**A public-artifact audit toolkit and evidence dataset for foundation-model benchmarks in data science**

<p>
  <img src="https://img.shields.io/badge/Status-v1.1.0-ff6b35?style=for-the-badge" alt="Status: v1.1.0" />
  <img src="https://img.shields.io/badge/Type-Audit%20Dataset%20%2B%20Pipeline-7c3aed?style=for-the-badge" alt="Audit Dataset and Pipeline" />
  <img src="https://img.shields.io/badge/Platform-Python-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python Platform" />
  <img src="https://img.shields.io/badge/License-CC--BY--4.0-lightgrey?style=for-the-badge" alt="License: CC-BY-4.0" />
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" alt="SciPy" />
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</p>

</div>

## Overview

This repository is a **public-artifact audit** of foundation-model benchmarks for data-science tasks. It asks whether a benchmark's public materials (docs, repos, datasets, evaluators) specify the evaluation well enough for an independent party to invoke the official evaluator — without foundation-model inference.

It also asks a question one level up, which turned out to be the study's main result: **is "adequately documented" a property that coders can agree on at all?** The same 156 benchmark-criterion cells were coded twice from identical frozen evidence — by three model judges from different providers, and by two blinded human raters under a pre-registered acceptance gate. **Both panels missed the same gate** (nominal Krippendorff's α = 0.471 and 0.432 against a ≥0.80 target), with 62% of human disagreement falling on one codebook seam: fully versus partially documented. The model panel matched individual human raters about as well as the raters matched each other, so this is a property of the construct rather than of the judges.

The release therefore ships the negative result with its full evidence: both completed rater files, all 63 disagreements uncollapsed, the adjudicated 156-cell gold set, and the model-versus-gold confusion matrix. Alongside them are the frozen corpus registry, line-addressable evidence packets, three-provider model judgments, golden fixtures with independently derived expected values, official-environment build specifications, CPU-only smoke-test logs, minimal-repair patches, and a single-command pipeline that validates schemas, recomputes statistics, and verifies output hashes.

It is **not** a benchmark-quality ranking, a leaderboard reproduction, or a population prevalence estimate.

## Audit Ladder

The audit defines four release-level outcomes:

| Level | Name | Meaning |
|---|---|---|
| A0 | Described | A public technical description of the benchmark exists |
| A1 | Accessible | Core referenced artifacts are publicly reachable |
| R2 | Sufficiently documented | Consequential evaluation details are documented without unsupported guesses (descriptive — see reliability note below) |
| E3 | Smoke-testable | Official evaluator produces a score/result from supplied or schema-valid synthetic predictions (CPU-only) |

The protocol, sensitivity analyses, and limitations are documented in [`artifact/docs/research_contract.md`](./artifact/docs/research_contract.md).

## Repository Layout

```text
reconstructing-benchmark-evaluations/
├── artifact/                 # Evidence dataset + analysis pipeline
│   ├── corpus/               # Screening frame, frozen release registry
│   ├── schema/               # Codebook v1.0.0 + JSON schemas
│   ├── audit/                # Evidence packets, R2 model panel, E3 records
│   ├── llm_judges/           # Three-provider judge runner (optional replay)
│   ├── execution/            # Smoke-test manifests, logs, repair patches
│   ├── analysis/             # master_outcomes.csv + stats pipeline
│   ├── figures/              # Generated TikZ/PNG figure sources
│   ├── tables/               # Generated CSV/TeX tables
│   ├── human_validation/     # Blinded two-coder study + adjudicated gold set
│   ├── redteam/              # Internal red-team report + resolution table
│   ├── environment/          # Frozen analysis + e3smoke envs, official-env builds
│   ├── docs/                 # Protocol contract and amendments
│   ├── reproduce.py          # Single-command reproduction interface
│   └── OUTPUT_HASHES.json    # SHA-256 of released outputs
├── CITATION.cff
├── LICENSE                   # CC-BY-4.0 (original contributions)
└── README.md
```

## Current App Structure

Inside [`artifact/`](./artifact/):

- [`corpus/`](./artifact/corpus/) — 35-candidate screening frame, PRISMA counts, frozen 26-release primary cohort (+ 4 post-freeze extensions)
- [`schema/`](./artifact/schema/) — codebook v1.0.0, audit-record and master-outcomes schemas
- [`audit/model_panel_v1/`](./artifact/audit/model_panel_v1/) — evidence packets, prompts, raw + aggregated judgments from three independently operated model judges, repeatability runs, usage ledgers
- [`execution/`](./artifact/execution/) — CPU-only smoke-test manifests, redacted logs, minimal-repair patches
- [`analysis/`](./artifact/analysis/) — `master_outcomes.csv`, phase stats, expanded sensitivity, extended analyses
- [`llm_judges/`](./artifact/llm_judges/) — optional tooling to prepare packets and re-run the judge panel (API keys required)
- [`reproduce.py`](./artifact/reproduce.py) — validate, recompute, regenerate tables/figures, verify hashes

## Current Status

**Implemented:**

- Frozen screening of 35 candidates; primary audit cohort of 26 releases (audit date 2026-07-13)
- Full evidence chain: packets, labels, aggregation, execution manifests/logs
- Three-provider R2 panel (OpenAI / Anthropic / Gemini) with released raw outputs and repeatability study
- CPU-only E3 smoke protocol with first-pass and documented minimal-repair passes
- `reproduce.py --check` / `--regenerate` for schema validation, stats recomputation, table/figure rebuild, and hash verification
- Expanded sensitivity outcomes for a 30-release declared extension cohort
- **Completed blinded two-rater human study**: all 156 cells coded twice, sealed-key protocol, 63 disagreements adjudicated by a third coder who was neither rater, and the resulting gold set released
- **Golden fixtures** pairing four scoring releases with expected values derived without running the scorer under test; one release reproduces its published score
- **Official-environment baselines**: per-release containers built only from each release's own documented setup, for the releases whose portable outcome was in doubt

**Still pending:**

- Maintainer confirmation/dispute study (protocol released, no responses collected)
- Official-environment baselines for the releases blocked by credentials, services, or missing data (14 releases; their labels should not depend on our provisioning, but that is unverified)
- Head-to-head execution of comparison frameworks on an overlap set
- CI workflow (not configured yet)
- Packaging as an installable Python project (`pyproject.toml` / pinned `requirements.txt` at repo root)

### Headline results (26 frozen releases)

| Endpoint | Result | Wilson 95% | Lineage-clustered 95% |
|---|---|---|---|
| Official repository resolved | 30/35 (85.7%) | [70.6%, 93.7%] | — |
| R2 documented (permissive, model panel) | 13/26 (50.0%) | [32.1%, 67.9%] | [32.1%, 71.4%] |
| R2 documented (strict) | 1/26 (3.8%) | [0.7%, 18.9%] | — |
| E3-portable: evaluator runs as documented | 5/26 (19.2%) | [8.5%, 37.9%] | [5.3%, 38.1%] |
| E3-portable after documented minimal repair | 7/26 (26.9%) | [13.7%, 46.1%] | [11.1%, 47.6%] |

Lineage-clustered bootstrap intervals over the 21 independent lineages are the intervals of record; Wilson intervals treat the 26 releases as exchangeable and are retained as conditional descriptive summaries. Declared 30-release expansion sensitivity: R2 16/30, first-pass E3 8/30, repaired E3 10/30.

### Reliability of the R2 coding — read this before using the R2 numbers

| Statistic | Model panel (3 judges) | Human panel (2 raters) |
|---|---|---|
| Exact agreement | 46.8% | 59.6% |
| Nominal Krippendorff's α | 0.471 | 0.432 |
| Pre-registered gate | ≥0.80 — **missed** | ≥0.80 — **missed** |
| Cells requiring adjudication | — | 63/156 (40.4%), gate was <15% — **missed** |

Against the adjudicated 156-cell gold set the model panel is 60.3% exact (95% CI [52.4%, 67.6%]) and 81.4% at the permissive binary boundary. Its accuracy on the 93 cells where both raters already agreed is 74.2%, but only 39.7% on the 63 cells that needed adjudication — so any accuracy figure computed on agreed cells alone is optimistic. The model panel and the human gold set both yield **13/26** at corpus level while disagreeing about *which* releases pass on 8 of 26, which is why an identical headline is not evidence of validity.

**Use R2 as a descriptive, binary indicator with the 7–16/26 coder interval attached.** Do not use it as a validated measure of whether a release can be reconstructed. The uncollapsed disagreements are released so the boundary can be re-drawn.

### Evaluator correctness ladder

E3 establishes only that a scorer was invoked. The frozen portable protocol
produced a score for seven releases; the union over portable and targeted
official-environment runs produced a score for ten. Levels below are cumulative:
L3 implies L2, and L2 implies L1.

| Scope | L1 invoked | L2 fixture-matched | L3 published-score reproduced |
|---|---:|---:|---:|
| Portable protocol | 7/26 | 4/7 | 1/7 |
| Any tested environment | 10/26 | 5/10 | 1/10 |

The mutually exclusive highest-level counts among the ten score-producing
releases are L1-only=5, L2=4, and L3=1. DSBench mattered most here: its scorer
writes to `result.txt` and prints nothing to stdout, so exit 0 alone had carried
its L1 pass. DS-1000 reaches L3 — run in its own documented environment on the
predictions the release ships, it reproduces the shipped score file (mean 0.387
against a published 0.388, exactly one problem of 1000 differing).

The per-release source of truth is
[`artifact/execution/fixtures/evaluation_levels.csv`](./artifact/execution/fixtures/evaluation_levels.csv);
the automated validator prevents denominator or hierarchy drift.

### E3-portable under-attributes

E3 as reported is measured in one shared environment (`e3smoke`). We rebuilt the documented environment of all seven releases whose portable failure we had attributed to the environment. **None of those seven attributions survived.**

| Release | E3-official | Corrected blocker |
|---|---|---|
| DS-1000 | pass | — (also reproduces its published score) |
| CERT | pass | — |
| MLGym | pass | — |
| WikiTableQuestions | pass | — |
| MLE-bench | fail | missing required data (Kaggle-gated) |
| TabFact | fail | missing required data (documented link returns 404) |
| RE-Bench | fail | privileged runtime + GPU |

So E3-portable is a **portability** endpoint, not a verdict on the release: at least 10/26 evaluators run on CPU in some environment we tested, against the 5/26 the portable protocol reports. Build specifications and captured output are in [`artifact/environment/official_runs/`](./artifact/environment/official_runs/); per-release records with the exact findings are in [`artifact/environment/official_env_specs/`](./artifact/environment/official_env_specs/).

One correction runs the other way: TabFact's documented data source (`get_data.sh` → S3) returned HTTP 404 on 2026-07-27. We did not re-check it at the 2026-07-13 audit date, so it is filed as a **candidate A1 correction** under the maintenance policy rather than folded into the frozen record.

## Quickstart

### Prerequisites

- Python `>=3.11` recommended (analysis scripts use the standard scientific stack)
- `pip`

### Install

```bash
git clone https://github.com/nausicaa2701/reconstructing-benchmark-evaluations
cd reconstructing-benchmark-evaluations
python -m pip install numpy scipy pandas matplotlib jsonschema
```

Frozen environment pins for deeper replay live under [`artifact/environment/`](./artifact/environment/).

### Verify

```bash
python artifact/reproduce.py --check
```

This validates the master dataset against its schema, recomputes headline statistics, checks the model-panel release hashes, and verifies SHA-256 hashes of released outputs.

### Run Locally

```bash
python artifact/reproduce.py --regenerate   # rebuild tables, figures, and OUTPUT_HASHES.json
```

Optional figure / analysis helpers:

```bash
python artifact/analysis/build_extended_analysis.py
python artifact/make_tex_figures.py
python artifact/make_figures.py             # matplotlib cross-check PNGs
```

Evaluator smoke tests are **not** part of `reproduce.py`. They depend on heterogeneous external benchmark repositories at frozen commits — see [`artifact/execution/README.md`](./artifact/execution/README.md).

Optional R2 judge panel replay (API keys required):

```bash
cp artifact/llm_judges/.env.example artifact/llm_judges/.env
# fill OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
python3 artifact/llm_judges/prepare_packets.py
python3 artifact/llm_judges/test_panel.py
```

Details: [`artifact/llm_judges/README.md`](./artifact/llm_judges/README.md).

## Useful Docs

- [`artifact/README.md`](./artifact/README.md) — artifact contents, provenance, reliability notes
- [`artifact/docs/research_contract.md`](./artifact/docs/research_contract.md) — frozen outcome definitions and scope
- [`artifact/docs/protocol_amendment_2026-07-14.md`](./artifact/docs/protocol_amendment_2026-07-14.md) — dated protocol amendment
- [`artifact/schema/codebook_documentation.md`](./artifact/schema/codebook_documentation.md) — coding instrument
- [`artifact/execution/README.md`](./artifact/execution/README.md) — E3 smoke-test replay protocol
- [`artifact/llm_judges/README.md`](./artifact/llm_judges/README.md) — three-provider judge runner
- [`artifact/analysis/phase6_documentation.md`](./artifact/analysis/phase6_documentation.md) — analysis notes
- [`CITATION.cff`](./CITATION.cff) — citation metadata

## CI And Review

CI workflow is not configured yet.

Local review gates today are:

```bash
python artifact/reproduce.py --check
python artifact/llm_judges/test_panel.py   # when replaying the judge tooling
```

## Additional Teammate Context

### Project Overview

- **Stack:** Python analysis pipeline (`numpy`, `scipy`, `pandas`, `matplotlib`, `jsonschema`); optional multi-provider LLM judge runner
- **Data model:** release-level outcomes in `artifact/analysis/master_outcomes.csv`, validated against `artifact/schema/`
- **R2 coding:** LLM-assisted descriptive coding from a three-provider panel; nominal inter-model reliability missed its pre-specified gate, so R2 is descriptive rather than validated ground truth. Raw judgments, prompts, and packets are released for audit or replacement
- **E3 execution:** CPU-only, zero GPU-hours, zero paid model API calls during smoke tests; path-redacted logs; minimal repairs recorded separately from first-pass outcomes
- **Redistribution:** third-party benchmark code/data are **not** mirrored; each release is pinned by owner/repo/commit in `artifact/corpus/corpus_frozen.csv`
- **License:** original evidence, code, tables, and figures under **CC-BY-4.0** ([`LICENSE`](./LICENSE))

### Extending the audit

To audit a new benchmark release:

1. Pin a commit and register it in the corpus manifests
2. Build an evidence packet (see `artifact/audit/model_panel_v1/packets/` for format)
3. Code the criteria against `artifact/schema/codebook_v1.json`
4. Run the two-pass CPU smoke protocol in `artifact/execution/`

### Primary Entry Points

- Reproduction CLI: [`artifact/reproduce.py`](./artifact/reproduce.py)
- Master outcomes: [`artifact/analysis/master_outcomes.csv`](./artifact/analysis/master_outcomes.csv)
- Frozen corpus: [`artifact/corpus/corpus_frozen.csv`](./artifact/corpus/corpus_frozen.csv)
- Codebook: [`artifact/schema/codebook_v1.json`](./artifact/schema/codebook_v1.json)
- Model panel release: [`artifact/audit/model_panel_v1/`](./artifact/audit/model_panel_v1/)
- E3 manifests index: [`artifact/execution/manifests/INDEX.json`](./artifact/execution/manifests/INDEX.json)
- Output integrity: [`artifact/OUTPUT_HASHES.json`](./artifact/OUTPUT_HASHES.json)

## License And Citation

Original contributions are released under **CC-BY-4.0** (see [`LICENSE`](./LICENSE)). Cite via [`CITATION.cff`](./CITATION.cff).

## Contact

Thi-Hong-Cuc Le — Ho Chi Minh City University of Technology (HCMUT), Vietnam National University Ho Chi Minh City.
