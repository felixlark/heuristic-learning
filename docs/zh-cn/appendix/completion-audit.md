---
title: 完成度审计
description: Heuristic Learning 仓库目标、证据、验证命令和剩余边界的验收矩阵
---

# 完成度审计

本页把“统一学习主线、可运行示例、可验证练习”的目标拆成证据矩阵。它不是发布宣传页，而是维护者、助教和编码智能体判断仓库是否接近完成的审计入口。

机器可读审计矩阵见 [`/completion-audit.json`](/completion-audit.json)，字段约束见 [`/completion-audit.schema.json`](/completion-audit.schema.json)。`npm run completion:audit:check` 会检查目标拆解、必跑命令、证据边界和完成前检查是否仍与本页一致。

## 目标拆解

| 要求 | 当前证据 | 验证方式 |
| --- | --- | --- |
| 中文课程入口 | README、[首页](/zh-cn/)、[课程地图](/zh-cn/course-map/)、[课程大纲](/zh-cn/syllabus/)、[学习单元矩阵](/zh-cn/appendix/learning-units)、[学习成果矩阵](/zh-cn/appendix/learning-outcomes)、[阶段检查点](/zh-cn/appendix/checkpoints) | `npm run course:structure:check`、`npm run learning:units:check`、`npm run learning:outcomes:check`、`npm run checkpoints:check` |
| 理论积累 | [学习闭环](/zh-cn/theory/learning-loop)、[研究框架](/zh-cn/theory/research-framework)、[研究命题](/zh-cn/theory/research-propositions)、[文献阅读指南](/zh-cn/appendix/reading-guide)、[评估指标矩阵](/zh-cn/appendix/evaluation-metrics)、[论文蓝图](/zh-cn/appendix/paper-blueprint)、[研究日志](/zh-cn/appendix/research-logbook)、`/evaluation-metrics.json`、`/paper-blueprint.json`、`/research-logbook.json` | `npm run metrics:check`、`npm run paper:blueprint:check`、`npm run research:logbook:check` + 页面 frontmatter + manifest 检查 |
| 可运行示例 | 6 个 `examples/*`、6 个 `tests/test_*.py`、6 个 `experiments/*/latest.json`、代码导览、Benchmark 结果摘要、消融计划、Artifact 差距分析 | `npm run examples:test`、`npm run examples:feedback`、`npm run code:tour:check`、`npm run benchmark:summary:check`、`npm run ablation:plan:check`、`npm run artifact:gap:check` |
| 案例库 | Ant、Breakout、VizDoom、Robot Soccer、Traffic、X signal、[案例矩阵](/zh-cn/appendix/case-registry)、[来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook)、`/case-registry.json` | `npm run source:registry:check`、`npm run cases:check`、`npm run source:case:check` |
| 课程材料 | 3 讲 + 2 Lab、讲者备注、教师指南、课程进度表、授课包、概念图谱、学习成果矩阵、研究课题、研究日志、练习集、Rubric | `npm run teaching:registry:check`、`npm run slides:check`、`npm run speaker:notes:check`、`npm run rubric:check`、`npm run exercises:check`、`npm run concept:graph:check`、`npm run learning:outcomes:check`、`npm run teaching:pack:check`、`npm run research:projects:check`、`npm run research:logbook:check` |
| 机器可读入口 | `/course-manifest.json` 统一登记核心页面、示例、public resources 和 CI gate；`/troubleshooting-tree.json` 把失败面映射到诊断、修复和复验；各 registry/schema 由对应检查脚本约束 | `npm run course:manifest:check`、`npm run troubleshooting:tree:check`、registry checks |
| 贡献与发布治理 | CONTRIBUTING、PR/issue templates、contribution contract、[贡献与研究协议](/zh-cn/appendix/contribution-protocol)、release checklist、CHANGELOG、LICENSE、CITATION | `npm run contribution:contract:check`、`npm run course:structure:check` |
| 来源和安全边界 | 来源登记、X 来源矩阵、引用页、`SECURITY.md`、敏感来源规则 | `npm run source:registry:check`、`npm run x:sources:check`、结构检查 |
| 文档构建 | VitePress site、sitemap、public JSON routes | `npm run verify` |
| 浏览器视觉验收 | [视觉与浏览器验收](/zh-cn/appendix/visual-verification)、`/visual-verification.json`、`/visual-verification.schema.json`、`/visual-acceptance-log.json` | `npm run visual:verification:check`、`npm run docs:routes:check`、`npm run release:readiness:check` |
| 可复现性 | [可复现性检查清单](/zh-cn/appendix/reproducibility)、`/reproducibility-checklist.json`、`/reproducibility-checklist.schema.json` | `npm run reproducibility:check`、`npm run verify` |

