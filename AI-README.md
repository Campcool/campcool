# Campcool AI 維護指南

這份文件提供 AI 開發代理與後續維護者目前有效的產品事實、改版決策及防回歸規則。一般專案說明與本機預覽方式請見 [`README.md`](README.md)；公開的服務、價格與地區資料分別以 [`services.md`](services.md)、[`pricing.md`](pricing.md)、[`areas.md`](areas.md) 及 [`faq.md`](faq.md) 為準。

最後更新：2026-08-16

## 專案與執行來源

- 正式網站是 GitHub Pages 上的靜態網站，網域為 `campcool.tw`。
- `index.html` 是正式首頁，包含主要 HTML、CSS 與原生 JavaScript，沒有建置步驟或執行期框架。
- `*.jsx` 是早期元件參考，不會載入正式網站。修改正式介面時，必須先改實際使用中的 HTML。
- `scripts/validate-site.mjs` 是網站內容、內嵌腳本、JSON-LD、canonical、sitemap 與重要產品規則的防回歸檢查。

## 多方協作規則（Claude／Codex／Manus 一體適用）

本專案同時有多個 AI 代理維護。以下規則**不是針對任何一方**，是三方共同的
防護欄，來自兩次實際教訓：

- **campcool-bot 資料消失**：兩個代理各自從本機副本推送，約 7,000 行的版本
  被約 3,000 行的版本整個覆蓋。
- **CSP 擋掉 Ads 轉換**（本 repo，2026-08-16）：變更直推 main 並部署，
  在自身驗證全綠的狀態下讓 Google Ads 轉換回傳全部失敗，事後複驗才發現。
  若當時正在投放，該期間的轉換數據已無法追回。

### 規則一：不直推 main

一律開分支，由**另一方複驗後**才合併。這是三條規則裡最重要的一條——
上述兩次事故若有複驗都不會發生。

### 規則二：四類變更必須做行為驗證，不能只跑 validate

| 變更類型 | 必要驗證 |
|---|---|
| CSP、第三方資源、beacon／fetch 目標 | 瀏覽器監聽 `securitypolicyviolation`，實際觸發一次轉換 |
| 索引指令（noindex／canonical／hreflang／robots） | 確認組合非官方反模式，並檢查 canonical 目標不受牽連 |
| 轉換追蹤（gtag／logLineClick／conversion label） | 實際點擊出口，確認事件與 conversion 都送出 |
| 價格、品項、押金、規格 | `index.html`／`pricing.md`／`llms.txt` 三處同步，並跑 validate 第 12 條 |

理由：這四類的錯誤**看原始碼與跑靜態驗證都看不出來**，但會直接影響金流或索引。

### 規則三：開工前先 `git pull` main

最便宜的防覆蓋手段。若本機副本已落後多個提交，先同步再改，
不要在舊基礎上大幅改寫後整檔覆蓋。

### 分工建議（按檢查類型，而非按檔案）

`index.html` 已逾 3,000 行且各方都需修改，按檔案切割不可行。建議按性質分工：

| 代理 | 適合負責 |
|---|---|
| Manus | 系統性掃描、工具鏈、CI、無障礙與效能的地毯式清理 |
| Codex | 產品與 UX 演進、版面改造 |
| Claude | 商業事實一致性、行為驗證、跨方交叉複驗 |

### 合併前檢查清單

```bash
git pull origin main                      # 規則三
node scripts/validate-site.mjs            # 20 項斷言
node scripts/validate-site.mjs --selftest # 確認驗證非假綠
# 若屬規則二的四類變更，另加瀏覽器實測
```

## 2026-07-30 改版基準

### 預約資料與 LINE 流程

官網預約表單只在訪客的瀏覽器內整理並複製訊息，不會在開啟 LINE 前把姓名、手機、日期或租借需求傳送到 Campcool Worker／D1。

```mermaid
flowchart LR
    A["訪客填寫預約欄位"] --> B["瀏覽器本機整理與複製訊息"]
    B --> C["訪客點擊開啟 LINE"]
    C --> D["LINE 顯示預填訊息"]
    D --> E["訪客確認並送出"]
    E --> F["LINE Bot／Worker 接收實際訊息"]
```

維護規則：

- 不得重新加入預約表單對 `/public/booking-leads` 的預先 POST。
- 不得在 LINE 送出前把 `renter_contact`、`ga_client_id` 或其他聯絡資料寫入 Worker／D1。
- `booking_form_view` 與 `booking_message_composed` 只用於一般漏斗分析，不算 LINE 聯絡轉換。
- 只有實際開啟 LINE 的動作才記錄 GA4 `line_click`，並在設定 `ADS_CONVERSION_LABEL` 時送出 Google Ads conversion。
- LINE 預填訊息保留 `[來源:booking_form]` 標記，供 LINE Bot 在收到實際訊息後識別來源。
- 頁面必須明確告知訪客：內容只在此裝置整理，Campcool 尚未收到資料，需在 LINE 內確認並自行送出。

