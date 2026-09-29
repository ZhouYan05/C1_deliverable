# CS146S Vibe Coding 中文资料包

> Stanford CS146S《The Modern Software Developer》（2025 秋季）课程公开资料的
> 中文译本仓库。**从获取 → 提取 → 术语统一 → 机器翻译 → 质量抽检 → 人工校对 →
> 发布**的完整信息获取与翻译管线产物。

---

## 一、这是什么

本仓库是斯坦福大学 CS146S 课程（AI 辅助软件开发 / 常称 "Vibe Coding" 课程）的
**中文资料包**。全部内容来自课程公开网站
[themodernsoftware.dev](https://themodernsoftware.dev/) 的离线缓存（抓取于
2026-04-02），经机器翻译 + 术语表约束 + 人工校对后整理发布。

- **授课教师：** Mihail Eric
- **助教：** Febie Lin、Brent Ju
- **课程周期：** 10 周，覆盖 LLM 基础、提示工程、编码智能体、MCP、AI 安全、
  代码评审、SRE 等主题

---

## 二、来源与版权处理

| 项目 | 说明 |
|---|---|
| 一手来源 | `https://themodernsoftware.dev/`（课程官网，含 Overview / Syllabus / FAQ） |
| 抓取方式 | 官网全站离线缓存（含 31 篇文章页、3 份 PDF、课程主页） |
| 抓取时间 | 2026-04-02 |
| 授权声明 | 原始版权归课程方及各文章原作者所有；本仓库仅用于学习交流，请勿商用 |

**分层处理策略（Tier 机制）：**

- **Tier A（全文翻译）**：官方课程页与公开文章，产出全文中文译本；
- **Tier B（精读笔记）**：第三方付费墙内容（Medium / Notion / Ghost 会员制），
  即使取得原文也仅产出笔记式摘要，不整篇复制。

---

## 三、覆盖范围（截至 2026-09-28）

### 3.1 语料盘点

| 类别 | 总数 | 有效数 | 已翻译 | 缺口 |
|---|---:|---:|---:|---:|
| 课程文章页（pages/*.html） | 31 | 27 | 19（已发布） | 4 篇抓取失败 |
| 课程 PDF（pdfs/*.pdf） | 3 | 3 | 1 | 2 待译 |
| 辅助资料（Vibe Coding Playbook） | 1 | 1 | 1（笔记） | — |
| **合计** | **35** | **31** | **21** | **—** |

**课程文章覆盖率：19 / 27 ≈ 70%**（4 篇抓取失败不计入分母，详见
`zh/00-抓取失败与缺口清单.md`）。另有 5 篇机器翻译初稿已在 `translated/`
目录中，尚未完成人工校对，校对后可进一步提升覆盖率。

### 3.2 已翻译篇目（19 篇，`zh/阅读材料/`）

按课程周次分布：

| 周次 | 主题 | 篇数 |
|---|---|---|
| Week 1 | LLM 与提示工程 | 2 |
| Week 2 | 编码智能体与 MCP | 4 |
| Week 3 | AI IDE 与上下文 | 2 |
| Week 4 | Claude Code 工作流 | 2 |
| Week 5 | Warp 与 AI 原生开发 | 2 |
| Week 6 | AI 安全与漏洞 | 2 |
| Week 7 | AI 代码评审 | 3 |
| Week 8–10 | 全栈 / SRE / 未来 | 2 |

完整清单见 `zh/阅读材料/` 目录。

### 3.3 术语表

`pipeline/glossary.csv`：**83 条**英中对照术语（≥ 50 条的挑战要求），
按「基础概念 / 智能体 / 协议与工具 / 安全 / 工程实践」分类。
全部机翻均通过系统提示词注入本表，保证译法全文一致。

---

## 四、翻译流程（可复跑管线）

```
离线缓存(HTML) ──extract.py──▶ 干净 Markdown(source/) ──translate.py──▶ 机翻初稿(translated/)
                                   │                                     │
                              glossary.csv                          spotcheck.py
                              （83 条术语注入）                      （术语一致性+硬伤抽检）
                                                                          │
                                                                          ▼
                                              人工校对 ──▶ 发布(zh/阅读材料/)
```

| 步骤 | 脚本 | 作用 |
|---|---|---|
| 1. 正文提取 | `pipeline/extract.py` | 通用启发式剥离 HTML 壳（`<article>`→`<main>`→文本密度最高 `<div>`），剔除脚本/导航/付费墙，输出干净 Markdown |
| 2. 术语约束 | `pipeline/glossary.csv` | 83 条术语注入翻译提示词，锁定译法 |
| 3. 机器翻译 | `pipeline/translate.py` | 按标题/段落分块（4000 字/块 + 200 字重叠），走 OpenAI 兼容接口，支持 `--prepare-only` 离线生成提示词 |
| 4. 质量抽检 | `pipeline/spotcheck.py` | 检查术语一致性（原文有术语、译文缺译名判漏译）、机翻硬伤叠词（"的的/被被/进行进行"）、字符覆盖率 |
| 5. 人工校对 | 人工 | 逐篇审校术语、句式与代码块完整性，合格后移入 `zh/` 发布 |

### 复跑方法（换一门课同样适用）

```bash
# 1) 提取正文
python pipeline/extract.py <离线缓存目录> ./source
# 2) 机翻（需设置 LLM_API_KEY；或 --prepare-only 离线生成提示词）
python pipeline/translate.py ./source ./translated
# 3) 抽检
python pipeline/spotcheck.py ./source ./translated
# 4) 人工校对后移入 zh/ 发布
```

依赖：Python 3 + `beautifulsoup4` + `lxml` + `requests`。

---

## 五、使用方法（陌生人视角）

1. **只读浏览**：打开 `zh/阅读材料/index.md`，这是课程主页的完整中文版，
   包含课程描述、周次大纲与 FAQ；每篇文章独立成文件。
2. **按周学习**：根据 `pipeline/week_map.csv` 的「周次 → 篇目」映射，
   从第 1 周开始顺序阅读。
3. **查术语**：遇到不确定的译法，翻 `pipeline/glossary.csv`。
4. **对照原文**：每篇译文头部 YAML 标注了 `source` 原始链接；
   英文原文位于 `source/` 目录（同名文件）。
5. **看缺口**：抓取失败与不完整的内容全部如实记录在
   `zh/00-抓取失败与缺口清单.md`，并附补救途径。

---

## 六、已知缺口（如实披露）

| 缺口 | 原因 | 补救状态 |
|---|---|---|
| `good-context-good-code` | Ghost 付费墙，需访问码 | 未补 |
| `how-warp-uses-warp` | Notion 客户端渲染，无正文 | 未补 |
| `lessons-from-ai-code-reviews` | 0 字符，完全未取到 | 未补 |
| `peeking-under-the-hood-of-claude-code` | Medium 拦截自动抓取 | 未补 |
| `prompt-engineering-guide` | 客户端渲染，仅取到开头 13 行 | 已译不完整版 |
| `owasp-top-ten` | 只抓到项目首页 | 已补「十大风险速查表」 |
| `claude-code-best-practices` | 抓到官方概览页而非指定博客 | 译文中已显著标注 |
| 2 份 PDF | 待译（`how-anthropic-uses-claude-code`、`ai-assisted-code-review-assessment`） | 未补 |
| 5 篇机翻初稿 | 待人工校对后发布 | 进行中 |

---

## 七、仓库结构

```
cs146s-vibe-coding-zh/
├── README.md                  ← 本文件（资料包说明）
├── AI_工作日志与AAR.md         ← AI 协作日志 + 七维 AAR 复盘
├── 拿来说明/                   ← 至少 3 个「拿来说明」（决策如何借助 AI 做出）
│
├── source/                    ← 提取后的英文原文（Markdown）
├── translated/                ← 机器翻译初稿（含翻译日志）
├── pdf_source/                ← 4 份 PDF 转 Markdown 原文
├── zh/                        ← 发布目录（最终中文版）
│   ├── 阅读材料/               ← 19 篇全文译文 + 课程主页中文版
│   ├── pdf/                   ← PDF 译文
│   └── 00-抓取失败与缺口清单.md
└── pipeline/                  ← 可复跑管线（脚本 + 术语表 + 周次映射）
```

---

## 八、致谢与声明

- 课程方：Stanford CS146S（Mihail Eric 等），原站 `themodernsoftware.dev`
- 翻译执行：机器翻译（OpenAI 兼容接口）+ 术语表约束 + 人工校对
- 本仓库为非官方学习资料，翻译质量以「可读、忠实、术语统一」为目标，
  如发现错漏欢迎提 Issue。
