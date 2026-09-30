---
name: model-business-knowledge
description: 將證據建成 CommonKADS 的 domain、inference、task 與交接模型，保留專家視角、衝突、案例和知識缺口。
---

# 建立業務知識模型

讀 [架構](../../../docs/architecture.md) 和 [資料契約](../../../docs/data-contract.md)。從 evidence 建立 draft。更新 release 保留 IDs、記 base_release，不改舊 snapshot。

1. 對照 engagement 的目的與優先理由，保存對部門任務重要的規則、判斷、例外、經驗與交接；重要判斷及必要核心主張使用 critical=true。分寫 domain（概念/事實/政策）、inference（由輸入線索得到判斷）、task（目標、順序、分支、停止）、communication（交接）。Context 保存角色、流程、systems 概覽；重要性與用途可記在現有 statement/scope/details，不另建模型。
2. inference 需 inputs、cues、reasoning、outcomes、missing/conflicting-input behavior、counterexamples。未知 detail 填 unknown 並連結 gap，不能補造。
3. refs 列出理解／執行本物件必需的 knowledge IDs，構成依賴。Expert perspective 可引用 inference；inference.expert_refs 僅歸屬，不形成依賴循環。
4. 個人做法保持 attributed；shared 需多個獨立來源支持及參與者確認共同適用；分歧保持 contested 並記 conflict gap。
5. cases.yaml 的 expected 先由來源/參與者建立，actual 於走查後記錄。模型自身輸出不能是唯一正解。
6. 執行 scripts/knowledge_workflow.py validate <draft> 和 render <draft>；修格式錯誤後交 `$validate-knowledge-release`。格式通過只證明契約及引用一致。

缺證據精確回流 elicit。工具/權限/畫面不足但概念知識可用時保留 execution gap，不阻止所有知識保存。