### LINE CTA 動效

- 主要 LINE CTA 使用 `cc-line-shimmer`，每 3 秒短暫流光一次。
- 流光只使用 transform 與 opacity，不攔截點擊。
- 必須保留 `@media (prefers-reduced-motion: reduce)`，讓偏好減少動態效果的訪客停用動畫。
- 預約結果中的「開啟 LINE 確認並送出」放在長訊息預覽之前，確保手機版立即看得到下一步。

### 取件政策

所有取件點都採預約制。不得宣稱 `24H 取還`、`24H 自取`、`社區寄櫃`、提供取件碼或可隨時自取。

目前有效說法：

- 竹北仍可使用「竹北社區取件」，但必須先透過 LINE 約定時間與交付方式。
- 公道五路、內湖、士林、五股與台中西屯同樣採預約取還。
- 未預約請勿直接前往。
- 目前不提供宅配、郵寄或直接送到營區。

涉及取件政策的主要檔案：

- `index.html`
- `hsinchu.html`
- `taipei.html`
- `taichung.html`
- `emergency-ac.html`
- `faq.html`
- `how-it-works.html`
- `reviews.html`
- `areas/*.html`
- `areas.md`、`faq.md`、`services.md`

### 社群分享定位

首頁的 OG 與 Twitter 預覽採「露營冷氣知識／選購指南」定位，讓 Campcool 能以知識型內容在 Facebook、Instagram 與社群分享。這是既定行銷策略，不應改成直接促銷型標題或廣告式封面，除非產品負責人明確要求。

保留重點：

- 知識型 OG title、description 與 `assets/og-cover.jpg`
- BTU、用電與機型比較的內容入口
- 分享預覽與站內租借轉換可以有不同角色

## 2026-08-16 改版基準

### 機型適用尺寸（唯一權威，不得再出現第二套）

**分界：3×3（300×300cm ＝ 9 ㎡ ≈ 2.72 坪）**

- 3×3 及以下 → 艾比酷 JUZ-400（5100 BTU）
- 超過 3×3 → 山水 SAC688（6300 BTU）
- 睡 5 人以上一律 SAC688

改版前站上有四套互斥規則，同一頂 300×300 帳在兩支計算機會得到相反答案。
維護規則：

- 兩支計算機門檻**必須一起改**，否則矛盾會重現：
  - `calcRecommend()`：單位為坪，`area > 2.75`
  - `onTentModelChange()`：單位為平方公尺，`area > 9`
- 不得再使用「4×4 以上」的說法（會讓 3×3～4×4 之間變成空窗），
  也不得使用「3-5 坪 / 5-8 坪」的舊標示。
- 文案分散於 index.html（規格卡、Product JSON-LD、MODEL_SPEC、SEO 入口）、
  faq.html、faq.md、btu-guide.html、juz-400.html、sac-688.html、
  camping-ac-rental.html、areas/taipei.html、services.md、pricing.md、llms.txt。

### 用電數字

- 露營常見電器加總為 **4.8A**（冷氣 3.9 + 冰箱 0.4 + 燈 0.2 + 手機 0.3）。
  加租製冰機（約 100W ≈ 0.9A）後約 **5.7A**。
- 改版前有 5 處寫 5.3A，與站上自列分項相加不符，讀者可當場推翻，已全部修正。
- **注意區辨**：SAC688 自身耗電 530W ÷ 110V 也是 4.8A，出現在
  index.html 規格卡、MODEL_SPEC、btu-guide 比較表，與上述加總無關，不可混改。

### 價格與押金揭露

- 冷氣押金 **$3,000／台**，必須顯示在首頁價目表，不能只寫在 faq。
- 其它小物**僅「電吉拉 mini 行動電站」收押金 $1,000**，其餘不收；
  頁面須明講「其餘品項不收押金」，否則客戶會以為每項都要壓錢。
- 小物**可單獨租借**，不必一併租冷氣。
- 動力延長線已可加購（5M $100／10M $150），不得再寫「需自備」。

### 轉換追蹤（影響 Google Ads 成效）

- **每個有 LINE 出口的頁面都必須載入 gtag.js 與 logLineClick helper**。
  改版前只有首頁與 emergency-ac 有，其餘 16 頁對 Ads 回報零轉換。
- 新增任何 `lin.ee` 連結時，必須加
  `onclick="logLineClick('<頁面>_<位置>', true)"`。
- 不得使用 `if(window.gtag)gtag(...)` 這種寫法——該頁若未載入 gtag 就是死碼。
- 只有真正開啟 LINE 的動作才傳 `convert=true`；站內導覽只記 GA4 事件。

### 圖片

- 頁內 `<img>` 一律使用 webp（`logo-88` / `sac688_product` / `og-cover` /
  `addon-*`）。
- **`og:image`、`twitter:image` 與所有 JSON-LD 的 `logo`／`image` 欄位一律維持
  `.jpg`**，社群平台與搜尋引擎對 webp 支援不一；原始 jpg 檔案不得刪除。
