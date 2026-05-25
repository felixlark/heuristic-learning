from __future__ import annotations

import argparse
import json
from pathlib import Path

from env import SoccerWorld, default_scenario
from policies import baseline_policy, heuristic_policy
from run import run_episode


def summarize(name: str) -> dict[str, object]:
    world = SoccerWorld()
    policy = baseline_policy if name == "baseline" else heuristic_policy
    result = run_episode(world, policy, default_scenario())
    return {
        "policy": name,
        "reason": result["reason"],
        "reward": result["reward"],
        "steps": result["steps"],
        "trace": [
            {
                "robot": state.robot,
                "ball": state.ball,
                "opponent": state.opponent,
                "has_ball": state.has_ball,
            }
            for state in result["trace"]
        ],
    }


def build_feedback_report() -> dict[str, object]:
    scenario = default_scenario()
    return {
        "case": "robot_soccer_blocked_lane",
        "environment": {
            "width": SoccerWorld().width,
            "height": SoccerWorld().height,
            "start": {
                "robot": scenario.robot,
                "ball": scenario.ball,
                "opponent": scenario.opponent,
                "goal_x": scenario.goal_x,
                "has_ball": scenario.has_ball,
            },
        },
        "policies": [summarize("baseline"), summarize("heuristic")],
        "feedback": [
            "The baseline shoots as soon as it owns the ball and the goal is nearby.",
            "The blocked-lane failure is isolated by placing the opponent on the direct shot lane.",
            "The heuristic policy must reposition before shooting when the lane is blocked.",
        ],
        "candidate_update": {
            "target": "examples/robot-soccer/policies.py",
            "rule": "Check the shot lane before shooting; preserve the blocked-lane regression test.",
            "verification": "python3 -m unittest discover -s tests",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = build_feedback_report()
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
