# campcool 前台現況分析基準（2026-08-16，接手狀態）

## 用戶指示
- Claude 修改完成，可以讀取、分析、評估、建議
- 跑十個 agent 腦力激盪（十角色辯證）
- 把分數拉到 100 分滿分制（不能壓線，要超過）

## 倉庫基本事實（HEAD 68bcda3，2026-08-16）
- 靜態站 GitHub Pages，網域 campcool.tw，index.html 是正式首頁（189KB，含 CSS/JS 內嵌）
- 無建置步驟；*.jsx 為早期參考，正式站不載入
- scripts/validate-site.mjs 防回歸檢查存在（需確認內容/是否有 CI/防假綠）
- Claude 已完成 20 個 commits（2026-08-16）：webp 圖片、機型分界統一（3×3=2.72坪分界）、用電 4.8A/5.7A 修正、押金揭露、13 頁轉換追蹤（gtag+logLineClick）、FAQPage 移出首頁、areas/* 殘頁處理、冰箱頁改「其它小物」15 品項/6 抽屜

## AI-README.md 要點（Claude 維護，已讀）
- 預約流程：LINE 預填、本機整理、不得 POST 個資
- 取件政策：全預約制，禁止 24H/寄櫃/取件碼/宅配文案
- 機型分界 3×3（calcRecommend area>2.75 坪、onTentModelChange area>9㎡ 兩支計算機須一起改）
- 電吉拉容量 1024Wh 定案；押金：冷氣 $3,000/台、僅電吉拉 mini 收 $1,000
- 圖片：img 用 webp；og/twitter/JSON-LD image 維持 jpg
- reduced-motion 須放樣式表最後；輪播不得 aria-live；sticky top:69px、scroll-padding-top:72px；safe-area-inset-bottom
- 待老闆確認 7 項（電吉拉重量、天幕尺寸等）+ 缺 7 張商品照
- 事實優先順序：老闆政策 > 正式頁面 > validate 規則 > md 檔 > jsx

## 現況實測指標（2026-08-16 檢查）
- .github/workflows 不存在 → 無 CI 門禁（最大缺口之一）
- validate-site.mjs 86 行，約 12 項斷言（canonical/JSON-LD/inline JS 語法/sitemap 殘頁/首頁 8 項必留/5 項禁入/24H/寄櫃），無防假綠自檢
- 18 個 HTML（14 根 + 4 areas）；areas/taipei/hsinchu/taichung 為 meta-refresh 轉址殘頁，無 noindex；只 new-taipei 進 sitemap ✅
- gtag/js 15 頁有；logLineClick 14 頁有；缺 emergency-ac.html（該頁用自訂 logEmergencyLine，需辯證是否算缺）；areas 殘頁缺屬可接受（轉址頁不埋點）
- GA4 ID 未 grep 到 G- 字串（可能以 measurement_id 變數方式？需再查）；Google Ads AW-18167565264 在 emergency-ac
- 大圖未壓縮：homepage_hero.png 1.5MB（已有 .webp 版但 png 仍載入？需確認 CSS 引用誰）、og-cover.jpg 256KB（政策要求 jpg，OK）、taiwan_map.png 912KB
- reviews.html 仍引 review-01~05.jpg（未轉 webp）
- 無 PWA manifest；favicon.ico 16K ✅
- llms.txt 完整（2026-07-27，價格/押金/取消政策；注意 llms.txt 價格與 index 是否同步）
- index.html 188KB（CSS/JS 全內嵌——純靜態零建置風格，抽離需辯證）
- 每頁 JSON-LD 豐富（LocalBusiness/Product/FAQPage/BreadcrumbList）
- AI-README 由 Claude 維護且完整（五要素大致齊）
- 【關鍵】GA4 ID 不在 repo 內！頁首從 campcool-line-bot Worker 的 /public/config?v=20260727 動態拉 ga4_measurement_id（空字串佔位＋正規 G- 檢查）——這是「GA4 ID 單一真源」的進階版，比 0988145875 更穩，但需 validate 檢查：fetch 失敗時網站仍正常（優雅降級）
- inline CSS 約 69KB（index 的 <style> 內容）；JS 也內嵌；index.html 188KB 是純靜態風格決策
- hero 無 <img>（homepage_hero.png 未使用？在 assets 但未見 src 引用 → 可能是 dead weight，需確認 CSS url() 與其餘 13 頁）
- 所有頁面 CTA 充足（1~5 個 lin.ee）

## 補遺實測（2026-08-16）
- homepage_hero.png（1.5MB）與 taiwan_map.png（912KB）均未被任何 HTML/CSS 引用 → 確定為 dead weight，git rm
- 線上站與 repo HEAD 同步（189,890B 相同）
- og-cover.jpg 被 og/twitter/JSON-LD 引用（政策要求 jpg 正確），og-cover.webp 也存在但無引用（可留）
- 自評起點（Claude 完成後）：約 94-95（功能完成度高、JSON-LD 豐富、AI-README 完整、13 頁追蹤補齊）
- 扣分缺口：①無 CI 門禁（validate 存在但無 workflow）②validate 無防假綠③大圖 dead weight ④reviews jpg 未轉 webp⑤areas 殘頁無 noindex⑥GA4 fetch 失敗降級的防回歸斷言⑦llms.txt 日期 07-27 過時且與 08-16 改版後價格同步性未驗證

## 其他倉庫滿分制先例（可直接複製到 campcool）
- 靜態站滿分制配置：validate-site.mjs 品牌事實斷言+防假綠、site-check.yml CI 門禁、AI-readme 五要素、防回歸規則寫進 validate
- 0988145875 得 99 的配置：GA4 ID 單一真源、佔位字串禁入、每頁 CTA 強制、試算閉環
- 滿分 100 的關鍵：可掌控項目全部掌控 + AI-readme 列明外部依賴 + 防假綠 + CI 門禁

## 十角色腦力激盪預定角度
架構師/資安/效能/維運/SEO/產品/UX/主管/使用者/QA

## 執行階段狀態（2026-08-16 執行中）
- 十角色辯證完成，方案檔：campcool/十角色辯證與修改方案.md（決議已裁決，勿重辯）
- 工作目錄：/home/ubuntu/audit/campcool（已 clone，HEAD 68bcda3，Claude 最後一筆 68bcda3 docs: 防回歸規則併入 AI-README）
- 本輪 commits 尚未開始
- validate-site.mjs 現 86 行，斷言類別：canonical/JSON-LD/inline JS/sitemap 殘頁/首頁必留 8 項/禁入 5 項/24H/寄櫃
- Claude 既定鐵律（AI-README §事實優先順序）：老闆政策>正式頁>validate>md>jsx；勿造價格/取件/地區/24H 文案
- GA4 fetch 現寫法：fetch('https://campcool-line-bot.a0920077473.workers.dev/public/config?v=20260727')，id 正規 G-[A-Z0-9]+ 檢查，失敗靜默 catch
- CAMPCOOL_CONFIG.ga4MeasurementId 初始 ''
- Google Ads：AW-18167565264（index.html line 11 gtag config）
- emergency-ac.html 用自訂 logEmergencyLine（非 logLineClick）——辯證裁定不算缺口
- 修改清單：P0 validate 擴充+selftest+site-check.yml；P1 git rm hero.png/map.png、reviews jpg→webp；P2 llms.txt 更新、areas 殘頁 noindex、GA4 fetch 3s 逾時；P3 AI-README 插入 Manus 條目
- 兩支計算機門檻：calcRecommend area>2.75（坪）、onTentModelChange area>9（㎡）——validate 跨函式一致性斷言目標
- 100分分析.md 是主進度文件（在 ~/audit/），campcool 章節需更新
- 滿分制評分模型：功能 25/穩定 25/可維護 20/UX 15/成本 15；防假綠=入場券；CI 全綠=必要條件
- 上一份總報告：~/audit/滿分制最終總報告.md（campcool 當時 93 未動，本次更新後需重評 campcool→目標 97-98+）

## 執行進度快照（壓縮前保存）
### 已完成
1. P1 完成：git rm homepage_hero.png(1.5MB)、taiwan_map.png(912KB)；reviews+index 的 review-01~05.jpg img 引用→webp（meta/JSON-LD 層 jpg 保留）；全域只剩 emergency-window-kit.jpg 一個 img jpg（產品實照，保留）
2. P2a 完成：areas/taipei|hsinchu|taichung 三殘頁補 noindex（robots+googlebot）
3. P2b 完成：llms.txt 更新——日期 2026-08-16、小物 15 品項（價格以頁面 data-price 實測為準：C40 冰箱$800、渦輪扇$300、簡易焚火台$300、青鸞觀火台$300、C8 投影機$300、製冰機$300、五米黃光燈條$200、十米黃光燈條$300、持久帳篷小燈$100、動力延長線5M$100/10M$150、5×8黑膠天幕$600、蝶形天幕$600、黑狗速開穹頂$600、電吉拉mini$1,000）、服務項目加「其它小物加購」、機型選擇規則、押金規則（電吉拉另收$1,000 押金）
4. P2c 完成：index.html GA4 fetch 加 3s AbortController 逾時（scripts/_patch_ga4_timeout.py），JS 語法 node --check 通過
5. 關鍵事實確認：GA4 endpoint `https://campcool-line-bot.a0920077473.workers.dev/public/config?v=20260727` 回 `{"ga4_measurement_id":""}`——**正式 GA4 ID 尚未掛上**（14 頁都走此 endpoint 統一）；Google Ads AW-18167565264 為現用追蹤
6. 頁面小物 15 品項與價格（提取腳本 scripts/_extract_addons.py 實測）：見上
7. 14 個頁面含 public/config?v=20260727（reviews/sac-688/taichung/areas/new-taipei 都有）

### 待辦（P0，最大項）
- 擴充 scripts/validate-site.mjs 到 20+ 斷言並加 --selftest 防假綠模式。現有斷言：canonical、inline JS 語法、JSON-LD、sitemap 殘頁、首頁必留 8 項、禁入 5 項、lead value 1000、24H、寄櫃
- 新增斷言建議：GA4 config endpoint 回 JSON 且含 ga4_measurement_id key；兩支計算機門檻一致性（calcRecommend area>2.75、onTentModelChange area>9 且 >16 拒租）；每頁 gtag/js 或 logEmergencyLine 覆蓋；logLineClick 每頁存在（areas 殘頁除外）；review webp 引用；無死重圖引用斷言（homepage_hero/taiwan_map 不在任何 html）；lin.ee CTA 每頁≥1；llms.txt 日期新鮮（>30天警告）且 llms.txt 價格與頁面一致（抓小物品項數=15、兩價一致）；殘頁 noindex；inline JS 全頁 node --check（validate 已有）
- selftest 模式：改壞一個必留字串→應抓住；改壞一個禁入→應抓住；計算機常數改壞→應抓住；全通過後還原
- 建 .github/workflows/site-check.yml：push+PR 觸發，job: validate（node 22、checkout 後跑 validate-site.mjs）、selftest 子模式、endpoint 探針（curl public/config 200+JSON）
- AI-README.md 插入 Manus 2026-08-16 滿分制條目（辯證決議+斷言清單+selftest 用法+GA4 空 ID 事實+死重圖移除）
- 清理臨時腳本：scripts/_extract_addons.py、scripts/_patch_ga4_timeout.py 需改名為正式工具或刪除（validate 內建斷言可取代）
- commit 訊息需含 100分制第二輪、更新 AI-README 同 commit、push 後 GitHub Pages 自動部署、gh run 確認全綠

### campcool-bot 正式金流 Worker URL 供參考
- https://campcool-line-bot.a0920077473.workers.dev

## P0 完成記錄（2026-08-16）
1. validate-site.mjs 擴充完成：20 項斷言（原有 6 項 + 死重圖引用/git index、每頁 LINE CTA、計算機門檻 2.75/9/16、15 品項逐項存在、config endpoint 14 頁版號統一、areas noindex、評論 img jpg≤1、llms 新鮮度≤60天）
2. --selftest 防假綠：4 種破壞測試全 PASS（必留文案/禁入標記/計算機門檻/小物品項），clean-state PASS
3. **重要根因修復**：GA4 patch 遺留 bug——index.html script 1 的 GA4 IIFE `(function(){...})` 漏寫結尾 `})();`，new Function() 解析失敗。已補結尾並通過語法驗證（根因：patch 腳本只替換開頭段，未補結尾）
4. 防回歸漏洞實測：單品項改名不改變 ad-name 計數（15→15），已改 15 品項逐項關鍵字斷言
5. .github/workflows/site-check.yml 已建：selftest→full validate→endpoint probe（HTTP+JSON 契約）
6. AI-README.md 已插入 Manus 滿分制第二輪條目（辯證決議+修改表+新增斷言+selftest 用法+GA4 空 ID 事實）
7. 臨時腳本已清理
8. 待辦：commit + push + CI 確認 + 更新主進度檔與總報告