- 圖片必須帶 `width`／`height`，且數值要與實際檔案相符（改版前有兩張不符造成
  版面位移）。

### 結構化資料

- **首頁不得再加入 FAQPage**：頁面上沒有對應可見內容，違反 Google 政策。
  FAQ 結構化資料集中在 faq.html。
- 兩台冷氣的 Product 以 `@id` 與機型頁合併，`offers.url` 指向各自機型頁。
- reviews.html 的 Organization 以 `@id` 指向首頁 LocalBusiness。
- LocalBusiness 的 `address` 為 **竹北市／新竹／TW**，與 geo 座標一致。
- 評分 4.95／160 則來源為 **LINE 官方帳號累積回饋，非 Google 商家評論**，
  reviews.html 必須保留來源揭露文字。
- `areas/taipei.html`、`areas/hsinchu.html`、`areas/taichung.html` 是
  meta-refresh 轉址殘頁，**任何連結與 JSON-LD 都不得指向它們**；
  `areas/new-taipei.html` 才是新北的正規頁。

### 其它小物分頁

- 分頁 `data-tab` 維持 `fridge`（保住既有 `#fridge` 深連結與 localStorage），
  顯示名稱為「其它小物」。
- 15 個品項分 6 個 `<details>` 分類抽屜，卡片為 `<label>` + 隱藏 checkbox。
- 勾選流程：`addonsUpdate()` 更新小計 → `addonsToForm()` 寫入
  `#bkNote` 並跳至預約表單，客戶於 LINE 送出。
- **新增或改價品項時，index.html 與 `pricing.md` 必須同步。**

### 無障礙與行動裝置（防回歸）

- 公告輪播**不得**加回 `aria-live`（每 4 秒打斷螢幕閱讀器），
  且必須保留「暫停輪播」按鈕。
- 選購指南子頁籤 sticky 為 `top:69px`（低於 header 65px 會被蓋住）；
  `html` 需保留 `scroll-padding-top:72px`。
- `body` 底部留白須含 `env(safe-area-inset-bottom)`。
- `prefers-reduced-motion` 的 media block **必須放在樣式表最後**，
  否則會被後面的動畫宣告覆蓋（已實測）。
- 資訊性灰字使用 `#6b7280`，不得改回對比不足的 `#9ca3af`。
- 取機日期須設 `min` 並在 `submitBooking()` 內再次把關（min 不約束 JS 送出）。

## 2026-08-16 Manus 滿分制第二輪優化

此輪由 Manus 以 100 分滿分制（五維度加權：功能完成度/穩定與安全 25%、可維護與交接 20%、使用者體驗 15%、成本效益 15%）接手 Claude 完成的 20 commits，執行十角色辯證後的修改。辯證裁決（不可逆）：不抽離 inline CSS/JS（保住零建置）、不做 PWA manifest（非 Web App）、保留 areas 殘頁+補 noindex（歷史連結不中斷）、不動 Claude 已定的產品事實（機型分界/押金/取件政策/LINE 流程）。

### 已完成的修改

| 項目 | 說明 |
|---|---|
| 死重圖片刪除 | `git rm assets/homepage_hero.png`（1.5MB）與 `taiwan_map.png`（912KB）；防回歸斷言已加（引用+git index 雙檢查） |
| 評論圖 webp 化 | reviews.html + index.html 的 review-01~05 webp 化，節省約 1.1MB；og/JSON-LD 層 jpg 依既有政策保留 |
| areas 殘頁 | taipei/hsinchu/taichung 補 `noindex`（meta-refresh 轉址頁不參與索引，validate 逐頁檢查） |
| GA4 fetch | index.html 的 config fetch 加 3 秒 AbortController 逾時（IIFE 閉包）；**注意：正式 GA4 ID 尚未掛上**，Worker 目前回傳 `{"ga4_measurement_id":""}`，架構正確、優雅降級，等老闆提供 ID |
| llms.txt | 更新至 2026-08-16：加 15 品項小物清單（價格以頁面 data-price 實測為準）與機型分界規則；validate 檢查新鮮度 ≤ 60 天且價格表覆蓋 ≥ 15 品項 |
| 防回歸驗證 | `scripts/validate-site.mjs` 從 6 項擴充至 20 項斷言（見下）並加 `--selftest` 防假綠模式 |
| CI 門禁 | `.github/workflows/site-check.yml`：push/PR 觸發，先跑 selftest 再跑完整 validate，外加 Worker config endpoint 探針 |

### validate-site.mjs 新增斷言（配合既有 6 項）

死重圖引用消失、每頁 LINE CTA 閉環（areas 殘頁除外）、兩支計算機門檻一致（`area > 2.75` 坪 / `area > 9` ㎡ / `area > 16` 坪拒租）、16 品項逐項存在（非僅計數——單品項改名計數不變，實測抓到漏洞）、config endpoint 版號統一且 14 頁覆蓋、areas 殘頁 noindex、評論 img src 僅限 1 張 jpg（產品實照）、llms.txt 新鮮度、git index 不含死重圖。

