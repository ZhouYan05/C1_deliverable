$ /$
跳至主要内容
Claude Code 文档主页
快速入门
使用 Claude Code 构建
部署
管理
配置
参考
资源

##### 快速入门

- 概览
- 快速开始
- 更新日志

##### 核心概念

- Claude Code 的工作原理
- 扩展 Claude Code
- 探索 .claude 目录
- 探索上下文窗口

##### 使用 Claude Code

- 存储指令与记忆
- 权限模式
- 常见工作流
- 最佳实践

##### 平台与集成

- 概览
- Remote Control
- 
- 
- Chrome 扩展（测试版）
- 计算机使用（预览版）
- Visual Studio Code
- JetBrains IDE
- 
- Slack 中的 Claude Code

- 开始使用
- 你能做什么
- 随时随地使用 Claude Code
- 后续步骤

Claude Code 是一款由 AI 驱动的编程助手，可帮助你构建功能、修复 Bug 并自动化开发任务。它能理解你的整个代码库，并可跨多个文件和工具协同工作以完成任务。

## 开始使用

选择你的环境开始使用。大多数界面需要 Claude 订阅或 Anthropic Console 账号。终端 CLI 和 VS Code 还支持第三方服务提供商 。
- 终端
- VS Code
- 桌面应用
- Web
- JetBrains

功能完整的 CLI，可直接在终端中使用 Claude Code。从命令行编辑文件、运行命令并管理整个项目。
要安装 Claude Code，请使用以下方法之一：
- 原生安装（推荐）
- Homebrew
- WinGet

macOS、Linux、WSL：

```
curl -fsSL https://claude.ai/install.sh | bash

```

Windows PowerShell：

```
irm https://claude.ai/install.ps1 | iex

```

Windows CMD：

```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

```

如果你看到 The token '&&' is not a valid statement separator（令牌“&&”不是有效的语句分隔符），说明你在 PowerShell 中而非 CMD。请改用上面的 PowerShell 命令。处于 PowerShell 时，你的提示符显示为 PS C:\。
Windows 需要 Git for Windows 。如果你还没有安装，请先安装它。
原生安装会在后台自动更新，使你始终使用最新版本。

```
brew install --cask claude-code

```

Homebrew 安装不会自动更新。请定期运行 brew upgrade claude-code 以获取最新功能和安全修复。

```
winget install Anthropic.ClaudeCode

```

WinGet 安装不会自动更新。请定期运行 winget upgrade Anthropic.ClaudeCode 以获取最新功能和安全修复。
然后在任意项目中启动 Claude Code：

```
cd your-project
claude

```

首次使用时会提示你登录。就这么简单！继续阅读快速开始 →
如需安装选项、手动更新或卸载说明，请参阅高级设置。如遇到问题，请访问故障排查。
VS Code 扩展可直接在你的编辑器中提供行内差异、@ 提及、计划审查和对话历史。
- 为 VS Code 安装
- 为 Cursor 安装

或在扩展视图中搜索“Claude Code”（Mac 上按 Cmd+Shift+X，Windows/Linux 上按 Ctrl+Shift+X）。安装后，打开命令面板（ Cmd+Shift+P / Ctrl+Shift+P ），输入“Claude Code”，然后选择在新标签页中打开 。
开始使用 VS Code →
一款独立应用，可在 IDE 或终端之外运行 Claude Code。可视化查看差异、并排运行多个会话、安排周期性任务并启动云端会话。
下载并安装：
- macOS（Intel 和 Apple Silicon）
- Windows（x64）
- Windows ARM64（仅限远程会话）

安装后，启动 Claude、登录，然后点击 Code 标签页开始编程。需要付费订阅。
了解桌面应用的更多信息 →
无需本地配置，即可在浏览器中运行 Claude Code。启动长时间运行的任务并在完成后回来查看，处理本地没有的仓库，或并行运行多个任务。可在桌面浏览器和 Claude iOS 应用上使用。
在 claude.ai/code 开始编程。
开始使用 Web 版 →
适用于 IntelliJ IDEA、PyCharm、WebStorm 和其他 JetBrains IDE 的插件，支持交互式差异查看和选区上下文共享。
从 JetBrains Marketplace 安装 Claude Code 插件，然后重启你的 IDE。
开始使用 JetBrains →

## 你能做什么

以下是你使用 Claude Code 的一些方式：
自动化你一直拖延的工作
Claude Code 能处理那些消耗你时间的繁琐任务：为未测试的代码编写测试、修复整个项目中的 Lint 错误、解决合并冲突、更新依赖以及编写发布说明。

```
claude "write tests for the auth module, run them, and fix any failures"

```

