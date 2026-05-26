---
title: 来源到案例 Playbook
description: 把公开来源、代码 artifact、脱敏应用问题和研究假设转成 HL 案例
---

# 来源到案例 Playbook

本页回答一个学习问题：看到一条公开讨论、一个代码 artifact、一个脱敏应用问题或一个研究假设之后，怎样把它变成可追溯、可运行或可验证的 HL 案例。它补充 [来源登记](/zh-cn/appendix/source-registry)、[X 来源案例](/zh-cn/cases/x-signal/) 和 [贡献与研究协议](/zh-cn/appendix/contribution-protocol)。

机器可读 playbook 见 [`/source-to-case-playbook.json`](/source-to-case-playbook.json)，字段约束见 [`/source-to-case-playbook.schema.json`](/source-to-case-playbook.schema.json)。`npm run source:case:check` 会检查每条路径的来源检查、必备 artifact、状态门槛、验证命令、课程落点和禁止声明。

## 四条入口路径

| 入口 | 先确认 | 必备 artifact | 状态门槛 | 验证 |
| --- | --- | --- | --- | --- |
| X / public discussion | 一手/二手分层、稳定 URL、可复核主张 | `/x-sources.json`、X 来源案例、case card、reproduction note | 已复核或已知 URL 可结构化；待采集方向只进路线图 | `npm run x:sources:check`、`npm run cases:check`、`npm run research:logbook:check` |
| Public code artifact | 文件路径、failure mode、可删掉的重依赖 | example registry、artifact gap、experiment record、reproduction note | 有 runnable example、report、test 才能写“已复现为轻量 replay” | `npm run examples:test`、`npm run artifact:gap:check`、`npm run research:logbook:check` |
| Sanitized operational problem | 只记录脱敏标签、日期、问题形态 | source registry、SECURITY、case card、experiment record、reproduction note | 能变成最小环境，但不能公开原文 | `npm run source:registry:check`、`npm run contribution:contract:check`、`npm run research:logbook:check` |
| Research hypothesis or uncollected lead | 状态、反驳路径、未来 artifact gap | claim review、claims registry、research projects、reproduction note | 没有 example、metric、command 前不能写成主线结论 | `npm run claims:registry:check`、`npm run research:projects:check`、`npm run research:logbook:check` |

其中 `Sanitized operational problem` 指脱敏后的真实应用问题；`Research hypothesis` 指还没有实验支撑、但可以被转成研究设计的问题。

## 分路径验收命令

| 路径 | 命令 |
| --- | --- |
| X / public discussion | `npm run x:sources:check`、`npm run source:registry:check`、`npm run cases:check` |
| Public code artifact | `npm run examples:test`、`npm run examples:reports:check`、`npm run artifact:gap:check` |
| Sanitized operational problem | `npm run source:registry:check`、`npm run examples:test`、`npm run contribution:contract:check` |
| Research hypothesis or uncollected lead | `npm run claims:registry:check`、`npm run research:projects:check`、`npm run metrics:check` |

## X 来源最短流程

1. 先确认是否有稳定 URL，以及材料是一手原帖、二手转述还是评论。
2. 如果只有二手转述，先抽取“可可学习、可验证的问题结构”，不要照搬分数、归因或未验证细节。
3. 更新 [`/x-sources.json`](/x-sources.json) 的 `sources` 和 `extraction_cards`。
4. 在 [X 来源案例](/zh-cn/cases/x-signal/) 说明来源层级、课程落点和边界。
5. 如果能落到可运行示例，再补 `examples/*`、`experiments/*/latest.json` 和测试；否则只进入 [研究路线图](/zh-cn/appendix/research-roadmap)。

Jiayi 原帖 `2052596837547495549` 当前只作为已知 URL 和待直接复核的一手来源。`@0xLogicrw` 中文转述可以用来定位课堂问题，但分数和归因不能当作课程复现实验结果。

## Case card 骨架

每条进入课程的来源都应先写成 case card；课程模板是 `templates/case-card.md`：

| 字段 | 要求 |
| --- | --- |
| Source | URL、采集日期、来源层级、登记状态 |
| Environment | 任务环境、可观察状态、动作空间 |
| Policy Surface | 可更新的代码、规则、检测器、配置或记忆 |
| Feedback | reward、测试、日志、回放、视频或人类评价 |
| HL Update | 下一轮修改应先读什么、改哪里 |
| Verification | 哪条命令或 replay 能证明没有破坏旧行为 |
| Course Link | 对应章节、讲义、练习或 runnable example |

如果来源还没有进入 case card，先用 `templates/reproduction-note.md` 记录来源状态、复现范围、缺失保真度、反驳路径和下一步实验。复现记录通过后，才升级为 case card、实验记录或研究日志条目。

## 禁止声明

- 不把待直接复核的一手帖写成已经直接读过。
- 不把二手转述中的分数写成课程 benchmark。
- 不把轻量 replay 写成真实 Atari、VizDoom 或 MuJoCo 高保真复现。
- 不公开私有原文、会议纪要、私有链接、X cookie、API token 或私有日志。
- 不把 research hypothesis 写成主线结论。

## 维护命令

```bash
npm run source:case:check
npm run x:sources:check
npm run source:registry:check
npm run verify
```
