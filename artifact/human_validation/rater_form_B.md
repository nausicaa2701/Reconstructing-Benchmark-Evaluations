# R2 Human Coding Form — Rater B

You are coding **156 items**. Each item is one benchmark release paired with one
evaluation criterion. Work through them in the order given; the order is
deliberately shuffled so that you judge each criterion on its own evidence
rather than forming an impression of a release and carrying it across criteria.

## The question you are answering

For each item: **based only on the evidence packet, could an independent
researcher reconstruct this aspect of the evaluation without guessing?**

You are not judging whether the benchmark is good, whether its authors did
careful work, or whether the evaluation is sound. You are judging what the
public artifacts state.

## Rules

1. **Use only the evidence packet.** Do not search GitHub, the paper, or the
   web. If evidence is not in the packet, it is not available to you. This
   matches the constraint the model judges worked under.
2. **Do not discuss items with the other rater** until both forms are frozen.
3. **Do not look at** `artifact/audit/raw_labels/` or any model output. If you
   have already seen model labels for a release, say so now — you cannot rate
   it.
4. **Every item needs an evidence pointer**: a file path, section heading, or
   line range from the packet. For `not-documented`, the pointer is where you
   looked (`README.md, evaluate.py — no grading section`).
5. **Do not leave blanks.** If you genuinely cannot decide, pick the more
   conservative label and say why in the note. The analysis refuses blank cells.
6. Expect this to take **3–5 hours**. Split it across sessions; do not rush the
   last 40 items.

## The six labels

- `documented-and-verifiable` — Public evidence states this and you can verify it in the packet.
- `partially-documented` — Some of it is stated but a bounded gap remains that you would have to guess.
- `claimed-but-not-verifiable` — The release asserts it exists but the packet does not let you confirm it.
- `not-documented` — You searched the packet and found no statement of this.
- `not-applicable` — The criterion does not apply to this kind of evaluation.
- `access-blocked` — Evidence is behind credentials, a dead link, or a gated service.

## The hardest boundary

`partially-documented` vs `not-documented` drives the whole study, so be
deliberate here:

- **partially-documented** — you could get to a working reconstruction with one
  bounded, clearly-scoped assumption you could state in a sentence.
- **not-documented** — you would have to invent the behaviour, or you would
  need several assumptions, or you cannot tell which of two plausible
  behaviours the release means.

If you find yourself writing "probably it means…", that is `not-documented`.

## Evidence packets

Packets are in `artifact/audit/evidence/r2_evidence_bundles.json`, keyed by the
packet ID shown on each item. Each packet contains the release's README and its
evaluation-related source files at a frozen commit. Open it with:

```bash
python artifact/human_validation/show_packet.py <PACKET_ID>
```

Releases are identified only by packet ID. If you recognise a release from its
content, that is fine and expected — do not go looking for its name.

## How to fill this in

Edit this file directly. For each item, fill the three fields. Leave the
structure exactly as it is — the ingest script parses these markers.

When finished:

```bash
python artifact/human_validation/ingest_rater_forms.py
python artifact/human_validation/analyze_labels.py
```

---

## HB-001 — Metric definition

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** MLAgentBench/benchmarks/CLRS/env/evaluation.py:125-202
- **Note:** Per-type MSE, F1, categorical accuracy, and pointer accuracy are fully implemented.

---

## HB-002 — Input/expected-output schema

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** ai_rd_fix_embedding/assets/score.py:16,38-134,165-199; restricted_mlm/assets/score.py:18,88-154; triton_cumsum/assets/score.py:112-172
- **Note:** Paths, callable interfaces, and result dictionaries are exact for three tasks, not the full suite.

---

## HB-003 — Predictions->aggregate-score mapping

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** eval.py:169-204
- **Note:** Per-game and first-round group means are defined, but the release exposes several columns rather than one unambiguous reported benchmark number.

---

## HB-004 — Metric definition

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluator.py:3-46,57-82,300-316
- **Note:** Correctness is exact set-size equality plus normalized string, numeric, or date item matching.

---

## HB-005 — Predictions->aggregate-score mapping

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:16-29; discovery_eval.py:40-56
- **Note:** The imported evaluator returns a result, but no mapping to a single aggregate score is available.

---

## HB-006 — Evaluator implementation available

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** bixbench/graders.py:14-329
- **Note:** An identifiable grader for MCQ and open-ended answers is present with executable decision paths.

---

## HB-007 — Grading rules & tie-breaking

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** fix_embedding score.py:93-104,137-164; restricted_mlm score.py:88-123; triton_cumsum score.py:69-147
- **Note:** Load errors, disallowed operations, wrong shape/value, timeouts, and exceptions are defined for shown tasks; other task rules are absent.

