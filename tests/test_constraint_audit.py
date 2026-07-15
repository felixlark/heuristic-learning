import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "constraint-audit"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("env", "policies", "run", "feedback_loop"):
    sys.modules.pop(module_name, None)

from env import Claim, default_world
from feedback_loop import build_feedback_report
from policies import baseline_policy, constraint_audit_policy
from run import run_audit


class ConstraintAuditTests(unittest.TestCase):
    def test_baseline_accepts_known_constraint_violation(self):
        result = run_audit(default_world(), baseline_policy)
        self.assertEqual(result["reason"], "accepted_constraint_violation")
        self.assertLess(result["reward"], 0)

    def test_audit_blocks_known_constraint_violation(self):
        result = run_audit(default_world(), constraint_audit_policy)
        self.assertEqual(result["reason"], "blocked_constraint_violation")
        self.assertGreater(result["reward"], 0)

    def test_unknown_claim_requires_external_evidence(self):
        world = default_world()
        claim = Claim("unlisted_object", "launch_year", "2027")
        self.assertEqual(constraint_audit_policy(world, claim), "request_external_evidence")

    def test_feedback_report_keeps_research_boundary(self):
        report = build_feedback_report()
        self.assertEqual(report["candidate_update"]["target"], "examples/constraint-audit/policies.py")
        self.assertEqual(report["policies"][0]["reason"], "accepted_constraint_violation")
        self.assertEqual(report["policies"][1]["reason"], "blocked_constraint_violation")
        self.assertIn("not a general hallucination detector", report["source"]["note"])


if __name__ == "__main__":
    unittest.main()
