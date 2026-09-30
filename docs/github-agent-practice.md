# GitHub 實作參考：Codex／Claude Code 如何蒸餾知識

本頁補足 [架構說明](architecture.md) 的操作依據。2026-09-30 查核 GitHub repository metadata 與原始 Skill／流程檔。Star 是**整個 repository** 的採用度線索，不能推定單一 Skill 的品質，也不能證明本專案能蒸餾出正確的部門知識。

## Reference 篩選規則

主要實作參考須同時通過：①與「來源／訪談 → 知識整理 → 可查證產物」至少一段直接相關；②能讀到實際指令、輸入、輸出及核對方式，而非只有 README 宣傳；③有可信的維護者或足夠的社群採用訊號，並檢查近期維護狀態。這次以約 **1,000 stars 以上**作為主要引用的採用度門檻；門檻是縮小搜尋範圍的工作規則，不是品質分數。最後仍須用本部門的真實案例檢驗來源可追溯、例外是否完整，以及接手者能否使用。

僅引用**實際採用的做法**，不因 repository 高星就搬入它的整套架構。不同用途分開判斷：Anthropic 提供業務研究的證據整理操作，Distilly 提供多來源擷取的操作，OpenAI Cookbook 提供 Codex 跨次執行的檔案管理操作。三者都沒有驗證本 repo 的完整 Knowledge Release 流程。

## 原始實作與本專案對照

