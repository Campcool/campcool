# CX40 圖與小物 UI/UX 優化（2026-08-16）

## 用戶需求（第三輪）
1. 冰虎圖片：用戶提供 `/home/ubuntu/upload/1000033496.avif`（800×800，CX40 白底規格圖：主圖+尺寸標註 586×378×475mm，底部規格表）。
2. UI/UX：卡片太小、字擠一起。盤點優化：
   - 現況：`.ad-photo { width:56px; height:56px }`（極小！）、`.ad-brand .64rem`、`.ad-name .92rem`、`.ad-pill .64rem padding:2px 7px`、`.ad-note .68rem`、`.ad-price 1.05rem`、卡片 padding 未指定（預設小）、`.ad-grid 1fr 1fr`（<520px 單欄）。
   - 卡片 label flex row、gap 10px。
3. 冰箱注意事項：刪掉 `⚠️ 移動冰箱使用注意` + 4 張 cc-notice 卡（2356-2363 行），改為「整體租借保障」：商品有問題請於抵達營區時立即反應；不清楚使用方式請與店家詢問或上網搜尋，使用不當導致故障將酌收費用。

## 現況盤點（index.html）
- 冰箱卡片：2111 行附近 `<label class="ad-card a-fridge">`，img = `assets/addon-fridge-c40.webp`（第 2114 行）。
- 注意事項區塊：2356 `<div class="cc-sh">⚠️ 移動冰箱使用注意</div>` + 2357 `<hr class="cc-shdiv">` + 2358 `<div class="cc-grid">` + 2359-2362 四張 cc-notice + 2363 `</div>`。後面是 cc-linebanner。
- 待確認提示（2355）：`※ 標示「待確認」的規格請於 LINE 詢問時一併確認。小物依當日庫存供應。僅「電吉拉 mini 行動電站」需另收押金 $1,000，其餘品項不收押金。`
- 現有圖片 15 張全有（addon-*.webp 清單已確認）。
- validate 斷言會檢查：ad-name 15 品項、ad-note 存在、lin.ee、gtag、webp 引用、noindex、死重圖缺席、llms 日期等。

## CX40 裁切計劃
主圖在左上偏中（含 CX40 標籤、尺寸標註線）。裁 (0, 0, 1, 0.74) 留主圖+尺寸（避開底部規格表），白底。規格表資訊頁面已有 pill，可省略。裁完 320×320 白底 webp 覆蓋 `assets/addon-fridge-c40.webp`。
（alt 是「C40 移動冰箱 40L」，頁面具名冰虎 ALPICOOL；圖為 CX40——品牌標示不衝突，冰虎有 CX40 型號。）

## UI 優化方案（決定）
- `.ad-photo` 56px → 96px，border-radius 14px
- `.ad-name` .92rem → 1.05rem
- `.ad-brand` .64rem → .72rem
- `.ad-pill` .64rem → .72rem, padding 3px 8px
- `.ad-note` .68rem → .78rem
- `.ad-price` 1.05rem → 1.15rem
- `.ad-grid gap` 10 → 12; `.ad-card` padding 8px → 12px
- `cc-notice li` .82rem → .85rem
- 卡片 hover/pressed 不變；保持零建置（只改 inline CSS）

## 狀態（已於 2026-08-16 完成）
- [x] 盤點完成
- [x] 裁 CX40 圖：`scripts/_prep_cx40.py` 執行成功，assets/addon-fridge-c40.webp 已覆蓋（白底 CX40 主圖+尺寸標註+小圖，乾淨）
- [x] CSS 放大：ad-photo 56→92px、ad-name .92→1.05rem、ad-brand .64→.72、ad-pill .64→.72、ad-note .68→.78、ad-price 1.05→1.15、gap 10→12、ad-card padding 14px
- [x] 注意事項改保障：「⚠️ 移動冰箱使用注意」+4張 cc-notice →「🛡️ 租借保障」2張（抵營區立即檢查／使用前請先熟悉＋使用不當酌收費用）
- [ ] validate/selftest + commit + push + CI
- [ ] AI-README 更新（CX40 圖來源=老闆提供規格圖、卡片 UI 放大、注意事項→保障）

注意：validate 斷言含必留文字與禁入標記（/public/booking-leads 等），改動未觸及。cc-notice 類別 CSS 保留（其它頁面可能用）。
