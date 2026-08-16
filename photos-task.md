# 其它小物商品照補齊任務（2026-08-16，用戶要求）

## 實際缺貨（實測 6 處 emoji 佔位，非 7）
AI-README 說缺 7 張，但實測缺 6 張（C40 冰箱已有 addon-fridge-c40.webp）：

| 行號 | 品項 | data-price | 卡片類 | 擬檔名 |
|---|---|---|---|---|
| 2196 | 動力延長線（綠）5M | 100 | a-power | addon-ext-cord-5m.webp |
| 2208 | 動力延長線（綠）10M | 150 | a-power | addon-ext-cord-10m.webp |
| 2231 | 五米黃光燈條 | 200 | a-light | addon-lamp-5m.webp |
| 2243 | 十米黃光燈條 | 300 | a-light | addon-lamp-10m.webp |
| 2325 | 製冰機 | 300 | a-fun | addon-ice-maker.webp |
| 2337 | 渦輪扇 | 300 | a-fun（品牌 ADAM OUTDOOR） | addon-fan.webp |

## 現有 8 張（不可動）
addon-fridge-c40 / addon-tarp-58 / addon-tarp-butterfly / addon-blackdog-dome / addon-bluetti-mini / addon-tent-lamp / addon-firepit-basic / addon-firepit-qingluan / addon-projector（實測 9 張，8 張+1?——AI-README 說 8 張）

## 規格（沿用既有）
- 320×320 webp（Pillow quality 82）
- img 帶 width=320 height=320 loading=lazy；alt = 品項名
- 裁掉賣場行銷字樣（AI-README 明定：裁切時移除賣場行銷字樣）
- 型號標示維持「待老闆確認」：渦輪扇不標確切型號、製冰機不標型號；品項名與頁面合約一致

## 注意
- 綠色延長線是台灣露營常用「動力延長線」（綠色粗線、附防雨帽）
- 黃光燈條 = 露營帳篷 LED 燈條（暖黃光）
- 製冰機 = 小型製冰機（100W）
- 渦輪扇 = ADAM OUTDOOR 品牌（多款差異大，選外觀代表性的便攜渦輪風扇）
- 品牌事實約束：不得自造型號、瓦數

## 交付
- git add assets/addon-*.webp + index.html 6 處替換
- validate + selftest → commit push → CI 確認
- AI-README 更新「待老闆確認」表（商品照欄更新為：缺 0 張；剩 7 項標示型號/尺寸待確認）

## 搜尋結果評估

### 動力延長線（綠）— 已搜
- 圖1 GEARit RV 30A（美式 TT-30 插頭，不符台灣品項）✗
- 圖2 VEVOR 橘色線盤 ✗（顏色不符）
- 圖3 DEWENWILS 綠線 43FT 3-outlet（美式，但有分接頭造型）△
- 圖4/7 SYNCO 新格 軍綠動力延長線 10米（PChome，含「新格牌/一擴三插/最新安規/MIT/贈收納袋」大量行銷字 ✗，但照片本體乾淨可裁）
- 圖5 Woods 2466 綠色 3-outlet 白底（乾淨、無行銷字、造型即「台灣露營動力延長線」典型樣貌）✓✓ 候選
- 圖6 Coupang 軍綠四座動力線（4.5米軍綠色標籤、有 Coupang 水印 ✗）
結論：延長線用圖5（Woods 2466 白底綠色三孔延長線，造型與台灣露營動力延長線一致）

### 黃光燈條 — 已搜
- 圖5 LIFECODE 12米暖光防水戶外燈條（台灣品牌、帳內懸掛實拍、黃光氛圍佳、左下角有「客廳帳使用 12米燈條」小標籤=需裁）✓ 候選（裁小標籤）
- 圖3 Tuff Stuff USB LED strip 白底但 LED 燈珠裸露、造型專業但較像「材料」△
結論：燈條用圖5（LIFECODE 實景暖光），裁左下角標籤

### 製冰機 — 已搜
- 圖4 CROWNFUL 白色桌上型製冰機（純白底、無行銷字、造型典型）✓ 候選
- 圖3 Igloo 白底 ✓ 備選
- 圖1 Frigidaire 白底 ✓ 備選
- 圖2/8 PChome 台灣通路（米白/金框款）△ 圖8 有行銷字需裁
結論：製冰機用圖4（CROWNFUL 白色款，最乾淨）；不標型號（AI-README 已列型號待確認）

### 渦輪扇（ADAM OUTDOOR）— 已搜
- 圖2 ADAMOUTDOOR 桌上型迷你渦輪扇（沙色、白底、品牌 logo 細小且位於機身）✓✓ 最佳候選
- 圖3 ADFN-UTB100（含型號標籤貼紙在機身，裁掉或選其他）△
- 圖1 黑款有 ADAMOUTDOOR 大 logo 浮水印 ✗
結論：渦輪扇用圖2（ADAMOUTDOOR 沙色桌上型渦輪扇，最接近品項「ADAM OUTDOOR 渦輪扇」且圖面乾淨）

