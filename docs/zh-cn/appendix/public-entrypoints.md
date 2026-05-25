---
title: 机器可读入口
description: Heuristic Learning public registries, schemas, and LLM entrypoints
---

# 机器可读入口

本页是给研究者、助教和编码智能体使用的 public entrypoints 索引。浏览器视觉验收检查本页是否可读；JSON/TXT 文件本身是否 200，由 `npm run docs:routes:check` 和 `npm run course:manifest:check` 验证。

机器可读总入口是 [`/course-manifest.json`](/course-manifest.json)，字段约束是 [`/course-manifest.schema.json`](/course-manifest.schema.json)。课程结构、示例、讲义、来源、可复现性和发布验收都应先从 manifest 追踪，不要靠人工猜目录。

## 核心入口

| 入口 | 用途 | 检查命令 |
| --- | --- | --- |
| [`/course-manifest.json`](/course-manifest.json) | 页面、示例、public resources 和 CI gate 总登记 | `npm run course:manifest:check` |
| [`/completion-audit.json`](/completion-audit.json) | 目标拆解、证据路径、必跑命令和完成前检查 | `npm run completion:audit:check` |
| [`/visual-verification.json`](/visual-verification.json) | 官方浏览器视觉验收矩阵 | `npm run visual:verification:check` |
| [`/visual-acceptance-log.json`](/visual-acceptance-log.json) | 实际官方浏览器验收记录 | `npm run visual:verification:check` |
| [`/llms.txt`](/llms.txt) | 面向 LLM 的阅读入口 | `npm run course:structure:check` |

## 研究与教学 registry

| 入口 | 用途 |
| --- | --- |
| [`/example-registry.json`](/example-registry.json) | 六个 runnable examples 的命令、报告和测试路径 |
| [`/benchmark-summary.json`](/benchmark-summary.json) | baseline failure、heuristic outcome 和证据摘要 |
| [`/case-registry.json`](/case-registry.json) | 案例到来源、示例、学习成果和命令的矩阵 |
| [`/claims-registry.json`](/claims-registry.json) | 研究命题、证据状态和反驳路径 |
| [`/teaching-registry.json`](/teaching-registry.json) | 讲义、课堂命令和交付物 |
| [`/research-projects.json`](/research-projects.json) | 项目制学习与后续研究课题 |
| [`/research-logbook.json`](/research-logbook.json) | 阅读、示例、命题和下一步实验记录 |
| [`/source-to-case-playbook.json`](/source-to-case-playbook.json) | X、公开 artifact、飞书线索和研究假设进入 case card 的路径 |
| [`/x-sources.json`](/x-sources.json) | X / FieldTheory 线索、来源层级和抽取卡 |

## 发布边界

JSON 和 TXT 是机器入口，不是视觉页面。如果官方浏览器客户端阻止顶层打开 `.json` 或 `.txt`，不要把 HTTP 预检写成视觉验收通过；应同时保留两类证据：

- `npm run docs:routes:check` 证明 JSON/TXT 路由可达。
- 官方 Browser/IAB 打开本页，证明公开入口索引、链接和发布边界对读者可见。

发布前至少运行：

```bash
npm run course:manifest:check
npm run docs:routes:check
npm run visual:verification:check
npm run release:readiness:check
```
