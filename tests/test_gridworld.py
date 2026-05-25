import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "heuristic-gridworld"
sys.path.insert(0, str(EXAMPLE_DIR))
for module_name in ("env", "policies", "run", "feedback_loop"):
    sys.modules.pop(module_name, None)

from env import GridWorld
from feedback_loop import build_feedback_report
from policies import baseline_policy, heuristic_policy
from run import run_episode


class GridWorldPolicyTests(unittest.TestCase):
    def test_heuristic_reaches_goal(self):
        result = run_episode(GridWorld(), heuristic_policy)
        self.assertEqual(result["reason"], "goal")
        self.assertGreater(result["reward"], 0)

    def test_heuristic_avoids_known_traps(self):
        result = run_episode(GridWorld(), heuristic_policy)
        traps = GridWorld().traps
        self.assertTrue(traps.isdisjoint(result["path"]))

    def test_heuristic_avoids_local_greedy_trap(self):
        env = GridWorld(start=(1, 1), goal=(3, 1), traps=frozenset({(2, 1)}))
        baseline_action = baseline_policy(env, env.start, [env.start])
        heuristic_action = heuristic_policy(env, env.start, [env.start])

        self.assertEqual(baseline_action, "right")
        self.assertNotEqual(heuristic_action, "right")
        self.assertNotIn(env.next_position(env.start, heuristic_action), env.traps)

    def test_feedback_report_names_update_target_and_verifier(self):
        report = build_feedback_report(episodes=3)
        self.assertEqual(report["candidate_update"]["target"], "examples/heuristic-gridworld/policies.py")
        self.assertEqual(report["candidate_update"]["verification"], "python3 -m unittest discover -s tests")
        self.assertEqual(len(report["policies"]), 2)
        self.assertEqual(report["probes"][0]["baseline_action"], "right")
        self.assertNotEqual(report["probes"][0]["heuristic_action"], "right")
        self.assertIn("feedback", report)


if __name__ == "__main__":
    unittest.main()
