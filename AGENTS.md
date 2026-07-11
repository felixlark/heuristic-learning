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
