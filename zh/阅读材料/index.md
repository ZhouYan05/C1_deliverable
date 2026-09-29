---
source: https://themodernsoftware.dev/ （离线缓存，抓取于 2026-04-02）
tier: A
handling: 全文翻译
page: 课程主页（概述 / 大纲 / FAQ）
---

# CS146S：现代软件开发者 —— 斯坦福大学

## 离线缓存说明

本文件是 `themodernsoftware.dev` 的本地保存版本，抓取于 **2026 年 4 月 2 日**。
文章页面保存在 `pages/` 目录，PDF 文档保存在 `pdfs/` 目录。
视频链接（YouTube）与 Google Slides 幻灯片保留为外部链接。

---

## 课程描述

过去几年，大语言模型为软件开发引入了一种全新的范式。传统软件开发生命周期的每一个
环节都在被 AI 自动化改造，这引出了一个问题：**下一代软件工程师应当如何利用这些
进展，把生产力提升十倍，并为自身的职业发展做好准备？**

本课程将论证：现代 AI 工具不仅能提升开发者生产力，还能让软件工程**普惠化**到更
广泛的群体。我们会展示软件开发如何从「0 到 1 的代码创造」演化为「规划 → 用 AI 生成
→ 修改 → 重复」的迭代式工作流。学生将同时掌握传统软件工程难题背后的理论，以及当今
用 AI 解决这些问题的前沿工具。

通过动手实践的工程任务，以及来自构建这些革命性工具的行业先驱者的分享，你将获得
AI 辅助开发、自动化测试、智能文档与安全漏洞检测方面的实践经验。课程结束时，你将
清晰理解如何把最先进的 LLM 模型融入复杂的开发工作流，并避开常见陷阱。

### 学分

3 学分

### 先修要求

具备 CS111 同等水平的编程经验。建议修过 CS221/229。

### 课程形式

每周讲座 + 动手编码实践 + 行业嘉宾分享 + 展示现代开发实践的期末项目。

### 目标

掌握现代开发工具、理解 AI 辅助编码、学习自动化测试与部署、探索新兴软件趋势。

### 教室

420-041

### 答疑时间（Office Hours）

- **Mihail Eric**：周五 12:00–12:30
- **Febie Lin**：周三 9:00–11:00（黄楼地下室 Huang Basement）

### 作业截止时间

见课程日历（Google Sheets）

### 教学团队

| 姓名 | 角色 |
|---|---|
| Mihail Eric | 讲师（Instructor） |
| Febie Lin | 助教（TA） |
| Brent Ju | 助教（TA） |

---

# 课程大纲

## 第 1 周：编码用 LLM 与 AI 开发入门

**主题**：课程事务安排 · LLM 究竟是什么 · 如何有效写提示词

**阅读材料**

- Deep Dive into LLMs（LLM 深入解析）
- Prompt Engineering Overview（提示词工程概览）
- Prompt Engineering Guide（提示词工程指南）
- AI Prompt Engineering: A Deep Dive
- How OpenAI Uses Codex（OpenAI 如何使用 Codex）

**作业**：LLM 提示词试验场（Prompting Playground）

**讲座**

- 周一 9/22：课程导入与 LLM 的构造原理
- 周五 9/26：面向 LLM 的高效提示技巧

## 第 2 周：编码智能体的解剖结构

**主题**：工具使用与函数调用 · MCP（模型上下文协议）

**阅读材料**

- MCP Introduction（MCP 介绍）
- Sample MCP Server Implementations（MCP 服务器示例实现）
- MCP Server Authentication（MCP 服务器认证）
- MCP Server SDK
- MCP Registry（MCP 注册中心）
- MCP Food-for-Thought

**作业**：AI IDE 入门实践

**讲座**

- 周一 9/29：从零构建一个编码智能体
- 周五 10/3：构建自定义 MCP 服务器

## 第 3 周：AI 集成开发环境（AI IDE）

**主题**：上下文管理与代码理解 · 面向智能体的 PRD · IDE 集成与扩展

**阅读材料**

- Specs Are the New Source Code（规格即新源代码）
- How Long Contexts Fail（长上下文为何失效）
- Devin: Coding Agents 101
- Getting AI to Work In Complex Codebases
- How FAANG Vibe Codes
- Writing Effective Tools for Agents（为智能体编写高效工具）

**作业**：构建自定义 MCP 服务器

**讲座**

- 周一 10/6：AI IDE 深入解析
- 周五 10/10：嘉宾 Silas Alberti（Cognition）
- 配套资源：设计文档模板

## 第 4 周：Claude Code 与智能体式编码

**主题**：Claude Code 架构与内部机制 · 智能体式编码工作流 · 面向智能体的上下文工程

**阅读材料**

- How Anthropic Uses Claude Code（Anthropic 内部如何使用 Claude Code）
- Claude Best Practices（Claude 最佳实践）
- Awesome Claude Agents
- Super Claude
- Good Context Good Code
- Peeking Under the Hood of Claude Code

