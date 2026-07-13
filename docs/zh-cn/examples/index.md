---
title: 可运行示例
description: Heuristic Learning 的最小动手实验
---

# 可运行示例

可运行示例是动手入口：它们回答“怎么运行、怎么生成反馈报告、怎么验证没有退化”。[案例库](/zh-cn/cases/) 回答另一个问题：这个任务为什么值得学、来源边界是什么、最小实验保留了原问题的哪一部分。

当前 v0.1 提供六个纯 Python 示例。GridWorld 是入门闭环；另外五个示例分别绑定案例库中的具体案例。这里的 `VizDoom Replay`、`Breakout Replay` 和 `Ant Gait Replay` 都是轻量 replay：它们保留 failure probe、策略更新对象和测试路径，不把学习门槛绑定到真实 MuJoCo、Atari 或 VizDoom 环境。

## 示例和案例怎么配合

| 示例 | 对应案例 | 关系 |
| --- | --- | --- |
| GridWorld | 无独立案例页 | 最小闭环，用来先理解 signal -> probe -> patch -> report |
| Breakout Replay | [Breakout 案例](/zh-cn/cases/breakout/) | 公开 Atari artifact 的轻量 replay |
| VizDoom Replay | [VizDoom 案例](/zh-cn/cases/vizdoom/) | 公开 VizDoom artifact 的轻量 replay |
| Ant Gait Replay | [Ant Gait 案例](/zh-cn/cases/ant-gait/) | 公开 MuJoCo Ant artifact 的轻量 replay |
| Robot Soccer | [机器人足球案例](/zh-cn/cases/robot-soccer/) | 脱敏应用场景的最小 blocked-lane 环境 |
| Traffic Grid | [交通模拟案例](/zh-cn/cases/traffic-simulation/) | 脱敏应用场景的最小 spillback 环境 |

每个示例目录都包含一个 `README.md`，其中固定列出 learning target、运行命令、反馈报告路径和测试路径。读者可以从本页按顺序跑，也可以先读案例页，再回到对应示例动手。

机器可读示例矩阵见 [`/example-registry.json`](/example-registry.json)，字段约束见 [`/example-registry.schema.json`](/example-registry.schema.json)。`npm run examples:registry:check` 会确认 registry、package scripts、README、报告、测试和课程链接没有漂移。
六个示例的 baseline/heuristic 当前结果汇总见 [Benchmark 结果摘要](/zh-cn/appendix/benchmark-results)，由 `npm run benchmark:summary:check` 检查。

## 0. 最小闭环

### GridWorld Heuristic System

位置：

```text
examples/heuristic-gridworld/
```

运行：

```bash
npm run examples:gridworld
```

生成反馈报告：

```bash
npm run examples:gridworld:feedback
```

测试：

```bash
npm run examples:test
npm run verify
```

## 你会看到什么

这个示例中，agent 需要从起点走到目标点，同时避开陷阱。`baseline` 策略只贪心靠近目标，`heuristic` 策略额外维护一组可读规则：

- 如果下一步会撞墙，换方向。
- 如果下一步会进入已知陷阱，选择次优安全动作。
- 如果两个动作距离目标一样，优先选择历史上更稳定的动作。

这些规则不是为了证明“规则比学习强”，而是为了展示 HL 的基本对象：策略代码、反馈记录、测试与可维护的更新点。

## 反馈报告如何使用

`examples:gridworld:feedback` 会生成 `experiments/gridworld/latest.json`。这个文件模拟一次最小 HL 实验记录：

- 环境配置是什么。
- baseline 与 heuristic 的结果如何。
- `local_greedy_trap` 这样的 probe 如何隔离“平均奖励看不出来”的失败模式。
- 本轮反馈指出了哪些维护约束。
- 下一次智能体更新应该改哪个文件、跑哪条验证命令。

JSON 报告让实验结果可以被学生、研究者和自动化检查脚本稳定复查。

## 建议练习

1. 在 `examples/heuristic-gridworld/policies.py` 中添加一个新陷阱规避规则。
2. 运行 `npm run examples:test`，确认旧场景没有退化。
3. 修改 `examples/heuristic-gridworld/run.py` 的地图，观察规则是否仍然有效。
4. 把实验结果写回案例笔记：规则解决了什么，是否引入了新冲突。

## 1. 应用场景最小环境

### Robot Soccer Blocked Lane

位置：

```text
examples/robot-soccer/
```

运行：

```bash
npm run examples:robot-soccer
```

生成反馈报告：

```bash
npm run examples:robot-soccer:feedback
```

