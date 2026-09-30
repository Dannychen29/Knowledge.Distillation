---
name: elicit-business-knowledge
description: 從文件、ACTA 訪談、案例與操作觀察擷取部門知識證據，特別挖掘資深員工的關鍵線索、判斷理由與例外。
---

# 擷取業務知識證據

讀 [ACTA 訪談](references/acta.md)、[來源 adapters](references/adapters.md) 及 [資料契約](../../../docs/data-contract.md)。讀 active engagement 和既有模型，依缺口提問。

1. 先查 library 和已提供資料。將政策、實際作法、個人建議分開記錄；建立 evidence ID、來源版本/位置、speaker 及摘錄。原始內容保留於 input。
2. ACTA 隨任務調整：task diagram → knowledge audit → 具體事件或 simulation → cognitive demands table。低判斷任務不必做全套。
3. 一次優先問一個會改變理解的問題。把抽象經驗追問成「線索、判斷、理由、反例、下一步」；區分回憶、假設和實際案例。
4. 專家分歧記 attributed/contested，不以多數或職級自動決定正確。文件與行為不符保留兩者。
5. 在 evidence 寫擷取結果與 interview 記錄，更新 draft evidence-index 和 gaps。將候選主張交 `$model-business-knowledge`；worker JSON 是中間證據，不能直接當 canonical model。

只在來源需要時呼叫媒體 workers。錄影需遵守 screen/microphone 授權程序；不用錄影也能完成蒸餾。
