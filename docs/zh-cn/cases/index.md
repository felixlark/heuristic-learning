---
title: 案例库
description: Jiayi Weng、X、飞书与公开仓库中的 HL 案例沉淀
---

# 案例库

案例库用于把零散的文章、X 线程、飞书消息和实验仓库整理成课程素材。每个案例都按同一个模板记录：

- 环境是什么？
- 状态如何表示？
- 策略如何写成代码？
- 反馈从哪里来？
- 智能体更新了什么？
- 如何验证没有退化？

所有案例的来源状态统一维护在 [来源登记](/zh-cn/appendix/source-registry)。案例页可以解释问题，但不能替代来源登记。案例到来源、示例、学习成果和验证命令的机器可读映射见 [案例矩阵](/zh-cn/appendix/case-registry)，公共入口为 [`/case-registry.json`](/case-registry.json)。

## 公开主源

Jiayi Weng 的 [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/) 与 [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients) 是当前最高信号源。该仓库包含文章、Atari、MuJoCo、VizDoom 示例和渲染脚本，因此不仅是概念文章，也有实验 artifact。

## 飞书线索：机器人足球

飞书消息搜索中已有一个内部应用方向：

> 把 Heuristic Learning 用在机器人足球中，让系统学出踢足球策略，并固化到系统里。

这条线索对应一个很适合 HL 的问题：现有机器人策略常常是“视觉 YOLO + 大量手工 Rule 规则”。痛点不是完全没有智能，而是 Rule 库维护繁琐、冲突难查、迭代慢。HL 可以把这些规则改造成可测试、可回放、可由编码智能体持续维护的 Heuristic System。

## 飞书线索：交通模拟

飞书消息搜索还定位到一个应用方向：把翁家翌的启发式学习用于武汉东湖交通模拟器。这个方向适合用来讨论规则库、仿真 replay 与人工管制经验如何进入 HL 闭环。

当前已沉淀为 [交通模拟案例](/zh-cn/cases/traffic-simulation/)，但它仍是待验证方向：后续需要补真实仿真接口、固定场景 replay 与最小 runnable example。

## X 线索

X 是重要一手来源。当前已把 FieldTheory cache 命中的 Jiayi 原帖引用和中文转述沉淀为 [X 线索案例](/zh-cn/cases/x-signal/)。后续维护规则：

- 普通搜索搜不到时，优先用 `ft sync --api` 或现有 FieldTheory/X 工具同步。
- 当前 `ft search` 不支持 `--json`，先使用文本输出或直接读取本地 JSONL cache。
- 每个 X 案例必须沉淀成上面的统一模板，而不是只贴链接。

## v1 案例清单

| 案例 | 当前状态 | 下一步 |
| --- | --- | --- |
| MuJoCo / Ant Gait | 已有 yaw-stabilization replay 示例 | 接入真实 Ant-v5/MuJoCo 高保真验证 |
| Atari / Breakout | 已有 wall-reflection replay 示例 | 对齐真实 Atari RAM/vision artifact |
| X / Jiayi 原帖线索 | 已有来源页，关联 Breakout 与 Ant | 继续采集 Jiayi 自己的 thread 和后续评论 |
| VizDoom | 已有 medikit-staging replay 示例 | 对齐真实 EnvPool/OpenCV artifact |
| 机器人足球 | 已有 blocked-lane 最小环境与测试 | 继续接入真实视觉/运动约束 |
| 交通模拟 | 已有 traffic-grid 最小环境与测试 | 对接真实交通仿真 replay |

案例矩阵由下面命令检查：

```bash
npm run cases:check
```
