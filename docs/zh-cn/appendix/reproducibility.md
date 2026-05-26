---
title: 可复现性检查清单
description: Heuristic Learning 仓库的环境、示例、研究问题、教学产物、贡献和站点复现检查
---

# 可复现性检查清单

本页给出复现 HL 学习材料时需要完成的检查。重点不是页面数量，而是理论、示例、报告、贡献协议和文档站是否都有可追溯证据与验证命令。

机器可读清单见 [`/reproducibility-checklist.json`](/reproducibility-checklist.json)，字段约束见 [`/reproducibility-checklist.schema.json`](/reproducibility-checklist.schema.json)。`npm run reproducibility:check` 会检查证据路径、命令、通过条件和已知边界是否仍然对齐。

## 检查矩阵

| 检查 | 复现对象 | 代表命令 | 边界 |
| --- | --- | --- | --- |
| 环境与安装 | clean checkout 到统一验证 | `npm run verify` | 本地 HTTP 预检不等于发布验收 |
| 可运行示例 | 六个 examples、reports、tests | `npm run examples:feedback` | 轻量 replay 不等于高保真环境 |
| 研究问题与来源 | claims、source、X 来源、引用边界 | `npm run claims:registry:check` | 未复核线索不能写成已复现 |
| 教学产物 | lecture、lab、exercise、rubric、teaching pack | `npm run exercises:check` | 结构通过不代替教师评审 |
| 贡献与发布 | contribution contract、PR、release、安全 | `npm run contribution:contract:check` | 禁止公开凭证和私有原文 |
| 站点与机器入口 | manifest、JSON route、llms、VitePress | `npm run docs:routes:check` | route 200 不等于视觉验收 |

## 推荐复现顺序

研究者或助教从零检查时，按下面顺序执行：

```bash
npm install
npm run examples:test
npm run examples:feedback
npm run examples:reports:check
npm run benchmark:summary:check
npm run claims:registry:check
npm run source:registry:check
npm run x:sources:check
npm run teaching:registry:check
npm run slides:check
npm run exercises:check
npm run rubric:check
npm run teaching:pack:check
npm run contribution:contract:check
npm run course:structure:check
npm run course:manifest:check
npm run docs:routes:check
npm run build
npm run verify
```

如果只想复查某个案例，先读对应 `examples/*/README.md`，再运行该示例的 `feedback` 命令，最后用 `npm run examples:reports:check` 和 `npm run examples:test` 判断是否仍能作为课程证据。

## 判定原则

- 可复现证据必须能落到文件、命令、报告或公开 route。
- 研究问题证据必须区分 working hypothesis、implemented course invariant 和未复核线索。
- 轻量 replay 可以作为课程证据，但不能夸大成真实环境复现。
- 贡献和发布必须通过 `npm run verify`，并且不能绕过来源、安全和视觉验收边界。

## 维护要求

新增主线示例、讲义、练习、研究问题、贡献路径或 public registry 时，必须同步更新 `/reproducibility-checklist.json`，或明确说明为什么已有清单已经覆盖该变更。
