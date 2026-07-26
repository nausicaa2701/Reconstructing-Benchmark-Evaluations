#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from aggregate_panel import aggregate_labels, gwet_ac1, nominal_alpha
from common import CRITERIA, canonicalize_evidence_refs, validate_decisions
from prepare_packets import build
from run_panel import ProviderHTTPError


class PanelTests(unittest.TestCase):
    def test_conservative_three_way_tie(self):
        label, rule = aggregate_labels([
            "documented-and-verifiable",
            "partially-documented",
            "not-documented",
        ])
        self.assertEqual(label, "partially-documented")
        self.assertEqual(rule, "conservative-three-way-tie")

    def test_exact_majority(self):
        label, rule = aggregate_labels([
            "not-documented", "not-documented", "partially-documented"
        ])
        self.assertEqual((label, rule), ("not-documented", "exact-majority"))

    def test_agreement_statistics(self):
        rows = [["not-documented"] * 3, ["partially-documented"] * 3]
        self.assertEqual(nominal_alpha(rows), 1.0)
        self.assertAlmostEqual(gwet_ac1(rows), 1.0)
        binary = [["pass", "pass", "fail"], ["fail", "fail", "fail"]]
        self.assertLess(gwet_ac1(binary, ["pass", "fail"]), 1.0)

    def test_http_retry_policy(self):
        self.assertFalse(ProviderHTTPError(400, "bad schema").retryable)
        self.assertFalse(ProviderHTTPError(429, "prepayment credits are depleted").retryable)
        self.assertTrue(ProviderHTTPError(429, "rate limit exceeded").retryable)
        self.assertTrue(ProviderHTTPError(503, "unavailable").retryable)

    def test_exact_path_reference_canonicalization(self):
        packet = {"sources": [{"source_id": "E001", "path": "README.md"}]}
        result = {"decisions": [{"evidence_refs": [{"source_id": "README.md"}]}]}
        changes = canonicalize_evidence_refs(result, packet)
        self.assertEqual(result["decisions"][0]["evidence_refs"][0]["source_id"], "E001")
        self.assertEqual(changes, [{"from": "README.md", "to": "E001"}])

    def test_packet_build_and_semantic_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            summary = build(target)
            self.assertEqual(summary["packets"], 26)
            import json
            packet = json.loads((target / "packets/B001.json").read_text())
            decisions = []
            for criterion in CRITERIA:
                decisions.append({
                    "criterion": criterion,
                    "label": "not-documented",
                    "evidence_refs": [{"source_id": "E001", "line_start": 1, "line_end": 1}],
                    "evidence_note": "The inspected source does not document this criterion.",
                    "confidence": "medium",
                })
            validate_decisions({"packet_id": "B001", "decisions": decisions}, packet)
            decisions[0]["evidence_refs"][0]["line_end"] = 10**9
            with self.assertRaises(ValueError):
                validate_decisions({"packet_id": "B001", "decisions": decisions}, packet)


if __name__ == "__main__":
    unittest.main()
