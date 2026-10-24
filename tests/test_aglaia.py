import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location("aglaia", Path(__file__).parents[1] / "scripts" / "aglaia.py")
aglaia = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aglaia)


class GovernanceTests(unittest.TestCase):
    def test_run_id_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            aglaia.safe_id("../outside")

    def test_append_only_events_are_valid_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(aglaia, "GOV", Path(tmp)):
            path = aglaia.append_event("run-001", "session.start", objective="demo")
            aglaia.append_event("run-001", "session.note", fact="ok")
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual([r["event"] for r in rows], ["session.start", "session.note"])

    def test_claim_refuses_existing_live_claim(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(aglaia, "CLAIMS", Path(tmp)):
            args = type("Args", (), {"resource": "asset-x", "owner": "test", "ttl": 90})()
            aglaia.claim(args)
            with self.assertRaisesRegex(ValueError, "held"):
                aglaia.claim(args)

    def test_close_records_digest_of_prior_history(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(aglaia, "GOV", Path(tmp)):
            path = aglaia.append_event("run-002", "session.start", objective="demo")
            digest = __import__("hashlib").sha256(path.read_bytes()).hexdigest()
            args = type("Args", (), {"run_id": "run-002", "status": "CLOSED", "summary": "done", "evidence": "test"})()
            aglaia.close(args)
            records = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(records[-1]["prior_events_sha256"], digest)

    def test_closed_session_rejects_late_event(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(aglaia, "GOV", Path(tmp)):
            aglaia.append_event("run-003", "session.start", objective="demo")
            args = type("Args", (), {"run_id": "run-003", "status": "CLOSED", "summary": "done", "evidence": "test"})()
            aglaia.close(args)
            with self.assertRaisesRegex(ValueError, "closed"):
                aglaia.append_event("run-003", "session.note", fact="late")


if __name__ == "__main__":
    unittest.main()
