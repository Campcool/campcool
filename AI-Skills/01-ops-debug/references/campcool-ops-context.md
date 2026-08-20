# Campcool 專案群環境現況快照（2026-08-14 後）

## campcool-bot（LINE Bot，正式營運中）
- Git：main / `0bbe46d`；正式 release tag `release-restock-resend-queue-20260718`
- 回復點：commit hash `42ca529`（tag 因權限沒推上去，用 hash）
- health：`auto_reply=keyword ai_shadow=off`；D1 暫錯時限流重試 3 次、失敗放行
- Cron（UTC）：`*/15` 候補/付款到期；UTC 01:00 台北 09:00 每日提醒；UTC 18:00 messages 保留期清理
- 單張訂單可多台機型；JUZ 依取件點推薦（內湖/竹北/新竹優先 JUZ，台中西屯優先山水）
- 測試：`node --check` + `npm test` 117/117（含 webhook 簽章 8 項）
- 部署：Cloudflare Worker + D1 + KV，wrangler 4.118.0

## leakdoctor-bot（灰汰郎，派工系統）
- 部署僅限 main 的 `deploy.yml`（需 production secrets）；PR 品質門禁 `pr-check.yml`
- 測試：`npm test` 268 passed（34 檔）；typecheck 綠
- Cron（UTC）：0 1 台北09:00 今日提醒＋清錯誤｜0 * 每小時逾時｜0 10 台北18:00 D-1＋完工詢問｜0 13 台北21:00 日報
- 話術依 `docs/CONVERSATION-PLAYBOOK.md`；Config keys：`google_review_url`、`ai_paused` 等

## campcool / leakdoctor / 0988145875（GitHub Pages 靜態站）
- Pages 來源必須是 GitHub Actions；`deploy.yml` 未過時線上維持前一版本
- Actions 頁出現「pages build and deployment」＝ 門禁失效（來源被改回 branch 模式）
- 退版：`git revert <commit> && git push origin main`
- TITAN-STAR：三頁面 noindex 止血；斷言取樣範圍必須印出來

## 通用禁令
- 中文檔案 UTF-8 無 BOM
- D1 不可逆操作前唯讀查影響範圍；不憑文件舊數字判斷
- CI 綠燈 ≠ 行為正確，需實際觸發驗證（防假綠）
