---
name: validate-knowledge-release
description: 檢查知識模型的來源、衝突與案例，取得參與者對版本的確認，產生可閱讀且可追溯的 Knowledge Release。
---

# 檢驗與發布

讀 [資料契約](../../../docs/data-contract.md) 及 [工作流程](../bu-knowledge-workflow/references/workflow.md)。

1. validate <draft> 檢查引用，另外核對來源含義。render <draft> 產生 handbook/coverage，對照 engagement 的目的、使用者與 priority_reason，說明哪些重要業務問題已能回答、是否保留理由／例外／交接、哪些仍缺。提供現有成果連結及歸屬、衝突、缺口摘要；不以物件或 Skill 數量驗收。
2. 每個 critical=true 物件至少由一個有來源／參與者支持 expected 的 case 涵蓋；同一案例可涵蓋多項知識。可 replay 或 hypothetical walkthrough，但記 method、actual、result、參與者；hypothetical 不冒充實際操作。無法測者保留 draft 或經使用者同意縮 scope；不能為通過而改 critical。
3. 完成模型內容與 validation 狀態後，digest <draft> 取得模型指紋，再呈現目前版本。收到確認才在 draft/review.yaml 記參與者、時間、原始位置、digest；scenario record 同樣綁 digest。原始確認／案例證據留 review/ 或明確可追溯位置。AI 不得捏造 confirmation，也不得把舊案例直接改 digest 當成重測。
4. validate <draft> --release 通過後，以 publish <draft> --library knowledge/<department>/<domain> 建新版本。這是本機 snapshot，不是 Git push 或正式部門核准。
5. 更新 state.release_path。已要求產品則 stage=derive，否則 complete、completion=knowledge-only、next_action=null。

可留明列的非核心 inferred/unresolved；coverage 顯示限制，不宣稱涵蓋整個部門。handbook/index 本身是知識庫成果。發布契約通過不等於接手者已能運用；真實試點另用未參與建模的案例或使用回饋評估，結果沿用 cases/review 保存。
