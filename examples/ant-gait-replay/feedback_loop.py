from __future__ import annotations

import argparse
import json
from pathlib import Path

from policies import baseline_policy, heuristic_policy
from replay_env import AntGaitReplayWorld, GaitCommand
from run import run_episode


def summarize_command(command: GaitCommand) -> dict[str, float]:
    return {
        "phase_increment": round(command.phase_increment, 4),
        "stance_duty": round(command.stance_duty, 4),
        "yaw_feedback": round(command.yaw_feedback, 4),
        "drive": round(command.drive, 4),
    }


def summarize(name: str) -> dict[str, object]:
    world = AntGaitReplayWorld()
    policy = baseline_policy if name == "baseline" else heuristic_policy
    result = run_episode(world, policy)
    return {
        "policy": name,
        "reason": result["reason"],
        "reward": result["reward"],
        "steps": result["steps"],
        "first_commands": [summarize_command(command) for command in result["commands"][:4]],
        "final_state": result["trace"][-1].__dict__,
    }


def build_feedback_report() -> dict[str, object]:
    world = AntGaitReplayWorld()
    return {
        "case": "ant_gait_yaw_stabilization",
        "source": {
            "repo": "Trinkle23897/learning-beyond-gradients",
            "artifact": "mujoco/ant/heuristic_ant.py",
            "note": "The course replay keeps the CPG, speed adaptation, stance duty and yaw feedback ideas without requiring MuJoCo.",
        },
        "environment": {
            "target_speed": world.target_speed,
            "yaw_limit": world.yaw_limit,
            "initial_yaw_rate": world.initial_yaw_rate,
            "max_steps": world.max_steps,
        },
        "policies": [summarize("baseline"), summarize("heuristic")],
        "feedback": [
            "The baseline fixed rhythm cannot absorb a persistent yaw perturbation.",
            "The heuristic policy adapts cadence and stance duty while feeding yaw/yaw-rate back into the gait.",
            "The maintainable update target is the gait controller, not a black-box reward optimizer.",
        ],
        "candidate_update": {
            "target": "examples/ant-gait-replay/policies.py",
            "rule": "Keep yaw feedback and speed-adaptive stance duty coupled when tuning gait parameters.",
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
