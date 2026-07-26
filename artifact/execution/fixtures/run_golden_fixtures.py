#!/usr/bin/env python3
"""Run L2 golden fixtures: official scorer vs. an independently derived expected value.

Each fixture pairs an input with an expected output computed WITHOUT executing the
scorer under test -- by reimplementing the release's own documented metric in a few
lines. A fixture passes at L2 when the official scorer's emitted value matches the
independently derived value within the stated tolerance.

Usage:
    python run_golden_fixtures.py --releases-root /path/containing/clones

The clones must sit at the frozen commits recorded in fixture_spec.json:
    dsbench  -> ba786096137a5108af11c016ad3f09cdb97beefd
    qrdata   -> de450af45ff7101b328bb064c6b475f73414a7ed
"""
import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs"


def sh(cmd, cwd):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
    return proc.returncode, proc.stdout, proc.stderr


def expected_rmsle(answer_csv, predict_csv, column="Rings"):
    """Independent reimplementation of the documented metric (RMSLE)."""
    import csv

    def col(path):
        with open(path) as f:
            return [float(row[column]) for row in csv.DictReader(f)]

    a, p = col(answer_csv), col(predict_csv)
    return math.sqrt(sum((math.log1p(x) - math.log1p(y)) ** 2 for x, y in zip(a, p)) / len(a))


def run_dsbench(root):
    """playground-series-s4e4_eval.py writes the score to <path>/<name>/result.txt."""
    scorer = root / "data_modeling" / "evaluation" / "playground-series-s4e4_eval.py"
    results = []
    for predict_name, label in (("predict.csv", "perturbed"),
                                ("predict_identical.csv", "identical")):
        answer = INPUTS / "dsbench" / "answer.csv"
        predict = INPUTS / "dsbench" / predict_name
        expected = expected_rmsle(answer, predict)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "fixture"
            out.mkdir()
            code, stdout, stderr = sh([
                sys.executable, str(scorer),
                "--path", tmp, "--name", "fixture",
                "--answer_file", str(answer), "--predict_file", str(predict),
                "--value", "Rings",
            ], cwd=root)
            emitted_path = out / "result.txt"
            emitted = float(emitted_path.read_text().strip()) if emitted_path.exists() else None
        results.append({
            "release": "DSBench",
            "fixture": f"playground-series-s4e4 RMSLE ({label} predictions)",
            "exit_code": code,
            "stdout_bytes": len(stdout),
            "emitted": emitted,
            "expected": expected,
            "tolerance": 1e-6,
            "L2_match": emitted is not None and abs(emitted - expected) <= 1e-6,
            "derivation": "RMSLE = sqrt(mean((log1p(answer)-log1p(prediction))^2)), "
                          "reimplemented from the release's documented metric without "
                          "invoking the scorer.",
            "stderr_tail": stderr.strip()[-300:],
        })
    return results


def run_qrdata(root):
    """eval.py reads ./tmp.json and prints accuracy to stdout."""
    scorer = root / "benchmark" / "eval.py"
    fixture = INPUTS / "qrdata" / "tmp.json"
    items = json.loads(fixture.read_text())
    # Independent derivation: each item's correctness follows from the documented
    # error_scale=0.03 rule and is recorded in its _why field.
    expected = sum(1 for i in items
                   if "incorrect" not in i["_why"] and "correct" in i["_why"]) / len(items)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copy(scorer, work / "eval.py")
        shutil.copy(fixture, work / "tmp.json")
        code, stdout, stderr = sh([sys.executable, "eval.py"], cwd=work)
    try:
        emitted = float(stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        emitted = None
    return [{
        "release": "QRData",
        "fixture": "six-item accuracy covering the tolerance boundary, percentage "
                   "gold, multiple-choice prefix match, and the unparseable-prediction "
                   "exception path",
        "exit_code": code,
        "stdout_bytes": len(stdout),
        "emitted": emitted,
        "expected": expected,
        "tolerance": 1e-9,
        "L2_match": emitted is not None and abs(emitted - expected) <= 1e-9,
        "derivation": "Item-level correctness follows by hand from the documented "
                      "error_scale=0.03 band and the prefix rule for multiple choice; "
                      "accuracy is the mean of those six hand-assigned outcomes.",
        "stderr_tail": stderr.strip()[-300:],
    }]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--releases-root", required=True, type=Path,
                    help="directory holding dsbench/ and qrdata/ clones at frozen commits")
    ap.add_argument("--out", type=Path, default=HERE / "golden_fixture_results.json")
    args = ap.parse_args()

    results = []
    results += run_dsbench(args.releases_root / "dsbench")
    results += run_qrdata(args.releases_root / "qrdata")

    summary = {
        "fixtures": results,
        "n_fixtures": len(results),
        "n_L2_match": sum(1 for r in results if r["L2_match"]),
        "releases_reaching_L2": sorted({r["release"] for r in results if r["L2_match"]}),
    }
    args.out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
