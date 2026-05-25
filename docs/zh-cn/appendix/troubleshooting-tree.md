---
title: 排错决策树
description: Heuristic Learning 仓库从安装、示例、报告、来源、课程结构到视觉验收的失败诊断路径
---

# 排错决策树

本页把 [本地运行与排错](/zh-cn/appendix/local-setup) 的长表压缩成可执行决策树。遇到失败时，先找失败面，再跑诊断命令，最后只修改对应证据层；不要直接从 `npm run verify` 的末尾错误跳到随意改文件。

机器可读决策树见 [`/troubleshooting-tree.json`](/troubleshooting-tree.json)，字段约束见 [`/troubleshooting-tree.schema.json`](/troubleshooting-tree.schema.json)。`npm run troubleshooting:tree:check` 会检查每个节点的诊断命令、修复动作、复验命令和关联页面是否存在。

## 决策路径

| 失败面 | 典型症状 | 先跑诊断命令 | 修复方向 | 复验 |
| --- | --- | --- | --- | --- |
| 安装或运行环境 | `npm install`、`npm run dev` 或 build 在课程检查前失败 | `node --version`、`npm --version`、`npm run lint` | Node 18+、重装依赖、清理 VitePress cache | `npm run lint`、`npm run build` |
| 示例行为 | `examples:test` 或某个 feedback 失败 | `npm run examples:test`、`npm run examples:feedback`、`npm run code:tour:check` | 按代码导览读示例，只改对应 `edit_target` | `npm run examples:reports:check` |
| 报告与 benchmark | report、benchmark、ablation 或 artifact gap 失败 | `npm run benchmark:summary:check`、`npm run ablation:plan:check`、`npm run artifact:gap:check` | 重新生成 report，同步 benchmark/消融/保真度边界 | `npm run examples:feedback` |
| 来源与命题 | source、X、case 或 claims 检查失败 | `npm run source:registry:check`、`npm run x:sources:check`、`npm run claims:registry:check` | 降级来源状态，补 case card，把未发表结论写成 hypothesis | `npm run cases:check` |
| 课程结构与公开路由 | manifest、structure、routes 或 build 失败 | `npm run course:manifest:check`、`npm run course:structure:check`、`npm run docs:routes:check` | 同步 sidebar、manifest、route check、structure checker | `npm run docs:routes:check` |
| 发布与视觉验收 | `release:readiness:check` 阻塞 | `npm run visual:verification:check`、`npm run release:readiness:check` | 用官方 Browser/IAB 复验页面；JSON/TXT 直达用 `npm run docs:routes:check`，浏览器只验收 [机器可读入口](/zh-cn/appendix/public-entrypoints) 索引页；更新 visual log | `npm run release:readiness:check` |

## 处理顺序

1. 先确认失败属于哪一个失败面。
2. 只跑该节点的 `diagnostic_commands`，不要先改代码。
3. 只执行该节点的 `fix_actions`，并保留来源和边界。
4. 跑 `verification_commands`。
5. 最后再回到 `npm run verify`。

## 不要做的事

- 不要因为 `docs:routes:check` 通过就声明视觉验收通过。
- 不要把 X/脱敏应用问题的来源状态从 `待采集` 直接提升为 `已复现`。
- 不要同时改环境、策略、报告和测试；先按 [代码导览](/zh-cn/appendix/code-tour) 缩小编辑面。
- 不要提交 `docs/.vitepress/dist`、`docs/.vitepress/cache` 或 `__pycache__`。

```bash
npm run troubleshooting:tree:check
npm run verify
```
