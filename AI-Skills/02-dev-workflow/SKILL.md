---
name: campcool-dev-workflow
description: 開發流程與計畫技能包。適用情境：收到多步驟任務規格、開始新功能開發、需要撰寫實施計畫、程式碼審查、Git 分支管理、平行子任務調度時使用。整合 obra/superpowers (⭐274k) 的 writing-plans、executing-plans、code-review、using-git-worktrees、finishing-a-development-branch、subagent-driven-development、dispatching-parallel-agents 與 vercel-labs (⭐30k) 的 composition-patterns。特別適用於 Campcool 專案群的 CI 門禁環境（GitHub Actions 部署、PR 品質門禁）。
---

# Campcool 開發流程技能包

## 一句話原則

寫計畫時假設接手的工程師對程式碼庫零上下文；執行時每個任務都是可獨立驗證的最小單元；完成前必須通過品質門禁（CI + 實際行為驗證）。

## 撰寫實施計畫（writing-plans）

開始多步驟開發前先寫計畫，存到 `docs/` 或專案既有的交接文件位置（Campcool 專案慣例放在 README/AI-README.md 的待辦區或 docs/）。

- **範圍檢查**：若規格涵蓋多個獨立子系統，先拆成多個計畫，每個計畫產出可獨立測試的軟體。
- **檔案結構先定**：先列出每個任務要動哪些檔案、各檔案的責任。檔案改一起就放一起；依責任切分而非依技術層切分；既有程式碼庫遵循既有模式。
- **任務粒度**：任務 = 最小單元，各自帶測試週期，值得一次新的審查門禁。建置、設定、文件等步驟併入所屬任務。
- **內容包含**：每個任務的具體修改、程式碼、要測試的東西、要讀的文件。DRY、YAGNI、TDD、勤 commit。

## 執行計畫（executing-plans）

- 照計畫逐項執行，但當證據顯示計畫有誤時允許修正方向（記錄偏離原因）。
- 每個任務完成即 commit，commit 訊息對應計畫中的任務名稱。
- 遇阻時回到根因調查（參考 `campcool-ops-debug` 技能），不要硬繞過。

## 程式碼審查

**請求審查（requesting-code-review）時**：說明改動範圍與風險點、哪些部分最需要關注、如何本地驗證。不要只丟一個 PR 等別人看。

**接收審查（receiving-code-review）時**：以理解為目標而非防衛；區分「事實錯誤」「可讀性」「風格偏好」；對有疑義的建議先問清楚再決定，避免來回多輪。

## Git 分支與工作樹

- **git worktrees（using-git-worktrees）**：同一專案多分支並行開發時使用 worktree 而非 stash 切換；每個 worktree 帶自己名稱（如 `wt-faq-dedupe`）。
- **收尾分支（finishing-a-development-branch）**：合併前先重跑測試、更新文件（**Campcool 慣例：同步更新 AI-README.md/AI-HANDOFF.md 的進度紀錄與待辦清單，與程式碼一起 commit**）、刪除或歸檔 worktree。
- **Campcool CI 門禁注意**：推 main 前確認 `deploy.yml`（typecheck→test→migrations→deploy）會通過；私有倉庫無 branch protection，`pr-check.yml` 是合併前品質門禁；正式部署僅限 main。

## 平行子任務調度

**dispatching-parallel-agents**：當任務可拆成多個同質子任務（如批次翻譯、批量驗證、多文件同步修改）時，平行派出多個子代理，各自帶完整指令與輸出格式，最後由主控代理整合驗收。適用：多站點同時修改 Google Ads 素材、批量更新 AI-README。

**subagent-driven-development**：大型功能開發時，主控代理把子任務（單元實作、測試、文件）分派給子代理，主控負責介面一致與整合測試。適用：TITAN-STAR 加功能、多頁面修改。

## 架構組合模式（composition-patterns）

前端元件與模組設計遵循：單一責任、介面先定、組合勝過繼承。React 專案（blossomkids、campcool-website）適用 vercel-labs 的元件組合指引。

## 參考文件

- `references/writing-plans.md` — 撰寫計畫（obra ⭐274k 原文）
- `references/executing-plans.md` — 執行計畫（obra ⭐274k 原文）
- `references/requesting-code-review.md` / `receiving-code-review.md` — 程式碼審查（obra ⭐274k 原文）
- `references/using-git-worktrees.md` / `finishing-a-development-branch.md` — Git 分支工作流（obra ⭐274k 原文）
- `references/subagent-driven-development.md` / `dispatching-parallel-agents.md` — 平行子任務（obra ⭐274k 原文）
- `references/composition-patterns.md` — 前端組合模式（vercel-labs ⭐30k 原文）