防假綠用法：`node scripts/validate-site.mjs --selftest` 會故意破壞 4 類產品事實（必留文案/禁入標記/計算機門檻/小物品項），確認 validate 全部抓住後還原，任何一步不符預期 selftest 本身 exit 1。CI 先跑 selftest 再跑完整 validate，杜絕「驗證腳本本身失效」的假綠。

## 嚴謹級衝刺（2026-08-16，Manus）

目標：Lighthouse 效能 ≥90（CDN 冷快取/server-response-time 不可修，以能控層面最大化）、WCAG 2.1 AA 0 serious violations（16 頁 axe 全清）、安全標頭、跨瀏覽器（webkit）驗證、自動化 E2E + CI 門禁。

### 結果摘要

| 維度 | 基準 | 嚴謹級後 |
|---|---|---|
| Lighthouse SEO / Best Practices | 大多 100 / 100 | 100 / 100（全部頁面） |
| Lighthouse 效能 | index 61 最差、pricing 55 | 效能主扣分為 server-response-time（CDN 冷快取，無法修）與 GA4 第三方 JS；可控層面已優化：GA4 延遲 2.5s/首次互動載入、reviews 首圖 fetchpriority=high |
| axe WCAG 2.1 AA（16 頁） | color-contrast 44→殘 5、region 147→殘 2 | **全部清零**（第九輪殘留已由 a690f10 修完：btu-guide thead/回首頁連結、reviews .summary 移入 main） |
| 跨瀏覽器 | — | webkit（Safari 引擎）headless 驗：tab 切換/小物勾選/無 overflow/h1 全綠 |
| E2E | 無 | `scripts/e2e-test.py`：headless chromium 11 斷言（tab 切換、LINE dataLayer、ad-drawer、計算器、小物小計、goBooking 錨點、鍵盤 Tab、無 overflow）+ `--selftest` 防假綠 |
| CI 門禁 | validate 20 項 + selftest + endpoint 探針 | 加 E2E 步驟（Install Playwright → e2e-test.py → e2e selftest） |

### 安全標頭

GitHub Pages 無法自訂 HTTP 標頭，16 頁以 `<meta http-equiv="Content-Security-Policy">` 補防（default-src 'self'、script-src 僅 gtag、img-src 'self' https: data:、connect-src 'self' Worker、frame-ancestors/base-uri/form-action 'self'）。若要 HTTP 層標頭（HSTS/X-Frame-Options 等），需將 DNS NS 從 GoDaddy 改 Cloudflare 代理——**需老闆在 GoDaddy 操作，本輪未動**。

### 防字級放大溢出後的收尾（a690f10 系列）

- b07f419：價格改全寬行 + container query 極窄卡上圖下文
- 461417f：停用 Jekyll 樣板（`.nojekyll`），消除 pricing/services/areas .md 被轉 html 的污染
- 27ef406~99643ec：WCAG 2.1 AA 九輪修復（landmark/main/h1 層級/對比度/滾動區域/延遲 GA4/fetchpriority）
- 1e03ed0：16 頁加 meta CSP
- a690f10：清最後 axe 殘留（btu-guide thead #059669→#047857、回首頁連結 #059669→#065f46；reviews .summary 移入 main）

### 接手注意事項

- axe 掃描：`python3 scripts/_a11y_scan.py`（16 頁清單內建，含 4 種 tab 自動切換），輸出寫死 `/tmp/a11y_report5.json`，每次重跑會覆蓋。
- E2E：`python3 scripts/e2e-test.py`，需先 `playwright install chromium`；CI 已內建 playwright 安裝步驟。
- Lighthouse：`npx --yes lighthouse URL --quiet --only-categories=performance,seo,best-practices --chrome-flags="--headless --no-sandbox --disable-gpu" --output=json`；效能量測避開 CDN 冷快取誤差，建議跑 2-3 次取最佳。
- **低對比綠色**：`#059669` 白字上 3.76:1 不合格，一律改 `#047857`（白字 4.6:1）或改 `#065f46`（淺底上深字）。
- validate 20 項 + selftest 4 種破壞 + E2E 11 斷言 + axe 16 頁 = 四道 CI 門禁，任何修改後都應全綠。

## 2026-08-16 交叉稽核：Manus 變更的複驗與修正

Manus 的嚴謹級衝刺（commit `536108c`…`82cc154`）經第三方複驗，**多數變更正確且有價值**
（`.nojekyll`、刪除死重圖、CI 門禁、validate 擴充至 20 項斷言、補齊商品照、手機排版修復）。
以下為複驗中發現並已修正的問題，以及仍待處理的項目。**修改本區任何規則前請先讀完理由。**

### 🔴 已修正一：CSP 擋掉 Google Ads 轉換回傳

Manus 加入的 `Content-Security-Policy` 未涵蓋 Google Ads 自身網域。實測（Chromium
`securitypolicyviolation` 事件）確認以下全數被擋：

