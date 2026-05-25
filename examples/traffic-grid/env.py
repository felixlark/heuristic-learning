from __future__ import annotations

from dataclasses import dataclass


Action = str


@dataclass(frozen=True)
class TrafficState:
    step: int
    main_queue: int
    side_queue: int
    downstream_queue: int


@dataclass(frozen=True)
class TrafficWorld:
    downstream_capacity: int = 8
    target_downstream: int = 5
    max_steps: int = 12

    def step(self, state: TrafficState, action: Action) -> tuple[TrafficState, int, bool, str]:
        main_queue = state.main_queue
        side_queue = state.side_queue
        downstream_queue = state.downstream_queue
        reward = -1

        if action == "release_main":
            released = min(3, main_queue)
            main_queue -= released
            downstream_queue += released
            reward += released
        elif action == "release_side":
            released = min(2, side_queue)
            side_queue -= released
            downstream_queue += released
            reward += released
        elif action == "hold":
            downstream_queue = max(0, downstream_queue - 2)
        elif action == "divert_main":
            diverted = min(2, main_queue)
            main_queue -= diverted
            downstream_queue += 1 if diverted else 0
            reward += diverted
        else:
            raise ValueError(f"unknown action: {action}")

        next_state = TrafficState(
            step=state.step + 1,
            main_queue=main_queue,
            side_queue=side_queue,
            downstream_queue=downstream_queue,
        )

        if downstream_queue > self.downstream_capacity:
            return next_state, -12, True, "spillback"

        if (
            main_queue == 0
            and side_queue == 0
            and downstream_queue <= self.target_downstream
        ):
            return next_state, reward + 12, True, "stable_flow"

        return next_state, reward, False, "continue"


def default_scenario() -> TrafficState:
    return TrafficState(step=0, main_queue=6, side_queue=3, downstream_queue=7)
