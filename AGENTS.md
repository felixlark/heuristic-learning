# Heuristic Learning Repo Guidance

- This repository is a Chinese research/course repo for Heuristic Learning, not an EasyVibe fork with unchanged content.
- Reuse EasyVibe's VitePress/course structure, but keep public copy, metadata, examples, and README focused on Heuristic Learning.
- Every theory page should point to a runnable example, case study, or source reference.
- Every example must have a short command and a test path. Prefer small, readable code over heavy dependencies.
- Treat Jiayi Weng's `learning-beyond-gradients` article/repo as the highest-signal public source, but phrase unvalidated claims as research hypotheses.
- X/Twitter cases should be integrated into the main learning flow once retrieved through `ft` or supported X API tooling.
- Do not commit generated VitePress build output under `docs/.vitepress/dist`.

## Worktree Policy

- Follow the global `~/.codex/AGENTS.md` worktree-first rule for Codex development: new non-read-only coding or multi-file documentation tasks should start in a dedicated Codex-managed worktree.
- Use the Local checkout only for read-only investigation, final handoff/inspection, tasks that must reuse a single running app/server, or when the user explicitly asks to stay local.
- Branch names should use `codex/<repo>-<short-task>`; manual long-lived worktree directories should use `~/Projects/<repo>-<short-task>`.
- Initialize dependencies inside each worktree and keep ports, databases, device/simulator state, build outputs, and ignored local config isolated per checkout.
- Preserve existing dirty checkouts. Inspect `git status --short` before editing, and do not stash, commit, remove, or migrate user changes unless explicitly asked.
- After merge or abandonment, clean up with `git worktree remove <path>` and use `git worktree prune` only for stale metadata.
