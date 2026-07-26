#!/usr/bin/env python3
"""Build the blinded adjudication packet for the third coder.

The adjudicator must not be either rater and must work before seeing model
labels. This script emits a form in which the two rater labels are presented in
a randomised left/right order under neutral headings, so the adjudicator cannot
tell which column is rater A, and so no positional habit can develop across the
63 items.

Output: adjudication_form.csv  (one row per disagreement, blank decision column)
        adjudication_key.json  (which side was which; sealed until ingest)
"""
import csv
import hashlib
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 20260727


def main():
    rows = list(csv.DictReader(open(HERE / "human_disagreements_for_adjudication.csv")))
    rng = random.Random(SEED)
    form, key = [], {}
    for i, row in enumerate(rows, start=1):
        item = f"ADJ-{i:03d}"
        flip = rng.random() < 0.5
        left, right = ("B", "A") if flip else ("A", "B")
        key[item] = {"option_1_is_rater": left, "option_2_is_rater": right,
                     "benchmark": row["benchmark"], "criterion": row["criterion"]}
        form.append({
            "item_id": item,
            "benchmark": row["benchmark"],
            "criterion": row["criterion"],
            "frozen_commit": row["frozen_commit"],
            "evidence_bundle": row[f"evidence_bundle_{left}"],
            "option_1_label": row[f"label_{left}"],
            "option_1_pointer": row[f"evidence_pointer_{left}"],
            "option_1_note": row[f"evidence_note_{left}"],
            "option_2_label": row[f"label_{right}"],
            "option_2_pointer": row[f"evidence_pointer_{right}"],
            "option_2_note": row[f"evidence_note_{right}"],
            # to be filled by the adjudicator:
            "adjudicated_label": "",
            "adjudication_pointer": "",
            "adjudication_note": "",
        })

    out = HERE / "adjudication_form.csv"
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(form[0]))
        writer.writeheader()
        writer.writerows(form)
    (HERE / "adjudication_key.json").write_text(json.dumps(key, indent=1) + "\n")

    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"{out.name}: {len(form)} items, sha256 {digest}")
    print("Adjudicator rules:")
    print("  - must not be rater A or rater B")
    print("  - may choose either option's label, or a third label the evidence supports")
    print("  - must supply a pointer for every decision, including not-documented")
    print("  - must not open packet_key.json or artifact/audit/ before submitting")


if __name__ == "__main__":
    main()
