#!/usr/bin/env python3
"""Shared constants, validation, and cost helpers for the model-judge panel."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = HERE / "work"

CRITERIA = [
    "Input/expected-output schema",
    "Metric definition",
    "Evaluator implementation available",
    "Grading rules & tie-breaking",
    "Predictions->aggregate-score mapping",
    "Sample predictions / trajectories",
]
R2_CRITERIA = set(CRITERIA[:5])
LABELS = {
    "documented-and-verifiable",
    "partially-documented",
    "claimed-but-not-verifiable",
    "not-documented",
    "not-applicable",
    "access-blocked",
}
PERMISSIVE_PASS = {
    "documented-and-verifiable", "partially-documented", "not-applicable"
}
STRICT_PASS = {"documented-and-verifiable", "not-applicable"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def load_config() -> dict[str, Any]:
    return read_json(HERE / "config.json")


def load_dotenv(path: Path | None = None) -> None:
    path = path or ROOT / ".env"
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def estimate_tokens(text: str) -> int:
    """Conservative provider-neutral estimate used only for preflight budgeting."""
    return max(1, (len(text.encode("utf-8")) + 2) // 3)


def request_cost(model_cfg: dict[str, Any], input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens * float(model_cfg["input_usd_per_million"])
        + output_tokens * float(model_cfg["output_usd_per_million"])
    ) / 1_000_000


def validate_decisions(result: dict[str, Any], packet: dict[str, Any]) -> None:
    if result.get("packet_id") != packet["packet_id"]:
        raise ValueError("packet_id does not match request")
    decisions = result.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != len(CRITERIA):
        raise ValueError("expected exactly six decisions")
    if {d.get("criterion") for d in decisions} != set(CRITERIA):
        raise ValueError("criteria are missing, duplicated, or unknown")
    source_lines = {s["source_id"]: s["line_count"] for s in packet["sources"]}
    for decision in decisions:
        if decision.get("label") not in LABELS:
            raise ValueError(f"invalid label for {decision.get('criterion')}")
        refs = decision.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            raise ValueError(f"evidence_refs required for {decision.get('criterion')}")
        for ref in refs:
            source_id = ref.get("source_id")
            start, end = ref.get("line_start"), ref.get("line_end")
            if source_id not in source_lines:
                raise ValueError(f"unknown evidence source {source_id}")
            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError("evidence line ranges must be integers")
            if start < 1 or end < start or end > source_lines[source_id]:
                raise ValueError(f"invalid line range for {source_id}: {start}-{end}")
        note = decision.get("evidence_note", "")
        if not isinstance(note, str) or not note.strip() or len(note) > 500:
            raise ValueError("evidence_note must contain 1-500 characters")


def canonicalize_evidence_refs(result: dict[str, Any], packet: dict[str, Any]) -> list[dict[str, str]]:
    """Replace an exact unique source path with its packet source ID; change nothing else."""
    by_id = {source["source_id"] for source in packet["sources"]}
    path_to_ids: dict[str, list[str]] = {}
    for source in packet["sources"]:
        path_to_ids.setdefault(source["path"], []).append(source["source_id"])
    changes = []
    for decision in result.get("decisions", []):
        for ref in decision.get("evidence_refs", []):
            value = ref.get("source_id")
            candidates = path_to_ids.get(value, [])
            if value not in by_id and len(candidates) == 1:
                ref["source_id"] = candidates[0]
                changes.append({"from": value, "to": candidates[0]})
    return changes


def render_packet(packet: dict[str, Any]) -> str:
    parts = [
        f"PACKET_ID: {packet['packet_id']}",
        f"FROZEN_COMMIT: {packet['frozen_commit']}",
        f"PACKET_SHA256: {packet['packet_sha256']}",
    ]
    for source in packet["sources"]:
        parts.extend([
            "",
            f"===== {source['source_id']} | {source['path']} | sha256={source['sha256']} =====",
            source["numbered_content"],
        ])
    return "\n".join(parts)
