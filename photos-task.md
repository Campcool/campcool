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
