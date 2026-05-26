---
title: 课程地图
description: Heuristic Learning 的统一学习主线、实验入口和验证路径
---

# 课程地图

本页把 HL 收束成一份连续学习材料。读者不需要按身份分流；从概念开始，跑通最小闭环，阅读案例，再完成一次可验证的 heuristic update。

## 一份学习材料

| 顺序 | 学习目标 | 先读 | 再做 | 验收 |
| --- | --- | --- | --- | --- |
| 1. 建立概念 | 理解 HL 的更新对象不是权重，而是软件结构 | [学习路线](/zh-cn/stage-1/)、[HL 基础概念](/zh-cn/stage-2/) | 写出 feedback、update target、verification 的定义 | 一页术语笔记 |
| 2. 跑通闭环 | 观察 baseline failure 如何变成 feedback report | [学习闭环](/zh-cn/theory/learning-loop)、[可运行示例](/zh-cn/examples/) | `npm run examples:gridworld`、`npm run examples:gridworld:feedback` | GridWorld 实验记录 |
| 3. 对照理论 | 区分 RL、DL 和 HL 的更新机制 | [从 RL/DL 到 HL](/zh-cn/stage-3/)、[研究框架](/zh-cn/theory/research-framework) | 把一个案例映射到 state、action、feedback、patch、regression | 一张闭环图 |
| 4. 阅读案例 | 学会处理公开 artifact、X 来源和脱敏应用问题 | [案例库](/zh-cn/cases/)、[来源登记](/zh-cn/appendix/source-registry) | 写一张 case card，标注来源状态和边界 | case card |
| 5. 修改验证 | 只改一个策略点，并确认旧经验没有退化 | [代码导览](/zh-cn/appendix/code-tour)、[Lab 1](/zh-cn/slides/lab-1/) | `npm run examples:test`、`npm run examples:feedback` | 更新后的 report 与测试结果 |
| 6. 复盘扩展 | 把一次更新写成可反驳的研究问题 | [Lab 2](/zh-cn/slides/lab-2/)、[研究命题](/zh-cn/theory/research-propositions) | `npm run verify`，再写反遗忘复盘 | anti-forgetting checklist |

## 概念到实验

| 阶段 | 要回答的问题 | 进入下一步的证据 |
| --- | --- | --- |
| HL 基础概念 | 更新对象是不是软件结构，而不是权重？ | 能说明 feedback、update target、verification |
| 学习闭环 | 失败如何变成可维护的规则或测试？ | 能画出一次 baseline -> patch -> report |
| RL/DL/HL 对照 | 这个问题适合改参数、改策略，还是改系统结构？ | 能说清更新对象和反馈来源 |
| 可运行示例 | 规则修改能否被命令复现？ | 有实验报告和测试结果 |
| 案例来源 | 公开 artifact、X 线索和脱敏案例边界是否清楚？ | 有来源状态和 case card |
| 反馈报告 | 报告是否能指导下一轮维护？ | 有失败模式、候选修改和风险说明 |
| 测试与回归 | 新规则是否破坏旧经验？ | 有 regression guard |
| 复盘与研究问题 | 这次更新能否形成可反驳问题？ | 有证据、反例和下一步实验 |

这张图说明课程的核心约束：理论页必须能落到示例或案例，示例必须能生成报告，报告必须能指导下一轮维护，维护必须被测试和复盘约束。

## 示例到练习

| 示例 | 适合学习的概念 | 推荐练习 |
| --- | --- | --- |
| GridWorld | 最小 HL 闭环、局部贪心失败 | A1、B1、C1 |
| Robot Soccer | 动作前提、blocked-lane probe | B2、C4、D3 |
| VizDoom Replay | 资源时机、视觉 artifact 轻量化 | B3、C3、D2 |
| Traffic Grid | 系统容量、安全约束 | B6、C2、D3 |
| Breakout Replay | 物理预测、replay probe | B4、C2、D2 |
| Ant Gait Replay | 连续控制、控制参数可审查性 | B5、C4、D2 |

练习编号见 [练习集](/zh-cn/appendix/exercises)。每个练习都要说明 baseline failure、heuristic patch、反馈报告和验证命令。

## 发布前检查

学习材料和示例更新后使用同一条命令：

```bash
npm run verify
```

它会执行：

1. VitePress theme lint。
2. 所有 Python 示例测试。
3. 六个 feedback report 重新生成。
4. 实验报告结构检查。
5. 来源登记检查。
6. course manifest 检查。
7. 课程结构检查。
8. 本地文档路由预检。
9. VitePress build。

局部排错可以使用 [本地运行与排错](/zh-cn/appendix/local-setup)，但最终验收不能绕过 `npm run verify`。

## 数据入口

面向复查、学习组织和自动化检查的入口：

- [`/course-manifest.json`](/course-manifest.json)：核心页面、示例、public resources 和 CI gate。
- [`/course-manifest.schema.json`](/course-manifest.schema.json)：manifest 字段约束。
- [`/case-registry.json`](/case-registry.json)：案例页到来源状态、示例、学习成果和验证命令的映射。
- [`/learning-units.json`](/learning-units.json)：章节级读、跑、改、复盘闭环。
- [`/learning-outcomes.json`](/learning-outcomes.json)：能力目标到学习单元、练习、Rubric 和验证命令的映射。
- [`/checkpoint-registry.json`](/checkpoint-registry.json)：每个学习单元的阶段自测、证据和通过条件。
- [`/evaluation-metrics.json`](/evaluation-metrics.json)：研究评估维度、证据路径和验证命令。
- [`/concept-graph.json`](/concept-graph.json)：核心概念到命题、示例、讲义和验证命令的映射。
- [`/rubric.json`](/rubric.json)：评分模块、权重和验收证据。
- [`/exercise-registry.json`](/exercise-registry.json)：练习题、输入材料、示例、交付物和验收命令。
- [`/contribution-contract.json`](/contribution-contract.json)：贡献类型、证据字段、必备路径、验证命令和禁止材料。
- [`/reproducibility-checklist.json`](/reproducibility-checklist.json)：环境、示例、命题、教学、贡献和站点复现检查。
- [`/experiment-report.schema.json`](/experiment-report.schema.json)：实验报告字段约束。
- [`/llms.txt`](/llms.txt)：面向自动化阅读的高信号入口。

阶段性完成判断见 [完成度审计](/zh-cn/appendix/completion-audit)，不要只用单个测试或本地 HTTP 200 代替完整证据链。

这些入口让读者可以从网页、命令和结构化数据三种方式复查同一套课程证据。
