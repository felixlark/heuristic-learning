---
title: 页面幻灯片
description: Heuristic Learning 页面级幻灯片功能说明
---

# 页面幻灯片

HL 不再把“幻灯片”作为单独学习章节。学习时请从 [课程大纲](/zh-cn/syllabus/) 或 [学习路线](/zh-cn/stage-1/) 进入正文页；每个正文页右上角都有 `幻灯片` 按钮，可以把当前 Markdown 页面临时转换成可翻页的浏览器幻灯片。

页面级幻灯片适合三种场景：

- 课堂或组会中直接讲当前页面。
- 读书会中把一个概念页拆成若干页讨论。
- 复盘实验时把案例、命令和报告按页播放。

## 使用方式

1. 打开任意正文页，例如 [HL 基础概念](/zh-cn/stage-2/)。
2. 点击页面右上角的 `幻灯片` 按钮。
3. 用方向键翻页；按 `Esc` 或右上角关闭按钮返回正文。

幻灯片只读取当前页面已经渲染出的内容，不改变 Markdown 源文件，也不会替代正文学习顺序。

## 学习入口

| 想学习什么 | 进入页面 |
| --- | --- |
| 先建立概念 | [HL 基础概念](/zh-cn/stage-2/) |
| 理解与 RL/DL 的区别 | [从 RL/DL 到 HL](/zh-cn/stage-3/) |
| 跑通最小闭环 | [可运行示例](/zh-cn/examples/) |
| 阅读案例 | [案例库](/zh-cn/cases/) |
| 完成练习 | [练习集](/zh-cn/appendix/exercises) |

## 机器可读材料

以下文件仍保留给授课包、讲者备注和自动校验使用；它们不是主学习入口：

- [`/teaching-registry.json`](/teaching-registry.json)
- [`/teaching-registry.schema.json`](/teaching-registry.schema.json)
- [`/slide-deck.json`](/slide-deck.json)
- [`/slide-deck.schema.json`](/slide-deck.schema.json)
- [`/speaker-notes.json`](/speaker-notes.json)
- [`/speaker-notes.schema.json`](/speaker-notes.schema.json)
