# 舊版到 MVP 的改造紀錄

2026-09-30。基準為 a742dca；這次改造保留 Git 歷史，因此移除的舊指令可由該 commit 查看。沒有將任何舊 run 或業務規則自動轉成已確認知識。

| 舊版 | 新版處理 |
| --- | --- |
| conduct-bu-interview | 由 frame + elicit 取代，加入 ACTA，不要求 PRD |
| distill-bu-knowledge | 由 model + validate-release 取代，產出 CommonKADS 模型 |
| build-bu-solution | 由 build-knowledge-solution 取代，增加 closure coverage |
| validate-and-improve-solution | 知識驗證進 validate-release；產品驗證進 build |
| implementation-spec、normalized-prd 為必交成果 | 只在選用產品需要時產生 |
| solution build 為完成必要条件 | knowledge-only 可以完成 |
| stage contracts 中的特定業務條款 | 移除；共用規則保持領域中立 |
| new-run.ps1、validate-agent-structure.ps1 | 由 scripts/knowledge_workflow.py 的 init/check-repo/validate 取代 |
| drawio extractor | 保留原位，改由 elicit adapter 引用 |
| 四個媒體 workers | 保留可發現 Skill 目錄，更新 caller、run 路徑及回傳契約 |
| 媒體 analysis/knowledge.json | 保留為中間證據格式，需映射到 canonical YAML |

刻意沒有建立 `.agents/skills/adapters/` 這個假 Skill：文件與 browser adapter 在 elicit/references/adapters.md；媒體仍為四個可呼叫 worker Skill。這讓來源路由清楚，也不破壞既有 worker 的相對 scripts 路徑。

若需使用外部保存的舊 run：先讓 Codex 唯讀盤點來源、模型與確認紀錄，再建新 draft；缺少新契約的資料標 gap，重新取得目前版本確認。不可只改副檔名或把舊 implementation-spec 標成已驗證 release。
