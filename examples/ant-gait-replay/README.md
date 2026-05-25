# Ant Gait Replay Yaw Stabilization

This lightweight replay keeps the gait-control structure from the `learning-beyond-gradients` MuJoCo Ant artifact without requiring MuJoCo. It focuses on how cadence, stance duty, drive and yaw feedback become maintainable HL update targets.

## Learning Target

- Failure mode: `yaw_drift`
- Baseline: use a fixed open-loop rhythm.
- Heuristic patch: couple speed-adaptive cadence, stance duty and yaw feedback.
- Update target: `examples/ant-gait-replay/policies.py`

## Run

```bash
npm run examples:ant-gait-replay
```

## Feedback Report

```bash
npm run examples:ant-gait-replay:feedback
```

Report path:

```text
experiments/ant-gait-replay/latest.json
```

## Test

```bash
npm run examples:test
```

Focused test path:

```text
tests/test_ant_gait_replay.py
```

## Course Links

- Case: `docs/zh-cn/cases/ant-gait/index.md`
- Source registry: `docs/zh-cn/appendix/source-registry.md`
- Anti-forgetting lab: `docs/zh-cn/slides/lab-2/index.md`
