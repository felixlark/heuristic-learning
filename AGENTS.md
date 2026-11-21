# Heuristic Learning Repo Guidance


## 团队职位与制度源

- 本项目以**经理**负责技术方案、专员分工和交付闭环，**专员**负责具体实现、测试与成果证据。实际线程、工作根、权限、模型和已绑定主 Issue 依正式运行入口与原事项核实。
- 用户与 **ChatGPT 办公室**的秘书长（Bot）／秘书讨论目标、取舍和跨组织事项；GitHub Issue／PR 承载正式公文，本项目内部按已授权范围使用 A2A。
- 团队共用制度：[Cabinet/GOVERNANCE.md](https://github.com/smart-shadow/Cabinet/blob/main/GOVERNANCE.md)；版本采用：[同步规范](https://github.com/smart-shadow/Cabinet/blob/main/organization/source-sync.md)。本项目根 `AGENTS.md` 是专业规则正本。

- This repository is a Chinese research/course repo for Heuristic Learning, not an EasyVibe fork with unchanged content.
- Reuse EasyVibe's VitePress/course structure, but keep public copy, metadata, examples, and README focused on Heuristic Learning.
- Every theory page should point to a runnable example, case study, or source reference.
- Every example must have a short command and a test path. Prefer small, readable code over heavy dependencies.
- Treat Jiayi Weng's `learning-beyond-gradients` article/repo as the highest-signal public source, but phrase unvalidated claims as research hypotheses.
- X/Twitter cases should be integrated into the main learning flow once retrieved through `ft` or supported X API tooling.
- Do not commit generated VitePress build output under `docs/.vitepress/dist`.

## 当前执行基线

- 全团队所有 Codex 任务统一使用 DeepSeek V4.1 Flash 路由组 `auto/deepseek-v4.1-flash`。经理 High；专员、全局新任务及无专用角色档位 Max；sub-agent 继承父档，不配置其他模型 fallback。
- 模型路由不扩大数据授权。私有 GitHub、设备、客户和个人敏感数据只在入口实际解析到获准 DeepSeek 上游时使用。
- 需要用户补充信息时优先使用 Ask 模式。当前 Codex Desktop 对应 `request_user_input_async`，提出一次清晰问题并保持可答，同时继续执行不依赖答案的已授权工作；收到实际答复后再处理依赖分支。
- 只有不可逆动作、外部授权、本人认证或答案决定整个后续路径时，才暂停受影响部分。不得自答、假定选项或因等待立即结束任务。
- 设置、配置保存、自然运行和业务验收分别取证。未读回实际 `model`、`provider` 和 `effort` 时，以 unknown 记录，不凭规则文本宣称配置已生效。
- 保留现有 dirty checkout。编辑前检查 `git status`，不新建 worktree，不清理历史资源；在规范 checkout 串行写入并使用唯一 writer。
- 开发交付由原结果负责人连续完成相称检查、commit、push、PR、必要评审、合并和既定部署验收。普通 Codex 自动评审不是默认等待门，任务或仓库负责人明确要求的评审条件继续执行。
- 第三方署名、许可和真实引用保持原样。公开内容及元数据按当前公开身份核验规则检查。

## 项目合同

- **项目目标**：建立 Heuristic Learning 的可验证研究表述、案例与方法，并将可运行课程工程保留在独立规范仓。科研事实以 [Research #11](https://github.com/smart-shadow/Research/issues/11) 为准。
- **项目经理与专员**：经理依据真实项目主 Issue 统筹研究与工程交付，专员承办具体成果；当前指派和来源以正式组织登记与原 Issue 核实。
- **项目 Issue 入口**：研究种子、选题和交付验收使用 Research #11；工程缺陷和产品改动由该原案分流到规范仓 Issue 或 PR。
- **验收门**：理论页须连接可运行例子、案例或来源；例子有命令和测试路径；未验证主张标为假设。科研文稿须区分来源、结论与未知，并经 PR 和结果负责人核验。
- **发布与运行责任**：课程站点和技术发布由项目结果负责人执行既定构建、检查、部署与真实入口验收。不得提交生成目录。
- **暂停与恢复**：恢复工作前读取原 Issue、最新制度和当前 writer；未知副作用先对账。本规则不启动后台调度、不恢复已停例程。
- **用户升级边界**：费用、外部发表、生产发布、权限扩大、非授权数据、不可逆动作或需要本人取舍的事项回原 Issue 说明事实、选项和影响。

## 限制类改动规则

1. 新增或调小任何上限、槽位、名额、闸门、门槛、退避（包括并发数、负载准入、超时退避等）时，PR 正文须单列「新增限制」一节，写明位置、默认值和依据，经仓库负责人定稿后才可合并。此类改动不得绕过 PR 直接进入 main。
2. 资源类参数默认不限、只观测；确需限制时须通过显式配置开启，不得在代码中写死最大值。外部硬限制（如外部接口限流、部署锁）须在注释中写明来源。
