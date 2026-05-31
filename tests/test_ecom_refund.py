from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pvcore import Goal, ObstructionReport, Commit, run_pvcore  # noqa: E402


class EcomRefundTests(unittest.TestCase):
    def load_task(self, name: str):
        return json.loads((ROOT / f"examples/ecom/{name}").read_text(encoding="utf-8"))

    def test_refund_commit_when_obligations_pass(self) -> None:
        task = self.load_task("refund-task.json")
        result = run_pvcore(Goal.from_dict(task["goal"]), task["witnesses"])
        self.assertIsInstance(result, Commit)
        data = result.to_dict()
        self.assertEqual(data["status"], "verified")
        self.assertTrue(data["trusted_state"]["trusted"])
        self.assertEqual({v["result"] for v in data["verifications"]}, {"accepted"})

    def test_duplicate_refund_obstructs(self) -> None:
        task = self.load_task("refund-task-duplicate.json")
        result = run_pvcore(Goal.from_dict(task["goal"]), task["witnesses"])
        self.assertIsInstance(result, ObstructionReport)
        data = result.to_dict()
        self.assertEqual(data["status"], "obstructed")
        self.assertIn("O-NO-DUPLICATE-REFUND", data["obstruction"]["failed_obligations"])


if __name__ == "__main__":
    unittest.main()
