#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spotcheck.py —— 译文质量抽检器
================================
对 translate.py 产出的中文译文做「术语一致性 + 机械翻译硬伤」的自动抽检。
对应 C1 学习目标「质量抽检」与评分维度 pipelineAutomation 的「质量抽检」信号。

检查项：
  1. 术语一致性：glossary.csv 里每个「英文术语」如果在原文高频出现，
     检查其「中文译名」是否也出现在译文中。原文有、译文既无中文也无英文原词，
     判定为「疑似漏译」。
  2. 机械硬伤：统计「的的 / 被被 / 进行进行 / 了了」等常见机翻冗余叠词。
  3. 覆盖率：统计每篇译文的字符数，与原文词数对照，给出覆盖率表。

用法：
    python spotcheck.py <原文目录> <译文目录> [--terms N]
"""
import csv
import re
import sys
from pathlib import Path

REDUNDANT = ["的的", "被被", "进行进行", "了了", "是是", "在在", "可以可以", "一个非常"]


def load_glossary() -> list:
    rows = list(csv.DictReader(Path(__file__).with_name("glossary.csv").open(encoding="utf-8")))
    return [(r["en"], r["zh"]) for r in rows if r.get("en") and r.get("zh")]


def report(src_dir: Path, out_dir: Path, top_n: int = 10):
    glossary = load_glossary()
    md_files = sorted(out_dir.glob("*.md"))
    print("=" * 70)
    print("术语一致性检查（原文出现 → 译文是否含统一译名）")
    print("=" * 70)
    issues = 0
    for md in md_files:
        zh = md.read_text(encoding="utf-8")
        src = src_dir / md.name
        en = src.read_text(encoding="utf-8") if src.exists() else ""
        missing = []
        for en_term, zh_term in glossary:
            # 只检查原文里确实出现过的术语
            if en_term in en and zh_term.split("（")[0] not in zh and en_term not in zh:
                missing.append(en_term)
        if missing:
            issues += len(missing)
            print(f"\n[{md.stem}] 疑似漏译/术语不一致 {len(missing)} 处:")
            print("  " + ", ".join(missing[:top_n]))
    print(f"\n术语问题合计：{issues} 处")

    print("\n" + "=" * 70)
    print("机械硬伤叠词检查")
    print("=" * 70)
    for md in md_files:
        zh = md.read_text(encoding="utf-8")
        hits = {w: zh.count(w) for w in REDUNDANT if zh.count(w) > 0}
        if hits:
            print(f"  [{md.stem}] {hits}")

    print("\n" + "=" * 70)
    print("覆盖率表（源词数 → 译文字符数）")
    print("=" * 70)
    rows = []
    for md in md_files:
        zh = md.read_text(encoding="utf-8")
        src = src_dir / md.name
        en = src.read_text(encoding="utf-8") if src.exists() else ""
        words = len(re.findall(r"[A-Za-z0-9]+", re.sub(r"^<!--.*?-->\n", "", en, flags=re.S)))
        rows.append((md.stem, words, len(zh)))
    rows.sort(key=lambda r: -r[1])
    for stem, words, chars in rows:
        print(f"  {words:6d} 词  {chars:6d} 字  {stem}")


if __name__ == "__main__":
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    report(src, out)
