from __future__ import annotations

from replay_env import Action, BreakoutFrame, BreakoutReplayWorld


def _move_toward(world: BreakoutReplayWorld, paddle_x: float, target_x: float) -> Action:
    if target_x - paddle_x > world.hit_deadband_px:
        return "right"
    if paddle_x - target_x > world.hit_deadband_px:
        return "left"
    return "stay"


def baseline_policy(world: BreakoutReplayWorld, frame: BreakoutFrame) -> Action:
    return _move_toward(world, frame.paddle_x, frame.ball_x)


def heuristic_policy(world: BreakoutReplayWorld, frame: BreakoutFrame) -> Action:
    return _move_toward(world, frame.paddle_x, world.intercept_x(frame))
