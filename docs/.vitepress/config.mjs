import { defineConfig } from 'vitepress'
import markdownItKatex from 'markdown-it-katex'

const base = process.env.BASE || '/heuristic-learning/'
const siteUrl =
  process.env.SITE_URL || 'https://longbiaochen.github.io/heuristic-learning'

export default defineConfig({
  title: 'Heuristic Learning',
  description: '直觉学习：从思想、案例到可运行系统的中文研究课程',
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
      { text: '学习路线', link: '/zh-cn/stage-1/' },
      { text: '理论框架', link: '/zh-cn/stage-2/' },
      { text: '动手实验', link: '/zh-cn/examples/' },
      { text: '案例库', link: '/zh-cn/cases/' },
      { text: '幻灯片', link: '/zh-cn/slides/' },
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
            { text: '学习路线', link: '/zh-cn/stage-1/' }
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
            { text: '来源: X 线索', link: '/zh-cn/cases/x-signal/' }
          ]
        },
        {
          text: '课程材料',
          items: [
            { text: 'Slides 目录', link: '/zh-cn/slides/' },
            { text: '第 1 讲', link: '/zh-cn/slides/lecture-1/' },
            { text: '第 2 讲', link: '/zh-cn/slides/lecture-2/' },
            { text: '第 3 讲', link: '/zh-cn/slides/lecture-3/' },
            { text: 'Lab 1', link: '/zh-cn/slides/lab-1/' },
            { text: 'Lab 2', link: '/zh-cn/slides/lab-2/' }
          ]
        },
        {
          text: '附录',
          items: [
            { text: '资料与维护规范', link: '/zh-cn/appendix/' },
            { text: '本地运行与排错', link: '/zh-cn/appendix/local-setup' },
            { text: '排错决策树', link: '/zh-cn/appendix/troubleshooting-tree' },
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
            { text: '讲者备注', link: '/zh-cn/appendix/speaker-notes' },
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
        link: 'https://github.com/longbiaochen/heuristic-learning'
      }
    ],
    search: {
      provider: 'local'
    },
    editLink: {
      pattern:
        'https://github.com/longbiaochen/heuristic-learning/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页'
    },
    footer: {
      message: 'Heuristic Learning research and hands-on course.',
      copyright: 'CC-BY-NC-SA-4.0'
    }
  }
})
