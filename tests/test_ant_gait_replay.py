import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "ant-gait-replay"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("replay_env", "policies", "run", "feedback_loop"):
    sys.modules.pop(module_name, None)

from feedback_loop import build_feedback_report
from policies import baseline_policy, heuristic_policy
from replay_env import AntGaitReplayWorld
from run import run_episode


class AntGaitReplayPolicyTests(unittest.TestCase):
    def test_baseline_drifts_under_yaw_perturbation(self):
        result = run_episode(AntGaitReplayWorld(), baseline_policy)
        self.assertEqual(result["reason"], "yaw_drift")
        self.assertLess(result["reward"], 0)

    def test_heuristic_stabilizes_stride(self):
        result = run_episode(AntGaitReplayWorld(), heuristic_policy)
        self.assertEqual(result["reason"], "stable_stride")
        self.assertGreater(result["reward"], 0)

    def test_heuristic_uses_yaw_feedback_and_adaptive_duty(self):
        state = AntGaitReplayWorld().initial_state()
        baseline = baseline_policy(state)
        heuristic = heuristic_policy(state)
        self.assertEqual(baseline.yaw_feedback, 0.0)
        self.assertGreater(heuristic.yaw_feedback, 0.0)
        self.assertGreater(heuristic.stance_duty, baseline.stance_duty)

    def test_feedback_report_targets_ant_policy(self):
        report = build_feedback_report()
        self.assertEqual(report["case"], "ant_gait_yaw_stabilization")
        self.assertEqual(report["candidate_update"]["target"], "examples/ant-gait-replay/policies.py")
        self.assertEqual(report["policies"][0]["reason"], "yaw_drift")
        self.assertEqual(report["policies"][1]["reason"], "stable_stride")


if __name__ == "__main__":
    unittest.main()
