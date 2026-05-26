---
title: 课程进度表
description: Heuristic Learning 4-6 周课程的每周阅读、实验、讲义和验收安排
---

# 课程进度表

本页给出一条 4-6 周的学习安排，适合研究生专题课、实验室 reading group 或工程团队内部训练。每周都同时包含阅读、代码、反馈报告和验收证据，避免学习只停留在概念讨论。

## 使用方式

教师可以按 4 周压缩版或 6 周完整版执行：

| 版本 | 节奏 | 适用场景 |
| --- | --- | --- |
| 4 周压缩版 | 每周 1 次讲授 + 1 次 lab | 组会专题、工程训练营 |
| 6 周完整版 | 每周 1 次讨论 + 1 次作业复盘 | 研究生课程、长期 reading group |

无论采用哪个版本，最终验收都必须回到同一条命令：

```bash
npm run verify
```

一次性导读、2 小时工作坊和项目课的可执行课堂包见 [授课包](/zh-cn/appendix/teaching-pack)。

## 6 周完整版

| 周次 | 主题 | 阅读 | 动手命令 | 验收产物 |
| --- | --- | --- | --- | --- |
| Week 0 | 环境与课程地图 | [课程地图](/zh-cn/course-map/)、[本地运行与排错](/zh-cn/appendix/local-setup) | `npm install`、`npm run verify` | 本地验证截图或日志摘要 |
| Week 1 | 从规则到学习闭环 | [学习路线](/zh-cn/stage-1/)、[HL 基础概念](/zh-cn/stage-2/)、[第 1 讲](/zh-cn/slides/lecture-1/) | `npm run examples:gridworld`、`npm run examples:gridworld:feedback` | GridWorld 实验记录 |
| Week 2 | 来源、case card 与 X/公开 artifact | [第 2 讲](/zh-cn/slides/lecture-2/)、[来源登记](/zh-cn/appendix/source-registry)、[引用与署名](/zh-cn/appendix/citation) | `npm run examples:vizdoom-replay`、`npm run examples:breakout-replay` | 1 张 case card |
| Week 3 | 失败类型与反遗忘 | [第 3 讲](/zh-cn/slides/lecture-3/)、[学习闭环](/zh-cn/theory/learning-loop)、[研究框架](/zh-cn/theory/research-framework) | `npm run examples:ant-gait-replay:feedback`、`npm run examples:traffic-grid:feedback` | failure mode 对照表 |
| Week 4 | 研究问题与可反驳实验 | [研究问题](/zh-cn/theory/research-framework)、[实验协议](/zh-cn/appendix/benchmark-protocol)、[研究课题](/zh-cn/appendix/research-projects) | `npm run examples:feedback`、`npm run examples:reports:check` | 研究问题 + 最小 probe 设计 |
| Week 5 | 贡献、发布与最终验收 | [贡献与研究协议](/zh-cn/appendix/contribution-protocol)、[课程 Rubric](/zh-cn/appendix/rubric)、[发布清单](/zh-cn/appendix/release-checklist) | `npm run source:registry:check`、`npm run teaching:registry:check`、`npm run course:structure:check`、`npm run docs:routes:check`、`npm run verify` | 最终 PR 或课程报告 |

## 4 周压缩版

| 周次 | 合并内容 | 必做命令 | 交付 |
| --- | --- | --- | --- |
| Week 1 | Week 0 + Week 1 | `npm run verify`、`npm run examples:gridworld:feedback` | 解释 signal -> probe -> report |
| Week 2 | Week 2 | `npm run examples:vizdoom-replay`、`npm run examples:breakout-replay:feedback` | 公开 artifact case card |
| Week 3 | Week 3 + Week 4 | `npm run examples:feedback`、`npm run examples:reports:check` | 一个可反驳研究问题 |
| Week 4 | Week 5 | `npm run source:registry:check`、`npm run teaching:registry:check`、`npm run course:structure:check`、`npm run docs:routes:check`、`npm run verify` | 最终报告或 PR |

## 每周固定检查

每周作业不以“写了多少文字”为主要标准，而以证据链是否完整为标准：

| 检查项 | 最低要求 |
| --- | --- |
| 来源 | 有公开 URL、脱敏应用问题说明或仓库 artifact 路径 |
| Failure mode | 能命名一个失败模式，而不是只说效果不好 |
| Baseline | 有自然但不充分的策略 |
| Patch | 能指出更新对象：阈值、检测器、控制律、测试或文档结构 |
| Report | 有 `experiments/*/latest.json` 或 `templates/experiment-record.md` |
| Regression | 至少跑过相关示例测试，最终必须跑 `npm run verify` |

## 最终项目格式

最终项目可以选择三种形态：

| 形态 | 适合对象 | 最低交付 |
| --- | --- | --- |
| 案例研究 | 偏研究阅读的学生 | `templates/case-card.md` + 来源登记更新 + 研究问题映射 |
| 可运行示例 | 偏工程实现的学生 | `examples/*` + `experiments/*/latest.json` + `tests/test_*.py` |
| 课程材料 | 偏助教或讲师 | 新增讲义页或 lab 页 + demo 命令 + Rubric 对齐 |

最终提交必须能回答：

1. 这个材料支持或反驳哪一个 [研究问题](/zh-cn/theory/research-framework)？
2. 它的来源状态是什么，是否需要脱敏或降级为线索？
3. 它的最小失败场景是什么？
4. 它的 heuristic patch 修改了哪个可维护对象？
5. `npm run verify` 是否通过？

## 教师执行建议

- Week 0 不讲新概念，只处理环境、命令和仓库结构。
- 每周最多讲一个主要 failure mode，保证学生有时间读代码。
- 不接受只有成功截图的作业；必须有 baseline failure。
- X/脱敏应用问题只能作为来源线索进入课程，公开提交必须按 `SECURITY.md` 脱敏。
- 期末展示优先看证据链，其次才看实现复杂度。

更短的一次性工作坊可以直接使用 [教师指南](/zh-cn/appendix/instructor-guide)；更严格的评分细则见 [课程 Rubric](/zh-cn/appendix/rubric)。
