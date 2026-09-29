---
source: PDF — how-openai-uses-codex.pdf
原始来源: OpenAI 官方工程材料
license: 专有内容（OpenAI）
tier: B
handling: 中文精读笔记（非逐段译文）
week: 1
原文页数: 13
---

# 精读笔记：OpenAI 内部如何使用 Codex

> 原文：How OpenAI uses Codex（OpenAI 官方 PDF，共 13 页）
> ⚠️ 本笔记为**提炼与讲解**，非逐段译文。原文版权归 OpenAI 所有。
> 📌 课程定位：Week 1 阅读材料之一（与 Prompt Engineering 两篇同周）。

## 一句话结论

**Codex 在 OpenAI 内部最成功的用法不是「写代码」，而是「读代码」与「清理技术债」。**
本文给出 7 类用例 + 5 条最佳实践，每类都配了可直接套用的提示词。

## 使用范围

Codex 已被 OpenAI 多个技术团队**日常使用**：安全、产品工程、前端、API、基础设施、
性能工程。用于加速从理解复杂系统、重构大型代码库，到发布新功能、在紧迫期限内
解决事故等各类工程任务。

## 七类用例

### 1. 代码理解（Code understanding）

在入职、调试、事故调查时快速熟悉陌生代码区域。典型动作：定位某个功能的核心逻辑、
**绘制服务/模块间的关系图**、追踪系统中的数据流；还常用于**发现架构模式或文档缺失**。

> **「在事故响应中，Codex 通过暴露组件间交互、追踪故障状态如何跨系统传播，
> 帮助工程师快速切入新领域。」**

工程师原话：

- 「修 bug 时我用 **Ask 模式**看看代码库里**其他地方还可能出同样的问题**。」
- 「值班时我把**堆栈跟踪贴进去，问 Codex 认证流程在哪**。它直接跳到正确的文件，
  我能很快分诊。」（SRE，API 平台）
- 「Codex 回答我『这个该在哪儿改？』这类跨 Terraform 和 Python 的仓库问题，
  **比 grep 快得多**。」（DevOps，基础设施服务）

**可套用提示词**
```text
Where is the authentication logic implemented in this repo?
Summarize how requests flow through this service from entrypoint to response.
Which modules interact with [module name] and how are failures handled?
```

### 2. 重构与迁移（Refactoring and migrations）

最适合**跨多文件/多包**的改动：更新 API、改变模式实现方式、迁移到新依赖。
**当同一次更新需要在几十个文件里应用，或更新需要理解正则与查找替换抓不到的结构与
依赖关系时，尤其有用。** 也用于拆分过大模块、用现代模式替换旧模式、为可测试性做准备。

> 「Codex 把我们新服务模式里所有遗留的 `getUserById()` 都换掉并开了 PR，
> **几分钟做完了本来要几小时的事**。」（后端，ChatGPT Web）

**可套用提示词**
```text
Split this file into separate modules by concern and generate tests for each one.
Convert all callback-based database access to async/await.
```

### 3. 性能优化（Performance optimization）

分析慢或吃内存的代码路径（低效循环、冗余操作、昂贵查询）并建议优化替代方案。
也被用于**识别风险或已废弃但仍在使用的模式**，以**降低长期技术债、主动防止回归**。

> 「用 Codex 扫描**重复的昂贵 DB 调用**。它很擅长标记热点路径并起草批处理查询，
> 我之后可以再调优。」

**可套用提示词**
```text
Optimize this loop for memory efficiency and explain why your version is faster.
Find repeated expensive operations in this request handler and suggest caching opportunities.
```

### 4. 提升测试覆盖率

在**覆盖率薄弱或完全缺失**的地方特别有用。修 bug 或重构时常让它建议覆盖**边界情况
与可能的失败路径**；对新代码可基于函数签名与周边逻辑生成单元或集成测试。
**特别擅长发现边界条件**：空输入、最大长度、异常但合法的状态。

> 「我整晚让 Codex 盯着低覆盖模块，第二天醒来就有**可运行的单元测试 PR**。」

**可套用提示词**
```text
Write unit tests for this function, including edge cases and failure paths.
Generate a property-based test for this sorting utility.
Extend this test file to cover missing scenarios around null inputs and invalid states.
```

### 5. 提升开发速度（Increasing development velocity）

**同时加速开发周期的两端**：

- **起步**：脚手架——生成文件夹、模块、API 桩，快速产出可运行代码
- **收尾**：临近发布时处理**较小但必要**的任务——bug 分诊、填补最后一公里实现、
  生成发布脚本、遥测钩子、配置文件
- 也用于**把产品反馈变成起始代码**：粘贴用户请求或规格，让 Codex 生成粗稿待后续精修

