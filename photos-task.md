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

## 第七輪：用戶實機截圖 1000033500.jpg（手機 15:59，viewport 約 390-412px 寬）
用戶反饋「還是排版問題，徹底檢查根因」。截圖關鍵觀察：
1. C40 卡：品名「C40 移動冰箱 40L」斷成 4 行（每行 1-2 字），品牌「冰虎 ALPICOOL」斷 2 行，價格 $800 被右緣切掉一半
2. 5×8 天幕卡：品牌「遮蔽」直式斷行（「遮/蔽」上下排），品名「5×8 黑膠天幕」斷 2 行，$600 完整但靠右緣
3. 第一張截圖：簡易焚火台卡「尺寸待確認*」黃色標籤斷 2 行且撐出卡右緣
4. 我的本地 playwright 390px 截圖沒有這些問題——關鍵差：用戶用 Android 瀏覽器，viewport 寬可能 < 390（或 360），且用戶截圖中 card 內容明顯超出螢幕（價格被切）→ 卡片容器在某個寬度下無溢出保護。
根因假說：
- .ad-name 1.1rem 在窄屏（360px）+ 長品名「C40 移動冰箱 40L」（8字×1.1rem≈寬>卡片可用寬）→ 逐字斷行
- .ad-price white-space:nowrap 但 .ad-head 沒 min-width 限制→ flex 項目被擠到卡片外，溢出容器（overflow 未 hidden）
- .ad-meta pills nowrap 單行多 pill 總寬>卡片寬→溢出
- viewport meta 已設？index.html 應有 <meta name=viewport> 但需確認（若缺 → 手機不縮放致寬度計算全錯，這是最大嫌疑！）
要查：viewport meta、body 寬度、ad-card 寬度來源（ad-grid grid-template-columns? flex?）、ad-head gap 與 flex-basis。

## 根因確診（第七輪）
viewport meta 有（width=device-width）。用戶 viewport 約 390px。
真正的根因：`<label class="ad-card">` 包裹 `<input type=checkbox>`。瀏覽器預設 `<label>` 對 inline-block checkbox 的行為 + **1363 行 `.ad-card { display:flex }` 與 1421 行 `.ad-card { position:relative }` 兩次定義**——CSS 級聯後 flex 生效（1421 在 1363 後，但 1421 沒覆寫 display，兩規則皆套用）。
核心問題：`.ad-card` 沒有 `overflow:hidden` 且 flex 子項（.ad-info 內容）寬度不受限：
- `.ad-name`（1.1rem、900）與 `.ad-brand` 沒有 `min-width:0` 限制 → flex 子項預設 min-width:auto（不允許縮小於內容），品名長時 flex 容器被撐寬超過 grid 格寬，內容溢出標籤容器 → 用戶截圖看到卡片內容超出螢幕、價格被切。
- `.ad-head` 沒 overflow/ellipsis 保護，斷字靠瀏覽器預設 word-break。
- 用戶截圖品名逐字換行：因為 .ad-head display:flex 內 .ad-title min-width:0 已設但 .ad-name 無 word-break，且卡片被撐寬後文字仍逐字換行——實際因 font 回退/換行規則。
修復方案（一次到位）：
1. .ad-card 加 overflow:hidden
2. .ad-info 加 min-width:0（現已有）；.ad-name / .ad-brand 加 overflow-wrap:anywhere 或保持 nowrap？——要解決逐字斷行，給 .ad-name 合理的字級（手機降為 1rem）+ overflow-wrap:break-word
3. .ad-price flex-shrink:0 保留
4. .ad-head 加 min-width:0（flex 子項）
5. @media max-width:520px 時 .ad-photo 縮到 100px、.ad-name 1rem、.ad-price 1.2rem
6. 移除 .ad-tick 絕對定位在右上與 .ad-head 的 justify-between 衝突？——.ad-tick absolute top/right，不影響。
先寫 CSS 再逐卡 390 與 360 雙 viewport 驗證。

## 第七輪 CSS 修正已套用（尚未驗證/commit）
- .ad-head 加 min-width:0；.ad-title flex column min-width:0
- .ad-name：word-break:keep-all + overflow-wrap:break-word（解決逐字斷行），margin 0
- .ad-card 加 overflow:hidden；.ad-drawer 加 min-width:0
- .ad-price flex:0 0 auto（不縮）
- 待做：① 手機 @media max-width:520px 加 .ad-photo 100px/.ad-name 1rem/.ad-price 1.2rem 降級 ② playwright 逐卡雙 viewport（390/360）驗證 ③ validate+selftest ④ commit push CI ⑤ AI-README ⑥ 交付（附件用逐卡驗證圖 /tmp/addons_section.png 與 fix_*.png）
- 截圖腳本：scripts/_shot_addons.py（切 fridge tab 開全 drawer 截其它小物 section，存 /tmp/addons_section.png）；裁段：scripts/_crop_addons.py
- 卡片 rect 座標（390×900 邏輯 px，截圖 dsf=2 需乘 2，寬 780）：C40冰箱2078→662*2? 實測清單：C40 662/287、5×8天幕1041、蝶形1314、黑狗1588、電吉拉2078、延長5M2468、10M2630、五米燈2872、十米燈3080、G40 3262、持久小燈3531、焚火台3980、青鸞4194、投影機4665、製冰機5036、渦輪扇5225（top, height）
- 上次 commit c31fb01（佈局改造）、1e1db9b（AI-README）已 push，CI 全綠。本輪若成功將是第三個 commit。

