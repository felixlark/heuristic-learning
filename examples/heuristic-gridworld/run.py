from __future__ import annotations

import argparse
from collections.abc import Callable

from env import GridWorld, Position
from policies import baseline_policy, heuristic_policy


Policy = Callable[[GridWorld, Position, list[Position]], str]


def run_episode(env: GridWorld, policy: Policy) -> dict[str, object]:
    pos = env.reset()
    history = [pos]
    total_reward = 0

    for step in range(1, env.max_steps + 1):
        action = policy(env, pos, history)
        pos, reward, done, reason = env.step(pos, action)
        history.append(pos)
        total_reward += reward
        if done:
            return {
                "steps": step,
                "reward": total_reward,
                "reason": reason,
                "path": history,
            }

    return {
        "steps": env.max_steps,
        "reward": total_reward,
        "reason": "timeout",
        "path": history,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=["baseline", "heuristic"], default="heuristic")
    parser.add_argument("--episodes", type=int, default=20)
    args = parser.parse_args()

    env = GridWorld()
    policy = baseline_policy if args.policy == "baseline" else heuristic_policy

    outcomes = [run_episode(env, policy) for _ in range(args.episodes)]
    successes = sum(outcome["reason"] == "goal" for outcome in outcomes)
    avg_reward = sum(int(outcome["reward"]) for outcome in outcomes) / args.episodes
    first = outcomes[0]

    print(f"policy={args.policy}")
    print(f"episodes={args.episodes}")
    print(f"successes={successes}")
    print(f"avg_reward={avg_reward:.2f}")
    print(f"first_reason={first['reason']}")
    print(f"first_steps={first['steps']}")
    print("first_path=" + " -> ".join(map(str, first["path"])))


if __name__ == "__main__":
    main()
