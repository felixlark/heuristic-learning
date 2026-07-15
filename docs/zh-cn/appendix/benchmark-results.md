---
title: Benchmark 结果摘要
description: Heuristic Learning 七个主线示例的 baseline、heuristic、报告和验证入口
---

# Benchmark 结果摘要

本页把七个主线示例压成一张研究结果表。它不是通用分数榜，也不声称轻量 replay 等同于真实 MuJoCo、Atari 或 VizDoom 复现；它的作用是让读者快速看到每个实验的 baseline failure、heuristic outcome、反馈报告、测试和课程落点。

机器可读摘要见 [`/benchmark-summary.json`](/benchmark-summary.json)，字段约束见 [`/benchmark-summary.schema.json`](/benchmark-summary.schema.json)。`npm run benchmark:summary:check` 会从 `docs/public/example-registry.json` 和 `experiments/*/latest.json` 交叉验证每一行，避免表格和实验报告漂移。

当前结果表只记录已经可复跑的 baseline/heuristic 对照；下一步变量对照和不变量见 [消融计划](/zh-cn/appendix/ablation-plan) 与 [`/ablation-plan.json`](/ablation-plan.json)。`npm run ablation:plan:check` 会检查每个计划是否绑定示例、指标、证据和命令。

## 结果矩阵

| 示例 | Baseline failure | Heuristic outcome | Report | Test |
| --- | --- | --- | --- | --- |
| GridWorld | `local_greedy_trap` | `trap_avoided` | `experiments/gridworld/latest.json` | `tests/test_gridworld.py` |
| Robot Soccer | `blocked_shot` | `goal` | `experiments/robot-soccer/latest.json` | `tests/test_robot_soccer.py` |
| VizDoom Replay | `wasted_pickup` | `valued_pickup` | `experiments/vizdoom-replay/latest.json` | `tests/test_vizdoom_replay.py` |
| Traffic Grid | `spillback` | `stable_flow` | `experiments/traffic-grid/latest.json` | `tests/test_traffic_grid.py` |
| Breakout Replay | `missed_after_wall_reflection` | `intercepted` | `experiments/breakout-replay/latest.json` | `tests/test_breakout_replay.py` |
| Ant Gait Replay | `yaw_drift` | `stable_stride` | `experiments/ant-gait-replay/latest.json` | `tests/test_ant_gait_replay.py` |
| Constraint Audit | `accepted_constraint_violation` | `blocked_constraint_violation` | `experiments/constraint-audit/latest.json` | `tests/test_constraint_audit.py` |

## 怎么读这张表

每一行都遵循同一个实验协议：

```text
case signal -> minimal environment/replay -> baseline failure
            -> heuristic patch -> feedback report -> regression test
```

因此本页的重点不是“heuristic reward 更高”，而是：

- baseline failure 是否稳定可命名；
- heuristic outcome 是否能在报告里被复查；
- `candidate_update.target` 是否指向真实可维护文件；
- 测试和课程页是否能保护旧经验不被下一轮修改破坏。

## 统一验证

运行：

```bash
npm run benchmark:summary:check
npm run examples:feedback
npm run examples:reports:check
npm run examples:test
npm run verify
```

`benchmark:summary:check` 只检查摘要与当前报告是否一致；完整验收仍以 `npm run verify` 为准。

## 边界

- GridWorld 是教学最小环境，不代表真实游戏或机器人任务。
- Breakout、VizDoom、Ant 是轻量 replay，用来隔离策略对象和 failure mode，不等同于完整高保真复现。
- Robot Soccer 和 Traffic Grid 来自脱敏应用问题抽象，不公开私有原文。
- Constraint Audit 是闭世界研究夹具，不评估通用事实性或纳什均衡收敛。
- 如果未来接入真实环境，本页应保留轻量 replay 行，并新增高保真验证行，而不是覆盖已有教学结果。