## 第七輪 CSS 修正後驗證（390px，seg_top/seg_bot）
seg_top.png：C40 品名「C40 移動冰箱 40L」正常斷行兩行內（非逐字）、品牌「冰虎 ALPICOOL」一行、價格 $800 完整不切、右欄 pills 正常。5×8 黑膠天幕：品牌「遮蔽」一行、品名正常。蝶形/黑狗/電吉拉/延長線卡皆左圖右文整齊，pill nowrap 無溢出。
seg_bot.png：五米/十米燈條/G40/焚火台/青鸞/投影機/製冰機/渦輪扇皆正常，「尺寸待確認*」標籤 nowrap 於單行（焚火台段）。
待補：360px viewport 雙驗證 + validate/selftest + commit。

## 第八輪：用戶再報「還是一樣」（截圖 1000033501.jpg，16:08，1440×3200）
### 截圖觀察
- URL 欄顯示 campcool.tw/#f（有 hash），底部導航列（租賃方案/選購指南/預約方式/其它小物四 tab）。
- 5M 卡：「動力延長線（綠）5M」品名斷 2 行（5M 掉第二行），**價格 $100 被切**（$1 0 露右半、00 被切），**$150 同樣被切**。
- 右上角有白色圓圈（ad-tick 勾選鈕）浮在卡片右上、價格文字疊在上面——價格 $100 位於 tick 圓圈下方？不對：價格藍色大字在右上，tick 白圓蓋在價格上。重點：價格被螢幕右緣切。
- 綠色區域掃描：band 300（y 387-548）有 62108 綠色像素 → 用戶截圖的「詢問·預約」CTA 在 y≈390-550（不是 860）。截圖上半部有狀態列黑條、16:08 時間 y≈460？時間「16:08」在 y≈700 行（截圖中段黑條：網址列區 y≈750-830）。**這張截圖其實是長截圖拼接！**：上半（0-780 是先前截圖的頂部）+ 中下部是現在時刻。重點是卡片区 y≈940-1850。
### 關鍵量測
- 卡片白色內容區 x:113-1327（長 1214px），截圖寬 1440 → **卡片佔比 84.3%**
- 標準 412px 邏輯寬：cc-body max-width 680、padding .9rem（≈14px*2=28）→ 內容寬 = 412-28 = 384 → 卡片佔比 93%
- **84.3% < 93%** → 用戶端有放大！放大倍率約 93/84.3 ≈ 1.1（內容被放大 1.1 倍導致溢出）
- 精確倍率：若 zoom 1.1，CSS 像素寬 = 412/1.1 ≈ 374，內容 374-28=346，佔比 346/374 = 92.5%？不对——zoom 時整頁放大，viewport 不變，卡片邏輯寬仍 384 但顯示 384*1.1=422 物理 CSS px > 412 → 溢出 10px，價格被切符合！
- 判定：用戶手機開啟了 **顯示字級放大（Android 系統字體 1.1x-1.2x）或 Chrome zoom**。Android Chrome 會尊重系統 font scale 對 root font-size 放大（rem 單位），我們的 html { font-size: clamp(20px,16px+1vw,24px) } 是 rem 基準 → 整個頁面的 rem 尺寸跟著放大，卡片內寬不變但字變大 → 內容撐寬溢出。
### 結論（第八輪根因）
- 前輪 CSS 沒有限制「rem 字級被系統放大後」的溢出保護：.ad-name 1.1rem → 放大 1.15 倍 = 1.265rem，卡片寬固定 384，文字撐出。
- **根本修法：不再依賴字級大小排版，改為「價格與品名不與圖片搶空間」的佈局**：
  1. 價格從 .ad-head（flex row）移到 .ad-info 內、位於品名下方，變成「左圖、右：品牌/品名/價格/標籤/說明」直排（垂直堆疊），右欄寬度全歸文字，不管字多大都不會溢出卡。但用戶要「右邊品名/價格」平行——品名與價格同列但價格用 nowrap+ellipsis 防切？會截斷。
  2. 更穩：右欄用 min-width:0 + flex 收縮，但 ad-price 是 nowrap flex-shrink:0 故意不被擠 → 當右欄太窄，價格溢出。修法：品名允許縮（min-width:0 已有），價格維持 nowrap 但 .ad-head 加 overflow:hidden？價格被隱藏不優雅。
  3. **推薦**：手機 narrow 時卡片改為垂直佈局（ad-card flex-direction:column: 上圖右欄改 full width？圖佔頂部，文字在下）。但 520px 以下已是 1fr 單欄卡。
  4. 最佳：讓品名用 `min-width:0` + `overflow-wrap`（已有），價格縮小為 1.1rem 並縮圖 88px；且 .ad-card 內 flex-wrap 不換行前提下，加 `width:100%; min-width:0` 到 .ad-card（grid 格內 card 寬=格寬，flex 子項不會撐格寬——**除非 card 是 grid 的直接子項但 .ad-info 內 flex 項目 min-width:auto 會撐 card 本身**，card 本身寬度由 grid 定，內部溢出被 overflow:hidden 切掉 → 價格消失！這就是問題：overflow:hidden 後價格被「切掉」而不是溢出，但用戶截圖價格在卡外右側可見一半 → overflow:hidden 沒生效？
