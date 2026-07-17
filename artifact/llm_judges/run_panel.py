#!/usr/bin/env python3
"""Run the frozen three-provider panel with a hard dollar-denominated guard."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    HERE, ROOT, WORK, canonical_hash, canonicalize_evidence_refs, estimate_tokens,
    load_config, load_dotenv, read_json, render_packet, request_cost, validate_decisions,
)
from prepare_packets import build

KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
}


class ProviderHTTPError(RuntimeError):
    def __init__(self, code: int, detail: str):
        super().__init__(f"HTTP {code} from provider: {detail}")
        self.code = code
        self.detail = detail

    @property
    def retryable(self) -> bool:
        depleted = "prepayment credits are depleted" in self.detail.lower()
        return self.code >= 500 or (self.code == 429 and not depleted)


def post_json(url: str, headers: dict[str, str], body: dict, timeout: int) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode(),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:2000]
        raise ProviderHTTPError(exc.code, detail) from exc


def extract_openai_text(data: dict) -> str:
    if isinstance(data.get("output_text"), str):
        return data["output_text"]
    texts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                texts.append(content["text"])
    if not texts:
        raise ValueError("OpenAI response contained no output_text")
    return "".join(texts)


def call_openai(cfg: dict, system: str, prompt: str, schema: dict, timeout: int) -> tuple:
    body = {
        "model": cfg["model"],
        "instructions": system,
        "input": prompt,
        "reasoning": {"effort": cfg["reasoning_effort"]},
        "max_output_tokens": cfg["max_output_tokens"],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "benchmark_artifact_judgment",
                "strict": True,
                "schema": schema,
            }
        },
        "store": False,
    }
    data = post_json(
        "https://api.openai.com/v1/responses",
        {"Authorization": f"Bearer {os.environ[KEYS['openai']]}"}, body, timeout,
    )
    usage = data.get("usage", {})
    return (
        extract_openai_text(data), data,
        int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)),
    )


def call_anthropic(cfg: dict, system: str, prompt: str, schema: dict, timeout: int) -> tuple:
    body = {
        "model": cfg["model"],
        "max_tokens": cfg["max_output_tokens"],
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
        "output_config": {
            "effort": cfg["effort"],
            "format": {"type": "json_schema", "schema": schema},
        },
    }
    data = post_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": os.environ[KEYS["anthropic"]],
            "anthropic-version": "2023-06-01",
        }, body, timeout,
    )
    texts = [part["text"] for part in data.get("content", []) if part.get("type") == "text"]
    if not texts:
        raise ValueError("Anthropic response contained no text block")
    usage = data.get("usage", {})
    return (
        "".join(texts), data,
        int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)),
    )


def call_gemini(cfg: dict, system: str, prompt: str, schema: dict, timeout: int) -> tuple:
    model = urllib.parse.quote(cfg["model"], safe="")
    generation_config = {
        "responseMimeType": "application/json",
        "responseJsonSchema": schema,
        "maxOutputTokens": cfg["max_output_tokens"],
    }
    if cfg.get("thinking_level"):
        generation_config["thinkingConfig"] = {"thinkingLevel": cfg["thinking_level"]}
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": generation_config,
    }
    data = post_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"x-goog-api-key": os.environ[KEYS["gemini"]]}, body, timeout,
    )
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    texts = [part["text"] for part in parts if isinstance(part.get("text"), str)]
    if not texts:
        raise ValueError("Gemini response contained no text part")
    usage = data.get("usageMetadata", {})
    output_tokens = int(usage.get("candidatesTokenCount", 0)) + int(
        usage.get("thoughtsTokenCount", 0)
    )
    return (
        "".join(texts), data,
        int(usage.get("promptTokenCount", 0)), output_tokens,
    )


CALLERS = {"openai": call_openai, "anthropic": call_anthropic, "gemini": call_gemini}


def existing_spend(ledger: Path) -> float:
    if not ledger.exists():
        return 0.0
    return sum(json.loads(line)["cost_usd"] for line in ledger.read_text().splitlines() if line)


def global_spend() -> float:
    return sum(existing_spend(path) for path in (WORK / "runs").glob("*/usage.jsonl"))


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def planned_jobs(providers: list[str], packet_ids: list[str], run_dir: Path) -> list[tuple]:
    jobs = []
    for packet_id in packet_ids:
        for provider in providers:
            normalized = run_dir / "normalized" / provider / f"{packet_id}.json"
            if not normalized.exists():
                jobs.append((provider, packet_id))
    return jobs


def response_text(provider: str, response: dict) -> str:
    if provider == "openai":
        return extract_openai_text(response)
    if provider == "anthropic":
        return "".join(
            part["text"] for part in response.get("content", []) if part.get("type") == "text"
        )
    parts = response.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return "".join(part["text"] for part in parts if isinstance(part.get("text"), str))


def recover_canonicalizable_outputs(
    providers: list[str], packet_ids: list[str], run_dir: Path
) -> int:
    recovered = 0
    for provider in providers:
        for packet_id in packet_ids:
            normalized = run_dir / "normalized" / provider / f"{packet_id}.json"
            if normalized.exists():
                continue
            packet = read_json(WORK / "packets" / f"{packet_id}.json")
            attempts = sorted((run_dir / "raw" / provider).glob(f"{packet_id}.attempt-*.json"))
            for path in reversed(attempts):
                payload = read_json(path)
                try:
                    result = json.loads(response_text(provider, payload["response"]))
                    changes = canonicalize_evidence_refs(result, packet)
                    if not changes:
                        continue
                    validate_decisions(result, packet)
                except (ValueError, json.JSONDecodeError, KeyError):
                    continue
                metadata = dict(payload["metadata"])
                metadata["validation_status"] = "valid-after-reference-canonicalization"
                metadata["canonicalized_refs"] = changes
                normalized.parent.mkdir(parents=True, exist_ok=True)
                normalized.write_text(
                    json.dumps({"metadata": metadata, "judgment": result}, indent=2) + "\n"
                )
                recovered += 1
                break
    return recovered


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Make billable API requests")
    parser.add_argument("--confirm-spend", default="", help="Must equal USD10 when --execute is used")
    parser.add_argument("--providers", nargs="+", choices=sorted(CALLERS), default=sorted(CALLERS))
    parser.add_argument("--packet", action="append", dest="packets", help="Run only this packet ID")
    parser.add_argument("--run-id", default="panel-v1")
    parser.add_argument("--retry-invalid", type=int, default=1, choices=range(0, 3))
    parser.add_argument(
        "--gemini-thinking-level", choices=["minimal", "low", "medium", "high"],
        help="Explicit Gemini thinking level; frozen into the paid-run manifest",
    )
    args = parser.parse_args()

    config = load_config()
    schema = read_json(HERE / "judge_output_schema.json")
    system = (HERE / "prompt.txt").read_text()
    if not (WORK / "packet_manifest.json").exists():
        build(WORK)
    manifest = read_json(WORK / "packet_manifest.json")
    available = [row["packet_id"] for row in manifest]
    packet_ids = args.packets or available
    unknown = set(packet_ids) - set(available)
    if unknown:
        raise SystemExit(f"Unknown packet IDs: {sorted(unknown)}")

    run_dir = WORK / "runs" / args.run_id
    ledger = run_dir / "usage.jsonl"
    run_manifest = {
        "protocol_version": config["protocol_version"],
        "config_sha256": canonical_hash(config),
        "schema_sha256": canonical_hash(schema),
        "prompt_sha256": hashlib.sha256(system.encode()).hexdigest(),
        "packets": {row["packet_id"]: row["packet_sha256"] for row in manifest},
        "runtime_overrides": {"gemini_thinking_level": args.gemini_thinking_level},
    }
    recovered = recover_canonicalizable_outputs(args.providers, packet_ids, run_dir)
    jobs = planned_jobs(args.providers, packet_ids, run_dir)
    estimates = []
    for provider, packet_id in jobs:
        packet = read_json(WORK / "packets" / f"{packet_id}.json")
        prompt = render_packet(packet)
        cfg = config["models"][provider]
        estimates.append(request_cost(cfg, estimate_tokens(system + prompt), config["max_output_tokens"]))
    plan = {
        "mode": "execute" if args.execute else "dry-run",
        "run_id": args.run_id,
        "providers": args.providers,
        "packets": len(packet_ids),
        "pending_requests": len(jobs),
        "locally_recovered_outputs": recovered,
        "conservative_planned_cost_usd": round(sum(estimates), 4),
        "run_spend_usd": round(existing_spend(ledger), 4),
        "global_study_spend_usd": round(global_spend(), 4),
        "hard_budget_usd": config["budget_usd"],
        "protocol_sha256": canonical_hash(run_manifest),
    }
    print(json.dumps(plan, indent=2))
    if not args.execute:
        return
    if args.confirm_spend != "USD10":
        raise SystemExit("Billable execution requires --confirm-spend USD10")
    frozen_manifest_path = run_dir / "run_manifest.json"
    if frozen_manifest_path.exists():
        if read_json(frozen_manifest_path) != run_manifest:
            if existing_spend(ledger) == 0 and not any((run_dir / "normalized").glob("*/*.json")):
                frozen_manifest_path.write_text(json.dumps(run_manifest, indent=2) + "\n")
            else:
                raise SystemExit("Run manifest differs from the frozen paid-run protocol")
    else:
        frozen_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        frozen_manifest_path.write_text(json.dumps(run_manifest, indent=2) + "\n")
    load_dotenv()
    missing = [KEYS[p] for p in args.providers if not os.environ.get(KEYS[p])]
    if missing:
        raise SystemExit(f"Missing API keys: {', '.join(missing)}")
    if global_spend() + sum(estimates) > float(config["budget_usd"]):
        raise SystemExit("Conservative preflight estimate exceeds the hard budget")

    for job_index, (provider, packet_id) in enumerate(jobs, 1):
        packet = read_json(WORK / "packets" / f"{packet_id}.json")
        prompt = render_packet(packet)
        model_cfg = {**config["models"][provider], "max_output_tokens": config["max_output_tokens"]}
        if provider == "gemini" and args.gemini_thinking_level:
            model_cfg["thinking_level"] = args.gemini_thinking_level
        reserved = request_cost(
            model_cfg, estimate_tokens(system + prompt), config["max_output_tokens"]
        )
        if global_spend() + reserved > float(config["budget_usd"]):
            raise SystemExit("Hard budget guard stopped before the next request")
        print(f"[{job_index}/{len(jobs)}] {provider} {packet_id}", flush=True)
        for attempt in range(args.retry_invalid + 1):
            started = time.monotonic()
            try:
                output_text, raw, input_tokens, output_tokens = CALLERS[provider](
                    model_cfg, system, prompt, schema, int(config["request_timeout_seconds"])
                )
            except ProviderHTTPError as exc:
                append_jsonl(run_dir / "errors.jsonl", {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "provider": provider,
                    "packet_id": packet_id,
                    "attempt": attempt + 1,
                    "error": str(exc),
                })
                if not exc.retryable or attempt >= args.retry_invalid:
                    raise
                time.sleep(min(2 ** attempt, 10))
                continue
            cost = request_cost(model_cfg, input_tokens, output_tokens)
            metadata = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "provider": provider,
                "model": model_cfg["model"],
                "packet_id": packet_id,
                "packet_sha256": packet["packet_sha256"],
                "protocol_sha256": canonical_hash(run_manifest),
                "attempt": attempt + 1,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": cost,
                "elapsed_seconds": round(time.monotonic() - started, 3),
            }
            raw_path = run_dir / "raw" / provider / f"{packet_id}.attempt-{attempt + 1}.json"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_text(json.dumps({"metadata": metadata, "response": raw}, indent=2) + "\n")
            try:
                result = json.loads(output_text)
                changes = canonicalize_evidence_refs(result, packet)
                validate_decisions(result, packet)
                metadata["validation_status"] = "valid"
                if changes:
                    metadata["canonicalized_refs"] = changes
            except (ValueError, json.JSONDecodeError) as exc:
                metadata["validation_status"] = "invalid"
                append_jsonl(ledger, metadata)
                append_jsonl(run_dir / "errors.jsonl", {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "provider": provider,
                    "packet_id": packet_id,
                    "attempt": attempt + 1,
                    "error": str(exc),
                })
                if attempt >= args.retry_invalid:
                    raise
                continue
            append_jsonl(ledger, metadata)
            break
        normalized_path = run_dir / "normalized" / provider / f"{packet_id}.json"
        normalized_path.parent.mkdir(parents=True, exist_ok=True)
        normalized_path.write_text(
            json.dumps({"metadata": metadata, "judgment": result}, indent=2) + "\n"
        )
    print(
        f"Complete. Run spend: ${existing_spend(ledger):.4f}; "
        f"global study spend: ${global_spend():.4f}"
    )


if __name__ == "__main__":
    main()
