# Traffic Grid Downstream Spillback

This minimal traffic-grid replay is derived from an internal Feishu signal about East Lake traffic simulation. It keeps the learning object small: a signal policy must protect downstream capacity before releasing upstream queues.

## Learning Target

- Failure mode: `spillback`
- Baseline: release the largest upstream queue.
- Heuristic patch: treat downstream capacity as a hard safety constraint before releasing flow.
- Update target: `examples/traffic-grid/policies.py`

## Run

```bash
npm run examples:traffic-grid
```

## Feedback Report

```bash
npm run examples:traffic-grid:feedback
```

Report path:

```text
experiments/traffic-grid/latest.json
```

## Test

```bash
npm run examples:test
```

Focused test path:

```text
tests/test_traffic_grid.py
```

## Course Links

- Case: `docs/zh-cn/cases/traffic-simulation/index.md`
- Source registry: `docs/zh-cn/appendix/source-registry.md`
- Anti-forgetting lab: `docs/zh-cn/slides/lab-2/index.md`
