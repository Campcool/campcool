# Campcool AI-Skills

本目錄是專案群的可更新工作基準。現有程式碼、交接與參考全文用於理解現況，技術選型與流程依目前任務、官方資訊及驗證結果調整，不以歷史文件或固定版本作永久標準。

## 技能路由

| 技能 | 用途 |
|---|---|
| [維運與除錯](01-ops-debug/SKILL.md) | 根因、外部服務、Pages／Worker 與真實流程驗證 |
| [開發流程](02-dev-workflow/SKILL.md) | 計畫、Git、技術變更、審查與產物一致性 |
| [文件產出](03-doc-production/SKILL.md) | 文字與二進位文件、報告、試算表、簡報、渲染與重算 |
| [資料分析](04-data-analysis/SKILL.md) | 資料品質、分母、事件口徑、租借／詢價／維修分析 |
| [技術查核與版本更新](TECHNOLOGY-REVIEW.md) | 官方版本、LTS、相容性、升級驗證與來源 |

涉及技術或版本更新時先讀 TECHNOLOGY-REVIEW，再選相關技能。2026-10-03 已修正四套路由，共 41 份 reference 的連結對回現有檔名。

## 使用方式

可由支援 SKILL.md 的工具直接讀取本目錄，或複製四個技能目錄及共同的 TECHNOLOGY-REVIEW.md 至同一個根目錄。跨資料夾連結依這個佈局解析；單獨匯入某個 SKILL.md 時，需一併提供其 references 與共同文件。

上游 reference 可能提到額外程式或素材；若未在目前 repo／環境找到，不代表本技能帶有該工具。工作前查核實際可用能力。

## 與專案的對應

- 網站維運：campcool、灰汰郎、潔淨坊、潔美淨、華兒園。
- 工廠分析／離線工具：TITAN-STAR。
- Bot：campcool-bot、leakdoctor-bot 等完整倉庫名稱與權限先實際核對，不能以舊文件或前台 URL 取代後端讀取。
- React 組合模式以潔淨坊與華兒園的正式入口為主；campcool 根目錄 JSX 是歷史參考。

## 來源與更新

既有 references 來自 obra/superpowers、anthropics/skills、K-Dense-AI/scientific-agent-skills、vercel-labs/agent-skills 的先前收錄快照。保留來源與有用內容，按任務查核官方新版；本次未宣稱 41 份全文已全部同步。

[205 技能掃描清冊](catalog/205-skills-full-list.md) 是歷史盤點，不是當日可用技能總數。原「星數 ≥30,000」與「49 個入選」不再作技能品質或實際檔案數的標準；以用途、來源、版本、可執行性與驗證結果選用。

## 變更紀錄

- 2026-10-03：改為可更新的基準；加入官方技術查核、LTS／Current 與相容性流程；修正 41 份 reference 路徑、部署名稱假設、文字／二進位格式驗證、正式產物與轉換口徑。只修改技能／交接文件，未升級網站相依。
- 2026-08-20：建立四分類與歷史上游技能快照。
