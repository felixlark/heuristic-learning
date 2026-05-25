from __future__ import annotations

import argparse
from collections.abc import Callable

from replay_env import ReplayFrame, ReplayWorld
from vizdoom_policies import baseline_policy, heuristic_policy


Policy = Callable[[ReplayWorld, ReplayFrame], str]


def run_episode(world: ReplayWorld, policy: Policy) -> dict[str, object]:
    frame = world.initial_frame()
    trace = [frame]
    total_reward = 0.0

    for step in range(world.max_steps):
        action = policy(world, frame)
        frame, reward, done, reason = world.step(frame, action)
        trace.append(frame)
        total_reward += reward
        if done:
            return {
                "steps": step + 1,
                "reward": round(total_reward, 3),
                "reason": reason,
                "trace": trace,
            }

    return {
        "steps": world.max_steps,
        "reward": round(total_reward, 3),
        "reason": "timeout",
        "trace": trace,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=["baseline", "heuristic"], default="heuristic")
    args = parser.parse_args()

    world = ReplayWorld()
    policy = baseline_policy if args.policy == "baseline" else heuristic_policy
    result = run_episode(world, policy)

    print(f"policy={args.policy}")
    print(f"reason={result['reason']}")
    print(f"reward={result['reward']}")
    print(f"steps={result['steps']}")
    for frame in result["trace"]:
        print(
            "frame "
            f"step={frame.step} health={frame.health:.1f} "
            f"area={frame.medikit_area:.1f} offset={frame.medikit_offset:.2f}"
        )


if __name__ == "__main__":
    main()
