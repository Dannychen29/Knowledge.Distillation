---
name: bu-knowledge-workflow
description: 開始或續作部門／專家業務知識蒸餾，協調 CommonKADS 模型、ACTA 訪談、知識驗證與可選的 Skill 或知識庫產出。
---

# 部門知識蒸餾入口

先讀 [workflow.md](references/workflow.md)。repo 根目錄是此檔向上四層；所有 scripts、schemas、runs、knowledge 路徑均相對 repo root。

1. 新工作依既有材料選 source_route：guided-interview（零材料）、document-first（文件／範本）、map-first（訪談後流程圖）；混合材料以最有結構且相關的來源先讀，不要求使用者做技術選擇。由 `$frame-knowledge-engagement` 設定範圍並建立 run。既有工作先讀 state.yaml 與 engagement.yaml，沿 next_action 續作。多個 run 且無法判定時才詢問使用者。
2. 預設交付 Knowledge Release。只有使用者要求衍生產品才進入 `$build-knowledge-solution`；既有授權及已回答問題沿用。
3. 按 frame → elicit ↔ model → validate → release 路徑執行；每階段寫出 artifact、更新 state 後繼續可執行工作。需要人的資料或知識確認時，列出具體缺口及目前成果連結。
4. 所有 substantive claim 保留 evidence、scope、expert attribution、未解項目。AI 不能自行填寫 participant confirmation 或聲稱案例實測成功。
5. 來源更新先查 library 既有 IDs。修改發布內容時，從 base release 建立新 draft，保留穩定 ID；舊 release 不覆寫。

新材料／錯誤修正按原因回流：來源不足 → elicit；推理或模型錯誤 → model；產品實作錯誤 → build。精準標記受影響 ID 與衍生產品，不必整個重跑。

MVP 不要求正式 owner 核准、審批委員會、資料庫或 RAG 服務。交付時說明已完成範圍、未解缺口、知識驗證層級及衍生產品是否經測試。
