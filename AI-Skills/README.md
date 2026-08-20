# Campcool AI-Skills 總目錄

> 本目錄存放 Campcool 專屬的 AI Agent Skills 分類技能包，來源為 GitHub 上星數最高的 AI Agent Skills 倉庫（2026-08-20 掃描），依 Campcool 業務需求（維運+FAE+自動化接案+小型 SaaS+租賃出租）篩選分類。

## 篩選標準

以倉庫星數 **≥ 30,000** 為門檻，並篩選與 Campcool 業務相關度 ≥ 4/5 的技能，共 **49 個**入選，分類存放於四個技能包。

| 倉庫 | 星數 | 貢獻技能數 |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | ⭐274,450 | 14（開發流程、除錯、程式碼審查） |
| [anthropics/skills](https://github.com/anthropics/skills) | ⭐170,537 | 12（docx/pdf/xlsx/pptx、webapp-testing、前端） |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | ⭐33,948 | 21（資料分析、統計、市場研究、時序預測） |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | ⭐30,236 | 5（React 前端、部署、組合模式） |

另有 156 個科學專用技能（生物/化學/藥學）與業務無關，未納入。完整 205 個技能掃描明細見 `catalog/205-skills-full-list.md`。

## 目錄結構

```
AI-Skills/
├── README.md                      ← 本文件
├── 01-ops-debug/                  維運與除錯（campcool-bot / leakdoctor-bot / 各站維運）
├── 02-dev-workflow/               開發流程（計畫、審查、Git、平行子任務）
├── 03-doc-production/             文件產出（docx/pdf/xlsx/pptx、品牌與內部文件）
├── 04-data-analysis/              資料分析（統計、報表、預測、市場研究）
└── catalog/                       掃描清冊（205 技能完整清單、星數、分類、相關度）
```

## 使用方式

每個技能包為 Manus Agent Skill 格式（SKILL.md + references/）。可兩種方式使用：

1. **Manus 技能**：將 SKILL.md 匯入 Manus「我的技能」（Add to My Skills），後續任務會自動觸發。
2. **本地 D 槽**：clone 本倉庫後把四個資料夾複製到 `D:\AI-Skill\` 對應分類，提供給其他支援 SKILL.md 的 AI 工具（Claude Code 等）讀取。

## 與 Campcool 專案的對應

| 專案 | 主要套用技能包 |
|---|---|
| campcool-bot（LINE Bot 正式營運） | 01-ops-debug、02-dev-workflow |
| leakdoctor-bot（灰汰郎派工） | 01-ops-debug、02-dev-workflow、04-data-analysis |
| campcool / leakdoctor / 0988145875（靜態網站） | 01-ops-debug、03-doc-production、04-data-analysis |
| TITAN-STAR（廠內工具） | 01-ops-debug、03-doc-production |
| blossomkids / campcool-website | 02-dev-workflow、03-doc-production |

## 變更紀錄

- 2026-08-20：建立 AI-Skills 目錄，初版四分類技能包（49 個入選技能、156 個未納入）