这个示例来自机器人足球案例：baseline 拿到球后看到球门距离近，就直接射门；heuristic policy 会先检查射门通道是否被对手挡住，如果挡住就先换到安全路线。

它展示了 HL 的一个核心教学点：**平均表现不是唯一反馈**。一个明确的 blocked-lane probe 能把“规则为什么需要维护”暴露出来，并给下一轮修改留下证据。

### Traffic Grid Downstream Spillback

位置：

```text
examples/traffic-grid/
```

运行：

```bash
npm run examples:traffic-grid
```

生成反馈报告：

```bash
npm run examples:traffic-grid:feedback
```

这个示例把交通控制问题压缩成一个最小网格：主路和支路都想放行，但下游路段已经接近容量上限。

baseline policy 只看上游队列大小，所以会优先放行主路并造成 `spillback`。heuristic policy 把下游容量作为硬约束，先等待或分流，再恢复放行，最终达到 `stable_flow`。

它展示了 HL 在工程系统里的另一个常见对象：学习不是只改变“选择哪个动作”，还要把管制经验、容量阈值和 replay probe 固化成可维护规则。

## 2. 公开 Artifact 轻量 Replay

### Breakout Replay Wall Reflection

位置：

```text
examples/breakout-replay/
```

运行：

```bash
npm run examples:breakout-replay
```

生成反馈报告：

```bash
npm run examples:breakout-replay:feedback
```

这个示例改写自 `learning-beyond-gradients` 的 `atari/breakout/heuristic_breakout.py`。原始 artifact 会从 RAM 或 RGB 画面解码球和挡板位置，估计球速，并把轨迹按侧墙反射到挡板高度。

课程版只保留一个 probe：baseline 追当前球 x，球撞右墙后反弹到左侧，导致 `missed_after_wall_reflection`；heuristic policy 提前预测反射后的截点，得到 `intercepted`。

### VizDoom Replay Medikit Staging

位置：

```text
examples/vizdoom-replay/
```

运行：

```bash
npm run examples:vizdoom-replay
```

生成反馈报告：

```bash
npm run examples:vizdoom-replay:feedback
```

这个示例改写自 Jiayi Weng `learning-beyond-gradients` 仓库中的 `vizdoom/heuristic_vizdoom_d1_cv.py`。原始 artifact 使用 EnvPool 与 OpenCV 在 VizDoom D1 中识别 medikit，并在血量仍然较高时先停在 medikit 附近，等拾取有奖励价值时再前进。

轻量 replay 保留同一个策略要点，但移除了重型依赖：`ReplayWorld` 只记录血量、medikit 可见性、面积和偏移量。baseline 会立刻吃掉 medikit，得到 `wasted_pickup`；heuristic policy 会等待血量低于阈值后再拾取，得到 `valued_pickup`。

这个示例适合练习把视觉游戏 artifact 转成可运行实验：先保留可解释的 replay/probe，再逐步替换成真实环境。

### Ant Gait Replay Yaw Stabilization

位置：

```text
examples/ant-gait-replay/
```

运行：

```bash
npm run examples:ant-gait-replay
```

生成反馈报告：

```bash
npm run examples:ant-gait-replay:feedback
```

这个示例改写自 `learning-beyond-gradients` 的 `mujoco/ant/heuristic_ant.py`。原始 artifact 使用 rhythmic CPG、PD tracking、速度自适应、姿态/航向反馈，并可叠加短时域 MuJoCo rollout 搜索 residual action。

课程版抽出一个最小 gait replay：baseline 使用固定开环节律，遇到持续 yaw 扰动后得到 `yaw_drift`；heuristic policy 同时维护 `phase_increment`、`stance_duty` 和 `yaw_feedback`，最终得到 `stable_stride`。它展示了 HL 在连续控制里的形态：可维护对象不是一条离散 if 规则，而是一组可审计的控制参数和反馈通道。

## 统一验证

所有主线示例都纳入统一验证入口：

```bash
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
npm run course:structure:check
npm run verify
```

`examples:feedback` 会重新生成六个 `experiments/*/latest.json`；`examples:reports:check` 会检查每个报告是否保留 baseline/heuristic 对照、feedback 和 candidate update。这样课程内容、实验代码和研究记录不会各自漂移。
报告字段约束见 [`/experiment-report.schema.json`](/experiment-report.schema.json)，用于说明主线实验报告至少需要保留的结构。

完成一次完整练习可以参考 [Lab 1：跑通 Heuristic Learning 闭环](/zh-cn/examples/)。