### 候選圖檔路徑（/home/ubuntu/upload/search_images/）
- 延長線：TDK4mbJBpEg9.jpeg（Woods 綠色 3-outlet，白底）
- 燈條：062bvymWmlZE.jpg（LIFECODE 12米暖光，裁左下標籤）
- 製冰機：8XDRok0sMKBA.jpg（CROWNFUL 白色）
- 渦輪扇：GHqlAnRij6jC.jpg（ADAMOUTDOOR 沙色）

### 五米 vs 十米燈條
5M 與 10M 是同一品項不同長度，共用同圖會誤導。策略：5M 用燈條特寫（Tuff Stuff kKRBEQXk9BL3.jpg 或 COB strip），10M 用實景暖光圖。5M 選 Tuff Stuff USB LED strip（白底專業照，5ft≈1.5m 但表徵「燈條」品類）——更佳：5M 用 h8j0f5DDdl1M.jpg（COB 5ft 暖白，白底特寫）。

### 延長線最終定案
- 5M（addon-ext-cord-5m）：TDK4mbJBpEg9.jpeg（Woods 綠色 3-outlet，白底乾淨，短線直線造型適合 5M 表徵）
- 10M（addon-ext-cord-10m）：YW6AjxwfpCPt.jpg（SYNCO 軍綠 10M 圓捲造型，含品牌角標需裁掉左上 SYNCO logo）
- 燈條 5M：h8j0f5DDdl1M.jpg（COB 暖白特寫白底）
- 燈條 10M：062bvymWmlZE.jpg（LIFECODE 實景，裁左下「客廳帳使用 12米燈條」小標籤）
- 製冰機：8XDRok0sMKBA.jpg（CROWNFUL 白）
- 渦輪扇：GHqlAnRij6jC.jpg（ADAMOUTDOOR 沙色）

### 圖面檢查結果
- TDK4mbJBpEg9（5M 延長線）：白底乾淨無行銷字 ✓ 直接用
- YW6AjxwfpCPt（10M 延長線）：白底乾淨，插頭有規格刻字（AX-286 15A 125V，產品規格非行銷字）✓ 直接用
- h8j0f5DDdl1M（原定 5M 燈條）：是廣告圖「Powered by USB & Battery」+四格圖示 ✗ 棄用；換 kKRBEQXk9BL3.jpg（Tuff Stuff 白底特寫）

### 最終候選圖檢查紀錄（已查看原圖）
| 品項 | 檔 | 尺寸 | 行銷字 | 裁切 |
|---|---|---|---|---|
| 5M 延長線 | /home/ubuntu/upload/search_images/TDK4mbJBpEg9.jpeg | 1800×1800 | 無 | 居中方形裁切即可 |
| 10M 延長線 | /home/ubuntu/upload/search_images/YW6AjxwfpCPt.jpg | 1000×1000 | 無（插頭規格刻字=產品規格，OK） | 直接用 |
| 5M 燈條 | /home/ubuntu/upload/search_images/kKRBEQXk9BL3.jpg | 512×512 | 無（Tuff Stuff 白底特寫） | 直接用 |
| 10M 燈條 | /home/ubuntu/upload/search_images/062bvymWmlZE.jpg | 1080×900 | 左下角「客廳帳使用 12米燈條」灰標籤 | 裁掉左下約 0-18% 高 × 0-22% 寬 |
| 製冰機 | /home/ubuntu/upload/search_images/8XDRok0sMKBA.jpg | 894×964 | 無（CROWNFUL 白底） | 居中方形裁切 |
| 渦輪扇 | /home/ubuntu/upload/search_images/GHqlAnRij6jC.jpg | 800×800 | 無（ADAMOUTDOOR 沙色，機身 logo 小） | 直接用 |

### 處理規格
- 輸出 assets/addon-ext-cord-5m.webp、addon-ext-cord-10m.webp、addon-lamp-5m.webp、addon-lamp-10m.webp、addon-ice-maker.webp、addon-fan.webp
- 320×320、webp quality 82、白底補邊（center-crop 保持主體）
- index.html 6 處 <span class="ad-ph-ico">🔌/💡/🧊/🌀</span> 替換為 <img src=... alt=品項名 width=320 height=320 loading=lazy>

## 用戶糾正：動力線應為 ADAM 軍綠色（2026-08-16）
替換兩張：5WlyZSBh6Tgu.jpeg（ADAM 軍綠近距特寫、白底、插頭紅燈清楚、無行銷字）用於 5M；ZdfWBuLoB6oa.jpg 為廣告圖（含「軍風戶外延長動力線/10M/通電指示燈」字樣✗，需大幅裁切中心圓盤區）。
實際策略：5M 用 5WlyZSBh6Tgu.jpeg 直接置中裁；10M 用 ZdfWBuLoB6oa.jpg 裁中心圓盤（約 x 5%-70%、y 30%-80% 的線盤主體），避開周圍行銷字。
檔名不變：addon-ext-cord-5m.webp / addon-ext-cord-10m.webp（原地覆蓋）。

