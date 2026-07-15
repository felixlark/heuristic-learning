---
title: 消融计划
description: Heuristic Learning 七个主线示例的变量对照、证据路径和验证命令
---

# 消融计划

本页把七个 runnable examples 的后续研究对照写成可检查计划。它补充 [Benchmark 结果摘要](/zh-cn/appendix/benchmark-results)：benchmark 当前回答“现在跑出了什么”，消融计划回答“下一步应该改变哪个变量，保留哪个旧行为，如何避免把轻量 replay 写成过强结论”。

机器可读计划见 [`/ablation-plan.json`](/ablation-plan.json)，字段约束见 [`/ablation-plan.schema.json`](/ablation-plan.schema.json)。`npm run ablation:plan:check` 会检查每个消融是否绑定示例、评估指标、证据路径和验证命令。

## 七个对照

| 示例 | 变量 | 必须保留的不变量 | 验证命令 |
| --- | --- | --- | --- |
| GridWorld 陷阱规避消融 | trap avoidance 与 tie-break 规则 | 避开 `local_greedy_trap` 后仍能到达目标 | `npm run examples:gridworld:feedback`、`npm run examples:test` |
| Constraint Audit 证据升级消融 | 是否区分目录未知与已知约束冲突 | 不把未知主张伪装为已验证事实，同时阻断已知矛盾 | `npm run examples:constraint-audit:feedback`、`npm run examples:test` |
| Robot Soccer 射门通道消融 | 射门前是否检查 blocked lane | blocked shot 变成 goal，安全通道不被过度延迟 | `npm run examples:robot-soccer:feedback`、`npm run examples:test` |
| VizDoom Medikit 阈值消融 | `pickup_health` 与 `stage_area` 阈值 | 避免 `wasted_pickup`，低血量仍拾取 | `npm run examples:vizdoom-replay:feedback`、`npm run examples:reports:check` |
| Traffic Grid 下游容量消融 | downstream capacity 是否作为硬约束 | 避免 `spillback`，不永久 hold | `npm run examples:traffic-grid:feedback`、`npm run examples:test` |
| Breakout 反射预测消融 | 是否预测墙面反射后的截点 | 处理 `missed_after_wall_reflection`，保留直线球反应 | `npm run examples:breakout-replay:feedback`、`npm run examples:reports:check` |
| Ant Gait 偏航反馈消融 | yaw feedback、cadence、stance duty 是否协同启用 | 抑制 `yaw_drift`，保持向前推进 | `npm run examples:ant-gait-replay:feedback`、`npm run examples:test` |

## 使用方式

1. 先跑对应示例的 feedback 命令，确认当前报告可复现。
2. 打开 `/ablation-plan.json`，查看 `variable_under_test` 和 `expected_invariant`。
3. 只改变一个变量，记录 baseline condition、heuristic condition 和不变量。
4. 如果结果要进入论文或技术报告，同步更新 [论文蓝图](/zh-cn/appendix/paper-blueprint) 的实验章节。
5. 如果结果要进入课程作业，同步更新 [练习集](/zh-cn/appendix/exercises) 或 [研究课题](/zh-cn/appendix/research-projects)。

## 边界

当前消融计划仍服务于教学型轻量 replay。它不能替代真实 MuJoCo、Atari、VizDoom 或交通仿真环境中的系统性消融。任何对外结论都必须保留来源边界和复现状态。

```bash
npm run ablation:plan:check
npm run verify
```
