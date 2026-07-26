# R2 Human Coding Form — Rater A

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

## HA-001 — Evaluator implementation available

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval/eval.py:30-110
- **Note:** eval/eval.py contains identifiable SQL-evaluation helpers (normalize_table, query execution with timeout) used to score generated queries.

---

## HA-002 — Predictions->aggregate-score mapping

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** data_modeling/evaluation/bike-sharing-demand_eval.py:23-29
- **Note:** Each per-competition script writes one metric to result.txt; packet has no code for benchmark-wide aggregation across tasks.

---

## HA-003 — Metric definition

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** bixbench/graders.py:14-22
- **Note:** Binary 0/1 grading is explicit via GradeType.CORRECT/INCORRECT and numeric_grade mapping.

---

## HA-004 — Evaluator implementation available

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** bixbench/graders.py:55-108
- **Note:** GradingFunction and MCQ/OpenEnded grader classes implement the benchmark scoring logic.

---

## HA-005 — Evaluator implementation available

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:14-47
- **Note:** benchmark/eval.py defines calc_acc with identifiable per-item scoring for numerical and multiple-choice items.

---

## HA-006 — Predictions->aggregate-score mapping

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** MetaGPT/examples/werewolf_game/evals/eval.py:169-190
- **Note:** calc_avg_rate groups per-vote good_vote_rate by file and maps to avg_rate/vote1_rate columns in output CSV.

---

## HA-007 — Metric definition

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** MetaGPT/examples/werewolf_game/evals/eval.py:106-115
- **Note:** good_vote_rate metric is defined as correct_votes divided by num_non_werewolves with inline worked example.

---

## HA-008 — Metric definition

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluator.py:1-46
- **Note:** Official evaluator docstring precisely defines denotation matching rules for strings, numbers, and dates.

---

## HA-009 — Grading rules & tie-breaking

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** execution.py:17-77
- **Note:** Timeout and exec-failure paths return passed/result strings, but packet lacks rules for ties, empty outputs, or partial credit.

---

## HA-010 — Metric definition

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** ai_rd_fix_embedding/assets/score.py:122-129
- **Note:** Task score is log(validation_loss - 1.5) from estimate_loss over fixed train/val batches.

---

## HA-011 — Input/expected-output schema

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** data/bertMNLI/evaluate.py:48-75
- **Note:** Per-task evaluate scripts show some input sources (HF dataset, pickle) but no unified submission IO schema across MLGym tasks.

---

## HA-012 — Sample predictions / trajectories

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** partially-documented
- **Evidence pointer:** mlebench/competitions/AI4Code/grade.py:38-45
- **Note:** prepare_for_metric documents required submission columns and a comment cell_order example, but no full sample prediction file/trajectory.

---

## HA-013 — Predictions->aggregate-score mapping

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:47-47
- **Note:** Aggregate accuracy is correct_num divided by len(pred) over all items.

---

## HA-014 — Evaluator implementation available

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation/harness/grading.py:168-206
- **Note:** grading.py plus compute_scores.py provide identifiable evaluation harness and per-instance scoring code.

---

## HA-015 — Grading rules & tie-breaking

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** data/blotto/evaluate.py:22-27
- **Note:** Some edge cases covered (ties return 0/0, invalid strategies raise), but no unified timeout/malformed-output policy across tasks.

---

## HA-016 — Evaluator implementation available

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** da_agent/evaluators/evaluation.py:17-139
- **Note:** Evaluator class loads per-task outputs/gold and dispatches metric functions; identifiable despite truncated tail.

---

## HA-017 — Predictions->aggregate-score mapping

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** data/bertMNLI/evaluate.py:74-75
- **Note:** Per-task metrics are printed (e.g., validation_accuracy), but packet lacks one documented benchmark-level aggregate across all MLGym tasks.

---

## HA-018 — Input/expected-output schema

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** compute_scores.py:73-79
- **Note:** compute_scores reads input/input.json fields (gold_program_name, eval_script_name, output_fname) but full accepted submission schema is incomplete in packet.

---

## HA-019 — Sample predictions / trajectories

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** partially-documented
- **Evidence pointer:** MLAgentBench/benchmarks/CLRS/env/evaluation_test.py:33-45
- **Note:** Unit-test fixture shows concrete prediction DataPoint tensors, not an end-to-end model trajectory/sample submission.

---

## HA-020 — Predictions->aggregate-score mapping

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** calculate_metrics.py:6-73
- **Note:** evaluate_best_run selects best run per task then averages success_rate, codebert_score, valid_program_rate, and cost.

---

## HA-021 — Input/expected-output schema

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:35-38
- **Note:** README states submission format {test_id: label}, but packet lacks a complete evaluator input/output schema for the grading path.

---

## HA-022 — Grading rules & tie-breaking

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** eval/eval.py:177-190
- **Note:** Query timeout (func_timeout) and empty-query skipping are shown; exact/subset match scoring code is not present in packet.

---

