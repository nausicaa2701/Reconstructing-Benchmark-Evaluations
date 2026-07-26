#!/usr/bin/env python3
"""Merge completed Markdown rater forms back into the assignment CSVs.

Parses rater_form_{A,B}.md, validates every label against the codebook, refuses
partial or malformed submissions, and writes the labels into
assignments/coder_{A,B}.csv so analyze_labels.py can consume them unchanged.
A completed form is never overwritten by build_rater_forms.py.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VALID = {
    "documented-and-verifiable", "partially-documented",
    "claimed-but-not-verifiable", "not-documented", "not-applicable",
    "access-blocked",
}
ITEM = re.compile(
    r"^## (?P<id>H[AB]-\d{3}) — .*?$\n"
    r".*?^- \*\*Label:\*\*(?P<label>.*?)$\n"
    r"^- \*\*Evidence pointer:\*\*(?P<pointer>.*?)$\n"
    r"^- \*\*Note:\*\*(?P<note>.*?)$",
    re.MULTILINE | re.DOTALL,
)


def parse(coder: str) -> dict[str, dict[str, str]]:
    path = HERE / f"rater_form_{coder}.md"
    if not path.exists():
        raise SystemExit(f"missing {path.name}")
    text = path.read_text(encoding="utf-8")
    parsed, problems = {}, []
    for match in ITEM.finditer(text):
        label = match.group("label").strip().strip("`")
        pointer = match.group("pointer").strip()
        note = " ".join(match.group("note").split())
        item = match.group("id")
        if not label:
            problems.append(f"{item}: blank label")
        elif label not in VALID:
            problems.append(f"{item}: invalid label {label!r}")
        if not pointer:
            problems.append(f"{item}: missing evidence pointer")
        parsed[item] = {"label": label, "evidence_pointer": pointer,
                        "evidence_note": note}
    if problems:
        raise SystemExit(f"rater {coder}: {len(problems)} problem(s)\n  " +
                         "\n  ".join(problems[:25]))
    return parsed


def main() -> None:
    frozen = {}
    for coder in ("A", "B"):
        parsed = parse(coder)
        path = HERE / "assignments" / f"coder_{coder}.csv"
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
        missing = {row["assignment_id"] for row in rows} - set(parsed)
        extra = set(parsed) - {row["assignment_id"] for row in rows}
        if missing or extra:
            raise SystemExit(
                f"rater {coder}: {len(missing)} unanswered, {len(extra)} unknown items")
        for row in rows:
            row.update(parsed[row["assignment_id"]])
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        frozen[coder] = {
            "n_items": len(rows),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "label_counts": {label: sum(1 for row in rows if row["label"] == label)
                             for label in sorted(VALID)},
        }
    (HERE / "frozen_submissions.json").write_text(
        json.dumps(frozen, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(frozen, indent=2))
    print("\nboth forms frozen; adjudication may now consult the other rater, "
          "and packet_key.json may be unsealed")


if __name__ == "__main__":
    main()
