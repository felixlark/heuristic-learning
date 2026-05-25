---
title: 第 2 讲：从案例信号到可验证实验
description: 直觉学习课程第 2 讲讲义
---

# 第 2 讲：从案例信号到可验证实验

## Slide 1：问题

看到一个 X 帖、仓库 artifact 或内部应用线索后，怎样判断它能不能进入 HL 课程主线？

答案不是“观点是否新”，而是它能否被压缩成可验证闭环：

```text
signal -> probe -> baseline -> patch -> report -> regression
```

## Slide 2：Signal 不是结论

信号只能说明“这里可能有学习对象”。它必须先经过来源登记：

| 来源 | 进入课程前要问的问题 |
| --- | --- |
| X 原帖 | 作者、日期、URL、是否一手来源 |
| 公开代码 | artifact 路径、依赖、可复现程度 |
| 飞书线索 | 是否只是内部需求，能否抽成最小环境 |
| 实验日志 | 失败是否稳定，是否能保存 trace |

课堂示例：

- [X 线索案例](/zh-cn/cases/x-signal/)：区分 Jiayi 原帖和二手中文转述。
- [来源登记](/zh-cn/appendix/source-registry)：标注“已复现、已结构化、已定位、待采集”。

## Slide 3：Probe 是课程化的关键

一个案例进入主线前，必须先变成一个最小 probe。

| 案例 | Probe | 最小问题 |
| --- | --- | --- |
| Breakout | `missed_after_wall_reflection` | 当前坐标追踪不等于落点预测 |
| Ant Gait | `yaw_drift` | 固定节律不能吸收持续偏航 |
| Robot Soccer | `blocked_shot` | 单纯射门意图缺少通道检查 |
| Traffic Grid | `spillback` | 最大队列优先会破坏下游容量 |

Probe 的标准是稳定、短小、可测试。没有 probe 的材料只能留在案例库，不能写成“已复现”。

## Slide 4：Baseline 必须有教学价值

Baseline 不是故意写差的策略。它要代表一个自然但不充分的局部直觉：

- Breakout baseline 追当前球 x。
- Ant baseline 使用固定开环节律。
- Robot Soccer baseline 拿到球就射门。
- Traffic Grid baseline 放行最大上游队列。

这些 baseline 让读者看到：HL 学到的不是“更复杂的 if”，而是失败经验被重写成了可维护结构。

## Slide 5：Patch 要能被审查

不同领域的 patch 长得不一样：

| 类型 | 本仓库例子 | 审查重点 |
| --- | --- | --- |
| 阈值 | VizDoom `pickup_health` | 是否跨场景稳定 |
| 几何预测 | Breakout reflected intercept | 边界反射和速度估计 |
| 控制参数 | Ant cadence / stance duty / yaw feedback | 参数耦合与稳定性 |
| 安全约束 | Traffic downstream capacity | 吞吐与安全边界 |
| 动作前检查 | Robot Soccer shot lane | 检查器漏报/误报 |

Patch 的目标不是让代码看起来聪明，而是让下一轮智能体知道该维护哪里。

## Slide 6：Report 是学习记忆

每个示例都生成 `experiments/*/latest.json`。它至少回答：

- baseline 为什么失败？
- heuristic 改了什么？
- 下一轮应该改哪个文件？
- 改完必须跑什么验证？

课堂命令：

```bash
npm run examples:feedback
npm run examples:reports:check
```

如果 report 没有随着策略变化而更新，说明系统并没有形成可维护学习记忆。

## Slide 7：Regression 把经验锁住

HL 也会遗忘，形式通常是工程型退化：新规则修复一个 probe，却破坏旧 probe。

统一门槛：

```bash
npm run verify
```

它会同时检查示例测试、反馈报告、课程结构和 VitePress build。课程仓库的可信度来自这些检查，而不是来自页面上的叙述。

## Slide 8：课堂练习

选择一个未复现线索，按模板写一张 case card：

```text
Signal:
Probe:
Baseline:
Patch:
Report:
Regression:
Course note:
```

建议从 [X 线索案例](/zh-cn/cases/x-signal/) 的流体控制延展方向开始，但不要直接写成已验证结论。先找到公开代码或稳定 replay，再决定是否进入 `examples/*`。

配套阅读：[学习闭环](/zh-cn/theory/learning-loop) 与 [研究框架](/zh-cn/theory/research-framework)。
