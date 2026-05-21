#!/usr/bin/env python3
"""
Generate Claude Code Skills PDF from index.html.
Builds: cover page + TOC + 6 lesson sections → handouts/claude-code-skills-notes.pdf
"""

import re, subprocess, os, sys

ROOT      = "/Users/ding/Desktop/claude-code-skills-notes"
ELEC_HTML = f"{ROOT}/index.html"
PDF_OUT   = f"{ROOT}/handouts/claude-code-skills-notes.pdf"
CHROME    = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SOURCE    = "https://youtube.com/playlist?list=PLmWCw1CzcFim_hkruZSlABOUOAAQ5JMyo&si=fGO447oWArr1Txw9"

LESSONS = [
    ("lesson01", "What Are Skills?",                  "什麼是 Skills？"),
    ("lesson02", "Troubleshooting Skills",             "Skills 的除錯與排查"),
    ("lesson03", "Sharing Skills",                     "分享與部署 Skills"),
    ("lesson04", "Skills vs Other Features",           "Skills 與其他功能的差異"),
    ("lesson05", "Configuration & Multi-file Skills",  "進階設定與多檔案架構"),
    ("lesson06", "Creating Your First Skill",          "建立你的第一個 Skill"),
]

# ── 1. read source HTML ────────────────────────────────────────────────────

with open(ELEC_HTML, encoding="utf-8") as f:
    raw = f.read()

# ── 2. extract CSS ─────────────────────────────────────────────────────────

css_m = re.search(r'<style>(.*?)</style>', raw, re.DOTALL)
body_css = css_m.group(1) if css_m else ""

# strip sidebar/layout-only rules
for pat in [
    r'/\* ── Layout[^}]*\}',
    r'\.sidebar\b[^{]*\{[^}]*\}',
    r'\.sidebar-header\b[^{]*\{[^}]*\}',
    r'\.nav-[a-z-]+\b[^{]*\{[^}]*\}',
    r'\.layout\b[^{]*\{[^}]*\}',
    r'\.main\b[^{]*\{[^}]*\}',
    r'\.mobile-header\b[^{]*\{[^}]*\}',
    r'\.hamburger\b[^{]*\{[^}]*\}',
    r'\.sidebar-overlay\b[^{]*\{[^}]*\}',
]:
    body_css = re.sub(pat, '', body_css, flags=re.DOTALL)

# ── 3. extract lesson sections ─────────────────────────────────────────────

def extract_section(html, lid):
    pat = rf'(<section class="lesson" id="{lid}">.*?</section>)'
    m = re.search(pat, html, re.DOTALL)
    return m.group(1) if m else ""

VIDEO_URLS = {
    "lesson01": "https://www.youtube.com/watch?v=bjdBVZa66oU",
    "lesson02": "https://www.youtube.com/watch?v=YBa1cwaG7is",
    "lesson03": "https://www.youtube.com/watch?v=OCBi3eScNLk",
    "lesson04": "https://www.youtube.com/watch?v=IgNN4v0BJdU",
    "lesson05": "https://www.youtube.com/watch?v=98KaK_rn5rQ",
    "lesson06": "https://www.youtube.com/watch?v=Wx6_vjFFyHM",
}

lesson_sections = []
for lid, en, zh in LESSONS:
    sec = extract_section(raw, lid)
    # replace video thumbnail block with a pdf-friendly link block
    yt = VIDEO_URLS.get(lid, "")
    sec = re.sub(
        r'<a href="[^"]*" target="_blank" class="video-link">.*?</a>',
        f'<div class="pdf-video-link">▶ <a href="{yt}">前往 YouTube 觀看影片</a></div>',
        sec, flags=re.DOTALL
    )
    # inject "回目錄" button after lesson-tag span
    sec = re.sub(
        r'(<span class="lesson-tag">Lesson \d+</span>)',
        r'<div class="lesson-top">\1<a href="#toc" class="back-btn">↑ 回目錄</a></div>',
        sec
    )
    # inject 我的筆記 section before </section>
    notes_html = """
<div class="notes-section">
  <div class="notes-header">我的筆記 MY NOTES</div>
  <div class="notes-lines">
    <div class="notes-line"></div>
    <div class="notes-line"></div>
    <div class="notes-line"></div>
    <div class="notes-line"></div>
    <div class="notes-line"></div>
  </div>
</div>"""
    sec = sec.replace('</section>', notes_html + '\n</section>')
    lesson_sections.append((lid, en, zh, sec))

# ── inject pdf-source into last lesson ────────────────────────────────────
source_footer_html = f'<div class="pdf-source">資料來源：整理自 <a href="{SOURCE}">Claude Youtube 官方頻道課程 Claude Code Skills</a></div>'
lid, en, zh, sec = lesson_sections[-1]
sec = sec.replace('</section>', source_footer_html + '\n</section>')
lesson_sections[-1] = (lid, en, zh, sec)

# ── 4. build TOC ───────────────────────────────────────────────────────────

toc_items = "\n".join(
    f'    <li><a href="#{lid}"><span class="toc-num">0{i+1}</span>{en}<span class="toc-zh">{zh}</span></a></li>'
    for i, (lid, en, zh, _) in enumerate(lesson_sections)
)

lesson_html = "\n\n".join(sec for _, _, _, sec in lesson_sections)

# ── 5. assemble PDF HTML ───────────────────────────────────────────────────

pdf_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>Claude Code Skills — 學習筆記</title>
<style>
@page {{
  size: A4;
  margin: 16mm 18mm;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", sans-serif;
  background: #fff;
  color: #1a1a1a;
  font-size: 13.5px;
  line-height: 1.75;
}}

