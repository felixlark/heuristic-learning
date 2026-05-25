from __future__ import annotations

from dataclasses import dataclass


Action = str
Position = tuple[int, int]


DELTAS: dict[Action, Position] = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


@dataclass(frozen=True)
class GridWorld:
    width: int = 5
    height: int = 5
    start: Position = (0, 0)
    goal: Position = (4, 4)
    traps: frozenset[Position] = frozenset({(2, 1), (2, 2), (1, 3)})
    max_steps: int = 30

    def reset(self) -> Position:
        return self.start

    def in_bounds(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def next_position(self, pos: Position, action: Action) -> Position:
        dx, dy = DELTAS[action]
        candidate = (pos[0] + dx, pos[1] + dy)
        return candidate if self.in_bounds(candidate) else pos

    def step(self, pos: Position, action: Action) -> tuple[Position, int, bool, str]:
        nxt = self.next_position(pos, action)
        if nxt in self.traps:
            return nxt, -10, True, "trap"
        if nxt == self.goal:
            return nxt, 20, True, "goal"
        if nxt == pos:
            return nxt, -2, False, "wall"
        return nxt, -1, False, "move"

    def manhattan(self, pos: Position) -> int:
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])
