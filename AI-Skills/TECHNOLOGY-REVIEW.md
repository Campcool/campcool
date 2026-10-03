# 技術查核與技能更新流程

查核日期：2026-10-03（Asia/Taipei）。本文件的版本是當日官方發行快照，執行任務時重新查核。新版本可改善安全、效能、相容性與維護成本，但「最新」不自動等於適合每個專案。

## 更新原則

- 程式碼、AI-README、歷史 skill、既有檢查項目作為理解現況的基準。技術與流程依目前使用者指示、最新官方證據與可驗證效益演進。
- 不把歷史版本、固定 workflow 名稱、星數、僵化 TDD／審批流程或當時架構當作永久標準。官方範例也需符合本專案的正式產物與環境。
- 營運事實以目前可查證來源確認；工具升級不能替代價格、服務、照片授權、訂單狀態與資料欄位核對。
- 舊參考全文保留為歷史基準。更新使用到的指引時核對上游版本、來源與授權；上游提及的 scripts 不一定存在於此倉庫，不宣稱未打包工具為內建。
- 本次是人工查核與 skill 更新，不建立定時任務，不宣稱會自動更新依賴或監測版本。

## 每次查核的順序

1. **確認現況**：同時讀取可獨立取得的倉庫資料，記錄 full_name、分支、head SHA、package.json、lockfile、正式入口與部署產物。多倉庫 SHA 不代表同一交易時間，報告列明各自快照。
2. **確認來源**：以官方 release、支援／LTS 時程、安全公告、版本化 package metadata 與 migration guide 為主。GitHub latest 須核對發布日與 prerelease；latest 不一定是最大版本，也不代表沒有安全問題。
3. **處理更名**：讀回傳的 canonical repository，必要時跟隨官方重新導向。這次 React 原 facebook/react 已導向 react/react，不能把舊 URL 的移轉誤判成專案不存在。
4. **區分版本層**：專案 Node、Action 自身 runtime、Worker compatibility_date、套件版本與瀏覽器版本各自列出。不要因 actions/setup-node 使用 node24，就宣稱專案建置已升成 Node 24。
5. **確認相容性**：Node engines、peer dependencies、套件管理器／lockfile、插件、建置工具、原生模組、托管方式、靜態匯出與離線能力。
6. **形成最小變更**：寫明升級原因、現行／候選版本、官方來源、預期效益、必要驗證與可回退方法。一般先評估同支線修補，主要版本遷移另列，不同時無理由更換全部工具。
7. **驗證與收尾**：按正式產物做安裝／建置／型別／相關流程與必要安全檢查；技能文件查相對連結、格式與事實。環境或權限缺口單獨記錄，不把未跑測試寫成通過。

## 官方版本快照

| 技術 | 2026-10-03 查到的官方版本 | 對目前專案的判斷 |
|---|---|---|
| Node.js | 24.21.0；22.23.3；26.10.0 | v24 為 Active LTS、v22 為 Maintenance LTS；v26 當日仍是 Current，官方預定 10/28 才進 LTS。新 CI／專案先評估受支援 LTS；現有 Node 22 不因不是最新而列停站問題 |
| React | 19.3.0 | 對潔淨坊 React 19.1 與華兒園 19.2.6 評估 React／ReactDOM、型別與框架相容性；不要求原生靜態站改 React |
| Vite | 8.3.2 | 官方 package engines 為 ^20.19.0 或 >=22.12.0；仍需先選受支援 Node。潔淨坊 6.3→8 屬主要版本遷移，檢查 Rolldown／插件、多入口、base 與產物，不能只改版本號 |
| Next.js | 16.3.8 | 華兒園目前 16.2.6；需檢查 React peers、靜態 export、型別、out 測試與 vinext 預覽相容性，不把 Next 伺服器功能直接套到 Pages |
| Playwright | 1.63.0 | 測試套件與瀏覽器安裝配同版本；避免無版本約束安裝造成測試漂移；補相關核心流程，不以截圖取代接單 |
| pnpm | 12.8.1 | 現有部分倉庫 packageManager 固定 10.4.1；主要版本與 lockfile 需隔離驗證。先按目前凍結鎖檔重現，不直接改成 latest |
| actions/checkout | 7.0.1 | 已讀該 tag 的 action.yml，runs.using=node24 |
| actions/setup-node | 7.0.0 | 已讀 action.yml，Action runtime=node24；node-version 輸入另決定專案版本 |
| actions/configure-pages | 6.0.0 | 已讀 action.yml，runs.using=node24 |
| actions/upload-pages-artifact | 5.0.0 | composite action，內含固定 SHA 的 upload-artifact v7；不能稱本身是 Node action |
| actions/deploy-pages | 5.0.1 | 已讀 action.yml，runs.using=node24；既有 v5 是否更新依實際解析與相容性確認 |

