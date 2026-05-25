from __future__ import annotations

import argparse
import json
from pathlib import Path

from replay_env import ReplayWorld
from run import run_episode
from vizdoom_policies import baseline_policy, heuristic_policy


def summarize(name: str) -> dict[str, object]:
    world = ReplayWorld()
    policy = baseline_policy if name == "baseline" else heuristic_policy
    result = run_episode(world, policy)
    return {
        "policy": name,
        "reason": result["reason"],
        "reward": result["reward"],
        "steps": result["steps"],
        "trace": [
            {
                "step": frame.step,
                "health": frame.health,
                "medikit_visible": frame.medikit_visible,
                "medikit_area": frame.medikit_area,
                "medikit_offset": frame.medikit_offset,
            }
            for frame in result["trace"]
        ],
    }


def build_feedback_report() -> dict[str, object]:
    world = ReplayWorld()
    return {
        "case": "vizdoom_d1_medikit_staging",
        "source": {
            "repo": "Trinkle23897/learning-beyond-gradients",
            "artifact": "vizdoom/heuristic_vizdoom_d1_cv.py",
            "note": "The course example keeps the medikit staging decision but removes EnvPool/OpenCV dependencies.",
        },
        "thresholds": {
            "pickup_health": world.pickup_health,
            "stage_area": world.stage_area,
        },
        "policies": [summarize("baseline"), summarize("heuristic")],
        "feedback": [
            "The baseline consumes the medikit immediately and wastes pickup value.",
            "The heuristic system stages near the medikit while health is high.",
            "The update target is the policy threshold, not a neural-network parameter.",
        ],
        "candidate_update": {
            "target": "examples/vizdoom-replay/vizdoom_policies.py",
            "rule": "Keep medikit staging tied to health and visible area; preserve replay regression tests.",
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
