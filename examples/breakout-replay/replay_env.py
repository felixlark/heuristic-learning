from __future__ import annotations

from dataclasses import dataclass


Action = str


@dataclass(frozen=True)
class BreakoutFrame:
    step: int
    ball_x: float
    ball_y: float
    velocity_x: float
    velocity_y: float
    paddle_x: float


@dataclass(frozen=True)
class BreakoutReplayWorld:
    field_left: float = 8.0
    field_right: float = 151.0
    paddle_y: float = 189.5
    paddle_min_x: float = 15.5
    paddle_max_x: float = 152.5
    paddle_speed: float = 12.0
    hit_deadband_px: float = 6.0
    max_steps: int = 16

    def initial_frame(self) -> BreakoutFrame:
        return BreakoutFrame(
            step=0,
            ball_x=148.0,
            ball_y=141.5,
            velocity_x=8.0,
            velocity_y=6.0,
            paddle_x=110.0,
        )

    def reflect_position(self, value: float) -> float:
        span = self.field_right - self.field_left
        if span <= 0:
            return self.field_left
        period = 2.0 * span
        shifted = (value - self.field_left) % period
        if shifted <= span:
            return self.field_left + shifted
        return self.field_right - (shifted - span)

    def intercept_x(self, frame: BreakoutFrame) -> float:
        steps_to_paddle = max((self.paddle_y - frame.ball_y) / frame.velocity_y, 0.0)
        return self.reflect_position(frame.ball_x + frame.velocity_x * steps_to_paddle)

    def step(self, frame: BreakoutFrame, action: Action) -> tuple[BreakoutFrame, float, bool, str]:
        if action == "left":
            paddle_x = max(self.paddle_min_x, frame.paddle_x - self.paddle_speed)
        elif action == "right":
            paddle_x = min(self.paddle_max_x, frame.paddle_x + self.paddle_speed)
        elif action == "stay":
            paddle_x = frame.paddle_x
        else:
            raise ValueError(f"unknown action: {action}")

        next_y = frame.ball_y + frame.velocity_y
        raw_next_x = frame.ball_x + frame.velocity_x
        next_x = self.reflect_position(raw_next_x)
        next_velocity_x = frame.velocity_x
        if raw_next_x < self.field_left or raw_next_x > self.field_right:
            next_velocity_x = -frame.velocity_x
        next_frame = BreakoutFrame(
            step=frame.step + 1,
            ball_x=next_x,
            ball_y=next_y,
            velocity_x=next_velocity_x,
            velocity_y=frame.velocity_y,
            paddle_x=paddle_x,
        )

        if next_y >= self.paddle_y:
            miss_distance = abs(paddle_x - next_x)
            if miss_distance <= self.hit_deadband_px:
                return next_frame, 1.0, True, "intercepted"
            return next_frame, -1.0, True, "missed_after_wall_reflection"

        return next_frame, -0.01, False, "continue"
