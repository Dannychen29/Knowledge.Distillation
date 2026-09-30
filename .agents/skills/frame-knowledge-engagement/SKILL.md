---
name: frame-knowledge-engagement
description: 為部門知識蒸餾界定流程或能力範圍，支援從部門或資深員工出發，建立任務、角色、來源與知識缺口地圖。
---

# 建立蒸餾範圍

讀 [工作流程](../bu-knowledge-workflow/references/workflow.md)。利用已提供資訊，不強制選技術模式或提供 PRD。

1. 確定目的、使用者、department/domain、納入及排除範圍。材料盤點方式見 [entry-routes.md](references/entry-routes.md)；將所有現有材料類型並列記入 engagement.source_types，無材料時用空清單，從訪談開始。別把材料類型與 department-first/expert-first 的知識視角混為一談；專家視角先問擅長任務、困難判斷與代表案例。
2. 查 knowledge/<department>/<domain>/index.yaml（若存在）。建立 context：流程、角色／專家、系統、來源及候選任務。確認同名概念是否同義。
3. 依判斷難度、錯誤影響、知識集中程度、材料可得性，選一個 bounded task 優先蒸餾；記排序理由，不要求數字評分。
4. 以 repo root 的 scripts/knowledge_workflow.py init 建立 run；有材料時每種加一個 `--source-type <type>`，例如 `--source-type form --source-type process-map`。補完 engagement.yaml；state 記錄是否已要求 solution、base_release。原始材料以副本或可追溯引用放 input。後續新材料也更新 source_types 與 resources。
5. 提供範圍摘要讓使用者修正；已有確認則引用對話。設定 stage=elicit，交 `$elicit-business-knowledge`。

缺少系統存取不自動阻止概念或判斷蒸餾；只有目標要求實際操作時才索取相關資料。
