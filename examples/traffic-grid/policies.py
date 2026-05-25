from __future__ import annotations

from env import Action, TrafficState, TrafficWorld


def baseline_policy(world: TrafficWorld, state: TrafficState) -> Action:
    del world
    if state.main_queue >= state.side_queue and state.main_queue > 0:
        return "release_main"
    if state.side_queue > 0:
        return "release_side"
    return "hold"


def heuristic_policy(world: TrafficWorld, state: TrafficState) -> Action:
    if (
        state.main_queue > 0
        and state.downstream_queue + min(3, state.main_queue) > world.downstream_capacity
    ):
        if state.downstream_queue >= world.downstream_capacity - 1:
            return "hold"
        return "divert_main"

    if state.main_queue > 0:
        return "release_main"

    if (
        state.side_queue > 0
        and state.downstream_queue + min(2, state.side_queue) <= world.downstream_capacity
    ):
        return "release_side"

    return "hold"
