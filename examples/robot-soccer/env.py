from __future__ import annotations

from dataclasses import dataclass


Action = str
Position = tuple[int, int]


@dataclass(frozen=True)
class SoccerState:
    robot: Position
    ball: Position
    opponent: Position
    goal_x: int
    has_ball: bool = False


@dataclass(frozen=True)
class SoccerWorld:
    width: int = 7
    height: int = 5
    max_steps: int = 12

    def in_bounds(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def distance(self, a: Position, b: Position) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def move_toward(self, src: Position, dst: Position) -> Position:
        sx, sy = src
        dx, dy = dst
        if sx < dx:
            candidate = (sx + 1, sy)
        elif sx > dx:
            candidate = (sx - 1, sy)
        elif sy < dy:
            candidate = (sx, sy + 1)
        elif sy > dy:
            candidate = (sx, sy - 1)
        else:
            candidate = src
        return candidate if self.in_bounds(candidate) else src

    def step(self, state: SoccerState, action: Action) -> tuple[SoccerState, int, bool, str]:
        robot = state.robot
        ball = state.ball
        has_ball = state.has_ball

        if action == "chase":
            robot = self.move_toward(robot, ball)
            if robot == ball:
                has_ball = True
        elif action == "dribble":
            if not has_ball:
                return state, -4, False, "dribble_without_ball"
            next_ball = self.move_toward(ball, (state.goal_x, ball[1]))
            robot = ball
            ball = next_ball
        elif action == "shoot":
            if not has_ball:
                return state, -6, True, "shot_without_ball"
            if ball[1] == state.opponent[1] and ball[0] < state.opponent[0] < state.goal_x:
                return state, -10, True, "blocked_shot"
            if self.distance(ball, (state.goal_x, ball[1])) <= 2:
                return state, 20, True, "goal"
            return state, -3, False, "shot_too_far"
        elif action == "reposition":
            safe_lane = 1 if state.opponent[1] == 2 else 2
            robot = (robot[0], safe_lane)
            if has_ball:
                ball = robot
        else:
            raise ValueError(f"unknown action: {action}")

        if has_ball and robot == state.opponent:
            return SoccerState(robot, ball, state.opponent, state.goal_x, has_ball), -10, True, "tackled"

        return SoccerState(robot, ball, state.opponent, state.goal_x, has_ball), -1, False, "continue"


def default_scenario() -> SoccerState:
    return SoccerState(robot=(0, 2), ball=(2, 2), opponent=(4, 2), goal_x=6)
