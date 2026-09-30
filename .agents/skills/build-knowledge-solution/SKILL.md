---
name: build-knowledge-solution
description: 依指定 Knowledge Release 產生業務 Skill、知識庫或 SOP，檢查知識涵蓋、工具需求、來源映射與實際行為。
---

# 建立衍生產品

讀 [solution-contract.md](references/solution-contract.md)。沿用已指明產品與範圍，不強制重選；未要求產品不自行啟動。

1. 讀 release、handbook、gaps，填 solutions/<name>/target.yaml，指明任務 IDs、輸入輸出、工具、人工判斷點與排除範圍。
2. coverage <release> <target> 檢查 dependency closure。業務缺口回 elicit/model，runtime 缺失處理技術條件。
3. 封裝實際 artifact。Agent Skill 使用 skill-creator（若有）；分開 workflow、references、必要 scripts。advisory Skill 不要求工具，但 target 必須明確。
4. traceability.yaml 記 release ID/digest、coverage_status、accepted_task_refs、每項 behavior 的 knowledge_refs 和 tests。工具/觸發/顯示設計標 implementation，不當 business rule。
5. 執行 artifact 的 happy-path、stop/exception 測試，記 expected/actual、method、evidence/result 於 validation.md 和 traceability.tests。verify-solution 僅查追溯，不能取代行為測試。
6. 交付使用方式、範圍、限制和驗證層級。完整通過才 state.complete、completion=knowledge-and-solution。
