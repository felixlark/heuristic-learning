# GridWorld Heuristic System

This is the smallest teaching example in the course. It shows how a local greedy policy can walk into a known trap, and how a maintainable heuristic policy rejects unsafe shortest moves.

## Learning Target

- Failure mode: `local_greedy_trap`
- Baseline: move greedily toward the goal.
- Heuristic patch: keep trap avoidance explicit before path shortening.
- Update target: `examples/heuristic-gridworld/policies.py`

## Run

```bash
npm run examples:gridworld
```

## Feedback Report

```bash
npm run examples:gridworld:feedback
```

Report path:

```text
experiments/gridworld/latest.json
```

## Test

```bash
npm run examples:test
```

Focused test path:

```text
tests/test_gridworld.py
```

## Course Links

- Docs: `docs/zh-cn/examples/index.md`
- Lab: `docs/zh-cn/slides/lab-1/index.md`
- Anti-forgetting lab: `docs/zh-cn/slides/lab-2/index.md`