## 必须通过的本地命令

完整验收只认一条总命令：

```bash
npm run verify
```

它当前应覆盖：

1. `npm run lint`
2. `npm run examples:test`
3. `npm run examples:feedback`
4. `npm run examples:reports:check`
5. `npm run examples:registry:check`
6. `npm run code:tour:check`
7. `npm run benchmark:summary:check`
8. `npm run ablation:plan:check`
9. `npm run artifact:gap:check`
10. `npm run source:registry:check`
11. `npm run cases:check`
12. `npm run x:sources:check`
13. `npm run source:case:check`
14. `npm run claims:registry:check`
15. `npm run teaching:registry:check`
16. `npm run slides:check`
17. `npm run speaker:notes:check`
18. `npm run rubric:check`
19. `npm run exercises:check`
20. `npm run contribution:contract:check`
21. `npm run reproducibility:check`
22. `npm run troubleshooting:tree:check`
23. `npm run concept:graph:check`
25. `npm run learning:units:check`
26. `npm run learning:outcomes:check`
27. `npm run checkpoints:check`
28. `npm run metrics:check`
29. `npm run paper:blueprint:check`
30. `npm run teaching:pack:check`
31. `npm run research:projects:check`
32. `npm run research:logbook:check`
33. `npm run visual:verification:check`
34. `npm run release:readiness:check`
35. `npm run completion:audit:check`
36. `npm run course:manifest:check`
37. `npm run course:structure:check`
38. `npm run docs:routes:check`
39. `SITEMAP_NO_WRITE=1 npm run build`

局部命令可以帮助定位问题，但不能替代总命令。任何新增页面、示例、讲义或 registry 字段，都应该让 `npm run verify` 失败一次，再补齐证据链。

## 路由预检

本地 dev server 预检用于发现公开路由和 JSON 入口是否能被访问：

```bash
npm run dev -- --host 127.0.0.1
```

自动化预检命令：

```bash
npm run docs:routes:check
```

至少检查：

| 路由 | 目的 |
| --- | --- |
| `/heuristic-learning/` | 首页 |
| `/heuristic-learning/zh-cn/syllabus/` | 课程大纲 |
| `/heuristic-learning/zh-cn/examples/` | 示例入口 |
| `/heuristic-learning/zh-cn/slides/` | 讲义入口 |
| `/heuristic-learning/zh-cn/appendix/reading-guide` | 文献阅读入口 |
| `/heuristic-learning/zh-cn/appendix/case-registry` | 案例矩阵入口 |
| `/heuristic-learning/zh-cn/appendix/learning-units` | 学习单元入口 |
| `/heuristic-learning/zh-cn/appendix/learning-outcomes` | 学习成果入口 |
| `/heuristic-learning/zh-cn/appendix/checkpoints` | 阶段检查点入口 |
| `/heuristic-learning/zh-cn/appendix/evaluation-metrics` | 评估指标入口 |
| `/heuristic-learning/zh-cn/appendix/teaching-pack` | 授课包入口 |
| `/heuristic-learning/zh-cn/appendix/benchmark-results` | Benchmark 结果入口 |
| `/heuristic-learning/zh-cn/appendix/research-logbook` | 研究日志入口 |
| `/heuristic-learning/zh-cn/appendix/completion-audit` | 完成度审计 |
| `/heuristic-learning/zh-cn/appendix/visual-verification` | 视觉与浏览器验收 |
| `/heuristic-learning/zh-cn/appendix/reproducibility` | 可复现性检查清单 |
| `/heuristic-learning/course-manifest.json` | 课程 manifest 与 public resources 总入口 |
| `/heuristic-learning/course-manifest.schema.json` | 课程 manifest schema |
| `/heuristic-learning/example-registry.json` | 示例 registry |
| `/heuristic-learning/code-tour.json` | 代码导览 registry |
| `/heuristic-learning/benchmark-summary.json` | Benchmark 摘要 |
| `/heuristic-learning/ablation-plan.json` | 消融计划 registry |
| `/heuristic-learning/artifact-gap-analysis.json` | Artifact 差距分析 registry |
| `/heuristic-learning/troubleshooting-tree.json` | 排错决策树 registry |
| `/heuristic-learning/claims-registry.json` | 命题 registry |
| `/heuristic-learning/case-registry.json` | 案例矩阵 registry |
| `/heuristic-learning/teaching-registry.json` | 讲义 registry |
| `/heuristic-learning/slide-deck.json` | 讲义结构 registry |
| `/heuristic-learning/speaker-notes.json` | 讲者备注 registry |
| `/heuristic-learning/rubric.json` | 评分 Rubric registry |
| `/heuristic-learning/exercise-registry.json` | 练习题 registry |
| `/heuristic-learning/contribution-contract.json` | 贡献契约 registry |
| `/heuristic-learning/reproducibility-checklist.json` | 可复现性清单 registry |
| `/heuristic-learning/learning-units.json` | 学习单元 registry |
| `/heuristic-learning/learning-outcomes.json` | 学习成果 registry |
| `/heuristic-learning/checkpoint-registry.json` | 阶段检查点 registry |
| `/heuristic-learning/evaluation-metrics.json` | 评估指标 registry |
| `/heuristic-learning/paper-blueprint.json` | 论文蓝图 registry |
| `/heuristic-learning/concept-graph.json` | 概念图谱 registry |
| `/heuristic-learning/teaching-pack.json` | 授课包 registry |
| `/heuristic-learning/research-projects.json` | 研究项目 registry |
| `/heuristic-learning/research-logbook.json` | 研究日志 registry |
| `/heuristic-learning/completion-audit.json` | 完成度审计 registry |
| `/heuristic-learning/visual-verification.json` | 视觉验收 registry |
| `/heuristic-learning/visual-acceptance-log.json` | 视觉验收记录 |
| `/heuristic-learning/x-sources.json` | X 来源 registry |
| `/heuristic-learning/source-to-case-playbook.json` | 来源到案例 playbook |
| `/heuristic-learning/experiment-report.schema.json` | 实验报告 schema |

