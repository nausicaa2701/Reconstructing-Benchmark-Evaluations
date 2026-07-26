# Three-Provider LLM-Judge Panel

This directory implements the evidence-grounded R2 sensitivity study. It uses
three independently operated providers and never treats model agreement as
human inter-rater reliability or ground truth.

## Frozen design

- OpenAI: `gpt-5.1-2025-11-13`
- Anthropic: `claude-sonnet-5`
- Google: `gemini-3.5-flash`
- 26 primary-cohort releases, six decisions each, 468 raw decisions
- identical pseudonymous packets and a single frozen prompt
- no browsing, tools, code execution, or access to other judges/outcomes
- exact majority, then deterministic conservative tie-breaking
- permissive, strict, unanimous, and leave-one-judge-out R2 analyses
- hard local spend guard: USD 10

The four post-freeze releases are not mixed into this panel because their
current evidence records are coding summaries rather than the same frozen
README/source bundles used for the primary cohort.

## Secret setup

Create a local file that Git ignores:

```bash
cp .env.example .env
chmod 600 .env
```

Fill exactly these variables in `.env`:

```dotenv
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
```

Do not paste keys into prompts, issues, logs, or committed files. The runner
never serializes request headers and all generated work stays under the ignored
`artifact/llm_judges/work/` directory until explicit release.

Provider purchase and billing steps are in `API_KEY_SETUP.md`.

## Runbook

Prepare identical evidence packets and run all local tests:

```bash
python3 artifact/llm_judges/prepare_packets.py
python3 artifact/llm_judges/test_panel.py
python3 artifact/llm_judges/check_keys.py
```

Dry-run the complete panel. This does not make API calls:

```bash
python3 artifact/llm_judges/run_panel.py
```

Run a three-call pilot first. The same outputs will be reused by the full run:

```bash
python3 artifact/llm_judges/run_panel.py \
  --execute --confirm-spend USD10 --packet B001
```

Inspect the three normalized pilot files, then resume all missing requests:

```bash
python3 artifact/llm_judges/run_panel.py \
  --execute --confirm-spend USD10
```

For Gemini 3.5 Flash, use the pre-specified low-thinking production run so
reasoning tokens cannot crowd the structured JSON out of the 4k output cap:

```bash
python3 artifact/llm_judges/run_panel.py --run-id panel-v1-gemini-low \
  --providers gemini --gemini-thinking-level low \
  --execute --confirm-spend USD10
python3 artifact/llm_judges/aggregate_panel.py \
  --gemini-run-id panel-v1-gemini-low
```

The runner checks estimated cost before the run and before every request. It
resumes completed provider/packet pairs without charging for them again.

Aggregate only after all 78 primary requests are complete:

```bash
python3 artifact/llm_judges/aggregate_panel.py
```

Run the preselected 20% repeatability sample under a separate run ID:

```bash
python3 artifact/llm_judges/run_panel.py --run-id panel-v1-repeat \
  --providers openai anthropic --execute --confirm-spend USD10 \
  --packet B001 --packet B004 --packet B008 \
  --packet B009 --packet B021 --packet B024
python3 artifact/llm_judges/run_panel.py --run-id panel-v1-repeat-gemini-low \
  --providers gemini --gemini-thinking-level low \
  --execute --confirm-spend USD10 \
  --packet B001 --packet B004 --packet B008 \
  --packet B009 --packet B021 --packet B024
python3 artifact/llm_judges/repeatability.py \
  --gemini-base-run panel-v1-gemini-low \
  --gemini-repeat-run panel-v1-repeat-gemini-low
```

Repeatability spend is tracked in a separate run ledger, while the runner sums
all run ledgers before every request and enforces the USD 10 cap globally.

After analysis and repeatability checks, export a commit-ready, hash-verified
artifact. The exporter refuses incomplete runs and scans for common key forms:

```bash
python3 artifact/llm_judges/export_release.py \
  --gemini-run-id panel-v1-gemini-low \
  --repeat-run-id panel-v1-repeat-t600 \
  --gemini-repeat-run-id panel-v1-repeat-gemini-low \
  --superseded-partial-run-id panel-v1-repeat
```

## Outputs

`work/runs/<run-id>/` contains:

- `raw/`: complete provider responses without API keys;
- `normalized/`: schema- and evidence-validated judgments;
- `usage.jsonl`: model IDs, tokens, latency, and estimated cost;
- `errors.jsonl`: bounded error records, if any.

`work/analysis/` contains the raw decision table, deterministic aggregate,
benchmark R2 variants, reliability statistics, clustered bootstrap interval,
pairwise agreement, unanimity, leave-one-out bounds, and repeatability.

## Billing note

The dry-run estimate is based on the current packets and the prices frozen in
`config.json`. The local USD 10 guard limits recorded API consumption; it does
not control minimum initial credit purchases or provider-side auto-reload.
Disable auto-reload and set provider-side project limits wherever available.