## HA-023 — Grading rules & tie-breaking

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** spider2-dbt/evaluation_suite/evaluate.py:64-72
- **Note:** Per-item exceptions can pdb-break or set score=0 and multi-criteria answers use max(temp_scores); no full tie/timeout policy.

---

## HA-024 — Metric definition

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** examples/DA-Agent/eval_closed_form.py:18-25
- **Note:** Closed-form accuracy is defined via @name[value] parsing and exact or float-tolerance (1e-6) equality checks.

---

## HA-025 — Input/expected-output schema

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** data_modeling/evaluation/cat-in-the-dat_eval.py:9-25
- **Note:** Evaluator CLI requires answer_file and predict_file CSVs with configurable value column and writes scalar metric output.

---

## HA-026 — Predictions->aggregate-score mapping

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** bigcodebench/evaluate.py:214-223
- **Note:** Packet references estimate_pass_at_k and remote Gradio/E2B paths; local pass@k aggregation implementation is truncated/missing.

---

## HA-027 — Sample predictions / trajectories

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** bigcodebench/syncheck.py:27-28
- **Note:** Only documents solution dict keys (task_id, solution/completion); no concrete sample prediction content appears in packet.

---

## HA-028 — Predictions->aggregate-score mapping

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** README.md:7-12
- **Note:** README says results are aggregated for reporting but provides no code defining per-item-to-aggregate-score mapping.

---

## HA-029 — Predictions->aggregate-score mapping

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/fastchat_agent.py:23-39
- **Note:** Packet contains agent inference code only; no SQL-evaluation or score-aggregation logic for BIRD.

---

## HA-030 — Grading rules & tie-breaking

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** bixbench/graders.py:76-101
- **Note:** Covers exact/partial/LLM/range/refusal grading paths, but silent on timeouts and malformed-output handling.

---

## HA-031 — Input/expected-output schema

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** spider2-dbt/evaluation_suite/evaluate.py:22-40
- **Note:** Evaluation expects gold spider2_eval.jsonl and results_metadata.jsonl merged on instance_id with answer_type and answer_or_path fields.

---

## HA-032 — Input/expected-output schema

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** desktop_env/evaluators/getters/file.py:12-28
- **Note:** Getter configs document some input fields (path, file_type, file_content), but full evaluator IO contract is incomplete without metric functions.

---

## HA-033 — Grading rules & tie-breaking

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** compute_scores.py:37-46
- **Note:** Defines 900s timeout, missing-output failure, and invalid-exec handling; tie-breaking across metrics only partly specified.

---

## HA-034 — Predictions->aggregate-score mapping

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** desktop_env/evaluators/getters/file.py:1-28
- **Note:** Packet has data getter utilities only; no code maps per-task evaluator outputs to a benchmark aggregate score.

---

## HA-035 — Metric definition

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** da_agent/evaluators/metrics/dbt.py:19-62
- **Note:** One metric (check_yaml_file returns 1/0) is defined; broader benchmark metric set referenced via metrics module is not in packet.

---

## HA-036 — Input/expected-output schema

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** MetaGPT/examples/werewolf_game/evals/eval.py:46-57
- **Note:** Vote-log parser documents required moderator/vote line format with a concrete multi-player example block.

---

## HA-037 — Grading rules & tie-breaking

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation/evaluation.py:33-47
- **Note:** Cell comparison rules cover empty/None equivalence, type mismatch failure, and numeric rounding via transform_value.

---

## HA-038 — Evaluator implementation available

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** blade_bench/eval/convert.py:50-116
- **Note:** Convert class and EvalRunResults handling provide identifiable automatic evaluation pipeline code for submissions.

---

## HA-039 — Grading rules & tie-breaking

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:233-242
- **Note:** Shows unfinished tasks score 0.0 and metric evaluation timeout wrapper, but packet truncates before full scoring/tie-break logic.

---

## HA-040 — Input/expected-output schema

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:41-47
- **Note:** README documents train/dev JSON fields (question, query, sql, db_id) and pred file as one SQL per line with etype flags.

---

## HA-041 — Grading rules & tie-breaking

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** examples/DA-Agent/eval_closed_form.py:18-25
- **Note:** Numeric answers use 1e-6 tolerance via is_equal; missing/empty responses are skipped when matching labels, with no documented tie/timeout/malformed-output rules.

---

## HA-042 — Metric definition

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** bigcodebench/evaluate.py:87-114
- **Note:** Correctness is test-suite execution via untrusted_check; README names pass@k outputs but estimate_pass_at_k formula is not in the packet.

---

## HA-043 — Sample predictions / trajectories

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/fastchat_agent.py:1-33
- **Note:** Packet contains Alfshop LLM agent code only; no BIRD SQL prediction or trajectory example.

---

## HA-044 — Predictions->aggregate-score mapping

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** README.md:45-46
- **Note:** README reports macro averages over DB/NLQ/SQL perturbation sets but does not define per-set aggregation code in the packet.

---

