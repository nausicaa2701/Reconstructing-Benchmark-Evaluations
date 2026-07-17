# API Key and Billing Setup

The panel consumes at most USD 10 according to its local ledger. Provider
minimum deposits are separate and may make the initial cash outlay larger than
the study's actual consumption.

## OpenAI

1. Open <https://platform.openai.com/settings/organization/billing/overview>.
2. Add payment details and buy the minimum prepaid balance offered. New-account
   prepaid billing currently has a USD 5 minimum and USD 10 default.
3. Turn auto-recharge off for this one-off audit.
4. Open <https://platform.openai.com/api-keys> and create a project key.
5. Give it only the permissions required to read models and create Responses.
6. Put the one-time-displayed secret in `OPENAI_API_KEY` inside `.env`.

ChatGPT subscriptions and API billing are separate.

## Anthropic

1. Open <https://console.anthropic.com/settings/billing> and buy the smallest
   usage-credit amount the Console permits.
2. Keep auto-reload disabled.
3. Open <https://console.anthropic.com/settings/keys> and create a key for this
   audit workspace.
4. Put it in `ANTHROPIC_API_KEY` inside `.env`.

Anthropic API usage is prepaid; successful calls consume usage credits.

## Google Gemini

1. Open <https://aistudio.google.com/apikey> and create a dedicated project/key.
2. The free tier may be enough for the 26-call judge workload. For paid-service
   data terms and steadier limits, choose **Set up billing** for that project.
3. New paid accounts may require a USD 10 prepayment. Disable auto-reload and
   set a project spend cap where available.
4. Use the new authorization-key type offered by AI Studio.
5. Put the key in `GEMINI_API_KEY` inside `.env`.

## Local verification

```bash
cp .env.example .env
chmod 600 .env
# Edit .env locally, then:
python3 artifact/llm_judges/check_keys.py
python3 artifact/llm_judges/run_panel.py
```

The second command is a free dry-run. Do not use `--execute` until all three
credential checks pass and the displayed estimate is below USD 10.