---

## HB-008 — Input/expected-output schema

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** evaluation.py:18-27,100-139; README.md:88-103
- **Note:** Function-level DataPoint dictionaries and returned score fields are exact, but the top-level log-to-evaluation JSON file schema is not in the packet.

---

## HB-009 — Grading rules & tie-breaking

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** evaluation.py:43-56,133-188
- **Note:** Type/shape/name assertions, masked values, thresholds, and zero divisions are explicit, but top-level timeout/runtime-error grading is outside the packet.

---

## HB-010 — Predictions->aggregate-score mapping

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:7-12 — says results are aggregated; no aggregation code in packet
- **Note:** Aggregation is asserted without a denominator, weighting, or implementation.

---

## HB-011 — Predictions->aggregate-score mapping

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** 3SATTime/evaluate.py:20-37; bertMNLI/evaluate.py:61-75; blotto/evaluate.py:52-79
- **Note:** Exact totals/means are implemented for three tasks, but no benchmark-wide or remaining-task mapping is present.

---

## HB-012 — Sample predictions / trajectories

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:174-189; three grade.py files — no complete submission row
- **Note:** The packet references sample-submission files but contains no concrete evaluator-consumed submission.

---

## HB-013 — Metric definition

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:139-146; AI4Code/grade.py:9-35; alaska2-image-steganalysis/grade.py:43-99
- **Note:** Three competition metrics are implementable, but the release covers 75 competitions and most graders are absent from this packet.

---

## HB-014 — Grading rules & tie-breaking

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** compute_scores.py:28-63; calculate_metrics.py:16-55
- **Note:** Timeout, nonzero exit, missing output, evaluator exceptions, and best-run ties are defined, but task-specific success rules are unavailable.

---

## HB-015 — Evaluator implementation available

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** examples/DA-Agent/eval_closed_form.py:1-203
- **Note:** A complete identifiable evaluator loads responses, grades them, aggregates results, and writes output.

---

## HB-016 — Input/expected-output schema

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** discovery_eval.py:18-58
- **Note:** CLI input names/types and an output JSON path are exact, but the eval_result JSON fields are not defined.

---

