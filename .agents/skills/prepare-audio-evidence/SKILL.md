---
name: prepare-audio-evidence
description: 為 elicit-business-knowledge 準備已授權的音訊與逐字稿，保留時間碼、說話者不確定性及來源；音訊不能證明畫面操作。
---

# 準備 Audio Evidence

閱讀 [audio-evidence-contract.md](references/audio-evidence-contract.md) 與 [transcription-adapter-contract.md](references/transcription-adapter-contract.md)。

1. 驗證 engagement、evidence ID、authorization、source hash、language 與可用的 transcription adapter。
2. 找出可用 Python runtime 與已確認的 local faster-whisper model path，然後執行 `scripts/transcribe_media.py --model <local-model-path>` 建立 local、附有 timecode 的 transcript。此 script 預設拒絕 non-local model name。僅在使用者明確授權該 run 使用 network access 後，才傳入 `--allow-model-download`。若設定的 model 不存在，在 active run 的 `evidence/download-ledger.csv` 記錄確切 model、revision、預期 file 與 offline staging requirement，回 elicit 說明限制並使用可用材料。
3. 標記 inaudible span、uncertain word、overlapping speech、speaker uncertainty 與 adapter limitation。
4. 保留 decision、exception 與 correction 的前後 question context。
5. 將 package 寫入 active run 的 `evidence/audio/<evidence-id>/`，執行 `scripts/validate_audio_package.py`。正規化外部 transcript 時使用 `build_audio_manifest.py`。
6. 保留 decision、rationale、exception、input/output、handoff 的 question context。帶 timecode 回傳 `$elicit-business-knowledge`。spoken evidence 仍為 stated，不能證明 visible action。

audio 可以支持參與者所述或解釋的內容，但無法證明出現的是哪個 screen、field、click 或 visible result。

錄製後的 transcript 已足以進行 gap review，但不是 live streaming transcript。將 correction 保留於 interview record；不得悄悄改寫 raw evidence。

預設使用 locally staged multilingual `small` model、CPU 與 `int8`。僅將 engagement、已確認知識或提供文件中的 vocabulary 作為 `--initial-prompt` 傳入，以改善 domain-term recognition，不要求另外準備 Requirements Brief。僅在 smoke test 或受限 machine 時使用較小 model。不得宣稱有 speaker diarization；local V1 adapter 將 speaker 標示為 `speaker_unknown`。

在 active run 的 `evidence/download-ledger.csv` 記錄 Python、dependency、model revision/path/size/hash 及下載或重用狀態。若無預先設定 runtime，可使用當前可用 Python；不得假設存在 bundled runtime。
