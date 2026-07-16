---
title: 明暗如何变成凹凸：视觉先验案例
description: 用 shape from shading 区分图像输入、场景假设与知觉解释
---

# 明暗如何变成凹凸：视觉先验案例

这张图不是在证明“大脑篡改了像素”，而是在暴露一个更基础的问题：**单幅图像中的明暗渐变，不能唯一决定物体形状、材质和光源方向。** 视觉系统必须综合场景线索与先验，在多个解释之间做选择。

<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 720 300" role="img" aria-labelledby="sfs-title sfs-desc">
  <title id="sfs-title">明暗塑形的歧义探针</title>
  <desc id="sfs-desc">两个圆盘具有相反的纵向明暗渐变；凹凸判断取决于假设的光照方向。</desc>
  <defs>
    <linearGradient id="case-top-bright" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f8fafc"/>
      <stop offset="1" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="case-bottom-bright" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#334155"/>
      <stop offset="1" stop-color="#f8fafc"/>
    </linearGradient>
  </defs>
  <rect width="720" height="300" rx="24" fill="#0f172a"/>
  <circle cx="220" cy="130" r="92" fill="url(#case-top-bright)"/>
  <circle cx="500" cy="130" r="92" fill="url(#case-bottom-bright)"/>
  <g fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="18" text-anchor="middle">
    <text x="220" y="260">上亮下暗</text>
    <text x="500" y="260">上暗下亮</text>
  </g>
</svg>

在“光大致来自上方”的简化假设下，左边通常更符合凸面解释，右边更符合凹面解释。把整张刺激旋转 180° 后，**同一个图形资产**的屏幕方向和视网膜方向都发生了变化，所以不能说“眼睛收到的像素完全一样”；准确说法是：仅改变相对方向，就足以改变知觉解释。

## 来源核验

本案例由 [`@0xdeusyu` 的 X 帖](https://x.com/0xdeusyu/status/1986696571006951603)触发，但不直接继承帖文的修辞性结论。逐项核验结果如下：

| 帖文线索 | 核验结果 | 课程写法 |
| --- | --- | --- |
| 1744 年已有观察 | 后续同行评议文献把最早记录追溯到 Gmelin 1744 年在伦敦皇家学会报告的 relief inversion；本轮未直接取得 1744 年原始文本 | 写为“后世文献追溯至 1744 年”，不写成已直接复核原始记录 |
| Ramachandran 1988 年在 Nature 系统研究 | 已确认。论文说明 shape from shading 是一种全局操作，并报告视觉解释倾向于为整个图像假设单一光源 | 只把“全局、单一光源假设”归给该论文 |
| 《科学美国人》做过专题 | 已确认。Ramachandran 的 *Perceiving Shape from Shading* 刊于 1988 年 8 月号 | 作为面向大众的作者自述，不替代 Nature 论文 |
| 大脑默认光从上方照 | 有大量实验支持“light-from-above prior”，但它不是不可改变的硬编码常量；实验显示主动经验与场景光线会改变判断 | 写为可适应的知觉先验，并保留凸面偏好、个体差异和场景线索 |
| 大脑“篡改证据” | 这是传播性比喻，不是严谨机制描述 | 改写为“在欠定输入上做带先验的推断” |

关键文献：

- V. S. Ramachandran, [Perception of shape from shading](https://doi.org/10.1038/331163a0), *Nature* 331, 163–166 (1988)。
- V. S. Ramachandran, [Perceiving Shape from Shading](https://doi.org/10.1038/scientificamerican0888-76), *Scientific American* 259(2), 76–83 (1988)。
- Wendy J. Adams, Erich W. Graf, Marc O. Ernst, [Experience can change the ‘light-from-above’ prior](https://doi.org/10.1038/nn1312), *Nature Neuroscience* 7, 1057–1058 (2004)。
- Baoxia Liu, James T. Todd, [Perceptual biases in the interpretation of 3D shape from shading](https://doi.org/10.1016/j.visres.2004.03.024), *Vision Research* 44, 2135–2145 (2004)。
- Michael J. Proulx, [The perception of shape from shading in a new light](https://doi.org/10.7717/peerj.363), *PeerJ* 2:e363 (2014)。

## 把知觉先验写成可检查的 heuristic

最小探针只保留两个字段：圆盘哪一边更亮，以及系统当前假设光来自上方还是下方。

```bash
npm run examples:shape-from-shading
```

输出包含三组对照：

1. 上亮 + 上方光照假设 → `convex`。
2. 旋转后下亮 + 同一个上方光照假设 → `concave`。
3. 上亮 + 明确的下方场景光线 → `concave`。

聚焦测试：

```bash
python3 -m unittest tests/test_shape_from_shading.py
```

这不是人类视觉模型，也不声称所有观察者都会给出同样回答。它把“先验 + 当前证据 → 解释”显式化，使旋转、冲突光源和经验更新可以变成 regression probe。

## 对 Heuristic Learning 的启发

视觉先验和工程 heuristic 有相同的维护问题：

- 一个在常见环境中高效的默认规则，可能在非常规光照下稳定地产生错误。
- 规则不应伪装成输入事实；日志需要分开记录 observation、assumption 和 inference。
- 更强的场景线索出现时，系统应允许局部证据压过默认先验。
- 经验可以改变先验，因此更新对象不只是一条 if-else，也可能是先验权重、适用条件和冲突处理顺序。

因此，“眼见为实”的更好反例不是“大脑不可信”，而是：**任何从不完整观测到行动的系统，都需要公开自己的默认设定，并为默认设定失效准备测试。**
