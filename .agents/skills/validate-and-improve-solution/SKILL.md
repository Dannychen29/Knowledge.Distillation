---
name: validate-and-improve-solution
description: 以具代表性的 case 驗證 BU solution、記錄 human feedback，並將每個 defect 導回最小的 workflow stage 進行 correction 與 retest。
---

# 驗證並改善 Solution

僅在 `run-state.yaml.current_stage` 為 `validation` 時使用此 skill。閱讀 [feedback-contract.md](../bu-knowledge-workflow/references/feedback-contract.md)、[run-state-contract.md](../bu-knowledge-workflow/references/run-state-contract.md) 與 [workflow-contract.md](../bu-knowledge-workflow/references/workflow-contract.md)。僅在將此 workflow 與 native Codex 比較時，才閱讀 [value-measurement-contract.md](../bu-knowledge-workflow/references/value-measurement-contract.md)。

確認最小的 representative test case、expected result 與具名 BU reviewer。在 authorization 與 source data 允許時，測試實際 source-to-output path；若僅能做 structural-only test，應明確標記。將每項 result 記錄於 `evaluation/`，每個 defect 記錄於 `feedback/`。

對每個 failure，先分類、寫入其 `feedback/iteration-log.csv` record、更新 state，並且僅使指定的 downstream artifact 失效，然後才可做任何變更：

- 缺少、矛盾或未驗證的 source fact → `$conduct-bu-interview`；
- 不完整的 workflow、decision、mapping 或 acceptance condition → `$distill-bu-knowledge`；
- 已確認 knowledge 的 implementation 有誤 → `$build-bu-solution`；
- 無法取得的 permission、system 或 data → visible external blocker。

correction 後，retest failed case 與受影響的 downstream case。不得僅因 syntax、mock 或結構有效的 file 通過，就宣告 business validation 通過。

BU reviewer 可隨時提供直接的 correction instruction。變更 artifact 前，先將其轉為 stable issue record，分類出最小的 affected stage、回報 affected ID 與 retest scope，然後再 iterate。若請求變更 solution target、納入的 process scope、source availability、business rule 或 acceptance condition，則不是單純的 implementation fix，必須導回 upstream。

acceptance 後，寫入 `evaluation/validation-record.md`，設定 `status: complete`、`current_stage: complete`、`next_skill: null` 與 `next_action: null`。若有 external dependency，設定 `status: blocked` 並寫明精確的 resume condition。最後提供 validation level、known limitation、unresolved blocker 與下一個 human action。
