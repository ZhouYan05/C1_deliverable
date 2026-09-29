---
source: https://code.claude.com/docs/en/overview
license: Anthropic 官方文档（允许翻译，需署名）
tier: A
handling: 全文翻译
week: 4
note: 原始抓取页面实为 Claude Code 官方文档「概览」页，非同名博客文章
---

# Claude Code 概览 —— Claude Code 官方文档

> 原文：Claude Code overview - Claude Code Docs
> 授权：Anthropic 官方文档，允许翻译，需署名并回链原文
> ⚠️ 抓取说明：离线缓存中此文件名为 `claude-code-best-practices.html`，但实际抓取
>    到的内容是 Claude Code 文档的**概览页**，而非 Week 4 阅读列表里的
>    "Claude Best Practices" 博客文章。两者内容不同，勿混淆。

## 文档导航

- **入门**：概览 · 快速开始 · 更新日志
- **核心概念**：Claude Code 如何工作 · 扩展 Claude Code · 探索 `.claude` 目录 · 探索上下文窗口
- **使用 Claude Code**：存储指令与记忆 · 权限模式 · 常见工作流 · 最佳实践
- **平台与集成**：概览 · 远程控制 · Chrome 扩展（beta）· 计算机使用（预览）· Visual Studio Code · JetBrains IDE · Slack 中的 Claude Code

---

## 什么是 Claude Code

Claude Code 是一个由 AI 驱动的编码助手，帮助你构建功能、修复缺陷、自动化开发任务。
它理解你的整个代码库，能够跨多个文件与多种工具工作，把事情真正做完。

## 快速开始

选择你的使用环境。大部分形态需要 Claude 订阅或 Anthropic Console 账号；终端 CLI 与
VS Code 插件也支持第三方模型提供方。

可选环境：**终端** · **VS Code** · **桌面应用** · **网页版** · **JetBrains**

### 终端

功能完整的 CLI，可直接在终端中与 Claude Code 协作。编辑文件、执行命令、从命令行
管理整个项目。

安装方式（三选一）：**原生安装（推荐）** · Homebrew · WinGet

**macOS / Linux / WSL：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell：**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD：**

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> 若你看到 `The token '&&' is not a valid statement separator`（`&&` 不是有效的
> 语句分隔符）报错，说明你用的是 PowerShell 而非 CMD，请改用上面的 PowerShell 命令。
> 提示符显示 `PS C:\` 即表示当前在 PowerShell 中。
> Windows 需要先安装 **Git for Windows**。原生安装会在后台自动更新，保持最新版本。

**Homebrew：**

```bash
brew install --cask claude-code
```

Homebrew 安装不会自动更新，需定期执行 `brew upgrade claude-code` 获取新功能与安全修复。

**WinGet：**

```cmd
winget install Anthropic.ClaudeCode
```

WinGet 安装同样不会自动更新，需定期执行 `winget upgrade Anthropic.ClaudeCode`。

随后在任意项目中启动：

```bash
cd your-project
claude
```

首次使用会提示登录。完成！接着看快速开始 →
如需安装选项、手动更新或卸载说明，参见高级设置；遇到问题参见故障排查。

### VS Code

VS Code 扩展直接在编辑器内提供内联 diff、@ 提及、计划审查与会话历史。
安装完成后，打开命令面板（`Cmd+Shift+P` / `Ctrl+Shift+P`），输入 "Claude Code"，
选择 Open in New Tab。

### 桌面应用

独立应用，可在 IDE 或终端之外运行 Claude Code。可视化审查 diff、并排运行多个会话、
安排周期性任务、启动云端会话。需要付费订阅。

### 网页版

在浏览器中运行 Claude Code，无需本地配置。可启动长耗时任务后稍后回来查看、在本地
没有的仓库上工作，或并行运行多个任务。支持桌面浏览器与 Claude iOS 应用。

### JetBrains

面向 IntelliJ IDEA、PyCharm、WebStorm 等 JetBrains IDE 的插件，支持交互式 diff 查看与
选中文本共享。从 JetBrains Marketplace 安装后重启 IDE 即可。

---

## 你可以用它做什么

### 自动化你一直拖着不做的工作

Claude Code 负责那些吞噬你时间的琐碎任务：为未测试的代码补测试、修复整个项目的
lint 错误、解决合并冲突、更新依赖、撰写发布说明。

```bash
claude "write tests for the auth module, run them, and fix any failures"
```

### 构建功能与修复缺陷

用日常语言描述你想要什么。Claude Code 会规划方案、跨多个文件编写代码，并验证其可用。
对于缺陷，直接粘贴报错信息或描述症状——它会在代码库中追溯问题、定位根因并实施修复。

### 创建提交与拉取请求

Claude Code 直接与 git 协作：暂存改动、编写提交信息、创建分支、发起 PR。

```bash
claude "commit my changes with a descriptive message"
```

在 CI 中，还可以用 GitHub Actions 或 GitLab CI/CD 自动化代码审查与 issue 分流。

### 用 MCP 连接你的工具

模型上下文协议（MCP）是连接 AI 工具与外部数据源的开放标准。借助 MCP，Claude Code
可以读取 Google Drive 中的设计文档、更新 Jira 工单、从 Slack 拉取数据，或使用你自己的
自定义工具。

### 用指令、技能与钩子定制

**CLAUDE.md** 是放在项目根目录的 Markdown 文件，Claude Code 每次会话开始时都会读取。
用它设定编码规范、架构决策、偏好库与审查清单。Claude 还会自动构建记忆，在工作中把构建
命令、调试心得等经验跨会话保存下来，无需你手写。

自定义命令（如 `/review-pr`、`/deploy-staging`）可以把可复用的工作流打包分享给团队。

**钩子（Hooks）** 让你在 Claude Code 动作前后执行 shell 命令，例如每次编辑文件后自动
格式化、每次提交前运行 lint。

### 运行智能体团队与自定义智能体

派生多个 Claude Code 智能体同时处理任务的不同部分，由一个主智能体协调、分配子任务并
合并结果。若需完全自定义工作流，**Agent SDK** 让你构建自己的智能体，并完全掌控编排、
工具访问与权限。

### 用 CLI 管道、脚本与自动化

Claude Code 遵循 Unix 哲学，具备可组合性。可以把日志管道给它、在 CI 中运行，或与其他
工具串联：

```bash
# 分析最近的日志输出
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# 在 CI 中自动化翻译
claude -p "translate new strings into French and raise a PR for review"

