import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "vizdoom-replay"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("replay_env", "vizdoom_policies", "run", "feedback_loop"):
    sys.modules.pop(module_name, None)

from feedback_loop import build_feedback_report
from replay_env import ReplayWorld
from run import run_episode
from vizdoom_policies import baseline_policy, heuristic_policy


class VizDoomReplayPolicyTests(unittest.TestCase):
    def test_baseline_wastes_medikit(self):
        result = run_episode(ReplayWorld(), baseline_policy)
        self.assertEqual(result["reason"], "wasted_pickup")
        self.assertLess(result["reward"], 0)

    def test_heuristic_waits_then_uses_medikit(self):
        result = run_episode(ReplayWorld(), heuristic_policy)
        self.assertEqual(result["reason"], "valued_pickup")
        self.assertGreater(result["reward"], 0)

    def test_heuristic_first_action_is_staging_wait(self):
        world = ReplayWorld()
        frame = world.initial_frame()
        self.assertEqual(baseline_policy(world, frame), "forward")
        self.assertEqual(heuristic_policy(world, frame), "wait")

    def test_feedback_report_links_source_and_update_target(self):
        report = build_feedback_report()
        self.assertEqual(report["case"], "vizdoom_d1_medikit_staging")
        self.assertEqual(report["policies"][0]["reason"], "wasted_pickup")
        self.assertEqual(report["policies"][1]["reason"], "valued_pickup")
        self.assertEqual(report["candidate_update"]["target"], "examples/vizdoom-replay/vizdoom_policies.py")


if __name__ == "__main__":
    unittest.main()
