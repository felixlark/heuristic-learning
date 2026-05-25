# VizDoom Replay Medikit Staging

This lightweight replay preserves the medikit-staging idea from Jiayi Weng's `learning-beyond-gradients` VizDoom artifact while removing EnvPool and OpenCV dependencies for course use.

## Learning Target

- Failure mode: `wasted_pickup`
- Baseline: pick up the medikit immediately.
- Heuristic patch: wait near the medikit while health is high, then pick it up when it has value.
- Update target: `examples/vizdoom-replay/vizdoom_policies.py`

## Run

```bash
npm run examples:vizdoom-replay
```

## Feedback Report

```bash
npm run examples:vizdoom-replay:feedback
```

Report path:

```text
experiments/vizdoom-replay/latest.json
```

## Test

```bash
npm run examples:test
```

Focused test path:

```text
tests/test_vizdoom_replay.py
```

## Course Links

- Case: `docs/zh-cn/cases/vizdoom/index.md`
- Source registry: `docs/zh-cn/appendix/source-registry.md`
- Anti-forgetting lab: `docs/zh-cn/slides/lab-2/index.md`