HTTP 200 只能证明路由可达。正式公开发布仍需要 GitHub Pages 或目标部署面的真实访问检查；如果官方 Browser/IAB 不可用，应把它记为视觉验收缺口，而不是把 HTTP 预检当作最终视觉验证。

## 证据边界

| 主题 | 当前状态 | 不应过度声明 |
| --- | --- | --- |
| Jiayi Weng 原始思想 | 以 `learning-beyond-gradients` 文章和公开 artifact 为最高信号来源 | 不写成已有正式论文结论 |
| X 来源信号 | 作为 source signal 和待结构化案例；`/x-sources.json` 区分 已复核摘要、待直接复核、待采集 | 未通过 `ft` 或公开 URL 复核前不写成已复现 |
| 脱敏应用问题 | 只允许脱敏后变成最小环境或脱敏应用问题 | 不公开私有原文、会议纪要或私有链接 |
| 轻量 replay | 可作为教学复现和 failure probe | 不等同于真实 MuJoCo/Atari/VizDoom 高保真复现 |
| 本地 HTTP 预检 | 可证明 dev server 路由可达 | 不等同于 GitHub Pages 发布验收 |
| Browser/IAB 视觉验收 | 由 [视觉与浏览器验收](/zh-cn/appendix/visual-verification) 定义官方浏览器路径 | 未跑官方 Browser/IAB 前不能声明视觉验收通过 |

## 完成前不得跳过

在标记仓库阶段性完成前，至少要重新确认：

1. `npm run verify` 当前通过。
2. `docs/.vitepress/dist`、`docs/.vitepress/cache` 和 `__pycache__` 没有残留。
3. README、syllabus、course-map、examples、slides、appendix 入口互相可达。
4. 关键 registry 与对应 schema 都能从 dev server 访问。
5. 来源登记没有把 X/脱敏应用问题写成已复现事实。
6. `SECURITY.md` 仍然约束凭证、私有原文、X cookie/API token 和私有日志。
7. `visual-verification.json` 仍把发布前必须复验的官方 Browser/IAB 路径标记为 required-before-release；若未来有未完成路径，`visual-acceptance-log.json` 只能标记为 not-run 或 blocked，并写明原因。
8. `npm run release:readiness:check` 只有在官方 Browser/IAB 或记录允许的官方浏览器验收路径完成后才能通过；如果未来出现 blocked 项，不能声明公开发布就绪。
9. 如果要公开发布，GitHub Actions 和 Pages 真实路由需要在目标平台重新验收。

本页的作用是防止“测试绿了所以完成”的误判。HL 仓库的完成度必须同时由理论、案例、示例、讲义、来源、机器可读入口和构建验证共同支撑。
