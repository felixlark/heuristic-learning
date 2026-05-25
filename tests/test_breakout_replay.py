import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "breakout-replay"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("replay_env", "policies", "run", "feedback_loop"):
    sys.modules.pop(module_name, None)

from feedback_loop import build_feedback_report
from policies import baseline_policy, heuristic_policy
from replay_env import BreakoutReplayWorld
from run import run_episode


class BreakoutReplayPolicyTests(unittest.TestCase):
    def test_baseline_misses_after_wall_reflection(self):
        result = run_episode(BreakoutReplayWorld(), baseline_policy)
        self.assertEqual(result["reason"], "missed_after_wall_reflection")
        self.assertLess(result["reward"], 0)

    def test_heuristic_intercepts_after_wall_reflection(self):
        result = run_episode(BreakoutReplayWorld(), heuristic_policy)
        self.assertEqual(result["reason"], "intercepted")
        self.assertGreater(result["reward"], 0)

    def test_heuristic_moves_toward_reflected_intercept(self):
        world = BreakoutReplayWorld()
        frame = world.initial_frame()
        self.assertLess(world.intercept_x(frame), frame.ball_x)
        self.assertEqual(baseline_policy(world, frame), "right")
        self.assertEqual(heuristic_policy(world, frame), "left")

    def test_feedback_report_targets_breakout_policy(self):
        report = build_feedback_report()
        self.assertEqual(report["case"], "breakout_wall_reflection_intercept")
        self.assertEqual(report["candidate_update"]["target"], "examples/breakout-replay/policies.py")
        self.assertEqual(report["policies"][0]["reason"], "missed_after_wall_reflection")
        self.assertEqual(report["policies"][1]["reason"], "intercepted")


if __name__ == "__main__":
    unittest.main()
