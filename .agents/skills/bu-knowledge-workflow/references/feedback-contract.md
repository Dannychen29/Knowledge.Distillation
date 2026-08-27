# Feedback and Correction Contract

Use one row per reported issue in `feedback/iteration-log.csv`. Keep the row stable while the issue is investigated.

| Field | Requirement |
| --- | --- |
| `issue_id` | Stable identifier, for example `ISS-001` |
| `test_case_id` | The validation case that exposed the issue |
| `expected` / `actual` | Reviewable expected and actual result |
| `classification` | `intake_evidence`, `distilled_knowledge`, `solution_implementation`, or `environment_access` |
| `route_to` | The smallest affected skill or `external_blocker` |
| `affected_ids` | Relevant step, decision, field, rule, or acceptance-condition IDs |
| `correction` | What changed; never silently change a rule |
| `retest_result` | `pass`, `fail`, or `pending` |
| `reviewer` / `reviewed_at` | Named human review record |

Do not correct an apparent rule error in solution code until the source knowledge is confirmed. `environment_access` issues do not change business knowledge. Re-open downstream checks after every upstream correction.

## BU 指令式迭代

BU reviewer 可以直接以自然語言指出「錯誤、期待行為、影響範圍」來啟動迭代，不必重走完整訪談。先把指令轉成 issue row，再依最小分類路由；回覆時必須提供：受影響 artifact／ID、修正內容、重測範圍、仍需 BU 決定的唯一事項。每次修正都產生新的 iteration；先前的 artifact 不得被靜默覆蓋或遺忘。

當初版 solution 尚未成熟時，允許連續多輪 `solution_implementation` 修正與重測。若 BU 指令改變目標、範圍、資料來源、決策規則或 acceptance condition，改路由至 `distilled_knowledge` 或 `intake_evidence`，不得只修改 solution。

The validation acceptance gate passes only when every planned test case has a recorded outcome, all material failures are either retested as `pass` or remain visible blockers, and the named reviewer accepts the supported scope.
