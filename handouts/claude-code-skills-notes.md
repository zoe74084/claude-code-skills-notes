# Claude Code Skills — 學習筆記

> 資料來源：整理自 Claude Youtube 官方頻道課程 Claude Code Skills
> 整理日期：2026-05-21

---

## Lesson 1：What Are Skills?

### 核心定義
Skills 是一種 Markdown 檔案，用來教 Claude 如何做某件事一次，之後 Claude 會在適當時機自動套用。

與傳統「每次對話重新說一遍」相比，Skills 是**一次寫好、自動觸發**的知識注入機制。

### Skills 的三個存放位置

| 位置 | 路徑 | 適用對象 |
|------|------|---------|
| 個人 Skills | `~/.claude/skills/` | 個人偏好（commit 格式、解釋風格）、跟著你走 |
| 專案 Skills | `./.claude/skills/`（repo 根目錄） | 團隊標準，clone 就有 |
| Plugin Skills | 透過 Marketplace 安裝 | 社群分享的通用 Skill |

### Skill 的組成結構
```
my-skill/
└── skill.md       ← 唯一必要檔案（名稱固定）
```

`skill.md` 包含：
1. **Frontmatter（YAML）**：`name`、`description` 等 metadata
2. **Instructions**：`---` 之後的所有內容是 Claude 執行時讀取的指令

### Skills vs CLAUDE.md

| | CLAUDE.md | Skills |
|-|-----------|--------|
| 載入時機 | **每次對話都載入** | **按需載入（匹配才載入）** |
| 適用情境 | 永遠有效的專案規範 | 特定任務才需要的知識 |
| 範例 | 「永遠用 TypeScript strict mode」 | PR review checklist |

### 關鍵原則
- Skills 最適合：特定任務的專業知識、只有部分時候才需要的規則
- 一旦你發現自己重複向 Claude 解釋同樣的事情 → **那就是一個 Skill**

---

## Lesson 2：Troubleshooting Skills

### 四類常見問題

#### 問題 1：Skill 沒有觸發
**原因：** description 的語義與你的請求沒有足夠重疊
**解法：**
1. 檢查你的 description，確認和你說的話意思有重疊
2. 加入 trigger phrases（你實際會說的句子）
3. 測試多種說法：「幫我 profile」「為什麼這麼慢」「讓這個更快」

#### 問題 2：Skill 沒有出現在清單中
**需確認的事項：**
- `skill.md` 必須放在以 **skill 名稱命名的目錄**裡，不能直接放在 skills 根目錄
- 檔名必須是 `skill.md`（全小寫）
- 跑 `claude --debug` 看載入錯誤

#### 問題 3：用到錯誤的 Skill（衝突）
**原因：** 兩個 Skill 的 description 太相似
**解法：**
- 讓各 Skill 的 description 明顯不同
- 個人 Skill 若與企業 Skill 同名 → **企業版永遠優先**，請改名

**Priority 順序（高→低）：**
1. Enterprise（管理設定）
2. Personal（`~/.claude/skills/`）
3. Project（`./.claude/skills/`）
4. Plugins

#### 問題 4：Skill 載入但執行失敗
- 確認外部套件已安裝
- Script 需要執行權限：到處用 `/`，Windows 也一樣

### 快速排查清單
```
沒觸發？    → 優化 description 和 trigger phrases
沒載入？    → 檢查路徑、檔名、YAML 語法
用錯 Skill？→ 讓 descriptions 更明確
被覆蓋？    → 確認 priority，必要時改名
Plugin 不見？→ 清 cache、重新安裝
執行失敗？  → 確認相依套件、檔案權限
```

---

## Lesson 3：Sharing Skills

### 三種分享方式

#### 方式 1：提交到 Repository（最簡單）
- 把 Skills 放進 `.claude/skills/`
- Clone repo 的人自動就有，push 更新後大家下次 pull 即可
- 適合：團隊 coding 規範、專案特定的 workflow

