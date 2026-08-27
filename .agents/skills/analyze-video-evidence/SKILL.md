---
name: analyze-video-evidence
description: 分析單一 BU engagement 所選取、附有 timecode 的 video evidence package，產出可追溯的畫面操作、欄位、workflow step、decision rationale、heuristic、例外、pain point 與 open question。由 distill-bu-knowledge 在 extract-video-evidence 後呼叫；不得分析無關的完整錄影或核准 business knowledge。
---

# 分析 Video Evidence

閱讀 [input-evidence-contract.md](references/input-evidence-contract.md)、[analysis-framework.md](references/analysis-framework.md)、[screen-action-contract.md](references/screen-action-contract.md) 與 [knowledge-contract.md](references/knowledge-contract.md)。

1. 對選取的 package 執行 `scripts/validate_evidence_package.py`，並記錄缺漏的 clip、frame、transcript、OCR 或 interaction event。
2. 結合 transcript 與操作前／操作中／操作後的 visual state，檢視每個語意連貫的 segment。
3. 擷取結構化的 operational step，而不只是畫面順序。每一步分別記錄 trigger、precondition、actor、確切的 source system/location、依序的取得方法、選取依據、input object/field、依序 action、transformation、output object、output formation rule、destination system/location、content validation、completion condition、completion evidence、failure/fallback、exception 與 escalation。不得將這些內容濃縮成籠統的 `input → output` 句子。
4. 每項 decision 均記錄 decision question 與 owner、所有 input 的 provenance、freshness、rule/threshold/heuristic、rationale、input 缺漏／衝突時的處理方式、counterexample 與 downstream effect。每個 deliverable 均記錄 output schema、required field、format/template、recipient、delivery channel/destination、timing、acceptance check 與 delivery proof。用有方向性的 `data_flows` 連結 step、system 與 deliverable，並指出 payload field、schema、transport、trigger、validation 與 failure behavior。
5. 若重要細節沒有 evidence，設為 `unknown` 並建立連結的 targeted open question。沒有 source、destination、object 與 verification 時，諸如「download」、「upload」、「process」和「deliver」等籠統動詞並不完整。僅有 transcript 的描述應標記為 `stated`；除非有 frame、clip、interaction event 或等效 artifact 佐證，否則不能證明畫面順序、field mapping、檔案移動、validation 或 completion。
6. 將 claim 分類為 `observed`、`stated`、`corroborated`、`inferred` 或 `unresolved`。
7. 靜態 frame 只能證明可見 state，不能證明 click 或因果結果。action claim 必須有 sequence、clip 或 interaction event。
8. 保留 loop、retry、alternative、contradiction 與缺失資訊。
9. 在綜整前，對每個選取的 segment 建立 evidence-atom pass。保留每一個精確的 field/question identifier、enumerated value、threshold、conditional phrase、source fallback、必要 screenshot 或保留 attachment。為每個 selected segment 給定 `consumed`、`duplicate`、`out_of_scope` 或 `unresolved` 的 disposition；籠統 workflow step 不算已消耗其 field-level atom。
10. 視覺 evidence 缺席時，明確的 transcript fact 仍維持 `stated`。不得以 `unknown` 取代已 stated 的 field、source、rule 或 deliverable component；若 readiness 需要 visual proof，應記錄 stated value 及其連結的 observation gap。
11. 將結果寫入 `20_distilled/derived/video/<evidence-id>/analysis/`，使用穩定的 segment ID 與 timecode，然後執行 `scripts/validate_knowledge_package.py`。
12. 將 structured knowledge 與 targeted gap 回傳給 `$distill-bu-knowledge`。若 visual evidence 不足以確認與開發相關的 I/O，應索取最小且具體的 follow-up evidence，不得虛構 action。

產出 `analysis/knowledge.json` 後，務必執行 `scripts/validate_knowledge_package.py`。只有有效的 package 才能合併至 engagement knowledge。
