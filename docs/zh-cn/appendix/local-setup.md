---
title: 本地运行与排错
description: Heuristic Learning 仓库的安装、运行、验证和常见问题处理
---

# 本地运行与排错

本页给学生和贡献者提供一条稳定的本地路径：先跑文档，再跑示例，最后跑统一验证。遇到失败时，先看 [排错决策树](/zh-cn/appendix/troubleshooting-tree)，按失败面定位诊断命令、修复动作和复验命令。

## 环境要求

| 工具 | 用途 | 建议 |
| --- | --- | --- |
| Node.js | VitePress、lint、npm scripts | 18+，CI 使用 20 |
| npm | 安装依赖和运行脚本 | 使用 `npm install` 或 CI 的 `npm ci` |
| Python | 运行示例、测试和检查脚本 | 3.10+，CI 使用 3.12 |

课程的主线示例刻意保持纯 Python，不依赖 MuJoCo、Atari、VizDoom、OpenCV 或 EnvPool。真实环境接入是后续高保真验证，不是入门前提。

## 第一次运行

```bash
npm install
npm run dev
```

本地文档默认地址：

```text
http://127.0.0.1:5173/heuristic-learning/
```

如果只想确认仓库是否完整，直接运行：

```bash
npm run verify
```

## 推荐验证顺序

当 `npm run verify` 失败时，不要直接改策略。按下面顺序拆开跑：

```bash
npm run lint
npm run examples:test
npm run examples:feedback
npm run examples:reports:check
npm run ablation:plan:check
npm run cases:check
npm run source:case:check
npm run source:registry:check
npm run claims:registry:check
npm run teaching:registry:check
npm run speaker:notes:check
npm run exercises:check
npm run contribution:contract:check
npm run reproducibility:check
npm run troubleshooting:tree:check
npm run learning:outcomes:check
npm run checkpoints:check
npm run metrics:check
npm run paper:blueprint:check
npm run course:manifest:check
npm run course:structure:check
npm run docs:routes:check
npm run build
```

这条顺序对应 HL 的维护纪律：先确认代码和反馈通道可用，再判断课程结构是否漂移。

## 常见失败

