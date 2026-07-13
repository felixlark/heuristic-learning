---
title: 教师指南
description: 面向授课、组会和助教验收的 HL 课程使用说明
---

# 教师指南

本页把 Heuristic Learning 仓库转成可授课、可组会、可助教验收的交付流程。目标不是把 HL 讲成已经定型的论文体系，而是让学生看到：一个规则型智能系统如何从失败、反馈和代码更新中形成可复查的学习闭环。

如果需要明天直接开课，先看 [授课包](/zh-cn/appendix/teaching-pack)。它把 90 分钟导读、2 小时工作坊、研究讨论和 4-6 周项目课拆成讲义、demo 命令、exit ticket 和验收产物。

## 课程形态

| 形态 | 建议时长 | 适用场景 | 交付物 |
| --- | --- | --- | --- |
| 90 分钟导读 | 1 次课 | 组会、读书会、快速介绍 | 跑通一个示例，提交一张 case card |
| 2 小时工作坊 | 1 次课 | 课程实验、工程内部分享 | 跑通两个示例，提交一份实验记录 |
| 3 讲 + 2 Lab | 2-3 周 | 研究生课程、专题训练 | 完成一个新 failure mode 或一个可验证案例 |
| 4-6 周课程 | 4-6 周 | 独立 mini course | 按 [课程进度表](/zh-cn/appendix/course-schedule) 完成来源登记、实验、文档和验收报告 |

## 课前检查

授课前在干净工作区跑一遍：

```bash
npm install
npm run verify
npm run examples:gridworld
npm run examples:gridworld:feedback
```

需要打开的页面：

- [课程大纲](/zh-cn/syllabus/)
- [学习闭环](/zh-cn/theory/learning-loop)
- [可运行示例](/zh-cn/examples/)
- [来源登记](/zh-cn/appendix/source-registry)
- [练习集](/zh-cn/appendix/exercises)
- [课程评分与验收 Rubric](/zh-cn/appendix/rubric)
- [课程进度表](/zh-cn/appendix/course-schedule)
- [授课包](/zh-cn/appendix/teaching-pack)

如果 `npm run verify` 在课前失败，不要临时跳过检查。先看 [本地运行与排错](/zh-cn/appendix/local-setup)，确认失败属于依赖安装、实验报告、来源登记、manifest 还是文档构建。

## 讲授顺序

### 第 1 讲：从规则到可学习规则

配套材料：

- [学习路线](/zh-cn/stage-1/)
- [HL 基础概念](/zh-cn/stage-2/)
- [第 1 讲](/zh-cn/talk/)
- [Lab 1](/zh-cn/examples/)

课堂演示：

```bash
npm run examples:gridworld
npm run examples:gridworld:feedback
```

验收重点：学生能指出 baseline 为什么失败、feedback 写给谁、candidate update 应该修改什么代码。

### 第 2 讲：从来源到实验

配套材料：

- [第 2 讲](/zh-cn/talk/)
- [案例库](/zh-cn/cases/)
- [来源登记](/zh-cn/appendix/source-registry)
- `templates/case-card.md`

课堂演示：

```bash
npm run examples:vizdoom-replay
npm run examples:breakout-replay:feedback
```

验收重点：学生能把公开 artifact、X 来源或脱敏应用问题分成“已复现”“教学最小化”“待验证线索”，并避免把未验证材料写成事实。

### 第 3 讲：失败类型与反遗忘

配套材料：

- [第 3 讲](/zh-cn/talk/)
- [Lab 2](/zh-cn/theory/learning-loop)
- [学习闭环](/zh-cn/theory/learning-loop)
- [研究框架](/zh-cn/theory/research-framework)

课堂演示：

```bash
npm run examples:ant-gait-replay:feedback
npm run examples:traffic-grid:feedback
npm run verify
```

验收重点：学生能解释一次 heuristic patch 如何被测试、报告、案例页和来源登记共同约束，避免下一轮修改把旧失败带回来。

## 作业设计

| 作业 | 最小要求 | 加分项 |
| --- | --- | --- |
| 案例卡片 | 填写 `templates/case-card.md`，说明来源状态和 failure mode | 能给出可复现环境或数据切片 |
| 实验记录 | 填写 `templates/experiment-record.md`，包含 baseline、heuristic、report 和 test | 新增一个稳定测试覆盖反例 |
| 示例扩展 | 新增或修改 `examples/*`，提供 run、feedback、README 和 test | 接入 `npm run verify` 与 manifest |
| 理论短文 | 把案例映射到状态、动作、反馈、更新对象和度量 | 指出 HL 与 RL/DL 的边界条件 |

评分按 [课程 Rubric](/zh-cn/appendix/rubric) 执行。不要只看结果分数；必须看来源、失败模式、反馈报告和测试是否能支撑结论。
需要自动核对评分表字段时使用 [`/rubric.json`](/rubric.json) 和 `npm run rubric:check`。
题目选择可以直接使用 [练习集](/zh-cn/appendix/exercises) 的 A/B/C/D 分层结构。

## 助教验收清单

每个学生提交至少检查：

- 来源是否登记在 [来源登记](/zh-cn/appendix/source-registry) 或明确标注为待验证。
- 案例是否有 baseline failure，而不是只展示成功路径。
- 示例是否有一条最短运行命令和一条 feedback 命令。
- `experiments/*/latest.json` 是否通过 `npm run examples:reports:check`。
- 新增测试是否能被 `npm run examples:test` 跑到。
- 文档是否链接到对应示例、报告或来源。
- 最终是否通过 `npm run verify`。

## 常见课堂故障

| 故障 | 处理 |
| --- | --- |
| 示例测试失败 | 先跑对应 `npm run examples:*`，确认是策略输出变了还是测试假设过窄 |
| 报告检查失败 | 检查 `baseline`、`heuristic`、`feedback`、`candidate_update` 字段是否完整 |
| 来源登记失败 | 检查状态词、X 来源证据和 reproduced 条目的 example 路径 |
| manifest 失败 | 检查 `docs/public/course-manifest.json` 是否列出新增核心页或示例 |
| VitePress 构建失败 | 先看 dead link、frontmatter 和站内 route，不要直接删除链接 |

## 教学边界

HL 目前更适合作为研究假设与工程学习框架来讲授。Jiayi Weng 的文章和公开 artifact 是高信号来源，但仓库中的 X/私有来源案例仍然需要按来源状态分层处理。课堂上应鼓励学生提出可验证反例，而不是把 heuristics 讲成优于梯度学习的通用替代品。
