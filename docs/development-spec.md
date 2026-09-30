# 業務知識蒸餾 MVP 開發規格書

狀態：對照 2026-09-30 repository 現有 Skill、`schemas/` 和 `scripts/knowledge_workflow.py`。本文件定義**目前可執行的資料流程與契約**，不把未做的網站、資料庫或自動業務判斷寫成已實作功能。設計依據見 [來源對照](reference-map.md)，欄位完整規則以 [資料契約](data-contract.md) 和 [`schemas/`](../schemas/) 為準。

## 1. 目的、使用者與完成條件

**目的**：將一項有邊界的部門工作中重要的規則、判斷線索與理由、例外、交接及資深人員經驗，整理成可閱讀、可追溯、可修訂的 **Knowledge Release**。Codex 執行閱讀、訪談與建模；業務參與者提供材料、修正理解與確認版本；Python CLI 檢查檔案契約、產生閱讀文件並發布本機快照。

**MVP 完成條件**：目的與範圍清楚；重要知識連到來源；已知衝突與缺口明列；參與者確認目前版本；`critical=true` 的知識有當前版本的通過案例；`publish` 產生 Release。這代表**本次確認範圍完成**，不代表整個部門已蒸餾完畢，也不保證接手者已能獨立執行。Skill／SOP／Script 是使用者要求時才建的選用應用。

## 2. 一眼看懂的資料流

```text
使用者目的、現有知識、文件／訪談／案例
  → frame：runs/<RUN>/engagement.yaml + state.yaml + input/
  → elicit：evidence/ 原始紀錄 + draft/evidence-index.yaml + gaps.yaml
  → model：draft/ 的知識 YAML → handbook.md + coverage.md
  → validate：review/ 原始核對紀錄 + draft/review.yaml
  → release：knowledge/<department>/<domain>/releases/<id>/ + index.yaml
  → [選用] build：solutions/<name>/ 的應用與測試紀錄

任何階段發現來源不足 → elicit；知識解讀錯誤 → model；應用實作錯誤 → build。
```

`runs/<RUN>/` 是**一次工作**，`draft/` 是**本次可修改的唯一知識模型**，`knowledge/.../releases/<id>/` 是**發布後的版本快照**。`input/` 放原始材料，`evidence/` 放有定位的摘錄、訪談及媒體中間證據；兩者都不等於已確認知識。`review/` 放人員回覆與案例走查的原始紀錄，`draft/review.yaml` 只放可檢查的摘要。`solutions/` 不參與 Knowledge Release 的基本完成條件。

## 3. 系統邊界與檔案責任

| 位置 | 內容／格式 | 誰建立與更新 | 誰使用 |
| --- | --- | --- | --- |
| `.agents/skills/` | `SKILL.md` 指令、`references/` 方法、`scripts/` 媒體工具 | 開發者維護 | Codex 依階段執行；不是業務知識庫 |
| `runs/<RUN>/engagement.yaml` | 一次工作的目的、部門、領域、參與者、範圍、來源類型與優先理由 | CLI `init` 建空欄；Codex 與使用者在 frame 填完整 | 全階段判斷是否切題 |
| `runs/<RUN>/state.yaml` | `stage/status/next_action/pending` 等進度 | `init` 建立，Codex 每輪更新 | 中斷後續作；**不存業務規則** |
| `runs/<RUN>/input/` | 原始檔副本或清楚的外部引用；格式隨原始材料 | Codex 收集 | elicit 查來源；若不複製檔案，引用須記在 `engagement.resources` 與 evidence locator |
| `runs/<RUN>/evidence/` | 訪談原始紀錄、擷取片段、逐字稿、媒體證據包；按來源保留原格式 | Codex／選用媒體 Skill | elicit 建可定位的 evidence index；中間 JSON 不是正式知識 |
| `runs/<RUN>/draft/` | **11 個 YAML 內容檔**；render 後另有 `handbook.md`、`coverage.md` | `init` 建空骨架；Codex 持續更新 YAML；CLI 產生 Markdown | model／validate 的單一維護位置 |
| `runs/<RUN>/review/` | 確認對話、案例實際結果、修正理由等原始紀錄；可為 Markdown 或可定位引用 | Codex 保存真人回覆 | validate 及後續稽核；不是 CLI 直接驗證的固定 schema |
| `knowledge/<department>/<domain>/` | `index.yaml`＋`releases/<id>/` 的已確認快照 | CLI `publish` 新增 | 交付手冊、查來源／範圍、開始下一版 |
| `solutions/<name>/` | 選用應用、知識映射及測試 | build Skill／Codex | 使用者要求 Skill／SOP 等時 |

