from __future__ import annotations

from replay_env import AntGaitState, GaitCommand


def _clip(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def baseline_policy(state: AntGaitState) -> GaitCommand:
    """Fixed open-loop rhythm: useful until yaw drift compounds."""

    return GaitCommand(
        phase_increment=0.66,
        stance_duty=0.50,
        yaw_feedback=0.0,
        drive=0.92,
    )


def heuristic_policy(state: AntGaitState) -> GaitCommand:
    """Speed-adaptive CPG with yaw feedback, mirroring the Ant artifact."""

    speed_error = state.speed - 5.8
    phase_increment = _clip(0.6609 - 0.02 * speed_error, 0.62, 0.72)
    stance_duty = _clip(0.6355 - 0.01 * speed_error, 0.60, 0.67)
    yaw_feedback = _clip(0.72 * state.yaw + 1.35 * state.yaw_rate, -1.0, 1.0)
    drive = _clip(1.02 + 0.04 * (5.8 - state.speed), 0.9, 1.14)
    return GaitCommand(
        phase_increment=phase_increment,
        stance_duty=stance_duty,
        yaw_feedback=yaw_feedback,
        drive=drive,
    )
