---
source: https://www.warp.dev/university/getting-started/warp-vs-claude-code
license: Warp 商业站点，专有内容
tier: B
handling: 中文精读笔记（非逐段译文）
week: 5
---

# 精读笔记：Warp 与 Oz 入门

> 原文：Getting started with Warp and Oz（Warp 官方文档）
> ⚠️ 本笔记为**提炼与讲解**，非逐段译文。内容为厂商官方材料，版权归 Warp 所有。
> 📌 抓取说明：离线缓存中此文件名为 `warp-vs-claude-code.html`，但实际抓到的是
>    **「Warp 与 Oz 入门」**页，而非课程 Week 5 指定的对比文章（见下方「抓取缺口」）。

## 一句话结论

**Warp 是终端界面 + 本地智能体；Oz 是云端智能体的编排平台。** 二者共用同一套底层
智能体能力，可本地/云端无缝接力。

## 关键概念

| 概念 | 含义 |
|---|---|
| **Warp** | 智能体式开发环境（Agentic Development Environment），现代终端 + 强大智能体 |
| **Oz** | 支撑 Warp 全部智能功能的**云端智能体编排平台** |
| **Agent Modality** | 在「干净的终端」与「专用会话视图」间切换 |
| **Warp Drive / Rules / MCP 服务器** | 本地与云端智能体**共享**的上下文与工具 |

## Warp 的核心能力

- **智能体模态**：命令用纯终端，多轮智能体工作流用会话视图
- **现代终端体验**：光标移动、块式导航、多行编辑、语法高亮、丰富补全；**Rust 编写**，
  性能高
- **代码编辑器**：文件树、支持 LSP 的编辑器、交互式代码审查
- **智能体集成**：语音输入、基于终端的图像处理与 `@` 选择；兼容 Oz，或 Claude Code、
  Codex 等外部智能体

## Oz：两种运行模式

### 本地智能体（Local Agents）

直接在 Warp 应用内运行，实时交互式编码辅助：

- 跨代码库编写与重构代码
- 调试问题、修复错误
- 执行命令并解读结果
- 规划并执行多步任务

> **控制权在你手里**：可审查改动、任务中途引导智能体、执行前批准动作。

### 云端智能体（Cloud Agents）

在 Warp 基础设施（或你自己的基础设施）后台运行，面向规模化自动化：

- **触发器（Triggers）**：响应 Slack、Linear、GitHub 或自定义 webhook 事件
- **计划任务（Schedules）**：周期性任务，如依赖更新、死代码清理
- **并行（Parallelism）**：跨仓库或跨任务并发运行多个智能体
- **可观测性（Observability）**：每次运行都可追踪、可审计、可与团队共享

> 适合**不需要你即时关注**的工作：PR 审查、issue 分流、例行维护、集成驱动的工作流。

## 两者如何协同

- **同一个智能体，任何地方**：本地交互与云端运行用的是**同一套底层能力**
- **无缝接力**：云端启动任务，需要亲手控制时在本地 Warp 接手，**不丢进度与上下文**
- **共享上下文**：Warp Drive、Rules 与 MCP 服务器在本地与云端通用
- **团队协作**：分享智能体会话、审查智能体动作、引导运行中的任务——无论谁启动的

## 多模型与隐私

- **多模型**：Oz 天然多模型，可从精选模型集中按任务挑选最合适的 LLM
- **合规**：Warp 通过 **SOC 2**，与所有签约 LLM 提供商实行**零数据保留（ZDR）**——
  不保留、不存储客户 AI 数据，也不用于训练
- **可全局关闭** AI 功能：设置 > AI

## 抓取缺口（重要）

课程 Week 5 的阅读列表要求 **"Warp vs Claude Code"**，但本次抓取到的页面是
Warp 官方的产品入门页，**并非两者的对比评测**。若作业需要真正的产品对比，
请直接访问 <https://www.warp.dev/university/getting-started/warp-vs-claude-code>
在线阅读，或列入本仓库 README 的「已知缺口」。

## 与本课程的关系

- Week 5 主题是「AI 原生终端开发」——Warp 的块式导航、模态切换正是终端从「字符流」
  演进为「结构化输出块」的典型代表。
- **云端智能体 + 触发器/计划任务**这套模式，与 Week 9 的「智能体值班工程」是同一
  套架构思路：把重复性运维交给后台智能体。
- 「可全局关闭 AI」与 ZDR 承诺，是企业采纳 AI 编码工具时的核心合规问题。

## 延伸阅读

- 原文入口：<https://www.warp.dev/university/getting-started/warp-vs-claude-code>
- 对照阅读：本仓库 `claude-code-best-practices.md`（Claude Code 官方文档概览）