## HA-045 — Sample predictions / trajectories

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** ai_rd_fix_embedding/assets/score.py:16-17
- **Note:** Scorer loads a model checkpoint path; no concrete example of model output the evaluator consumes.

---

## HA-046 — Metric definition

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:213-216
- **Note:** README names Test Suite Accuracy, component/exact/exec matching at clause level; full metric code is external to the packet.

---

## HA-047 — Input/expected-output schema

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** copy_pre_perturbation_predictions.py:19-32
- **Note:** Predictions are one SQL string per line in pred.sql under predictions/; evaluation itself defers to external test-suite-sql-eval.

---

## HA-048 — Evaluator implementation available

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** not-documented
- **Evidence pointer:** README.md:34-37
- **Note:** Packet has only preprocessing/copy scripts; README points to external test-suite evaluation with no evaluator implementation here.

---

## HA-049 — Sample predictions / trajectories

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:35-38
- **Note:** README states submission format {test_id: label} but provides no concrete model-output example in the packet.

---

## HA-050 — Sample predictions / trajectories

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** evaluator.py:351-353
- **Note:** Prediction file format is described (ex_id tab items) but no filled example line appears in the packet.

---

## HA-051 — Grading rules & tie-breaking

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/base.py:7-33
- **Note:** No BIRD grading rules, tie-breaking, or SQL evaluation logic in the packet artifacts.

---

## HA-052 — Predictions->aggregate-score mapping

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** README.md:55-69
- **Note:** README describes aggregate_grading_reports.py and any_medal_percentage mean±SEM; aggregation script is not included in the packet.

---

## HA-053 — Metric definition

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:14-47
- **Note:** Accuracy uses 3% relative band for numerical answers and prefix match for multiple-choice items.

---

## HA-054 — Input/expected-output schema

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** mlebench/competitions/AI4Code/grade.py:41-47
- **Note:** Grade functions document per-competition DataFrame columns (e.g. id, cell_order) but no unified MLE-bench submission schema is defined.

---

## HA-055 — Evaluator implementation available

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** execution.py:17-77
- **Note:** check_correctness executes submitted code with timeout and returns passed/result flags; README ties this to DS-1000 test_execution.

---

## HA-056 — Evaluator implementation available

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** code/run_BERT.py:288-317
- **Note:** README directs Table-BERT evaluation via run_BERT.py; script computes acc/f1 via compute_metrics on dev predictions.

---

## HA-057 — Predictions->aggregate-score mapping

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** evaluator.py:300-316
- **Note:** Per-example correctness via check_denotation is fully specified; packet truncates before aggregate accuracy computation.

---

## HA-058 — Sample predictions / trajectories

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:87-94
- **Note:** README names multirun_analyses.json output but packet contains no concrete LM analysis submission example.

---

## HA-059 — Grading rules & tie-breaking

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** ai_rd_fix_embedding/assets/score.py:150-162
- **Note:** Score path returns NaN on 300s timeout or exceptions; no rules for ties, empty outputs, or malformed predictions.

---

## HA-060 — Sample predictions / trajectories

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** eval_tablebench_script.py:144-148
- **Note:** Script reads parsed_prediction fields from results but includes no concrete prediction/trajectory example.

---

## HA-061 — Input/expected-output schema

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:46-54
- **Note:** Eval config comments list func/conj/result/options fields and result.json trajectory path; full eval JSON schema files are not in packet.

---

## HA-062 — Metric definition

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** data/bertMNLI/evaluate.py:74-75
- **Note:** Included task scripts define metrics (e.g. validation_accuracy, Monte-Carlo Score) but no single benchmark-wide metric is specified.

---

## HA-063 — Evaluator implementation available

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/fastchat_agent.py:23-38
- **Note:** Packet lacks any identifiable BIRD SQL evaluator implementation.

---

## HA-064 — Input/expected-output schema

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** blade_bench/eval/convert.py:50-68
- **Note:** Convert class references EntireAnalysis types and dataset CSV paths; full submission JSON schema is not fully specified in packet.

---

## HA-065 — Input/expected-output schema

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** discovery_eval.py:18-25
- **Note:** CLI documents required inputs (gold_hypo, pred_hypo, metadata_path, metadata_type, query) and eval_output_path output.

---

## HA-066 — Predictions->aggregate-score mapping

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** README.md:35-38
- **Note:** README gives CodaLab label submission format only; no per-item-to-aggregate-score mapping code in packet.

---

## HA-067 — Evaluator implementation available

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** data/3SATTime/evaluate.py:13-37
- **Note:** Per-task evaluate.py scripts are identifiable but packet shows no unified MLGym evaluator or overall aggregation.

---

## HA-068 — Predictions->aggregate-score mapping

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** examples/DA-Agent/eval_closed_form.py:111-131
- **Note:** Three aggregate accuracies are explicitly defined: by-question, by-sub-question, and proportional by-sub-question.

---