#### 方式 2：透過 Plugin 分發
- 在 plugin 專案中建立 `skills/` 目錄
- 結構與 `.claude/skills/` 相同（名稱目錄 + `skill.md`）
- 上架 Marketplace 後其他人可下載安裝
- 適合：不限特定專案的通用 Skill、開源社群分享

#### 方式 3：Enterprise 管理員部署
- 透過 Managed Settings 組織級部署
- **優先權最高**，會覆蓋同名的個人/專案/Plugin Skill
- 適合：強制標準、合規需求、安全流程

### 重要：Sub-agents 不自動繼承 Skills

Sub-agent 啟動時是**全新的乾淨 context**，不會自動看到你的 Skills。

**規則：**
- 內建 agents（Explorer、Plan、Verify）**完全無法存取** Skills
- 只有你**自訂的 sub-agent** 能用，而且要**明確列出**

**作法：在 `.claude/agents/your-agent.md` 加入 `skills` 欄位**
```yaml
---
name: frontend-reviewer
skills:
  - pr-review
  - brand-guidelines
---
```

**注意：** Sub-agent 的 Skills 是**啟動時一次載入**，不是按需載入。只列永遠相關的 Skills。

---

## Lesson 4：Skills vs 其他 Claude Code 功能

### 五種客製化工具對比

| 工具 | 載入時機 | 適用情境 |
|------|---------|---------|
| **CLAUDE.md** | 每次對話都載入 | 永遠有效的專案規範、框架偏好 |
| **Skills** | 請求匹配才載入 | 特定任務的專業知識 |
| **Sub-agents** | 獨立 context 執行 | 委派獨立任務、需要隔離的工作 |
| **Hooks** | 事件觸發 | 每次存檔時 lint、特定動作前驗證 |
| **MCP Servers** | 提供外部工具 | 連接外部 API、資料庫等 |

### 決策框架

**用 CLAUDE.md 當：**
- 規則永遠需要套用（「永遠不要修改 DB schema」）
- 框架偏好、程式碼風格

**用 Skills 當：**
- 知識只在特定任務時需要
- 詳細的流程說明（放進每次對話會太佔 context）

**用 Sub-agents 當：**
- 想委派任務到獨立執行環境
- 需要與主對話不同的工具存取權

**用 Hooks 當：**
- 每次存檔都要跑的操作
- 特定工具呼叫前的驗證

### 典型組合
```
CLAUDE.md       → 永遠有效的專案規範
Skills          → 特定任務的專業知識（PR review、brand guide）
Hooks           → 自動化操作（存檔時 lint）
```

---

## Lesson 5：Configuration & Multi-file Skills

### skill.md Metadata 欄位

```yaml
---
name: pr-review          # 必填，小寫+連字號，max 64 字
description: |           # 必填，Claude 用來決定何時啟動，max 1024 字
  Helps with PR review...
  Trigger: "review PR", "check my changes"
allowed_tools:           # 選填，限制此 Skill 可用的工具
  - Read
  - Bash
model: claude-sonnet-4-6 # 選填，指定使用哪個模型
---
```

### allowed_tools：限制工具存取
- 如果你只想讓 Skill 讀檔（不能改）→ 只列 `Read`
- 省略 `allowed_tools` → 不限制（沿用一般權限模型）

### Progressive Disclosure（漸進式揭露）
**問題：** 一個複雜 Skill 如果全塞進 `skill.md`，會佔滿 context window 又難維護。

**解法：** 主要指令放 `skill.md`，詳細參考資料放外部檔案，讓 Claude 按需讀取。

```
my-skill/
├── skill.md              ← 核心指令，< 500 行
├── references/
│   └── architecture.md   ← 只有被問到系統設計時才讀
├── scripts/
│   └── validate.sh       ← 執行腳本（不讀進 context，直接跑）
└── assets/
    └── template.json     ← 模板資料
```

**在 skill.md 裡這樣引用：**
```markdown
如果被問到系統架構，讀 references/architecture.md。
```

