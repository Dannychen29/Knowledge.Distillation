---
name: extract-video-evidence
description: 將已授權的 business screen recording 或 video 縮減為單一 BU engagement 可追溯、附有 timecode 的 evidence package。由 distill-bu-knowledge 在深入 video analysis 前呼叫，尤其適用於長錄影；Codex 應選取高價值的 operation、decision、exception 與操作前／操作中／操作後 state，而非以最高成本分析整段 video。
---

# 擷取 Video Evidence

作為 `$distill-bu-knowledge` 的 media-reduction worker 運作。

處理 recording 時，閱讀 [selection-policy.md](references/selection-policy.md)、[timeline-contract.md](references/timeline-contract.md)、[media-adapter-contract.md](references/media-adapter-contract.md) 與 [evidence-package-contract.md](references/evidence-package-contract.md)。

1. 驗證 source evidence ID、authorization、hash、engagement 與 analysis goal。
2. 對 source video 與 local transcript 執行 `scripts/extract_media_timeline.py`，從語音與 visual change 建立低成本 timeline。沒有已核准 adapter 時，將 OCR 與 interaction event 回報為 unavailable。
3. 選取可高涵蓋的 segment，其中包括 operation、decision input 與 rationale、source acquisition/download、field entry 與 validation、destination upload/handoff、deliverable acceptance、exception、error、output 及參與者明確強調的內容。納入 system transition 與 handoff 前／操作中／操作後的 context。
4. 保留促成重要回答的 question 或 context，以及確認 action 的 result。
5. 執行 `scripts/materialize_evidence.py`，為每個選取的 segment 建立具 timecode 的 transcript slice、representative frame 與 contact sheet。需要檢視動態時，使用原始 video 加上 timecode。
6. 將 package 寫入 `20_distilled/derived/video/<evidence-id>/evidence-package/`，執行 `scripts/build_evidence_manifest.py`、materialize 其 evidence，並驗證 manifest。
7. 將 package 交給 `$analyze-video-evidence`。

不得僅因 interval 無聲、畫面靜止或缺少 transcript 而丟棄它。明確標記 privacy-blocked 與 low-confidence interval。
