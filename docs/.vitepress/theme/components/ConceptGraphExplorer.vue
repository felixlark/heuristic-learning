<script setup>
import { computed, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'

const concepts = ref([])
const selectedId = ref('heuristic-learning')
const loadError = ref('')

const roleMap = {
  'heuristic-learning': 'center',
  signal: 'source',
  probe: 'verify',
  baseline: 'verify',
  'heuristic-patch': 'update',
  'feedback-report': 'memory',
  regression: 'memory',
  'source-status': 'source'
}

const roleLabels = {
  center: '核心',
  source: '来源',
  verify: '验证',
  update: '更新',
  memory: '复盘'
}

const routeForPath = (path) => {
  const route = path
    .replace(/^docs\/zh-cn\//, '/zh-cn/')
    .replace(/\/index\.md$/, '/')
    .replace(/\.md$/, '')
  return route
}

const nodeLines = (term) => {
  if (term === 'Heuristic Learning') return ['Heuristic', 'Learning']
  if (term === 'Heuristic patch') return ['Heuristic', 'patch']
  if (term === 'Feedback report') return ['Feedback', 'report']
  if (term === 'Source status') return ['Source', 'status']
  return [term]
}

const fallbackConcepts = [
  {
    id: 'heuristic-learning',
    term: 'Heuristic Learning',
    definition: '由编码智能体消费反馈并维护软件结构的学习过程。',
    claim_ids: ['software-structure-learning', 'feedback-report-as-agent-input'],
    example_ids: ['gridworld', 'breakout-replay', 'ant-gait-replay'],
    material_ids: ['lecture-1', 'lecture-2'],
    pages: ['docs/zh-cn/stage-2/index.md', 'docs/zh-cn/theory/learning-loop.md'],
    commands: ['npm run claims:registry:check', 'npm run examples:feedback']
  }
]

const graphConcepts = computed(() => (concepts.value.length ? concepts.value : fallbackConcepts))

const selectedConcept = computed(
  () => graphConcepts.value.find((concept) => concept.id === selectedId.value) ?? graphConcepts.value[0]
)

const positionedNodes = computed(() => {
  const nodes = graphConcepts.value
  const center = nodes.find((node) => node.id === 'heuristic-learning')
  const outer = nodes.filter((node) => node.id !== 'heuristic-learning')
  const radius = 154

  const result = []
  if (center) {
    result.push({
      ...center,
      x: 300,
      y: 220,
      role: roleMap[center.id] ?? 'center'
    })
  }

  outer.forEach((node, index) => {
    const angle = -Math.PI / 2 + (index / outer.length) * Math.PI * 2
    result.push({
      ...node,
      x: 300 + Math.cos(angle) * radius,
      y: 220 + Math.sin(angle) * radius,
      role: roleMap[node.id] ?? 'verify'
    })
  })

  return result
})

const edges = computed(() => {
  const nodes = positionedNodes.value
  const byId = new Map(nodes.map((node) => [node.id, node]))
  const center = byId.get('heuristic-learning')
  if (!center) return []

  const result = nodes
    .filter((node) => node.id !== center.id)
    .map((node) => ({
      id: `${center.id}-${node.id}`,
      from: center,
      to: node,
      kind: node.role
    }))

  const pairs = [
    ['signal', 'source-status'],
    ['signal', 'probe'],
    ['probe', 'baseline'],
    ['baseline', 'heuristic-patch'],
    ['heuristic-patch', 'feedback-report'],
    ['feedback-report', 'regression'],
    ['regression', 'probe']
  ]

  pairs.forEach(([fromId, toId]) => {
    const from = byId.get(fromId)
    const to = byId.get(toId)
    if (from && to) result.push({ id: `${fromId}-${toId}`, from, to, kind: 'loop' })
  })

  return result
})

const selectConcept = (id) => {
  selectedId.value = id
}

onMounted(async () => {
  try {
    const response = await fetch(withBase('/concept-graph.json'), { cache: 'no-store' })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    concepts.value = Array.isArray(data.concepts) ? data.concepts : []
  } catch {
    loadError.value = '图谱数据暂时无法读取，下面显示最小核心节点。'
  }
})
</script>

<template>
  <section class="concept-graph-explorer" aria-label="Heuristic Learning interactive concept graph">
    <div class="concept-graph-toolbar">
      <div>
        <p class="eyebrow">Interactive Graph</p>
        <h2>从一个概念进入学习闭环</h2>
      </div>
      <div class="legend" aria-label="节点类型">
        <span v-for="(label, role) in roleLabels" :key="role" :class="['legend-item', `role-${role}`]">
          <span aria-hidden="true"></span>{{ label }}
        </span>
      </div>
    </div>

    <p v-if="loadError" class="graph-error">{{ loadError }}</p>

    <div class="graph-layout">
      <div class="graph-canvas" role="img" aria-label="Heuristic Learning concept graph">
        <svg viewBox="0 0 600 440" class="graph-svg" aria-hidden="true">
          <defs>
            <marker
              id="concept-arrow"
              markerWidth="8"
              markerHeight="8"
              refX="7"
              refY="4"
              orient="auto"
              markerUnits="strokeWidth"
            >
              <path d="M0,0 L8,4 L0,8 Z" />
            </marker>
          </defs>

          <line
            v-for="edge in edges"
            :key="edge.id"
            :class="['graph-edge', `edge-${edge.kind}`]"
            :x1="edge.from.x"
            :y1="edge.from.y"
            :x2="edge.to.x"
            :y2="edge.to.y"
          />

          <g
            v-for="node in positionedNodes"
            :key="node.id"
            :class="['graph-node', `role-${node.role}`, { selected: node.id === selectedConcept.id }]"
            :transform="`translate(${node.x}, ${node.y})`"
            tabindex="0"
            role="button"
            :aria-label="`查看 ${node.term}`"
            @click="selectConcept(node.id)"
            @keydown.enter.prevent="selectConcept(node.id)"
            @keydown.space.prevent="selectConcept(node.id)"
          >
            <circle :r="node.role === 'center' ? 52 : 42" />
            <text :y="nodeLines(node.term).length > 1 ? -12 : -4" text-anchor="middle">
              <tspan
                v-for="(line, index) in nodeLines(node.term)"
                :key="line"
                x="0"
                :dy="index === 0 ? 0 : 14"
              >
                {{ line }}
              </tspan>
            </text>
            <text :y="nodeLines(node.term).length > 1 ? 24 : 16" text-anchor="middle">{{ roleLabels[node.role] }}</text>
          </g>
        </svg>

        <div class="node-buttons" aria-label="选择概念">
          <button
            v-for="node in positionedNodes"
            :key="node.id"
            :class="['node-button', `role-${node.role}`, { selected: node.id === selectedConcept.id }]"
            type="button"
            @click="selectConcept(node.id)"
          >
            {{ node.term }}
          </button>
        </div>
      </div>

      <aside class="concept-detail" aria-live="polite">
        <p class="detail-label">{{ roleLabels[roleMap[selectedConcept.id] ?? 'verify'] }}</p>
        <h3>{{ selectedConcept.term }}</h3>
        <p>{{ selectedConcept.definition }}</p>

        <div class="detail-grid">
          <section>
            <h4>代表示例</h4>
            <div class="chips">
              <span v-for="example in selectedConcept.example_ids" :key="example">{{ example }}</span>
            </div>
          </section>

          <section>
            <h4>讲义材料</h4>
            <div class="chips">
              <span v-for="material in selectedConcept.material_ids" :key="material">{{ material }}</span>
            </div>
          </section>

          <section>
            <h4>阅读页面</h4>
            <ul>
              <li v-for="page in selectedConcept.pages" :key="page">
                <a :href="withBase(routeForPath(page))">{{ page.replace('docs/zh-cn/', '') }}</a>
              </li>
            </ul>
          </section>

          <section>
            <h4>验证命令</h4>
            <div class="commands">
              <code v-for="command in selectedConcept.commands" :key="command">{{ command }}</code>
            </div>
          </section>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.concept-graph-explorer {
  margin: 20px 0 28px;
  padding: 18px;
  border: 1px solid var(--vp-c-divider);
  background: color-mix(in srgb, var(--vp-c-bg-soft) 72%, transparent);
}

.concept-graph-toolbar {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 14px;
}

.concept-graph-toolbar h2 {
  margin: 0 !important;
  padding: 0 !important;
}

.eyebrow,
.detail-label {
  margin: 0 0 4px !important;
  color: var(--vp-c-text-2);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  justify-content: flex-end;
  max-width: 300px;
}

.legend-item {
  display: inline-flex;
  gap: 6px;
  align-items: center;
  color: var(--vp-c-text-2);
  font-size: 12px;
  line-height: 1.2;
}

.legend-item span {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.graph-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  align-items: stretch;
}

.graph-canvas,
.concept-detail {
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
}

.graph-canvas {
  min-width: 0;
  padding: 8px;
}

.graph-svg {
  display: block;
  width: 100%;
  min-height: 420px;
}

.graph-edge {
  stroke: var(--vp-c-divider);
  stroke-width: 1.7;
  marker-end: url('#concept-arrow');
}

.edge-loop {
  stroke-dasharray: 5 5;
}

.graph-node {
  cursor: pointer;
}

.graph-node circle {
  fill: var(--node-fill);
  stroke: var(--node-stroke);
  stroke-width: 2;
  transition:
    filter 0.18s ease,
    stroke-width 0.18s ease,
    transform 0.18s ease;
}

.graph-node text {
  fill: var(--vp-c-text-1);
  font-size: 12px;
  font-weight: 700;
  pointer-events: none;
}

.graph-node text + text {
  fill: var(--vp-c-text-2);
  font-size: 10px;
  font-weight: 600;
}

.graph-node:hover circle,
.graph-node:focus-visible circle,
.graph-node.selected circle {
  filter: drop-shadow(0 10px 18px rgba(0, 0, 0, 0.14));
  stroke-width: 3;
}

.concept-detail {
  min-width: 0;
  padding: 18px;
}

.concept-detail h3 {
  margin: 0 0 8px !important;
  font-size: 22px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 16px;
}

.detail-grid h4 {
  margin: 0 0 6px !important;
  color: var(--vp-c-text-2);
  font-size: 13px;
}

.detail-grid ul {
  padding-left: 1em;
}

.chips,
.commands {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chips span,
.node-button {
  border: 1px solid var(--node-border, var(--vp-c-divider));
  background: var(--node-soft, var(--vp-c-bg-soft));
}

.chips span {
  padding: 3px 8px;
  color: var(--vp-c-text-1);
  font-size: 12px;
}

.commands code {
  display: inline-block;
  padding: 5px 8px;
  white-space: normal;
}

.node-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 4px;
}

.node-button {
  padding: 7px 10px;
  color: var(--vp-c-text-1);
  font: inherit;
  font-size: 12px;
  cursor: pointer;
}

.node-button.selected {
  border-color: var(--node-stroke);
  box-shadow: inset 0 0 0 1px var(--node-stroke);
}

.role-center {
  --node-fill: #dbeafe;
  --node-soft: #eff6ff;
  --node-stroke: #2563eb;
  --node-border: rgba(37, 99, 235, 0.32);
}

.role-source {
  --node-fill: #dcfce7;
  --node-soft: #f0fdf4;
  --node-stroke: #16a34a;
  --node-border: rgba(22, 163, 74, 0.3);
}

.role-verify {
  --node-fill: #fef3c7;
  --node-soft: #fffbeb;
  --node-stroke: #d97706;
  --node-border: rgba(217, 119, 6, 0.34);
}

.role-update {
  --node-fill: #ffe4e6;
  --node-soft: #fff1f2;
  --node-stroke: #e11d48;
  --node-border: rgba(225, 29, 72, 0.32);
}

.role-memory {
  --node-fill: #ede9fe;
  --node-soft: #f5f3ff;
  --node-stroke: #7c3aed;
  --node-border: rgba(124, 58, 237, 0.3);
}

.legend-item.role-center span,
.legend-item.role-source span,
.legend-item.role-verify span,
.legend-item.role-update span,
.legend-item.role-memory span {
  background: var(--node-stroke);
}

.graph-error {
  margin: 0 0 12px !important;
  color: var(--vp-c-danger-1);
}

@media (max-width: 820px) {
  .concept-graph-toolbar,
  .detail-grid {
    display: block;
  }

  .legend {
    justify-content: flex-start;
    margin-top: 10px;
  }

  .graph-svg {
    min-height: 320px;
  }
}

@media (max-width: 560px) {
  .concept-graph-explorer {
    padding: 12px;
  }

  .graph-svg {
    display: none;
  }

  .node-buttons {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
  }
}
</style>
