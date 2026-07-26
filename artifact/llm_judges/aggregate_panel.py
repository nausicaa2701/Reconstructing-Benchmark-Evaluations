#!/usr/bin/env python3
"""Deterministically aggregate model labels and compute robustness statistics."""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from common import (
    CRITERIA, HERE, LABELS, PERMISSIVE_PASS, R2_CRITERIA, STRICT_PASS, WORK,
    read_json,
)

PROVIDERS = ["openai", "anthropic", "gemini"]
WEAKNESS = {
    "not-documented": 0,
    "access-blocked": 0,
    "claimed-but-not-verifiable": 1,
    "partially-documented": 2,
    "documented-and-verifiable": 3,
    "not-applicable": 4,
}


def aggregate_labels(labels: list[str]) -> tuple[str, str]:
    counts = Counter(labels)
    if counts["not-applicable"] >= 2:
        return "not-applicable", "majority-not-applicable"
    label, count = counts.most_common(1)[0]
    if count >= 2:
        return label, "exact-majority"
    pass_labels = [label for label in labels if label in PERMISSIVE_PASS]
    fail_labels = [label for label in labels if label not in PERMISSIVE_PASS]
    side = pass_labels if len(pass_labels) >= 2 else fail_labels
    return min(side, key=lambda value: (WEAKNESS[value], value)), "conservative-three-way-tie"


def nominal_alpha(rows: list[list[str]]) -> float:
    if not rows:
        return float("nan")
    observed_pairs = total_pairs = 0
    pooled = Counter()
    for row in rows:
        pooled.update(row)
        for left, right in itertools.combinations(row, 2):
            observed_pairs += left != right
            total_pairs += 1
    observed = observed_pairs / total_pairs
    n = sum(pooled.values())
    expected = 1 - sum(v * (v - 1) for v in pooled.values()) / (n * (n - 1))
    return 1.0 if expected == 0 else 1 - observed / expected


def gwet_ac1(rows: list[list[str]], categories: list[str] | None = None) -> float:
    agreement = sum(a == b for row in rows for a, b in itertools.combinations(row, 2))
    pair_count = sum(1 for row in rows for _ in itertools.combinations(row, 2))
    pa = agreement / pair_count
    pooled = Counter(label for row in rows for label in row)
    category_values = categories or LABELS
    n, category_count = sum(pooled.values()), len(category_values)
    probabilities = [pooled[label] / n for label in category_values]
    pe = sum(p * (1 - p) for p in probabilities) / (category_count - 1)
    return 1.0 if pe == 1 else (pa - pe) / (1 - pe)


def binary_rows(rows: list[list[str]]) -> list[list[str]]:
    return [
        ["pass" if label in PERMISSIVE_PASS else "fail" for label in row]
        for row in rows
    ]


def pairwise_agreement(rows: list[list[str]]) -> dict[str, float]:
    return {
        f"{left}__{right}": sum(
            row[PROVIDERS.index(left)] == row[PROVIDERS.index(right)] for row in rows
        ) / len(rows)
        for left, right in itertools.combinations(PROVIDERS, 2)
    }


