---
name: bu-knowledge-workflow
description: 協調完整的 BU knowledge-distillation 流程，從 intake 到已驗證 solution，並具備明確的 stage gate、持久 state 與精準 correction loop。
---

# BU Knowledge 工作流程

將此技能作為新的或續作的端到端 business-knowledge 請求入口。此技能與所有 child skill 必須維持 domain-neutral。開始前閱讀 [run-state-contract.md](references/run-state-contract.md) 與 [workflow-contract.md](references/workflow-contract.md)。

## 開始或續作

1. 從使用者提供的路徑或目前對話找出 active run。對於新請求，呼叫 `$conduct-bu-interview`；該技能會在確認 intake mode 與必要材料後建立 run 及其 initial state。
2. 對於既有 run，先讀取 `run-state.yaml`。不得重問已確認的問題，或重複已完成的 stage。
3. 只執行 state 中記錄的 `next_skill` 與 `next_action`。若 state 缺失或與 artifact 不一致，應依 artifact 修復 state 並記錄原因後再繼續。

## 不可違反的協調規則

- stage 僅能在寫出 exit artifact、通過 exit gate、設定 `current_stage`、`next_skill` 與 `next_action` 後完成，接著必須立即呼叫所記錄的下一個 skill，或提出唯一已記錄的 BU decision。
- 當 `next_action` 存在時，不得僅以 stage summary 結束。human-decision gate 只能等待 state 中記錄的確切 decision 或最小缺失 evidence。
- 不得從原始 interview evidence 直接跳至 solution building；不得從尚未選定的 option 開始 build；不得未經 validation 便由 build 跳至 completion。
- 當 correction 回溯至上游時，只依 correction record 使受影響的 downstream artifact 失效，接著遵循產生的 `next_skill`。
- case-specific content 僅屬於 active run；不得複製到這些可重用 skill 或 reference。

## 標準路徑

`conduct-bu-interview -> distill-bu-knowledge -> build-bu-solution -> validate-and-improve-solution`

確切允許的 transition、artifact schema、stop condition 與 resume behavior 定義於 [workflow-contract.md](references/workflow-contract.md)。只有在比較不同 approach 或報告 benefit 時，才讀取 [value-measurement-contract.md](references/value-measurement-contract.md)。
