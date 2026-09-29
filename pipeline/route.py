#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
route.py —— 按授权分级路由处理策略
=====================================
依据 license_manifest.csv 对每份资料决定产出形态：

    tier A -> full_translation  授权允许翻译，产出逐段完整译文
    tier B -> study_notes       专有或禁止演绎(ND)，产出中文精读笔记
    tier C -> pending_ocr       无可提取文本，待 OCR
    unavailable -> 抓取失败，列入已知缺口

为什么要有这一层：课程要求「≥80% 讲义有对应中文」且要「发布」，
但这 31 篇来源授权差异极大——Google SRE Book 是 CC BY-NC-**ND**（禁止演绎，
翻译即违规），OWASP 是 CC BY-SA（可以翻），多数商业博客则未授权全文再发布。
不分级就会做出一个「看着完整、实际不能发」的包。

用法：
    python route.py                     # 只打印分流计划
    python route.py --check             # 校验产物是否齐全并给出覆盖率
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "pipeline" / "license_manifest.csv"
SOURCE = ROOT / "source"
PDF_SOURCE = ROOT / "pdf_source"
ZH = ROOT / "zh"

LABEL = {
    "full_translation": "A 全文翻译",
    "study_notes": "B 中文精读笔记",
    "pending_ocr": "C 待 OCR",
    "unavailable": "X 抓取失败",
}


def load():
    with MANIFEST.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv):
    rows = load()
    plan = {}
    for r in rows:
        plan.setdefault(r["handling"], []).append(r)

    if "--check" in argv:
        done_a = done_b = 0
        missing = []
        for r in rows:
            page = r["page"]
            is_pdf = page.endswith(".pdf")
            target = (ZH / "pdf" if is_pdf else ZH / "阅读材料")
            target = target / (page.replace(".pdf", "") + ".md")
            ok = target.exists() and target.stat().st_size > 200
            if r["handling"] == "full_translation" and ok:
                done_a += 1
            elif r["handling"] == "study_notes" and ok:
                done_b += 1
            elif r["handling"] in ("unavailable", "pending_ocr"):
                pass
            else:
                missing.append(page)
        total_zh = done_a + done_b
        pct = total_zh / max(1, done_a + done_b + len(missing)) * 100
        print(f"覆盖：{total_zh} / {len(rows)}  ({pct:.1f}%)")
        print(f"  A 全文翻译完成：{done_a}")
        print(f"  B 精读笔记完成：{done_b}")
        print(f"  缺失 {len(missing)} 篇：")
        for m in missing:
            print(f"    - {m}")
        return 0 if pct >= 80 else 1

    for handling, items in sorted(plan.items()):
        print(f"\n=== {LABEL.get(handling, handling)}  ({len(items)} 篇) ===")
        for r in items:
            print(f"  {r['page']:<42} {r['license']}")
    print(
        "\n提示：A 级做全文翻译；B 级做精读笔记（核心概念+代码+数据+原文链接，"
        "不逐段复述原文）；X 级列入 README「已知缺口」。"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