## HA-069 — Metric definition

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:2-3
- **Note:** Task is entailment vs refutation classification; run_BERT.py shows acc/f1 computation but full TabFact metric spec is incomplete in packet.

---

## HA-070 — Sample predictions / trajectories

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** copy_pre_perturbation_predictions.py:19-23
- **Note:** Script reads pred.sql lines but packet contains no concrete SQL prediction example text.

---

## HA-071 — Predictions->aggregate-score mapping

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:233-247
- **Note:** Unfinished tasks score 0.0; packet truncates mid-score loop so total_score aggregation is not reconstructable.

---

## HA-072 — Evaluator implementation available

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** examples/DA-Agent/eval_closed_form.py:29-49
- **Note:** eval_closed_form.py is an identifiable closed-form evaluator matching responses to labels and computing correctness.

---

## HA-073 — Grading rules & tie-breaking

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** eval_tablebench_script.py:6-29
- **Note:** Module docstring maps task subtypes to EM, EM_with_error_10, ROUGE-L, Pass@1; edge cases for ties/timeouts/malformed outputs are not specified.

---

## HA-074 — Metric definition

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** mlebench/competitions/AI4Code/grade.py:9-35
- **Note:** Sample grade.py files implement competition-specific metrics (e.g. Kendall tau, ROC-AUC) but MLE-bench has no single metric definition in packet.

---

## HA-075 — Metric definition

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** not-documented
- **Evidence pointer:** README.md:63-70
- **Note:** README documents HumanEval Pass@k only; no PandasEval/NumpyEval CERT metric definition appears in the packet.

---

## HA-076 — Sample predictions / trajectories

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** evaluation/evaluation.py:204-218
- **Note:** Evaluator compares spreadsheet workbooks; no sample model output file or trajectory is included.

---

## HA-077 — Sample predictions / trajectories

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** spider2-dbt/evaluation_suite/evaluate.py:27-29
- **Note:** Code expects results_metadata.jsonl but packet provides no concrete example submission line.

---

## HA-078 — Grading rules & tie-breaking

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** bigcodebench/evaluate.py:296-298
- **Note:** Evaluator skips unknown task_ids and uses min_time_limit/gt_time_limit; timeout/malformed handling in untrusted_check is outside the packet.

---

## HA-079 — Evaluator implementation available

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval_tablebench_script.py:125-142
- **Note:** eval_tablebench_script.py computes per-task metrics (Pass@1, ECR@1) from parsed predictions.

---

## HA-080 — Sample predictions / trajectories

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** baselines/nl2code/evaluation.py, README.md
- **Note:** Evaluator writes decode outputs to files but packet contains no concrete model-output example.

---

## HA-081 — Input/expected-output schema

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:91-104
- **Note:** README shows JSON fields model_name and prediction but omits full per-record schema.

---

## HA-082 — Sample predictions / trajectories

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** apicoder/CodeGenAPI/eval_baseline.py, apicoder/CodeGenAPI/eval_private.py
- **Note:** Code generates and saves samples.jsonl but packet has no concrete completion example.

---

## HA-083 — Input/expected-output schema

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:68-73
- **Note:** README documents prompt and code_context test functions but not full submission file format.

---

## HA-084 — Input/expected-output schema

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:7-12
- **Note:** README describes SQL-eval procedure and CSV question/output paths without full column schema.

---

## HA-085 — Grading rules & tie-breaking

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** README.md, copy_pre_perturbation_predictions.py, data_preprocess.py
- **Note:** Packet has preprocessing scripts only; no tie/empty/malformed/timeout grading rules.

---

## HA-086 — Grading rules & tie-breaking

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** mlebench/competitions/AI4Code/grade.py:39-59
- **Note:** grade.py raises InvalidSubmissionError on length/column/id mismatches; other edge cases silent.

---

## HA-087 — Predictions->aggregate-score mapping

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** README.md:70-73, apicoder/CodeGenAPI/eval_baseline.py
- **Note:** README reports Pass@k results table but packet has no pass@k aggregation code.

---

## HA-088 — Metric definition

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:7-11
- **Note:** README names exact and subset dataframe match metrics without full reimplementation detail in packet.

---

## HA-089 — Predictions->aggregate-score mapping

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** blade_bench/eval/datamodel/run.py, blade_bench/eval/convert.py
- **Note:** Packet has coverage averages but no per-item-to-reported-score aggregation mapping.

---

## HA-090 — Sample predictions / trajectories

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md, execution.py
- **Note:** execution.py grades completions but packet contains no example model output.

---

## HA-091 — Evaluator implementation available

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** ai_rd_fix_embedding/assets/score.py:37-38
- **Note:** Identifiable evaluate_model scoring function in score.py.

---

## HA-092 — Sample predictions / trajectories

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** partially-documented
- **Evidence pointer:** README.md:193-194
- **Note:** README describes JSONL run_logs and eval_logs format without inline trajectory example.

---