/* ── Cover ── */
.cover {{
  height: 265mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #1a1a1a;
  color: #fff;
  border-radius: 6px;
  padding: 32px;
  overflow: hidden;
  break-after: page;
  page-break-after: always;
}}
.cover-tag {{ font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #d97706; background: rgba(217,119,6,.15); padding: 4px 14px; border-radius: 99px; margin-bottom: 24px; }}
.cover h1 {{ font-size: 36px; font-weight: 900; color: #fff; letter-spacing: -0.01em; margin-bottom: 10px; line-height: 1.2; border: none; padding: 0; }}
.cover-sub {{ font-size: 16px; color: #aaa; margin-bottom: 36px; font-weight: 400; }}
.cover-divider {{ width: 48px; height: 3px; background: #d97706; border-radius: 2px; margin: 0 auto 32px; }}
.cover-desc {{ font-size: 13px; color: #888; line-height: 1.8; max-width: 420px; }}
.cover-source {{ margin-top: 36px; font-size: 11px; color: #555; }}
.cover-source a {{ color: #d97706; text-decoration: none; }}

/* ── TOC ── */
.toc-page {{ break-after: page; page-break-after: always; }}
.toc-page h2 {{ font-size: 22px; font-weight: 800; color: #111; margin-bottom: 28px; padding-bottom: 10px; border-bottom: 3px solid #d97706; display: block; letter-spacing: normal; text-transform: none; }}
.toc-page h2::before {{ display: none; }}
.toc-list {{ list-style: none; padding: 0; }}
.toc-list li {{ margin-bottom: 0; border-bottom: 1px solid #f0f0ee; }}
.toc-list a {{ display: flex; align-items: baseline; gap: 12px; padding: 10px 4px; color: #1a1a1a; text-decoration: none; font-size: 14px; font-weight: 600; }}
.toc-num {{ font-size: 11px; font-weight: 700; color: #d97706; min-width: 24px; font-family: "SF Mono", monospace; }}
.toc-zh {{ font-size: 12px; font-weight: 400; color: #888; margin-left: 6px; }}

/* ── Back-to-TOC ── */
.lesson-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }}
.back-btn {{ font-size: 11px; font-weight: 600; color: #b45309; background: #fef3c7; border: 1px solid #fde68a; border-radius: 99px; padding: 3px 12px; text-decoration: none; white-space: nowrap; flex-shrink: 0; }}

/* ── Lesson pagination ── */
.lesson {{ margin-bottom: 0; padding-bottom: 0; border-bottom: none; break-before: page; page-break-before: always; }}

/* ── No-split rules ── */
table, thead, tbody, tr, pre,
.example-box, .tip-box, .key-rule, .warn-box, .cta-box, .note-box,
.workflow, .priority-cards, .priority-card {{ break-inside: avoid; page-break-inside: avoid; }}
h1, h2, h3 {{ break-after: avoid; page-break-after: avoid; orphans: 4; widows: 4; }}
li {{ break-inside: avoid; page-break-inside: avoid; }}

/* ── Notes Section ── */
.notes-section {{ margin-top: 28px; padding-top: 16px; border-top: 2px dashed #fde68a; break-inside: avoid; page-break-inside: avoid; }}
.notes-header {{ font-size: 11px; font-weight: 700; letter-spacing: 0.09em; color: #b45309; text-transform: uppercase; display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }}
.notes-header::before {{ content: ""; display: block; width: 4px; height: 14px; background: #d97706; border-radius: 2px; }}
.notes-lines {{ display: flex; flex-direction: column; gap: 26px; }}
.notes-line {{ height: 0; border-bottom: 1px solid #e5e7eb; }}

/* ── PDF Source Footer ── */
.pdf-source {{ margin-top: 20px; padding: 10px 0 4px; border-top: 1px solid #e5e7eb; font-size: 11px; color: #aaa; text-align: center; }}
.pdf-source a {{ color: #d97706; text-decoration: none; }}

/* ── Inherited styles ── */
{body_css}
</style>
</head>
<body>

<div class="cover">
  <div class="cover-tag">Course Notes</div>
  <h1>Claude Code Skills</h1>
  <div class="cover-sub">學習筆記</div>
  <div class="cover-divider"></div>
  <div class="cover-desc">
    6 個模組，涵蓋 Claude Code Skills 的建立、設定、分享與除錯
  </div>
  <div class="cover-source">
    資料來源：整理自 <a href="{SOURCE}">Claude Youtube 官方頻道課程 Claude Code Skills</a>
  </div>
</div>

<div class="toc-page" id="toc">
  <h2>目錄 Contents</h2>
  <ul class="toc-list">
{toc_items}
  </ul>
</div>

{lesson_html}

</body>
</html>"""

# ── 6. write temp HTML & generate PDF ─────────────────────────────────────

pdf_src = f"{ROOT}/_dev/_pdf_src.html"
with open(pdf_src, "w", encoding="utf-8") as f:
    f.write(pdf_html)
print(f"PDF source written ({len(pdf_html):,} chars)")

print("Generating PDF with Chrome headless...")
cmd = [
    CHROME,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_OUT}",
    f"file://{pdf_src}",
]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("Chrome stderr:", result.stderr[:500])
    sys.exit(1)

os.remove(pdf_src)
size_kb = os.path.getsize(PDF_OUT) // 1024
print(f"PDF saved: {PDF_OUT} ({size_kb} KB)")
print("Done.")
