#!/usr/bin/env python3
"""Validate the authoritative L1/L2/L3 table against frozen execution outcomes."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "artifact"
LEVELS = ARTIFACT / "execution" / "fixtures" / "evaluation_levels.csv"
E3 = ARTIFACT / "audit" / "e3" / "e3_outcomes.csv"
OFFICIAL = ARTIFACT / "environment" / "official_environment_results.csv"
STATUS = ARTIFACT / "execution" / "fixtures" / "golden_fixture_status.json"

BINARY_FIELDS = [
    "portable_first_pass",
    "portable_after_repair",
    "portable_any",
    "official_tested",
    "official_pass",
    "L1_any_environment",
    "L2_fixture_matched",
    "L3_published_score_reproduced",
]


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_bool(row, field):
    value = row[field]
    assert value in {"0", "1"}, f"{row['benchmark']}: {field}={value!r} is not binary"
    return value == "1"


def main():
    rows = read_csv(LEVELS)
    assert len(rows) == 26, f"expected 26 releases, found {len(rows)}"
    assert len({row["benchmark"] for row in rows}) == 26, "duplicate benchmark in level table"

    by_name = {row["benchmark"]: row for row in rows}
    for row in rows:
        for field in BINARY_FIELDS:
            as_bool(row, field)
        portable = as_bool(row, "portable_first_pass") or as_bool(row, "portable_after_repair")
        assert as_bool(row, "portable_any") == portable, f"{row['benchmark']}: portable OR mismatch"
        l1 = portable or as_bool(row, "official_pass")
        assert as_bool(row, "L1_any_environment") == l1, f"{row['benchmark']}: L1 union mismatch"
        assert not as_bool(row, "official_pass") or as_bool(row, "official_tested"), (
            f"{row['benchmark']}: official pass without test"
        )
        assert not as_bool(row, "L2_fixture_matched") or l1, f"{row['benchmark']}: L2 without L1"
        assert not as_bool(row, "L3_published_score_reproduced") or as_bool(
            row, "L2_fixture_matched"
        ), f"{row['benchmark']}: L3 must imply L2"
        expected_highest = (
            "L3"
            if as_bool(row, "L3_published_score_reproduced")
            else "L2"
            if as_bool(row, "L2_fixture_matched")
            else "L1"
            if l1
            else "none"
        )
        assert row["highest_level"] == expected_highest, (
            f"{row['benchmark']}: expected highest_level={expected_highest}"
        )
        evidence = ROOT / row["evidence"]
        assert evidence.exists(), f"{row['benchmark']}: missing evidence {row['evidence']}"

    frozen = {row["benchmark"]: row for row in read_csv(E3)}
    assert set(frozen) == set(by_name), "level table and frozen E3 cohort differ"
    for name, row in by_name.items():
        source = frozen[name]
        assert as_bool(row, "portable_first_pass") == (source["E3_first_pass"] == "True"), (
            f"{name}: portable first-pass mismatch"
        )
        assert as_bool(row, "portable_after_repair") == (source["E3_after_repair"] == "True"), (
            f"{name}: portable repair mismatch"
        )
        assert as_bool(row, "portable_any") == (source["E3_smoke_testable"] == "True"), (
            f"{name}: portable-any mismatch"
        )

    official = {row["benchmark"]: row for row in read_csv(OFFICIAL)}
    assert len(official) == 7, f"expected 7 official-environment tests, found {len(official)}"
    for name, row in by_name.items():
        tested = name in official
        passed = tested and official[name]["official_pass"] == "1"
        assert as_bool(row, "official_tested") == tested, f"{name}: official-tested mismatch"
        assert as_bool(row, "official_pass") == passed, f"{name}: official-pass mismatch"

    counts = {
        "portable_L1": sum(as_bool(row, "portable_any") for row in rows),
        "portable_L2": sum(
            as_bool(row, "portable_any") and as_bool(row, "L2_fixture_matched")
            for row in rows
        ),
        "portable_L3": sum(
            as_bool(row, "portable_any") and as_bool(row, "L3_published_score_reproduced")
            for row in rows
        ),
        "official_tested": sum(as_bool(row, "official_tested") for row in rows),
        "official_pass": sum(as_bool(row, "official_pass") for row in rows),
        "L1_any_environment": sum(as_bool(row, "L1_any_environment") for row in rows),
        "L2_fixture_matched": sum(as_bool(row, "L2_fixture_matched") for row in rows),
        "L3_published_score_reproduced": sum(
            as_bool(row, "L3_published_score_reproduced") for row in rows
        ),
    }
    expected = {
        "portable_L1": 7,
        "portable_L2": 4,
        "portable_L3": 1,
        "official_tested": 7,
        "official_pass": 4,
        "L1_any_environment": 10,
        "L2_fixture_matched": 5,
        "L3_published_score_reproduced": 1,
    }
    assert counts == expected, f"level counts changed: {counts}"

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["L1_invoked"] == counts["L1_any_environment"]
    assert status["L2_fixture_matched"] == counts["L2_fixture_matched"]
    assert status["L3_published_score_reproduced"] == counts["L3_published_score_reproduced"]

    print(
        "[evaluation-levels] OK: portable L1/L2/L3=7/4/1; official tested=7/26, pass=4/7; "
        "any-environment L1=10/26; cumulative L2=5/10; cumulative L3=1/10"
    )


if __name__ == "__main__":
    main()
