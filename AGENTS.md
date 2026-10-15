# Heuristic Learning Repo Guidance

- This repository is a Chinese research/course repo for Heuristic Learning, not an EasyVibe fork with unchanged content.
- Reuse EasyVibe's VitePress/course structure, but keep public copy, metadata, examples, and README focused on Heuristic Learning.
- Every theory page should point to a runnable example, case study, or source reference.
- Every example must have a short command and a test path. Prefer small, readable code over heavy dependencies.
- Treat Jiayi Weng's `learning-beyond-gradients` article/repo as the highest-signal public source, but phrase unvalidated claims as research hypotheses.
- X/Twitter cases should be integrated into the main learning flow once retrieved through `ft` or supported X API tooling.
- Do not commit generated VitePress build output under `docs/.vitepress/dist`.

## Main-first Policy

- Follow the global `~/.codex/AGENTS.md` main-first development rule: work in the current Local checkout by default and use a worktree only when the global exception list applies.
- Follow the global `~/.codex/AGENTS.md` official browser/GUI automation policy: Chrome plugin for signed-in browser state, Browser plugin for unauthenticated rendering, and Computer Use for native desktop boundaries. Do not bypass it with AppleScript or `osascript` unless the global exception rules are met.
- Preserve existing dirty checkouts. Inspect `git status --short` before editing, and do not stash, commit, remove, or migrate user changes unless explicitly asked.
- When a worktree is genuinely needed, use `codex/<repo>-<short-task>` branch names, isolate dependencies/ports/databases/device state inside that checkout, and clean up with `git worktree remove <path>` after merge or abandonment.

## 合并前评审

合并前须等待 Codex 自动评审完成，且评审意见已全部处理清零（无未解决的阻塞性评论）之后，方可合并。不得在评审结果出来之前合并。

### Pre-merge review (English translation)

Before merging, wait for Codex automatic review to finish and address all review feedback, leaving no unresolved blocking comments. Do not merge before the review results are available.

## 限制类改动规则

1. 新增或调小任何上限、槽位、名额、闸门、门槛、退避（包括并发数、负载准入、超时退避等）时，PR 正文须单列「新增限制」一节，写明位置、默认值和依据，经仓库负责人定稿后才可合并。此类改动不得绕过 PR 直接进入 main。
2. 资源类参数默认不限、只观测；确需限制时须通过显式配置开启，不得在代码中写死最大值。外部硬限制（如外部接口限流、部署锁）须在注释中写明来源。
