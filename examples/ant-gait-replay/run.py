from __future__ import annotations

import argparse
from collections.abc import Callable

from policies import baseline_policy, heuristic_policy
from replay_env import AntGaitReplayWorld, AntGaitState, GaitCommand


Policy = Callable[[AntGaitState], GaitCommand]


def run_episode(world: AntGaitReplayWorld, policy: Policy) -> dict[str, object]:
    state = world.initial_state()
    trace = [state]
    commands: list[GaitCommand] = []
    total_reward = 0.0

    for _ in range(world.max_steps):
        command = policy(state)
        commands.append(command)
        state, reward, done, reason = world.step(state, command)
        trace.append(state)
        total_reward += reward
        if done:
            return {
                "steps": state.step,
                "reward": round(total_reward, 3),
                "reason": reason,
                "commands": commands,
                "trace": trace,
            }

    return {
        "steps": world.max_steps,
        "reward": round(total_reward, 3),
        "reason": "timeout",
        "commands": commands,
        "trace": trace,
    }


def format_state(state: AntGaitState) -> str:
    return (
        f"step={state.step} speed={state.speed:.3f} yaw={state.yaw:.3f} "
        f"yaw_rate={state.yaw_rate:.3f} stability={state.stability:.3f} "
        f"distance={state.distance:.3f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=["baseline", "heuristic"], default="heuristic")
    args = parser.parse_args()

    world = AntGaitReplayWorld()
    policy = baseline_policy if args.policy == "baseline" else heuristic_policy
    result = run_episode(world, policy)

    print(f"policy={args.policy}")
    print(f"reason={result['reason']}")
    print(f"reward={result['reward']}")
    print(f"steps={result['steps']}")
    for state in result["trace"]:
        print("trace " + format_state(state))


if __name__ == "__main__":
    main()