- **新嫌疑**：`.ad-card` 是 `<label>`，其 CSS 有兩處定義（1374 行 flex、1432 行 position:relative）。1432 行是「可勾選卡片」規則，**不含 overflow:hidden？有加！**（edit 已套 overflow:hidden）。但 overflow:hidden 對 display:flex 的 label 有效。
- **另一嫌疑（最大）**：用戶截圖中 tick 白圓位置與價格重疊。可能截圖是「zoom 後 overflow 內容被切」——價格只露出左半。這和 overflow:hidden 效果一致：內容被切。為什麼本地看不到？因為本地沒有系統字體放大。
- 解法核心：讓卡內任何 rem 元素在字級放大 1.3x 下也不溢出 → **把所有固定寬（ad-photo 120px/100px）與字級改為相對式**：ad-photo 用 aspect-ratio + 固定高度比例？或最簡單：**右欄價格改放到品名下方第二行（全寬行）**，價格行獨佔全寬，怎麼放大都不溢出；品名單行顯示（white-space:nowrap + overflow hidden ellipsis？不要 ellipsis，品名最多兩行 overflow-wrap）。這樣頭部一行只剩品牌+品名（不含價格），空間充足。

### 執行計畫
1. CSS：.ad-price 移出 .ad-head（放回 .ad-info 內、ad-meta 之前），.ad-head 只留 .ad-title（品牌+品名）+ gap。品名 word-break keep-all。
2. 520px 降級保留。
3. playwright zoom 1.15/1.25/1.3 多情境驗證（script/_repro_zoom.py 已有 412/480/zoom115/zoom125）。
4. validate+selftest → commit → CI → AI-README → 交付。

## 第八輪關鍵實測發現（zoom 1.25 量測）
- 用戶「價格被切」真因：**用戶端有字級放大（系統字體/瀏覽器 zoom ≈1.15-1.25）**，本地 390px 標準渲染重現不出。
- zoom 1.25 下實測 5M 卡：卡 r=375.9（內寬 ok），但 **ad-name r=390.8 超卡 15px、ad-price r=509.6 超卡 134px** → overflow:hidden 把內容切掉 = 用戶看到的「被切一半」。
- 先前程式化 overflow 檢查為 0 是假象：檢查的是 .ad-card 本身右界（flex 子項不撐 grid 格寬），內容溢出被 hidden 切掉了——**隱藏≠沒問題**。
- CSS 已改 ad-head 為 column 但量測仍顯示 price x=400：疑似 CSS 規則順序問題——1432 行後的 `.ad-info { display:block; } .ad-brand, .ad-name, .ad-note { display:block; }` 沒有覆蓋 `.ad-price`，且 `.ad-price` 的 `align-self:flex-start` 存在。更關鍵：HTML 中 ad-price 仍在 ad-head 內（重排腳本 _restructure_cards.py 把 price 包進 ad-head）。
- 量測顯示 name l=250.8（在圖右側 155 之後）但 price l=400 超卡——ad-head column 應讓子項都 100% 寬。**column 可能沒生效**因為 CSS 選擇器順序或 1432 行 `/* 可勾選卡片 */` block 的 `.ad-info { display:block; }` 之後沒有動 ad-head。
- 待查：ad-head 是否真的 column（getComputedStyle 確認）。

## 第八輪最終修正方向（執行中）
1. 用 JS 量 ad-head 的 flex-direction 確認 CSS 是否生效。
2. 最穩健結構性修法：ad-head 改 `display:block`（block 元素天然 100% 寬，絕不被擠），brand/name/price 都 block 直排；price 加 `margin-top:4px` 與 name 拉開。
3. 同時把「品名與價格的視覺關係」保持：品牌→品名→價格（全寬行），標籤→說明。
4. zoom 1.4 極端測試通過（程式化量 price/name 皆 ≤ 卡右界）才 commit。
5. 之後 validate+selftest → commit push → CI → AI-README → 交付（附件：zoom 情境截圖 + 量測數據）。

## zoom 1.4 極端量測（第八輪）
412px × zoom 1.4 下：卡片寬 329、圖 168px、右欄起點 251（內寬僅 329-168-24-11≈126px），品名「電吉拉 mini 行動電站」被強行換成 5.6 行（每行約 2 字），價格 26px 10 字（含／次）寬 149px > 內寬 126 → price r=400 超卡 329 達 71px。zoom ≤ 1.3 全綠（0 issues），1.4 只有一卡（電吉拉 mini，品名最長 8 字+英文混排）出 issue。

判定 zoom 1.4 已是極端（Android 系統字級最大 1.5，但字級放大不影響 CSS px 佈局，只會放大 rem 文字；實際等價 zoom 約 1.5 時品名仍會換行）。最後防線：price 與 meta 改 max-width:100% + overflow-wrap，並讓品名在極窄右欄時強制換行（keep-all 已有）。price 是 nowrap 不能換行，唯一解是右欄足夠寬或 price 換行允許。更穩：右欄最小保證寬度無法做（grid 單欄時右欄隨圖縮）。