**建立時間**：`init` 會建立 `input/`、`evidence/`、`draft/`、`review/` 和全部 11 個 YAML 骨架；`engagement.yaml`、草稿當時有空欄，**預期尚未通過驗證**。`render` 成功後才有草稿手冊與涵蓋文件。`publish` 只複製模型 YAML 和生成的 Markdown；**不複製 `input/`、`evidence/`、`review/` 原始資料**，查核者仍須有權取得它們或外部來源。

## 4. 主流程的 INPUT／OUTPUT 契約

以下表格的「完成」是進下一階段的工作條件；正式發布仍以 CLI 的 release 檢查及真人核對為準。階段可以反覆，並非每一階段只跑一次。

| 階段與執行者 | 必要 INPUT | 具體 OUTPUT／格式與作用 | 進下一階段的條件 |
| --- | --- | --- | --- |
| **入口／續作** `bu-knowledge-workflow` | 新請求：目的、材料；續作：`state.yaml`、`engagement.yaml`、現有草稿 | 新請求呼叫 `init`；每輪更新 `state.yaml` 的 `stage/status/next_action/pending`，說明讀了什麼與待補問題 | 已找到一項具體工作；若缺人提供資料，保留 `awaiting_input` 和具體問題，不假裝完成 |
| **1. frame 界定範圍** | 部門目的、候選任務、接手者、參與者、已有材料；若有舊版先讀 library `index.yaml` | `engagement.yaml` 填 `objective/users/included/excluded/priority_reason/participants/resources/scope_confirmation`；`draft/context.yaml` 記流程、角色與系統；來源放 `input/` 或記引用 | 參與者核對本次要保存的**一項重要任務**與邊界；`state.stage=elicit` |
| **2. elicit 擷取證據** | `input/`、訪談／案例／觀察、library 既有知識、目前 `gaps.yaml` | `evidence/` 保存原始摘錄及訪談；`draft/evidence-index.yaml` 每筆記 EVD ID、來源、定位、版本、摘錄；`draft/gaps.yaml` 列未知及影響 ID；候選主張交 model | 對至少一項任務有足以建模的材料；不足、矛盾和未觀察的部分仍明列，不把推論當觀察 |
| **3. model 建知識模型** | `engagement.yaml`、證據索引、候選主張、既有 draft／舊 Release | 更新 `draft/` 中的 `context/domain/inference/task/communication/expert-perspectives/cases` 等 YAML，設定來源與依賴 refs；執行 `validate <draft>` 和 `render <draft>`，產出 `handbook.md`、`coverage.md` | Schema、ID、來源與依賴可解析；重要規則、理由、例外、交接及缺口能交由參與者閱讀；缺來源回 elicit |
| **4. validate 核對** | 草稿手冊、來源、案例預期結果、業務參與者回覆 | `review/` 保存原始確認及案例走查；`draft/review.yaml` 記確認者、時間、原始位置、模型 digest、案例實際結果與 pass/fail | 參與者確認**目前模型版本**；所有 `critical=true` 物件有當前版本的通過案例；失敗回 model／elicit |
| **5. release 本機發布**（仍由 validate Skill 執行） | 已確認的 `draft/`、目標 `knowledge/<department>/<domain>/` | `publish` 建立 `releases/<release_id>/`：11 YAML、`handbook.md`、`coverage.md`、`release-lock.yaml`；更新 `index.yaml`；`state.release_path` 指向新版本 | `validate --release` 通過、release ID 未用過；未要求應用則 `completion=knowledge-only` |
| **6. derive 選用應用** `build-knowledge-solution` | 指定 Release、使用者指定的用途、任務 ID、工具條件 | `solutions/<name>/target.yaml` 指定目標；`artifact/` 放 Skill／SOP 等；`traceability.yaml` 映射來源；`validation.md` 記實際測試與限制 | 需求範圍的知識足夠，應用有 happy／stop 測試；知識缺口回 elicit／model |

### 階段進度格式

`state.yaml` 的 `stage` 為 `frame`、`elicit`、`model`、`validate`、`release`、`derive` 或 `complete`；`status` 為 `active`、`awaiting_input`、`blocked`、`complete`。`next_action` 必須寫可執行的下一步，完成時為 `null`；`pending` 記具體待回答問題。Codex 維護此檔，CLI **不自動跑訪談、切階段或填確認**。

## 5. 知識檔格式：11 個 YAML 各做什麼