| 原始檔與 repository 採用訊號 | 原始檔中的可執行做法 | 本 repo 借用之處與界線 |
| --- | --- | --- |
| Anthropic [synthesize-research Skill](https://github.com/anthropics/knowledge-work-plugins/blob/main/product-management/skills/synthesize-research/SKILL.md)；[customer-research Skill](https://github.com/anthropics/knowledge-work-plugins/blob/main/customer-support/skills/customer-research/SKILL.md)。[repository](https://github.com/anthropics/knowledge-work-plugins)：25,887 stars、3,046 forks，2026-09-29 有 push。 | 讀訪談、逐字稿、回饋及其他來源；逐來源擷取觀察、行為與脈絡；依來源標示證據、信心、矛盾和未解問題；研究完成後建議寫回知識庫。 | `elicit`／`model` 保存來源及候選判斷，`gaps` 保存未知，`validate` 核對版本。這兩個 Skill 面向產品與客服研究，未提供本 repo 的部門任務模型或 Knowledge Release 驗收。 |
| [Distilly 的 Claude Code Skill](https://github.com/titanwings/distilly/blob/main/SKILL.md)。[repository](https://github.com/titanwings/distilly)：25,155 stars、2,173 forks，2026-09-22 有 push。 | 由對話、文件、連結、上傳檔案匯入個人工作材料；生成工作及人物檔案，追加材料與對話修正時更新版本。 | `input/` 接收多種材料，`evidence/` 保留來源位置，後續修正開新版本。其核心產品是「同事／個人 Skill」，且容許只憑少量手動資訊生成；這不符合部門重要知識須有證據及確認的發布條件。 |
| [OpenAI Cookbook 的 Codex 工作流程](https://github.com/openai/openai-cookbook/blob/main/examples/codex/iterating-development-workflows-with-codex.md)。[repository](https://github.com/openai/openai-cookbook)：76,276 stars、12,898 forks，2026-09-29 有 push。 | 以 repo 內可讀檔保存目標、分階段進度、執行脈絡與驗證結果，讓 Codex 下一次接續工作。 | 沿用既有 `engagement.yaml` 記目的、`state.yaml` 記 next_action、`review/` 記確認與案例；不複製其軟體開發用的整套 harness。這是 Codex 操作持久化的參考，不能證明業務知識整理方法有效。 |

數字來自查核當日的 GitHub repository metadata；`pushed_at` 只能表示 repository 近期有 push，**不代表表中 Skill 最近更新**。各 repository 的 stars 也不能當作部門知識準確率。原表其餘五個專案已退出主要引用：[claude-code-recipes](https://github.com/sgharlow/claude-code-recipes) 388 stars、[data-context-layer-studio](https://github.com/nimrodfisher/data-context-layer-studio) 1、[claude-code-automation](https://github.com/elmisi/claude-code-automation) 0、[codex-howto](https://github.com/Phelan164/codex-howto) 10、[crucible](https://github.com/jkitchin/crucible) 12。它們的片段可作探索線索，但不再支撐架構主張。

對這些做法的最小歸納是：Agent **讀來源 → 問未明之處 → 保存證據 → 整理候選知識 → 請業務人員核對 → 發布並接收修正**。這是本專案的設計組合，不是任何單一高星專案已驗證的完整流程。現有 Codex Skills 與本機檔案能實作這條資料流；效果仍須靠真實部門試點測量。

## 在本 repo 逐步執行

入口是 [bu-knowledge-workflow](../.agents/skills/bu-knowledge-workflow/SKILL.md)。Codex 有材料時先讀 `knowledge/<department>/<domain>/index.yaml`（若存在）及所有提供的材料；無材料時建空 run，從具體事件訪談。每輪更新 `state.yaml` 的 next_action。四個階段 Skill 分別是 [frame](../.agents/skills/frame-knowledge-engagement/SKILL.md)、[elicit](../.agents/skills/elicit-business-knowledge/SKILL.md)、[model](../.agents/skills/model-business-knowledge/SKILL.md)、[validate](../.agents/skills/validate-knowledge-release/SKILL.md)。

| Codex 做什麼 | 讀入 | 寫出 | 檢查點 |
| --- | --- | --- | --- |
| 定一個重要任務 | 目的、接手者、材料、舊版索引 | `engagement.yaml`；原始材料／引用進 `input/` | 目的、優先理由與範圍清楚 |
| 讀來源並追問 | `input/`、具體事件、現有 gaps | `evidence/` 的紀錄；`draft/evidence-index.yaml` 與 `gaps.yaml` | 候選判斷能指出來源位置；未知具名 |
| 整理知識 | 證據、候選主張、舊版知識 | `draft/` 的 domain、inference、task 等及手冊草稿 | 重要判斷保留線索、理由、反例、範圍與 evidence ID |
| 請人核對 | 手冊、來源、案例 | `review/` 原始回覆；`draft/review.yaml` 摘要 | 目前版本確認；核心知識有通過案例 |
| 發布供使用 | 通過檢查的 draft | `knowledge/<department>/<domain>/releases/<id>/`、index | 手冊、coverage、缺口及來源可查；修正回新 draft |

例如受訪者說「上次因某欄位異常而停止」：Codex 追問當時看見的值、判斷理由、其他可能原因與交接動作；在 `evidence/` 記原話與案例位置，在 `inference.yaml` 記有依據的判斷，在 `gaps.yaml` 留未回答的條件，再用另一個案例核對。若來源只能證明欄位存在，理由仍是缺口。這是目前 Skill 應執行的操作順序，尚無真實部門案例跑通。

## 用現有合成資料檢查檔案流向

[source.md](../examples/synthetic/source.md) 的 S1 是虛構訪談，S2 是事先寫好的案例答案。現有 [合成示範](../examples/synthetic/README.md) 以它建立以下連結：

```text
examples/synthetic/source.md#S1
  → runs/synthetic-demo/draft/evidence-index.yaml 的 EVD-001
  → runs/synthetic-demo/draft/inference.yaml 的 INF-001
  → runs/synthetic-demo/draft/cases.yaml 的 CASE-001／CASE-002
  → runs/synthetic-demo/draft/review.yaml 的合成確認與案例結果
  → runs/synthetic-demo/knowledge/synthetic/toy/releases/toy-v1/handbook.md
```

在 repo 根目錄檢查目前示範檔的資料契約：

```powershell
.venv/Scripts/python.exe scripts/knowledge_workflow.py validate runs/synthetic-demo/draft
.venv/Scripts/python.exe scripts/knowledge_workflow.py validate runs/synthetic-demo/draft --release
```

確認與案例結果由示範腳本預設填入，**沒有 AI 訪談、真人確認或接手者使用**。真實試點須由 Codex 實際完成上述步驟、保留原始證據，特別檢查是否漏掉重要例外、過度概括專家一次經驗，以及手冊能否讓接手者看懂。