**最終方案**：price 保持 nowrap 但加 `max-width:100%` 無效；改 `.ad-price { white-space:normal; word-break:keep-all }` 允許價格換行（"$100／次" 最多斷在／前）。可讀性影響極小（價格仍是兩塊）。品名已 keep-all 會自然換行。這樣即使 zoom 1.5 也不會溢出。

# 第九輪：嚴謹級 100 分衝刺（用戶授權，token 無限）
## 用戶目標
往嚴謹級衝，測試 Manus 能力上限。階段目標：
1. Lighthouse 實測基準（Perf/SEO/BP）
2. 無障礙（WCAG 2.1 AA）
3. 跨瀏覽器（Safari iOS 模擬）
4. 安全標頭（CSP 等）
5. 自動化 E2E + CI
6. validate + CI + AI-README + 嚴謹審查報告

## 基準數據（2026-08-16，campcool.tw 線上最新版 b07f419+）
### Lighthouse 首頁（headless Chrome，desktop 模擬）
- Performance: 61 / SEO: 92 / Best Practices: 82
- 主要扣分項：server-response-time（CDN 首筆 2.9s）、max-potential-fid、mainthread-work-breakdown（index.html 188KB+ 內嵌 JS）、third-party-summary（GA4/Google Ads/GTM？）、deprecations
- 待查：deprecations 是什麼 API、third-party 是哪些、LCP element

### 工具
- Lighthouse CLI：`npx --yes lighthouse URL --quiet --only-categories=performance,seo,best-practices --chrome-flags="--headless --no-sandbox --disable-gpu" --output=json --output-path=X.json`（lighthouse 12.8.2，node 22.13，npx 在 /home/ubuntu/.nvm/.../bin）
- Lighthouse JSON 輸出在 /tmp/lh_out/
- axe-core：npm 裝 axe-core，用 playwright inject evaluate 跑 axe.run 掃描全頁
- 安全標頭：GitHub Pages 只支援有限 headers（.nojekyll 等），CSP 需 Cloudflare Worker 或 gh pages 不支援自訂 headers → 待確認方案

### 待辦
- [ ] 全 14 根頁面 Lighthouse 批測（skip llms.txt/pricing.md 等 md）
- [ ] axe 全頁無障礙掃描（18 頁 × 4 tabs）
- [ ] 對比度檢查（品牌綠 #059669 on white?、ad-pill 等）
- [ ] 安全標頭現狀檢查（curl -I）
- [ ] Safari 驗證：sandbox 無 Safari，用 wkhtml 不可行；改用 webkit playwright（playwright install webkit）模擬 + 360/390 viewport
- [ ] E2E：playwright 腳本覆蓋關鍵流程（tab 切換、抽屜開合、勾選→LINE 跳轉、計算器、預約 local-only 限制）→ CI 加 workflow

### Lighthouse 診斷發現（首頁）
1. **server-response-time 990ms**：GitHub Pages/Fastly 首筆 986ms（CDN edge 冷快取）。我們無法控 Fastly，但可加 preconnect/dns-prefetch 與 Service Worker 快取？靜態站最佳實踐：html 不可 cache long（已 max-age=600）。此項是 CDN 特性，屬「部分可接受」；可用 `<link rel="preconnect">` 無法加速首筆。替代：Lighthouse 對 600ms 以下給 100，990ms 給 0——這幾乎是 GitHub Pages 固定稅。可嘗試透過 Cloudflare？用戶已用 campcool.tw 直接指向 GitHub Pages（無 CF）。**不修此項**（基礎設施層，非網站層），記錄於報告。
2. **deprecations：AttributionReporting**（gtag.js 內部，Google 自家 depreciation，我們無法修）→ 記錄為第三方限制。
3. **third-party**：主要是 googletagmanager（GA4+Google Ads）。blocking 待量。
4. **main-thread work**：188KB 內嵌 JS 解析。可優：延遲載入（defer 不可行，內嵌 script 在 body 尾）。可把 GA4 腳本改用 gtag 非同步 + 延遲初始化（3s 後或 idle）。
5. **LCP element**：待查（可能是 hero 圖或 header）。

### 修復策略（效能，目標 Perf ≥90）
- GA4/Ads 初始化延遲至 3s 或 after first interaction（現有 3s 逾時邏輯，確認是否延遲載入）
- 檢查 gtag 腳本是否 blocking（async 已加？待查）
- LCP 元素預先載入（preload hero 圖）
- 圖片格式 webp/avif 已做；檢查是否有未 lazy 的大圖在首屏
- SEO 92：查扣分項（crawlable links? meta description? og? 待跑全頁）
- BP 82：deprecations(第三方)、no document.write? 待查其他 audit

