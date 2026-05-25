import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "robot-soccer"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("env", "policies", "run", "feedback_loop"):
    sys.modules.pop(module_name, None)

from env import SoccerState, SoccerWorld, default_scenario
from feedback_loop import build_feedback_report
from policies import baseline_policy, heuristic_policy
from run import run_episode


class RobotSoccerPolicyTests(unittest.TestCase):
    def test_baseline_shot_gets_blocked(self):
        result = run_episode(SoccerWorld(), baseline_policy, default_scenario())
        self.assertEqual(result["reason"], "blocked_shot")

    def test_heuristic_repositions_and_scores(self):
        result = run_episode(SoccerWorld(), heuristic_policy, default_scenario())
        self.assertEqual(result["reason"], "goal")
        self.assertGreater(result["reward"], 0)

    def test_heuristic_blocks_direct_shot_when_lane_blocked(self):
        world = SoccerWorld()
        state = SoccerState(robot=(2, 2), ball=(2, 2), opponent=(4, 2), goal_x=6, has_ball=True)
        self.assertEqual(baseline_policy(world, state), "shoot")
        self.assertEqual(heuristic_policy(world, state), "reposition")

    def test_feedback_report_targets_robot_soccer_policy(self):
        report = build_feedback_report()
        self.assertEqual(report["candidate_update"]["target"], "examples/robot-soccer/policies.py")
        self.assertEqual(report["policies"][0]["reason"], "blocked_shot")
        self.assertEqual(report["policies"][1]["reason"], "goal")


if __name__ == "__main__":
    unittest.main()
