# 拿来说明 01：课程 README.md 的全文翻译是怎么借助 AI 做出来的

> 本文档说明：`CS146S_offline/README.md`（英文，105 行）→ `README_zh.md`
> （中文，106 行）的翻译决策、prompt 与产出对比。

---

## 一、决策背景

材料目录中有一份 CS146S 课程离线缓存包的英文 README，是全部语料的「门面」。
挑战的第一个动作就是翻译它。难点不在英文本身，而在三类**不可译项**的处理：

- 文件名与目录树结构（`index.html`、`pdfs/`、`pages/` 等）；
- URL 与人名（Mihail Eric、Febie Lin、Brent Ju）、教室号（420-041）；
- Markdown 语义（标题层级、表格、代码块围栏必须与原文一一对应）。

## 二、原文（节选）

```markdown
# CS146S: The Modern Software Developer — Offline Cache

## How to Use This Offline Cache

1. **Open `index.html`** in any web browser — this is the main course page
   with full navigation (Overview, Syllabus, FAQ).
...
## What Requires Internet Access

| Resource | Reason |
|---|---|
| YouTube videos (3 links) | Video files not downloaded by design |
...
- **Week 1:** Introduction to LLMs and prompt engineering
- **Week 2:** Coding agents, tool use, and MCP (Model Context Protocol)
```

## 三、我给 AI 的 prompt（原样）

```
翻译该文件的全部内容，要求：

1. 文件名、目录树结构、URL、人名（Mihail Eric / Febie Lin / Brent Ju）、
   教室号保持原文不译；
2. 技术术语首次出现时用「中文（English）」格式加注原文，
   例如：提示注入（Prompt Injection）、模型上下文协议（MCP）；
3. 严格保留 Markdown 语义：标题层级、表格列数、代码块围栏、分隔线
   全部与原文对齐；
4. 代码块（目录树）内只翻译 ← 箭头后的注释，文件名一律不动；
5. 输出为完整 Markdown，不要省略任何行，不要加前言后语。
```

## 四、AI 产出（节选，与原文同位置对照）

```markdown
# CS146S：现代软件开发者 —— 离线缓存

## 如何使用本离线缓存

1. **用任意浏览器打开 `index.html`** —— 这是课程主页，包含完整导航
   （概览、大纲、常见问题）。
...
## 需要联网访问的资源

| 资源 | 原因 |
|---|---|
| YouTube 视频（3 个链接） | 出于设计考虑，未下载视频文件 |
...
- **第 1 周：** 大语言模型（LLM）与提示工程导论
- **第 2 周：** 编码智能体、工具调用与 MCP（模型上下文协议）
```

AI 还主动多做了一件事：在译文目录树里补了一行
`README_zh.md ← 本文件的中文译本`，让译本对读者自指可见。

## 五、对比与评价

| 维度 | 直译（不做约定） | 本次产出（有约定） |
|---|---|---|
| 文件名 | 可能被译成中文，导致目录树与磁盘文件对不上 | 全部原样保留 ✅ |
| 术语 | "prompt injection" 可能译成 提示词注入/提示注入/指令注入 混用 | 首次「提示注入（Prompt Injection）」锁定 ✅ |
| 结构 | 表格列数、代码块围栏易漂移 | 105 行 → 106 行，仅多 1 行自指条目 ✅ |
| 元信息 | 无 | 译本自我可见 ✅ |

**结论**：翻译前把「不可译项清单 + 术语加注规则 + 结构对齐要求」写进 prompt，
产出即达到发布质量，省掉了一整轮人工返工。这个 prompt 模板随后被复用到
`translate.py` 的系统提示词中，成为 32 篇批量翻译的统一约束。