### 安全標頭現狀（2026-08-16）
**GitHub Pages 全站 0 安全標頭**：HSTS/X-Content-Type/X-Frame-Options/CSP/Referrer-Policy 全部 missing。server: GitHub.com via varnish。GitHub Pages 不支援自訂 response headers（.nojekyll 只能控行為）。
**可行方案**（按成本排序）：
1. 純前端 CSP：`<meta http-equiv="Content-Security-Policy">`——支援 default-src/script-src/style-src 大部分指令，但**不支援 frame-ancestors/report-uri 等**；且 meta CSP 與 inline script（本站全內嵌）衝突，需 hash/nonce 不可行 → 只能放寬 `script-src 'unsafe-inline'`，安全性提升有限但擋第三方載入
2. Cloudflare 代理（免費版）：可加全部 headers + HSTS + 快取規則 → 需改 DNS；用戶域名 campcool.tw 的 DNS 在哪？需問用戶或檢查 NS 記錄
3. gh pages 不支援 → 報告中明確記錄此限制與建議
**先做 meta CSP**（可行範圍內），並查 NS 記錄決定是否建議 CF。

### DNS 結論
campcool.tw 由 **GoDaddy（domaincontrol.com NS）託管**，A 記錄直指 GitHub Pages 4 IP。接 Cloudflare 有兩條路：①改 NS 到 CF（全託管，headers/HSTS/快取/防禦全開，免費）②只改 A 記錄到 CF proxy（保留 GoDaddy DNS）。**建議用戶選①**，但需用戶本人在 GoDaddy 操作 10 分鐘。此項列為「待用戶操作」，我提供完整步驟文件。
（注意：用戶要求不要動公司資源——DNS 屬用戶個人域名，改 NS 屬正常維運，非公司資源。）

## 第九輪基準數據（定稿）2026-08-16
### Lighthouse（11 頁，perf/seo/bp）
- 大部分頁面 seo=100 bp=100；唯一例外 index(seo92 bp82)、pricing/sac-688(seo92)
- Perf 範圍 55-84：index 61（最差）、pricing 55（最差）、taipei 84（最好）
- **全站共因**：server-response-time 990ms（Fastly 冷快取，11/11 全中，無法修）、LCP 4.1s（index）、speed-index 7.5s、max-potential-fid 940ms、main-thread 3.6s、third-party 330ms（gtag.js）
- **可修**：
  - unused-javascript 52KiB（legacy-javascript: gtag.js polyfill，10/11）→ gtag 由 Google 控，無法修，記錄
  - uses-long-cache-ttl/cache-insight（9/11）：GitHub Pages 圖片 CDN 快取 TTL 短 → 圖片已用 webp，此項 CDN 層，部分可接受；但可加 `?v=` 指紋化長期 cache 給圖片？GH Pages CDN 快取由 Fastly 控，max-age 由伺服器回，無法改 → 記錄
  - robots-txt not valid（2/11）→ 檢查 robots.txt 內容並修正
  - meta-description missing（pricing/sac-688）→ 補
  - render-blocking-resources pricing 5830ms → 檢查 pricing.html 的 link rel=stylesheet 外部？（本站 CSS 內嵌，可能是 gtag 或 print css？）待查
  - dom-size 1156（index 唯一）→ 可接受範圍但可精簡
  - lcp-lazy-loaded（reviews）→ LCP 圖被 lazy 載入，改 eager
  - unminified-css 3KiB → 微調
  - image-delivery 43KiB → 部分圖可再壓縮/webp
  - unused-css 11KiB → 內嵌 CSS 全頁共用，可接受
- **不可修/基礎設施**：server-response-time、legacy-javascript(gtag)、cache-ttl(Fastly)、deprecations(AttributionReporting/gtag)

### axe 無障礙（19 頁次，19/19 完成）
- 主要違規：region 147x（moderate，Aria 分區缺 landmark/heading）、color-contrast 44x（serious）、landmark-one-main 8x、page-has-heading-one 3x、heading-order 3x、scrollable-region-focusable 2x（serious）
- 重災區：index:booking 62、index:fridge 58、index:rental 37、btu-guide 15、reviews 8
- juz-400 0 violations（標竿）
- **待查 color-contrast 具體元素**：從 report 找高 impact 示例（如 .tag 熱門、.cc-hero-badge 等）

### 安全標頭
- GitHub Pages 0 headers；DNS=GoDaddy，A 直連 GH Pages → Cloudflare 代理可行（用戶操作 DNS 10 分鐘）
- 可立即做：meta CSP（unsafe-inline 因全內嵌 script）
- GitHub Actions：加 HSTS? 不行，response headers 無法自訂 → CF 是唯一完整解

### 嚴謹級 100 分路線圖（campcool）
1. robots.txt 修正 + meta description 補齊（SEO）
2. pricing render-blocking 調查 + 內嵌 print CSS
3. LCP eager、首屏圖 preload、GA4 延遲初始化（Perf）
4. axe 違規全清（region→aria 分區、contrast→調色、landmark→main/nav、headings→order）
5. meta CSP + robots meta
6. webkit（playwright install webkit）390/360 驗證
7. E2E：playwright 測試 tab 切換/抽屜/計算器/LINE 跳轉/local-only → CI workflow
8. AI-README + 交付

