from __future__ import annotations

from env import Action, SoccerState, SoccerWorld


def baseline_policy(world: SoccerWorld, state: SoccerState) -> Action:
    if not state.has_ball:
        return "chase"
    if world.distance(state.ball, (state.goal_x, state.ball[1])) <= 4:
        return "shoot"
    return "dribble"


def heuristic_policy(world: SoccerWorld, state: SoccerState) -> Action:
    if not state.has_ball:
        return "chase"

    shot_lane_blocked = (
        state.ball[1] == state.opponent[1]
        and state.ball[0] < state.opponent[0] < state.goal_x
    )
    if shot_lane_blocked:
        return "reposition"

    if world.distance(state.ball, (state.goal_x, state.ball[1])) <= 2:
        return "shoot"
    return "dribble"
