---
name: campcool-data-analysis
description: 分析 Campcool 專案群的租借、清潔詢價、派工、投放與工廠維修資料，先查來源、粒度、分母與資料品質；工具和模型依目前證據選擇，保留可重現的計算與限制。
---

# Campcool 資料分析

## 基準與更新原則

現有程式碼、交接文件與本技能參考快照是理解現況的基準，不是永久技術標準。技術選型、版本、測試方法與過去的流程假設應依目前任務、最新官方證據及實際相容性重新評估；不要只因舊文件寫過，就阻止已授權的改進。

區分技術建議、目前實作與營運事實。價格、服務區、客戶紀錄、園所資訊等用可核對來源，不能因技術更新自行編造。

涉及版本或架構調整時，先讀 [技術查核與版本更新流程](../TECHNOLOGY-REVIEW.md)。其中版本表是 2026-10-03 的查核快照，執行時重新核對，不作永遠的最低版本。

## 分析流程

1. 定義要回答的營運問題、資料來源、期間、單位、粒度與指標。沒有資料時交付量測計畫，不捏造成效。
2. 唯讀取數，記錄來源、時間與版本；先查缺值、重複、join、更新時效、樣本與分母是否一致。
3. 用可重現腳本或查詢計算，數字附來源、分母、期間與不確定性。抽樣與全量要分清。
4. 先用最簡單且可驗證的方法回答問題；預測先比較季節性 naive 等基線，再考慮統計模型或 ML，不能僅因 reference 收錄 TimesFM 就預設使用。
5. 圖表與報告揭露口徑、資料缺口、反例與可執行建議；不要只交付工具列表或不受資料支持的百分比目標。

## 不同業務的指標

| 場景 | 指標與注意事項 |
|---|---|
| campcool 租借 | 訪客→方案／機型→LINE 意圖→有效租借詢問→實際訂租；出租率需明確可出租庫存與期間 |
| 潔美淨／潔淨坊清潔 | 聯絡意圖、有效詢價、報價、成交與服務完成分開；本機整理或開 LINE 不等於收到詢價 |
| 灰汰郎 | 前台成功建立 leadId、Bot 收件、廠商派工與完工分開；同線索／重試／多個事件要去重 |
| 華兒園 | 參觀意圖、實際預約、到訪、入園分開；核定容量不等於剩餘招生名額 |
| TITAN-STAR | 維修件數、整新台數、返修與工時需各自母體；未取得正式分母前，FPY／DPPM 代理標示與限制不能移除 |

GA4／Ads 的 Primary 或 Secondary 是帳號設定，不能從前台函式名推斷。照片入口、空白跳 LINE、訊息整理與正式收件應使用不同意義的事件，不把同一批意圖重複計算成成交。

## 工具與驗證

- 依資料規模、欄位與環境選 pandas／Polars、SQL、statsmodels 等；百萬列不是唯一分界，還要考慮記憶體、型別與運算。
- 新工具或模型 API 依官方版本文件查核；固定相依與資料版本，更新後用同資料／同口徑比較。
- 小樣本 A/B 不宣稱顯著提升；時間序列驗證不得讓未來資料洩漏至訓練。
- 分析事件與公開成品只保留必要非個資欄位；客戶資料用適當遮罩與權限。
- 未取得來源欄位，不能由程式憑空補製造日期、工時、交易分母或客戶事實。
- 圖表先確認數字與意義，再檢查單位、比例、色彩與中文渲染。

## 參考快照

- [K-Dense-AI_scientific-agent-skills__dask.md](references/K-Dense-AI_scientific-agent-skills__dask.md)
- [K-Dense-AI_scientific-agent-skills__database-lookup.md](references/K-Dense-AI_scientific-agent-skills__database-lookup.md)
- [K-Dense-AI_scientific-agent-skills__exploratory-data-analysis.md](references/K-Dense-AI_scientific-agent-skills__exploratory-data-analysis.md)
- [K-Dense-AI_scientific-agent-skills__geopandas.md](references/K-Dense-AI_scientific-agent-skills__geopandas.md)
- [K-Dense-AI_scientific-agent-skills__infographics.md](references/K-Dense-AI_scientific-agent-skills__infographics.md)
- [K-Dense-AI_scientific-agent-skills__iso-standards-readiness.md](references/K-Dense-AI_scientific-agent-skills__iso-standards-readiness.md)
- [K-Dense-AI_scientific-agent-skills__market-research-reports.md](references/K-Dense-AI_scientific-agent-skills__market-research-reports.md)
- [K-Dense-AI_scientific-agent-skills__matplotlib.md](references/K-Dense-AI_scientific-agent-skills__matplotlib.md)
- [K-Dense-AI_scientific-agent-skills__polars.md](references/K-Dense-AI_scientific-agent-skills__polars.md)
- [K-Dense-AI_scientific-agent-skills__scikit-learn.md](references/K-Dense-AI_scientific-agent-skills__scikit-learn.md)
- [K-Dense-AI_scientific-agent-skills__seaborn.md](references/K-Dense-AI_scientific-agent-skills__seaborn.md)
- [K-Dense-AI_scientific-agent-skills__shap.md](references/K-Dense-AI_scientific-agent-skills__shap.md)
- [K-Dense-AI_scientific-agent-skills__statistical-analysis.md](references/K-Dense-AI_scientific-agent-skills__statistical-analysis.md)
- [K-Dense-AI_scientific-agent-skills__statsmodels.md](references/K-Dense-AI_scientific-agent-skills__statsmodels.md)
- [K-Dense-AI_scientific-agent-skills__timesfm-forecasting.md](references/K-Dense-AI_scientific-agent-skills__timesfm-forecasting.md)
- [K-Dense-AI_scientific-agent-skills__transformers.md](references/K-Dense-AI_scientific-agent-skills__transformers.md)
