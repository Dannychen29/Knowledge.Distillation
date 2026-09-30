# MVP 架構與設計依據

本專案的主成果是**有來源、適用範圍、重要判斷與確認紀錄的部門知識**。Codex 執行訪談、理解和建模；Python 做可重複的檔案檢查與發布。使用者以自然語言參與，主要閱讀手冊、涵蓋說明與案例結果。

## 本次設計檢視

2026-09-30 檢視實際 Skill、schema、Python 工具及外部來源，結論如下：

| 面向 | 原設計的狀況 | 本次調整 |
| --- | --- | --- |
| 方法論支撐 | 有 ACTA、CommonKADS、KCS 等來源，但未充分區分研究、實務指引與實作參考 | 補上來源到設計的對照與證據限制；以 APQC 補強重要知識的選擇 |
| README | 已有入口與目錄說明；方法論、技術欄位和產品分支混在主線中 | 先呈現成果與四步資料流，再說明 Skill、資料夾與選用應用 |
| 目標一致 | 入口與發布 Skill 已允許 knowledge-only 完成；仍以「六核心」稱呼包含產品建置的 Skill | 改為 1 入口＋4 主流程＋1 選用應用＋4 選用媒體；強化重要知識驗收 |
| MVP 複雜度 | 不需伺服器，但多個 YAML 與媒體中間格式有理解成本 | 保留既有格式與工具；說清楚讀寫關係、唯一維護位置及選用路徑 |

設計具備啟動 MVP 的方法基礎；Codex 是否能忠實蒸餾、使用者能否運用成果，仍需真實試點。文件與指令調整不等於已完成業務驗證。

## 研究與設計依據

若要逐項回答「哪個設計借鏡哪種方法或公開 Agent 專案、哪一段是本 repo 自訂」，先看 [設計與來源對照](reference-map.md)。本節列出方法論本身與採用限制；[GitHub 實作參考](github-agent-practice.md) 則保留原始操作檔及採用訊號。

下列是來源支持的設計方向，並非本專案效果的實證。ACTA 有原始評估研究；CommonKADS 提供知識工程方法；APQC、KCS 提供組織實務指引。它們沒有直接驗證目前這套 Codex 工作流程。

