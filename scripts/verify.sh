#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

cleanup_generated() {
  rm -rf docs/.vitepress/dist docs/.vitepress/cache __pycache__
  find . -path '*/__pycache__' -type d -prune -exec rm -rf {} +
}

cleanup_generated
trap cleanup_generated EXIT

echo "==> Linting VitePress theme"
npm run lint

echo
echo "==> Testing runnable examples"
npm run examples:test

echo
echo "==> Regenerating and checking experiment reports"
npm run examples:feedback
npm run examples:reports:check
npm run examples:registry:check
npm run code:tour:check
npm run benchmark:summary:check
npm run ablation:plan:check
npm run artifact:gap:check

echo
echo "==> Checking source registry"
npm run source:registry:check
npm run cases:check
npm run x:sources:check
npm run source:case:check

echo
echo "==> Checking claims registry"
npm run claims:registry:check

echo
echo "==> Checking teaching registry"
npm run teaching:registry:check

echo
echo "==> Checking slide deck"
npm run slides:check

echo
echo "==> Checking speaker notes"
npm run speaker:notes:check

echo
echo "==> Checking rubric"
npm run rubric:check

echo
echo "==> Checking exercises"
npm run exercises:check

echo
echo "==> Checking contribution contract"
npm run contribution:contract:check

echo
echo "==> Checking reproducibility checklist"
npm run reproducibility:check

echo
echo "==> Checking troubleshooting tree"
npm run troubleshooting:tree:check

echo
echo "==> Checking course patterns"
npm run patterns:check

echo
echo "==> Checking concept graph"
npm run concept:graph:check

echo
echo "==> Checking learning units"
npm run learning:units:check

echo
echo "==> Checking learning outcomes"
npm run learning:outcomes:check

echo
echo "==> Checking checkpoints"
npm run checkpoints:check

echo
echo "==> Checking evaluation metrics"
npm run metrics:check

echo
echo "==> Checking paper blueprint"
npm run paper:blueprint:check

echo
echo "==> Checking teaching pack"
npm run teaching:pack:check

echo
echo "==> Checking research projects"
npm run research:projects:check

echo
echo "==> Checking research logbook"
npm run research:logbook:check

echo
echo "==> Checking visual verification matrix"
npm run visual:verification:check

echo
echo "==> Checking completion audit"
npm run completion:audit:check

echo
echo "==> Checking course manifest"
npm run course:manifest:check

echo
echo "==> Checking course structure"
npm run course:structure:check

echo
echo "==> Checking local documentation routes"
npm run docs:routes:check

echo
echo "==> Building without rewriting the tracked sitemap"
SITEMAP_NO_WRITE=1 npm run build
