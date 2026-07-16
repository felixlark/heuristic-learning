---
title: 案例库
description: Heuristic Learning 的案例、实验入口与证据边界
---

# 案例库

案例库不是示例代码列表，也不是来源材料堆叠。它的作用是把一个真实或公开任务整理成可学习的 case card：读者先理解问题场景、来源边界和 failure mode，再决定是否进入对应的可运行示例。

## 和可运行示例的关系

| 页面 | 读者要解决的问题 | 产物 |
| --- | --- | --- |
| [可运行示例](/zh-cn/examples/) | 这个 HL 闭环怎么跑起来？ | 命令、代码、测试、`experiments/*/latest.json` |
| 案例库 | 这个例子为什么值得学？证据边界是什么？ | 环境、状态、策略表面、failure mode、来源边界 |
| 具体案例页 | 一个任务怎样被压缩成最小实验？ | case card + 对应示例入口 |

因此它们不是并列重复关系：**示例负责动手，案例负责理解任务与证据边界**。大多数案例会绑定一个示例；`X 来源案例` 例外，它用于训练来源判断，只有被复核并转成最小环境后，才会进入 runnable example。

## 阅读模板

每个案例都按同一组问题阅读：

1. 环境是什么？
2. 状态如何表示？
3. 策略如何写成代码或控制结构？
4. 失败信号是什么？
5. 反馈从哪里来？
6. 更新对象是什么？
7. 如何验证没有退化？

案例到来源、示例、学习成果和验证命令的完整对照见 [案例矩阵](/zh-cn/appendix/case-registry)。

## 学习顺序

| 顺序 | 案例层级 | 读什么 | 跑什么 | 读完应能回答 |
| --- | --- | --- | --- | --- |
| 0 | 最小闭环 | [可运行示例](/zh-cn/examples/) 中的 GridWorld | `npm run examples:gridworld:feedback` | signal、probe、patch、report 是什么 |
| 1 | 公开 artifact：离散控制 | [Breakout 案例](/zh-cn/cases/breakout/) | `npm run examples:breakout-replay:feedback` | 轨迹预测怎样变成代码化经验 |
| 2 | 公开 artifact：感知阈值 | [VizDoom 案例](/zh-cn/cases/vizdoom/) | `npm run examples:vizdoom-replay:feedback` | 视觉线索怎样变成可测试阈值 |
| 3 | 公开 artifact：连续控制 | [Ant Gait 案例](/zh-cn/cases/ant-gait/) | `npm run examples:ant-gait-replay:feedback` | 控制器参数怎样成为学习对象 |
| 4 | 应用场景：动作前提 | [机器人足球案例](/zh-cn/cases/robot-soccer/) | `npm run examples:robot-soccer:feedback` | 规则系统怎样暴露 blocked-lane failure |
| 5 | 应用场景：系统约束 | [交通模拟案例](/zh-cn/cases/traffic-simulation/) | `npm run examples:traffic-grid:feedback` | 容量约束怎样进入策略维护 |
| 6 | 研究假设：事实审计 | [事实约束审计案例](/zh-cn/cases/constraint-audit/) | `npm run examples:constraint-audit:feedback` | 约束冲突与未知主张为何必须分开处理 |
| 7 | 来源线索 | [X 来源案例](/zh-cn/cases/x-signal/) | `npm run x:sources:check` | 一条公开讨论何时只能算线索，何时能变成案例 |
| 8 | 来源转研究探针 | [视觉先验案例](/zh-cn/cases/visual-prior/) | `npm run examples:shape-from-shading` | 如何把“默认设定影响解释”写成可检查 heuristic |

## 三类案例

### 公开 Artifact 案例

这一组来自 Jiayi Weng 的 [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/) 与 [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients)。它们用于学习“公开代码 artifact 如何被压缩成轻量 replay”。

| 案例 | 对应示例 | 学习重点 |
| --- | --- | --- |
| [Breakout](/zh-cn/cases/breakout/) | `examples/breakout-replay/` | side-wall reflection、轨迹预测、代码化经验记忆 |
| [VizDoom](/zh-cn/cases/vizdoom/) | `examples/vizdoom-replay/` | medikit staging、感知阈值、回放反馈 |
| [Ant Gait](/zh-cn/cases/ant-gait/) | `examples/ant-gait-replay/` | CPG、stance duty、yaw feedback、连续控制结构 |

### 应用场景案例

这一组来自脱敏后的应用问题。它们用于学习“已有规则系统如何暴露一个可维护 failure mode”。

| 案例 | 对应示例 | 学习重点 |
| --- | --- | --- |
| [机器人足球](/zh-cn/cases/robot-soccer/) | `examples/robot-soccer/` | blocked-lane、动作前提、规则冲突检查 |
| [交通模拟](/zh-cn/cases/traffic-simulation/) | `examples/traffic-grid/` | downstream spillback、容量约束、系统安全边界 |
| [事实约束审计](/zh-cn/cases/constraint-audit/) | `examples/constraint-audit/` | 已知约束冲突、未知主张、外部证据升级 |

### 来源线索案例

| 案例 | 对应示例 | 学习重点 |
| --- | --- | --- |
| [X 来源案例](/zh-cn/cases/x-signal/) | 部分线索已转成研究探针 | 一手来源、二手转述、公开 artifact 和待复核主张的边界 |
| [视觉先验案例](/zh-cn/cases/visual-prior/) | `examples/shape-from-shading/` | 欠定输入、光照先验、场景线索与可证伪边界 |

X 来源案例不是第六个 runnable case；它是来源训练页。它帮助读者判断一条公开讨论如何进入案例库：先成为线索，再绑定来源状态，最后才可能变成可运行示例。视觉先验探针是其中一条线索完成独立文献核验后的研究性产物，不计入 v0.1 的七个核心示例。

## 验证

案例矩阵由下面命令检查：

```bash
npm run cases:check
```

如果一个案例已经绑定示例，还应能通过：

```bash
npm run examples:feedback
npm run examples:reports:check
npm run examples:test
```