| 來源與性質 | 能支持什麼 | 本專案怎麼採用 | 適用限制 |
| --- | --- | --- | --- |
| [Militello & Hutton, 1998，ACTA 原始研究](https://pubmed.ncbi.nlm.nih.gov/9819578/)；Ergonomics 41(11), 1618–1641，[DOI](https://doi.org/10.1080/001401398186108) | 用訪談擷取完成任務所需的認知技能；原研究評估方法的可用性與產出用途 | elicit 用任務草圖、知識稽核及情境訪談，保存線索、理由與認知難點 | 人類訪談研究不能直接推論 AI 訪談同樣可靠；仍需回述、來源核對與案例 |
| [CommonKADS 官方 Basics](https://commonkads.org/basics/)、[IJCAI 1997 方法論教程](https://www.ijcai.org/past/ijcai-97/CI/TUTORIAL/sp3.html) | 先分析與表達知識，再決定應用設計；知識模型能跨應用重用 | model 建立可獨立閱讀的知識；Release 可直接交付；build 是選用分支 | 只採分析骨架，未實作完整 CommonKADS 方法或形式推理引擎 |
| [AIAI CommonKADS 課程](https://www.aiai.ed.ac.uk/project/ftp/Yesterday/pub/home/iwh/cdrom/www/aiai/training/kads-syl.htm) | Domain、Inference、Task 的分層及模型驗證 | 分別保存規則／概念、判斷、任務順序，配合情境及交接 | 檔案分類和欄位是本專案改編，不是原版模型的逐項複製 |
| [APQC：Understanding Structured Knowledge Transfer](https://www.apqc.org/resource-library/resource/understanding-structured-knowledge-transfer-0/html) | 先盤點重要知識、排列轉移優先序，再選擇擷取方式；部分隱性知識仍需人際傳承 | frame 記業務影響、知識集中與使用對象；優先處理一個任務 | 公開實務指引，不是本專案的比較實驗；不宣稱文件能保存所有經驗 |
| [KCS v6 Practices Guide：Summary](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/041) | 擷取、結構化、重用與改善，以及避免過度設計流程 | 先查既有知識；使用回饋回到來源／模型，建立新版本 | 只採循環原則，不導入完整人員授權、績效或治理體系 |
| [KCS：Sufficient to Solve](https://library.serviceinnovation.org/KCS/Principles_and_Core_Concepts/201-Core_Concepts/07_Sufficient_to_Solve) | 內容與流程應足夠支援使用，避免過度工程化 | 一個任務先完成；細節按需讀取；無材料時可從訪談開始 | 本專案對確認與發布的具體門檻仍屬自己的設計 |

[Distilly](https://github.com/titanwings/distilly) 是多來源與個人經驗整理的**實作參考**。其公開 README 以 Person Profile 與 Agent Skill 封裝為主要方向；本專案只參考來源保留與經驗歸屬，不以該產品形態決定部門知識的交付方式，也不把專案流行程度當成有效性證據。

本次核對 ACTA 原始論文摘要／書目與其他來源的官方頁面或索引內容；未將未讀取的付費教材當成依據，也未做系統性文獻回顧。以上來源足以說明 MVP 為何這樣設計；要支持「有效保存本部門知識」仍需實際試點。

Codex／Claude Code 專案**實際如何組織訪談、證據、知識與使用回饋**，另見 [GitHub Agent 實作參考](github-agent-practice.md)。它們提供操作樣例，不能替代本部門案例驗證。

### 哪些是自己的設計決定

下列是可在試點後調整的工程約定，沒有聲稱是方法論強制要求：

- YAML 分檔、穩定 ID、依賴 refs、檔案指紋與本機 snapshot。
- `shared` 需兩個獨立來源群組並確認共同適用。單一來源的經驗仍可具名保存；這個門檻不表示多來源必然正確。
- 參與者確認綁定目前模型指紋；所有 `critical=true` 物件需有目前版本的通過案例。
- `expert-perspectives` 是歸屬與經驗的擴充；`cases` 是驗證與學習材料。

CommonKADS 原版的 Organization、Task、Agent 情境分析在此收斂到 context；其 Knowledge Model 的 domain/inference/task 用三個檔案表達，Communication 對應交接，Design 留在選用應用。因此「六種知識分類」不等於原版「六模型」。

## 重要知識如何從範圍走到驗收

frame 在現有 `engagement.objective/users/priority_reason/included/excluded` 記清楚：支援哪項部門工作、誰需要、判斷錯誤有何影響、為何值得保存。可從部門任務或資深員工的代表事件切入；都需連回實際工作。

model 把重要判斷或必要核心主張標為 `critical=true`，用 `scope` 與任務關係說明用途。有證據的規則、經驗、交接與失敗教訓均可納入；不以能否自動化或生成 Skill 判斷價值。

validate 回到原定目的，帶參與者核對「哪些重要問題已能回答、依據和例外是否保留、還缺什麼」。使用現有 handbook、coverage、cases 和 review 紀錄，不另外建立一套評分表。重要但未解的知識保留於草稿及 gap；需要縮小發布範圍時明確說明並取得範圍確認，不能只取消 critical 來通過檢查。

程式只能檢查被標示的 critical 及其案例；**是否漏掉重要知識、來源含義是否被誤解，須由 Codex 與參與者核對**。試點用未參與建模的案例、接手者的使用結果或具體修正回饋評估可用性，記入既有 cases／review。發布檢查不會自動證明知識已成功轉移。

## 各階段的 DATA FLOW

以下路徑除 `knowledge/`、`solutions/` 外，均相對於 `runs/<RUN>/`。

| 階段／負責 Skill | 讀入 | 寫出 | 何時往下走 |
| --- | --- | --- | --- |
| 入口 bu-knowledge-workflow | 使用者目的；既有 state、engagement | `state.yaml` 的進度與具體 next_action | 有可執行工作就繼續；缺人的資料時列問題及成果位置 |
| frame | 任務、材料、參與者；既有 library index／Release | `engagement.yaml`、`draft/context.yaml`；原始材料副本／引用進 `input/` | 範圍與優先任務已確認 |
| elicit | `input/`、新訪談、已有知識與 gap | `evidence/` 的來源片段／候選主張；`draft/evidence-index.yaml`、`draft/gaps.yaml` | 足以整理一個任務；其餘缺口明列 |
| model | evidence、候選主張、現有 draft | `draft/` 的知識 YAML、案例、來源與 gap；render 產生手冊及 coverage | 格式與引用通過，能讓人核對；缺來源回 elicit |
| validate | 草稿手冊、原始來源、案例、參與者回覆 | `review/` 原始確認／案例／修正紀錄；`draft/review.yaml` 的可檢查摘要 | 目前版本真實確認，核心物件案例通過；錯誤回 model 或 elicit |
| release（同一 validate Skill） | 通過發布檢查的 draft | 複製至 `knowledge/<department>/<domain>/releases/<id>/`，更新 index；寫檔案指紋及 state.release_path | 未要求應用即可完成 knowledge-only |
| 選用 build | Release＋使用者指定用途 | `solutions/<name>/` 的 target、artifact、traceability、validation | 知識適用且應用目標經測試 |

多個 Skill 可以更新同一草稿：elicit 維護證據與缺口，model 整理主張，validate 寫確認結果。MVP 由同一 Codex 工作流程依序維護，不讓各階段另存一份互相競爭的知識庫。

### 三種資料要分清楚

- **原始材料**：`input/` 副本或外部引用；進行中的訪談原始紀錄也可能直接保存在 `evidence/`。來源位置必須可追溯。
- **中間證據**：`evidence/` 的摘錄、逐字稿、候選主張與媒體 JSON。不能因為產出 JSON 就當作知識已確認。
- **知識內容**：`draft/` 的 YAML 是當次工作的維護位置；handbook/coverage 由它產生。發布後 Release 是該次內容的快照。

`review/` 放原始對話、走查與修正證據；`draft/review.yaml` 只放工具所需的確認摘要、結果、來源定位及版本指紋。這兩者以引用連結，不要求人工重寫兩份業務內容。

### 選用媒體的流向

```text
需要觀察操作的缺口
  → record（取得畫面／麥克風同意）
  → evidence/recordings/影片
既有音訊／逐字稿或錄製的語音
  → prepare-audio → evidence/audio/<id>/
既有影片或錄製影片＋可用逐字稿
  → extract-video → evidence/video/<id>/evidence-package/
  → analyze-video → evidence/video/<id>/analysis/
  → elicit 核對候選主張與來源 → model 寫 draft/
```

沒有媒體時整段略過。沒有聲音的影片仍可提供視覺證據；缺少畫面時口述仍可作 stated 證據。工具不可用則明列限制，使用現有可核對材料。媒體路由詳見 [adapters](../.agents/skills/elicit-business-knowledge/references/adapters.md)。

### 修正怎麼流

使用中發現問題 → 定位知識 ID → 來源不足回 elicit、理解有誤回 model → 更新草稿 → 重測受影響案例並確認目前版本 → 發布新 Release。

已發布內容不直接修改；續作以舊 Release 為 base，保留穩定 ID，記 `base_release`，清理舊確認後重新核對。`review/changes.md` 記原因、影響 ID、修改及重測範圍。只有應用的工具／呈現有誤才直接回 build；業務規則修正必須回知識層。

## 知識檔案分工

一個 Release 有 **11 個內容 YAML、2 個閱讀文件、1 個檔案指紋 YAML**；這是同一份知識的分類與閱讀形式，不是 14 個流程。draft 使用相同內容格式，但沒有 release-lock。

| 檔案 | 保存什麼 | 典型問題 |
| --- | --- | --- |
| `manifest.yaml` | 版本、部門／領域、範圍、排除與空白分類理由 | 這版涵蓋什麼？ |
| `context.yaml` | 工作情境、角色、流程、系統 | 誰為何做這項任務？ |
| `domain.yaml` | 概念、事實、政策 | 名詞與明確規則是什麼？ |
| `inference.yaml` | 判斷的輸入、線索、理由、結果與反例 | 為何這樣判斷？何時失效？ |
| `task.yaml` | 目標、步驟、分支、輸出及停止條件 | 何時做哪個判斷？ |
| `communication.yaml` | 人／系統之間的交接 | 交付誰、什麼資料、如何驗收？ |
| `expert-perspectives.yaml` | 具名經驗、策略、新手易錯與邊界 | 是誰的方法，適用到哪裡？ |
| `cases.yaml` | 實際或假設案例的輸入與預期；失敗教訓 | 用什麼案例檢查，學到了什麼？ |
| `evidence-index.yaml` | 證據 ID、來源位置／版本、摘錄、可取得性 | 每項主張的依據在哪裡？ |
| `gaps.yaml` | 未知／衝突、影響 ID、是否阻擋與處理狀態 | 還缺什麼？ |
| `review.yaml` | 目前版本的參與者確認與案例實際結果 | 誰確認、測過什麼？ |
| `handbook.md` | 由上述內容產生的知識手冊 | 人先讀這份 |
| `coverage.md` | 逐項確認、來源、歸屬與缺口 | 知識可用到什麼程度？ |
| `release-lock.yaml` | publish 產生的檔案 hash | 快照檔案有沒有變動？ |

至少 context、domain、task 有內容；其餘分類無適用內容時可空，並說明原因。空白不能用來隱藏已知判斷或缺口。

`refs` 指主張必需的其他知識，`expert_refs` 指經驗歸屬，`evidence_refs` 指來源。例如 **TASK-001 的步驟需要 INF-001；INF-001 根據 DOM-001 並引用 EVD-001**。這是引用方式示例，不是本部門規則。

Library 是 `knowledge/<department>/<domain>/` 這個資料夾；run 是一次整理工作；Release 是一次已確認範圍的版本。MVP 不另建資料庫。`index.yaml` 列版本，沒有自動跨版本合併或全庫搜尋服務。

## MVP 的取捨與剩餘風險

保留來源定位、重要知識、適用範圍、缺口、真人確認和案例，因為它們直接影響成果是否可信。工作先限一個任務，模型由 Codex 維護，使用者不必填 11 個 YAML。媒體與產品功能按需啟動。

現有格式仍有成本：handbook 按模型分類且含技術欄位，尚未經 BU 閱讀測試；媒體 JSON 比文字主線更細；所有確認綁同一模型指紋，改動後需重新取得目前版本確認。先在試點觀察理解與維護成本，再決定是否合併檔案或調整確認粒度。

`release-lock.yaml` 能偵測意外變動，不能提供安全簽章或併發控制。`publish` 不複製所有原始材料，接手者仍需取得來源才可核對。所有參與者確認、案例與來源語意都不能由格式檢查代替。

方法層完成的驗證與尚未實測項目見 [validation.md](validation.md)。MVP 下一個驗證重點是完成真實任務的知識版本並實際使用，記錄漏掉的判斷、錯誤、追問次數及使用者是否能理解成果。
