# Knowledge → Solution

target 依 schemas/solution-target.yaml。required_task_refs 不可省略；optional_task_refs 允許因缺口排除。knowledge readiness 與 runtime readiness 分開。

- ready：全部 required/optional 依賴可用。
- limited-scope：required 可用但部分 optional 缺知識，明確排除。
- knowledge-gap：任一 required 不足，不能宣告目標完成。

使用 participant-confirmed/scenario-tested 且 observed/stated 的主張。拒絕 unresolved/inferred/conflicting/contested 和 blocking gap 規則。attributed 只有 target.allowed_expert_refs 明列專家才可使用，產品保留歸屬。

release 不保證支援任意 Skill。coverage 查特定任務及依賴；業務缺口回知識層。UI path、connector、工具權限不足記 runtime limitation。口述可支持 advisory Skill，execution Skill 需證明實際 source-to-output 路徑。

| 知識 | 轉換 |
| --- | --- |
| Context | 觸發及適用範圍 |
| Domain | 定義、reference、資料規格 |
| Task | 順序、分支、完成判準 |
| Inference | cues、理由、判斷及人工決策點 |
| Communication | 輸入、輸出、交接 |
| Expert | 有歸屬的策略及限制 |
| Cases | 來源支持的 expected、回歸案例 |

traceability.yaml 必填 release_id、model_digest、coverage_status、accepted_task_refs、behaviors、tests。behavior 含 id、artifact（solution 下的檔案）、knowledge_refs；test 含 id、kind（happy/stop）、method、expected、actual、result、evidence。validation.md 說明 runtime、限制及使用方式。

expected 先於 actual，至少 happy 與 stop 各一例。AI 演練標 simulated，不能冒充執行。MVP compiler 是有契約的 Codex 轉換工作；scripts 只做 validation、coverage、render、snapshot、追溯檢查。
