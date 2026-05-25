---
title: 学习闭环
description: Heuristic Learning 从案例信号到可维护系统的六步流程
---

# 学习闭环

HL 的课程目标不是让读者记住“启发式规则有用”，而是让读者能重复执行一套学习闭环：从一个失败信号开始，把经验压缩成可运行、可测试、可复盘的软件结构。

本仓库采用六步闭环：

```text
signal -> probe -> baseline -> patch -> report -> regression
```

## 1. Signal：找到值得学习的信号

Signal 可以来自 X 线程、公开仓库 artifact、飞书消息、日志、视频回放或一次失败测试。进入课程前，必须先回答：

| 问题 | 说明 |
| --- | --- |
| 来源是否可追溯 | 至少有 URL、内部消息线索或文件路径 |
| 主张是否可拆解 | 能否转成状态、动作、反馈和更新对象 |
| 边界是否清楚 | 哪些内容已经验证，哪些只是研究假设 |

例子：[X 线索案例](/zh-cn/cases/x-signal/) 把 Jiayi 原帖和中文转述拆开记录；[来源登记](/zh-cn/appendix/source-registry) 再标注它们在本仓库里的状态。

## 2. Probe：把失败压缩成最小场景

Probe 是课程仓库和普通科普文章的分界线。一个好 probe 应该小到读者能读完，又能稳定暴露失败。

| Probe | 暴露的问题 | 对应示例 |
| --- | --- | --- |
| `local_greedy_trap` | 贪心路径会走进已知陷阱 | `examples/heuristic-gridworld/` |
| `yaw_drift` | 固定 gait 节律无法吸收持续偏航扰动 | `examples/ant-gait-replay/` |
| `missed_after_wall_reflection` | 追当前球坐标会错过反射后的截点 | `examples/breakout-replay/` |
| `blocked_shot` | 只看球门距离会忽略射门通道被挡 | `examples/robot-soccer/` |
| `wasted_pickup` | 过早拾取 medikit 会浪费未来价值 | `examples/vizdoom-replay/` |
| `spillback` | 只看上游队列会压爆下游容量 | `examples/traffic-grid/` |

新增案例如果没有 probe，先不要写成主线章节。它最多只能留在来源登记或案例待办里。

## 3. Baseline：保留一个可解释的失败策略

Baseline 不是为了显得 heuristic 更强，而是为了固定“系统到底学会了什么”。课程示例的 baseline 应该满足三个条件：

- 行为简单，读者能在 1 分钟内解释。
- 会稳定触发 probe，而不是偶然失败。
- 失败原因能写进 `experiments/*/latest.json`。

如果 baseline 太弱，读者学不到边界；如果 baseline 太复杂，读者看不到 heuristic patch 的作用。

## 4. Patch：只修改可维护对象

HL 的 patch 不等同于“加一条 if”。连续控制中的 patch 可能是 stance duty 和 yaw feedback，游戏控制中的 patch 可能是轨迹预测器，工程系统中的 patch 可能是容量阈值。

| Patch 类型 | 例子 | 维护风险 |
| --- | --- | --- |
| 阈值 | VizDoom `pickup_health` | 阈值漂移、跨场景失效 |
| 几何预测 | Breakout 反射截点 | 边界条件和速度估计错误 |
| 控制参数 | Ant gait cadence / stance duty | 参数耦合、稳定性退化 |
| 安全约束 | Traffic downstream capacity | 过度保守、吞吐下降 |
| 动作前检查 | Robot Soccer shot lane | 检查器漏报或误报 |

一个 patch 只有在它能被 review、被测试、被记录时，才算进入 HL 闭环。

## 5. Report：让反馈成为智能体可读的证据

每个主线示例都必须生成 `experiments/*/latest.json`。报告不是附属日志，而是下一轮智能体更新的输入。

报告至少包含：

- `policies`：baseline 与 heuristic 对照。
- `feedback`：本轮观察到的维护约束。
- `candidate_update.target`：下一轮应该改哪个文件。
- `candidate_update.verification`：修改后必须跑哪条验证命令。

这使得 HL 的“学习记忆”不只存在于人的脑子里，也存在于可被工具读取的结构化记录里。

## 6. Regression：把新经验锁住

最后一步是回归验证。一个 HL patch 不能只证明当前场景成功，还要证明旧 probe 没有退化。

本仓库的统一门槛是：

```bash
npm run verify
```

它会依次执行：

1. 主题代码 lint。
2. 所有 Python 示例测试。
3. 重新生成 feedback reports。
4. 检查 report schema。
5. 检查课程页面、示例、脚本、报告和 syllabus 是否对齐。
6. 构建 VitePress 文档站。

## 课程化要求

把一个案例写进主线课程前，必须能填完这张表：

| 字段 | 说明 |
| --- | --- |
| Signal | 来源 URL、消息线索或公开 artifact |
| Probe | 可复现的最小失败 |
| Baseline | 稳定触发失败的简单策略 |
| Patch | 可审查的 heuristic 更新对象 |
| Report | 结构化 feedback report |
| Regression | 单元测试与 `npm run verify` |
| Course note | 案例页或示例页解释 |

这个表是新增章节的准入标准。没有 runnable example 的材料可以进入案例库，但不能宣称“已复现”；没有来源登记的材料不能进入主线结论。
