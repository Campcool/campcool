---
name: campcool-ops-debug
description: 維運與除錯核心技能包。適用情境：正式環境（LINE Bot、Cloudflare Worker、GitHub Pages 網站）出錯、測試失敗、異常行為、性能問題、部署異常時使用。整合 GitHub 高星技能庫精華：obra/superpowers (⭐274k) 的 systematic-debugging、verification-before-completion、test-driven-development，以及 K-Dense-AI (⭐34k) 的 exploratory-data-analysis。同時包含 Campcool 專案群（campcool-bot、leakdoctor-bot、campcool、leakdoctor）的正式環境變更保護規則：D1 資料保護、webhook 簽章驗證、CI 門禁、防假綠驗證。
---

# Campcool 維運與除錯技能包

## 鐵律

**未找到根因前，不允許提任何修復方案。** 症狀式修復（symptom fixes）等同失敗。

> NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

## 適用範圍

任何技術問題：測試失敗、正式環境 bug、預期外行為、性能問題、部署失敗、整合問題。以下情境更要強制使用本流程：
- 時間壓力下（緊急時刻最容易猜）
- 看似「只有一個快速修復」時
- 已經試過多次修復仍無效時
- 上次修復沒有解決問題時

## 四階段除錯流程

### 階段一：根因調查（必做，未完成不得進入修復）

1. **完整閱讀錯誤訊息**：不跳過任何錯誤或警告；完整讀 stack trace；記下行號、路徑、錯誤碼。
2. **穩定重現**：寫下確切觸發步驟；確認可重複觸發；找出最簡重現方式。
3. **檢查環境與狀態**：
   - LINE Bot：`curl .../health` 確認 `auto_reply`、`ai_shadow` 狀態；檢查 D1 是否有暫時性錯誤（曾於 2026-08-13 因 D1 暫錯導致老闆被洗版）。
   - GitHub Pages：檢查 Actions 是否出現「pages build and deployment」——若出現代表 CI 門禁失效（來源被改回 branch 模式）。
4. **查看近期變更**：`git log --oneline -20`、比對最近 deploy 的 commit；檢查 migration 順序（D1 migration 未套用時存檔會有明確警告，不要忽略）。
5. **隔離變因**：區分是程式碼、資料、第三方服務（LINE API、Cloudflare、OpenAI/Claude）或時序問題（Cron UTC vs 台北時區）。

### 階段二：建立假設與驗證計畫

- 每個假設對應一個可證偽的測試。
- 從最便宜、最有可能的假設開始驗證。
- 記錄每個被排除的假設與證據，避免反覆繞路。

### 階段三：最小化修復

- 修復只動根因，不順便改其他東西。
- 每個修復附測試（先寫失敗的測試，修完變綠）。
- 正式環境變更前：先用唯讀查詢確認影響範圍（`SELECT COUNT(*)`、`SELECT * LIMIT 10`），絕不憑文件舊數字判斷。
- D1 不可逆操作（批次狀態修改、刪除、migration）必須先確認影響範圍並取得授權。

### 階段四：完工驗證（防假綠）

> CI 綠色 ≠ 問題解決。綠燈只證明「寫的測試通過」，不代表行為正確。

- 實際觸發一次完整流程（例如：LINE 傳測試訊息、點擊轉換按鈕、模擬 webhook 簽章）。
- 檢查 side effect：通知是否重複、push 是否正確、時間是否正確（UTC/台北時區）。
- 對正式環境：確認 health endpoint 狀態符合預期後才宣布完成。

## 防假綠（Anti-False-Green）檢查表

| 變更類型 | 必要驗證 |
|---|---|
| 程式碼修正 | `node --check` + `npm test` 全綠 + 實際觸發一次完整流程 |
| webhook / 簽章 / CSP / 第三方資源 | 實際發一次請求，確認行為與事件都送出 |
| D1 migration | 遠端 `d1 migrations apply --remote` 前先 dry-run；確認舊 migration 順序不被破壞 |
| GitHub Pages 部署 | Actions 頁只出現「Validate and deploy」；檢查 noindex/CSP 組合未被改動 |
| 文字/文案修改 | 檢查 UTF-8 無 BOM（曾發生 AI 存檔導致中文變亂碼） |
| 斷言/測試規則修改 | 確認新規則沒有掩蓋舊問題（例如取樣範圍規則曾暴露三個隱藏問題） |

## Campcool 正式環境特殊保護

- **campcool-bot**：D1 有正式訂單與訊息，任何 migration、刪除、狀態批次修改或部署都要先確認影響範圍。回滾用 commit hash（如 `42ca529`），不用 tag（曾因權限沒推上去）。
- **leakdoctor-bot**：正式部署僅限 main 的 `deploy.yml`；PR 品質門禁走 `pr-check.yml`（私有倉庫無 branch protection）。
- **campcool / leakdoctor / 0988145875**：Pages 來源必須是 GitHub Actions；`deploy.yml` 未通過時線上維持前一正常版本。退版用 `git revert <commit> && git push`。
- **TITAN-STAR**：三個頁面帶 noindex 止血；斷言取樣範圍必須印出來。

## 參考文件

- `references/obra-systematic-debugging.md`：obra/superpowers ⭐274k 原版系統性除錯流程全文
- `references/verification-before-completion.md`：完工前驗證流程（obra ⭐274k）
- `references/campcool-ops-context.md`：Campcool 專案群環境現況快照（health check、Cron、release tag）
