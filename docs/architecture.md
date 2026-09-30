# MVP 架構與設計理由

本專案是一套由 Codex 執行的知識工作流程，加上本機檔案與驗證工具。語意理解、訪談及 Skill 產生由 Codex 完成；Python 負責可重複的格式、引用、涵蓋範圍與快照檢查。

## 方法論如何對應實作

| 來源 | 採用部分 | 落地位置 | 不宣稱做到的部分 |
| --- | --- | --- | --- |
| CommonKADS | organization/task/agent 情境；domain/inference/task knowledge；communication；design 分離 | context、domain、inference、task、communication；solution target | 完整 CommonKADS 表單、形式推理引擎或認證 |
| ACTA | task diagram、knowledge audit、simulation interview、cognitive demands table | elicit Skill 的訪談 reference | 自動重現專家所有隱性知識 |
| KCS | 工作中擷取、先搜尋重用、情境、使用回饋 | 新 evidence 查舊 ID；scope；修正路由 | 完整 KCS 人員授權、績效管理 |
| APQC | 界定、收集、檢視、分享、使用、學習循環 | frame 到 release 到 feedback | 全企業知識治理 |
| Distilly | 多來源、具來源的專家做法、更新 | expert-perspectives 與 evidence refs | 人格複製或把所有知識包成 Skill |

本專案把 CommonKADS Organization、Task、Agent 的情境盤點收斂到 context。CommonKADS 的 Agent 可指承擔任務的人/系統，並非僅指 AI agent。知識模型內的 task 是解題目標、分解及控制順序，與 context 中的流程清單不同。inference 是使用領域知識進行判斷的可說明步驟，不聲稱取得模型或人腦的內部思考記錄。

Expert perspective 是本專案擴充，cases 是跨模型驗證材料，兩者不冒充 CommonKADS 原始獨立模型。Design 的產品化部分在選用的 build 階段實現。

## 三種粒度

- Library：一個部門之下的一個業務領域，如 `knowledge/<department>/<domain>/`。
- Engagement/run：一次有範圍的訪談與整理工作，可從人或任務切入。
- Release：一個有範圍的知識 snapshot。新 engagement 可以接續同 library 的 base release。

部門有許多 domain，不一次訪談整個部門。`manifest.scope` 與 exclusions 明確描述這次實際涵蓋；物件數量不是部門知識完成百分比。

## 六模型＋案例

| 檔案 | 知識粒度 | 典型問題 |
| --- | --- | --- |
| context.yaml | 部門、角色、流程、系統 | 誰為何做這項任務？ |
| domain.yaml | 概念、事實、政策 | 名詞是什麼？條件和限制是什麼？ |
| inference.yaml | 一個有輸入和結果的判斷 | 注意什麼線索？為何如此判斷？何時失效？ |
| task.yaml | 目標、任務分解及控制 | 何時判斷、分支、重試或停止？ |
| communication.yaml | 一次人/系統之間的交接 | 交付什麼？對方如何知道可繼續？ |
| expert-perspectives.yaml | 具歸屬的經驗策略 | 某專家怎麼看、有哪些限制？ |
| cases.yaml | 案例或 lesson | 如何驗證？做過後學到什麼？ |

部門入口先盤點流程任務再找專家；專家入口先採集代表事件，再映射回任務/domain。expert_refs 表示歸屬，refs 表示依賴。不同專家說法不必被迫統一：共同支持使用 shared，個人方法 attributed，互相衝突 contested。

## 證據到產品的責任分工

input 原始來源 → evidence 指定位置/片段 → model 的可追溯主張 → participant confirmation + scenario → release → target 的 dependency closure → artifact + traceability + tests。

同一 evidence 可支持多個物件；同一物件可有多個來源。source_group 用來標示真正獨立來源，不因文件份數增加信心。人類確認紀錄與 scenario 綁 model_digest，防止模型修改後沿用過期確認。

`release-lock.yaml` 偵測 accidental edits；它是 hash 清單，不是加密簽章或不可竄改儲存。發布會拒絕覆蓋既有 release；更正從舊版本複製為新 draft，更新 release_id/base_release，清掉舊 review 再確認。

## MVP 邊界

提供檔案型知識庫、可閱讀 handbook、手動/agent 依 ID 搜尋、知識到 Skill 的契約與工具。沒有 web UI、向量搜尋、RAG server、帳號系統、正式審批或定期治理。這些可在實證蒸餾品質後另加。

YAML 並非讓 BU 使用者手工填；Codex 維護它。使用者主要透過訪談、handbook、coverage 和案例結果掌握內容。自然語言修正必須回填 YAML，再重新 render。

## 方法論原始參考

- [CommonKADS Basics](https://commonkads.org/basics/)
- [CommonKADS methodology tutorial](https://www.ijcai.org/past/ijcai-97/CI/TUTORIAL/sp3.html)
- [ACTA 原始研究：Militello & Hutton, 1998](https://web.mit.edu/16.459/www/Militello98.pdf)
- [KCS Practices Guide](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide)
- [APQC Structured Knowledge Transfer](https://www.apqc.org/resource-library/resource/understanding-structured-knowledge-transfer-0/html)
- [Distilly](https://github.com/titanwings/distilly)

方法論內容採摘要與本專案設計，未直接複製其完整教材。研究基礎確認於 2026-09-30。
