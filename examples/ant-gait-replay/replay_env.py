from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AntGaitState:
    step: int
    phase: float
    speed: float
    yaw: float
    yaw_rate: float
    stability: float
    distance: float


@dataclass(frozen=True)
class GaitCommand:
    phase_increment: float
    stance_duty: float
    yaw_feedback: float
    drive: float


class AntGaitReplayWorld:
    """Small Ant gait replay distilled from the MuJoCo heuristic artifact."""

    max_steps = 24
    target_speed = 5.8
    yaw_limit = 0.72
    initial_yaw_rate = 0.105

    def initial_state(self) -> AntGaitState:
        return AntGaitState(
            step=0,
            phase=0.0,
            speed=4.2,
            yaw=0.0,
            yaw_rate=self.initial_yaw_rate,
            stability=1.0,
            distance=0.0,
        )

    def step(self, state: AntGaitState, command: GaitCommand) -> tuple[AntGaitState, float, bool, str]:
        cadence_error = abs(command.phase_increment - 0.66)
        duty_error = abs(command.stance_duty - 0.64)

        yaw_rate = (
            state.yaw_rate
            + 0.026
            - 0.18 * command.yaw_feedback
            + 0.08 * duty_error
        )
        yaw = state.yaw + yaw_rate

        drive_error = abs(command.drive - 1.0)
        speed = state.speed + 0.34 * command.drive - 0.09 * abs(yaw) - 0.15 * cadence_error
        stability = state.stability - 0.035 * abs(yaw) - 0.02 * drive_error
        distance = state.distance + max(0.0, speed) * 0.05

        next_state = AntGaitState(
            step=state.step + 1,
            phase=state.phase + command.phase_increment,
            speed=round(speed, 3),
            yaw=round(yaw, 3),
            yaw_rate=round(yaw_rate, 3),
            stability=round(stability, 3),
            distance=round(distance, 3),
        )

        reward = round(0.2 * speed + stability - 1.8 * abs(yaw), 3)
        if abs(yaw) > self.yaw_limit:
            return next_state, reward - 6.0, True, "yaw_drift"
        if next_state.step >= self.max_steps:
            return next_state, reward + 1.0, True, "stable_stride"
        return next_state, reward, False, "running"
