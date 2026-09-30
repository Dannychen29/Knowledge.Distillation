# Workflow 與資料位置

閱讀 repo root 的 [architecture.md](../../../../docs/architecture.md) 了解模型；格式以 [data-contract.md](../../../../docs/data-contract.md) 與 schemas 為準。

`runs/<id>/` 是 engagement；draft 使用 release 格式。input 保留來源；evidence 放抽取、轉錄及觀察；review 保存確認、案例測試和變更紀錄。

| stage | Skill | 離開條件 | 下一步 |
| --- | --- | --- | --- |
| frame | frame-knowledge-engagement | 範圍確認，知識密集任務、來源與參與者已盤點 | elicit |
| elicit | elicit-business-knowledge | 足以建模一個任務，material gap 明列 | model |
| model | model-business-knowledge | 模型引用可解析，衝突及缺口明列 | validate；缺來源回 elicit |
| validate | validate-knowledge-release | 參與者確認版本，重要 inference 案例通過 | release；修正回 model/elicit |
| release | validate-knowledge-release | publish 建立 snapshot、handbook、coverage、index | complete 或 derive |
| derive | build-knowledge-solution | coverage 可用，產品存在且目標案例已驗證 | complete；缺知識回 elicit/model |
| complete | 入口 | knowledge-only 或 knowledge-and-solution 完成 | 有新工作才重啟 |

status 使用 active、awaiting_input、blocked、complete。next_action 是具體下一步，complete 時為 null。pending 記錄具體問題及資料位置。state 只控制進度，模型才是業務內容來源。

資料不足不必阻止所有建模；同一任務可反覆 elicit/model。無內容的 section 用空清單，manifest.empty_sections 寫理由，至少 context、domain、task 有內容。

review.confirmation 記錄參與者、時間、對話/檔案位置、model_digest。digest 涵蓋模型、來源、gap、範圍，內容改變後舊確認失效。scenario-tested 必須對應 review scenario 的 pass，不能只靠格式驗證。

修正時在 review/changes.md 記下原因、affected_ids、修改及重測範圍。已發布 release 不覆寫；新版本完成前，向使用者說明受影響衍生物限制。source 不在本機時記 unavailable；口述不冒充視覺操作證據。發布不等於 Git commit、push 或部署。
