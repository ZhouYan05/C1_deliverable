# 拿来说明 02：通用 HTML 正文提取器（extract.py）是怎么借助 AI 设计出来的

> 本文档说明：`pipeline/extract.py` 的核心设计决策——面对十几个来源站点、
> 结构各异的 31 个 HTML 页面，如何借助 AI 定下「零站点特判」的通用方案。

---

## 一、决策背景

31 篇文章来自 Google Cloud、promptingguide.ai、Stytch、Cloudflare、Anthropic、
Semgrep、Medium、Notion、Ghost 等十几个站点，HTML 结构完全不同：

- 有的正文在 `<article>`，有的在 `<main>`，有的只是嵌套 `<div>`；
- 有的带导航/侧栏/页脚噪音，有的带 cookie 横幅与付费墙提示；
- 还有 4 篇根本没有正文（会员制 / 客户端渲染 / 0 字符）。

如果按传统爬虫思路「每个站点写一套 CSS 选择器」，31 篇要写十几套规则，
且换一门课全部作废。这正是需要求助 AI 做方案设计的场景。

## 二、原文（AI 的输入样本，节选两例差异极大的页面骨架）

```html
<!-- 站点 A：语义化良好 -->
<html><body>
  <header>…导航…</header>
  <article>
    <h1>Prompt Engineering Overview</h1>
    <p>Prompt engineering is the practice of…</p>
    …
  </article>
  <footer>…</footer>
</body></html>

<!-- 站点 B：纯 div 流 -->
<html><body>
  <div class="app">
    <div class="sidebar">…</div>
    <div class="content">
      <h2>How to Review Code Effectively</h2>
      <p>Code review is the single…</p>
      …
    </div>
  </div>
</body></html>
```

## 三、我给 AI 的 prompt（原样）

```
我有 31 个来自不同站点的课程文章 HTML 文件，要批量提取正文转 Markdown。
不要为任何站点写特判规则（站点会变，规则会腐烂）。

请设计一个通用提取器的算法流程，要求：

1. 正文定位优先级：<article> → <main> → 文本密度最高的 <div>；
2. 污点清理：整块丢弃 script/style/nav/header/footer/form/iframe 等标签，
   但保留 a/strong/code 等行内标签的文本；
3. 付费墙/占位页识别：正文有效文本过短（如 <200 字符）标记为 blocked，
   不进入后续翻译队列，单独登记；
4. 输出：每篇一个 Markdown 文件 + 一份清单（ok / blocked / empty 状态）；
5. 用 Python + BeautifulSoup 实现，代码里要有清晰的文档字符串。
```

## 四、AI 产出（节选核心逻辑）

```python
# 正文定位启发式（按优先级）
def _locate_main(soup):
    for tag in ("article", "main"):
        node = soup.find(tag)
        if node is not None:
            return node
    # 文本密度最高的 <div>
    return max(soup.find_all("div"),
               key=lambda d: len(d.get_text(strip=True)),
               default=soup.body)

# 污点标签：直接整体丢弃
STRIP_TAGS = {"script", "style", "nav", "header", "footer",
              "form", "iframe", "svg", ...}
# 仅丢弃标签本身、保留文本
UNWRAP_TAGS = {"a", "span", "strong", "code", ...}
```

AI 同时给出了占位页的判定阈值思路与 `_manifest.json` 清单格式，全部落地为
`extract.py`（230 行，含文档字符串）。

## 五、对比与评价

| 维度 | 逐站点 CSS 选择器方案 | 本次通用启发式方案 |
|---|---|---|
| 规则数量 | 31 篇 ≈ 十几套选择器 | 0 套特判，3 条优先级 ✅ |
| 换课复用 | 全部作废重写 | 直接复用（extract.py 零修改）✅ |
| 新站点鲁棒性 | 未写规则即失败 | 文本密度兜底，总有正文可提取 ✅ |
| 失败显性化 | 静默输出空文件 | blocked / empty 状态进清单 ✅ |

**实测结果**：27 篇正常提取，4 篇被准确标记为 blocked——其中
`good-context-good-code.html`（Ghost 付费墙）提取出 "Enter access code" 提示
而非正文，`how-warp-uses-warp.html`（Notion）只剩 "Notion" 一词。AI 的
「占位识别优先于硬翻」设计直接避免了后面把付费墙空壳喂给翻译模型的错误。

**结论**：把「不要写特判、要通用启发式、要失败显性化」三条约束讲清楚，
AI 给出的是可迁移的方案而非一次性脚本——这正是挑战要求的「换一门课同样可复跑」。