### Scripts 的優勢
- Script **執行**，不把內容讀進 context → 只消耗 output 的 tokens
- 適合：環境驗證、資料轉換、需要可靠性的操作（比 LLM 生成的程式碼更穩定）
- 告訴 Claude「**執行**這個 script」，而不是「讀」它

### 建議
- `skill.md` 控制在 **500 行以內**，超過就考慮拆分
- 把常用的「重型參考資料」移到 `references/`

---

## Lesson 6：Creating Your First Skill

### 建立流程（以個人 Skill 為例）

```bash
# 1. 在 personal skills 目錄建立 skill 目錄
mkdir -p ~/.claude/skills/explain-code

# 2. 建立 skill.md
touch ~/.claude/skills/explain-code/skill.md
```

**skill.md 內容結構：**
```markdown
---
name: explain-code
description: |
  Explains code using visual diagrams and analogies.
  Use when asked to "explain this function", "help me understand this code",
  "what does this do", "walk me through this".
---

當解釋程式碼時：
1. 先用一個日常生活的比喻說明核心概念
2. 用流程圖（ASCII 或文字描述）展示資料流
3. 逐步說明每個關鍵步驟
4. 最後給一個使用範例
```

```bash
# 3. 重啟 Claude Code 讓它載入新 Skill
# 4. 確認 Skill 已載入
claude --list-skills

# 5. 測試
# 在對話中說：「幫我解釋這段 function 在做什麼」
```

### Claude Code 載入 Skill 的流程

```
啟動 → 掃描 4 個位置（Enterprise > Personal > Project > Plugin）
     → 載入每個 Skill 的 name + description（不載入完整內容）
     ↓
收到請求 → 比對 descriptions（語義匹配）
         → 找到匹配 → 詢問確認是否載入
         → 確認後讀取完整 skill.md 並執行
```

**重點：** 啟動時只載入 name + description，**全文不進 context**，直到被觸發才讀。

### Priority 規則（衝突時）

```
Enterprise（管理設定）        → 最高優先
Personal（~/.claude/skills/） → 第二
Project（./.claude/skills/）  → 第三
Plugins                       → 最低
```

**避免衝突的命名建議：**
- `review` → 太泛
- `frontend-pr-review` 或 `security-review` → 明確、不易衝突

### 更新與刪除
- **更新：** 直接編輯 `skill.md`，重啟 Claude Code
- **刪除：** 刪除整個 skill 目錄，重啟 Claude Code

---

## 核心重點總覽

| 概念 | 一句話 |
|------|--------|
| Skill 定義 | 一次寫好，Claude 自動按情境載入的知識 |
| 存放位置 | Personal / Project / Plugin，各有適用對象 |
| 觸發機制 | description 語義匹配 → 按需載入 |
| vs CLAUDE.md | CLAUDE.md 永遠載入，Skills 只在需要時載入 |
| Priority | Enterprise > Personal > Project > Plugin |
| Sub-agent | 不繼承 Skills，要明確列出 |
| 多檔案 | skill.md < 500 行，詳細資料放外部按需讀取 |
| Scripts | 執行不讀入，省 context tokens |

---

## 延伸學習資源

| 資源 | 說明 |
|------|------|
| [Claude Code Skills — YouTube 官方頻道](https://youtube.com/playlist?list=PLmWCw1CzcFim_hkruZSlABOUOAAQ5JMyo&si=fGO447oWArr1Txw9) | 本份筆記的原始資料來源，共 6 支短片 |
| [Introduction to Agent Skills — Anthropic Skilljar](https://anthropic.skilljar.com/introduction-to-agent-skills) | 官方認證課程，完成可取得證照 |
| [The Complete Guide to Building Skills for Claude（PDF）](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) | Anthropic 官方完整 Skills 建立指南 |
| [Claude Cookbook — Skills Notebooks](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) | ⚠️ 此連結為 Anthropic API Skills（透過 API 生成 Excel / PowerPoint / PDF），與本課程的 Claude Code Skills（skill.md 檔案）是不同的功能 |