Node v24 預定 2026-10-20 進 Maintenance、支援至 2028-04-30；v22 支援至 2027-04-30。這些日期依官方當次 schedule，後續以重新查核為準。

查核官方發行紀錄不等於做完 dependency audit 或 CVE 適用性評估。本次未確認特定專案有新漏洞，也沒有實際升級網站、Actions 或 Bot 相依。

## 專案產物與最小驗證

| 專案 | 基準產物／行為 | 技術更新時驗證 |
|---|---|---|
| campcool | 原生多頁 HTML；根目錄 JSX 僅舊參考；Bot 提供公開查詢與設定 | 靜態內容、hash、產品／價目一致、LINE 與 API 降級、Ads／CSP |
| 灰汰郎 | 原生多頁 HTML；leads API 與 Bot | leadId、重試／去重、六服務價目與 availability、LINE／webview、下游事件 |
| 潔淨坊 | React／Vite 多 HTML 入口、dist | lint/build、首頁／案例／工具入口、assets/base、篩選、聯絡及預渲染方案 |
| 潔美淨 | 原生 HTML、費用試算與本機 LINE 整理 | 試算／預填／私有 query 清除、剪貼簿備援、事件口徑 |
| 華兒園 | STATIC_EXPORT=1 的 Next out；vinext 僅預覽 | 正式 out 測試、參觀表單、照片公開範圍、字型子集、預覽相容性 |
| TITAN-STAR | 線上資產＋離線 HTML；月報來源與兩條匯入 | parser、資料口徑、CLI／瀏覽器 manifest、離線 vendor 與 bundle 可重現 |

讀不到的倉庫不能當作已盤點。GitHub 404 可能是無權限、改名、移除或不存在；先核對完整名稱與連線範圍，不能直接宣稱只有公開清單上的專案存在。

## Skill 與參考快照的維護

- 此目錄四套 SKILL.md 是任務路由與本地使用方法；41 份既有 reference 是先前收錄的原文快照，不宣稱已全部同步上游最新版。
- 本次已修正路由對這 41 份檔案的實際相對連結；新用到的技術 API 優先查版本化官方文件。
- 每次更新技能寫明日期、舊假設、新證據、適用範圍、已驗及未驗。保留有用來源與授權，不以星數門檻決定是否採用。
- 安全、版本與技術建議可重評；檢查仍須針對此次真正要做的事，不憑空新增核准或部署步驟。

## 本次官方來源

- [Node 官方 release 清單](https://github.com/nodejs/node/releases)；[24.21.0](https://github.com/nodejs/node/releases/tag/v24.21.0)、[22.23.3](https://github.com/nodejs/node/releases/tag/v22.23.3)、[26.10.0](https://github.com/nodejs/node/releases/tag/v26.10.0)
- [Node 支援時程](https://github.com/nodejs/Release/blob/main/schedule.json)
- [React 19.3.0](https://github.com/react/react/releases/tag/v19.3.0)；[版本 package metadata](https://github.com/react/react/blob/v19.3.0/packages/react/package.json)
- [Vite 8.3.2](https://github.com/vitejs/vite/releases/tag/v8.3.2)；[engines 與建置相依](https://github.com/vitejs/vite/blob/v8.3.2/packages/vite/package.json)
- [Next 16.3.8](https://github.com/vercel/next.js/releases/tag/v16.3.8)；[版本 package metadata](https://github.com/vercel/next.js/blob/v16.3.8/packages/next/package.json)
- [Playwright 1.63.0](https://github.com/microsoft/playwright/releases/tag/v1.63.0)；[pnpm 12.8.1](https://github.com/pnpm/pnpm/releases/tag/v12.8.1)
- [checkout v7.0.1 action.yml](https://github.com/actions/checkout/blob/v7.0.1/action.yml)
- [setup-node v7.0.0 action.yml](https://github.com/actions/setup-node/blob/v7.0.0/action.yml)
- [configure-pages v6.0.0 action.yml](https://github.com/actions/configure-pages/blob/v6.0.0/action.yml)
- [upload-pages-artifact v5.0.0 action.yml](https://github.com/actions/upload-pages-artifact/blob/v5.0.0/action.yml)
- [deploy-pages v5.0.1 action.yml](https://github.com/actions/deploy-pages/blob/v5.0.1/action.yml)

上游技能倉庫目前 main（查核身份與最近變更，非聲稱已匯入全部新版）：
[anthropics/skills@8a1541c](https://github.com/anthropics/skills/commit/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4)、
[obra/superpowers@8ca22db](https://github.com/obra/superpowers/commit/8ca22dba9a94f28898bbce59f2537ff4d87c747d)、
[vercel-labs/agent-skills@063bee9](https://github.com/vercel-labs/agent-skills/commit/063bee94c3f4df8453406c830b0a7df0f2860278)。
