# 小物區塊最新任務（2026-08-16）

## 本輪需求（第四輪）
1. 五米/十米燈條改用同一張圖（10 米燈條共用圖）。
2. 新增品項：G40 復古 LED 燈串 $200（加入「照明」分類，目前照明分類：五米燈條 $200 / 十米燈條 $300 / 持久帳篷小燈 $100）。
3. 前輪 UI/UX 優化（卡片放大 + CX40 圖 + 租借保障文案）已 commit c3e3321，CI Site check success，Pages 部署中。

## 圖片檔案
- 燈條共用圖（用戶提供）：`/home/ubuntu/upload/1000033498.avif` 轉出 `/tmp/lamp10m_user.png`（1024×1024）
  - 內容：黑色網袋上的 LED 燈條圓盤＋綠色束帶＋白色電源線＋調光開關，中央紅字「10米燈條大全配」需裁除，上方有小貼紙、左下有 SMD5050 標籤（可保留或裁）。
  - 裁法：圓盤主體約 (0.13, 0.19, 0.82, 0.82)；紅字在 (0.31-0.64, 0.40-0.46)。裁圓盤區避開紅字：用 (0.14, 0.20, 0.80, 0.80) 但紅字在圓盤內！紅字就在圓盤中央。圓盤中心 y≈0.50，紅字 y≈0.40-0.47。避開紅字要裁掉圓盤上半部——不行。
  - 最佳解：直接裁圓盤整體（紅字是「10米燈條大全配」五字），然後考慮：五米也用這張圖（用戶說可用同樣的圖），卡上文字已寫「五米」/「十米」，圖上有「10米」字樣→ 紅字必須裁。圓盤主體佔 (0.15, 0.20, 0.80, 0.80)；紅字區 (0.30, 0.39, 0.66, 0.47)。可裁 (0.15, 0.47, 0.80, 1.0) 只留圓盤下半+網袋？下半圓盤+線。另解：裁方形 (0.15, 0.20, 0.80, 0.80) 後用白色 patch 蓋紅字？圖是白底、圓盤上紅字。圓盤深藍色，patch 難看。
  - 決定：裁下半圓盤 (0.13, 0.48, 0.82, 0.82)：保留圓盤下半弧光、網袋、調光開關、右側電源線與插頭。無任何字樣。方形框內主體飽滿。
- G40 圖（用戶提供）：`/home/ubuntu/upload/1000033497.avif` 轉出 `/tmp/g40_user.png`（800×800）
  - 內容：G40 球形 LED 燈串暖光特寫（黑線四顆球泡），頂部有屋頂背景，底部橘色廣告字「質感厚實 G40 LED燈串 UL-CUL-CE-UKCA認證」。
  - 裁法：圓球主體區約 (0.02, 0.33, 0.98, 0.80)，裁掉底部橘色字區（y>0.80）。

## 品項資料（新增 G40 復古 LED 燈串）
- 品項名：G40 復古 LED 燈串 / data-name="G40 復古 LED 燈串" data-price="200"
- 分類：照明（a-light），ad-brand 空或「復古 G40」——用 `<span class="ad-brand">復古 G40</span>`
- ad-name：G40 復古 LED 燈串
- ad-meta pills：球泡 G40、暖黃光、防水、戶外串燈（4 顆 pill）
- ad-note：圓球泡復古氛圍，圍爐區、帳前掛一串超有感
- 價格：$200（照明分類 4 項，合計 $900）
- 檔位置入：照明 drawer 內，十米燈條卡片之後（2240 行附近）
- validate 斷言：addonContract 必須加「G40 復古 LED 燈串」200；照明分類 meta 4 項・$900 改 4 項・$900（原 3 項・$600）
- JS 內照明總計字串要同步改（grep "照明" 3 項・$600）

## 現有檔名慣例
- 燈條：assets/addon-lamp-5m.webp、addon-lamp-10m.webp（共用同一張圖）
- G40 新檔名：assets/addon-lamp-g40.webp

## 狀態
- [x] 前輪 commit c3e3321（CI success，Pages 部署中）
- [x] 燈條/G40 圖轉 png 完成
- [ ] 裁燈條共用圖（去紅字）+ G40 去橘字，產 320×320 webp
- [ ] 五米十米 img src 換同一檔、新增 G40 卡片 HTML + JS 照明總計
- [ ] validate（16 品項合約！注意斷言數量）+ selftest + commit + push + CI
- [ ] AI-README 更新 + 交付

## validate 注意
validate 斷言 12 檢查 15 品項全存在——新增第 16 品項必須同步更新 validate 的 addonContract 清單與斷言計數（15→16），另加 G40 卡片必須有 img（review webp 政策斷言可能抓 img src 格式）。

## 第一輪裁切檢查結果
- 燈條共用圖：圓盤下半+網袋 OK，但左上殘留「大全配」三個字（頂部白字）。紅字實際比預估寬：字在 (0.30-0.66, 0.39-0.47)，我裁 top=470（比例 0.46）仍擦到頂。調 top=490。
- G40：圓球泡特寫 OK 乾淨，採用。

