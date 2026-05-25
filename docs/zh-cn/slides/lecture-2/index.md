---
title: 第 2 讲：从案例信号到可验证实验
description: 直觉学习课程第 2 讲讲义
---

# 第 2 讲：从案例信号到可验证实验

## 本讲问题

看到一个 X 讨论、公开仓库 artifact 或应用问题后，怎样判断它能不能变成 HL 学习材料？

答案不是“观点是否新”，而是它能否被压缩成可验证闭环。学完这一讲，你应该能完成四个动作：

- 判断一条材料能支持什么结论，不能支持什么结论。
- 把材料改写成一个短小、稳定、可测试的 probe。
- 为 probe 设计自然但不充分的 baseline。
- 用 report 和 regression gate 保存学习结果。

## 从来源到实验的路径

```text
source boundary -> probe -> baseline -> heuristic patch -> feedback report -> regression gate
```

一条材料只有走完整条路径，才适合写成“已验证的 HL 示例”。在此之前，它只能作为研究线索或案例素材。

## 第一步：判断来源边界

来源边界决定了读者能相信什么。它不替代实验，只约束叙述的强度。

| 来源 | 可以支持 | 不能直接支持 | 下一步 |
| --- | --- | --- | --- |
| X 公开讨论 | 研究问题、失败现象、概念线索 | 已复现结论 | 记录作者、日期、URL 和一手程度 |
| 公开代码 artifact | 环境、策略、失败 replay | 跨场景有效性 | 固定依赖，保存最小运行命令 |
| 脱敏应用问题 | 工程需求、状态抽象、反馈形态 | 私有系统的完整结论 | 抽成最小环境或模拟任务 |
| 实验日志 | 稳定失败、可回放 trace | 未覆盖场景的泛化 | 写 probe，并保留运行输出 |

学习材料可以使用两类入口：

- [X 来源案例](/zh-cn/cases/x-signal/)：学习如何把公开讨论降级为可追踪线索。
- [来源登记](/zh-cn/appendix/source-registry)：学习如何标注“已复现、已结构化、已定位、待采集”。

## 第二步：压缩成 probe

Probe 是“最小可失败问题”。它的标准是稳定、短小、可测试。没有 probe 的材料只能作为线索保存，不能写成“已复现”。

| 案例 | Probe | 最小问题 |
| --- | --- | --- |
| Breakout | `missed_after_wall_reflection` | 当前坐标追踪不等于落点预测 |
| Ant Gait | `yaw_drift` | 固定节律不能吸收持续偏航 |
| Robot Soccer | `blocked_shot` | 单纯射门意图缺少通道检查 |
| Traffic Grid | `spillback` | 最大队列优先会破坏下游容量 |

写 probe 时先问：失败能否在一条命令、一段 replay 或一个单元测试里稳定出现？如果不能，先继续收集材料，不要急着写 patch。

## 第三步：设计 baseline

Baseline 不是故意写差的策略。它要代表一个自然但不充分的局部直觉：

- Breakout baseline 追当前球 x。
- Ant baseline 使用固定开环节律。
- Robot Soccer baseline 拿到球就射门。
- Traffic Grid baseline 放行最大上游队列。

这些 baseline 让读者看到：HL 学到的不是“更复杂的 if”，而是失败经验被重写成了可维护结构。

## 第四步：让 patch 可审查

不同领域的 patch 长得不一样：

| 类型 | 课程例子 | 审查重点 |
| --- | --- | --- |
| 阈值 | VizDoom `pickup_health` | 是否跨场景稳定 |
| 几何预测 | Breakout reflected intercept | 边界反射和速度估计 |
| 控制参数 | Ant cadence / stance duty / yaw feedback | 参数耦合与稳定性 |
| 安全约束 | Traffic downstream capacity | 吞吐与安全边界 |
| 动作前检查 | Robot Soccer shot lane | 检查器漏报/误报 |

Patch 的目标不是让代码看起来聪明，而是让下一轮智能体知道该维护哪里。

## 第五步：保存学习记忆

每个示例都生成 `experiments/*/latest.json`。它至少回答：

- baseline 为什么失败？
- heuristic 改了什么？
- 下一轮应该改哪个文件？
- 改完必须跑什么验证？

运行：

```bash
npm run examples:feedback
npm run examples:reports:check
```

如果 report 没有随着策略变化而更新，说明系统并没有形成可维护学习记忆。

## 第六步：用回归检查锁住经验

HL 也会遗忘，形式通常是工程型退化：新规则修复一个 probe，却破坏旧 probe。

统一门槛是：

```bash
npm run verify
```

它会同时检查示例测试、反馈报告、课程结构和文档构建。学习材料的可信度来自这些检查，而不是来自页面上的叙述。

## 练习：写一张 case card

选择一个未复现线索，按模板写一张 case card：

```text
Source boundary:
Probe:
Baseline:
Heuristic patch:
Feedback report:
Regression gate:
Learning note:
```

建议从 [X 来源案例](/zh-cn/cases/x-signal/) 的流体控制延展方向开始，但不要直接写成已验证结论。先找到公开代码或稳定 replay，再决定是否进入 `examples/*`。

配套阅读：[学习闭环](/zh-cn/theory/learning-loop) 与 [研究框架](/zh-cn/theory/research-framework)。
