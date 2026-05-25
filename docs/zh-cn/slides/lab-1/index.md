---
title: Lab 1：跑通 Heuristic Learning 闭环
description: 第 1 讲配套实验：运行、观察、修改并验证六个 HL 最小系统
---

# Lab 1：跑通 Heuristic Learning 闭环

本实验对应 [第 1 讲：Learning Beyond Gradients](/zh-cn/slides/lecture-1/)。目标不是训练模型，而是让你亲手看到 HL 的四个对象：策略代码、失败 probe、反馈报告和回归验证。

## 时间安排

| 时间 | 任务 | 产出 |
| --- | --- | --- |
| 0-10 分钟 | 安装依赖并跑统一验证 | `npm run verify` 通过 |
| 10-30 分钟 | 阅读六个 feedback report | 记录每个 baseline failure |
| 30-55 分钟 | 修改一个 heuristic rule | 形成一个小 patch |
| 55-75 分钟 | 补或更新一个测试 | `npm run examples:test` 通过 |
| 75-90 分钟 | 重新生成报告并复盘 | 一段实验记录 |

## 准备

```bash
npm install
npm run verify
```

如果 `verify` 失败，先不要改策略。先定位是 Python 测试、feedback report、report schema 还是 VitePress build 失败。HL 的基本纪律是：反馈通道坏了，不能开始学习。

## Step 1：观察四类失败

运行：

```bash
npm run examples:feedback
npm run examples:reports:check
```

阅读六个报告：

| 报告 | 重点观察 |
| --- | --- |
| `experiments/gridworld/latest.json` | `local_greedy_trap` 如何暴露贪心路径问题 |
| `experiments/ant-gait-replay/latest.json` | `yaw_drift` 如何暴露固定节律的连续控制问题 |
| `experiments/breakout-replay/latest.json` | `missed_after_wall_reflection` 如何暴露当前坐标追踪问题 |
| `experiments/robot-soccer/latest.json` | `blocked_shot` 如何把单场失败变成回归 probe |
| `experiments/vizdoom-replay/latest.json` | `wasted_pickup` 如何把回放经验变成阈值规则 |
| `experiments/traffic-grid/latest.json` | `spillback` 如何把交通管制经验变成容量约束 |

记录一个句子：baseline 失败在哪里，heuristic 维护了什么结构。

## Step 2：选择一个改造点

任选一个小改动，不要同时改多个系统：

| 示例 | 可选改动 | 必须保留 |
| --- | --- | --- |
| GridWorld | 增加一个陷阱或 tie-break 规则 | `local_greedy_trap` 仍然通过 |
| Ant Gait Replay | 调整 yaw feedback 或 stance duty | baseline 仍然 `yaw_drift`，heuristic 仍然 `stable_stride` |
| Breakout Replay | 调整挡板速度或反射截点控制 | baseline 仍然 `missed_after_wall_reflection` |
| Robot Soccer | 修改安全路线选择 | blocked-lane probe 仍然变成 `goal` |
| VizDoom Replay | 调整 `pickup_health` 或 `stage_area` | baseline 仍然 `wasted_pickup` |
| Traffic Grid | 修改 hold/divert 优先级 | baseline 仍然 `spillback`，heuristic 仍然 `stable_flow` |

只改策略还不够。HL 的改动应该连着测试和反馈记录一起更新。

## Step 3：写验证

先跑针对性测试：

```bash
npm run examples:test
```

再跑完整验证：

```bash
npm run verify
```

`verify` 会重新生成 feedback report，所以如果你改了策略但报告没有体现变化，说明实验记录没有跟上代码。

## Step 4：实验记录

用 5 到 8 行写清楚：

```text
改动对象：
失败 probe：
改动前行为：
改动后行为：
新增或修改的测试：
verify 结果：
剩余风险：
```

这段记录可以放进 `templates/experiment-record.md` 的结构里。关键是让下一位读者或编码智能体知道：这个规则为什么存在，什么场景不能被破坏。

## 验收标准

本 lab 完成的标准：

- 能解释 baseline failure 与 heuristic patch 的关系。
- 至少改过一个策略文件或测试文件。
- `npm run verify` 通过。
- `experiments/*/latest.json` 与代码行为一致。
- 复盘文字没有把未验证结论写成事实。

进一步的评分细则见 [课程评分与验收 Rubric](/zh-cn/appendix/rubric)。
可布置的变体题见 [练习集](/zh-cn/appendix/exercises) 的 B 组和 C 组。