這 11 個檔案是**同一份知識的分類**，不是 11 道人工流程。至少 `context`、`domain`、`task` 要有物件；其他分類不適用時可為 `[]`，並在 `manifest.empty_sections` 說明。每個知識物件至少有 `id/kind/title/statement/scope/evidence_refs/evidence_mode/validation/sharing/expert_refs/refs/critical/details`。逐欄型別見 [`knowledge-release.yaml`](../schemas/knowledge-release.yaml)；各 `details` 的必填項見 [資料契約](data-contract.md#details-的必填欄位)。

| `draft/` 內檔案 | 主要內容 | 對應使用者問題 |
| --- | --- | --- |
| `manifest.yaml` | release ID、部門／領域、範圍、排除、上一版、空分類理由 | 這版涵蓋什麼？ |
| `context.yaml` | 角色、工作情境、流程、系統 | 誰在什麼情境做？ |
| `domain.yaml` | 概念、事實、政策與例外 | 名詞和明確規則是什麼？ |
| `inference.yaml` | 輸入、線索、理由、結果、缺值／衝突處理、反例 | 為何作這個判斷？ |
| `task.yaml` | 目標、觸發、步驟、分支、輸出、停止條件 | 何時做什麼？ |
| `communication.yaml` | 人／系統之間的交接與檢查 | 誰交給誰、交什麼？ |
| `expert-perspectives.yaml` | 具名專家經驗、策略、新手錯誤、適用邊界 | 誰的做法？適用到哪裡？ |
| `cases.yaml` | 來源支持的案例預期、實際／假設標記、失敗教訓 | 用什麼情境核對？ |
| `evidence-index.yaml` | EVD ID、來源、定位、版本、摘錄、說話者、可取得性 | 每項主張根據什麼？ |
| `gaps.yaml` | 未知／衝突、影響哪些知識 ID、是否阻擋、處理狀態 | 哪些重要問題還沒回答？ |
| `review.yaml` | 參與者確認及案例實際結果，綁定模型 digest | 誰確認這一版？測過什麼？ |

`handbook.md` 與 `coverage.md` **由 `render` 產生**：前者供人閱讀知識內容、來源與限制；後者逐項顯示證據、確認、歸屬、核心標記與未解缺口。修正時改 YAML 再 render，不直接改生成文件。`release-lock.yaml` 由 publish 建立檔案 SHA-256 指紋，用來偵測快照變動；不是安全簽章。

### 最短追溯鏈

```text
input/訪談筆記的第 4 段
  → evidence/原始訪談紀錄
  → draft/evidence-index.yaml：EVD-001（source + locator + excerpt）
  → draft/inference.yaml：INF-001.evidence_refs=[EVD-001]
  → draft/task.yaml：TASK-001.refs=[INF-001]
  → draft/cases.yaml：CASE-001.refs=[INF-001, TASK-001]
  → review/案例走查原始紀錄
  → draft/review.yaml：CASE-001 的實際結果與 model_digest
  → release/handbook.md 與 coverage.md
```

此處 ID 只是連結方式示例。若來源只能證明「某欄位存在」，不能因此認定某位同事停下操作的**理由**已獲證明；理由需另外追問或留在 gap。

以下是[合成示範](../runs/synthetic-demo/draft/evidence-index.yaml)的一筆 evidence 格式（內容為虛構）：

```yaml
- id: EVD-001
  source: examples/synthetic/source.md
  locator: S1-S3
  source_group: synthetic-expert
  source_version: fixture-v1
  excerpt: blue → accept；缺失或其他 → stop。全部為虛構規格。
  speaker: SYNTHETIC Demo
  availability: available
```

對應的[判斷物件](../runs/synthetic-demo/draft/inference.yaml)用 `evidence_refs: [EVD-001]` 指向它，再以 `details.inputs/cues/reasoning/outcomes/counterexamples` 解釋判斷；[確認物件](../runs/synthetic-demo/draft/review.yaml)則記確認來源、案例實際結果與 `model_digest`。完整有效範例請讀這三個檔案；單筆摘錄不是可單獨發布的 Release。

### 關鍵欄位的意義

| 欄位 | 格式／選值 | 用途與判讀 |
| --- | --- | --- |
| `evidence_refs` | 非空 EVD ID 清單 | 指向 [`evidence-index.yaml`](../schemas/evidence.yaml) 的來源；每筆含 `source/locator/source_group/source_version/excerpt/speaker/availability` |
| `refs` | 知識 ID 清單，可空 | 本物件理解或執行時依賴哪些知識；用於追溯與應用 coverage |
| `evidence_mode` | `observed/stated/inferred/conflicting/unresolved` | 來源支持方式；`observed` 也不自動等於真實或通用 |
| `validation` | `draft/participant-confirmed/scenario-tested` | 核對歷程；與來源支持方式是兩個獨立維度 |
| `sharing` | `shared/attributed/contested` | 共同適用、具名經驗或分歧；`shared` 需至少兩個獨立 `source_group`，發布時還需參與者確認 |
| `critical` | `true/false` | 是否為本次範圍的重要判斷／必要主張；`true` 需當前版本通過案例，不得只為通過檢查改成 `false` |

## 6. 確認與發布的檢查規則

| 指令 | 輸入 | 實際檢查／輸出 |
| --- | --- | --- |
| `init --department <slug> --domain <slug>` | 部門、領域；可重複 `--source-type` | 建立 `runs/RUN-.../` 空骨架；回傳路徑；**尚不可發布** |
| `validate <draft>` | 11 個 YAML | Schema、必填 details、ID 唯一、refs／evidence_refs 可解析、未知有 gap 等；回傳 `structure-only`，不證明內容正確 |
| `render <draft>` | 通過結構檢查的 draft | 產生／重建 `handbook.md`、`coverage.md` |
| `digest <draft>` | 目前模型、來源、缺口及範圍 | 回傳 SHA-256 模型指紋；`review.yaml` 本身不納入 digest |
| `validate <draft> --release` | 當前 draft 與 `review.yaml` | 除結構外，確認 digest 未過期、`critical` 有通過案例、核心不確定性已處理；回傳 `release-contract` |
| `publish <draft> --library knowledge/<department>/<domain>` | 通過 release 契約的 draft | 重新 render、建立不可覆寫的新 Release、`release-lock.yaml` 和 `index.yaml`；本機發布，不等於 Git push／正式部門核准 |

案例的 `expected` 應先來自來源或參與者，走查後才記 `actual`、`result` 與原始紀錄位置。確認與案例都要綁**同一個目前模型 digest**；模型、來源、範圍或 gap 改變，舊確認不能直接移植。程式檢查紀錄的格式與版本，不會判斷受訪者說的業務內容是否真實。

## 7. 選用媒體與選用應用

**媒體**僅在文字資料不足、需要聽語音或看實際操作時啟動；文字訪談和文件可完成主流程。`prepare-audio-evidence` 產出 `evidence/audio/<id>/` 的時間碼資料，`extract-video-evidence` 產出 `evidence/video/<id>/evidence-package/`，`analyze-video-evidence` 產出 `evidence/video/<id>/analysis/` 的候選主張；`record-bu-walkthrough` 可在授權後把畫面／聲音錄到 `evidence/recordings/`。精確媒體中間格式見各 Skill `references/`；它們最後都回到 elicit 建 EVD、留缺口，再由 model 決定是否寫入正式知識。音訊口述不能當作畫面操作已發生的證據。

**應用**在 Release 發布後才按需求建立。`solutions/<name>/target.yaml` 的格式由 [`solution-target.yaml`](../schemas/solution-target.yaml) 定義，至少指定產品種類、advisory／execution 模式、使用者、結果、必要任務 ID、輸入與輸出；`artifact/` 放實際產品；`traceability.yaml` 把產品行為連回 Release 的知識 ID；`validation.md` 留 happy／stop 測試。`coverage` 能檢查指定任務及依賴的知識缺口；`verify-solution` 能檢查映射與測試紀錄契約，**不能單靠它證明產品行為正確**。沒有提出應用需求時，Release 完成即可結案。

## 8. 更新既有知識的規則

已發布的 Release 不直接改。新材料或使用回饋先找受影響的知識 ID：缺來源回 elicit，解讀或規則錯誤回 model，只有產品呈現／工具錯誤才回 build。新 run 的 `manifest.base_release` 指向上一版，保留穩定 ID，`review/changes.md` 記修正原因與重測範圍；更新模型後重新 render、取得目前版本確認與必要案例，再 publish 新 release ID。`index.yaml` 同時列出新舊版本。

## 9. 實作狀態與最小驗收示例

目前有 10 個方法 Skill、4 份 schema、CLI、18 個契約測試，以及[合成示範](../examples/synthetic/README.md)。合成示範能檢查 `EVD → INF → CASE → review → Release` 的檔案鏈，但使用的是**預設的假受訪者與假案例結果**，沒有真實訪談或接手者使用。真實試點應用一項部門任務，保留原始資料、取得真人確認、以未參與建模的案例核對，最後請接手者實際讀手冊並回報無法判斷之處。

在 repo 根目錄執行現有契約檢查：

```powershell
.venv/Scripts/python.exe scripts/knowledge_workflow.py check-repo
.venv/Scripts/python.exe -m unittest discover -s tests -v
```