## 狀態快照（防壓縮遺失，2026-08-16）
已完成的步驟與結果：
1. 6 張 320×320 webp 已產生於 assets/：addon-ext-cord-5m、addon-ext-cord-10m、addon-lamp-5m、addon-lamp-10m、addon-ice-maker、addon-fan
2. index.html 6 處 emoji 佔位已替換為 img（_patch_addon_photos.py 成功，verify 6 img refs、0 殘留）
3. 第一輪 commit 0d38460 已 push（當時用 Woods 綠線與 CROWNFUL 製冰機）
4. 用戶糾正：動力線要 ADAM 軍綠色 → 已換圖重處理
   - 5M：5WlyZSBh6Tgu.jpeg（ADAM 軍綠特寫白底，乾淨）✓
   - 10M：ZdfWBuLoB6oa.jpg（原廣告圖裁中心線盤）——裁框迭代中，最新 (0.02, 0.31, 0.60, 0.84)，待視覺確認
   - 製冰機：用戶說「隨便弄一台即可」，CROWNFUL 白款保留
5. 殘餘待辦：10M 裁框最終確認 → git add 6 張 webp + index.html → commit push → CI 確認 → 更新 AI-README（商品照待老闆確認表：改為延長線/渦輪扇已用 ADAM 款、製冰機型號仍待確認）→ 交付
6. validate + selftest 已在本輪驗證通過（ALL-GREEN），commit 後 CI 應全綠
7. 交付訊息語言：繁體中文，簡潔幽默，附對照圖
8. 10M 裁框最終：(0.02, 0.345, 0.515, 0.825)，右上角黑點為插頭本體材質非文字，可接受，已定稿

## 燈條替換（逐浪天下，2026-08-16 第三輪）
用戶糾正：燈條要「逐浪天下」（逐露天下 CAMP WORLD）的 5M/10M 款。

### 候選圖評估
| 檔 | 來源 | 評估 |
|---|---|---|
| jnBDDsem5UGO.webp (640×640) | momo 逐露天下極光燈條10米套餐 | 黑底產品照：收納盤+盤繞燈條（無字，可用，裁左半主體）★ 10M |
| RHl9wNOh1mUj.webp (640×640) | momo 逐露天下極光燈條5米套餐 | 同款黑底產品照 ★ 5M |
| 3V7zbJvrELUD.jpg (640×640) | PChome 逐露天下極光 5米 | 含「專利燈條 極光」行銷字，不可直接用 |
| 7eTMrqAzpdZA.jpg (800×800) | 逐露天下極光LED燈條 | 帳篷實景+「全台最亮燈條」標籤，裁字麻煩 |
| TSxSHXPVDVM2.jpg (1024×1024) | 逐露天下黑焰LED燈條 | 「黑焰」另一系列，與頁面已用款不同 |
| GCUbWWieX22X.jpg / fhgOOYJgOT2k.jpg | 非逐露天下，淘汰 |

### 決策
- 5M ← RHl9wNOh1mUj.webp；10M ← jnBDDsem5UGO.webp（同系列黑底官方照，無行銷字）
- 處理：裁右側留白或縮放置中、320×320 webp、檔名 addon-lamp-5m.webp / addon-lamp-10m.webp 覆蓋
- 頁面引用已是這兩檔名，只需覆蓋圖檔 → validate + selftest → commit push → CI

### 修正（第一輪裁框錯誤）
RHl9wNOh1mUj（5M）全圖左半是乾淨燈條特寫（三段橫條），右半與頂部是廣告文字。可行：裁 (0.0, 0.42, 0.52, 0.62) 取中段黑焰燈條？太窄。更好的：裁左半直條 (0.0, 0.12, 0.34, 0.88) 得 217×486 直條燈條特寫。
jnBDDsem5UGO（10M）是晶片廣告圖，完全無產品 → 改用 7eTMrqAzpdZA（逐露天下極光 800×800，帳篷實景，裁頂部黃色標籤）或 TSxSHXPVDVM2 黑焰系列。
待辦：重新裁 → 視覺確認 → 覆蓋 → commit。

確認：jnBDDsem5UGO 全圖為「CAMP WORLD 逐露天下」晶片廣告，無燈條主體，放棄。
10M 改用 7eTMrqAzpdZA.jpg（800×800，逐露天下官方極光燈條實景圖，頂部有「全台最亮燈條」黃色標籤需裁除）。

### 燈條替換完成狀態（2026-08-16）
- 5M ← RHl9wNOh1mUj.webp 裁 (0,0.31,0.34,0.88)，三段燈條特寫黑底，乾淨定稿
- 10M ← 7eTMrqAzpdZA.jpg 裁 (0,0.30,1,1)，逐露天下極光帳篷黃光實景，乾淨定稿
- 兩張均為逐露天下（CAMP WORLD）官方圖，符合用戶指定品牌
- 檔名 addon-lamp-5m.webp / addon-lamp-10m.webp 直接覆蓋，頁面引用無需改
- 剩餘：commit push → CI → AI-README 更新（燈條品牌註記）→ 交付
- AI-README 商品照段落現文：「五米／十米黃光燈條」+「燈條與製冰機圖取自網路商品圖，正式營業前建議以自家庫存品照片替換」——更新品牌名為逐露天下
