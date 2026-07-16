import { defineConfig } from 'vitepress'
import markdownItKatex from 'markdown-it-katex'

const base = process.env.BASE || '/heuristic-learning/'
const siteUrl =
  process.env.SITE_URL || 'https://felixlark.github.io/heuristic-learning'

export default defineConfig({
  title: 'Heuristic Learning',
  description: '面向开发者和 AI 爱好者的 Heuristic Learning 中文 Web 课程',
  base,
  lang: 'zh-CN',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: [/^https:\/\/x\.com\//],
  head: [
    ['link', { rel: 'icon', href: `${base}hl-logo.svg` }],
    ['meta', { name: 'theme-color', content: '#1f6feb' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Heuristic Learning' }],
    [
      'meta',
      {
        property: 'og:description',
        content: '直觉学习中文研究与动手课程：先理解理论，再运行示例，最后完成可验证练习。'
      }
    ],
    ['meta', { property: 'og:url', content: siteUrl }],
    [
      'script',
      { type: 'application/ld+json' },
      JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Course',
        name: 'Heuristic Learning',
        description: '直觉学习中文研究与动手课程',
        inLanguage: 'zh-CN',
        educationalLevel: 'Intermediate'
      })
    ]
  ],
  markdown: {
    config(md) {
      md.use(markdownItKatex)
    }
  },
  themeConfig: {
    logo: '/hl-logo.svg',
    nav: [
      { text: '课程大纲', link: '/zh-cn/syllabus/' },
      { text: '一小时导读', link: '/zh-cn/talk/' },
      { text: '理论框架', link: '/zh-cn/stage-2/' },
      { text: '动手实验', link: '/zh-cn/examples/' },
      { text: '案例库', link: '/zh-cn/cases/' },
      { text: '研究进阶', link: '/zh-cn/benchmark/' },
      { text: '参考', link: '/zh-cn/appendix/' }
    ],
    sidebar: {
      '/zh-cn/': [
        {
          text: '开始',
          items: [
            { text: '首页', link: '/zh-cn/' },
            { text: '课程地图', link: '/zh-cn/course-map/' },
            { text: '课程大纲', link: '/zh-cn/syllabus/' },
            { text: '学习路线', link: '/zh-cn/stage-1/' },
            { text: '一小时导读', link: '/zh-cn/talk/' }
          ]
        },
        {
          text: '理论',
          items: [
            { text: 'HL 基础概念', link: '/zh-cn/stage-2/' },
            { text: '从 RL/DL 到 HL', link: '/zh-cn/stage-3/' },
            { text: '学习闭环', link: '/zh-cn/theory/learning-loop' },
            { text: '研究框架', link: '/zh-cn/theory/research-framework' }
          ]
        },
        {
          text: '实践',
          items: [
            { text: '可运行示例', link: '/zh-cn/examples/' },
            { text: '案例库总览', link: '/zh-cn/cases/' },
            { text: 'Artifact: Breakout', link: '/zh-cn/cases/breakout/' },
            { text: 'Artifact: VizDoom', link: '/zh-cn/cases/vizdoom/' },
            { text: 'Artifact: Ant Gait', link: '/zh-cn/cases/ant-gait/' },
            { text: '应用: 机器人足球', link: '/zh-cn/cases/robot-soccer/' },
            { text: '应用: 交通模拟', link: '/zh-cn/cases/traffic-simulation/' },
            { text: '研究: 事实约束审计', link: '/zh-cn/cases/constraint-audit/' },
            { text: '研究: 视觉先验', link: '/zh-cn/cases/visual-prior/' },
            { text: '研究: 技术与社会', link: '/zh-cn/cases/technology-society/' },
            { text: '研究: AI 治理与医疗', link: '/zh-cn/cases/ai-governance-medical/' },
            { text: '来源: X 线索', link: '/zh-cn/cases/x-signal/' }
          ]
        },
        {
          text: '研究进阶',
          items: [
            { text: '真实环境 Benchmark', link: '/zh-cn/benchmark/' },
            { text: '实验协议', link: '/zh-cn/appendix/benchmark-protocol' },
            { text: '结果与边界', link: '/zh-cn/appendix/benchmark-results' }
          ]
        },
        {
          text: '附录',
          items: [
            { text: '资料与维护规范', link: '/zh-cn/appendix/' },
            { text: '本地运行与排错', link: '/zh-cn/appendix/local-setup' },
            { text: '术语表', link: '/zh-cn/appendix/glossary' },
            { text: '参考文献与仓库', link: '/zh-cn/appendix/references' },
            { text: '文献阅读指南', link: '/zh-cn/appendix/reading-guide' },
            { text: '案例矩阵', link: '/zh-cn/appendix/case-registry' },
            { text: '代码导览', link: '/zh-cn/appendix/code-tour' },
            { text: '学习单元矩阵', link: '/zh-cn/appendix/learning-units' },
            { text: '学习成果矩阵', link: '/zh-cn/appendix/learning-outcomes' },
            { text: '阶段检查点', link: '/zh-cn/appendix/checkpoints' },
            { text: '评估指标矩阵', link: '/zh-cn/appendix/evaluation-metrics' },
            { text: '论文蓝图', link: '/zh-cn/appendix/paper-blueprint' },
            { text: '概念图谱', link: '/zh-cn/appendix/concept-graph' },
            { text: '授课包', link: '/zh-cn/appendix/teaching-pack' },
            { text: '引用与署名', link: '/zh-cn/appendix/citation' },
            { text: '来源登记', link: '/zh-cn/appendix/source-registry' },
            { text: '来源到案例 Playbook', link: '/zh-cn/appendix/source-to-case-playbook' },
            { text: '发布清单', link: '/zh-cn/appendix/release-checklist' },
            { text: '课程 Rubric', link: '/zh-cn/appendix/rubric' },
            { text: '教师指南', link: '/zh-cn/appendix/instructor-guide' },
            { text: '课程进度表', link: '/zh-cn/appendix/course-schedule' },
            { text: '完成度审计', link: '/zh-cn/appendix/completion-audit' },
            { text: '机器可读入口', link: '/zh-cn/appendix/public-entrypoints' },
            { text: '视觉验收', link: '/zh-cn/appendix/visual-verification' },
            { text: '可复现性检查', link: '/zh-cn/appendix/reproducibility' },
            { text: '练习集', link: '/zh-cn/appendix/exercises' },
            { text: '研究课题', link: '/zh-cn/appendix/research-projects' },
            { text: '事实约束审计研究', link: '/zh-cn/appendix/constraint-audit' },
            { text: '研究日志', link: '/zh-cn/appendix/research-logbook' },
            { text: '消融计划', link: '/zh-cn/appendix/ablation-plan' },
            { text: 'Artifact 差距分析', link: '/zh-cn/appendix/artifact-gap-analysis' },
            { text: '实验协议', link: '/zh-cn/appendix/benchmark-protocol' },
            { text: 'Benchmark 结果', link: '/zh-cn/appendix/benchmark-results' },
            { text: '研究路线图', link: '/zh-cn/appendix/research-roadmap' },
            { text: '贡献与研究协议', link: '/zh-cn/appendix/contribution-protocol' }
          ]
        }
      ]
    },
    socialLinks: [
      {
        icon: 'github',
        link: 'https://github.com/felixlark/heuristic-learning'
      }
    ],
    search: {
      provider: 'local'
    },
    editLink: {
      pattern:
        'https://github.com/felixlark/heuristic-learning/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页'
    },
    footer: {
      message: 'Heuristic Learning research and hands-on course.',
      copyright: 'CC-BY-NC-SA-4.0'
    }
  }
})
