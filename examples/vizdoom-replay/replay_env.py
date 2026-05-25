from __future__ import annotations

from dataclasses import dataclass


Action = str


@dataclass(frozen=True)
class ReplayFrame:
    step: int
    health: float
    medikit_visible: bool
    medikit_area: float
    medikit_offset: float


@dataclass(frozen=True)
class ReplayWorld:
    pickup_health: float = 68.0
    stage_area: float = 180.0
    max_steps: int = 12

    def initial_frame(self) -> ReplayFrame:
        return ReplayFrame(
            step=0,
            health=92.0,
            medikit_visible=True,
            medikit_area=220.0,
            medikit_offset=0.0,
        )

    def step(self, frame: ReplayFrame, action: Action) -> tuple[ReplayFrame, float, bool, str]:
        if action == "forward":
            next_frame = ReplayFrame(
                step=frame.step + 1,
                health=frame.health,
                medikit_visible=frame.medikit_visible,
                medikit_area=frame.medikit_area,
                medikit_offset=frame.medikit_offset,
            )
            if not frame.medikit_visible:
                return next_frame, -0.2, False, "blind_forward"
            if frame.health > self.pickup_health:
                return next_frame, -1.0, True, "wasted_pickup"
            return next_frame, 1.0, True, "valued_pickup"

        if action == "wait":
            next_health = max(1.0, frame.health - 6.0)
            next_area = min(260.0, frame.medikit_area + 4.0)
            return (
                ReplayFrame(
                    step=frame.step + 1,
                    health=next_health,
                    medikit_visible=frame.medikit_visible,
                    medikit_area=next_area,
                    medikit_offset=frame.medikit_offset,
                ),
                -0.02,
                False,
                "staging",
            )

        if action == "turn_left":
            return (
                ReplayFrame(
                    step=frame.step + 1,
                    health=max(1.0, frame.health - 4.0),
                    medikit_visible=True,
                    medikit_area=frame.medikit_area,
                    medikit_offset=frame.medikit_offset - 0.25,
                ),
                -0.05,
                False,
                "aligning",
            )

        if action == "turn_right":
            return (
                ReplayFrame(
                    step=frame.step + 1,
                    health=max(1.0, frame.health - 4.0),
                    medikit_visible=True,
                    medikit_area=frame.medikit_area,
                    medikit_offset=frame.medikit_offset + 0.25,
                ),
                -0.05,
                False,
                "aligning",
            )

        raise ValueError(f"unknown action: {action}")
