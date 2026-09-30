# 資料契約：給 Codex 與需要深入理解的人

`schemas/*.yaml` 是以 YAML 撰寫的 JSON Schema；實際資料也是 YAML。CLI 組合各模型檔後驗證，再檢查 IDs、依賴、型別專屬欄位、確認版本及案例。

## Release 檔案

| 檔案 | 格式與用途 |
| --- | --- |
| manifest.yaml | schema_version=1、release_id、安全的 department/domain slug、scope、exclusions、base_release、empty_sections |
| 七個模型/案例 YAML | object 清單；無內容 section 為 []，在 empty_sections 解釋 |
| evidence-index.yaml | evidence 清單，格式見下 |
| gaps.yaml | id、question、affects（知識 IDs）、blocking、status=open/resolved、resolution |
| review.yaml | confirmation 及 scenarios；confirmation 未取得為 null |
| handbook.md | 由模型渲染，含主張、適用範圍、來源與所有 details |
| coverage.md | 逐物件證據/確認/歸屬狀態與缺口，不宣稱任意產品都可建 |
| release-lock.yaml | publish 產生的檔案 hash；draft 沒有此檔 |

至少 context、domain、task 有內容；其他 section 可因範圍不適用而空。不可用空清單避開已知決策。

## 每個知識物件的共用欄位

| 欄位 | 意義 |
| --- | --- |
| id | bundle 中唯一且跨修訂穩定；建議 CTX/DOM/INF/TASK/COM/EXP/CASE/LESS 前綴 |
| kind | context/concept/fact/policy/inference/task/handoff/expert/case/lesson |
| title、statement、scope | 名稱、完整主張、成立的具體情境 |
| evidence_refs | 一個或更多 EVD ID |
| evidence_mode | observed/stated/inferred/conflicting/unresolved |
| validation | draft/participant-confirmed/scenario-tested |
| sharing | shared/attributed/contested |
| expert_refs | 專家 EXP ID；attributed 必填；專家物件可指自己 |
| refs | 本物件理解/執行不可缺的其他知識 ID；coverage 遞迴追蹤 |
| critical | 是否為此次範圍的重要判斷或必要核心主張；依 engagement 的業務目的及 priority_reason 選定，不以是否能做 Skill 決定；不可為通過驗證降低它 |
| details | 依 kind 的結構化內容 |

evidence_mode 是來源支持方式；validation 是檢視歷程，兩個軸獨立。observed 不等於正確；stated 可經 participant-confirmed。無充分支持的 inferred 不能只改 status 就當 observed/stated，需補 evidence。shared 至少兩個獨立 source_group 且經參與者確認；這是 MVP 的保守約定，不表示來源多就一定正確。contested 保留不同觀點和 gap。

## details 的必填欄位

下表標 * 的欄位是字串清單，其餘是字串。清單項目可以寫具體 ID，但所有必要依賴仍需在 refs 宣告，程式不推測文字中的隱含關係。

| kind | 必填欄位 |
| --- | --- |
| context | roles*、processes*、systems* |
| concept | definition |
| fact | value |
| policy | condition、rule、exceptions* |
| inference | inputs*、cues*、reasoning*、outcomes*、missing_input、conflicting_input、counterexamples* |
| task | goal、trigger、inputs*、steps*、outputs*、stop_conditions*、completion |
| handoff | sender、receiver、payload*、trigger、channel、check |
| expert | role、experience_scope、mental_models*、heuristics*、novice_mistakes*、boundaries* |
| case | scenario、inputs*、expected、expected_source、case_type（actual 或 hypothetical） |
| lesson | expected、actual、reason、next_time |

可加確有必要的 details，例如 field mapping、規則有效時間、資料格式。重要但未知的內容填字串 unknown，並新增 affects 該 ID 的 open gap。無例外/反例不等於不知道：確認無項目用 []；尚未訪談用 [unknown]。純粹不適用可明寫理由，不發明操作細節。

inference 的 inputs/reasoning/outcomes、task 的 inputs/steps/outputs/stop_conditions、handoff.payload 不可空。這些是最小可理解單位，未知值會阻止產品 readiness。

## Evidence

每筆有 id、source（檔案/URL/原始紀錄）、locator（頁碼/段落/時間碼/cell）、source_group（獨立來源識別）、source_version、excerpt、speaker（可 null）、availability。

本機 source 以 repo-relative 路徑或明確外部絕對路徑記錄，locator 不只寫「訪談」。raw 在 runs 被忽略時，他人仍能看到 excerpt/locator，但可能拿不到原始檔：availability=unavailable，coverage/handbook 必須揭露。格式檢查只驗欄位，不保證原始來源存在或含義正確。

## 確認與案例

confirmation 有 participant、confirmed_at（加引號的 ISO 日期時間）、source（真實對話或檔案定位）、model_digest。scenario 有 case_ref、knowledge_refs、method=walkthrough/replay、participant、actual、result=pass/fail、source、model_digest。case.refs 必須包含測試的 knowledge_refs。

digest 不含 review 本身，避免簽確認改變其被確認內容。先更新模型狀態，再算 digest，再記錄該版本的真實確認/案例。模型、scope、evidence 或 gaps 改變會使先前確認過期，需重測受影響案例並重新確認目前版本；不可直接重寫 hash 偽裝已確認。

`validate --release` 要求目前版本確認、critical 物件有 passing scenario、critical 不確定性已解決。非 critical 缺口可留在 release，coverage 會顯示，衍生產品的 closure 若涉及它就不 ready。

## Solution

target 依 solution-target schema；required_task_refs 不可省略，optional_task_refs 可排除，allowed_expert_refs 決定是否採用具名方法。coverage 遞迴沿 refs 檢查，輸出 ready/limited-scope/knowledge-gap；runtime_readiness 固定 not-assessed，必須另做工具測試。

traceability.yaml 的格式與轉換規則見 [solution contract](../.agents/skills/build-knowledge-solution/references/solution-contract.md)。verify-solution 驗證檔案存在、無跨出 solution 目錄、release 指紋、採用範圍、知識映射、happy/stop 紀錄。它無法讀懂並證明 Skill 行為，需另外實際測試或明列 simulated 限制。

## Run

engagement 依 engagement schema；frame 時空草稿可以存在，離開 frame 前必須完整。`entry_mode` 是 department-first/expert-first 的知識視角；`source_types` 是現有材料類型清單，可同時列出 document、form、process-map、interview-record、case、media、observation，沒有材料時為空清單。具體檔案或引用記在 `resources`；後續取得新材料時同步更新，無須擇一材料路線。state 記 run_id、stage、status、next_action、pending、solution_requested、base_release、release_path、completion。Codex 更新 state；工具不自動執行訪談或跳 stage。release 完成且未要求 solution，completion=knowledge-only。