## HB-017 — Sample predictions / trajectories

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; data_modeling/evaluation/*_eval.py — no prediction rows
- **Note:** No concrete CSV prediction example is included.

---

## HB-018 — Input/expected-output schema

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:14-17,22-47,49-50; README.md:7-19
- **Note:** tmp.json is a list with pred, answer, and meta_data.question_type, and the evaluator returns/prints one float.

---

## HB-019 — Predictions->aggregate-score mapping

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:20-47
- **Note:** Correct answers are divided by len(pred), so malformed predictions remain in the denominator.

---

## HB-020 — Evaluator implementation available

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** bigcodebench/evaluate.py:29-35,87-114,117-330
- **Note:** The orchestration is identifiable, but correctness checking and pass@k logic are imported from files not in the packet.

---

## HB-021 — Predictions->aggregate-score mapping

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:59-73
- **Note:** Pass@k values are reported without estimator formula, denominator, or local scoring code.

---

## HB-022 — Evaluator implementation available

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluator.py:1-370
- **Note:** The official evaluator and complete value normalization/matching machinery are identifiable in the packet.

---

## HB-023 — Grading rules & tie-breaking

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** bixbench/graders.py:58-108,155-206,223-277
- **Note:** Normalization, refusal, range, and invalid-mode behavior are explicit, but LLM decisions depend on omitted prompts and a range failure path is incomplete.

---

## HB-024 — Predictions->aggregate-score mapping

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluate.py:38-40,114-123
- **Note:** The reported score is exact successes divided by the intersection of gold and submitted instance IDs.

---

## HB-025 — Input/expected-output schema

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval.py:45-71,92-115,135-167; utils.py:68-99
- **Note:** The accepted log grammar and returned/output dataframe fields are stated and implemented.

---

## HB-026 — Predictions->aggregate-score mapping

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:211-230
- **Note:** The official accuracy is asserted without the test-suite denominator/aggregation implementation.

---

## HB-027 — Grading rules & tie-breaking

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** bigcodebench/evaluate.py:148-180,292-329; syncheck.py:14-21,84-102
- **Note:** Missing tasks, invalid pass_k, timeouts, empty code, and syntax errors have behavior, but final execution statuses are hidden in an omitted dependency.

---

## HB-028 — Grading rules & tie-breaking

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation.py:18-47,123-188,212-228
- **Note:** Missing/bad workbooks fail, blanks equal None, numbers round to two decimals, datetimes normalize, and all specified cells/ranges must match.

---

## HB-029 — Predictions->aggregate-score mapping

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation.py:125-139; 100-122
- **Note:** The global score is the unweighted mean of all output scores; hint time aggregation states its weighted denominator.

---

## HB-030 — Grading rules & tie-breaking

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:61-87,131-139,225-243; metrics/dbt.py:28-65
- **Note:** Missing/unfinished outputs, timeouts, length mismatch, and YAML errors have behavior, but the truncated scoring block omits remaining cases.

---

## HB-031 — Predictions->aggregate-score mapping

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** code/run_BERT.py:288-302
- **Note:** simple_accuracy is the mean of per-example equality; acc_and_f1 is the unweighted mean of accuracy and F1.

---

## HB-032 — Sample predictions / trajectories

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; benchmark/eval.py — no concrete prediction object
- **Note:** Question keys are listed but no model answer in the consumed JSON structure is supplied.

---

## HB-033 — Grading rules & tie-breaking

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** data_modeling/evaluation/*_eval.py — no explicit empty/malformed/tie handling
- **Note:** The scripts delegate invalid and degenerate cases to libraries without documenting their treatment.

---

## HB-034 — Grading rules & tie-breaking

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** README.md:53-76,193-200; eval_tablebench_script.py:224-270
- **Note:** Task metric selection and ±10% intent are stated, but normalization, exact tolerance boundary, ROUGE, parse failure, and chart tests are incomplete.

---

## HB-035 — Metric definition

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:7-12; eval/eval.py:30-110
- **Note:** The README names exact and subset dataframe matching and normalization is shown, but the actual match functions are absent.

---

## HB-036 — Input/expected-output schema

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:127-150; bixbench/graders.py:280-327
- **Note:** The README claims trajectory JSON uses a shared format, but that file schema is absent; only the in-memory grader arguments are shown.

---

## HB-037 — Input/expected-output schema

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** apicoder/CodeGenAPI/eval_baseline.py:117-140; eval_private.py:141-189
- **Note:** Generated JSONL records have task_id and completion, but evaluator result fields are not in the packet.

---

## HB-038 — Sample predictions / trajectories

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** Awesome-Self-Evolution-of-LLM/README.md; agent files — no consumed prediction example
- **Note:** No concrete evaluator-consumed output or trajectory is included.

---

## HB-039 — Metric definition

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:53-76; eval_tablebench_script.py:224-270; metrics/base_metric.py
- **Note:** Metric names and high-level tolerances are given, but QAMetric's EM/ROUGE implementation is absent.

---

## HB-040 — Evaluator implementation available

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** compute_scores.py:11-89; calculate_metrics.py:6-102; evaluation/harness/grading.py
- **Note:** Generic execution and aggregation are available, but per-task eval programs required for correctness are omitted.

---

## HB-041 — Predictions->aggregate-score mapping

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** bike-sharing-demand_eval.py:8-11,23-29; cat-in-the-dat-ii_eval.py:19-25
- **Note:** RMSLE explicitly averages over prediction rows; AUROC maps the complete target/score vectors to one result.

---

## HB-042 — Input/expected-output schema

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** bike-sharing-demand_eval.py:13-29; cat-in-the-dat-ii_eval.py:9-25
- **Note:** Both inputs are CSVs with a named target column and result.txt output, but row identity/order and allowed value types are unstated.

---

## HB-043 — Sample predictions / trajectories

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** documented-and-verifiable
- **Evidence pointer:** MLAgentBench/benchmarks/CLRS/env/evaluation_test.py:24-51
- **Note:** The test constructs concrete prediction and mask tensors and verifies the exact consumed/returned structure.

---

## HB-044 — Metric definition

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** not-documented
- **Evidence pointer:** Awesome-Self-Evolution-of-LLM/README.md; EPO/Alfshop/eval_agent/agents/base.py; fastchat_agent.py — no evaluation metric
- **Note:** The packet is a survey README plus model-serving agent code, not a scorer.

---

## HB-045 — Predictions->aggregate-score mapping

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:156-167
- **Note:** Majority-vote analysis and an evaluation CSV are claimed, but postprocessing and its denominator are not in the packet.

---

## HB-046 — Input/expected-output schema

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/base.py:22-32; fastchat_agent.py:40-99 — message/API schema only
- **Note:** These structures configure generation; no evaluator input and output schema is stated.

---

## HB-047 — Evaluator implementation available

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation.py:29-202; evaluation_test.py:1-55
- **Note:** The CLRS evaluator is present, identifiable, and accompanied by executable tests.

---

## HB-048 — Evaluator implementation available

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:37-44; execution.py:17-77
- **Note:** The packet includes a generic sandbox checker, but the stated test_ds1000 evaluator and per-problem tests are absent.

---

## HB-049 — Grading rules & tie-breaking

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** execution.py:45-77; README.md:72-73
- **Note:** Exceptions and timeouts fail and both tests must pass, but empty/malformed solution behavior inside the absent task harness is incomplete.

---

## HB-050 — Grading rules & tie-breaking

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** README.md; generation scripts — no scorer edge-case rules
- **Note:** No evidence states how empty code, exceptions, timeouts, or partial test passes are graded.

---

## HB-051 — Metric definition

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:34-49
- **Note:** Execution accuracy is named and pre/post reporting is described, but what constitutes correct execution is delegated to an absent external evaluator.

---

## HB-052 — Predictions->aggregate-score mapping

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** fix_embedding score.py:108-134; restricted_mlm score.py:52-72,88-125; triton_cumsum score.py:36-96
- **Note:** Batch means and final transformations are exact for three tasks, while the other task mappings are only summarized.

---

## HB-053 — Sample predictions / trajectories

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; eval/eval.py; gcs_eval.py; gcs_eval_checkpoints.py — no concrete generated SQL record
- **Note:** Commands and filenames are examples, not a model prediction in the evaluator's consumed format.

---

## HB-054 — Sample predictions / trajectories

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; calculate_metrics.py; compute_scores.py — no concrete predicted program or trajectory record
- **Note:** Example filenames do not constitute a model output in the consumed format.

---

## HB-055 — Input/expected-output schema

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** bigcodebench/evaluate.py:148-154,280-318; syncheck.py:24-45
- **Note:** JSONL keys task_id, _identifier, and solution/completion are visible, but the saved evaluation-result structure is truncated.

---

## HB-056 — Metric definition

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:59-73
- **Note:** Pass@1/10/100 and functional correctness are named, but their definitions are delegated to an absent HumanEval package.

---

## HB-057 — Grading rules & tie-breaking

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** eval.py:58-71,92-115; utils.py:84-99 — no malformed/empty policy
- **Note:** Nonmatching logs can yield missing chunks or division by zero, but no grading rule states how such cases count.

---

## HB-058 — Sample predictions / trajectories

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; evaluation suite files — no concrete results_metadata record
- **Note:** Gold SQL links and dataset references do not provide a model output in this packet.

---

## HB-059 — Grading rules & tie-breaking

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** 3SATTime/evaluate.py:20-29; blotto/evaluate.py:13-41
- **Note:** Shown tasks define early failure, allocation validation, and game ties, but remaining tasks and runtime/malformed cases are absent.

---

## HB-060 — Metric definition

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** code/run_BERT.py:288-302
- **Note:** Accuracy is exact label equality mean; F1 and the arithmetic acc/F1 mean are also defined.

---

## HB-061 — Grading rules & tie-breaking

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** README.md; getter files — no task grading or edge-case rules
- **Note:** The packet does not specify partial completion, malformed actions, timeouts, or evaluator ties.

---

## HB-062 — Metric definition

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:8-17,211-218
- **Note:** Official Test Suite Accuracy is named, but its scorer is only linked externally and packet code concerns an older baseline.

---

## HB-063 — Metric definition

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** data/3SATTime/evaluate.py:13-37; bertMNLI/evaluate.py:48-75; blotto/evaluate.py:13-79
- **Note:** Metrics are exact for three tasks, but the README describes a 13-task benchmark and the other task metrics are unavailable.

---

## HB-064 — Input/expected-output schema

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:35-47,128-163; calculate_metrics.py:76-102; compute_scores.py:66-85
- **Note:** Predicted Python programs and run/eval JSONL fields are largely clear, but protected task input/output schemas are not in the packet.

---

## HB-065 — Input/expected-output schema

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:220-230
- **Note:** Gold and prediction line formats and CLI arguments are explicit, but evaluator output fields are not.

---

## HB-066 — Grading rules & tie-breaking

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** eval/eval.py:177-235,247-318
- **Note:** Query timeout and exceptions are defined, but their conversion into grades and handling of empty/malformed predictions are absent.

---

## HB-067 — Metric definition

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:133-140; bigcodebench/evaluate.py:29-39,117-137
- **Note:** Pass@k is named and pass/fail execution is indicated, but the imported pass@k estimator and test checker are absent.

---

## HB-068 — Sample predictions / trajectories

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:184-191; evaluator.py — grammar but no concrete prediction values
- **Note:** The format is precise, but no actual model prediction instance is provided.

---

## HB-069 — Sample predictions / trajectories

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** partially-documented
- **Evidence pointer:** README.md:89-106
- **Note:** A concrete 'Final Answer: 1062' prediction and model_name are shown, but surrounding required record fields are elided.

---

## HB-070 — Metric definition

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** bixbench/graders.py:14-52,58-170,173-277
- **Note:** Binary exact/range/LLM grading is shown, but LLM grading prompts are imported and unavailable.

---

## HB-071 — Evaluator implementation available

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:8,211-218; baselines/nl2code/evaluation.py
- **Note:** Official evaluator code is external; the included baseline evaluator does not implement the declared official test-suite metric.

---

## HB-072 — Metric definition

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:16-29; discovery_eval.py:3,40-50
- **Note:** A faceted evaluation is asserted, but all scoring logic is in an omitted imported function.

---

## HB-073 — Grading rules & tie-breaking

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** discovery_eval.py:6-15,18-26,54-58
- **Note:** Empty required strings and output-write errors are handled, but correctness, ties, partial credit, and evaluation failures are not.

---

## HB-074 — Predictions->aggregate-score mapping

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:46-61
- **Note:** The output reports library counts/means and DS-1000 overall mean; the listed counts total the 1000-item denominator.

---

## HB-075 — Sample predictions / trajectories

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; evaluation.py; metrics/dbt.py — no concrete result.json or answer artifact
- **Note:** No model trajectory or prediction instance in the consumed format is shown.

---

## HB-076 — Grading rules & tie-breaking

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** README.md; copy_pre_perturbation_predictions.py; data_preprocess.py — no grading behavior
- **Note:** No packet evidence states treatment of invalid SQL, timeouts, empty lines, or partial matches.

---

## HB-077 — Sample predictions / trajectories

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; packet source files — no concrete predicted SQL line
- **Note:** Paths and file generation are shown without an actual model prediction.

---

## HB-078 — Predictions->aggregate-score mapping

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** Awesome-Self-Evolution-of-LLM/README.md; fastchat_agent.py — no score aggregation
- **Note:** No per-item results or reported benchmark score are defined.

---

## HB-079 — Metric definition

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** MetaGPT/examples/werewolf_game/evals/eval.py:73-115,135-167
- **Note:** Voting accuracy is correct non-werewolf votes divided by all non-werewolf voters and is rounded to two decimals.

---

## HB-080 — Sample predictions / trajectories

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; eval_closed_form.py — format regex but no concrete response object
- **Note:** The grammar alone is not a complete model-output example.

---

## HB-081 — Sample predictions / trajectories

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:68-84; execution.py — no concrete generated solution
- **Note:** The prompt instruction is illustrative, but no complete evaluator-consumed model output is supplied.

---

## HB-082 — Metric definition

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** data_modeling/evaluation/bike-sharing-demand_eval.py:7-11,23-29; cat-in-the-dat-ii_eval.py:19-25
- **Note:** RMSLE is fully defined and AUROC is invoked directly with true labels and prediction scores.

---

## HB-083 — Evaluator implementation available

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation/evaluation.py:1-239; open_spreadsheet.py; parity_test.py
- **Note:** An identifiable workbook evaluator and supporting recalculation/parity utilities are present.

---

## HB-084 — Input/expected-output schema

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:46-87,141-180,198-229
- **Note:** JSON/JSONL config and result.json fields are largely visible, but final evaluation-result fields are truncated.

---

## HB-085 — Input/expected-output schema

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:174-189; AI4Code/grade.py:38-65; alaska2-image-steganalysis/grade.py:102-130
- **Note:** The outer JSONL and several CSV column schemas are exact, while competition-specific formats for the remaining tasks are only referenced.

---

## HB-086 — Predictions->aggregate-score mapping

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** evaluation/evaluation.py:209-232
- **Note:** The evaluator writes per-instruction soft/hard values but never defines a single score across the 912 instructions.

---

## HB-087 — Predictions->aggregate-score mapping

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval_closed_form.py:64-131,155-166
- **Note:** Question, sub-question, proportional, and concept denominators are implemented exactly, including zero-denominator behavior.

---

## HB-088 — Sample predictions / trajectories

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:220-230 — line grammar only; no predicted SQL instance
- **Note:** No concrete model prediction is included.

---

## HB-089 — Input/expected-output schema

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval_closed_form.py:9-15,29-49,134-199
- **Note:** Responses are JSONL objects with id and response using @name[value], and the output JSON fields are explicit.

---

## HB-090 — Sample predictions / trajectories

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:123-125,191-196
- **Note:** Concrete example analysis files are linked by name but their contents are absent from the packet.

---

## HB-091 — Evaluator implementation available

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:31-38,59-65; eval_baseline.py; eval_private.py
- **Note:** Packet scripts generate samples; the HumanEval scorer implementing correctness is external and absent.

---

## HB-092 — Metric definition

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:18-25,127-156; blade_bench/eval/datamodel/run.py:28-103
- **Note:** Hit-rate fields and some formulas are present, but the imported matching metrics are absent.

---

## HB-093 — Sample predictions / trajectories

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:127-150,225-232
- **Note:** Trajectory/result data are described and downloadable, but no concrete consumed record is included in the packet.

---

## HB-094 — Predictions->aggregate-score mapping

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:133-140; bigcodebench/evaluate.py:214-223
- **Note:** The packet requests pass@k but omits the imported estimator and the code that saves its final values.

---

## HB-095 — Evaluator implementation available

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** discovery_eval.py:1-62
- **Note:** Only a CLI wrapper is present; the function that implements evaluation is imported from a missing module.

---

## HB-096 — Grading rules & tie-breaking

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** code/run_BERT.py:288-321 — no prediction decoding or invalid-output rules
- **Note:** The packet does not expose empty, malformed, timeout, or tie behavior for generated predictions.

---

## HB-097 — Metric definition

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:67-89,102-112; desktop_env/evaluators/getters/*.py
- **Note:** A per-task evaluation score is demonstrated, but task evaluator definitions/configurations are absent; getters alone do not define correctness.

---

## HB-098 — Metric definition

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:68-84; execution.py:17-77
- **Note:** Functional correctness and the requirement to pass execution and string tests are stated, but dataset code_context tests are not in the packet.

---

## HB-099 — Sample predictions / trajectories

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:67-89
- **Note:** The quick start supplies a concrete pyautogui action string passed directly to env.step before evaluation.

---

## HB-100 — Evaluator implementation available

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:7-12; eval/eval.py:1-326
- **Note:** Evaluation helpers are present, but the identifiable runner and dataframe comparison implementation are not in the packet.

---

## HB-101 — Predictions->aggregate-score mapping

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:70,241-250 — implementation truncates before score combination
- **Note:** The config defaults to 'avg', but the packet does not show how scores are actually combined; assuming a mean would be guessing.

---

## HB-102 — Grading rules & tie-breaking

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluator.py:17-45,57-82,131-182,185-316; README.md:184-191
- **Note:** Duplicates collapse to sets, sizes must match, invalid numbers/dates become strings, NaN/inf are rejected, and an empty prediction line is explicitly supported.

---

## HB-103 — Metric definition

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:35-47,182-199; compute_scores.py:11-63
- **Note:** Valid-program, task success, CodeBERTScore, and cost are identified, but task-specific eval programs are absent.

---

## HB-104 — Evaluator implementation available

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** eval_tablebench_script.py; metrics/base_metric.py:1-12
- **Note:** Evaluation orchestration is present, but the concrete QAMetric implementation imported by the script is not in the packet.

---

## HB-105 — Evaluator implementation available

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval.py:23-218; utils.py:15-134
- **Note:** The vote-log extraction, parsing, scoring, grouping, and CSV writer are identifiable.

---

## HB-106 — Sample predictions / trajectories

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; discovery_eval.py — no concrete predicted hypothesis/workflow
- **Note:** No consumed model output example appears in the packet.

---

## HB-107 — Input/expected-output schema

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:176-193; evaluator.py:319-369
- **Note:** Prediction lines are ex_id followed by tab-separated items, including the explicit no-prediction form; tagged targets and parsing are defined.

---

## HB-108 — Sample predictions / trajectories

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md; three evaluate.py files — no concrete submitted strategy/model output
- **Note:** No evaluator-consumed prediction example is shown.

---

## HB-109 — Evaluator implementation available

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** ai_rd_fix_embedding/assets/score.py; ai_rd_restricted_mlm/assets/score.py; ai_rd_triton_cumsum/assets/score.py
- **Note:** Three identifiable scorers are available for a larger task suite.

---

## HB-110 — Sample predictions / trajectories

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md dataset examples; code/run_BERT.py — no model prediction example
- **Note:** Dataset records are not sample model outputs.

---

## HB-111 — Input/expected-output schema

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** evaluate.py:22-40,48-57,75-107,129-137
- **Note:** Required result filenames and fields instance_id, answer_type, answer_or_path are visible, but no formal result example or output artifact schema is provided.

---

## HB-112 — Grading rules & tie-breaking

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluate.py:64-107; eval_utils.py:11-180,184-243
- **Note:** Alternative answers use max, excluded strings fail, numeric precision and table tolerances are exact, and file/DB errors generally score zero.

---

## HB-113 — Predictions->aggregate-score mapping

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** eval_tablebench_script.py:224-270
- **Note:** Per-type parse/ECR rates use explicit counts and QAMetric gets full vectors, but metric internals and a single overall benchmark number are absent.

---

## HB-114 — Input/expected-output schema

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:89-106,109-190; eval_tablebench_script.py
- **Note:** Prediction/model_name and downstream parsed fields are shown, but the example elides required dataset metadata and parser implementation is not in the packet.

---

## HB-115 — Predictions->aggregate-score mapping

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:53-77
- **Note:** Any Medal percentage and mean±SEM are requested, but medal thresholds and leaderboard aggregation code are not in the packet.

---

## HB-116 — Predictions->aggregate-score mapping

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** blade_bench/eval/datamodel/run.py:106-176,301-348
- **Note:** Several coverage and average outputs are exposed, but key imported metric definitions and the truncated tail leave the full mapping incomplete.

---

## HB-117 — Evaluator implementation available

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** spider2-dbt/evaluation_suite/evaluate.py; eval_utils.py
- **Note:** The evaluator dispatch and concrete match functions are present and identifiable.

---

## HB-118 — Evaluator implementation available

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:127-162; blade_bench/eval/convert.py; datamodel/run.py
- **Note:** Conversion/result models are present, while the runner and matching implementations that perform evaluation are missing.

---

## HB-119 — Sample predictions / trajectories

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:66-161; score.py files — scores but no submitted model/code example
- **Note:** Starting and official scalar scores are results, not concrete evaluator-consumed model outputs.

---

## HB-120 — Predictions->aggregate-score mapping

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** README.md:45-49
- **Note:** Macro averages over DB, NLQ, and SQL perturbation sets are claimed, but weighting and treatment of set sizes/failures are not stated.

---

## HB-121 — Metric definition

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** spider2-dbt/evaluation_suite/evaluate.py:48-123; eval_utils.py:11-180
- **Note:** Binary string, number, CSV/table, DuckDB, and multi-table matching are implemented.

---

## HB-122 — Sample predictions / trajectories

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval.py:46-57,73-90
- **Note:** The docstrings provide a concrete multi-player vote-log chunk in the exact regex-consumed format.

---

## HB-123 — Grading rules & tie-breaking

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:4-11,18-45
- **Note:** It uses the first number, handles percentages, catches nonnumeric outputs as incorrect, uses strict tolerance bounds, and defines MC prefix matching.

---

## HB-124 — Evaluator implementation available

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:1-50
- **Note:** The complete compact evaluator is present and directly executable.

---

## HB-125 — Predictions->aggregate-score mapping

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** README.md:176-193; evaluator.py:346-370
- **Note:** The batch evaluator loads all targets and predictions, but the frozen file ends before the final correct/total score and missing-ID denominator behavior.

---

## HB-126 — Predictions->aggregate-score mapping

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** README.md; desktop_env/evaluators — no mapping across 494 tasks
- **Note:** No denominator, weighting, or exclusion policy for a benchmark-wide number is stated.

---

## HB-127 — Evaluator implementation available

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:34-40; copy_pre_perturbation_predictions.py; data_preprocess.py
- **Note:** The actual test-suite evaluator is only linked externally; packet code merely prepares data/predictions.

---

## HB-128 — Input/expected-output schema

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:68-78; execution.py:17-18,73-77
- **Note:** The solution is a code string and the checker return dict is defined, but the answers JSONL record schema is not shown.

---

## HB-129 — Evaluator implementation available

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** da_agent/evaluators/evaluation.py:17-250; metrics/dbt.py:19-65
- **Note:** The task evaluator and an identifiable metric implementation are present, although the frozen file ends mid-function.

---

## HB-130 — Metric definition

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** examples/DA-Agent/eval_closed_form.py:18-49,110-131
- **Note:** Exact/numeric equality and all three accuracy variants are explicitly defined.

---

## HB-131 — Input/expected-output schema

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:124-140,295-305; gcs_eval.py:57-90
- **Note:** CLI inputs and CSV output paths are shown, but required prediction/result columns and evaluator return fields are not.

---

## HB-132 — Evaluator implementation available

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** mlebench/competitions/AI4Code/grade.py; aerial-cactus-identification/grade.py; alaska2-image-steganalysis/grade.py
- **Note:** Identifiable graders exist for three competitions, not the full 75-competition evaluation.

---

## HB-133 — Evaluator implementation available

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** desktop_env/evaluators/__init__.py; getters/dbt.py; getters/file.py
- **Note:** Only state getter utilities are present, not the task-specific evaluation functions invoked by env.evaluate().

---

## HB-134 — Evaluator implementation available

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/base.py:7-20; fastchat_agent.py:23-161
- **Note:** The packet contains agent inference code but no identifiable evaluation implementation.

---

## HB-135 — Sample predictions / trajectories

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** eval_baseline.py:142-170; eval_private.py:188-218
- **Note:** Example prompts are present, but there is no concrete generated completion record.

---

## HB-136 — Input/expected-output schema

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:87-95,123-125,191-196
- **Note:** The README points to example JSON schemas, but those example files and their field definitions are not in the packet.

---

## HB-137 — Input/expected-output schema

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:47-56,127-129; evaluation.py:204-232
- **Note:** Input/output workbook locations and dataset fields are described, but README and code disagree on processed path and no complete workbook output example is present.

---

## HB-138 — Grading rules & tie-breaking

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval_closed_form.py:18-49,98-131
- **Note:** Numeric tolerance, missing response exclusion, missing named answers, partial sub-answer credit, and empty denominators are encoded.

---

## HB-139 — Sample predictions / trajectories

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:82-83,187-190
- **Note:** Pre-generated samples are asserted and linked as a release attachment, but no sample record is in the packet.

---

## HB-140 — Metric definition

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation/evaluation.py:18-47,123-188,204-229
- **Note:** Cell equality, per-case booleans, soft fraction over three cases, and hard all-three success are exact.

---

## HB-141 — Input/expected-output schema

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** 3SATTime/evaluate.py:13-20; bertMNLI/evaluate.py:42-46,48-75; blotto/evaluate.py:29-50,76-79
- **Note:** Imported function/model interfaces and printed JSON fields are visible for three tasks, not a complete submission schema for all tasks.

---

## HB-142 — Metric definition

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:4-47
- **Note:** Accuracy is exactly defined for numerical answers within a strict 3% interval and MC answers by case-folded prefix.

---

## HB-143 — Metric definition

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:46-139; metrics/dbt.py:19-65
- **Note:** The configurable metric interface and one exact YAML metric are shown, but the packet omits most metric functions.

---

## HB-144 — Input/expected-output schema

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** not-documented
- **Evidence pointer:** README.md; code/run_BERT.py — model/dataset pipeline but no accepted prediction file and returned artifact schema
- **Note:** The packet does not state how to supply standalone model predictions to the evaluator.

---

## HB-145 — Input/expected-output schema

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:31-40; copy_pre_perturbation_predictions.py:19-33
- **Note:** Predictions are one SQL query per line at exact paths, but evaluator outputs and database association format are absent.

---

## HB-146 — Sample predictions / trajectories

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:19-25,47-56
- **Note:** The release claims a 200-item sample archive, but no concrete generated workbook/output is included in the evidence packet.

---

## HB-147 — Evaluator implementation available

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** code/run_BERT.py:288-321; README.md:67-98
- **Note:** Metric functions and CLI claims are present, but the frozen evaluator file ends at main before inference/evaluation orchestration.

---

## HB-148 — Metric definition

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:66-161; three assets/score.py files
- **Note:** The README names scores for all tasks and three scorers fully define log-loss/runtime metrics, but other task implementations are absent.

---

## HB-149 — Grading rules & tie-breaking

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** AI4Code/grade.py:38-70; alaska2-image-steganalysis/grade.py:102-136
- **Note:** Length, columns, IDs, numeric values, and NaNs are handled for shown tasks, but rules for the other competitions are absent.

---

## HB-150 — Grading rules & tie-breaking

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** fastchat_agent.py:75-99,137-161 — generation retries only; no grading rules
- **Note:** Timeout handling is for model serving and does not specify evaluation grading.

---

## HB-151 — Grading rules & tie-breaking

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** blade_bench/eval/convert.py:17-22,221-301; datamodel/run.py:301-312
- **Note:** Failure modes and empty failed runs are represented, but the core match decisions and all malformed cases are not available.

---

## HB-152 — Predictions->aggregate-score mapping

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** calculate_metrics.py:6-73
- **Note:** Best runs are selected lexicographically by success, validity, CodeBERTScore, then cost, and selected task values are averaged over all tasks.

---

## HB-153 — Grading rules & tie-breaking

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** README.md:211-230; included baseline files — no official test-suite edge rules
- **Note:** Invalid SQL, execution errors, empty predictions, timeouts, and partial suite passes are not specified for the official metric.

---

## HB-154 — Evaluator implementation available

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** data/3SATTime/evaluate.py; data/bertMNLI/evaluate.py; data/blotto/evaluate.py
- **Note:** Three identifiable evaluators are present for a 13-task release.

---

## HB-155 — Evaluator implementation available

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** data_modeling/evaluation/*_eval.py
- **Note:** Three small, identifiable evaluation scripts directly load predictions and write their scores.

---

## HB-156 — Input/expected-output schema

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:67-89,102-112; getters/dbt.py; getters/file.py
- **Note:** The environment accepts action strings and returns a scalar score, but the linked task-config format and evaluator output schema are missing.

---
