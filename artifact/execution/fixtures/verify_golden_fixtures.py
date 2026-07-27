#!/usr/bin/env python3
"""Report the golden-fixture level reached by every reachable evaluator.

Levels are defined in fixture_spec.json.  This script does not execute the
benchmark scorers: it validates the fixture records, checks that each fixture
either carries an independently derived expected value or is explicitly
recorded as L1-only, and emits the three-level summary used in the paper.
Running the scorers requires re-cloning each release at its frozen commit and
is driven by artifact/execution/README.md.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEVELS = ["L1_invoked", "L2_fixture_matched", "L3_published_score_reproduced"]


def main() -> None:
    spec = json.loads((HERE / "fixture_spec.json").read_text(encoding="utf-8"))
    fixtures = spec["fixtures"]
    counts = {"L1": 0, "L2": 0, "L3": 0}
    rows = []
    for fixture in fixtures:
        status = fixture["status"]
        if status not in {"L1-only", "L2-retrospective", "L2", "L3"}:
            raise SystemExit(f"{fixture['benchmark']}: unknown status {status}")
        has_expected = fixture.get("expected") not in (None, {}) and any(
            value is not None for value in
            (fixture["expected"].values() if isinstance(fixture["expected"], dict)
             else [fixture["expected"]]))
        if status.startswith("L2") and not has_expected:
            raise SystemExit(f"{fixture['benchmark']}: L2 claimed without an expected value")
        if status == "L1-only" and has_expected:
            raise SystemExit(
                f"{fixture['benchmark']}: expected value present but level not raised")
        counts["L1"] += 1
        if status.startswith("L2"):
            counts["L2"] += 1
        if status == "L3":
            counts["L2"] += 1
            counts["L3"] += 1
        rows.append({"benchmark": fixture["benchmark"], "status": status,
                     "retrospective": status.endswith("retrospective")})

    summary = {
        "spec_version": spec["spec_version"],
        "n_reachable_evaluators_with_a_pass": len(fixtures),
        "portable_releases_with_a_pass": 0,
        "official_environment_releases_tested": 0,
        "official_environment_releases_with_a_pass": 0,
        "L1_invoked": counts["L1"],
        "L2_fixture_matched": counts["L2"],
        "L3_published_score_reproduced": counts["L3"],
        "levels_are_cumulative": True,
        "highest_level_counts": {
            "L1": sum(row["status"] == "L1-only" for row in rows),
            "L2": sum(row["status"].startswith("L2") for row in rows),
            "L3": sum(row["status"] == "L3" for row in rows),
        },
        "all_L2_are_retrospective": all(
            row["retrospective"] for row in rows if row["status"].startswith("L2")),
        "per_release": rows,
    }
    with (HERE / "evaluation_levels.csv").open(newline="", encoding="utf-8") as handle:
        level_rows = list(csv.DictReader(handle))
    summary["portable_releases_with_a_pass"] = sum(
        row["portable_any"] == "1" for row in level_rows
    )
    summary["official_environment_releases_tested"] = sum(
        row["official_tested"] == "1" for row in level_rows
    )
    summary["official_environment_releases_with_a_pass"] = sum(
        row["official_pass"] == "1" for row in level_rows
    )
    for row in summary["per_release"]:
        if row["status"] == "L3":
            row["also_counts_toward_cumulative_L2"] = True
    (HERE / "golden_fixture_status.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
