---
title: 视觉与浏览器验收
description: Heuristic Learning 公开页面在官方 Browser/IAB 或 Chrome 插件上的人工验收矩阵
---

# 视觉与浏览器验收

本页记录 `npm run verify` 之外的人工浏览器验收边界。HTTP 200、VitePress build 和 route check 只能证明页面可达；课程仓库公开发布前，还需要在官方浏览器表面确认页面可读、导航可用、移动端不溢出、机器可读入口索引页可读。

机器可读矩阵见 [`/visual-verification.json`](/visual-verification.json)，字段约束见 [`/visual-verification.schema.json`](/visual-verification.schema.json)。实际验收记录写入 [`/visual-acceptance-log.json`](/visual-acceptance-log.json)，字段约束见 [`/visual-acceptance-log.schema.json`](/visual-acceptance-log.schema.json)。`npm run visual:verification:check` 会检查本页、矩阵、日志、schema、manifest 和 completion audit 是否一致。

## 工具边界

| 场景 | 使用表面 | 不接受的替代 |
| --- | --- | --- |
| 未登录本地或公开页面 | Codex Browser plugin / in-app browser | Playwright、Chrome for Testing、`open`、CDP-only helpers |
| 需要用户 Chrome 登录态 | Official Chrome plugin | Computer Use、未授权浏览器 profile |
| Codex in-app browser 截图或点击 | Browser plugin 的 IAB 后端 | Computer Use for Codex in-app browser |

如果官方 Browser/IAB 或 Chrome 插件不可用，本项应记录为验收阻塞；不要把脚本预检写成“视觉验收已通过”。

## 必验路径

| ID | 路由 | 视口 | 验收重点 | 预检 |
| --- | --- | --- | --- | --- |
| `home-course-entry` | `/heuristic-learning/` | desktop | 首屏课程定位、核心导航、无空白主内容 | `npm run docs:routes:check` |
| `course-map-mobile` | `/heuristic-learning/zh-cn/course-map/` | mobile | 角色路径可读、中文标题不溢出、返回核心入口 | `npm run course:structure:check` |
| `examples-run-loop` | `/heuristic-learning/zh-cn/examples/` | desktop | 六个示例都有命令、报告、测试和复现边界 | `npm run examples:test` |
| `slide-deck-scan` | `/heuristic-learning/zh-cn/slides/` | desktop | 3 讲 + 2 Lab 入口、课堂命令、交付物 | `npm run slides:check` |
| `public-registry-entrypoints` | `/heuristic-learning/zh-cn/appendix/public-entrypoints` | desktop | registry/schema 索引页可读，链接到 course manifest、completion audit、visual verification 和 llms.txt；JSON/TXT 直达由 `npm run docs:routes:check` 验证 | `npm run course:manifest:check` |
| `completion-audit-page` | `/heuristic-learning/zh-cn/appendix/completion-audit` | desktop | 目标拆解、证据边界、视觉验收链接可读 | `npm run completion:audit:check` |

## 记录模板

视觉验收完成后，在发布记录或 PR 描述中保留以下字段；不要把凭证、Cookie、飞书私有链接或 X token 写入仓库。

| 字段 | 说明 |
| --- | --- |
| `date` | 验收日期 |
| `surface` | `in-app browser` 或 `Chrome plugin` |
| `route` | 实际访问的 URL |
| `viewport` | desktop 或 mobile |
| `observed_outcome` | 看到的成功路径或失败现象 |
| `remaining_issue` | 无问题写 `none`；否则写阻塞项 |

同一组字段也必须更新到 `/visual-acceptance-log.json`。未跑时保留 `status: not-run`；工具不可用或页面有问题时写 `blocked`；只有真实官方 Browser/IAB 或 Chrome 插件验收通过后才能写 `passed`。

## 当前状态

当前仓库状态把视觉验收定义为 `required-before-release`，通过与否由 `/visual-acceptance-log.json` 的真实运行记录决定。2026-05-25 复测时，官方 Browser/IAB 已重新注册到当前线程，并用 1280x720 桌面视口与 390x844 移动视口完成页面验收。JSON/TXT 顶层资源仍可能被浏览器客户端以 `net::ERR_BLOCKED_BY_CLIENT` 拦截，因此发布证据拆成两层：`npm run docs:routes:check` 验证 JSON/TXT 直达 200，Browser/IAB 验证 [机器可读入口](/zh-cn/appendix/public-entrypoints) 索引页可读。本地自动化必须先通过：

```bash
npm run visual:verification:check
npm run verify
npm run release:readiness:check
```

随后再用官方 Browser/IAB 或可控视口的 Official Chrome plugin 访问上述路径。只有所有必验路径都完成真实浏览器验收并更新 `/visual-acceptance-log.json` 为 `passed` 后，`npm run release:readiness:check` 才应该通过，也才能在发布清单里写“视觉验收通过”。