构建功能并修复 Bug
用通俗的语言描述你的需求。Claude Code 会规划实现方案、跨多个文件编写代码，并验证其是否可用。
对于 Bug，粘贴错误信息或描述症状。Claude Code 会在你的代码库中追踪问题、定位根本原因并实施修复。更多示例请参阅常见工作流。
创建提交和拉取请求
Claude Code 直接与 Git 协作。它可以暂存更改、编写提交信息、创建分支并发起拉取请求。

```
claude "commit my changes with a descriptive message"

```

在 CI 中，你可以使用 GitHub Actions 或 GitLab CI/CD 自动化代码审查和问题分类。
使用 MCP 连接你的工具
模型上下文协议（MCP）是一项开放标准，用于将 AI 工具连接到外部数据源。借助 MCP，Claude Code 可以读取 Google Drive 中的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或使用你自己的自定义工具。
使用指令、技能和钩子进行自定义
CLAUDE.md 是一个添加到项目根目录的 Markdown 文件，Claude Code 会在每个会话开始时读取它。你可以用它来设置编码规范、架构决策、首选库和审查清单。Claude 在工作时还会自动构建记忆，跨会话保存构建命令和调试心得等经验，无需你手动记录。
创建自定义命令以打包团队可共享的可重复工作流，例如 /review-pr 或 /deploy-staging 。
钩子允许你在 Claude Code 操作之前或之后运行 Shell 命令，例如每次编辑文件后自动格式化，或在提交前运行 Lint。
运行 Agent 团队并构建自定义 Agent
生成多个 Claude Code Agent，同时处理任务的不同部分。由主 Agent 协调工作、分配子任务并合并结果。
对于完全自定义的工作流，Agent SDK 允许你借助 Claude Code 的工具和能力构建自己的 Agent，并可完全控制编排、工具访问和权限。
使用 CLI 进行管道处理、脚本编写和自动化
Claude Code 具有可组合性，并遵循 Unix 哲学。你可以将日志通过管道传入、在 CI 中运行它，或与其他工具串联使用：

```
# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"

```

完整的命令和参数列表请参阅 CLI 参考。
安排周期性任务
按计划运行 Claude，以自动化重复性工作：早间的 PR 审查、夜间的 CI 失败分析、每周的依赖审计，或在 PR 合并后同步文档。
- 云端计划任务运行在 Anthropic 管理的基础设施上，即使你的电脑关机也能持续运行。可以从 Web、桌面应用创建，或在 CLI 中运行 /schedule 创建。
- 桌面计划任务在你的机器上运行，可直接访问你的本地文件和工具
- /loop 会在 CLI 会话中重复执行某个提示词，用于快速轮询

随时随地办公
会话不局限于单一界面。随着上下文的变化，你可以在不同环境之间切换工作：
- 离开办公桌后，仍可通过 Remote Control 用手机或任意浏览器继续工作
- 通过 Message Dispatch 从手机派发任务，并打开它创建的桌面会话
- 在 Web 或 iOS 应用上启动长时间运行的任务，然后用 claude --teleport 将其拉取到终端
- 使用 /desktop 将终端会话交接给桌面应用，以进行可视化差异审查
- 从团队聊天中路由任务：在 Slack 中 @Claude 并附上 Bug 报告，即可收到一个拉取请求

## 随时随地使用 Claude Code

每个界面都连接到同一个底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置和 MCP 服务器在所有界面上都能通用。
除了上述终端 、 VS Code 、 JetBrains 、 桌面 和 Web 环境外，Claude Code 还与 CI/CD、聊天和浏览器工作流集成：
| 我想要？ | 最佳选择 |
| 用手机或其他设备继续本地会话 | Remote Control |
| 将 Telegram、Discord、iMessage 或自定义 Webhook 的事件推送到会话中 | Channels |
| 在本地启动任务，在移动端继续 | Web 或 Claude iOS 应用 |
| 按周期性计划运行 Claude | 云端计划任务或桌面计划任务 |
| 自动化 PR 审查和问题分类 | GitHub Actions 或 GitLab CI/CD |
| 对每个 PR 自动进行代码审查 | GitHub Code Review |
| 将 Slack 中的 Bug 报告转化为拉取请求 | Slack |
| 调试线上 Web 应用 | Chrome |
| 为自己的工作流构建自定义 Agent | Agent SDK |

## 后续步骤

安装 Claude Code 后，这些指南将帮助你深入了解。
- 快速开始 ：完整走一遍你的第一个真实任务，从探索代码库到提交修复
- 存储指令与记忆 ：通过 CLAUDE.md 文件和自动记忆为 Claude 提供持久化指令
- 常见工作流与最佳实践 ：充分发挥 Claude Code 作用的模式
- 设置 ：为你的工作流自定义 Claude Code
- 故障排查 ：常见问题的解决方案
- code.claude.com ：演示、定价和产品详情

此页面对你有帮助吗？

快速开始
? I
$ /$
助手
回复由 AI 生成，可能包含错误。