---
title: X 来源案例
description: 从公开讨论中抽取可验证的 Heuristic Learning 问题
---

# X 来源案例

案例定位：

| 维度 | 内容 |
| --- | --- |
| 类型 | 来源线索案例 |
| 对应示例 | `examples/shape-from-shading/`；其余线索待转化 |
| Failure mode | 明暗塑形探针已显式化默认光照假设；其余线索待复核 |
| 学习重点 | 公开讨论如何进入来源登记、案例库和研究问题 |

本页把 X 公开讨论拆成可学习、可验证的课程入口。它不替代论文和代码 artifact；它只回答一个问题：一条公开讨论怎样被转成案例、实验或研究问题，而不越过证据边界。Jiayi Weng 相关讨论仍是 HL 主线来源；其他帖子只有在能落到独立文献与明确课程问题时才进入本页。

来源矩阵见 [`/x-sources.json`](/x-sources.json)。`npm run x:sources:check` 会检查本页和来源登记是否区分“已读到的材料”“已知 URL 但待复核的材料”和“待采集方向”。

## 公开讨论入口

| 日期 | 来源 | 证据层级 | 学习落点 |
| --- | --- | --- | --- |
| 2025-11-07 | `@0xdeusyu` 关于 shape from shading 的中文科普帖 | X 原帖 URL + 独立同行评议文献 | [视觉先验案例](/zh-cn/cases/visual-prior/)、`examples/shape-from-shading/` |
| 2026-05-08 | Jiayi Weng / `@Trinkle23897` 原帖，被 `@0xLogicrw` 中文转述引用 | 一手原帖 + 二手中文摘要 | [Breakout 案例](/zh-cn/cases/breakout/)、[Ant Gait 案例](/zh-cn/cases/ant-gait/) |
| 2026-05-19 | `@0xLogicrw` 转述 Paul Garnier 受 Jiayi 文章启发的流体控制实验 | 二手中文摘要 + 被引用原帖 | 后续可扩展为流体控制案例 |
| 2026-06-26 | `@safaricheung` 转述 Android 地震预警 | X 二手摘要 + USGS、Google 与 Science 论文 | [技术与社会研究卡](/zh-cn/cases/technology-society/) |
| 2026-06-29 | `@dotey` 转述 Brain2Qwerty v1/v2 | X 二手摘要 + Nature Neuroscience、Meta 预印本与项目页 | [技术与社会研究卡](/zh-cn/cases/technology-society/) |
| 2026-06-29 | `@yatingzhao_ux` 阅读许怡《机器时代》 | 读书摘要 + 书目、作者档案与相关论文 | [技术与社会研究卡](/zh-cn/cases/technology-society/) |
| 2026-07-01 | `@Phoenixyin13` 转述 Economic Connectedness | X 二手摘要 + 两篇 Nature 论文 | [技术与社会研究卡](/zh-cn/cases/technology-society/) |
| 2026-07-14 | `@AYi_AInotes` 转述 Demis Hassabis 的前沿 AI 治理文章 | X 二手摘要 + 作者原文 | [AI 治理与医疗研究卡](/zh-cn/cases/ai-governance-medical/) |
| 2026-07-14 | `@Phoenixyin13` 转述 *Language Models Need Sleep* | X 二手摘要 + arXiv v2 预印本 | [AI 治理与医疗研究卡](/zh-cn/cases/ai-governance-medical/) |
| 2026-01-13 | `@aigclink` 介绍 MedGemma 1.5 与 MedASR | X 二手摘要 + Google 发布说明与 model cards | [AI 治理与医疗研究卡](/zh-cn/cases/ai-governance-medical/) |

## 2025-11-07：视觉先验与欠定输入

