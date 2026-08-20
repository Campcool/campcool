---
name: campcool-data-analysis
description: 資料分析與研究技能包。適用情境：商業報表、訂單/租賃/派工數據分析、市場調查、時序預測（庫存與需求）、統計檢驗、資料視覺化、合規準備時使用。整合 K-Dense-AI/scientific-agent-skills (⭐34k) 的 statistical-analysis、exploratory-data-analysis、statsmodels、scikit-learn、matplotlib、seaborn、polars、geopandas、market-research-reports、timesfm-forecasting、transformers、shap、dask、database-lookup、iso-standards-readiness、infographics。適用 Campcool 營運數據（campcool-bot 訂單、leakdoctor-bot 派工、Google Ads 投放成效）。
---

# Campcool 資料分析技能包

## 適用情境

- **營運報表**：營涼社訂單、機型出租率、缺貨分析；灰汰郎派工量、夥伴績效。
- **投放分析**：Google Ads 關鍵字成效、轉換成本（campcool、leakdoctor、0988145875 各站）。
- **市場研究**：新服務區評估、競品價格帶（接案與擴點決策）。
- **時序預測**：夏季租賃需求預測、庫存備貨（timesfm-forecasting）。
- **統計驗證**：A/B 測試（如新版首頁轉換率）、抽樣調查的可信度（statistical-power）。
- **合規準備**：ISO/稽核文件準備（iso-standards-readiness，TITAN-STAR 為廠內工具）。

## 分析鐵律

1. **先看原始資料再下結論**：用唯讀查詢或匯出檔做探索性分析（EDA），不憑印象或舊文件數字。
2. **單位與不確定性**：所有數字標註單位、期間、樣本數；異常值先查明原因再決定去留。
3. **可重現**：分析腳本化，輸出包含：圖、表、結論、下一步建議四件套。
4. **個資隔離**：分析檔案不放姓名+電話+地址同時出現；個資欄位在分析前先遮罩。

## 工具選擇

| 情境 | 工具 | 參考 |
|---|---|---|
| 中小資料集（<百萬列）報表 | pandas / polars | `references/polars.md` |
| 統計檢驗與建模 | statsmodels | `references/statsmodels.md` |
| 機器學習/分類預測 | scikit-learn | `references/scikit-learn.md` |
| 時序預測（需求/庫存） | timesfm-forecasting | `references/timesfm-forecasting.md` |
| 視覺化報表 | matplotlib / seaborn | `references/matplotlib.md`、`references/seaborn.md` |
| 地點分析（服務區、物流） | geopandas | `references/geopandas.md` |
| 市場調查報告 | market-research-reports | `references/market-research-reports.md` |
| 大資料集 | dask | `references/dask.md` |
| 資料庫查詢 | database-lookup | `references/database-lookup.md` |
| 模型解釋 | shap | `references/shap.md` |
| NLP/文件分類 | transformers | `references/transformers.md` |
| 稽核合規 | iso-standards-readiness | `references/iso-standards-readiness.md` |

## 標準流程

1. **定義問題與指標**：這次分析要回答什麼商業問題、成功指標是什麼。
2. **取數**：唯讀查詢（D1: `SELECT ...` 透過 wrangler）或匯出 CSV；記錄取數時間與範圍。
3. **EDA**：檢查缺失值、異常值、分佈；用 `references/exploratory-data-analysis.md` 流程。
4. **分析/建模**：依上表選工具；簡單問題先用統計檢驗，別動不動就上 ML。
5. **視覺化**：中文標籤用 Noto Sans CJK；圖表附標題、單位、資料期間。
6. **結論與行動**：結論必須可對應到具體行動（改價格、補庫存、調廣告預算），不寫空泛觀察。

## 參考文件

所有 `references/*.md` 為 K-Dense-AI ⭐34k 原版技能全文，含完整使用指令與範例；大檔依各 skill 內部的 grep 指引按需讀取相關段落。
