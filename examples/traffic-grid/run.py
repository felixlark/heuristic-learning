from __future__ import annotations

import argparse
from collections.abc import Callable

from env import TrafficState, TrafficWorld, default_scenario
from policies import baseline_policy, heuristic_policy


Policy = Callable[[TrafficWorld, TrafficState], str]


def run_episode(
    world: TrafficWorld,
    policy: Policy,
    start: TrafficState | None = None,
) -> dict[str, object]:
    state = start or default_scenario()
    trace = [state]
    actions: list[str] = []
    total_reward = 0

    for step in range(1, world.max_steps + 1):
        action = policy(world, state)
        actions.append(action)
        state, reward, done, reason = world.step(state, action)
        trace.append(state)
        total_reward += reward
        if done:
            return {
                "steps": step,
                "reward": total_reward,
                "reason": reason,
                "actions": actions,
                "trace": trace,
            }

    return {
        "steps": world.max_steps,
        "reward": total_reward,
        "reason": "timeout",
        "actions": actions,
        "trace": trace,
    }


def format_state(state: TrafficState) -> str:
    return (
        f"step={state.step}, main={state.main_queue}, "
        f"side={state.side_queue}, downstream={state.downstream_queue}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", choices=["baseline", "heuristic"], default="heuristic")
    args = parser.parse_args()

    world = TrafficWorld()
    policy = baseline_policy if args.policy == "baseline" else heuristic_policy
    result = run_episode(world, policy)

    print(f"policy={args.policy}")
    print(f"reason={result['reason']}")
    print(f"reward={result['reward']}")
    print(f"steps={result['steps']}")
    print("actions=" + ",".join(result["actions"]))
    for state in result["trace"]:
        print("trace " + format_state(state))


if __name__ == "__main__":
    main()