### Jekyll 樣板污染（嚴謹級重大發現）
GitHub Pages 預設 Jekyll 引擎會把根目錄的 .md（pricing/services/areas/faq）自動轉成 .html，並注入 Jekyll 樣板（en-US lang、Jekyll CSS style.css + anchor-js render-blocking 5.8s、lang=en-US 與 zh-TW 站矛盾）。services.html/areas.html/faq.html 同樣被污染（200 OK），llms.txt 是 txt 不受影響。
**方案：加 .nojekyll 到 repo** → 停用 Jekyll，.md 不再被轉 .html，站內連結（pricing.md 直接引用）不受影響（index.html 39 行 link alternate 與 2468 行 footer 都指向 .md 原文）。副作用檢查：validate-site.mjs 對 pricing.md 有合約檢查（引用 .md）→ 確認 validate 不會壞。風險：若之前依賴 services.html 的舊連結 → 404，但站內無此連結且此為個人行銷站，可接受。
同時 pricing Lighthouse 的 render-blocking/meta-description 問題隨 .nojekyll 消失（.md 不再被 Lighthouse 抓 .html 版本？Lighthouse 測的是 pricing.html——若停用 Jekyll，pricing.html 404，LH 分數表需改測 pricing.md 或移除）。
**決策：加 .nojekyll，驗證 validate 通過，移除 pricing.html 從 LH 批測清單（改測 pricing.md 文本或直接移除）。**

### 效能診斷定稿（index）
LCP = h1.cc-hero-title 文字元素，TTFB 佔 LCP 的 83%（3393ms！注意：這是 headless 冷跑，含 DNS+TLS+CDN 冷快取，實機通常較快）。render delay 691ms = 主線程阻塞。所以 Perf 的核心戰場：**減少主線程阻塞時間（GA4/gtag 延遲初始化）+ TTFB（無法控，靠快取 warm）**。
具體動作：
1. gtag.js async 已加，但 gtag() 初始化立刻執行 + config 呼叫。改：`initGtag()` 延遲 3s 或 `requestIdleCallback`/首次互動後才載入 gtag.js 並補齊 config（轉換追蹤不能丟——需保留 line_click 即時性；方案：gtag.js 延遲載入但 dataLayer 照記，載入後一次性 flush config）
2. 移除/延遲 legacy-javascript：gtag.js 內 polyfill 屬 Google 控，無法修 → AI-README 記錄
3. reviews 頁 LCP 圖被 lazy → 首張 review 圖改 eager/fetchpriority=high
4. unused-javascript：主要來自 gtag + 站內 inline 腳本（validate 合約、LINE 追蹤）→ 站內腳本無法外移（無 build），可接受
5. dom-size 1156：index 全部 tabs 都在 DOM（display:none 切換）→ 架構性，改動大風險高，可接受但記錄
6. unminified-css 3KiB → 可微調
7. image-delivery 43KiB → 檢查哪些圖可再優化（webp 已做）
8. TTFB 990ms 快取 warm 後 ~200-400ms：可在報告說明
### .nojekyll 已推（commit 461417f）：pricing/services/areas .html 樣板污染已消除（404），faq.html 為 repo 本身 HTML 正常。validate 綠。

## 第九輪執行進度（嚴謹級修復）
### 已完成
1. ✅ .nojekyll（commit 461417f 已推）：pricing/services/areas .html 樣板污染消除。faq.html 是 repo 本身 HTML 不受影響。validate 綠。
2. ✅ gtag.js 延遲載入：index.html 手改 + scripts/_patch_gtag_defer.py 批次改 13 頁（btu-guide/camping-*/emergency-ac/faq/how-it-works/hsinchu/juz-400/reviews/sac-688/taichung/taipei）。模式：2.5s 定時或首次 pointerdown/keydown/scroll 後載入 gtag.js，dataLayer 先行記錄。validate 綠。
3. ✅ reviews.html 首張圖 fetchpriority=high（取代 loading=lazy）。

### 待做
4. axe 違規修復（index 4 tabs 重災區 + 其它頁）：region 147x、color-contrast 44x、landmark-one-main 8x、page-has-heading-one 3x、heading-order 3x、scrollable-region-focusable 2x → 待查具體元素
5. meta CSP：index.html head 加 `<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://www.google.com; img-src 'self' https: data:; style-src 'self' 'unsafe-inline'; connect-src 'self' https://campcool-line-bot.a0920077473.workers.dev https://www.google-analytics.com https://analytics.google.com https://www.googletagmanager.com; frame-ancestors 'none'">`（frame-ancestors meta 不支援，記錄限制）
6. webkit 跨瀏覽器驗證：playwright install webkit，390/360 截圖比對（小物 tabs 為主，之前已綠）
7. E2E：scripts/_e2e.py playwright 測試：tab 切換 4 個、抽屜開合、LINE 跳轉網址正確、計算器輸出、local-only booking、無障礙基本（documentElement lang、title）→ CI 加 workflow 步驟
8. validate + selftest + commit + push + CI
9. AI-README 更新（嚴謹級章節）
10. 其它倉庫嚴謹級審查：leakdoctor、0988145875、TITAN-STAR、campcool（後台？）等 → 先 clone 讀 AI-README
### 注意
- CI workflow 在 .github/workflows/site-check.yml（selftest + validate + config endpoint probe）
- 部署：GitHub Pages，約 1-2 分鐘後生效，CDN cache 600s（加 ?cb= 避開）
- 權限：gh CLI 已登入，repo campcool/leakdoctor 等
- 用戶最新指示：campcool 嚴謹級完成後更新 AI-README；然後用嚴謹級標準重新審查其他專案衝 100，標記在各 AI-README；最後給總報告
- 嚴謹級分數模型五維度：功能25/穩定安全25/可維護20/體驗15/成本15

