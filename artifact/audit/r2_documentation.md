# Evidence-Grounded Three-Provider Model Panel — R2

**Audit date:** 2026-07-13. **Panel run:** 2026-07-16--17.
**Corpus:** 26 frozen releases. **Codebook:** v1.0.0.

## Protocol

Three heterogeneous model judges independently coded the same six criteria for
all 26 primary releases (156 cells; 468 raw decisions):

- OpenAI `gpt-5.1-2025-11-13`, low reasoning;
- Anthropic `claude-sonnet-5`, low effort;
- Google `gemini-3.5-flash`, low thinking.

Each judge received an identical pseudonymous packet containing only frozen,
line-numbered official repository artifacts. Browsing, tools, benchmark names,
other judges' labels, and outcomes were unavailable. Every decision required a
source ID and valid line range; local validation rejected missing, unknown, or
out-of-range evidence pointers.

No LLM adjudicator was used. Exact majority determines the aggregate label. A
three-way tie uses a deterministic conservative rule: select the weaker label
on the side supported by at least two judges at the permissive pass/fail
boundary. The released code reproduces majority, strict, unanimous,
leave-one-judge-out, pairwise, and clustered-bootstrap analyses.

## Protocol history

A default-thinking Gemini pilot was excluded wholesale after reasoning tokens
crowded structured JSON out of the output cap. All 26 Gemini production packets
were rerun with low thinking. The OpenAI/Anthropic portion of the preselected
six-release repeat increased only the HTTP timeout from 180 to 600 seconds;
model, prompt, schema, packets, and inference settings were unchanged. Gemini
repeat completed under the original timeout. The release preserves the excluded
pilot, superseded partial repeat, manifests, raw responses, errors, and usage.

## Agreement and repeatability

| Statistic | Result |
|---|---:|
| Nominal Krippendorff alpha, all 156 cells | 0.471 |
| Benchmark-cluster bootstrap 95% CI | [0.373, 0.548] |
| Exact unanimous, all labels | 46.8% |
| Binary alpha, five R2 criteria | 0.622 |
| Binary Gwet AC1, five R2 criteria | 0.806 |
| Binary pairwise agreement, five R2 criteria | 86.2%--88.5% |
| Binary unanimous, five R2 criteria | 80.8% |
| Test--retest exact agreement, preselected sample | 84.3% |
| Test--retest binary agreement, preselected sample | 93.5% |

The pre-specified nominal-alpha target of 0.80 was not met. These are
**inter-model** and test--retest statistics, not human inter-rater reliability
and not validation against ground truth. R2 is therefore an LLM-assisted
descriptive outcome; A1 and E3 remain the paper's stronger static/executable
outcomes.

## R2 sensitivities

R2 uses five criteria: input/output schema, metric definition, evaluator
implementation, grading/tie-breaking, and predictions-to-score mapping. Sample
predictions are coded but assigned to E3 rather than R2.

| Rule | R2 |
|---|---:|
| Deterministic majority, permissive | 13/26 |
| Deterministic majority, strict | 1/26 |
| All three judges permissive | 7/26 |

Leaving out one judge gives pessimistic two-judge counts of 7--10 and optimistic
counts of 14--17. The sensitivity is reported rather than collapsed into a
single validated estimate.

## Released evidence

`model_panel_v1/` contains frozen packets, raw provider responses, normalized
line-level judgments, deterministic aggregates, panel statistics,
repeatability outputs, run manifests, usage ledgers, protocol history, and a
SHA-256 manifest. The earlier same-vendor two-model coding files remain in the
artifact as superseded provenance and are not the paper's final R2 source.
Recorded API spend across production, pilots, retries, and repeat runs was
$3.2361; no local GPU was used.
