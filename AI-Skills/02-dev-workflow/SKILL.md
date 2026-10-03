---
name: campcool-dev-workflow
description: 為 Campcool 專案群規劃、實作、審查與驗證多步驟技術變更，依真實倉庫與正式產物選工作流程；技術文件與歷史技能作基準，允許有證據的更新。
---

# Campcool 開發流程

## 基準與更新原則

現有程式碼、交接文件與本技能參考快照是理解現況的基準，不是永久技術標準。技術選型、版本、測試方法與過去的流程假設應依目前任務、最新官方證據及實際相容性重新評估；不要只因舊文件寫過，就阻止已授權的改進。

區分技術建議、目前實作與營運事實。價格、服務區、客戶紀錄、園所資訊等用可核對來源，不能因技術更新自行編造。

涉及版本或架構調整時，先讀 [技術查核與版本更新流程](../TECHNOLOGY-REVIEW.md)。其中版本表是 2026-10-03 的查核快照，執行時重新核對，不作永遠的最低版本。

## 計畫與執行

- 先確認任務目的、範圍、現有 git head、實際入口與正式產物，再列可交付的最小單元。
- 每項列具體檔案、依賴、預期行為與必要驗證；用目前程式查核舊待辦，已完成的不重做。
- 先完成已授權工作；證據改變時更新計畫與原因。不要將歷史技能的抽象核准步驟當作新的阻擋條件。
- 修改技術前依 TECHNOLOGY-REVIEW 做官方版本、安全與相容性查核；在隔離分支或 worktree 形成可回退的差異。
- 先提交與範圍相符的變更；文件／流程、依賴升級與產品行為變更分開，便於驗證與回退。
- 複雜邏輯或已知缺陷用必要回歸測試；簡單文件與可逆小改動直接查核，不一律要求 TDD。

## Git 與部署

- 多人／多工具工作前及推送前重新確認遠端 head，避免以舊副本覆蓋新的工作；不要 force push 來掩蓋差異。
- Worktree 用於需要隔離或同時維護多分支的任務，不是所有任務的前置條件。
- 依目前使用者指示選直推、分支或 PR。既有直推模式可以保留並補自動門禁；PR 不應無故增加人工批准。
- 讀 workflow 的真實觸發、權限與 needs，不把 typecheck→test→migrations→deploy 或 pr-check.yml 當成所有專案共同結構。靜態站不憑空添加 migration。
- 本機驗證與 CI 應針對會發布的同一產物；發布、實際可用、接單完成分開記錄。
- 有 AI-README／AI-HANDOFF 的倉庫同步更新有效摘要、進度及待辦；過期技術決策明確以新證據取代，不只在長文件尾端堆疊互相矛盾的狀態。

## 審查

說明觸發問題、結果行為、必要測試與剩餘缺口。分開事實錯誤、實作取捨和風格偏好；有爭議先用程式或官方資料查核，避免套用過時模式。

## 同時讀取與委派

獨立倉庫／檔案可並行讀取並標記各自 SHA。修改、推送及資料遷移依其相依順序執行。同時讀取不等於委派多個代理；只有本次授權與工作環境允許時才採用子代理，並明確分工及整合驗收。

## 正式技術映射

- campcool、灰汰郎、潔美淨：原生 HTML/CSS/JS；先保留靜態可讀內容，依效益決定是否模組化或升級架構。
- 潔淨坊：React／Vite；華兒園：Next 靜態匯出＋vinext 預覽。React 與組合模式對這些實際入口套用。
- campcool 根目錄 JSX 是舊設計參考；改正式畫面不能只改這些檔案。
- TITAN-STAR：Excel parser／analysis、離線 bundle、月報匯入與 localStorage 有各自契約；不要暗示 localStorage 是共享資料庫。
- Bot 倉庫必須真正能讀取才可盤點其部署／資料邏輯，從前台 URL 或舊交接不能推斷後台現況。

## 參考快照

- [obra_superpowers__dispatching-parallel-agents.md](references/obra_superpowers__dispatching-parallel-agents.md)
- [obra_superpowers__executing-plans.md](references/obra_superpowers__executing-plans.md)
- [obra_superpowers__finishing-a-development-branch.md](references/obra_superpowers__finishing-a-development-branch.md)
- [obra_superpowers__receiving-code-review.md](references/obra_superpowers__receiving-code-review.md)
- [obra_superpowers__requesting-code-review.md](references/obra_superpowers__requesting-code-review.md)
- [obra_superpowers__subagent-driven-development.md](references/obra_superpowers__subagent-driven-development.md)
- [obra_superpowers__using-git-worktrees.md](references/obra_superpowers__using-git-worktrees.md)
- [obra_superpowers__writing-plans.md](references/obra_superpowers__writing-plans.md)
- [vercel-labs_agent-skills__composition-patterns.md](references/vercel-labs_agent-skills__composition-patterns.md)
