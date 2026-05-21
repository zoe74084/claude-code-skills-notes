#!/usr/bin/env python3
"""Replace non-Taiwan tech terms with Taiwan-standard equivalents in all handout files."""

import os

BASE = "/Users/ding/Desktop/claude-code-skills-notes/handouts"

REPLACEMENTS = [
    # 編程 → 程式設計
    ("編程工具",    "程式設計工具"),
    ("編程",        "程式設計"),
    # 技術棧 → 技術堆疊
    ("技術棧",      "技術堆疊"),
    # 腳本 → 指令稿（shell/script 語境）
    ("執行腳本",    "執行指令稿"),
    ("腳本",        "指令稿"),
    # 工作流 → 工作流程
    ("工作流中",    "工作流程中"),
    ("工作流的",    "工作流程的"),
    # 子代理 → 子代理程式
    ("子代理程式",  "子代理程式"),   # passthrough
    ("子代理，",    "子代理程式，"),
    ("子代理。",    "子代理程式。"),
]

def apply_replacements(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text

exts = (".html", ".md")
changed = []

for fname in sorted(os.listdir(BASE)):
    if not any(fname.endswith(e) for e in exts):
        continue
    path = os.path.join(BASE, fname)
    with open(path, encoding="utf-8") as f:
        original = f.read()
    updated = apply_replacements(original)
    if updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        changed.append(fname)
        print(f"  updated: {fname}")
    else:
        print(f"  no change: {fname}")

print(f"\nDone. {len(changed)} files updated.")
