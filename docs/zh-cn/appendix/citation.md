---
title: 引用与署名
description: Heuristic Learning 仓库、原始来源和课程材料的引用规则
---

# 引用与署名

课程是一个可学习、可验证研究仓库，不是 Jiayi Weng 原始文章或 `learning-beyond-gradients` artifact 的替代版本。使用课程时，需要区分三类引用：原始思想来源、课程仓库、以及具体实验或案例页。

## 推荐引用

如果引用本课程仓库本身，可以使用根目录的 `CITATION.cff`。当前推荐文本：

```text
Heuristic Learning Contributors. Heuristic Learning: A Chinese Research and Hands-on Course. Version 0.1.0, 2026. https://github.com/felixlark/heuristic-learning
```

如果引用某个具体示例，还应同时写明：

- 示例目录，例如 `examples/breakout-replay/`。
- 实验报告路径，例如 `experiments/breakout-replay/latest.json`。
- 验证命令，例如 `npm run examples:breakout-replay:feedback` 或 `npm run verify`。

## 原始来源必须单独引用

课程的 HL 概念和多个案例来自 Jiayi Weng 的公开文章与 artifact。引用相关思想或原始实现时，应优先引用：

- [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/)
- [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients)
- 对应 X 原帖或公开讨论链接，状态见 [来源登记](/zh-cn/appendix/source-registry)

课程中的 replay 和最小环境是教学压缩版。它们可以说明课程实验如何组织，但不能替代真实 Atari、VizDoom、MuJoCo 或机器人环境中的原始结果。

## 署名边界

| 内容 | 引用方式 |
| --- | --- |
| HL 概念、Jiayi 原始案例 | 引用 Jiayi 公开文章、仓库或 X 原帖 |
| 本课程结构、中文讲义、练习和实验协议 | 引用课程 `CITATION.cff` |
| 轻量 replay 示例 | 引用课程示例目录和报告路径，同时说明它是教学复现 |
| 内部脱敏应用问题 | 不公开引用敏感来源，只引用课程中脱敏后的最小环境 |
| 背景概念材料 | 只作为问题边界参考，不作为 HL 结论证据 |

敏感来源和凭证处理见根目录 `SECURITY.md`。引用页只说明署名边界，不允许替代安全披露流程。

## 复现实验引用格式

建议在报告或论文笔记里保留以下字段：

```text
Case:
Source:
Course example:
Feedback report:
Verification:
Source status:
Limitations:
```

示例：

```text
Case: Breakout wall-reflection intercept
Source: Trinkle23897/learning-beyond-gradients, atari/breakout/heuristic_breakout.py
Course example: examples/breakout-replay/
Feedback report: experiments/breakout-replay/latest.json
Verification: npm run examples:breakout-replay:feedback && npm run verify
Source status: reproduced-lightweight-artifact
Limitations: lightweight replay, not a full Atari environment reproduction
```

## 许可证

根目录 `LICENSE`、`package.json` 和 `CITATION.cff` 当前声明仓库许可证为 `CC-BY-NC-SA-4.0`。如果后续需要把代码示例和课程文档拆成不同许可证，应同步更新：

- `LICENSE`
- `package.json`
- `CITATION.cff`
- 本页
- README
- 发布说明

引用规则和许可证声明必须保持一致，避免读者误以为本课程仓库拥有原始来源的全部版权或实验结论。
