---
name: validate-knowledge-release
description: 檢查知識模型的來源、衝突與案例，取得參與者對版本的確認，產生可閱讀且可追溯的 Knowledge Release。
---

# 檢驗與發布

讀 [資料契約](../../../docs/data-contract.md) 及 [工作流程](../bu-knowledge-workflow/references/workflow.md)。

1. validate <draft> 檢查引用，另外核對來源含義。render <draft> 產生 handbook/coverage，提供連結及重要決策、歸屬、衝突、缺口摘要。
2. critical=true inference 至少走查一個有獨立 expected 的 case。可 replay 或 hypothetical walkthrough，但記 method、actual、result、參與者。無法測者保留 draft 或經使用者同意縮 scope；不能為通過而改 critical。
3. digest <draft> 取得模型指紋。收到確認才在 review.yaml 記參與者、時間、原始位置、digest；scenario record 同樣綁 digest。AI 不得捏造 confirmation。
4. validate <draft> --release 通過後，以 publish <draft> --library knowledge/<department>/<domain> 建新版本。這是本機 snapshot，不是 Git push 或正式部門核准。
5. 更新 state.release_path。已要求產品則 stage=derive，否則 complete、completion=knowledge-only、next_action=null。

可留明列的非核心 inferred/unresolved；coverage 顯示限制，不宣稱涵蓋整個部門。handbook/index 本身是可用知識庫成果。
