from __future__ import annotations

from replay_env import Action, ReplayFrame, ReplayWorld


def baseline_policy(world: ReplayWorld, frame: ReplayFrame) -> Action:
    del world
    if not frame.medikit_visible:
        return "turn_left"
    if frame.medikit_offset < -0.15:
        return "turn_left"
    if frame.medikit_offset > 0.15:
        return "turn_right"
    return "forward"


def heuristic_policy(world: ReplayWorld, frame: ReplayFrame) -> Action:
    if not frame.medikit_visible:
        return "turn_left"
    if frame.medikit_offset < -0.15:
        return "turn_left"
    if frame.medikit_offset > 0.15:
        return "turn_right"
    if frame.medikit_area >= world.stage_area and frame.health > world.pickup_health:
        return "wait"
    return "forward"
