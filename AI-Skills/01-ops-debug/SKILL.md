---
name: campcool-ops-debug
description: 調查 Campcool 專案群的網站、LINE Bot、Worker、資料與部署異常；以目前版本、重現證據、最小修復及實際流程驗證排除問題。既有參考是基準，技術與流程可依最新官方資訊更新。
---

# Campcool 維運與除錯

## 基準與更新原則

現有程式碼、交接文件與本技能參考快照是理解現況的基準，不是永久技術標準。技術選型、版本、測試方法與過去的流程假設應依目前任務、最新官方證據及實際相容性重新評估；不要只因舊文件寫過，就阻止已授權的改進。

區分技術建議、目前實作與營運事實。價格、服務區、客戶紀錄、園所資訊等用可核對來源，不能因技術更新自行編造。

涉及版本或架構調整時，先讀 [技術查核與版本更新流程](../TECHNOLOGY-REVIEW.md)。其中版本表是 2026-10-03 的查核快照，執行時重新核對，不作永遠的最低版本。

## 調查流程

1. 記錄倉庫、分支、commit、部署版本、時間、錯誤與觸發步驟。分清本機、測試環境、正式站與外部 API。
2. 重現並檢查近期程式、資料、設定與第三方服務變更。每個假設配一個可證偽的檢查；不能重現時明確列出缺的證據。
3. 用證據支撐修復，優先改根因。緊急事件可採用可回退的緩解措施，說明它處理的症狀與尚未確認的根因。
4. 依變更風險選驗證：複雜邏輯或缺陷修復用能抓到原缺陷的回歸測試；純文件或低風險調整用直接查核。不要為可逆的小改動一律添加鏡像測試。
5. 驗證要區分「檢查執行了」「檢查通過」「實際流程有效」。環境缺相依或無 API 權限屬驗證缺口，不直接判成產品失敗。

## 部署與外部服務

- 讀各倉庫真實 workflow 的觸發、permissions、needs、建置／測試／upload／deploy 依賴鏈，不能假設所有站都叫 deploy.yml。
- Pages 門禁確認 build_type=workflow，檢查欲部署的實際產物。workflow 顯示名稱只能作線索，不能用「只出現某個名稱」判斷來源或健康。
- 用 Pages 來源自檢或有權限的唯讀 API 查設定；API 權限不足明確記錄。排程成功不等於 DNS、TLS、HTTP、真機與接單都正常。
- Bot／Worker 檢查可用 health、logs、對應 API、webhook 簽章及時區；先唯讀確認影響範圍，沿用目前任務的授權。
- 發訊息、建立訂單與派工會產生實際 side effect。用隔離測試與授權範圍驗證；單純盤點不代送正式訊息。
- 逾時不保證後端未寫入。分清「未建立」「無法確認」「已建立」；核對重試 idempotency、同線索事件去重及使用者返回後的狀態。
- 回退依目前遠端 head、正確部署版本及資料相容性安排，使用可審閱的 revert；不要套用文件裡某個歷史 commit 或盲目 force push。

## 驗證對應

| 變更 | 驗證 |
|---|---|
| JS／TS／React 行為 | 實際專案語法／型別／建置工具與相關流程；node --check 不能代替 JSX／TS 編譯 |
| 聯絡、表單、試算 | 完整主流程、剪貼簿失敗備援、開 LINE／返回、防重；有 webview 時補真機 |
| CSP、第三方腳本、公開查詢 | 真實請求與回應、console／網路錯誤、必要事件接收；static regex 不足以驗 API |
| Pages 部署 | 正確來源、同 commit 的門禁與產物、公開白名單、正式入口 |
| 測試規則 | 範圍與分母、代表性反例；反例驗的是實際要發布的內容 |
| 文件 | 連結存在、狀態與來源對得上；文字編碼和二進位格式用各自檢查 |

## 專案差異

- campcool 與潔美淨的詢價表單主要在本機整理 LINE 訊息；整理或開 LINE 不代表商家收件。
- 灰汰郎前台會呼叫外部 leads API；成功回 leadId 與下游廠商收件要分開驗證。
- 潔淨坊是 React／Vite 多入口；華兒園正式產物是 Next 靜態 out，不能只驗 vinext 預覽。
- TITAN-STAR 的線上與離線產物、CLI 與瀏覽器匯入都要對齊；noindex 不是存取控制。

## 參考快照

只在相關時讀取；相對路徑以下列實際檔名為準。舊原文不是最新 API 保證，套用前核對版本與執行環境。

- [anthropics_skills__webapp-testing.md](references/anthropics_skills__webapp-testing.md)
- [campcool-ops-context.md](references/campcool-ops-context.md)
- [obra_superpowers__systematic-debugging.md](references/obra_superpowers__systematic-debugging.md)
- [obra_superpowers__test-driven-development.md](references/obra_superpowers__test-driven-development.md)
- [obra_superpowers__verification-before-completion.md](references/obra_superpowers__verification-before-completion.md)
