#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PORT="${PORT:-5183}"
HOST="127.0.0.1"
BASE_URL="http://${HOST}:${PORT}"
LOG_FILE="$(mktemp -t heuristic-learning-routes.XXXXXX.log)"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  rm -f "$LOG_FILE"
  rm -rf docs/.vitepress/cache
}
trap cleanup EXIT

npm run dev -- --host "$HOST" --port "$PORT" >"$LOG_FILE" 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 40); do
  if curl -fsS "${BASE_URL}/heuristic-learning/" >/dev/null 2>&1; then
    break
  fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    cat "$LOG_FILE" >&2
    echo "VitePress dev server exited before routes were ready" >&2
    exit 1
  fi
  sleep 0.25
done

routes=(
  "/heuristic-learning/"
  "/heuristic-learning/zh-cn/syllabus/"
  "/heuristic-learning/zh-cn/course-map/"
  "/heuristic-learning/zh-cn/examples/"
  "/heuristic-learning/zh-cn/cases/visual-prior/"
  "/heuristic-learning/zh-cn/cases/technology-society/"
  "/heuristic-learning/zh-cn/cases/ai-governance-medical/"
  "/heuristic-learning/zh-cn/talk/"
  "/heuristic-learning/zh-cn/benchmark/"
  "/heuristic-learning/zh-cn/appendix/reading-guide"
  "/heuristic-learning/zh-cn/appendix/case-registry"
  "/heuristic-learning/zh-cn/appendix/code-tour"
  "/heuristic-learning/zh-cn/appendix/learning-units"
  "/heuristic-learning/zh-cn/appendix/learning-outcomes"
  "/heuristic-learning/zh-cn/appendix/checkpoints"
  "/heuristic-learning/zh-cn/appendix/evaluation-metrics"
  "/heuristic-learning/zh-cn/appendix/paper-blueprint"
  "/heuristic-learning/zh-cn/appendix/concept-graph"
  "/heuristic-learning/zh-cn/appendix/teaching-pack"
  "/heuristic-learning/zh-cn/appendix/ablation-plan"
  "/heuristic-learning/zh-cn/appendix/artifact-gap-analysis"
  "/heuristic-learning/zh-cn/appendix/benchmark-results"
  "/heuristic-learning/zh-cn/appendix/research-projects"
  "/heuristic-learning/zh-cn/appendix/research-logbook"
  "/heuristic-learning/zh-cn/appendix/source-to-case-playbook"
  "/heuristic-learning/zh-cn/appendix/contribution-protocol"
  "/heuristic-learning/zh-cn/appendix/completion-audit"
  "/heuristic-learning/zh-cn/appendix/public-entrypoints"
  "/heuristic-learning/zh-cn/appendix/visual-verification"
  "/heuristic-learning/zh-cn/appendix/reproducibility"
  "/heuristic-learning/course-manifest.json"
  "/heuristic-learning/course-manifest.schema.json"
  "/heuristic-learning/example-registry.json"
  "/heuristic-learning/example-registry.schema.json"
  "/heuristic-learning/code-tour.json"
  "/heuristic-learning/code-tour.schema.json"
  "/heuristic-learning/benchmark-summary.json"
  "/heuristic-learning/benchmark-summary.schema.json"
  "/heuristic-learning/ablation-plan.json"
  "/heuristic-learning/ablation-plan.schema.json"
  "/heuristic-learning/artifact-gap-analysis.json"
  "/heuristic-learning/artifact-gap-analysis.schema.json"
  "/heuristic-learning/troubleshooting-tree.json"
  "/heuristic-learning/troubleshooting-tree.schema.json"
  "/heuristic-learning/claims-registry.json"
  "/heuristic-learning/claims-registry.schema.json"
  "/heuristic-learning/case-registry.json"
  "/heuristic-learning/case-registry.schema.json"
  "/heuristic-learning/rubric.json"
  "/heuristic-learning/rubric.schema.json"
  "/heuristic-learning/exercise-registry.json"
  "/heuristic-learning/exercise-registry.schema.json"
  "/heuristic-learning/contribution-contract.json"
  "/heuristic-learning/contribution-contract.schema.json"
  "/heuristic-learning/reproducibility-checklist.json"
  "/heuristic-learning/reproducibility-checklist.schema.json"
  "/heuristic-learning/learning-units.json"
  "/heuristic-learning/learning-units.schema.json"
  "/heuristic-learning/learning-outcomes.json"
  "/heuristic-learning/learning-outcomes.schema.json"
  "/heuristic-learning/checkpoint-registry.json"
  "/heuristic-learning/checkpoint-registry.schema.json"
  "/heuristic-learning/evaluation-metrics.json"
  "/heuristic-learning/evaluation-metrics.schema.json"
  "/heuristic-learning/paper-blueprint.json"
  "/heuristic-learning/paper-blueprint.schema.json"
  "/heuristic-learning/concept-graph.json"
  "/heuristic-learning/concept-graph.schema.json"
  "/heuristic-learning/teaching-pack.json"
  "/heuristic-learning/teaching-pack.schema.json"
  "/heuristic-learning/research-projects.json"
  "/heuristic-learning/research-projects.schema.json"
  "/heuristic-learning/research-logbook.json"
  "/heuristic-learning/research-logbook.schema.json"
  "/heuristic-learning/completion-audit.json"
  "/heuristic-learning/completion-audit.schema.json"
  "/heuristic-learning/visual-verification.json"
  "/heuristic-learning/visual-verification.schema.json"
  "/heuristic-learning/visual-acceptance-log.json"
  "/heuristic-learning/visual-acceptance-log.schema.json"
  "/heuristic-learning/x-sources.json"
  "/heuristic-learning/x-sources.schema.json"
  "/heuristic-learning/source-to-case-playbook.json"
  "/heuristic-learning/source-to-case-playbook.schema.json"
  "/heuristic-learning/experiment-report.schema.json"
  "/heuristic-learning/llms.txt"
)

for route in "${routes[@]}"; do
  url="${BASE_URL}${route}"
  status="$(curl -fsS -o /dev/null -w "%{http_code}" "$url")"
  if [[ "$status" != "200" ]]; then
    echo "route check failed: ${status} ${route}" >&2
    exit 1
  fi
  echo "200 ${route}"
done

echo "checked ${#routes[@]} local routes"
