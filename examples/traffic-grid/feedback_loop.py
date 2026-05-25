from __future__ import annotations

import argparse
import json
from pathlib import Path

from env import TrafficWorld, default_scenario
from policies import baseline_policy, heuristic_policy
from run import run_episode


def summarize(name: str) -> dict[str, object]:
    world = TrafficWorld()
    policy = baseline_policy if name == "baseline" else heuristic_policy
    result = run_episode(world, policy, default_scenario())
    return {
        "policy": name,
        "reason": result["reason"],
        "reward": result["reward"],
        "steps": result["steps"],
        "actions": result["actions"],
        "trace": [
            {
                "step": state.step,
                "main_queue": state.main_queue,
                "side_queue": state.side_queue,
                "downstream_queue": state.downstream_queue,
            }
            for state in result["trace"]
        ],
    }


def build_feedback_report() -> dict[str, object]:
    scenario = default_scenario()
    world = TrafficWorld()
    return {
        "case": "traffic_grid_downstream_spillback",
        "source": {
            "kind": "feishu_task_signal",
            "note": "Derived from an internal task direction about applying Heuristic Learning to an East Lake traffic simulator.",
        },
        "environment": {
            "downstream_capacity": world.downstream_capacity,
            "target_downstream": world.target_downstream,
            "start": {
                "main_queue": scenario.main_queue,
                "side_queue": scenario.side_queue,
                "downstream_queue": scenario.downstream_queue,
            },
        },
        "policies": [summarize("baseline"), summarize("heuristic")],
        "feedback": [
            "The baseline releases the largest upstream queue and causes downstream spillback.",
            "The heuristic system treats downstream capacity as a hard safety constraint.",
            "The update target is the signal/diversion rule, plus a replay regression test.",
        ],
        "candidate_update": {
            "target": "examples/traffic-grid/policies.py",
            "rule": "Protect downstream capacity before releasing the largest upstream queue.",
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