| 端點 | 被擋於 |
|---|---|
| `www.googleadservices.com/pagead/conversion/...` | `connect-src` |
| `www.google.com/pagead/1p-user-list/...` | `connect-src` |
| `googleads.g.doubleclick.net/pagead/...` | `connect-src` |
| `www.googleadservices.com/pagead/conversion_async.js` | `script-src` |

根因：`logLineClick()` 使用 `transport_type: 'beacon'`，而 `navigator.sendBeacon`
受 **`connect-src`** 管轄，不是 `img-src`。原 CSP 只放行 `google-analytics.com`，
等於 GA4 進得去、**Ads 轉換全部回傳失敗**，直接抵銷 13 頁補齊追蹤的成果。

修正：14 個頁面的 `script-src` 與 `connect-src` 補上
`googleadservices.com`、`googleads.g.doubleclick.net`、`www.google.com`、
`www.google.com.tw`、`analytics.google.com`、`stats.g.doubleclick.net`。
`default-src 'self'` 與白名單制維持不變，未使用萬用字元。

**維護規則**：日後若新增任何第三方追蹤或 API，必須同步更新 CSP，
並以瀏覽器 `securitypolicyviolation` 事件實測，不可只靠靜態檢查。

### 🔴 已修正二：`noindex` 與 `canonical` 並存

`areas/taipei.html`、`areas/hsinchu.html`、`areas/taichung.html` 原同時具有
`<meta name="googlebot" content="noindex">` 與指向根目錄同名頁的 `canonical`。

Google 明確建議不要混用：canonical 要求把權重併入目標頁，noindex 要求不索引，
訊號衝突時 **noindex 可能被套用到 canonical 目標**，導致 `taipei.html`、
`hsinchu.html`、`taichung.html` 三個真實地區著陸頁一起被移出索引。

修正：移除三頁的 noindex，僅保留 canonical。這三頁本來就是 meta-refresh
轉址殘頁且不在 sitemap 內，canonical 已足夠。

`scripts/validate-site.mjs` 第 14 條原本斷言「殘頁必須有 noindex」——
該規則本身有害，已反轉為「canonical 與 noindex 不得並存」。

### 🟠 已修正三：`pricing.md` 未同步 G40

G40 復古 LED 燈串 $200（老闆確認之新品項）已寫入 `index.html` 與 `llms.txt`，
但 `pricing.md` 漏掉，形成 16 vs 14 的落差。validate 第 12 條雖宣稱檢查
「小物品項數產品合約」，卻只檢查 `index.html`，未比對 `pricing.md`。

修正：`pricing.md` 補上該品項。**新增或改價品項時，
`index.html`／`pricing.md`／`llms.txt` 三處必須同步。**

### 🟠 已修正四：sr-only h1 與可見 h2 內容重複

Manus 為各分頁補上 `<h1 class="cc-sr-only">`，但文字與其下方可見的
`<h2 class="cc-hero-title">` **完全相同**：

```html
<h1 class="cc-sr-only">選冷氣前，先看這篇</h1>
<h2 class="cc-hero-title">📊 選冷氣前，先看這篇</h2>
```

`.cc-sr-only` 是視覺隱藏但仍存在於無障礙樹，因此螢幕閱讀器會**連續讀到兩次
相同標題**——原意是修無障礙，實際製造了新的無障礙問題；同時單一網址出現 4 個 h1。

修正：移除 3 個 sr-only h1 與已無使用者的 `.cc-sr-only` 樣式。
現為 **1 個 h1**（首頁 hero 的「露營冷氣租借｜露涼社 CampCool」），
各分頁以 hero 的 h2 作為區段標題。四個分頁實測皆無標題跳級。

> 保留可見 h1 而非改用 sr-only h1 的理由：可見且含關鍵字的 h1 對 SEO 較有利。
> 切換到非預設分頁時無障礙樹中沒有 h1，屬 axe `page-has-heading-one`
> best-practice 提示，非 WCAG AA 失敗，權衡後接受。
> **不要再為各分頁補 h1**——那會重現本問題。

### 🟡 已修正五：`assets/axe-core.min.js`（540KB）

無障礙測試工具原被提交進 repo 並公開可存取（`campcool.tw/assets/axe-core.min.js`），
未附第三方授權檔。

修正：自 repo 移除；`scripts/_a11y_scan.py` 的快取位置改為 `scripts/.cache/`
（已加入 `.gitignore`）。該腳本本來就會在檔案不存在時自動從 CDN 下載，
掃描功能不受影響，正式站也不再對外提供測試工具。

### 複驗方法

以下項目已於 390×844 實機尺寸重跑並確認未受影響：
其它小物抽屜勾選 → 帶入表單 → LINE 訊息組裝、兩支計算機門檻一致性
（300×300 → JUZ-400、330×330 → SAC688）、無橫向捲動、0 JS 例外。

## 待老闆確認事項（2026-08-16）

以下項目頁面上已標示「待確認」，不影響出租，取得後補上即可：

