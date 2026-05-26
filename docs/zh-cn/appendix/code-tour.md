---
title: 代码导览
description: Heuristic Learning 六个可运行示例的代码阅读顺序、运行命令、编辑目标和测试路径
---

# 代码导览

本页把“跑通示例”推进到“读懂闭环”。每个 tour 都告诉读者先读环境、再读策略、再读运行入口、反馈报告和测试；这样可以把 HL 的状态、动作、反馈、更新对象和回归验证对应到具体文件。

机器可读导览见 [`/code-tour.json`](/code-tour.json)，字段约束见 [`/code-tour.schema.json`](/code-tour.schema.json)。`npm run code:tour:check` 会检查每个 tour 是否绑定示例、`reading_order`、运行命令、`edit_target` 和测试文件。

## 六个示例的阅读顺序

| Tour | 阅读顺序 | 关键问题 | 运行命令 |
| --- | --- | --- | --- |
| GridWorld 代码导览 | `env.py` -> `policies.py` -> `run.py` -> `feedback_loop.py` -> `tests/test_gridworld.py` | 为什么平均 episode 成功仍需要 `local_greedy_trap` probe？ | `npm run examples:gridworld`、`npm run examples:gridworld:feedback` |
| Robot Soccer 代码导览 | `env.py` -> `policies.py` -> `run.py` -> `feedback_loop.py` -> `tests/test_robot_soccer.py` | blocked-lane 检查为什么应该是显式规则？ | `npm run examples:robot-soccer`、`npm run examples:robot-soccer:feedback` |
| VizDoom Replay 代码导览 | `replay_env.py` -> `vizdoom_policies.py` -> `run.py` -> `feedback_loop.py` -> `tests/test_vizdoom_replay.py` | 检测字段如何转成 pickup 策略？ | `npm run examples:vizdoom-replay`、`npm run examples:vizdoom-replay:feedback` |
| Traffic Grid 代码导览 | `env.py` -> `policies.py` -> `run.py` -> `feedback_loop.py` -> `tests/test_traffic_grid.py` | downstream capacity 为什么是安全不变量？ | `npm run examples:traffic-grid`、`npm run examples:traffic-grid:feedback` |
| Breakout Replay 代码导览 | `replay_env.py` -> `policies.py` -> `run.py` -> `feedback_loop.py` -> `tests/test_breakout_replay.py` | 侧墙反射预测如何变成课程 replay？ | `npm run examples:breakout-replay`、`npm run examples:breakout-replay:feedback` |
| Ant Gait Replay 代码导览 | `replay_env.py` -> `policies.py` -> `run.py` -> `feedback_loop.py` -> `tests/test_ant_gait_replay.py` | 连续控制 heuristic 如何保持可 review？ | `npm run examples:ant-gait-replay`、`npm run examples:ant-gait-replay:feedback` |

## 读代码的固定动作

1. 先读 `env.py` 或 `replay_env.py`，找出状态字段和 failure mode。
2. 再读 `policies.py` 或 `vizdoom_policies.py`，标出 baseline 和 heuristic 的分叉点。
3. 运行 `run.py` 对应的 npm 命令，只看最小输出。
4. 运行 feedback 命令，确认 report 里有 baseline failure、heuristic outcome 和 candidate update。
5. 最后读 test 文件，确认旧 probe 如何防止下一次更新遗忘。

## 编辑边界

每个 tour 都有一个 `edit_target`。新读者只应该先修改这个文件，并运行对应测试；不要同时改环境、报告和测试，否则无法判断一次 heuristic update 的实际作用。若要改变环境或报告 schema，先更新 [实验协议](/zh-cn/appendix/benchmark-protocol)、[消融计划](/zh-cn/appendix/ablation-plan) 和 [Artifact 差距分析](/zh-cn/appendix/artifact-gap-analysis)。

```bash
npm run code:tour:check
npm run examples:test
npm run examples:reports:check
npm run verify
```