### 無障礙修復方案定稿
1. **color-contrast**（各頁）：
   - .s（logo 副標，#059669 on 白 header #fff）：對比度不足（#059669/白 = 4.4:1 接近但可能因 font-size .66rem <14px 需 7:1 AA large text 門檻）→ 改 #047857（6.4:1）或加 font-size .75rem（≥14px 則 4.5:1 即可，#059669 = 4.4 仍不足 → 改 #03694d... 直接改 #047857 6.5:1 穩過）
   - .review-date #9ca3af on 白（4.3:1 不足需 4.5）→ #7f8a94 或 #84909b（4.6:1）→ 用 #6b7280（7:1）
   - .btn（各頁 LINE CTA，#06C755 白字 5.09:1 應過... 但 btu .line-btn 可能背景不同）→ 具體修法：把 .btn/.line-btn 前景改深（如 .btn a 白字 #fff 在 #06C755 上 5.1:1 過 AA；若 fail 代表字 <18px 需 4.5:1 仍過... axe 報 serious 可能是 hover 態或特定組合）→ 直接調高對比：LINE 綠改 #00a844（5.9:1）
   - .tag（rental 熱門：#059669 底白字 → 白字在 #059669 = 5.2:1 過... fail 原因可能是背景是漸層 hero？tag 實際在 hero 上背景 #059669 本身 → 需查）→ 安全修法：tag 文字改 #047857 或保持白字改底 #065f46
   - 決策：一律用可驗證深一階的色，不用猜：改後跑 axe 復測
2. **landmark-one-main / page-has-heading-one**（index 3 tabs + 其它）：index 的 cc-page 用 div，缺 main/nav；每頁加 <main> 包裹內容 + header 用 <header>；booking/wiki/fridge tabs 內的 h1 是 div 或 h2 → 確保每 tab 顯示區有 h1
3. **region**（147x）：hero 內非標題元素、proof-strip 等 → 對 cc-hero 加 role="banner"、cc-proof-strip 加 tabindex="-1" 或 aria-hidden（非互動裝飾則 aria-hidden），region 規則要求每個非標題內容需在 landmark/heading/role=region 內 → 修法：cc-hero 改為 <header> 包裹（role=banner），cc-proof-strip 加 aria-hidden（裝飾性），小卡片的 .ad-info 內的文字區加 role=region + aria-label？region 數量太大 → 更務實：把每張 ad-card 的品名 h3 提升（原本就是 h3？）→ 查後決定
4. **heading-order**（3x）：btu-guide .toc > h3 在 h1 前？或 h4 跳級 → 改為 h2
5. **scrollable-region-focusable**（2x）：cc-proof-strip（橫卷）與 btu 比較表 overflow-x div → 加 tabindex="0"

### 對比度檢查結果（scripts/_contrast_check.py 可複跑）
FAIL 組合：.logo .s(3.77)、.review-date(2.54)、camping-ac .btn #06a06f(3.35)、camping-fridge .btn #0284c7(4.10)、camping-power .btn #ea580c(3.56)、sac-688 .btn #059669(3.77)、btu .line-btn #06C755(2.26)、.tag 白字/#059669(3.77)、reviews banner a(2.26)
新配色（需複算 ≥4.5:1）：
- .btn 白字底改深綠 #047857(6.47)、深藍 #075985(6.73)、深橙 #c2410c(4.81)、btu line-btn #047857、reviews banner a 改深綠字或深綠底
- .tag 熱門：底改 #047857 白字 OK，或底白字改 #047857
- .review-date 已改 #6b7280 (4.83 PASS)
- .logo .s 已改 #047857 (5.48 PASS)
待辦：sed 批次改 .btn 色 → 複跑 _contrast_check.py 確認 → axe 復測
NOTE：btu .line-btn axe 報 fail 但 ratio 2.26 說明 axe 測的是線性漸層或該元素背景非純 #06C755（cta-block > a 無背景=白底綠字 2.26 也 fail → 需改字色 #047857）
reviews banner a：background:#fff;color:#059669;border:#10b981 → 白底綠字 2.26 → 改 color:#047857

## 第九輪：嚴謹級衝刺進度（2026-08-16）

### 基準數據（已完成）
- LH 全頁批測：/tmp/lh_out/（彙總曾輸出：SEO/BP 大多 100，效能 55-84，index 61）
- axe 基準：color-contrast 44、region 147、landmark-one-main 8、page-has-heading-one 3、heading-order 3、scrollable-region 2
- 安全標頭：GitHub Pages 無自訂標頭；Cloudflare 可加（DNS 在 GoDaddy，A 記錄直連 GitHub Pages IP）

### 已完成修復
1. .nojekyll 推送（461417f）：pricing/services/areas .html 被 Jekyll 樣板污染已消除（現在 404）
2. GA4 gtag.js 延遲初始化（2.5s 或首次互動）已套全部 14 頁
3. reviews 首圖 fetchpriority=high
4. index landmark：header role=banner、main#main-content、hero-badge role=status、proof-strip tabindex=0、tabs 三個 hero-title 改 h2 role=heading aria-level=1（實際應改回 h2 即可，role 冗餘）
5. 對比度全修（scripts/_contrast_check.py 14/15 PASS；ann-dot 裝飾非文字）：
   - .logo .s / .cc-logo-sub / .invite .s / .cta-block a / banner a / google-review-cta a → #047857
   - .review-date → #6b7280；.cc-price td.price → #047857；.cc-price td.desc → #6b7280
   - .cc-price .tag 底 → #047857（白字 5.48）
   - camping-ac .btn #047857、fridge #075985、power #c2410c、sac-688 #047857、btu line-btn/btn-line/btn-site #047857
   - btu .toc h3 → #047857
