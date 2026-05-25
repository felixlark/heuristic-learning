---
title: 来源到案例 Playbook
description: 把 X、公开 artifact、飞书线索和研究假设转成 Heuristic Learning 课程案例的操作路径
---

# 来源到案例 Playbook

本页回答一个课程仓库维护问题：看到一条 X 线程、公开 artifact、飞书线索或研究假设之后，怎样把它变成可追溯、可运行或可验证的 HL 案例。它补充 [来源登记](/zh-cn/appendix/source-registry)、[X 线索案例](/zh-cn/cases/x-signal/) 和 [贡献与研究协议](/zh-cn/appendix/contribution-protocol)。

机器可读 playbook 见 [`/source-to-case-playbook.json`](/source-to-case-playbook.json)，字段约束见 [`/source-to-case-playbook.schema.json`](/source-to-case-playbook.schema.json)。`npm run source:case:check` 会检查每条路径的来源检查、必备 artifact、状态门槛、验证命令、课程落点和禁止声明。

## 四条入口路径

| 入口 | 先确认 | 必备 artifact | 状态门槛 | 验证 |
| --- | --- | --- | --- | --- |
| X / FieldTheory thread | `ft status`、`ft show`、一手/二手分层 | `/x-sources.json`、X 线索案例、case card、reproduction note | `cached` 或 `referenced-not-cached` 可结构化；`to-collect` 只进路线图 | `npm run x:sources:check`、`npm run cases:check`、`npm run research:logbook:check` |
| Public code artifact | 文件路径、failure mode、可删掉的重依赖 | example registry、artifact gap、experiment record、reproduction note | 有 runnable example、report、test 才能写“已复现为轻量 replay” | `npm run examples:test`、`npm run artifact:gap:check`、`npm run research:logbook:check` |
| Internal Feishu or private operational signal | 只记录脱敏标签、日期、问题形态 | source registry、SECURITY、case card、experiment record、reproduction note | 能变成最小环境，但不能公开原文 | `npm run source:registry:check`、`npm run contribution:contract:check`、`npm run research:logbook:check` |
| Research hypothesis or uncached lead | 状态、反驳路径、未来 artifact gap | claim review、claims registry、research projects、reproduction note | 没有 example、metric、command 前不能写成主线结论 | `npm run claims:registry:check`、`npm run research:projects:check`、`npm run research:logbook:check` |

其中 `Internal Feishu signal` 是 `Internal Feishu or private operational signal` 的课程短名；`Research hypothesis` 是 `Research hypothesis or uncached lead` 的课程短名。短名用于目录和课堂讨论，完整名用于机器 registry 和状态门槛。

## 分路径验收命令

| 路径 | 命令 |
| --- | --- |
| X / FieldTheory thread | `npm run x:sources:check`、`npm run source:registry:check`、`npm run cases:check` |
| Public code artifact | `npm run examples:test`、`npm run examples:reports:check`、`npm run artifact:gap:check` |
| Internal Feishu or private operational signal | `npm run source:registry:check`、`npm run examples:test`、`npm run contribution:contract:check` |
| Research hypothesis or uncached lead | `npm run claims:registry:check`、`npm run research:projects:check`、`npm run metrics:check` |

## X 线索最短流程

1. 运行 `ft status`，记录 cache 更新时间。
2. 对稳定 URL 运行 `ft show <status_id>`；如果返回 `Bookmark not found`，只能写 `referenced-not-cached`。
3. 如果只有二手转述，先抽取“可课程化的问题结构”，不要照搬分数、归因或未验证细节。
4. 更新 [`/x-sources.json`](/x-sources.json) 的 `sources` 和 `extraction_cards`。
5. 在 [X 线索案例](/zh-cn/cases/x-signal/) 说明来源层级、课程落点和边界。
6. 如果能落到可运行示例，再补 `examples/*`、`experiments/*/latest.json` 和测试；否则只进入 [研究路线图](/zh-cn/appendix/research-roadmap)。

当前 Jiayi 原帖 `2052596837547495549` 仍是 `referenced-not-cached`，因此只能作为已知 URL 和待直接读取的一手来源。已缓存的 `@0xLogicrw` 中文转述可以用来设计课堂问题，但分数和归因不能当作本仓库复现实验结果。

## Case card 骨架

每条进入课程的来源都应先写成 `templates/case-card.md` 形态：

| 字段 | 要求 |
| --- | --- |
| Source | URL、采集日期、来源层级、登记状态 |
| Environment | 任务环境、可观察状态、动作空间 |
| Policy Surface | 可更新的代码、规则、检测器、配置或记忆 |
| Feedback | reward、测试、日志、回放、视频或人类评价 |
| HL Update | 下一轮编码智能体应先读什么、改哪里 |
| Verification | 哪条命令或 replay 能证明没有破坏旧行为 |
| Course Link | 对应章节、讲义、练习或 runnable example |

如果来源还没有进入 case card，先用 `templates/reproduction-note.md` 记录来源状态、复现范围、缺失保真度、反驳路径和下一步实验。复现记录通过后，才升级为 case card、实验记录或研究日志条目。

## 禁止声明

- 不把 `referenced-not-cached` 的一手帖写成已经直接读过。
- 不把二手转述中的分数写成本仓库 benchmark。
- 不把轻量 replay 写成真实 Atari、VizDoom 或 MuJoCo 高保真复现。
- 不公开飞书原文、会议纪要、私有链接、X cookie、API token 或私有日志。
- 不把 research hypothesis 写成主线结论。

## 维护命令

```bash
npm run source:case:check
npm run x:sources:check
npm run source:registry:check
npm run verify
```