| 失败位置 | 常见原因 | 处理方式 |
| --- | --- | --- |
| `npm install` | Node 版本过旧或 lockfile 与 npm 版本不兼容 | 切到 Node 18+，重新安装 |
| `examples:test` | 策略行为或 replay 边界被改坏 | 先读对应 `tests/test_*.py`，再读 `examples/*/README.md` |
| `examples:reports:check` | `latest.json` 缺少 policies、feedback 或 candidate update | 重新跑对应 `examples:*:feedback`，检查 feedback loop |
| `cases:check` | 案例页、来源状态、绑定示例、failure mode、学习成果或命令漂移 | 更新 `/case-registry.json` 或 [案例矩阵](/zh-cn/appendix/case-registry) |
| `source:case:check` | 来源到 case card 的路径、必备 artifact、状态门槛或禁止声明漂移 | 更新 `/source-to-case-playbook.json` 或 [来源到案例 Playbook](/zh-cn/appendix/source-to-case-playbook) |
| `ablation:plan:check` | 消融变量、示例、指标、不变量、证据路径或验证命令漂移 | 更新 `/ablation-plan.json` 或 [消融计划](/zh-cn/appendix/ablation-plan) |
| `source:registry:check` | 来源状态、X 证据或已复现条目缺失 | 更新 [来源登记](/zh-cn/appendix/source-registry)，不要把线索写成事实 |
| `claims:registry:check` | 研究命题没有绑定证据页、示例或验证命令 | 更新 `/claims-registry.json` 或 [研究命题](/zh-cn/theory/research-propositions) |
| `teaching:registry:check` | 讲义、Lab、阅读材料或演示命令漂移 | 更新 `/teaching-registry.json` 或对应讲义页 |
| `exercises:check` | 练习题、输入材料、示例、验收命令、学习单元或 Rubric 漂移 | 更新 `/exercise-registry.json` 或 [练习集](/zh-cn/appendix/exercises) |
| `contribution:contract:check` | 贡献类型、证据字段、必备路径、验证命令或禁止材料漂移 | 更新 `/contribution-contract.json`、`CONTRIBUTING.md` 或 PR 模板 |
| `reproducibility:check` | 可复现性证据、命令、通过条件或已知边界漂移 | 更新 `/reproducibility-checklist.json` 或 [可复现性检查清单](/zh-cn/appendix/reproducibility) |
| `troubleshooting:tree:check` | 失败面、诊断命令、修复动作、复验命令或关联页面漂移 | 更新 `/troubleshooting-tree.json` 或 [排错决策树](/zh-cn/appendix/troubleshooting-tree) |
| `learning:outcomes:check` | 学习成果、练习、Rubric、证据路径或验证命令漂移 | 更新 `/learning-outcomes.json` 或 [学习成果矩阵](/zh-cn/appendix/learning-outcomes) |
| `checkpoints:check` | 阶段自测、证据、命令、通过条件或常见失败漂移 | 更新 `/checkpoint-registry.json` 或 [阶段检查点](/zh-cn/appendix/checkpoints) |
| `metrics:check` | 评估指标、示例、命题、证据路径或验证命令漂移 | 更新 `/evaluation-metrics.json` 或 [评估指标矩阵](/zh-cn/appendix/evaluation-metrics) |
| `paper:blueprint:check` | 论文章节、命题、指标、示例、证据路径或边界漂移 | 更新 `/paper-blueprint.json` 或 [论文蓝图](/zh-cn/appendix/paper-blueprint) |
| `speaker:notes:check` | 讲者备注、demo 节点、讨论题、常见误解或 exit ticket 漂移 | 更新 `/speaker-notes.json` 或 [讲者备注](/zh-cn/appendix/speaker-notes) |
| `course:manifest:check` | manifest 字段、路径或 schema 漂移 | 更新 `/course-manifest.json` 和 `/course-manifest.schema.json` |
| `course:structure:check` | 页面、脚本、示例、报告或 syllabus 不一致 | 按报错补齐对应页面或路径 |
| `docs:routes:check` | 本地 dev server 页面或 JSON route 不可达 | 检查 VitePress base、public 文件和站内路由 |
| `build` | VitePress 页面链接、frontmatter 或组件错误 | 先定位报错页面，再跑本地 dev server |

实验报告的公共结构见 [`/experiment-report.schema.json`](/experiment-report.schema.json)。如果新增报告字段，可以扩展具体示例；但主线报告不能缺少 baseline/heuristic、feedback 和 candidate update。

## 缓存清理

正常贡献不需要提交构建输出。验证后可以清理：

```bash
rm -rf docs/.vitepress/dist docs/.vitepress/cache
find examples tests -name '__pycache__' -type d -prune -exec rm -rf {} +
```

不要提交 `docs/.vitepress/dist`。GitHub Pages workflow 会在部署时重新构建。

`.gitignore` 已忽略 Node 依赖、VitePress 构建输出、Python `__pycache__`、本地缓存和 `.env` 文件。`npm run course:structure:check` 会检查这些忽略规则是否存在，并确认 `docs/.vitepress/dist`、`docs/.vitepress/cache` 和示例目录下的 `__pycache__` 没有残留。

## 新增示例最短路径

新增主线示例时，至少要补齐：

```text
examples/<name>/run.py
examples/<name>/feedback_loop.py
examples/<name>/README.md
tests/test_<name>.py
experiments/<name>/latest.json
```

还要同步：

- `package.json` 示例命令。
- [课程大纲](/zh-cn/syllabus/) 的实验矩阵。
- [可运行示例](/zh-cn/examples/) 的说明。
- `/course-manifest.json` 的 example 条目。
- `scripts/check-course-structure.py` 的 `EXAMPLES` 配置。

完成后运行：

```bash
npm run examples:feedback
npm run examples:test
npm run verify
```

## 验收口径

本地 HTTP 200、build 成功和测试通过都是必要证据，但不是研究结论。一个 HL 贡献只有同时具备来源、probe、baseline、patch、report 和 regression，才可以进入主线课程。
