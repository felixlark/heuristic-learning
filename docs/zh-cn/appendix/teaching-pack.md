---
title: 授课包
description: Heuristic Learning 讲义、演示、课堂问题和验收材料清单
---

# 授课包

本页面向教师、助教和组会主持人，把已有讲义转成可执行课堂包。它回答一个更具体的问题：如果明天要讲 HL，应该打开哪些页面、跑哪些命令、问哪些问题、收什么产物。

机器可读授课包见 [`/teaching-pack.json`](/teaching-pack.json)，字段约束见 [`/teaching-pack.schema.json`](/teaching-pack.schema.json)。`npm run teaching:pack:check` 会检查每个课堂包对应的讲义、阅读材料、命令、交付物和验收项是否仍然存在。

实际授课时配合 [讲者备注](/zh-cn/appendix/speaker-notes) 使用。`/speaker-notes.json` 给出每讲的开场问题、demo 节点、讨论题、常见误解和 exit ticket，`npm run speaker:notes:check` 会检查它们仍然绑定当前讲义。

## 使用原则

| 原则 | 执行方式 |
| --- | --- |
| 先验证环境 | 每次课前先跑 `npm run verify`，不要在坏反馈通道上讲策略更新 |
| 每课一个核心问题 | 不把所有案例塞进同一节课；围绕一个 failure mode 或研究命题展开 |
| 演示必须可复现 | demo 命令必须是 `package.json` 里的脚本 |
| 课后必须有产物 | exit ticket、实验记录、case card 或 Rubric 自评至少交一种 |

## 课堂包总览

| 包 | 场景 | 时长 | Demo | 交付物 |
| --- | --- | --- | --- | --- |
| TP0 快速导读 | 组会/reading group | 90 分钟 | `npm run examples:gridworld:feedback` | exit ticket |
| TP1 工作坊 | 工程训练/课程实验 | 2 小时 | `npm run examples:feedback` | experiment record |
| TP2 研究讨论 | 研究生专题 | 2-3 周 | `npm run claims:registry:check` | claim review |
| TP3 期末项目 | mini course/capstone | 4-6 周 | `npm run verify` | project report 或 PR |

## TP0：90 分钟快速导读

目标：让听众理解 HL 不是“手写规则”，而是反馈驱动的软件结构维护。

课堂流程：

| 时间 | 内容 | 材料 |
| --- | --- | --- |
| 0-10 分钟 | 说明问题背景 | [第 1 讲](/zh-cn/slides/lecture-1/) |
| 10-30 分钟 | 跑 GridWorld | [可运行示例](/zh-cn/examples/) |
| 30-55 分钟 | 解释 feedback report | `experiments/gridworld/latest.json` |
| 55-75 分钟 | 对照 HL / RL / DL | [从 RL/DL 到 HL](/zh-cn/stage-3/) |
| 75-90 分钟 | exit ticket | [术语表](/zh-cn/appendix/glossary) |

Demo：

```bash
npm run examples:gridworld
npm run examples:gridworld:feedback
```

Exit ticket：

```text
HL 的更新对象是什么？
baseline failure 是什么？
feedback report 写给谁？
下一轮应该跑什么验证？
```

## TP1：2 小时工作坊

目标：让参与者跑完六个示例，选择一个小改动，并用测试和报告证明没有破坏旧行为。

课堂流程：

| 时间 | 内容 | 材料 |
| --- | --- | --- |
| 0-15 分钟 | 环境验证 | [本地运行与排错](/zh-cn/appendix/local-setup) |
| 15-35 分钟 | 阅读六个 failure mode | [学习单元矩阵](/zh-cn/appendix/learning-units) |
| 35-70 分钟 | 分组修改一个策略或测试 | [Lab 1](/zh-cn/slides/lab-1/) |
| 70-100 分钟 | 重新生成反馈报告 | [实验协议](/zh-cn/appendix/benchmark-protocol) |
| 100-120 分钟 | Rubric 自评 | [课程 Rubric](/zh-cn/appendix/rubric) |

Demo：

```bash
npm run verify
npm run examples:feedback
npm run examples:reports:check
```

交付物：一份 `templates/experiment-record.md` 风格的实验记录。

## TP2：研究讨论

目标：把 HL 当前主张拆成证据、反例和下一步实验，而不是把未发表思想讲成定论。

课堂流程：

| 环节 | 内容 | 材料 |
| --- | --- | --- |
| 读前 | 阅读 Jiayi 文章和课程阅读指南 | [文献阅读指南](/zh-cn/appendix/reading-guide) |
| 讨论 1 | 命题是否能被示例支撑 | [研究命题](/zh-cn/theory/research-propositions) |
| 讨论 2 | 现有 replay 的边界 | [研究路线图](/zh-cn/appendix/research-roadmap) |
| 讨论 3 | 如何从 X/脱敏应用问题变成 case card | [来源登记](/zh-cn/appendix/source-registry) |
| 收尾 | 形成一个可反驳实验设计 | [研究课题](/zh-cn/appendix/research-projects) |

Demo：

```bash
npm run source:registry:check
npm run claims:registry:check
npm run paper:blueprint:check
```

交付物：一页 `templates/claim-review.md` 风格的 claim review，说明一个命题的证据、缺口、反驳路径和下一步 probe。

## TP3：4-6 周项目课

目标：让学生从来源线索推进到可验证 HL 项目，交付 case card、runnable example、feedback report、test 或课程材料。

执行方式：

- 按 [课程进度表](/zh-cn/appendix/course-schedule) 安排周次。
- 用 [学习单元矩阵](/zh-cn/appendix/learning-units) 控制每周“读、跑、改、复盘”。
- 用 [贡献与研究协议](/zh-cn/appendix/contribution-protocol) 控制 PR 或报告证据。
- 用 [完成度审计](/zh-cn/appendix/completion-audit) 做最终检查。

Demo：

```bash
npm run learning:units:check
npm run teaching:pack:check
npm run verify
```

交付物：最终项目报告或 PR，必须包含来源状态、baseline failure、heuristic patch、feedback report、测试和 `npm run verify` 结果。

## 课前总检查

每次授课前至少运行：

```bash
npm run teaching:registry:check
npm run learning:units:check
npm run teaching:pack:check
npm run verify
```

这四条命令分别确认讲义、学习单元、授课包和全仓库验证没有漂移。
