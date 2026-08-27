---
name: prepare-audio-evidence
description: 將單一 BU engagement 已授權的 interview 或 business audio file 準備為精簡、附有 timecode 且具 speaker-aware 資訊的 evidence package。由 distill-bu-knowledge 處理純 audio input，或 video 的 spoken track 必須分開處理時呼叫；保留不確定性，且不得僅憑 audio 宣稱 screen action。
---

# 準備 Audio Evidence

閱讀 [audio-evidence-contract.md](references/audio-evidence-contract.md) 與 [transcription-adapter-contract.md](references/transcription-adapter-contract.md)。

1. 驗證 engagement、evidence ID、authorization、source hash、language 與可用的 transcription adapter。
2. 找出 bundled workspace Python runtime 與已確認的 local faster-whisper model path，然後執行 `scripts/transcribe_media.py --model <local-model-path>` 建立 local、附有 timecode 的 transcript。此 script 預設拒絕 non-local model name。僅在使用者明確授權該 run 使用 network access 後，才傳入 `--allow-model-download`。若設定的 model 不存在，於上層 engagement 的 `download-ledger.csv` 記錄確切 model、revision、預期 file 與 offline staging requirement，然後停止 transcription route。
3. 標記 inaudible span、uncertain word、overlapping speech、speaker uncertainty 與 adapter limitation。
4. 保留 decision、exception 與 correction 的前後 question context。
5. 對 `$conduct-bu-interview` 期間錄製的 walkthrough，將第一份已驗證 package 寫入 `10_evidence/transcripts/<evidence-id>/`，讓 interview 可在 distillation 前審閱 gap。對外部提供的 standalone media，將 derived output 寫入 `20_distilled/derived/audio/<evidence-id>/`。兩種情況都執行 `scripts/validate_audio_package.py`。只有在正規化外部提供的 transcript、而非執行 local transcription 時，才使用 `build_audio_manifest.py`。
6. 保留關於 decision input、source 與 destination location、download/export/upload/delivery method、field requirement、output format、recipient 與 acceptance check 的 question 與 statement。將這些 fact 與 targeted gap 附帶 timecode 回傳給 `$distill-bu-knowledge`。spoken evidence 仍屬 `stated`；它無法證明 visible location 或 action。

audio 可以支持參與者所述或解釋的內容，但無法證明出現的是哪個 screen、field、click 或 visible result。

錄製後的 transcript 已足以進行 gap review，但不是 live streaming transcript。將 correction 保留於 interview record；不得悄悄改寫 raw evidence。

預設使用 locally staged multilingual `small` model、CPU 與 `int8`。僅將 Requirements Brief 或提供文件中已確認的 vocabulary 作為 `--initial-prompt` 傳入，以改善 domain-term recognition。僅在 smoke test 或受限 machine 時使用較小 model。不得宣稱有 speaker diarization；local V1 adapter 將 speaker 標示為 `speaker_unknown`。

在 `20_distilled/download-ledger.csv` 記錄選用的 Python runtime、faster-whisper/CT2/AV dependency version、model revision、cache/local path、size、可用時的 hash，以及本 run 是下載還是重用這些項目。
