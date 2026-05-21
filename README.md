# Claude Code Skills 學習筆記

整理自 [Claude Youtube 官方頻道課程 Claude Code Skills](https://youtube.com/playlist?list=PLmWCw1CzcFim_hkruZSlABOUOAAQ5JMyo&si=fGO447oWArr1Txw9)，共 6 堂課。

## 閱讀方式

| 格式 | 連結 |
|------|------|
| 網頁版（GitHub Pages） | https://zoe74084.github.io/claude-code-skills-notes/ |
| PDF 下載 | [claude-code-skills-notes.pdf](handouts/claude-code-skills-notes.pdf) |
| Markdown 純文字 | [claude-code-skills-notes.md](handouts/claude-code-skills-notes.md) |

## 課程內容

| # | 主題 |
|---|------|
| 01 | What Are Skills? — Skills 的定義、存放位置、vs CLAUDE.md |
| 02 | Troubleshooting Skills — 觸發失敗、路徑錯誤、衝突排查 |
| 03 | Sharing Skills — Repo 提交、Plugin、Enterprise 部署、Sub-agents |
| 04 | Skills vs Other Features — 與 CLAUDE.md / Sub-agents / Hooks / MCP 的差異 |
| 05 | Configuration & Multi-file Skills — Metadata 欄位、Progressive Disclosure、Scripts |
| 06 | Creating Your First Skill — 建立流程、Priority 規則、更新與刪除 |

## 延伸學習

- [Introduction to Agent Skills — Anthropic Skilljar](https://anthropic.skilljar.com/introduction-to-agent-skills)（官方認證課程，完成後可取得 Skills 相關證照）
- [The Complete Guide to Building Skills for Claude（PDF）](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)（Anthropic 官方發布的 Skills 建立指南）

## 檔案結構

```
├── index.html          # 網頁版（GitHub Pages 服務）
├── handouts/
│   ├── *.pdf           # PDF 版（含筆記欄）
│   └── *.md            # Markdown 純文字版
└── _dev/
    ├── build_pdf.py    # PDF 產生器（Chrome headless）
    └── fix_terms.py    # 台灣用語批次替換
```