> 「我整天都在开会，**仍然合并了 4 个 PR，因为 Codex 在后台工作**。」

**可套用提示词**
```text
Scaffold a new API route for POST /events with basic validation and logging.
Create a stub implementation based on this spec: [insert spec or product feedback].
```

### 6. 保持心流（Staying in flow）

日程碎片化、频繁被打断时保持生产力：**捕捉未完成的工作、把笔记变成可运行原型、
把探索性任务分离出来稍后再回来**。这让**暂停与恢复不丢失上下文**——值班或会议多时尤其有用。

> 「我经常把 Slack 话题串、Datadog trace、issue **转发给 Codex**，
> 这样我就能专注在高优先级工作上。」

**可套用提示词**
```text
Generate a plan to refactor this service and split it into smaller modules.
Stub out the retry logic and add a TODO — I'll fill in the backoff logic later.
Summarize this file so I can pick up where I left off tomorrow.
```

### 7. 探索与构思（Exploration and ideation）

开放式工作：**为问题提供多种解法、检验设计决策**。让 Codex 提示不同解法、
探索陌生模式、**对假设做压力测试**，从而**暴露权衡、扩展设计选项、锐化实现选择**。

也能**识别相关 bug**：给定一个已知问题或废弃方法，找出代码中其他地方的类似模式。

**可套用提示词**
```text
How would this work if the system were event-driven instead of request/response?
Find all modules that manually build SQL strings instead of using our query builder.
Rewrite this in a more functional style, avoid mutation and side effects.
```

## 最佳实践（五条）

### 1. 从 Ask 模式开始

> **大改动先用 Ask 模式让 Codex 给出实现计划**，该计划再作为切换到 Code 模式后
> 后续提示词的输入。**这个两步流程让 Codex 保持聚焦并避免输出错误。**

**任务粒度指导**：

> **「Codex 在范围界定清晰的任务上表现最好——那些你或同事大约一小时能完成、
> 或几百行代码能实现的任务。」** 随着模型进步，可承接的任务规模预期会增大。

### 2. 迭代改进 Codex 的开发环境

**配置启动脚本、环境变量、互联网访问，能显著降低错误率。**
运行任务时留意构建错误并在环境配置中修正。**可能需要几轮迭代，但长期收益显著。**

### 3. 像写 GitHub Issue 那样组织提示词

> **「当提示词像你描述 PR 或 issue 中的改动时，Codex 响应更好。」**

具体意味着：相关时**包含文件路径、组件名、diff、文档片段**。
用「**照 [模块 X] 的方式实现这个**」这类模式提示能显著改善结果。

### 4. 把 Codex 任务队列当轻量级待办清单

用来**捕获旁支想法、部分工作、顺手的修复**。**不必一次生成完整 PR。**
Codex 是个**暂存区**，等你恢复专注时再回来取。

### 5. 用 `AGENTS.md` 提供持久上下文

维护 `AGENTS.md` 帮助 Codex **跨提示词**更有效地在你的仓库中工作。
这类文件通常包含**命名约定、业务逻辑、已知怪癖，或无法从代码单独推断的依赖**。

> 📌 **与 Claude Code 的 `CLAUDE.md` 是同一理念**——见本仓库
> `claude-code-best-practices.md`。

### 6.（附加）用 "Best of N" 提升产出

**同时为单个任务生成多个响应**，快速探索多种方案并挑选最佳。
更复杂的任务可以**审查多轮迭代，并组合不同响应的部分**以获得更强结果。

## 展望

Codex 仍处于**研究预览（research preview）**阶段，但已对构建方式产生实际影响——
**让团队跑得更快、写出更好的代码，并承接那些原本永远不会被优先处理的工作**。

---

## 与本课程的关系

- **Week 1 指定阅读**，与提示词工程两篇配套。
- **与 `specs-are-the-new-source-code` 高度呼应**：本文的
  「**像写 GitHub Issue 那样写提示词**」正是那篇「规格即源代码」论点的实操版本。
- **与 `code-review-essentials` 呼应**：本文大量用例（找相似 bug、找废弃模式、
  补测试、生成发布摘要）本质是**把人工审查中最机械的部分自动化**。
- **与 `multi-agent-systems-ai-native` 对照**：本文是「**编码侧** AI 化」的成功案例，
  那篇指出**生产调试侧仍未 AI 化**——两者合起来才是完整的现状图景。

## 可迁移到实践的四条

1. **大改动先要计划再动手**（Ask → Code 两步法），显著降低返工。
2. **把 `AGENTS.md` / `CLAUDE.md` 当作一等公民维护**——这是提示词工程里
   投入产出比最高的一项。
3. **提示词按「工单」标准写**：给文件路径、给参照模块、说明范围。
4. **任务队列用来抓「顺手的活」**，别指望一次生成完整 PR。
