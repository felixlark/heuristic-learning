from __future__ import annotations

import argparse
from collections.abc import Callable

from env import SoccerState, SoccerWorld, default_scenario
from policies import baseline_policy, heuristic_policy


Policy = Callable[[SoccerWorld, SoccerState], str]


def run_episode(world: SoccerWorld, policy: Policy, start: SoccerState | None = None) -> dict[str, object]:
    state = start or default_scenario()
    trace = [state]
    total_reward = 0

    for step in range(1, world.max_steps + 1):
        action = policy(world, state)
        state, reward, done, reason = world.step(state, action)
        trace.append(state)
        total_reward += reward
        if done:
            return {
                "steps": step,
                "reward": total_reward,
                "reason": reason,
                "trace": trace,
            }

    return {
        "steps": world.max_steps,
        "reward": total_reward,
        "reason": "timeout",
        "trace": trace,
    }


def format_state(state: SoccerState) -> str:
    return (
        f"robot={state.robot}, ball={state.ball}, opponent={state.opponent}, "
        f"has_ball={state.has_ball}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=["baseline", "heuristic"], default="heuristic")
    args = parser.parse_args()

    world = SoccerWorld()
    policy = baseline_policy if args.policy == "baseline" else heuristic_policy
    result = run_episode(world, policy)

    print(f"policy={args.policy}")
    print(f"reason={result['reason']}")
    print(f"reward={result['reward']}")
    print(f"steps={result['steps']}")
    for index, state in enumerate(result["trace"]):
        print(f"trace[{index}] {format_state(state)}")


if __name__ == "__main__":
    main()