[`@0xdeusyu` 原帖](https://x.com/0xdeusyu/status/1986696571006951603)用上下明暗相反的圆点解释凹凸错觉。课程没有直接采用“大脑篡改证据”的结论，而是把帖子拆成四个可以分别核验的问题：

- 1744 年的历史归因由后世同行评议文献支持，但本轮没有直接读到 Gmelin 的原始记录。
- Ramachandran 1988 年的 Nature 论文和同年 Scientific American 文章都已确认。
- “单一光源假设”与“光从上方的先验”不是同一个主张，不能都笼统归给一篇论文。
- 光照先验会受主动经验与场景光源影响，因此不应写成不可改变的硬编码常量。

课程把它转成“视觉先验与欠定输入”抽取卡，落到 [视觉先验案例](/zh-cn/cases/visual-prior/) 和零依赖探针：

```bash
npm run examples:shape-from-shading
npm run examples:test
```

`examples/shape-from-shading/` 只显式展示 observation、assumed light 和 inferred shape 的关系，不模拟人脑，也不把单个观察者的知觉反应推广成普遍定律。

## 2026-06-26 至 07-01：技术与社会研究批次

四条收藏已整理到 [技术与社会：四条 X 线索的证据审计](/zh-cn/cases/technology-society/)。对应的课程概念是：

- **众包传感与公共基础设施**：Android 地震预警是事件开始后的 early warning，不是 earthquake prediction。
- **非侵入式脑机接口的外部有效性**：Brain2Qwerty v2 的实验指标不能直接外推到无法打字的患者。
- **自动化的组织后果**：《机器时代》的田野材料需要按工厂、岗位和章节抽取，不能压成“机器是否裁员”。
- **经济连接度与因果边界**：县级和学校级结果不能直接变成个人“蹭富人圈子”的致富建议。

这四张卡都保留为非 runnable 研究入口；它们完成了来源和主张核验，但还没有定义数据夹具、failure probe 和实验报告。

## 2026-01-13 与 07-14：AI 治理、持续学习与医疗模型批次

三条收藏已整理到 [AI 治理、持续学习与医疗模型的证据审计](/zh-cn/cases/ai-governance-medical/)。对应的课程概念是：

- **前沿 AI 标准机构与可执行治理**：Demis Hassabis 的 FINRA 式机构、30 天预审和季度 benchmark 是政策提案，不是已经生效的规则；“可读输出 token”也需要单独验证忠实性。
- **持续学习的证据边界**：Sleep 预印本验证了特定 consolidation 与 synthetic rehearsal 设计，不能写成已经普遍、彻底解决 catastrophic forgetting。
- **医疗基础模型的部署边界**：MedGemma 与 MedASR 的开放权重、本地运行和 benchmark 成绩，不等同于临床有效、合规或获准直接诊疗。

这三张卡同样没有 runnable example。后续如果进入实验，应分别补治理阈值模拟、持续学习回归套件与医疗场景分层验证，不能只复述文章或 model card 的成功数字。

## 2026-05-08：Jiayi 原帖

已知公开 URL 指向 Jiayi Weng 的原帖：`https://x.com/Trinkle23897/status/2052596837547495549`。在直接读到并复核原帖之前，课程只把它当作“已知 URL、待直接复核的一手来源”，不扩写未验证细节。

课程中只抽取三个可验证主张：

- Breakout 的学习对象是策略代码与实验日志，而不是重新训练神经网络。
- MuJoCo Ant 显示连续控制也可以被压缩成可维护的 heuristic controller。
- 复杂感知仍是边界，后续更合理的方向是感知模型与可维护规则系统混合。

## 课程抽取卡

下面三张卡说明公开讨论如何进入学习路径。每张卡都必须保留来源层级、证据状态、学习落点、验证命令和边界。

| ID | 概念 | 可学习、可验证主张 | 落点 | 验证 |
| --- | --- | --- | --- | --- |
| `breakout-code-as-memory` | 代码作为经验记忆 | Breakout 案例把学习结果保存在球路预测、卡球检测、回归测试和实验日志中，而不是保存在新训练的神经网络权重中。分数变化只来自二手中文转述，不能当作课程复现结果。 | [Breakout 案例](/zh-cn/cases/breakout/)、`examples/breakout-replay/` | `npm run examples:breakout-replay`、`npm run examples:breakout-replay:feedback`、`npm run examples:test` |
| `ant-controller-as-readable-policy` | 可读控制器作为策略 | Ant 案例把连续控制问题压缩成 CPG、stance duty、speed adaptation 和 yaw feedback 等可维护控制器组件。 | [Ant Gait 案例](/zh-cn/cases/ant-gait/)、`examples/ant-gait-replay/` | `npm run examples:ant-gait-replay`、`npm run examples:ant-gait-replay:feedback`、`npm run examples:test` |
| `hybrid-perception-boundary` | 感知与规则的混合边界 | 复杂视觉感知不应被硬写成 if-else；更稳妥的 HL 架构应把感知模型、可维护规则、日志审查和周期性数据更新分层。 | [RL/DL/HL 对照](/zh-cn/stage-3/)、[研究路线图](/zh-cn/appendix/research-roadmap) | `npm run x:sources:check`、`npm run claims:registry:check` |

第三张卡没有 runnable example，因此只能作为研究问题和讨论入口。只有当它转成最小环境、实验报告和测试后，才能进入“已复现”层级。

对应到课程实验：

- `examples/breakout-replay/` 复现“落点预测和反射处理”这个最小策略对象。
- `examples/ant-gait-replay/` 复现“CPG、stance duty、yaw feedback”这个连续控制策略对象。
- [研究框架](/zh-cn/theory/research-framework) 把这些主张写成“更新对象、反馈通道、验证边界”的课程语言。

## 2026-05-19：流体控制延展方向

另一个公开讨论方向指向受 Jiayi 文章启发的流体力学控制，已知 URL 为 `https://x.com/0xLogicrw/status/2056695371984982195`。课程目前不把它写成已验证结论，只记录为待结构化案例：

- 可能的环境：流体动力学控制或工业仿真。
- 可能的 baseline failure：训练型控制器跨设备或跨时长泛化失败。
- 可能的 HL 对象：短代码控制规则、诊断日志、仿真测试。
- 下一步：找到被引用原帖和公开代码，再决定是否转成 `examples/fluid-control-replay/`。

## 阅读规则

X 来源进入主线课程前必须满足：

1. 有稳定 URL。
2. 区分一手作者原帖、二手转述和评论。
3. 至少落到一个案例页、示例代码或来源状态说明。
4. 不把二手转述中的数值和归因写成未验证事实；优先用公开代码 artifact 交叉验证。
