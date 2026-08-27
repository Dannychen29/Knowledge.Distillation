---
name: conduct-bu-interview
description: 開始或續作 BU knowledge-distillation 的 interview stage，收集符合契約的 intake package，並僅在通過 exit gate 後交接。
---

# 進行 BU Interview

開始前閱讀共用的 [intake contract](../bu-knowledge-workflow/references/intake-contract.md)、[run-state contract](../bu-knowledge-workflow/references/run-state-contract.md) 與 [workflow contract](../bu-knowledge-workflow/references/workflow-contract.md)。

對於新 run，先請 BU 使用者選擇 `codex-led` 或 `ba-assisted`。確認選擇與初始必要材料後，以 `../bu-knowledge-workflow/scripts/new-run.ps1` 建立 run；它會建立 `current_stage: interview` 的 `run-state.yaml`。

對於 `codex-led`，第一個問題先完整盤點 BU 可用資源（系統、URL／存取方式、範本、資料匯出、樣本、權限與限制），後續一次提出一個聚焦問題。對於 `ba-assisted`，先盤點 BA 訪談產出的流程圖、既有文件範本、系統／網站、可下載資料與其他佐證，再只要求具名的 material gap；不得把尚未需要的資源變成硬性要求。對 `.drawio` 流程圖，必須先以 UTF-8 位元組安全方式解析 XML；使用 `../bu-knowledge-workflow/scripts/extract-drawio-evidence.py` 輸出可追溯的 page、cell 與 edge evidence。不得因終端機文字亂碼而推論來源圖檔內容有問題；若流程關係會影響規則，還須以圖形化檢視驗證。若流程圖或其他證據提及資料庫／網站，但使用者尚未提供 URL 或可存取方式，主動索取該最小必要資訊。若使用者提供可存取的網站作為資料來源，必須使用 `openCLI` 依流程圖核對該網站的實際頁面、欄位與文件可得性，再形成 mapping 或進入 distillation；未提供網站、且流程未提及網站時，不得將網站探索視為必要條件。不得將 PRD 或 implementation spec 視為 intake 前置材料：它們是後續 `distill-bu-knowledge` 根據 intake 產生的 artifact。將來源存放於 `input/`，working intake package 存放於 `output/`。

若缺少 intake item，設定 `status: awaiting_bu`、`next_skill: conduct-bu-interview`，並提出一個明確的 `open_item` 問題。不得交接或詢問 solution 問題。

僅當 intake contract 通過時，寫入 `output/intake-package.md`，設定 `current_stage: distillation`、`next_skill: distill-bu-knowledge` 與 `next_action: create_implementation_spec`，然後立即呼叫 `$distill-bu-knowledge`。不得在此技能選擇或建置 solution。
