#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract.py —— CS146S 离线缓存正文提取器
========================================
从 Stanford CS146S「The Modern Software Developer」课程离线缓存中，
把每一篇阅读文章的「正文」从 HTML 壳子里剥离出来，输出干净的 Markdown。

设计目标（对应 C1 学习目标「批量抓取并归档」）：
  1. 异源鲁棒：课程文章来自 Google Cloud / promptingguide.ai / Stytch /
     Cloudflare / Anthropic / Semgrep … 等十几个站点，HTML 结构完全不同，
     因此不做任何站点特判，只用通用启发式。
  2. 正文定位启发式（按优先级）：
       <article>  →  <main>  →  文本密度最高的 <div>
  3. 污点清理：剔除 script / style / nav / header / footer / form /
     dialog / svg / iframe，以及 paywall 与 cookie 横幅。
  4. 占位识别：把「只有几段话的 paywall / 占位页」单独标记为 blocked，
     不进入翻译队列（这些是课程材料里已知的缺口）。

用法：
    python extract.py <离线缓存目录> <输出目录>
    python extract.py ../CS146S_offline ./source

输出：
    <输出目录>/<页面名>.md    每篇一篇 Markdown
    <输出目录>/_manifest.json  提取清单（含状态：ok / blocked / empty）
"""
import json
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    sys.stderr.write("需要 bs4：pip install beautifulsoup4 lxml\n")
    raise

# —— 污点标签：直接整体丢弃 ——
STRIP_TAGS = {
    "script", "style", "noscript", "template", "iframe", "svg", "canvas",
    "nav", "header", "footer", "aside", "form", "dialog", "select",
    "input", "button", "textarea", "object", "embed", "video", "audio",
    "picture", "source",
}
# —— 仅丢弃标签本身、保留其文本 ——
UNWRAP_TAGS = {"a", "span", "b", "strong", "i", "em", "u", "code", "mark"}


def _block_tags(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(STRIP_TAGS):
        tag.decompose()


def _text_density(node: Tag) -> int:
    """粗略衡量一个容器里『真正正文』的量：按段落/标题计权。"""
    score = 0
    for p in node.find_all(["p", "li", "blockquote", "pre"]):
        t = p.get_text(" ", strip=True)
        score += min(len(t), 300)  # 单段封顶，避免一坨长文刷分
    for h in node.find_all(["h1", "h2", "h3", "h4"]):
        score += 80
    return score


def _pick_main(soup: BeautifulSoup) -> Tag:
    """正文定位：article → main → 文本密度最高的 div/body。"""
    for sel in ("article", "main"):
        node = soup.find(sel)
        if node is not None and _text_density(node) > 200:
            return node
    best, best_score = soup.body or soup, -1
    for cand in soup.find_all(["div", "section", "body"]):
        s = _text_density(cand)
        if s > best_score:
            best, best_score = cand, s
    return best


def _inline_text(tag: Tag, out: list) -> None:
    for child in tag.children:
        if isinstance(child, NavigableString):
            out.append(str(child))
        elif isinstance(child, Tag):
            if child.name in STRIP_TAGS:
                continue
            if child.name in UNWRAP_TAGS or child.name in ("br",):
                _inline_text(child, out)
            else:
                out.append(" " + child.get_text(" ", strip=True) + " ")
    return


def _render(node, out: list, base: int = 0) -> None:
    """把正文 DOM 渲染成 Markdown 文本。"""
    for child in node.children:
        if isinstance(child, NavigableString):
            t = str(child)
            if t.strip():
                out.append(t.strip())
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name
        if name in STRIP_TAGS:
            continue
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            lvl = int(name[1])
            out.append("\n" + "#" * lvl + " " + child.get_text(" ", strip=True) + "\n")
        elif name == "p":
            txt = child.get_text(" ", strip=True)
            if txt:
                out.append("\n" + txt + "\n")
        elif name in ("ul", "ol"):
            for li in child.find_all("li", recursive=False):
                out.append("- " + li.get_text(" ", strip=True))
            out.append("")
        elif name == "pre":
            out.append("\n```\n" + child.get_text() + "\n```\n")
        elif name == "blockquote":
            out.append("\n> " + child.get_text(" ", strip=True).replace("\n", "\n> ") + "\n")
        elif name in ("table",):
            _render_table(child, out)
        elif name == "hr":
            out.append("\n---\n")
        elif name in ("div", "section", "article", "main", "figure", "figcaption", "details"):
            _render(child, out)
        else:
            txt = child.get_text(" ", strip=True)
            if txt:
                out.append(txt)
    return


def _render_table(table: Tag, out: list) -> None:
    for tr in table.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
        if cells:
            out.append("| " + " | ".join(cells) + " |")
    out.append("")


def _clean(text: str) -> str:
    text = text.replace("​", "").replace(" ", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_html(path: Path) -> dict:
    html = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")

    title = ""
    if soup.title:
        title = soup.title.get_text(" ", strip=True)
    h1 = soup.find("h1")
    if h1 and not title:
        title = h1.get_text(" ", strip=True)

    _block_tags(soup)
    main = _pick_main(soup)

    buf: list = []
    _render(main, buf)
    text = _clean("\n".join(buf))

    words = len(re.findall(r"[A-Za-z0-9]+", text))
    return {"title": title, "text": text, "words": words}


def classify(text: str, words: int) -> str:
    if words == 0:
        return "empty"
    if words < 60:
        return "blocked"  # paywall / 占位页
    return "ok"


def main(argv):
    src_dir = Path(argv[1])
    out_dir = Path(argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    pages = sorted((src_dir / "pages").glob("*.html"))
    manifest = {}

    for p in pages:
        info = extract_html(p)
        status = classify(info["text"], info["words"])
        manifest[p.stem] = {
            "status": status,
            "title": info["title"],
            "words": info["words"],
        }
        (out_dir / (p.stem + ".md")).write_text(
            f"<!-- source: {p.name} -->\n# {info['title']}\n\n{info['text']}\n",
            encoding="utf-8",
        )

    # 课程主页（index.html）单独导出
    idx = src_dir / "index.html"
    if idx.exists():
        info = extract_html(idx)
        manifest["index"] = {
            "status": "ok",
            "title": info["title"],
            "words": info["words"],
        }
        (out_dir / "index.md").write_text(
            f"<!-- source: index.html -->\n# {info['title']}\n\n{info['text']}\n",
            encoding="utf-8",
        )

    (out_dir / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    ok = sum(1 for m in manifest.values() if m["status"] == "ok")
    blocked = sum(1 for m in manifest.values() if m["status"] == "blocked")
    empty = sum(1 for m in manifest.values() if m["status"] == "empty")
    total_words = sum(m["words"] for m in manifest.values() if m["status"] == "ok")
    print(f"提取完成：ok={ok} blocked={blocked} empty={empty} 正文总词数={total_words}")
    for name, m in manifest.items():
        if m["status"] != "ok":
            print(f"  [!] {m['status']:7s} {name}: {m['title'][:60]}")


if __name__ == "__main__":
    main(sys.argv)
