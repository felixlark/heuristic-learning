#!/usr/bin/env python3
"""Evaluate transparent CartPole policies on a protected seed split."""

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from policy import baseline, improved

SPLITS = {
    "dev": range(0, 20),
    "holdout": range(1000, 1050),
    "audit": range(2000, 2050),
}


def seeds_for(split):
    if split not in SPLITS:
        raise ValueError(f"unknown split: {split}")
    return SPLITS[split]


def evaluate(policy, seeds):
    try:
        import gymnasium as gym
    except ImportError as exc:
        raise SystemExit(
            "Gymnasium is optional. Install it with: "
            "python3 -m pip install 'gymnasium[classic-control]'"
        ) from exc

    scores = []
    for seed in seeds:
        env = gym.make("CartPole-v1")
        observation, _ = env.reset(seed=seed)
        score = 0
        terminated = truncated = False
        while not (terminated or truncated):
            observation, _, terminated, truncated, _ = env.step(policy(observation))
            score += 1
        env.close()
        scores.append(score)
    return scores


def append_record(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=("baseline", "improved"), default="improved")
    parser.add_argument("--split", choices=tuple(SPLITS), default="dev")
    parser.add_argument("--ledger", type=Path, default=Path("experiments/cartpole/trials.jsonl"))
    args = parser.parse_args()

    policy = {"baseline": baseline, "improved": improved}[args.policy]
    scores = evaluate(policy, seeds_for(args.split))
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": "CartPole-v1",
        "policy": args.policy,
        "split": args.split,
        "episodes": len(scores),
        "mean_score": statistics.fmean(scores),
        "min_score": min(scores),
        "max_score": max(scores),
    }
    append_record(args.ledger, record)
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