## HA-093 — Grading rules & tie-breaking

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** documented-and-verifiable
- **Evidence pointer:** benchmark/eval.py:18-47
- **Note:** calc_acc applies 3% numerical tolerance and try/except skip on unparseable predictions.

---

## HA-094 — Input/expected-output schema

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** examples/DA-Agent/eval_closed_form.py:56-60
- **Note:** eval_closed_form.py reads JSONL with id and concepts; default question/label/response paths documented.

---

## HA-095 — Grading rules & tie-breaking

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** evaluator.py:176-184
- **Note:** evaluator.py has except handlers for parse failures; ties/empty/timeout not addressed.

---

## HA-096 — Sample predictions / trajectories

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md, data_modeling/evaluation/bike-sharing-demand_eval.py
- **Note:** Evaluation scripts present but packet has no concrete prediction example.

---

## HA-097 — Evaluator implementation available

**Packet:** `PKT-14` · commit `507f92e1138b`
**Packet contains:** `README.md`, `mlebench/competitions/AI4Code/grade.py`, `mlebench/competitions/aerial-cactus-identification/grade.py`, `mlebench/competitions/alaska2-image-steganalysis/grade.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** mlebench/competitions/AI4Code/grade.py:68-70
- **Note:** Identifiable grade() function scoring submissions via kendall_tau.

---

## HA-098 — Input/expected-output schema

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** bigcodebench/evaluate.py:297-303
- **Note:** evaluate.py expects jsonl samples with task_id and completion; full schema not fully spelled out.

---

## HA-099 — Grading rules & tie-breaking

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** discovery_eval.py:7-14
- **Note:** discovery_eval.py rejects empty query and option values; other edge cases not covered.

---

## HA-100 — Sample predictions / trajectories

**Packet:** `PKT-15` · commit `9d40c1b50352`
**Packet contains:** `README.md`, `data/3SATTime/evaluate.py`, `data/bertMNLI/evaluate.py`, `data/blotto/evaluate.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:176-182
- **Note:** README gives trajectory_dir CLI example but no concrete trajectory content in packet.

---

## HA-101 — Evaluator implementation available

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** desktop_env/evaluators/getters/file.py:12-34
- **Note:** Getter helpers extract evaluation inputs; __init__.py scorer stubs are commented out.

---

## HA-102 — Sample predictions / trajectories

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md, discovery_eval.py
- **Note:** discovery_eval.py accepts CLI hypothesis/workflow strings but no example output in packet.

---

## HA-103 — Sample predictions / trajectories

**Packet:** `PKT-12` · commit `3d6c4a70198e`
**Packet contains:** `README.md`, `examples/DA-Agent/eval_closed_form.py`, `pipeline/activities/eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md, examples/DA-Agent/eval_closed_form.py
- **Note:** README describes demo commands; no concrete model output or trajectory example in packet.

---

## HA-104 — Evaluator implementation available

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** spider2-dbt/evaluation_suite/eval_utils.py:11-17
- **Note:** Identifiable string_match evaluation helper in eval_utils.py.

---

## HA-105 — Evaluator implementation available

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** baselines/nl2code/evaluation.py:62-88
- **Note:** evaluate_decode_results implements BLEU and exact-match scoring over decode_results.

---

## HA-106 — Evaluator implementation available

**Packet:** `PKT-04` · commit `09dd993f46c3`
**Packet contains:** `README.md`, `bigcodebench/evaluate.py`, `bigcodebench/syncheck.py`, `decontamination/n_gram_check.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** bigcodebench/evaluate.py
- **Note:** bigcodebench/evaluate.py is the identifiable evaluation module for code samples.

---

## HA-107 — Predictions->aggregate-score mapping

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** bixbench/graders.py
- **Note:** graders.py grades individual items but packet has no aggregate-score computation.

---

## HA-108 — Sample predictions / trajectories

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:170-172
- **Note:** README lists trajectory config parameters; no concrete trajectory example in packet.

---

## HA-109 — Grading rules & tie-breaking

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** MetaGPT/examples/werewolf_game/evals/eval.py, MetaGPT/README.md
- **Note:** Werewolf vote evaluator present but no tie/empty/malformed/timeout grading rules documented.

---

## HA-110 — Sample predictions / trajectories