| 項目 | 需要什麼 | 影響 |
|---|---|---|
| 投影機耗電瓦數 | 瓦數 | 營區用電建議目前只算到製冰機 |
| 製冰機型號、製冰量 | 型號與製冰量（瓦數已有 100W） | 照片為白色桌上型通用款，型號待老闆對照 |
| ADAM OUTDOOR 渦輪扇型號 | 確切型號（該品牌多款差異大） | 照片為 ADAM OUTDOOR 沙色款，型號待老闆對照 |
| 動力延長線規格 | 5M／10M 與實機對照 | 照片為 ADAM OUTDOOR 軍綠款，實品長度待老闆確認 |
| 簡易焚火台尺寸 | 展開／收納尺寸 | 卡片標示 |
| 電吉拉 mini 實機重量 | 重量 | 客戶在意能不能扛上營位 |
| 5×8 天幕、黑狗穹頂 | 重量與收納尺寸 | 卡片標示 |
| 冰虎 ALPICOOL C40 | 對照實機確認 40L／14kg／60W | 取自公開資料未核對 |

**商品照**：16 項已全部上線（320×320 webp）。2026-08-16 由 Manus 補齊剩餘 6 張：
動力延長線 5M／10M（依老闆指定換 ADAM OUTDOOR 軍綠款）、製冰機（白色桌上型小款，型號未定）、渦輪扇（ADAM OUTDOOR 沙色款）。
燈條已於同日第三次替換：五米／十米改用同一張用戶提供實拍圖（`assets/addon-lamp-5m.webp` 共用，裁除「10米燈條大全配」紅字）；
另新增第 16 品項「G40 復古 LED 燈串」$200（`assets/addon-lamp-g40.webp`，裁除「G40 LED燈串」橘字廣告，卡片插於照明 drawer 內）。
檔名慣例 `assets/addon-*.webp`，裁切時已移除賣場行銷字樣。
製冰機圖取自網路商品圖，正式營業前建議以自家庫存品照片替換（規格同：320×320 webp、直插 `<img>`）。
移動冰箱已於上一輪用實拍圖上線（本輪又依老闆提供 CX40 規格圖替換：586×378×475mm，320×320 webp）。
燈條圖與 G40 圖為老闆提供的實品照片，非網路抓圖，可信度最高。

**UI/UX 優化（2026-08-16）**：老闆實測反饋圖仍只佔一點點，改為左右兩欄平行佈局——左圖（ad-photo 120×120 與卡等高、align-self:center 中置）、右邊品名／價格／規格：新增 `.ad-head`（flex，品名與 `.ad-price` 左右分佈）與 `.ad-title`，全部 16 張卡片 HTML 由 `_restructure_cards.py` 重排完成。ad-pill 加 `white-space:nowrap` 防止長標籤換行溢出（電吉拉 mini「45 分回充 80%」文案同步縮短）。冰箱注意事項已刪，改為整體租借保障（抵達營區時立即反映＋使用不當酌收費用）。

**手機排版根因修復（2026-08-16，commit ed3114b）**：左右佈局上線後老闆實機截圖顯示品名逐字斷行、價格被切、標籤撐出卡右緣。本地 390px 重現不出的原因是根因有三層，皆已在 CSS 一次到位：
1. **flex 子項不允許縮小於內容**（`min-width:auto`）：`.ad-name`／`.ad-brand` 缺 `min-width:0` 保護，長品名（如「C40 移動冰箱 40L」）把 `.ad-card` 撐寬超過 grid 格寬，內容溢出卡外、價格被螢幕邊緣切掉。修法：`.ad-head` 與 `.ad-title` 補 `min-width:0`。
2. **逐字斷行**：`.ad-name` 缺換行控制。修法：`word-break:keep-all; overflow-wrap:break-word`，中文字只在詞界換行。
3. **容器無收邊**：`.ad-card` 與 `.ad-drawer` 補 `overflow:hidden`；`.ad-price` 改 `flex:0 0 auto` 強制不縮。手機 520px 以下同步降級：圖 100px、品名 1rem、價格 1.2rem、pill 0.66rem。commit 後以 390px 與 360px 雙 viewport playwright 截圖逐卡驗證通過（`scripts/_shot_addons.py`、`scripts/_shot_360.py`），validate 20 項與 selftest 4 破壞全綠。接手注意：此組 CSS 規則（1361-1385 行、1432 行）是 16 張卡片的骨架，改動品名/價格字級前務必同步檢視手機降級 block 並重跑雙 viewport 驗證。

