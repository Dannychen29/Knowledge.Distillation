---
name: build-bu-solution
description: 對符合 contract 的 BU specification 執行 solution-selection 與 solution-build gate，產出可用 artifact 及必要的 validation handoff。
---

# 建置 BU Solution

閱讀 [solution-contract.md](../bu-knowledge-workflow/references/solution-contract.md)、[run-state-contract.md](../bu-knowledge-workflow/references/run-state-contract.md) 與 [workflow-contract.md](../bu-knowledge-workflow/references/workflow-contract.md)，再從 `output/` 讀取目前的 normalized PRD 與 implementation spec。

當 `current_stage: solution_target_confirmation` 時，寫入 `solution/target-confirmation.md`。內容必須說明請求的 business outcome、納入與排除的 process、目前實際可用的 source system/data、已知 data gap、預期 output、human control 與 acceptance target。僅提出一個 confirmation decision。尤其是，較廣泛的 process diagram 不會自動使其中每個 process 都成為已選 solution 的一部分；例如僅建置 risk rating 時，CDD/EDD 仍可排除。設定 `status: awaiting_bu`、`next_skill: build-bu-solution` 與 `next_action: confirm_solution_target`。在確認前不得提出 option 或進行 build。

當 `current_stage: solution_selection` 時，以白話在 `solution/solution-options.md` 寫入兩或三個實質不同的 option。說明可用 artifact、BU user 的使用方式、limitation、human control 與 trade-off。設定 `status: awaiting_bu`、`next_skill: build-bu-solution`、`next_action: select_solution_option`，並僅提出一個 selection question。未選定前不得 build。

使用者選定 option 後，寫入 `solution/solution-brief.md`，設定 `current_stage: solution_build`，並在同一任務中建置所選 option。solution 可以是 skill、script、prompt、knowledge base 或其他合適 artifact；不得強制固定類型。不得要求 BU user 執行 PowerShell 或撰寫程式碼。納入一個具代表性的 happy-path，以及 invalid、exception 或 stop-path case，並標示 expected result。若為 workbook output，須完成相關 workbook-build contract 定義的 extract-template → mapping artifact → final workbook path；僅當該契約明確允許時才可使用受控 OOXML／ZIP fallback。

solution contract 的 build gate 通過後，寫入 `solution/test-cases.md`，設定 `current_stage: validation`、`next_skill: validate-and-improve-solution` 與 `next_action: run_validation_case_<id>`；接著立即呼叫 `$validate-and-improve-solution`。working artifact 必須保持可編輯，Git commit、branch 與 release version 交由使用者控制。
