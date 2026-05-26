# Heuristic Learning

直觉学习（Heuristic Learning, HL）中文研究与动手课程。

这个仓库把 Jiayi Weng 在 [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/) 中提出的 Heuristic Learning 思路，整理成一份中文学习材料：先建立理论直觉，再运行最小示例，最后完成可验证的 heuristic update。

## 目标

- 用中文建立 HL 的基础概念、术语和研究问题。
- 把 Atari、MuJoCo、VizDoom、机器人足球等案例整理成可学习的案例库。
- 提供不依赖重型框架的 runnable examples，让读者先跑通状态、动作、反馈、代码更新的闭环。
- 形成清晰的学习路线、章节、案例、附录、讲义和 Lab 入口，便于读者按同一条主线学习与复盘。

## 快速开始

线上入口：[https://longbiaochen.github.io/heuristic-learning/](https://longbiaochen.github.io/heuristic-learning/)

```bash
npm install
npm run dev
```

打开本地 VitePress 地址后，从 `学习路线` 开始阅读。

推荐学习顺序：

1. 读 [课程大纲](docs/zh-cn/syllabus/index.md) 和 [学习路线](docs/zh-cn/stage-1/index.md)，明确 HL 的反馈、更新对象和验证方式。
2. 跑 `npm run examples:gridworld` 和 `npm run examples:gridworld:feedback`，观察最小闭环。
3. 读 [从 RL/DL 到 HL](docs/zh-cn/stage-3/index.md)，对照不同学习机制的更新对象。
4. 从 [案例库](docs/zh-cn/cases/index.md) 选择一个案例，写出来源状态、failure mode、baseline 和 heuristic patch。
5. 参考 [代码导览](docs/zh-cn/appendix/code-tour.md) 只改一个策略点，再用 `npm run examples:test` 和 `npm run verify` 保护回归。

本地环境、验证顺序和常见失败处理见 [本地运行与排错](docs/zh-cn/appendix/local-setup.md)。
失败面到诊断命令、修复动作和复验命令的机器可读路径已经合并到 [本地运行与排错](docs/zh-cn/appendix/local-setup.md)。
X、公开 artifact、脱敏应用问题和研究假设如何变成 case card 见 [来源到案例 Playbook](docs/zh-cn/appendix/source-to-case-playbook.md)。
把公开 artifact、X 来源或脱敏应用问题升级为案例前，先用 [`templates/reproduction-note.md`](templates/reproduction-note.md) 记录来源状态、复现范围、缺失保真度、反驳路径和下一步实验。
统一学习主线见 [课程地图](docs/zh-cn/course-map/index.md)。
章节级“读、跑、改、复盘”闭环见 [学习单元矩阵](docs/zh-cn/appendix/learning-units.md)。
六个示例的代码阅读顺序见 [代码导览](docs/zh-cn/appendix/code-tour.md)。
能力目标到练习、Rubric 和验证命令的映射见 [学习成果矩阵](docs/zh-cn/appendix/learning-outcomes.md)。
每个阶段学完如何自测见 [阶段检查点](docs/zh-cn/appendix/checkpoints.md)。
研究评估维度、证据路径和命令见 [评估指标矩阵](docs/zh-cn/appendix/evaluation-metrics.md)。
论文或技术报告写作结构见 [论文蓝图](docs/zh-cn/appendix/paper-blueprint.md)。
阅读、代码运行与下一步实验的研究记录见 [研究日志](docs/zh-cn/appendix/research-logbook.md)。
六个示例的后续变量对照见 [消融计划](docs/zh-cn/appendix/ablation-plan.md)。
轻量 replay 到真实 artifact 的保真度缺口见 [Artifact 差距分析](docs/zh-cn/appendix/artifact-gap-analysis.md)。
公开 registry、schema 和 LLM 入口见 [机器可读入口](docs/zh-cn/appendix/public-entrypoints.md)。

## 三步跑通

```bash
npm run examples:gridworld
npm run examples:gridworld:feedback
npm run verify
```

`examples:gridworld` 用来观察最小环境；`examples:gridworld:feedback` 用来看到一次 HL 反馈报告如何写给下一轮智能体；`verify` 用来确认仓库完整。

## 实验矩阵

| 实验 | Failure mode | 运行 | 反馈报告 |
| --- | --- | --- | --- |
| GridWorld | `local_greedy_trap` | `npm run examples:gridworld` | `npm run examples:gridworld:feedback` |
| Robot Soccer | `blocked_shot` | `npm run examples:robot-soccer` | `npm run examples:robot-soccer:feedback` |
| VizDoom Replay | `wasted_pickup` | `npm run examples:vizdoom-replay` | `npm run examples:vizdoom-replay:feedback` |
| Traffic Grid | `spillback` | `npm run examples:traffic-grid` | `npm run examples:traffic-grid:feedback` |
| Breakout Replay | `missed_after_wall_reflection` | `npm run examples:breakout-replay` | `npm run examples:breakout-replay:feedback` |
| Ant Gait Replay | `yaw_drift` | `npm run examples:ant-gait-replay` | `npm run examples:ant-gait-replay:feedback` |

统一测试与报告检查：

```bash
npm run examples:test
npm run examples:feedback
npm run examples:reports:check
npm run code:tour:check
npm run benchmark:summary:check
npm run ablation:plan:check
npm run artifact:gap:check
npm run cases:check
npm run source:case:check
npm run concept:graph:check
npm run slides:check
npm run rubric:check
npm run exercises:check
npm run contribution:contract:check
npm run reproducibility:check
npm run troubleshooting:tree:check
npm run research:projects:check
npm run research:logbook:check
npm run learning:outcomes:check
npm run checkpoints:check
npm run metrics:check
npm run visual:verification:check
npm run completion:audit:check
npm run docs:routes:check
npm run verify
```

六个示例的 baseline failure、heuristic outcome、报告、测试和边界见 [Benchmark 结果摘要](docs/zh-cn/appendix/benchmark-results.md)，机器入口为 [`/benchmark-summary.json`](docs/public/benchmark-summary.json)。

## 仓库结构

```text
docs/                         # VitePress 中文课程文档
  zh-cn/stage-1/              # 学习路线与入门
  zh-cn/stage-2/              # HL 理论框架
  zh-cn/stage-3/              # RL/DL/HL 对照与研究问题
  zh-cn/examples/             # 动手实验说明
  zh-cn/cases/                # Jiayi/X/脱敏应用案例
  zh-cn/appendix/source-to-case-playbook.md # X、artifact、脱敏应用问题和研究假设进入 case card 的路径
  zh-cn/appendix/case-registry.md # 案例到来源、示例、学习成果和命令的矩阵
  zh-cn/appendix/code-tour.md # 六个示例的代码阅读顺序、编辑目标和测试路径
  zh-cn/appendix/local-setup.md # 本地运行与排错
  zh-cn/appendix/learning-units.md # 章节级读、跑、改、复盘矩阵
  zh-cn/appendix/learning-outcomes.md # 能力目标、练习、Rubric 和验证命令矩阵
  zh-cn/appendix/checkpoints.md # 每个学习单元的阶段自测和通过条件
  zh-cn/appendix/evaluation-metrics.md # 研究评估指标、证据路径和验证命令
  zh-cn/appendix/paper-blueprint.md # 论文/技术报告的章节、证据和边界蓝图
  zh-cn/appendix/research-logbook.md # 阅读、示例、研究问题、指标与下一步实验记录
  zh-cn/appendix/public-entrypoints.md # public registries、schemas 和 LLM 入口索引
  zh-cn/appendix/concept-graph.md # 概念到研究问题、示例、讲义和命令的图谱
  zh-cn/appendix/exercises.md # 可布置、可验收的练习题库
  zh-cn/appendix/ablation-plan.md # 六个示例的变量对照与不变量计划
  zh-cn/appendix/artifact-gap-analysis.md # 轻量 replay 到真实 artifact 的保真度差距
  zh-cn/appendix/benchmark-results.md # 六个示例的 benchmark 摘要
  zh-cn/appendix/visual-verification.md # 官方 Browser/IAB 视觉验收矩阵
  zh-cn/appendix/reproducibility.md # 环境、示例、研究问题、教学和站点复现清单
examples/heuristic-gridworld/ # 纯 Python 最小 HL 示例
examples/robot-soccer/        # 机器人足球 blocked-lane 示例
examples/vizdoom-replay/      # VizDoom D1 medikit-staging 回放示例
examples/traffic-grid/        # 交通模拟 downstream spillback 示例
examples/breakout-replay/     # Atari Breakout wall-reflection 回放示例
examples/ant-gait-replay/     # MuJoCo Ant yaw-stabilization 回放示例
experiments/                  # 反馈报告与实验记录
tests/                        # 示例代码测试
templates/reproduction-note.md # 来源到案例前的复现记录模板
```

每个 `examples/*/README.md` 都是独立学习入口，固定包含 failure mode、baseline、heuristic patch、运行命令、反馈报告和测试路径。新增示例时，`npm run course:structure:check` 会检查这些字段，避免示例代码和课程说明漂移。

## 验证标准

```bash
npm run verify
```

`verify` 会执行四类检查：

- lint VitePress theme。
- 跑通所有 Python 示例测试。
- 重新生成 `experiments/*/latest.json`。
- 检查实验报告的 baseline/heuristic、feedback 和 candidate update 结构。
- 检查 `/code-tour.json` 所描述的示例代码阅读顺序、编辑目标、运行命令和测试路径。
- 检查 `/benchmark-summary.json` 与示例 registry、实验报告和测试路径一致。
- 检查 `/ablation-plan.json` 所描述的示例变量对照、评估指标、不变量、证据路径和验证命令。
- 检查 `/artifact-gap-analysis.json` 所描述的轻量 replay、真实 artifact 缺口、下一步实验和验证命令。
- 检查 `/experiment-report.schema.json` 所描述的实验报告公共字段。
- 检查 `/case-registry.json` 所描述的案例页、来源状态、绑定示例、failure mode、学习成果和验证命令。
- 检查 `/source-to-case-playbook.json` 所描述的 X、公开 artifact、脱敏应用问题和研究假设进入 case card 的路径。
- 检查来源登记、`/x-sources.json` 的 X 来源证据状态和“已复现”条目的 runnable example 落点。
- 检查研究问题、讲义 registry、讲义结构、评分 Rubric、学习单元、授课包和完成度审计。
- 检查 `/speaker-notes.json` 所描述的讲者备注、demo 节点、讨论题、常见误解和 exit ticket。
- 检查 `/learning-outcomes.json` 所描述的能力目标到学习单元、练习、Rubric、证据和验证命令的映射。
- 检查 `/checkpoint-registry.json` 所描述的阶段自测问题、证据、命令、通过条件和常见失败。
- 检查 `/evaluation-metrics.json` 所描述的任务结果、失败隔离、更新成本、回归风险和来源边界。
- 检查 `/paper-blueprint.json` 所描述的论文章节、研究问题、指标、示例、证据路径和边界。
- 检查 `/research-logbook.json` 所描述的阅读记录、绑定示例、研究问题、指标、命令、交付物和边界。
- 检查 `/exercise-registry.json` 所描述的练习题、输入材料、示例、交付物和验收命令。
- 检查 `/contribution-contract.json` 所描述的贡献类型、证据字段、必备路径和禁止材料。
- 检查 `/reproducibility-checklist.json` 所描述的环境、示例、研究问题、教学、贡献和站点复现检查。
- 检查 `/troubleshooting-tree.json` 所描述的失败面、诊断命令、修复动作、复验命令和关联页面。
- 检查 `/concept-graph.json` 所描述的核心概念到研究问题、示例、讲义和验证命令的映射。
- 检查 `/research-projects.json` 所描述的研究项目来源、failure mode、示例、交付物和验证命令。
- 检查 `/completion-audit.json` 所描述的目标拆解、必跑命令、证据边界和完成前检查。
- 检查 `/visual-verification.json` 和 `/visual-acceptance-log.json` 所描述的官方 Browser/IAB 视觉验收路径、视口、记录和发布前状态。
- 检查 `course-manifest.json` 与 `course-manifest.schema.json` 的字段、路径、示例入口和 public resources。
- 检查课程页面、示例、实验报告、测试和课程大纲是否互相对齐。
- 启动本地 VitePress dev server 并检查关键页面与 JSON route 可达。
- 构建 VitePress 文档站。

GitHub Actions 中的 `Verify course repository` workflow 会在 PR 和 `main` push 上运行同一条命令；Pages 部署也会先跑 `npm run verify`，再构建发布站点。
阶段性版本和发布检查见 [CHANGELOG.md](CHANGELOG.md)、[发布清单](docs/zh-cn/appendix/release-checklist.md) 与 [视觉与浏览器验收](docs/zh-cn/appendix/visual-verification.md)。
公开发布前还应单独运行 `npm run release:readiness:check`；它会检查官方 Browser/IAB 视觉验收记录，避免把本地绿色构建误写成发布完成。

## 授课与组会

需要把仓库用于组会、课程实验或助教验收时，先读 [教师指南](docs/zh-cn/appendix/instructor-guide.md)。它给出 90 分钟导读、2 小时工作坊、3 讲 + 2 Lab 的组织方式，以及课堂 demo 命令、作业设计和常见故障处理。可直接执行的课堂包见 [授课包](docs/zh-cn/appendix/teaching-pack.md)。4-6 周 mini course 使用 [课程进度表](docs/zh-cn/appendix/course-schedule.md) 安排每周阅读、命令和验收产物。作业题库见 [练习集](docs/zh-cn/appendix/exercises.md)；项目制学习入口见 [研究课题](docs/zh-cn/appendix/research-projects.md)，其中把六个 runnable examples 对应到入门项目、公开 artifact 项目和 capstone 交付物；阅读到实验的记录入口见 [研究日志](docs/zh-cn/appendix/research-logbook.md)；实验设计细则见 [实验协议](docs/zh-cn/appendix/benchmark-protocol.md)。

如果要把 HL 当作研究方向讨论，先读 [研究问题](docs/zh-cn/theory/research-framework.md)：它把当前思想拆成研究问题、证据状态和可反驳路径，避免把未发表论文的观点写成既成结论。
X 来源的证据状态和来源层级见 [X 来源案例](docs/zh-cn/cases/x-signal/index.md) 与 [`/x-sources.json`](docs/public/x-sources.json)。

## 贡献方式

新增理论、案例、实验或讲义前，先读 [CONTRIBUTING.md](CONTRIBUTING.md)。主线贡献必须能说明来源状态、baseline failure、heuristic update、反馈报告、测试路径和 `npm run verify` 结果；PR 模板也会要求填写这些证据。

不要把 API key、私有原文、X/Twitter cookie、私有日志或未脱敏截图写进 issue、PR、文档或实验报告。公开协作前先按 [SECURITY.md](SECURITY.md) 做脱敏和最小化。

## 参考源

- Jiayi Weng, [Learning Beyond Gradients](https://trinkle23897.github.io/learning-beyond-gradients/)
- [`Trinkle23897/learning-beyond-gradients`](https://github.com/Trinkle23897/learning-beyond-gradients)

引用本课程仓库时使用根目录的 [CITATION.cff](CITATION.cff)，并按 [引用与署名](docs/zh-cn/appendix/citation.md) 区分原始来源、课程材料和轻量 replay。许可证见 [LICENSE](LICENSE)，当前为 `CC-BY-NC-SA-4.0`。

## 当前状态

这是 v0.1 教学/研究仓库：理论页、案例索引、六个最小可运行示例、benchmark 摘要、来源矩阵、学习单元、授课包、研究项目矩阵、验证脚本、Browser/IAB 视觉验收和 GitHub Pages 部署已经就位。后续重点是补齐更高保真环境、继续从 Jiayi 的 X 案例抽取实验卡片，并扩展真实环境复现实验。