**Packet:** `PKT-06` · commit `b211daf51fdc`
**Packet contains:** `README.md`, `da_agent/evaluators/evaluation.py`, `da_agent/evaluators/metrics/dbt.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** da_agent/evaluators/evaluation.py:141-156
- **Note:** evaluation.py parses trajectory JSON fields but packet has no inline example trajectory.

---

## HA-111 — Predictions->aggregate-score mapping

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** spider2-dbt/evaluation_suite/evaluate.py:120-126
- **Note:** Final score computed as count of score==1 divided by len(output_list).

---

## HA-112 — Sample predictions / trajectories

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:158-161, bixbench/graders.py
- **Note:** README describes loading trajectory CSV externally; no concrete trajectory example in packet.

---

## HA-113 — Metric definition

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** not-documented
- **Evidence pointer:** discovery_eval.py
- **Note:** discovery_eval.py imports run_eval_gold_vs_gen_NL_hypo_workflow; no metric name or definition in packet.

---

## HA-114 — Predictions->aggregate-score mapping

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** eval_tablebench_script.py:135-142
- **Note:** Pass@1 aggregated as pass_1s.count(True)/total with percentage rounding.

---

## HA-115 — Evaluator implementation available

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** MetaGPT/examples/werewolf_game/evals/eval.py:23-26
- **Note:** Vote evaluation class with identifiable scoring methods in eval.py.

---

## HA-116 — Metric definition

**Packet:** `PKT-11` · commit `c64694a4a278`
**Packet contains:** `README.md`, `copy_pre_perturbation_predictions.py`, `data_preprocess.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:45-46
- **Note:** README names EX (execution) accuracy and points to external test-suite evaluation for definition.

---

## HA-117 — Predictions->aggregate-score mapping

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** MLAgentBench/benchmarks/CLRS/env/evaluation.py:137-141
- **Note:** Overall score is mean of per-output eval scores: sum(values)/len(evals).

---

## HA-118 — Metric definition

**Packet:** `PKT-19` · commit `72220ee8d20a`
**Packet contains:** `README.md`, `calculate_metrics.py`, `compute_scores.py`, `evaluation/harness/grading.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** compute_scores.py:28-63
- **Note:** Per-instance success_rate, valid_program, and codebert_score are computed in code, but task-level success criteria depend on external per-task eval scripts not included in the packet.

---

## HA-119 — Evaluator implementation available

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** discovery_eval.py:3-3
- **Note:** CLI wrapper imports eval.new_eval, but that evaluation module is not present in the packet to confirm the evaluator implementation.

---

## HA-120 — Predictions->aggregate-score mapping

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation/evaluation.py:221-228
- **Note:** Per-task soft accuracy is passed test cases over 3; hard accuracy is 1 only if all three pass.

---

## HA-121 — Metric definition

**Packet:** `PKT-25` · commit `6c61a2034040`
**Packet contains:** `README.md`, `eval_tablebench_script.py`, `metrics/base_metric.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:52-77
- **Note:** README names and defines task-type metrics: EM, EM_with_error_10, ROUGE-L, and Pass@1.

---

## HA-122 — Metric definition

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:70-73
- **Note:** README states pass/fail via test_execution and test_string, but per-problem test logic lives in dataset code_context files not included.

---

## HA-123 — Input/expected-output schema

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** not-documented
- **Evidence pointer:** README.md:88-95
- **Note:** Packet lacks MLAgentBench evaluator input/output schema; only unrelated CLRS env files and a requirements checker are included.

---

## HA-124 — Input/expected-output schema

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/fastchat_agent.py:1-161
- **Note:** Packet contains Alfshop agent client code only; no BIRD submission format or evaluator I/O schema is documented.

---

## HA-125 — Metric definition

**Packet:** `PKT-21` · commit `01a4c67c1e3f`
**Packet contains:** `README.md`, `spider2-dbt/evaluation_suite/eval_utils.py`, `spider2-dbt/evaluation_suite/evaluate.py`, `spider2-dbt/evaluation_suite/evaluate_beta.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** spider2-dbt/evaluation_suite/evaluate.py:57-123
- **Note:** Each instance is scored 0/1 via string_match, number_match, table_match, or duckdb_match; aggregate is correct count divided by total.

---

## HA-126 — Input/expected-output schema

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:47-55
- **Note:** README documents JSONL fields id, instruction, spreadsheet_path, instruction_type, and answer_position for each task.

---

## HA-127 — Grading rules & tie-breaking

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** data_modeling/evaluation/bike-sharing-demand_eval.py:7-29
- **Note:** Only RMSLE computation is shown; packet is silent on ties, empty predictions, malformed outputs, and timeouts.

---

## HA-128 — Evaluator implementation available

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** claimed-but-not-verifiable
- **Evidence pointer:** README.md:90-93
- **Note:** README references python -m MLAgentBench.eval, but that evaluator module is not included in the packet.

---

## HA-129 — Input/expected-output schema

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** README.md:7-12
- **Note:** Benchmark JSON keys are listed, but eval.py expects a tmp.json with pred fields without a complete documented submission schema.

---

## HA-130 — Input/expected-output schema

**Packet:** `PKT-05` · commit `49311180bdac`
**Packet contains:** `README.md`, `bixbench/graders.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** bixbench/graders.py:289-327
- **Note:** Grader API takes target/predicted/question strings, but trajectory or prediction file format is not specified in the packet.

---

## HA-131 — Metric definition

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** blade_bench/eval/datamodel/run.py:82-103
- **Note:** Hit-rate metrics are defined on matched model/spec fields, but full metric computation imports AllMetrics code absent from packet.

---

## HA-132 — Input/expected-output schema

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:184-188
- **Note:** Official prediction format is ex_id followed by tab-separated answer items; empty prediction is just ex_id.