6. _a11y_scan.py 重寫：axe 改為 add_init_script 本地下載（assets/axe-core.min.js），避免 CDN 注入失敗
7. validate 20 項仍全綠

### 複測結果（/tmp/a11y_report2.json）
- region 162x / color-contrast 59x / landmark 8 / heading-one 3 / heading-order 3 / html-has-lang 3(areas/pricing/services.html 404 頁) / link-name 3(areas/pricing/services 404 logo 無 alt) / scrollable 2
- **注意**：areas/pricing/services.html 已 404，scan 對 404 回應頁掃出 violations 是雜訊 → PAGES 應移除這三項
- color-contrast 剩 59x：需查哪些仍 fail（可能是 index wiki/booking/fridge tab 隱藏內容？或 404 頁貢獻）
- 剩餘待修：landmark-one-main（各頁 main 標籤）、page-has-heading-one、heading-order（index .policy-block h4、.cc-notice h4）、btu .toc h3 前無 h2（改 h2）、scrollable（index proof-strip 已加 tabindex=0，btu #comparison overflow div 需 tabindex=0）
- html-has-lang/link-name 修完 404 問題（scan 移除該三頁）後應消失；線上真實 404 頁不需修

### 待辦
- [ ] 各頁補 <main> 與 nav/aria-current（index 已做 main；其它頁需 main 標籤）
- [ ] index 三個 h2 role=heading aria-level=1 → 簡化回 h2（隱藏？不行——visible 才有效）→ 保持 h2 即可，page-has-heading-one 要求至少一個 visible heading
- [ ] btu .toc > h3 → h2
- [ ] index .policy-block h4 / .cc-notice h4 → h3
- [ ] btu #comparison overflow div → tabindex=0
- [ ] scan PAGES 移除 areas/pricing/services（404）重測
- [ ] Lighthouse 復測（效能：GA defer 已做，還剩 render-blocking？index 61 目標 80+）
- [ ] 安全標頭：Cloudflare 免費方案加 CSP/HSTS/X-Frame → 需用戶改 DNS NS，列為交付建議（要用戶操作）
- [ ] webkit 跨瀏覽器驗證（playwright webkit）
- [ ] E2E 測試 + CI 門禁新增
- [ ] AI-README 更新 + commit/push/CI

### 其它倉庫審查（用戶要求擴展）
待 campcool 嚴謹級完成後：leakdoctor、0988145875、TITAN-STAR + 3 個未列名倉庫，用嚴謹級標準審 + 衝 100 分 + 各自 AI-README 標記。最後出總報告。

### 第四輪線上掃描結果（/tmp/a11y_report4.json）— 大幅改善
從基準到第四輪：region 144→7、color-contrast 44→27、landmark 5→0、heading-one 3→0、scrollable 2→0。heading-order 仍 3x 待修。
剩餘 27 個 color-contrast 待定位（可能含隱藏 tab 內容、scroll-to 後才渲染的區域、或線上部署的 pages 頁）。
待修 heading-order 3x：定位中（可能是 index wiki/booking 的 h2 role=heading aria-level=1 仍被算，或其它頁 h3→h4 跳級）。
commit 27ef406 已推送，CI 全綠，Pages 部署成功。
scan 已改寫入 /tmp/a11y_report4.json（注意 _a11y_scan.py 內寫死 report2.json，每次需 sed 改或直接改腳本）。

### 第四輪後殘留違規與修複方案（2026-08-16 晚）
| 違規 | 數量 | 位置 | 修複 |
|---|---|---|---|
| color-contrast | 27 | .hl .desc (#6b7280 on #dcfce7 淺綠底) | .cc-price tr.hl td.desc → #047857 或 #166534 |
| color-contrast | - | .step-no (#059669 上白/灰底？) | .step-no → #047857 |
| color-contrast | - | taipei/faq .banner a (#059669 on 白) | → #047857 |
| color-contrast | - | btu-guide line 397 inline background:#10b981;color:#fff（1.92:1 FAIL） | background → #047857 或 color → #022c22 |
| heading-order | 3 | index wiki/booking/fridge 內 h3 在 h2 role=heading aria-level=1 之後仍算跳級？實際上 .knowledge-banner>div>h3、.policy-block:nth-child(13)>h3、.cc-notice.r>h3——前序元素非 h1/h2 | index 三 tab 的 hero-title h2 role=heading aria-level=1 應改回真正 <h1>（只顯示主 tab），或用 h1 隱藏 |

heading-order 根因：index 每 tab 用 <h2 role="heading" aria-level="1"> 偽裝 h1，但 aria-level 不改變 DOM 層級，axe 按 DOM 順序算 h2→h3 跳級。正解：每 tab 保留一個真實 <h1>（其它 tab 的 h1 用 visually-hidden 樣式而非 role 偽裝）。
