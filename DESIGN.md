# CampCool 網站設計基準

更新：2026-10-05。依業主「從 Campcool 開始整體改版」指示實作。

## 品牌與租借動線

採暖白、森林綠、自然影像與清楚的裝備資訊；首頁以「選設備 → 看租金 →
選取還點 → LINE 確認檔期」安排內容。第一屏說明服務、起租價與押金，
提供詢問檔期及第一次租借流程兩個入口。機型按鈕直接帶入預約表單。
首頁好評先呈現兩則，其餘三則以原生 details 展開；桌面兩欄、手機單欄，
原圖可開啟放大，也提供完整好評頁入口，避免大幅加寬後的截圖拉長整頁。

產品圖與山林圖沿用 repo 資產；山林圖是情境示意，alt 明示示意，不描述為
實際顧客案例。產品事實以 services.md、pricing.md、areas.md、faq.md 為基準。
不增加價格、據點、評論數或冷房效果承諾，JUZ 的免排水不能套用到 SAC。

## 視覺與響應式

正式共享樣式：assets/site-redesign.css，載入於 15 個公開內容頁。
其他三個 areas/ 別名頁保留跳轉與 canonical。

| Token | 值 | 用途 |
|---|---|---|
| paper | #f7f5ef | 頁面底色 |
| white | #fffefa | 卡片與圖說 |
| ink | #22382f | 主要文字 |
| muted | #5b6b62 | 說明文字 |
| green | #244b3b | 品牌、按鈕與導覽 |
| sage | #e7ece3 | 提示與選取狀態 |
| line | #dce2d7 | 分隔與邊框 |
| accent | #8b6035 | 小標 |

html 固定 20px；首頁桌面內容上限 1160px、文章 960px，640px 以下英雄區
與機型卡採單欄。1024px 起用頂部四頁籤導覽；較窄螢幕用底部導覽，共用
setTab、aria-current、網址 hash 與儲存偏好。獨立頁手機保留第二列導覽。

主要按鈕至少 44px、底部按鈕至少 64px、導覽標籤 14.4px；所有頁面提供
跳到主要內容與可見鍵盤焦點。不增加字型服務、框架或建置工具。
CTA 閃光停用，prefers-reduced-motion 下關閉動畫與平滑捲動。

## 功能、個資與驗證

預約仍只在使用者裝置整理與複製 LINE 訊息，未新增公開表單 API。
使用者在 LINE 確認並送出後店家才會收到資料。延用日期驗證、選機／
方案帶入、16 項小物、計算器、營區／帳篷 API、追蹤 ID 與 CSP。
獨立頁 header 的 LINE 連結延用 logLineClick('site_header', true)，
首頁導覽至表單不計為實際開啟 LINE 的轉換。

既有 validator、反例自測、核心 E2E 必須通過。新增 redesign-e2e.py 用本機
HTTP 站測 360／390／768／1440px 共 76 個頁面／頁籤尺寸組合，
檢查溢位、共享樣式、圖片、真實導覽與鍵盤、機型／方案與小物帶入、
日期必填、訊息整理不發外部請求、個資不進追蹤及新 header 轉換事件與 CSP。
測試攔截外部請求，不向正式 LINE 或分析服務送測試資料。

CI 的 campcool-redesign-browser-evidence artifact 提供手機／桌面截圖、
measurements.json、failures.json；保留 14 天，必要時重跑 workflow。
工作環境無法啟動時，完整內容與瀏覽器測試以此次 GitHub CI 結果為準。
內部 Markdown、腳本與測試產物不在正式網站公開產物內。