---

## HA-133 — Input/expected-output schema

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** ai_rd_fix_embedding/assets/score.py:126-133
- **Note:** Score function returns {score, message}, but unified agent submission file schema across RE-Bench tasks is not fully specified.

---

## HA-134 — Predictions->aggregate-score mapping

**Packet:** `PKT-10` · commit `c31fcf011e07`
**Packet contains:** `README.md`, `discovery_eval.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** not-documented
- **Evidence pointer:** discovery_eval.py:40-52
- **Note:** Script prints eval_result from missing eval.new_eval; no per-item-to-aggregate mapping code is in the packet.

---

## HA-135 — Evaluator implementation available

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation/evaluation.py:155-232
- **Note:** compare_workbooks and evaluation() provide an identifiable spreadsheet comparison evaluator in the packet.

---

## HA-136 — Evaluator implementation available

**Packet:** `PKT-26` · commit `7d455a5a707b`
**Packet contains:** `README.md`, `evaluator.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluator.py:1-3
- **Note:** evaluator.py is labeled the official WikiTableQuestions evaluator and implements denotation checking.

---

## HA-137 — Input/expected-output schema

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Could you write a file that this evaluator accepts, and do you know exactly
what it returns? Field names, types, and file format count.

- **Label:** partially-documented
- **Evidence pointer:** apicoder/CodeGenAPI/eval_private.py:177-185
- **Note:** Outputs HumanEval-style JSONL with task_id and completion, but CERT benchmark input schema beyond HumanEval is not fully documented.

---

## HA-138 — Sample predictions / trajectories

**Packet:** `PKT-17` · commit `de450af45ff7`
**Packet contains:** `README.md`, `benchmark/eval.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** benchmark/eval.py:49-50
- **Note:** Eval script loads tmp.json predictions, but no concrete sample prediction records are included in the packet.

---

## HA-139 — Evaluator implementation available

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** documented-and-verifiable
- **Evidence pointer:** apicoder/CodeGenAPI/eval_private.py:116-186
- **Note:** Packet includes identifiable code-generation evaluation scripts that generate and save sample completions for scoring.

---

## HA-140 — Grading rules & tie-breaking

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** baselines/nl2code/evaluation.py:117-121
- **Note:** Tokenization failures are skipped via continue, but no documented policy for ties, timeouts, or malformed outputs.

---

## HA-141 — Metric definition

**Packet:** `PKT-01` · commit `483554eae102`
**Packet contains:** `Awesome-Self-Evolution-of-LLM/README.md`, `EPO/Alfshop/eval_agent/agents/__init__.py`, `EPO/Alfshop/eval_agent/agents/base.py`, `EPO/Alfshop/eval_agent/agents/fastchat_agent.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** not-documented
- **Evidence pointer:** EPO/Alfshop/eval_agent/agents/fastchat_agent.py:1-33
- **Note:** Packet contains no BIRD SQL evaluation code or metric definition.

---

## HA-142 — Metric definition

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** README.md:94-99
- **Note:** README reports Overall success rates by split, but packet lacks code defining how per-task env.evaluate scores aggregate.

---

## HA-143 — Grading rules & tie-breaking

**Packet:** `PKT-24` · commit `2ab782ba42b5`
**Packet contains:** `README.md`, `code/preprocess_data.py`, `code/run_BERT.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** code/run_BERT.py:288-315
- **Note:** Accuracy and F1 are defined for label prediction, but edge cases like empty or malformed outputs are not documented.

---

## HA-144 — Predictions->aggregate-score mapping

**Packet:** `PKT-07` · commit `b39aab71da6d`
**Packet contains:** `README.md`, `execution.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:46-61
- **Note:** README shows expected aggregate output as per-library means and an overall mean pass rate across 1000 problems.

---

## HA-145 — Sample predictions / trajectories

**Packet:** `PKT-09` · commit `84ef3d4d94d7`
**Packet contains:** `MetaGPT/README.md`, `MetaGPT/examples/werewolf_game/evals/eval.py`, `MetaGPT/examples/werewolf_game/evals/utils.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** MetaGPT/examples/werewolf_game/evals/eval.py:1-7
- **Note:** Packet contains werewolf-game eval script only; no concrete sample predictions or trajectories in the packet.

---

## HA-146 — Metric definition

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** README.md:123-130
- **Note:** README defines Success Rate as runs with >10% improvement over baseline and Average Improvement among valid submissions.

---

## HA-147 — Grading rules & tie-breaking

**Packet:** `PKT-16` · commit `62d8430dfa0e`
**Packet contains:** `README.md`, `apicoder/CodeGenAPI/APICoder/get_lib_comment_for_eval.py`, `apicoder/CodeGenAPI/eval_baseline.py`, `apicoder/CodeGenAPI/eval_private.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** apicoder/CodeGenAPI/eval_baseline.py:15-16
- **Note:** Generated code is truncated at def/class boundaries, but timeout and malformed-output handling are not documented in packet.

