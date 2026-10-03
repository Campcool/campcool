---
name: campcool-doc-production
description: 為 Campcool 專案群產出可查核的文件、試算表、簡報、技術報告與互動文件；使用實際存在的格式工具與模板，按文字或二進位格式驗證，更新過時操作指引。
---

# Campcool 文件產出

## 基準與更新原則

現有程式碼、交接文件與本技能參考快照是理解現況的基準，不是永久技術標準。技術選型、版本、測試方法與過去的流程假設應依目前任務、最新官方證據及實際相容性重新評估；不要只因舊文件寫過，就阻止已授權的改進。

區分技術建議、目前實作與營運事實。價格、服務區、客戶紀錄、園所資訊等用可核對來源，不能因技術更新自行編造。

涉及版本或架構調整時，先讀 [技術查核與版本更新流程](../TECHNOLOGY-REVIEW.md)。其中版本表是 2026-10-03 的查核快照，執行時重新核對，不作永遠的最低版本。

## 產出流程

1. 明確受眾、目的、資料來源與需要的格式。模板作結構與風格起點，依目前指示調整。
2. 查核原始資料、版本與時間；歷史快照、推測、待確認與已實測分開，不能把舊狀態直接搬成最新結論。
3. 選執行環境真正具備的工具。參考全文可能提到上游 scripts 或 assets，未隨此 repo 打包的工具不能稱為「本技能內建」。
4. 產出後按格式驗證內容、數字、字型、排版、連結與開啟／重算行為；金額與重要計算以獨立方法核對。
5. 交付可直接閱讀的成品及必要來源；同步有效交接摘要與剩餘缺口。

## 格式與驗證

| 格式 | 建議處理與驗證 |
|---|---|
| Markdown／TXT／JSON／YAML／一般 CSV | 預設 UTF-8 無 BOM；實際 decode、parse、欄位／連結與必要 round-trip。若收件端明確需要 BOM 或其他編碼，依需求輸出並標示 |
| DOCX | 合法 OOXML／ZIP，用相容文件工具開啟；檢查段落、樣式、表格與分頁，必要時轉 PDF 預覽 |
| XLSX | 合法 OOXML／ZIP，用試算表工具開啟與重算；檢查公式、日期、欄寬、凍結窗格與加總。公式儲存不代表已有正確計算快取 |
| PPTX | 合法 OOXML／ZIP，渲染所有投影片；檢查字型、裁切、重疊、可讀性與圖表來源 |
| PDF | 驗證 PDF 結構、抽取文字及逐頁渲染；中文字型嵌入、跨頁表頭與長表格 |
| 網頁／互動文件 | 用實際瀏覽器檢查手機與桌機、互動、鍵盤、資料來源、必要 HTTP／API |

DOCX、XLSX、PPTX、PDF 是二進位格式，不能用 open(..., encoding="utf-8") 判斷有效與否。「UTF-8 無 BOM」不是所有檔案的通用鐵律。

## 文件品質

- 先寫具體問題與結論，數字附單位、期間、來源與分母。
- 明確區分基準、建議與驗收標準。舊報告分數或技能模板不是永久判準。
- 中文使用可用字型並實際驗證渲染；版本或工具範例更新依 TECHNOLOGY-REVIEW。
- 只收集必要資料；對外文件與分析事件避免完整姓名、電話、地址或訊息的非必要曝光。
- xlsx 公式與常數分開；pptx 每頁聚焦一個訊息；技術圖與文件需能對回目前實作。
- 不宣稱完成沒有跑過的渲染、重算、真機或正式環境驗證。

## 參考快照

- [K-Dense-AI_scientific-agent-skills__markdown-mermaid-writing.md](references/K-Dense-AI_scientific-agent-skills__markdown-mermaid-writing.md)
- [anthropics_skills__brand-guidelines.md](references/anthropics_skills__brand-guidelines.md)
- [anthropics_skills__doc-coauthoring.md](references/anthropics_skills__doc-coauthoring.md)
- [anthropics_skills__docx.md](references/anthropics_skills__docx.md)
- [anthropics_skills__frontend-design.md](references/anthropics_skills__frontend-design.md)
- [anthropics_skills__internal-comms.md](references/anthropics_skills__internal-comms.md)
- [anthropics_skills__pdf.md](references/anthropics_skills__pdf.md)
- [anthropics_skills__pptx.md](references/anthropics_skills__pptx.md)
- [anthropics_skills__theme-factory.md](references/anthropics_skills__theme-factory.md)
- [anthropics_skills__web-artifacts-builder.md](references/anthropics_skills__web-artifacts-builder.md)
- [anthropics_skills__xlsx.md](references/anthropics_skills__xlsx.md)
