#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translate.py —— 机器翻译 + 术语表注入流水线
============================================
把 extract.py 产出的英文 Markdown 翻译成中文，核心有三点（对应 C1 的
「机器翻译 + 术语表 + 人工校对」）：

  1. 术语统一：把 glossary.csv 的「英→中」对照注入系统提示词，要求模型
     全文使用统一译法，避免同一个词翻成好几种中文。
  2. 长文分块：按标题/段落切块，避免超上下文窗口，且块与块之间保留
     小段重叠以维持语篇连贯。
  3. 可复跑：换一门课的资料，只要替换 <源目录> 和 glossary.csv 即可重跑。

后端：默认走 OpenAI 兼容的 chat/completions 接口（可配 base_url / model /
      api_key，绝大多数国产模型与本地 Ollama 均兼容）。
      设置 --prepare-only 只生成「已注入术语的翻译提示词」到 prompts/ 目录，
      便于无 API Key 时离线人工/他方模型执行同一套提示词。

用法：
    python translate.py <源目录> <输出目录> [--prepare-only]
    python translate.py ./source ./translated --prepare-only

环境变量：
    LLM_API_KEY    API Key（未设且非 prepare-only 时直接报错退出）
    LLM_BASE_URL   默认 https://api.openai.com/v1
    LLM_MODEL      默认 gpt-4o-mini
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests  # type: ignore
except ImportError:
    requests = None

GLOSSARY = Path(__file__).with_name("glossary.csv")
# 每个请求的字符上限（中文按 1 字算，留出术语表占用）
CHUNK_CHARS = 4000
OVERLAP_CHARS = 200

SYSTEM_PROMPT = """你是技术文档英译中的资深译者，正在翻译斯坦福 CS146S「现代软件开发者」课程的阅读材料。
翻译要求：
1. 忠实准确：不遗漏、不增删信息，代码块、命令、URL、专有名词保持原样。
2. 术语统一：严格遵循下方「术语对照表」的译法；表中未列出的术语，首次出现用
   「中文（English）」标注，之后保持一致。
3. 语气专业、通顺，符合中文技术文档习惯，避免机器翻译腔（如生硬的"的"字句）。
4. 保留 Markdown 结构（标题层级、列表、代码块、表格、引用）。
5. 只在确有必要时调整语序以贴合中文表达，不改变原文含义。

术语对照表：
{glossary}
"""

TRANSLATE_TEMPLATE = """请将以下英文技术文档翻译成中文（保留 Markdown 格式）：

{chunk}
"""


def load_glossary(path: Path) -> str:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    lines = [f"- {r['en']} → {r['zh']}" for r in rows if r.get("en") and r.get("zh")]
    return "\n".join(lines)


def split_chunks(text: str, limit: int = CHUNK_CHARS) -> list:
    """按段落切块，尽量在标题/空行处断开，并加少量重叠保持连贯。"""
    paras = text.split("\n\n")
    chunks, cur = [], ""
    for p in paras:
        if len(cur) + len(p) + 2 <= limit:
            cur = (cur + "\n\n" + p).strip() if cur else p
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)

    # 加重叠（相邻块各带前一块的尾巴）
    if len(chunks) > 1:
        overlapped = [chunks[0]]
        for i in range(1, len(chunks)):
            prev_tail = chunks[i - 1][-OVERLAP_CHARS:]
            overlapped.append(prev_tail + "\n\n" + chunks[i])
        return overlapped
    return chunks


def prepare_prompts(glossary: str, text: str, out_dir: Path, stem: str) -> list:
    system = SYSTEM_PROMPT.format(glossary=glossary)
    chunks = split_chunks(text)
    prompt_dir = out_dir / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    metas = []
    for i, c in enumerate(chunks):
        meta = {
            "doc": stem,
            "chunk": i,
            "system": system,
            "user": TRANSLATE_TEMPLATE.format(chunk=c),
        }
        metas.append(meta)
        (prompt_dir / f"{stem}.{i:02d}.prompt.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return metas


def translate_via_api(system: str, user: str) -> str:
    if requests is None:
        raise RuntimeError("需要 requests：pip install requests")
    key = os.environ.get("LLM_API_KEY")
    if not key:
        raise RuntimeError("未设置 LLM_API_KEY")
    base = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    resp = requests.post(
        f"{base.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        },
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def main(argv):
    src_dir = Path(argv[1])
    out_dir = Path(argv[2])
    prepare_only = "--prepare-only" in argv
    out_dir.mkdir(parents=True, exist_ok=True)

    glossary = load_glossary(GLOSSARY)
    system = SYSTEM_PROMPT.format(glossary=glossary)

    md_files = sorted(src_dir.glob("*.md"))
    total = 0
    for md in md_files:
        if md.name.startswith("_"):
            continue
        text = md.read_text(encoding="utf-8")
        # 去掉 extract 留下的 source 注释头
        text = re.sub(r"^<!-- source: .* -->\n", "", text)

        if prepare_only:
            metas = prepare_prompts(glossary, text, out_dir, md.stem)
            print(f"[prepare] {md.stem}: {len(metas)} 块")
            continue

        translated_parts = [translate_via_api(system, TRANSLATE_TEMPLATE.format(chunk=c))
                            for c in split_chunks(text)]
        result = "\n\n".join(translated_parts)
        (out_dir / md.name).write_text(result, encoding="utf-8")
        total += 1
        print(f"[ok] {md.stem}")

    if prepare_only:
        print("已生成提示词到", out_dir / "prompts")
    else:
        print(f"翻译完成 {total} 篇 -> {out_dir}")


if __name__ == "__main__":
    main(sys.argv)