---

## HA-148 — Metric definition

**Packet:** `PKT-23` · commit `49b73a94775f`
**Packet contains:** `README.md`, `evaluation/evaluation.py`, `evaluation/open_spreadsheet.py`, `evaluation/parity_test.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** documented-and-verifiable
- **Evidence pointer:** evaluation/evaluation.py:33-47
- **Note:** Cell-level correctness compares normalized values in answer_position ranges; soft/hard task scores derived from three test cases.

---

## HA-149 — Grading rules & tie-breaking

**Packet:** `PKT-13` · commit `5d71205cc20a`
**Packet contains:** `README.md`, `MLAgentBench/agents/Auto-GPT/scripts/check_requirements.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation.py`, `MLAgentBench/benchmarks/CLRS/env/evaluation_test.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** README.md:123-124
- **Note:** README states >10% improvement threshold for success, but no rules for empty, malformed, or timed-out submissions.

---

## HA-150 — Evaluator implementation available

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Is the code implementing THIS evaluation present and identifiable in the
artifacts? Scoring buried in a training loop is not the same as an
identifiable evaluator.

- **Label:** partially-documented
- **Evidence pointer:** data_modeling/evaluation/bike-sharing-demand_eval.py:1-29
- **Note:** One task-specific RMSLE evaluator is present; README points to external docs for full benchmark evaluation.

---

## HA-151 — Grading rules & tie-breaking

**Packet:** `PKT-03` · commit `6118fa8d5007`
**Packet contains:** `README.md`, `blade_bench/eval/__init__.py`, `blade_bench/eval/convert.py`, `blade_bench/eval/datamodel/run.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** partially-documented
- **Evidence pointer:** blade_bench/eval/convert.py:111-116
- **Note:** RunError paths record execution/conversion failures, but tie-breaking and timeout policies are not documented.

---

## HA-152 — Metric definition

**Packet:** `PKT-08` · commit `ba786096137a`
**Packet contains:** `README.md`, `data_modeling/evaluation/bike-sharing-demand_eval.py`, `data_modeling/evaluation/cat-in-the-dat-ii_eval.py`, `data_modeling/evaluation/cat-in-the-dat_eval.py`

> Is the metric named AND defined precisely enough to reimplement? 'Accuracy'
alone is partial unless what counts as correct is stated.

- **Label:** partially-documented
- **Evidence pointer:** data_modeling/evaluation/bike-sharing-demand_eval.py:7-11
- **Note:** RMSLE formula is defined for bike-sharing-demand, but other DSBench task metrics are only referenced externally.

---

## HA-153 — Predictions->aggregate-score mapping

**Packet:** `PKT-20` · commit `b7b5b8c890cd`
**Packet contains:** `README.md`, `baselines/nl2code/evaluation.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/bleu.py`, `baselines/seq2seq_attention_copy/seq2seq/metrics/rouge.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** documented-and-verifiable
- **Evidence pointer:** baselines/nl2code/evaluation.py:243-252
- **Note:** Final metrics divide cumulative exact-match and BLEU sums by dataset.count to produce mean accuracy and BLEU.

---

## HA-154 — Grading rules & tie-breaking

**Packet:** `PKT-22` · commit `c2a3a6c2f5d7`
**Packet contains:** `README.md`, `desktop_env/evaluators/__init__.py`, `desktop_env/evaluators/getters/dbt.py`, `desktop_env/evaluators/getters/file.py`

> What happens on ties, empty predictions, malformed output, timeouts, or
partially correct answers? Silence on all of these is not-documented.

- **Label:** not-documented
- **Evidence pointer:** desktop_env/evaluators/getters/dbt.py:139-140
- **Note:** Getter helpers return None on missing jobs/files, but no comprehensive grading rules for edge cases are stated.

---

## HA-155 — Predictions->aggregate-score mapping

**Packet:** `PKT-18` · commit `93b98062e55f`
**Packet contains:** `README.md`, `ai_rd_fix_embedding/assets/score.py`, `ai_rd_restricted_mlm/assets/score.py`, `ai_rd_triton_cumsum/assets/score.py`

> How do per-item results become the single reported number? Mean over what
denominator, weighted how, excluding what?

- **Label:** partially-documented
- **Evidence pointer:** README.md:68-158
- **Note:** README lists per-task-family score formulas and starting/official values, but no code shows cross-task aggregation to one reported number.

---

## HA-156 — Sample predictions / trajectories

**Packet:** `PKT-02` · commit `b83332416ea2`
**Packet contains:** `README.md`, `eval/eval.py`, `gcs_eval.py`, `gcs_eval_checkpoints.py`

> Is there at least one concrete example of model output in the format the
evaluator consumes?

- **Label:** not-documented
- **Evidence pointer:** README.md:197-298
- **Note:** README shows sample CLI commands and output CSV paths, but no concrete model prediction or trajectory files are included.

---