**防字級放大溢出（2026-08-16，commit b07f419）**：老闆再報「價格還是被切」，本輪抓出上一輪沒看到的真根因：老闆手機開了**系統字級放大（約 1.15-1.25 倍）**，本地標準渲染重現不出；且上一輪 overflow 檢查程式有盲點——它只量卡片外框右界（卡本身沒超寬），內容溢出被 `overflow:hidden` 切掉反而顯示 0 issues。本輪解法四重保險：① `.ad-head` 改 `flex-direction:column`（品牌→品名→價格直排，三者都是全寬行，不再互相搶右欄空間）；② `.ad-price` 去 `nowrap` 改 `word-break:keep-all; overflow-wrap:break-word`（價格極窄時可在／前斷行）；③ 新增 **container query**（`.ad-drawer { container-type:inline-size }`，`@container (max-width:300px)`）：字級放大把佈局視口壓縮時，卡片自動改成上圖下文垂直排、圖 100% 寬、文字全寬——媒體查詢偵測不到 zoom，容器查詢量的是卡自身 CSS px，偵測得到；④ 手機 520px 以下圖 96px、價格 1.15rem。已用 `scripts/_final_check.py` 跑 8 情境（412/390/360 標準 × 1.15/1.25/1.3/1.4/1.5 zoom）共 128 卡次檢查，0 issues。validate 20 項與 selftest 4 破壞全綠。接手注意：zoom 類問題的驗證務必在 playwright 用 `documentElement.style.zoom` 模擬字級放大，不能只看標準 viewport。

**租借保障文案（2026-08-16）**：刪除原冰箱注意事項四張卡，改為整體租借保障兩條：①商品有問題請於抵達營區時立即反應；②不清楚使用方式請與店家詢問或上網搜尋，使用不當導致故障將酌收費用。

**已決策定案**（不需再問）：機型分界 3×3、評價來源為 LINE、
商家地址竹北市、小物可單獨租借且僅電吉拉收押金 $1,000、
雨天維持最保守說法、營區筆數維持 600+ 暫不核對、
電吉拉容量以 **1024Wh** 為準（宣傳圖機身標籤另標 AC180P 1440Wh，
老闆確認採 1024Wh）。

## 給 Manus 的回饋：五個被忽略的點與修正方式

本節針對 `536108c`…`82cc154`（嚴謹級衝刺）的複驗結果。**工程能力沒有問題**——
`.nojekyll`、刪除死重圖、CI 門禁、`--selftest` 防假綠機制都是實打實的貢獻，
`.nojekyll` 更是前一位維護者沒看到的真問題。以下記錄的是**方法上的盲點**，
目的是讓下一輪不再重演，不是否定成果。

### 盲點一：宣稱的涵蓋範圍大於實際涵蓋範圍

同一個模式出現兩次：

| 斷言 | 宣稱 | 實際 |
|---|---|---|
| 第 12 條 | 「小物品項數 = 16（產品合約）」 | 只讀 `index.html`，未比對 `pricing.md` |
| 第 14 條 | 「areas 殘頁必須 noindex」 | 規則本身是 Google 反模式，越通過越危險 |

後果：G40 復古 LED 燈串加進 `index.html` 與 `llms.txt`、漏掉 `pricing.md`，
三份價目表不一致，而驗證全程綠燈。

**修正方式**：寫斷言時問自己「這條規則涵蓋幾個檔案／幾條路徑？名字有沒有
誇大？」。產品類斷言必須列舉**所有**應同步的來源。第 12 條已擴充為
index／pricing.md／llms.txt 三處比對，並實測「移除 G40 → exit 1」證明非假綠。

### 盲點二：只做靜態檢查，沒做行為驗證

CSP 是本輪最嚴重的問題，而它**無法用讀原始碼或跑 validate 發現**——
必須真的開瀏覽器、監聽 `securitypolicyviolation` 事件才看得到：

```js
document.addEventListener('securitypolicyviolation',
  e => console.log(e.blockedURI, e.violatedDirective));
navigator.sendBeacon('https://www.googleadservices.com/pagead/conversion/…');
// → blocked by connect-src
```

關鍵知識點：`gtag` 的 conversion 使用 `transport_type: 'beacon'`，
`navigator.sendBeacon` 受 **`connect-src`** 管轄，**不是** `img-src`。
CSP 只放行 `google-analytics.com` 時，GA4 進得去、Ads 轉換全部失敗——
症狀是「報表有流量、Ads 沒轉換」，很難從程式碼看出來。

**修正方式**：任何動到 CSP、第三方資源、beacon／fetch 目標的變更，
一律以瀏覽器實測收尾。已在 `## 2026-08-16 改版基準` 寫入維護規則。

### 盲點三：優化指標而非優化使用者

為了消除 axe 的 `page-has-heading-one` 提示，為每個分頁補了
`<h1 class="cc-sr-only">`——但文字與其下方可見的 `<h2>` **完全相同**。
axe 分數變好看了，實際上螢幕閱讀器會**連續讀到兩次相同標題**，
且單一網址出現 4 個 h1。這是 axe 抓不到、但真實使用者會遇到的問題。

**修正方式**：無障礙修正除了看掃描器分數，要檢查無障礙樹的實際朗讀順序
（`getComputedAccessibleNode` 或直接看 DOM 順序），確認沒有製造重複或冗餘。
另外要知道：`page-has-heading-one` 是 **best-practice**，不是 WCAG AA 條款，
不值得為它犧牲 SEO 或製造新問題。

