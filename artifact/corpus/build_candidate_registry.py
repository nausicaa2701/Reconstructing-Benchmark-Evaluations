#!/usr/bin/env python3
"""Combine the frozen cohort and unresolved ledger into one screening registry."""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    extension = {
        row["benchmark"]: row
        for row in __import__("json").loads(
            (HERE / "rescreened_release_coding.json").read_text()
        )["releases"]
    }
    rows = []
    with (HERE / "corpus_frozen.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append({
                "benchmark": row["benchmark"],
                "category": row["category"],
                "screening_status": "repository_resolved_audit_cohort",
                "repository_or_artifact": row["repo_url"],
                "frozen_commit": row["frozen_commit"],
                "screening_note": row.get("paper_note", ""),
                "audit_date": row["audit_date"],
            })
    with (HERE / "corpus_excluded.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            found = extension.get(row["benchmark"])
            rows.append({
                "benchmark": row["benchmark"],
                "category": row["category"],
                "screening_status": "post_freeze_resolved_extension" if found else "official_artifact_unresolved_after_rescreen",
                "repository_or_artifact": found["repo_url"] if found else "",
                "frozen_commit": found["frozen_commit"] if found else "",
                "screening_note": ("Found during post-freeze search; coded as expansion sensitivity, not added retrospectively to the primary cohort"
                                   if found else row["exclusion_reason"]),
                "audit_date": "2026-07-16" if found else "2026-07-16",
            })
    if len(rows) != 35:
        raise SystemExit(f"expected 35 candidates, found {len(rows)}")
    fields = list(rows[0])
    with (HERE / "candidate_registry.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["benchmark"].lower()))
    print("wrote artifact/corpus/candidate_registry.csv: 26 primary + 4 extension + 5 unresolved")


if __name__ == "__main__":
    main()
