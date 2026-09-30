# Workflow 與資料位置

閱讀 repo root 的 [architecture.md](../../../../docs/architecture.md) 了解模型；格式以 [data-contract.md](../../../../docs/data-contract.md) 與 schemas 為準。

若要對照 Codex／Claude Code repo 的實際訪談、證據、建模與核對操作，讀 [GitHub Agent 實作參考](../../../../docs/github-agent-practice.md)。該頁提供操作樣例與原始專案連結；原始專案的其他工具、目錄與發布條件不自動成為本工作流程要求。

主線為 1 個入口＋4 個階段 Skill；release 與 validate 由同一 Skill 完成。build 是選用應用，四個媒體 Skill 是 elicit 按需使用的工具。它們不代表每次都要執行十個階段。

`runs/<id>/` 是 engagement；draft 使用 release 格式。input 保留來源；evidence 放抽取、轉錄及觀察；review 保存確認、案例測試和變更原始紀錄，draft/review.yaml 保存引用這些紀錄的確認／案例摘要。完整讀寫流向見 [DATA FLOW](../../../../docs/architecture.md#各階段的-data-flow)。

| stage | Skill | 離開條件 | 下一步 |
| --- | --- | --- | --- |
| frame | frame-knowledge-engagement | 範圍確認，知識密集任務、來源與參與者已盤點 | elicit |
| elicit | elicit-business-knowledge | 足以建模一個任務，material gap 明列 | model |
| model | model-business-knowledge | 模型引用可解析，衝突及缺口明列 | validate；缺來源回 elicit |
| validate | validate-knowledge-release | 參與者確認版本，所有 critical 物件有通過案例 | release；修正回 model/elicit |
| release | validate-knowledge-release | publish 建立 snapshot、handbook、coverage、index | complete 或 derive |
| derive | build-knowledge-solution | coverage 可用，產品存在且目標案例已驗證 | complete；缺知識回 elicit/model |
| complete | 入口 | knowledge-only 或 knowledge-and-solution 完成 | 有新工作才重啟 |

status 使用 active、awaiting_input、blocked、complete。next_action 是具體下一步，complete 時為 null。pending 記錄具體問題及資料位置。state 只控制進度，模型才是業務內容來源。

資料不足不必阻止所有建模；同一任務可反覆 elicit/model。無內容的 section 用空清單，manifest.empty_sections 寫理由，至少 context、domain、task 有內容。

review.confirmation 記錄參與者、時間、對話/檔案位置、model_digest。digest 涵蓋模型、來源、gap、範圍，內容改變後舊確認失效。scenario-tested 必須對應 review scenario 的 pass，不能只靠格式驗證。

修正時在 review/changes.md 記下原因、affected_ids、修改及重測範圍。已發布 release 不覆寫；新版本完成前，向使用者說明受影響衍生物限制。source 不在本機時記 unavailable；口述不冒充視覺操作證據。發布不等於 Git commit、push 或部署。
