---
name: distill-bu-knowledge
description: 將符合 contract 的 BU intake package 轉為可追溯的 implementation spec，接著推進下一個 solution-selection decision，不得跳過 workflow gate。
---

# 萃取 BU Knowledge

僅在 `run-state.yaml.current_stage` 為 `distillation` 時使用此 skill。閱讀 [spec-contract.md](../bu-knowledge-workflow/references/spec-contract.md)、[run-state-contract.md](../bu-knowledge-workflow/references/run-state-contract.md) 與 [workflow-contract.md](../bu-knowledge-workflow/references/workflow-contract.md)。僅在已識別的 evidence gap 需要時，才從 `../bu-knowledge-workflow/references/adapters/` 閱讀相關 adapter。

在該 run 的 `output/` 資料夾建立一份目前版本、可編輯的 `normalized-prd.md`、canonical `implementation-spec.yaml` 與人類可讀的 `implementation-spec.md`。保留 source reference，並以 input、action、output、owner 或 system、已知 validation，以及（當 evidence 存在時）精確 navigation、UI action、download/export artifact 與 extracted field，描述每一個重要 workflow step。明確記錄 field mapping、decision rule、僅能由人判斷的內容及 scenario-based acceptance case。decision、exception 與 unresolved item 必須明確保留。

若無法建立重要的 input、output、decision rule、exception、mapping 或 acceptance case，僅索取最小的缺失 evidence。此時設定 `status: awaiting_bu`、`next_skill: distill-bu-knowledge`，並在 `open_item` 寫入確切問題；尚不得提出 solution。

在請 BU participant 確認 distilled knowledge 前，必須於對話中提供目前 `output/normalized-prd.md`、`output/implementation-spec.yaml` 與 `output/implementation-spec.md` 的可點擊連結，以及精簡的已確認規則、未解項目與 evidence coverage 摘要。不得只要求確認而未提供可供審閱的 artifact。

specification contract 通過後，寫入全部三個 spec artifact，設定 `current_stage: solution_target_confirmation`、`next_skill: build-bu-solution` 與 `next_action: confirm_solution_target`；接著立即呼叫 `$build-bu-solution`。下一個 skill 必須先提出且僅提出一個最終 target-confirmation decision；確認前不得提供 solution option 或 build。
