# Robot Soccer Blocked Lane

This example turns a robot-soccer shot selection problem into a small deterministic probe. The baseline shoots as soon as it owns the ball; the heuristic policy checks whether the shot lane is blocked before committing.

## Learning Target

- Failure mode: `blocked_shot`
- Baseline: shoot when the goal is nearby.
- Heuristic patch: inspect the shot lane and reposition when blocked.
- Update target: `examples/robot-soccer/policies.py`

## Run

```bash
npm run examples:robot-soccer
```

## Feedback Report

```bash
npm run examples:robot-soccer:feedback
```

Report path:

```text
experiments/robot-soccer/latest.json
```

## Test

```bash
npm run examples:test
```

Focused test path:

```text
tests/test_robot_soccer.py
```

## Course Links

- Case: `docs/zh-cn/cases/robot-soccer/index.md`
- Lab: `docs/zh-cn/slides/lab-1/index.md`
- Anti-forgetting lab: `docs/zh-cn/slides/lab-2/index.md`
