---
title: 教学仓库对标矩阵
description: Heuristic Learning 仓库对 EasyVibe、d2l-zh、llm.c 和 easy-rl 的结构化借鉴
---

# 教学仓库对标矩阵

本页把“参考 EasyVibe、深度学习课程仓库和 Karpathy 风格研究代码”变成可维护的结构约束。它不是外部仓库评测，而是说明 HL 仓库从这些参考项目中借鉴了什么、没有借鉴什么，以及如何用命令验证这些约束仍然成立。

机器可读矩阵见 [`/course-patterns.json`](/course-patterns.json)，字段约束见 [`/course-patterns.schema.json`](/course-patterns.schema.json)。`npm run patterns:check` 会检查本页、manifest、LLM 入口和实际文件是否对齐。

## 借鉴原则

| 原则 | 本仓库含义 | 验证方式 |
| --- | --- | --- |
| 课程先于营销 | 首页直接进入课程、路线、示例和讲义，不做空泛 landing page | `npm run course:structure:check` |
| 理论必须落地 | 每个理论命题要指向来源、案例、示例、报告或可反驳路径 | `npm run claims:registry:check` |
| 示例必须能跑 | 研究代码以小而可读、可测试的 replay/minimal env 为主 | `npm run examples:test` |
| 章节可教学 | 每讲和 Lab 都要有阅读、命令和交付物 | `npm run teaching:registry:check` |
| 机器可续写 | 给编码智能体保留 manifest、registry、schema 和 `llms.txt` | `npm run verify` |

## 参考项目到 HL 结构

| 参考项目 | 借鉴点 | HL 对应落点 | 不照搬的部分 |
| --- | --- | --- | --- |
| EasyVibe (`datawhalechina/easy-vibe`) | VitePress 中文课程、章节化路线、实践优先 | [课程大纲](/zh-cn/syllabus/)、[学习路线](/zh-cn/stage-1/)、[Slides](/zh-cn/slides/) | 不照搬主题内容；HL 保留自己的来源和案例边界 |
| d2l-zh (`d2l-ai/d2l-zh`) | 理论、代码、练习和作业同步推进 | [研究框架](/zh-cn/theory/research-framework)、[练习集](/zh-cn/appendix/exercises)、[课程 Rubric](/zh-cn/appendix/rubric) | 不把未发表思想写成成熟教科书结论 |
| llm.c (`karpathy/llm.c`) | 研究代码应当小、直、可读、可运行 | `examples/*/run.py`、`examples/*/feedback_loop.py`、`tests/test_*.py` | 不追求单文件极限或 C 语言复刻 |
| easy-rl (`datawhalechina/easy-rl`) | 用清晰课程语言解释 RL 概念和实验术语 | [从 RL/DL 到 HL](/zh-cn/stage-3/)、[实验协议](/zh-cn/appendix/benchmark-protocol) | 不把 HL 简化成 RL 的规则版 |

## 对读者的体验要求

一个研究者或学生从仓库首页进入后，应该能在 15 分钟内完成三件事：

1. 通过 [课程地图](/zh-cn/course-map/) 选定学生、研究者、教师或编码智能体路径。
2. 通过 [可运行示例](/zh-cn/examples/) 找到一个 failure mode，并运行对应命令。
3. 通过 [文献阅读指南](/zh-cn/appendix/reading-guide) 或 [研究命题](/zh-cn/theory/research-propositions) 理解这个例子支持哪个研究问题。

对应命令：

```bash
npm run docs:routes:check
npm run course:structure:check
npm run teaching:registry:check
npm run claims:registry:check
npm run examples:test
npm run examples:feedback
npm run patterns:check
npm run verify
```

## 对维护者的结构要求

新增一章、一讲、一个案例或一个示例时，必须回答：

| 问题 | 应该落到哪里 |
| --- | --- |
| 这条材料来自哪里？ | [来源登记](/zh-cn/appendix/source-registry) |
| 它支持或反驳哪个命题？ | [`/claims-registry.json`](/claims-registry.json) |
| 它有没有可运行环境？ | `examples/*`、`tests/test_*.py`、`experiments/*/latest.json` |
| 它能不能被学生完成？ | [练习集](/zh-cn/appendix/exercises)、[课程进度表](/zh-cn/appendix/course-schedule) |
| 它是否影响仓库结构？ | [`/course-manifest.json`](/course-manifest.json)、[`/course-patterns.json`](/course-patterns.json) |

这也是本仓库和普通“资料合集”的分界：资料合集可以只收链接；HL 课程仓库必须把链接转成课程路径、可运行代码、验证报告和后续研究任务。

## 验收边界

当前对标矩阵只证明仓库组织方式已经显式参考这些项目，不能证明 HL 理论本身已经成熟。更严格的学术结论仍需要真实环境复现、跨场景对比和论文级实验。

因此本页的结论只能写成：

- HL 仓库已经具备课程型入口、示例型研究代码、练习和机器可读结构。
- 参考仓库的借鉴点已经被本仓库约束为页面、registry 和命令。
- 未发表论文的部分仍以研究命题、假设和可反驳任务呈现。

新增或修改本页后，至少运行：

```bash
npm run patterns:check
npm run course:structure:check
npm run verify
```
