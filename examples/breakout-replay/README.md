# Breakout Replay Wall Reflection

This lightweight replay keeps the trajectory-prediction idea from the `learning-beyond-gradients` Breakout artifact. The key lesson is that chasing the current ball coordinate is not the same as predicting the intercept point after a wall reflection.

## Learning Target

- Failure mode: `missed_after_wall_reflection`
- Baseline: move the paddle toward the current ball x position.
- Heuristic patch: predict the side-wall-reflected landing point at paddle height.
- Update target: `examples/breakout-replay/policies.py`

## Run

```bash
npm run examples:breakout-replay
```

## Feedback Report

```bash
npm run examples:breakout-replay:feedback
```

Report path:

```text
experiments/breakout-replay/latest.json
```

## Test

```bash
npm run examples:test
```

Focused test path:

```text
tests/test_breakout_replay.py
```

## Course Links

- Case: `docs/zh-cn/cases/breakout/index.md`
- Source registry: `docs/zh-cn/appendix/source-registry.md`
- Anti-forgetting lab: `docs/zh-cn/slides/lab-2/index.md`
