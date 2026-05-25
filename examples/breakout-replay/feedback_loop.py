from __future__ import annotations

import argparse
import json
from pathlib import Path

from policies import baseline_policy, heuristic_policy
from replay_env import BreakoutReplayWorld
from run import run_episode


def summarize(name: str) -> dict[str, object]:
    world = BreakoutReplayWorld()
    policy = baseline_policy if name == "baseline" else heuristic_policy
    result = run_episode(world, policy)
    return {
        "policy": name,
        "reason": result["reason"],
        "reward": result["reward"],
        "steps": result["steps"],
        "actions": result["actions"],
        "trace": [
            {
                "step": frame.step,
                "ball_x": frame.ball_x,
                "ball_y": frame.ball_y,
                "velocity_x": frame.velocity_x,
                "velocity_y": frame.velocity_y,
                "paddle_x": frame.paddle_x,
            }
            for frame in result["trace"]
        ],
    }


def build_feedback_report() -> dict[str, object]:
    world = BreakoutReplayWorld()
    start = world.initial_frame()
    return {
        "case": "breakout_wall_reflection_intercept",
        "source": {
            "repo": "Trinkle23897/learning-beyond-gradients",
            "artifact": "atari/breakout/heuristic_breakout.py",
            "note": "The course replay keeps the velocity + side-wall reflection idea and removes Atari/NumPy dependencies.",
        },
        "environment": {
            "field_left": world.field_left,
            "field_right": world.field_right,
            "paddle_y": world.paddle_y,
            "start": {
                "ball_x": start.ball_x,
                "ball_y": start.ball_y,
                "velocity_x": start.velocity_x,
                "velocity_y": start.velocity_y,
                "paddle_x": start.paddle_x,
                "intercept_x": round(world.intercept_x(start), 3),
            },
        },
        "policies": [summarize("baseline"), summarize("heuristic")],
        "feedback": [
            "The baseline chases the current ball x and misses after a side-wall reflection.",
            "The heuristic system estimates the landing point by reflecting the trajectory inside the field.",
            "The update target is the intercept predictor, not a neural-network weight.",
        ],
        "candidate_update": {
            "target": "examples/breakout-replay/policies.py",
            "rule": "Preserve side-wall reflection prediction before changing paddle control rules.",
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
