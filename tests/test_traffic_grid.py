import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "traffic-grid"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("env", "policies", "run", "feedback_loop"):
    sys.modules.pop(module_name, None)

from env import TrafficState, TrafficWorld, default_scenario
from feedback_loop import build_feedback_report
from policies import baseline_policy, heuristic_policy
from run import run_episode


class TrafficGridPolicyTests(unittest.TestCase):
    def test_baseline_causes_downstream_spillback(self):
        result = run_episode(TrafficWorld(), baseline_policy, default_scenario())
        self.assertEqual(result["reason"], "spillback")
        self.assertLess(result["reward"], 0)

    def test_heuristic_reaches_stable_flow(self):
        result = run_episode(TrafficWorld(), heuristic_policy, default_scenario())
        self.assertEqual(result["reason"], "stable_flow")
        self.assertGreater(result["reward"], 0)

    def test_heuristic_protects_downstream_capacity(self):
        world = TrafficWorld()
        state = TrafficState(step=0, main_queue=6, side_queue=3, downstream_queue=7)
        self.assertEqual(baseline_policy(world, state), "release_main")
        self.assertEqual(heuristic_policy(world, state), "hold")

    def test_feedback_report_targets_traffic_policy(self):
        report = build_feedback_report()
        self.assertEqual(report["case"], "traffic_grid_downstream_spillback")
        self.assertEqual(report["candidate_update"]["target"], "examples/traffic-grid/policies.py")
        self.assertEqual(report["policies"][0]["reason"], "spillback")
        self.assertEqual(report["policies"][1]["reason"], "stable_flow")


if __name__ == "__main__":
    unittest.main()