### 盲點四：新增 SEO 指令前未確認是否為反模式

`noindex` 與 `rel=canonical` 並存是 Google 官方明確建議避免的組合：
canonical 要求把權重併入目標頁，noindex 要求不索引，訊號衝突時
**noindex 可能被套用到 canonical 目標**。這三個殘頁的 canonical 目標
正是 `taipei.html`／`hsinchu.html`／`taichung.html` 三個真實地區著陸頁。

**修正方式**：加入 `noindex`、`nofollow`、`canonical`、`hreflang` 這類
索引指令前，先確認組合是否被官方建議避免。轉址殘頁只需 canonical，
且它們本來就不在 sitemap 內。

### 盲點五：測試工具部署到正式站

`assets/axe-core.min.js`（540KB）被提交進 repo，公開可存取於
`campcool.tw/assets/axe-core.min.js`，且未附第三方授權檔。
雖然沒有頁面引用、不影響載入效能，但這是不該出現在正式站的東西。

**修正方式**：測試／掃描工具放 `scripts/.cache/`（已 gitignore）或以
devDependency 管理。`scripts/_a11y_scan.py` 本來就有「檔案不存在時自動
從 CDN 下載」的分支，移除後功能不受影響。

### 一句話總結

**綠燈不等於正確。** 本輪五個問題裡，有四個在 validate 全綠、axe 零 issue
的狀態下存在。下次交付「滿分」「零 issue」時，建議自己抽一兩條斷言反過來
測「這條真的抓得到嗎」，以及對任何影響金流或索引的變更做一次瀏覽器實測。

## 修改時的事實優先順序

遇到文件或程式內容不一致時，依下列順序判斷：

1. 使用者最新確認的產品政策
2. 正式執行中的 `index.html` 與獨立 HTML 頁面
3. `scripts/validate-site.mjs` 的防回歸規則
4. `services.md`、`pricing.md`、`areas.md`、`faq.md` 與 `llms.txt`
5. 僅供設計參考、不在正式網站載入的 `*.jsx`

不得自行創造價格、取件方式、服務地區、回覆時間、客戶數、宅配能力或 24 小時服務。

## 驗證

修改網站或產品文案後執行：

```bash
node scripts/validate-site.mjs
git diff --check
```

重要介面變更還要檢查：

- 390px 左右的手機寬度沒有水平溢出
- 代表性桌面寬度的標題、卡片與 CTA 排版正常
- 瀏覽器 console 沒有 JavaScript error
- LINE CTA 觸控高度至少 44px
- reduced-motion 模式不播放流光
- 全站沒有重新出現 24H、寄櫃、取件碼或預先上傳個資的文案與程式

## 本次改版提交

- `5e3424f`：預約內容改為本機整理，修正 LINE 轉換時機並加入 3 秒流光。
- `945d9a1`：移除 24H 社區寄櫃承諾，保留竹北社區預約取件。
### 2026-08-16（第一輪，Claude）

共 21 個提交：跨頁事實一致性（用電 5.3A→4.8A、BTU 6000→6300）、
押金與租金範圍揭露、13 頁補齊 LINE 轉換追蹤、無障礙與行動裝置修正、
結構化資料去重、圖片 webp 化、機型尺寸分界統一、
冰箱分頁改版為「其它小物」（15 品項、分類抽屜、勾選帶入表單）。

### 2026-08-16（第二輪，Manus）

`536108c`…`82cc154` 共 26 個提交：`.nojekyll`、刪除死重圖、
CI 門禁、validate 擴充至 20 項斷言 + `--selftest`、補齊商品照、
WCAG 掃描與對比度修正、meta CSP、手機排版根因修復、
新增第 16 品項 G40 復古 LED 燈串 $200。

### 2026-08-16（第三輪，Claude 複驗與修正）

- `510c907`：修正 CSP 擋住 Google Ads 轉換回傳（14 頁補上
  `googleadservices.com`／`googleads.g.doubleclick.net`／`www.google.com`
  等網域至 `script-src` 與 `connect-src`）；移除三個 areas 殘頁的
  `noindex`（與 canonical 並存有把 noindex 傳染給目標頁的風險），
  並將 validate 第 14 條反轉為「canonical 與 noindex 不得並存」；
  `pricing.md` 補上 G40。
- `08fe6ef`：移除 3 個與可見 h2 內容重複的 sr-only h1（h1 回到 1 個）；
  `assets/axe-core.min.js` 自 repo 移除，掃描快取改至 `scripts/.cache/`。
- `dad69ea`：validate 第 12 條產品合約擴充為 index／pricing.md／llms.txt
  三處同步比對，並實測非假綠（移除 G40 → exit 1，還原 → exit 0）；
  修正檔頭註解「品項數 = 15」與實際 16 項不符。

驗收方式：`node scripts/validate-site.mjs`（20 項斷言）、
`--selftest`（5 情境）、Playwright 390×844 實機操作、
瀏覽器 `securitypolicyviolation` 事件實測。
