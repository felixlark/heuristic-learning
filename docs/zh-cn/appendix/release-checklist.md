---
title: 发布清单
description: Heuristic Learning 仓库版本发布、变更记录和发布前验证清单
---

# 发布清单

本页定义 HL 仓库发布或阶段性提交前的检查顺序。它补充 [贡献与研究协议](/zh-cn/appendix/contribution-protocol)：贡献协议约束单个 PR，本页约束一次课程版本或公开发布。

## 发布前必须回答

| 问题 | 检查位置 |
| --- | --- |
| 本次变化属于理论、案例、示例、讲义、工具还是发布结构？ | README、课程大纲、相关页面 |
| 是否新增或改变来源状态？ | [来源登记](/zh-cn/appendix/source-registry) |
| 是否改变案例页、案例来源或案例到示例的绑定？ | [案例矩阵](/zh-cn/appendix/case-registry)、`/case-registry.json` |
| 是否改变来源到 case card 的可学习、可验证路径？ | [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook)、`/source-to-case-playbook.json` |
| 是否新增 runnable example 或 report 字段？ | `examples/`、`experiments/`、report schema |
| 是否改变示例代码阅读顺序、编辑目标或测试路径？ | [代码导览](/zh-cn/appendix/code-tour)、`/code-tour.json` |
| 是否改变 benchmark 结果或实验解释？ | [Benchmark 结果摘要](/zh-cn/appendix/benchmark-results)、`/benchmark-summary.json` |
| 是否改变消融变量或后续对照计划？ | [消融计划](/zh-cn/appendix/ablation-plan)、`/ablation-plan.json` |
| 是否改变轻量 replay 与真实 artifact 的保真度边界？ | [Artifact 差距分析](/zh-cn/appendix/artifact-gap-analysis)、`/artifact-gap-analysis.json` |
| 是否改变失败诊断、修复动作或复验命令？ | [本地运行与排错](/zh-cn/appendix/local-setup)、`/troubleshooting-tree.json` |
| 是否改变课程入口或学习路径？ | [课程地图](/zh-cn/course-map/)、[课程大纲](/zh-cn/syllabus/) |
| 是否改变讲义、课堂提示或课堂交付？ | [页面幻灯片](/zh-cn/talk/)、[授课包](/zh-cn/appendix/teaching-pack) |
| 是否改变能力目标、练习或 Rubric 映射？ | [学习成果矩阵](/zh-cn/appendix/learning-outcomes)、`/learning-outcomes.json` |
| 是否改变阶段自测或每周验收口径？ | [阶段检查点](/zh-cn/appendix/checkpoints)、`/checkpoint-registry.json` |
| 是否改变研究评估维度或证据路径？ | [评估指标矩阵](/zh-cn/appendix/evaluation-metrics)、`/evaluation-metrics.json` |
| 是否改变论文/技术报告写作结构？ | [论文蓝图](/zh-cn/appendix/paper-blueprint)、`/paper-blueprint.json` |
| 是否改变引用、授权或来源边界？ | [引用与署名](/zh-cn/appendix/citation)、`LICENSE`、`CITATION.cff` |
| 是否包含敏感来源、凭证、私有日志或未脱敏截图？ | `SECURITY.md`、issue/PR 模板 |
| 是否改变完成度证据或验收口径？ | [完成度审计](/zh-cn/appendix/completion-audit) |
| 是否需要重新跑官方 Browser/IAB 或 Chrome 视觉验收？ | [视觉与浏览器验收](/zh-cn/appendix/visual-verification)、`/visual-verification.json`、`/visual-acceptance-log.json` |
| 是否需要记录版本变化？ | `CHANGELOG.md` |

## 验证顺序

发布前先跑局部检查定位问题：

```bash
npm run examples:test
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
npm run code:tour:check
npm run benchmark:summary:check
npm run ablation:plan:check
npm run artifact:gap:check
npm run source:registry:check
npm run cases:check
npm run x:sources:check
npm run source:case:check
npm run claims:registry:check
npm run rubric:check
npm run exercises:check
npm run contribution:contract:check
npm run reproducibility:check
npm run troubleshooting:tree:check
npm run paper:blueprint:check
npm run concept:graph:check
npm run learning:units:check
npm run learning:outcomes:check
npm run checkpoints:check
npm run metrics:check
npm run paper:blueprint:check
npm run teaching:pack:check
npm run research:projects:check
npm run visual:verification:check
npm run completion:audit:check
npm run course:manifest:check
npm run course:structure:check
npm run docs:routes:check
```

最终发布门槛只有一条：

```bash
npm run verify
```

通过局部命令不等于可以发布。`npm run verify` 必须作为最终证据，因为它会把示例、报告、来源、manifest、结构和 VitePress build 一起验证。

公开发布前再跑发布就绪门禁：

```bash
npm run release:readiness:check
```

这个命令故意不放进 `npm run verify`。当 [视觉与浏览器验收](/zh-cn/appendix/visual-verification) 仍是 `required-before-release`，或 `/visual-acceptance-log.json` 仍有 `not-run`/`blocked` 记录时，它应该失败，并列出还需要用官方 Browser/IAB 或 Chrome 插件验收的路径。只有 `npm run verify` 通过、真实浏览器验收记录完成、`/visual-verification.json` 与 `/visual-acceptance-log.json` 的对应状态更新为 `passed` 后，它才应该通过。

## Changelog 规则

每次公开版本或阶段性发布都应更新 `CHANGELOG.md`：

```text
## [version] - YYYY-MM-DD

### Added
### Changed
### Fixed
### Verification
### Source Boundary
```

写 changelog 时要避免两类问题：

- 不把未验证 X/脱敏应用问题写成已复现。
- 不把轻量 replay 写成真实环境完整复现。

如果只是内部小改动，可以不新增版本号，但仍应在 PR 或提交说明里写清楚验证命令。

## 发布后检查

GitHub Pages 发布后，应确认：

- 首页、课程地图、课程大纲、示例页和附录页能访问。
- `/course-manifest.json`、`/course-manifest.schema.json`、`/example-registry.json`、`/code-tour.json`、`/benchmark-summary.json`、`/ablation-plan.json`、`/artifact-gap-analysis.json`、`/troubleshooting-tree.json`、`/case-registry.json`、`/source-to-case-playbook.json`、`/learning-outcomes.json`、`/checkpoint-registry.json`、`/evaluation-metrics.json`、`/paper-blueprint.json`、`/visual-verification.json`、`/visual-acceptance-log.json`、`/x-sources.json`、`/experiment-report.schema.json` 能访问。
- README、`CITATION.cff`、`LICENSE` 和 `CHANGELOG.md` 彼此一致。
- `SECURITY.md`、来源登记和 issue/PR 模板对敏感来源的要求一致。
- GitHub Actions 的 `Verify course repository` 和 Pages deploy workflow 都通过。
- 官方 Browser/IAB 或 Chrome 插件完成 [视觉与浏览器验收](/zh-cn/appendix/visual-verification) 中的必验路径；未完成时只能写 `required-before-release`，不能写通过。
- `npm run release:readiness:check` 通过，证明本地验证和官方浏览器验收都已经闭合。

本地 HTTP 200 只能说明路由预检通过，不能替代 Pages 上的最终发布检查。
