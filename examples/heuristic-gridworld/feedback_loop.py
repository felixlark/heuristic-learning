from __future__ import annotations

import argparse
import json
from pathlib import Path

from env import GridWorld
from policies import baseline_policy, heuristic_policy
from run import run_episode


def summarize_policy(env: GridWorld, name: str, episodes: int) -> dict[str, object]:
    policy = baseline_policy if name == "baseline" else heuristic_policy
    outcomes = [run_episode(env, policy) for _ in range(episodes)]
    reasons: dict[str, int] = {}
    for outcome in outcomes:
        reason = str(outcome["reason"])
        reasons[reason] = reasons.get(reason, 0) + 1
    return {
        "policy": name,
        "episodes": episodes,
        "successes": reasons.get("goal", 0),
        "failures": episodes - reasons.get("goal", 0),
        "reasons": reasons,
        "sample_path": outcomes[0]["path"],
        "sample_reward": outcomes[0]["reward"],
    }


def build_feedback_report(episodes: int) -> dict[str, object]:
    env = GridWorld()
    baseline = summarize_policy(env, "baseline", episodes)
    heuristic = summarize_policy(env, "heuristic", episodes)
    trap_probe = GridWorld(start=(1, 1), goal=(3, 1), traps=frozenset({(2, 1)}))
    baseline_action = baseline_policy(trap_probe, trap_probe.start, [trap_probe.start])
    heuristic_action = heuristic_policy(trap_probe, trap_probe.start, [trap_probe.start])
    return {
        "environment": {
            "width": env.width,
            "height": env.height,
            "start": env.start,
            "goal": env.goal,
            "traps": sorted(env.traps),
            "max_steps": env.max_steps,
        },
        "policies": [baseline, heuristic],
        "probes": [
            {
                "name": "local_greedy_trap",
                "start": trap_probe.start,
                "goal": trap_probe.goal,
                "traps": sorted(trap_probe.traps),
                "baseline_action": baseline_action,
                "heuristic_action": heuristic_action,
                "baseline_next": trap_probe.next_position(trap_probe.start, baseline_action),
                "heuristic_next": trap_probe.next_position(trap_probe.start, heuristic_action),
                "lesson": "The heuristic policy rejects the shortest action when it enters a known trap.",
            }
        ],
        "feedback": [
            "Baseline and heuristic policies are evaluated on the same environment.",
            "The local_greedy_trap probe isolates a failure mode that average reward can hide.",
            "A policy update is accepted only if it keeps goal success and avoids known traps.",
            "Future agent edits should add tests before changing policy rules.",
        ],
        "candidate_update": {
            "target": "examples/heuristic-gridworld/policies.py",
            "rule": "Keep trap avoidance explicit and regression-tested before adding path-shortening rules.",
            "verification": "python3 -m unittest discover -s tests",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = build_feedback_report(args.episodes)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
