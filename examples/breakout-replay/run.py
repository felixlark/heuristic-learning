from __future__ import annotations

import argparse
from collections.abc import Callable

from policies import baseline_policy, heuristic_policy
from replay_env import BreakoutFrame, BreakoutReplayWorld


Policy = Callable[[BreakoutReplayWorld, BreakoutFrame], str]


def run_episode(world: BreakoutReplayWorld, policy: Policy) -> dict[str, object]:
    frame = world.initial_frame()
    trace = [frame]
    actions: list[str] = []
    total_reward = 0.0

    for step in range(1, world.max_steps + 1):
        action = policy(world, frame)
        actions.append(action)
        frame, reward, done, reason = world.step(frame, action)
        trace.append(frame)
        total_reward += reward
        if done:
            return {
                "steps": step,
                "reward": round(total_reward, 3),
                "reason": reason,
                "actions": actions,
                "trace": trace,
            }

    return {
        "steps": world.max_steps,
        "reward": round(total_reward, 3),
        "reason": "timeout",
        "actions": actions,
        "trace": trace,
    }


def format_frame(frame: BreakoutFrame) -> str:
    return (
        f"step={frame.step} ball=({frame.ball_x:.1f},{frame.ball_y:.1f}) "
        f"vel=({frame.velocity_x:.1f},{frame.velocity_y:.1f}) "
        f"paddle={frame.paddle_x:.1f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=["baseline", "heuristic"], default="heuristic")
    args = parser.parse_args()

    world = BreakoutReplayWorld()
    policy = baseline_policy if args.policy == "baseline" else heuristic_policy
    result = run_episode(world, policy)

    print(f"policy={args.policy}")
    print(f"intercept_x={world.intercept_x(world.initial_frame()):.1f}")
    print(f"reason={result['reason']}")
    print(f"reward={result['reward']}")
    print(f"steps={result['steps']}")
    print("actions=" + ",".join(result["actions"]))
    for frame in result["trace"]:
        print("trace " + format_frame(frame))


if __name__ == "__main__":
    main()