**作业**：用 Claude Code 编码

**讲座**

- 周一 10/13：Claude Code 深入解析
- 周五 10/17：嘉宾 Boris Cherney（Claude Code）

## 第 5 周：Warp 与 AI 终端

**主题**：AI 原生的终端开发 · 智能体式开发工作流

**阅读材料**

- Warp vs Claude Code
- How Warp Uses Warp to Build Warp（Warp 如何用 Warp 开发 Warp）
- Warp University

**作业**：用 Warp 进行智能体式开发

**讲座**

- 周一 10/20：Warp 与 AI 终端
- 周五 10/24：嘉宾 Zach Lloyd（Warp）

## 第 6 周：AI 安全与漏洞检测

**主题**：安全测试（SAST vs DAST）· 提示词注入攻击 · AI 辅助漏洞检测 · OWASP Top 10

**阅读材料**

- SAST vs DAST
- Copilot Remote Code Execution via Prompt Injection
- Finding Vulnerabilities in Modern Web Apps Using Claude Code and OpenAI Codex
- Agentic AI Threats: Identity Spoofing and Impersonation Risks
- OWASP Top Ten: The Leading Web Application Security Risks
- Context Rot: Understanding Degradation in AI Context Windows
- Vulnerability Prompt Analysis with O3

**作业**：编写安全的 AI 代码

**讲座**

- 周一 10/27：AI 安全深入解析
- 周五 10/31：嘉宾 Isaac Evans（Semgrep）

## 第 7 周：AI 驱动的代码审查

**主题**：代码审查最佳实践 · AI 辅助代码审查 · 自动化审查工具

**阅读材料**

- Code Reviews: Just Do It（代码审查：别想太多，干就完了）
- How to Review Code Effectively
- AI-Assisted Assessment of Coding Practices in Modern Code Review
- AI Code Review Implementation Best Practices
- Code Review Essentials for Software Teams
- Lessons from Millions of AI Code Reviews

**作业**：代码审查练习（Code Review Reps）

**讲座**

- 周一 11/3：AI 代码审查深入解析
- 周五 11/7：嘉宾 Tomas Reimers（Graphite）

## 第 8 周：全栈 AI 开发与部署

**主题**：多技术栈 Web 应用开发 · AI 辅助部署流水线

**作业**：多技术栈 Web 应用构建

**讲座**

- 周一 11/10：全栈 AI 开发
- 周五 11/14：嘉宾 Gaspar Garcia（Vercel）

## 第 9 周：SRE、可观测性与智能体值班

**主题**：站点可靠性工程基础 · 可观测性与监控 · 值班工程中的 AI 智能体 · 多智能体系统

**阅读材料**

- Introduction to Site Reliability Engineering（SRE 导论）
- Observability Basics You Should Know
- Kubernetes Troubleshooting with AI
- Your New Autonomous Teammate / Benefits of Agentic AI in On-call Engineering
- Role of Multi Agent Systems in Making Software Engineers AI-native

**讲座**

- 周一 11/17：SRE 与 AI 可观测性
- 周五 11/21：嘉宾 Mayank Agarwal & Milind Ganjoo（Resolve）

## 第 10 周：AI 在软件工程中的未来

**主题**：AI 辅助开发的未来趋势 · 行业视角与职业影响 · 期末项目答辩

**讲座**

- 周一 12/1：嘉宾 Martin Casado（a16z）
- 周五 12/5：期末项目展示

---

# 常见问题（FAQ）

### 这门课适合谁？

面向具备编程经验（CS111 同等水平）、希望学习如何利用现代 AI 工具大幅提升软件开发
生产力的学生。建议修过 CS221/229，但非强制。

### 这门课我要做什么？

学生将完成每周动手作业，内容涵盖 LLM 提示词、MCP 服务器开发、AI IDE 使用、
Claude Code 工作流、安全分析、代码审查自动化与全栈 Web 应用。课程以一个展示现代开发
实践的期末项目收尾。

### 我们会用到哪些工具？

课程覆盖一系列 AI 开发工具，包括 Claude Code、Warp 终端、Cursor/Windsurf IDE、
Semgrep、Graphite 与 Vercel；同时也会使用模型上下文协议（MCP）及各类 LLM API。

### 成绩如何评定？

由每周作业、课堂讨论参与度与期末项目综合评定。具体截止时间见作业日历。

### 讲座有录像吗？

录像是否提供请咨询课程工作人员。每讲讲义（Slides）链接已列在上方大纲中。

### 如何联系教学团队？

- **Mihail Eric**：答疑时间 周五 12:00–12:30
- **Febie Lin**：答疑时间 周三 9:00–11:00（黄楼地下室）
- **Brent Ju**：联系方式见课程 Slack / Ed

---

**讲师**：Mihail Eric　**助教**：Febie Lin、Brent Ju　**学分**：3　**教室**：420-041
