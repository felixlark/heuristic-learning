from __future__ import annotations

from collections.abc import Iterable

from env import Action, GridWorld, Position


ACTION_ORDER: tuple[Action, ...] = ("right", "down", "left", "up")


def baseline_policy(env: GridWorld, pos: Position, history: Iterable[Position]) -> Action:
    """Greedy policy: choose the legal action that most reduces goal distance."""
    del history
    return min(
        ACTION_ORDER,
        key=lambda action: env.manhattan(env.next_position(pos, action)),
    )


def heuristic_policy(env: GridWorld, pos: Position, history: Iterable[Position]) -> Action:
    """Small Heuristic System policy with explicit, testable rules."""
    visited = set(history)

    candidates = []
    for action in ACTION_ORDER:
        nxt = env.next_position(pos, action)
        if nxt == pos:
            continue
        if nxt in env.traps:
            continue
        candidates.append((action, nxt))

    if not candidates:
        return baseline_policy(env, pos, history)

    return min(
        candidates,
        key=lambda item: (
            env.manhattan(item[1]),
            item[1] in visited,
            ACTION_ORDER.index(item[0]),
        ),
    )[0]
