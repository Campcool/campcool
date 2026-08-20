---
name: campcool-doc-production
description: 文件產出技能包。適用情境：需要產生 docx（合約、SOP、報告）、pdf（提案、對帳單）、xlsx（帳務、報表、庫存）、pptx（簡報、提案）、品牌文案、內部溝通文件、網頁產物或技術文件時使用。整合 anthropics/skills (⭐170k) 的 docx、pdf、pptx、xlsx、frontend-design、web-artifacts-builder、theme-factory、internal-comms、doc-coauthoring、brand-guidelines 與 K-Dense-AI (⭐34k) 的 markdown-mermaid-writing、infographics。支援 UTF-8 無 BOM 的中文文件規範。
---

# Campcool 文件產出技能包

## 格式選擇指南

| 格式 | 用途 | 對應參考 |
|---|---|---|
| docx | 合約、SOP、訓練文件、維修記錄模板（TITAN-STAR 有既用模板） | `references/docx.md` |
| pdf | 對外提案、報價單、對帳單、客戶文件 | `references/pdf.md` |
| xlsx | 帳務、報表、庫存、維修記錄（campcool-bot 訂單、leakdoctor-bot 派工） | `references/xlsx.md` |
| pptx | 提案簡報、月報、培訓 | `references/pptx.md` |
| 網頁產物 | 快速互動文件、內部工具頁 | `references/frontend-design.md`、`web-artifacts-builder.md` |
| 內部文件 | 交接文件、內部通訊、品牌文案 | `references/internal-comms.md`、`doc-coauthoring.md`、`brand-guidelines.md` |
| 技術文件 | 附 Mermaid 流程圖的文件（SOP、架構說明） | `references/markdown-mermaid-writing.md` |

## 鐵律：中文文件規範

- 所有文件存檔必須 **UTF-8、無 BOM**。曾發生 AI 在 Big5/Windows 環境存檔導致中文變亂碼。
- 交付前驗證：`python3 -c "open('file',encoding='utf-8').read()"` 不報錯。
- xlsx 檔名與內容涉及客戶資料時，只放必要欄位，不放入完整個資（姓名+電話+地址不同時出現於同一非內部文件）。

## 標準產出流程

1. **確認需求與受眾**：這份文件給誰看、用來做什麼決定。
2. **選格式與模板**：依上表選格式；有既有模板（如 TITAN-STAR 維修記錄模板）就遵循其結構。
3. **產出**：依對應參考文件的官方流程；xlsx 用本技能內建 Excel 生成器、docx/pdf/pptx 依 Anthropic 官方腳本流程。
4. **驗證**：實際開啟檔案檢查中文渲染、表格欄位、數字加總；對帳務類文件用獨立計算二次驗算。
5. **交接**：文件放入對應倉庫的 docs/ 或資料區，並同步更新 AI-README 的進度紀錄。

## 各格式操作要點

**docx**：用參考文件附帶的腳本產生；段落、表格、樣式依官方模板；交付前轉 PDF 預覽一次確認版面。

**pdf**：先 Markdown 排版再轉；表格超過一頁時確認表頭重複；中文字型用 Noto Sans CJK。

**xlsx**：欄寬與凍結窗格必設；數字格式（貨幣 NT$、日期）統一；大報表用本技能內建 Excel 生成器；公式與常數分開列，避免硬編碼。

**pptx**：先定大綱與訊息層級再動版面；每頁一個重點；數據頁附上資料來源與日期。

**內部文件/交接文件**：先寫「一句話目標」與「目前公開狀態」再寫細節（Campcool AI-HANDOFF 慣例）；交接文件必須包含目前狀態快照、已知陷阱、下一步。

## 參考文件

- `references/docx.md`、`references/pdf.md`、`references/pptx.md`、`references/xlsx.md` — Anthropic 官方格式產出（⭐170k 原文）
- `references/frontend-design.md`、`references/web-artifacts-builder.md`、`references/theme-factory.md` — 網頁產物
- `references/internal-comms.md`、`references/doc-coauthoring.md`、`references/brand-guidelines.md` — 內部溝通與品牌文件
- `references/markdown-mermaid-writing.md`、`references/infographics.md` — 技術文件與資訊圖表
