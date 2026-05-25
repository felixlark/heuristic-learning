---
title: X 线索案例
description: 从 X / FieldTheory cache 抽取 Jiayi Heuristic Learning 的一手和二手传播线索
---

# X 线索案例

本页记录已经通过本地 `ft` / FieldTheory cache 命中的 X 线索。它的作用不是替代公开代码和文章，而是把社区传播中的主张拆成可验证的课程入口。把 X 线索转成 case card 的完整路径见 [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook)。

机器可读 X 线索矩阵见 [`/x-sources.json`](/x-sources.json)，字段约束见 [`/x-sources.schema.json`](/x-sources.schema.json)。`npm run x:sources:check` 会检查本页、来源登记和 LLM 入口是否区分 cached、referenced-not-cached 与 to-collect 三种状态。

## 已命中线索

| 日期 | 来源 | 证据层级 | 本仓库落点 |
| --- | --- | --- | --- |
| 2026-05-08 | Jiayi Weng / `@Trinkle23897` 原帖，被 `@0xLogicrw` 中文转述引用 | 一手原帖 + 二手中文摘要 | [Breakout 案例](/zh-cn/cases/breakout/)、[Ant Gait 案例](/zh-cn/cases/ant-gait/) |
| 2026-05-19 | `@0xLogicrw` 转述 Paul Garnier 受 Jiayi 文章启发的流体控制实验 | 二手中文摘要 + 被引用原帖 | 后续可扩展为流体控制案例 |

## 2026-05-08：Jiayi 原帖

FieldTheory cache 中 `https://x.com/0xLogicrw/status/2052701677615218717` 引用了 Jiayi Weng 的原帖：

```text
https://x.com/Trinkle23897/status/2052596837547495549
```

当前本地 `ft show 2052596837547495549` 返回 `Bookmark not found`，所以本仓库只能把 Jiayi 原帖标为 `referenced-not-cached`。在通过 `ft sync --api`、X API 或公开网页直接读到原帖前，不能扩写或引用原帖的未验证细节。

课程中只抽取三个可验证主张：

- Breakout 的学习对象是策略代码与实验日志，而不是重新训练神经网络。
- MuJoCo Ant 显示连续控制也可以被压缩成可维护的 heuristic controller。
- 复杂感知仍是边界，后续更合理的方向是感知模型与可维护规则系统混合。

## 课程抽取卡

`/x-sources.json` 中的 `extraction_cards` 把 X 线索转成课程入口。每张卡都必须保留来源、证据状态、落点、命令和边界。

| ID | 概念 | 课程化主张 | 落点 | 验证 |
| --- | --- | --- | --- | --- |
| `breakout-code-as-memory` | 代码作为经验记忆 | Breakout 案例把学习结果保存在球路预测、卡球检测、回归测试和实验日志中，而不是保存在新训练的神经网络权重中。分数变化只来自二手中文转述，不能当作本仓库复现结果。 | [Breakout 案例](/zh-cn/cases/breakout/)、`examples/breakout-replay/` | `npm run examples:breakout-replay`、`npm run examples:breakout-replay:feedback`、`npm run examples:test` |
| `ant-controller-as-readable-policy` | 可读控制器作为策略 | Ant 案例把连续控制问题压缩成 CPG、stance duty、speed adaptation 和 yaw feedback 等可维护控制器组件。 | [Ant Gait 案例](/zh-cn/cases/ant-gait/)、`examples/ant-gait-replay/` | `npm run examples:ant-gait-replay`、`npm run examples:ant-gait-replay:feedback`、`npm run examples:test` |
| `hybrid-perception-boundary` | 感知与规则的混合边界 | 复杂视觉感知不应被硬写成 if-else；更稳妥的 HL 架构应把感知模型、可维护规则、日志审查和周期性数据更新分层。 | [RL/DL/HL 对照](/zh-cn/stage-3/)、[研究路线图](/zh-cn/appendix/research-roadmap) | `npm run x:sources:check`、`npm run claims:registry:check` |

第三张卡没有 runnable example，因此只能作为研究命题和讨论入口。只有当它转成最小环境、实验报告和测试后，才能进入“已复现”层级。

对应到本仓库：

- `examples/breakout-replay/` 复现“落点预测和反射处理”这个最小策略对象。
- `examples/ant-gait-replay/` 复现“CPG、stance duty、yaw feedback”这个连续控制策略对象。
- [研究框架](/zh-cn/theory/research-framework) 把这些主张写成“更新对象、反馈通道、验证边界”的课程语言。

## 2026-05-19：流体控制延展线索

FieldTheory cache 中 `https://x.com/0xLogicrw/status/2056695371984982195` 指向一个受 Jiayi 文章启发的流体力学控制方向。当前本仓库不把它写成已验证结论，只记录为待结构化案例：

- 可能的环境：流体动力学控制或工业仿真。
- 可能的 baseline failure：训练型控制器跨设备或跨时长泛化失败。
- 可能的 HL 对象：短代码控制规则、诊断日志、仿真测试。
- 下一步：找到被引用原帖和公开代码，再决定是否转成 `examples/fluid-control-replay/`。

当前 `ft search "fluid" --limit 20` 和 `ft search "2056695371984982195" --limit 20` 未命中该线索，因此 `/x-sources.json` 将它标为 `to-collect`。

## 维护规则

X 线索进入主线课程前必须满足：

1. 有稳定 URL。
2. 区分一手作者原帖、二手转述和评论。
3. 至少落到一个案例页、示例代码或来源登记条目。
4. 不把二手转述中的数值和归因写成未验证事实；优先用公开代码 artifact 交叉验证。

维护本页后运行：

```bash
npm run x:sources:check
npm run source:case:check
npm run source:registry:check
npm run verify
```