def load_records(run_dirs: dict[str, Path]) -> tuple[dict, dict]:
    mapping = read_json(WORK / "private_benchmark_map.json")
    records = defaultdict(dict)
    for provider in PROVIDERS:
        provider_dir = run_dirs[provider] / "normalized" / provider
        if not provider_dir.exists():
            raise SystemExit(f"Missing provider output directory: {provider_dir}")
        for path in sorted(provider_dir.glob("B*.json")):
            payload = read_json(path)
            packet_id = payload["judgment"]["packet_id"]
            records[packet_id][provider] = {
                d["criterion"]: d for d in payload["judgment"]["decisions"]
            }
    incomplete = {packet: set(PROVIDERS) - set(values) for packet, values in records.items() if len(values) != 3}
    expected = set(mapping)
    if set(records) != expected or incomplete:
        raise SystemExit(f"Panel incomplete: packets={len(records)}/{len(expected)}, missing={incomplete}")
    return records, mapping


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def analyze(run_dirs: dict[str, Path], output_dir: Path, bootstrap_samples: int = 2000) -> dict:
    records, mapping = load_records(run_dirs)
    raw_rows, aggregate_rows, matrices = [], [], []
    per_criterion = defaultdict(list)
    benchmark_judge_pass = defaultdict(dict)
    benchmark_aggregate = defaultdict(dict)
    for packet_id in sorted(records):
        for criterion in CRITERIA:
            labels = [records[packet_id][p][criterion]["label"] for p in PROVIDERS]
            matrices.append(labels)
            per_criterion[criterion].append(labels)
            aggregated, rule = aggregate_labels(labels)
            benchmark_aggregate[packet_id][criterion] = aggregated
            row = {
                "packet_id": packet_id,
                "benchmark": mapping[packet_id]["benchmark"],
                "criterion": criterion,
                **{provider: label for provider, label in zip(PROVIDERS, labels)},
                "aggregated_label": aggregated,
                "aggregation_rule": rule,
            }
            aggregate_rows.append(row)
            for provider in PROVIDERS:
                decision = records[packet_id][provider][criterion]
                raw_rows.append({
                    "packet_id": packet_id,
                    "benchmark": mapping[packet_id]["benchmark"],
                    "criterion": criterion,
                    "provider": provider,
                    "label": decision["label"],
                    "evidence_refs": json.dumps(decision["evidence_refs"], separators=(",", ":")),
                    "evidence_note": decision["evidence_note"],
                    "confidence": decision["confidence"],
                })
        for provider in PROVIDERS:
            values = records[packet_id][provider]
            benchmark_judge_pass[packet_id][provider] = all(
                values[c]["label"] in PERMISSIVE_PASS for c in R2_CRITERIA
            )

    pairwise = pairwise_agreement(matrices)
    binary_matrices = binary_rows(matrices)
    r2_matrices = [
        row for row, aggregate_row in zip(matrices, aggregate_rows)
        if aggregate_row["criterion"] in R2_CRITERIA
    ]
    r2_binary_matrices = binary_rows(r2_matrices)
    unanimous = sum(len(set(row)) == 1 for row in matrices) / len(matrices)
    binary_unanimous = sum(
        len({label in PERMISSIVE_PASS for label in row}) == 1 for row in matrices
    ) / len(matrices)

    rng = random.Random(42)
    packet_ids = sorted(records)
    boot = []
    for _ in range(bootstrap_samples):
        sampled = [rng.choice(packet_ids) for _ in packet_ids]
        rows = []
        for packet_id in sampled:
            for criterion in CRITERIA:
                rows.append([records[packet_id][p][criterion]["label"] for p in PROVIDERS])
        boot.append(nominal_alpha(rows))
    boot.sort()
    ci = [boot[int(0.025 * len(boot))], boot[min(len(boot) - 1, int(0.975 * len(boot)))]]

    r2_rows = []
    for packet_id in packet_ids:
        values = benchmark_aggregate[packet_id]
        r2_rows.append({
            "packet_id": packet_id,
            "benchmark": mapping[packet_id]["benchmark"],
            "r2_majority_permissive": int(all(values[c] in PERMISSIVE_PASS for c in R2_CRITERIA)),
            "r2_majority_strict": int(all(values[c] in STRICT_PASS for c in R2_CRITERIA)),
            "r2_unanimous_permissive": int(all(benchmark_judge_pass[packet_id].values())),
        })

    leave_one_out = {}
    for omitted in PROVIDERS:
        kept = [p for p in PROVIDERS if p != omitted]
        pessimistic = optimistic = 0
        for packet_id in packet_ids:
            pessimistic += all(
                all(records[packet_id][p][c]["label"] in PERMISSIVE_PASS for p in kept)
                for c in R2_CRITERIA
            )
            optimistic += all(
                any(records[packet_id][p][c]["label"] in PERMISSIVE_PASS for p in kept)
                for c in R2_CRITERIA
            )
        leave_one_out[omitted] = {
            "kept": kept,
            "pessimistic_r2": pessimistic,
            "optimistic_r2": optimistic,
        }

    stats = {
        "protocol": "three-provider evidence-grounded model-judge panel",
        "packets": len(packet_ids),
        "cells": len(matrices),
        "raw_decisions": len(matrices) * len(PROVIDERS),
        "krippendorff_alpha_nominal": nominal_alpha(matrices),
        "krippendorff_alpha_nominal_benchmark_bootstrap_ci95": ci,
        "gwet_ac1_nominal": gwet_ac1(matrices),
        "pairwise_exact_agreement": pairwise,
        "exact_unanimous_rate": unanimous,
        "binary_pass_fail_unanimous_rate": binary_unanimous,
        "binary_pass_fail_alpha": nominal_alpha(binary_matrices),
        "binary_pass_fail_gwet_ac1": gwet_ac1(binary_matrices, ["pass", "fail"]),
        "pairwise_binary_pass_fail_agreement": pairwise_agreement(binary_matrices),
        "r2_criteria_cells": len(r2_matrices),
        "r2_criteria_nominal_alpha": nominal_alpha(r2_matrices),
        "r2_criteria_nominal_gwet_ac1": gwet_ac1(r2_matrices),
        "r2_criteria_exact_unanimous_rate": sum(
            len(set(row)) == 1 for row in r2_matrices
        ) / len(r2_matrices),
        "r2_criteria_binary_alpha": nominal_alpha(r2_binary_matrices),
        "r2_criteria_binary_gwet_ac1": gwet_ac1(
            r2_binary_matrices, ["pass", "fail"]
        ),
        "r2_criteria_binary_unanimous_rate": sum(
            len(set(row)) == 1 for row in r2_binary_matrices
        ) / len(r2_binary_matrices),
        "r2_criteria_pairwise_binary_agreement": pairwise_agreement(r2_binary_matrices),
        "per_criterion_alpha": {k: nominal_alpha(v) for k, v in per_criterion.items()},
        "r2_majority_permissive": sum(r["r2_majority_permissive"] for r in r2_rows),
        "r2_majority_strict": sum(r["r2_majority_strict"] for r in r2_rows),
        "r2_unanimous_permissive": sum(r["r2_unanimous_permissive"] for r in r2_rows),
        "leave_one_judge_out": leave_one_out,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "raw_model_judgments.csv", raw_rows)
    write_csv(output_dir / "aggregated_model_judgments.csv", aggregate_rows)
    write_csv(output_dir / "model_panel_r2.csv", r2_rows)
    (output_dir / "model_panel_stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="panel-v1")
    parser.add_argument("--gemini-run-id", default=None)
    parser.add_argument("--output-dir", type=Path, default=WORK / "analysis")
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    args = parser.parse_args()
    base = WORK / "runs" / args.run_id
    run_dirs = {provider: base for provider in PROVIDERS}
    if args.gemini_run_id:
        run_dirs["gemini"] = WORK / "runs" / args.gemini_run_id
    print(json.dumps(analyze(run_dirs, args.output_dir, args.bootstrap_samples), indent=2))


if __name__ == "__main__":
    main()