# 跨文件批量操作
git diff main --name-only | claude -p "review these changed files for security issues"
```

### 安排周期性任务

按计划运行 Claude 以自动化重复性工作：早晨的 PR 审查、隔夜的 CI 失败分析、每周的依赖
审计，或 PR 合并后的文档同步。

- **云端定时任务**运行在 Anthropic 托管的基础设施上，**即使你的电脑关机也在运行**。
  可从网页版、桌面应用创建，或在 CLI 中执行 `/schedule`。
- **桌面定时任务**在你的机器上运行，可直接访问本地文件与工具。
- `/loop` 在一次 CLI 会话内重复某个提示，用于快速轮询。

### 随时随地工作

会话不绑定单一环境。随着场景变化在不同环境间迁移工作：

- 离开工位，用**远程控制**从手机或任意浏览器继续工作
- 在手机上发消息派发任务，再打开它创建的桌面会话
- 在网页版或 iOS 应用启动长耗时任务，再用 `claude --teleport` 拉回终端
- 用 `/desktop` 把终端会话移交给桌面应用做可视化 diff 审查
- 从团队聊天路由任务：在 Slack 中 `@Claude` 并附缺陷报告，收到一个 PR

---

## 全场景使用 Claude Code

每个环境都连接同一个底层 Claude Code 引擎，因此你的 `CLAUDE.md`、设置与 MCP 服务器
在各环境间通用。除终端、VS Code、JetBrains、桌面与网页之外，Claude Code 还与 CI/CD、
聊天与浏览器工作流集成：

| 我想要…… | 推荐方案 |
|---|---|
| 从手机或其他设备继续本地会话 | 远程控制（Remote Control） |
| 把 Telegram / Discord / iMessage / 自建 webhook 的事件推入会话 | 渠道（Channels） |
| 本地启动任务、移动端继续 | 网页版或 Claude iOS 应用 |
| 按周期运行 Claude | 云端定时任务或桌面定时任务 |
| 自动化 PR 审查与 issue 分流 | GitHub Actions 或 GitLab CI/CD |
| 每个 PR 都自动获得代码审查 | GitHub Code Review |
| 把 Slack 里的缺陷报告转成 PR | Slack |
| 调试线上 Web 应用 | Chrome |
| 为自有工作流构建自定义智能体 | Agent SDK |

## 后续步骤

安装完成后，可通过以下指南进一步深入：

- **快速开始**：走完你的第一个真实任务——从探索代码库到提交修复
- **存储指令与记忆**：用 `CLAUDE.md` 与自动记忆给 Claude 持久化指令
- **常见工作流与最佳实践**：充分发挥 Claude Code 效能的模式
- **设置**：按你的工作流定制 Claude Code
- **故障排查**：常见问题的解决方案
- **code.claude.com**：演示、定价与产品详情

> 本页由 AI 生成回复，可能包含错误。

---

**本节要点**

- Claude Code 的定位是**可组合的编码智能体**，而非聊天式补全；Unix 管道哲学是其
  差异化能力（`claude -p` 可脚本化）。
- `CLAUDE.md` + 自动记忆 + 钩子 + 自定义命令，构成「把团队规范固化为智能体行为」
  的四件套。
- **云端定时任务在关机时仍运行**，这是与纯本地工具的关键差异。
- 会话可跨环境迁移（`--teleport`、`/desktop`、远程控制），上下文不中断。