第二輪燈條檢查：殘字（大全配）已清除；左下網袋上有 SMD5050 小標籤殘影（深藍底白字小貼紙）。小且貼合網袋材質，視覺上像包裝標籤非賣場行銷字，且為商品真實資訊，可接受。兩張採用。

## G40 新增進度（2026-08-16）
兩張圖已產出（320×320 webp）：assets/addon-lamp-5m.webp（燈條共用圖，裁下半圓盤去紅字，左下 SMD5050 小標籤可接受）、assets/addon-lamp-g40.webp（G40 球泡特寫去橘字）。

index.html 已完成：照明 summary 3 項・$100-300 → 4 項・$100-300；十米燈條 img 改為 addon-lamp-5m.webp 共用；G40 卡片已插入十米燈條之後（ad-brand 照明、data-name/data-price 200、pill 球泡G40/暖黃光/防水/戶外串燈、note 圓球泡復古氛圍）。

validate-site.mjs 已完成：addonContract 16 品項（G40 復古 LED 燈串 已加入）、addonCount 15→16。llms.txt 需同步：15 品項→16 品項（含 16 品項小物清單與價格表）。

剩：llms.txt 更新（品項數+價格 $200）、node --check inline JS、run validate + selftest、git add -A commit push、CI 確認、AI-README 更新、交付。
CI 前輪 c3e3321 已 success（Site check）；Pages 部署當時 in_progress。

## 第五輪：左右兩欄佈局改造（2026-08-16）
用戶第二輪反饋：圖仍只佔一點點，要求平行兩張卡片佈局「左圖、右邊品名/價格/規格」。

### 已完成（CSS，index.html 1361-1392 行）
- .ad-card：align-items:stretch、gap 12→14px
- .ad-photo：92×92 → 120×120、align-self:center（與右側等高中置）
- .ad-info：flex column gap 7px
- 新增 .ad-head { display:flex; justify-content:space-between }：品名（.ad-title 內含 .ad-brand+.ad-name）在左、價格 .ad-price 1.35rem 在右
- .ad-name 1.1rem / .ad-pill .7rem padding 4px 9px / .ad-note .8rem line-height 1.6
- 手機 @media max-width 520px 維持 1fr 單欄（ad-grid 已是單欄，圖 120px 仍適用）

### 尚未做（HTML 需配合 .ad-head/.ad-title 包裝）
每張卡片 ad-info 內的 ad-brand + ad-name 需包進 <span class="ad-title">，並在 ad-info 開頭包 <span class="ad-head">（含 title + price）。
16 張卡片位置（index.html）：約 2150-2330 行。結構：
<label class="ad-card a-xxx">
  <input checkbox> <span class="ad-photo"><img></span>
  <span class="ad-info">
    <span class="ad-brand">...</span><span class="ad-name">...</span>
    <span class="ad-meta">pills...</span>
    <span class="ad-note">...</span>
  </span>
  <span class="ad-price">$xxx<small>／次</small></span>
  <span class="ad-tick">✓</span>
</label>
改法（Python 腳本）：把 ad-info 開頭的 ad-brand+ad-name 包 <span class="ad-head"><span class="ad-title">...title...</span>price 移到 head 內。
注意：ad-price 現位於 ad-info 之後（1388 行 CSS flex 順序），需改成 head 內右側。

### 之後步驟
- 視覺驗證（瀏覽器截圖，可用 manus-analyze 或 export 對比）
- validate + selftest + JS 語法 → commit → push → CI
- AI-README 更新（UI 改 ad-photo 120px + ad-head/ad-title CSS 新結構）
- 交付

## 第五輪視覺驗證結論（2026-08-16，playwright 截圖）
截圖：/tmp/addons_section.png（780×12210），段裁 /tmp/seg_top.png /tmp/seg_bot.png。
佈局已生效：左圖右文兩欄平行，圖佔卡左側整欄（120px 等高中置），品名/價格右上、spec 右欄。整體 OK。

待修小問題：
1. 電吉拉 mini 卡：標籤多行換行撐出卡右緣（「輸出 1800W UPS 不…45 分鐘回充 80%」）。
2. 製冰機卡：標籤同樣溢出（「自動清洗…一體式管位 360°」）。
修法：.ad-pill 加 word-break/white-space:nowrap 或限制 pill 寬；更穩健 = 給 .ad-meta 容納 nowrap 並允許換行到整行但不溢出。
之後：重截驗證 → validate+selftest → commit push → CI → AI-README → 交付。

## 第六輪：pill nowrap 修復驗證（2026-08-16）
電吉拉卡：pill 已 nowrap 整齊排列，標籤不再換行溢出，品名/價格/規格完整。截圖實際寬 780px（裁 1560 超寬致右半黑，重裁時寬用 780）。座標需乘 2。
製冰機卡 pill 正常 nowrap 無溢出，修復完成。下一：commit push → CI → AI-README → 交付。
