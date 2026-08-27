---
name: record-bu-walkthrough
description: 由 Codex 控制已授權的 Windows business screen walkthrough，包含 preflight、啟用 microphone 的 start、stop、file discovery、audio-track check、hashing 與附加至 active BU engagement。當 interview 發現必須觀察實際 screen operation 或 spoken decision rationale 的 gap 時使用；未取得明確的 screen 與 microphone consent 時不得使用。
---

# 錄製 BU Walkthrough

僅針對一個 active engagement 中已具名的 information gap 使用此 worker。

此 worker 為 optional。不得對每個 interview、每個 process，或僅因可錄製就呼叫它。僅在 `$conduct-bu-interview` 判定短時間的 screen walkthrough 是補足 material gap 的最小可靠方式後才呼叫。

在同一台 machine 首次錄製前，閱讀 [windows-game-bar.md](references/windows-game-bar.md)。

## 工作流程

1. 說明需要錄製的 application 與 operation、要補足的 gap、必須有 microphone narration，以及 file 儲存位置。
2. 請參與者關閉無關的 sensitive application、開啟 target app，並明確同意 screen 與 microphone recording。
3. 執行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/recording_control.ps1 -Action check -EngagementPath <path>`。
4. 若 `ready` 為 false，說明未通過的 check 並索取最小的 fallback evidence。不得模擬成功。
5. 明確同意後，執行 `-Action start -Confirmed`。告知參與者已請求開始 recording，且僅提供第一個 operation prompt。
6. 讓參與者操作並口述每項重要選擇的原因。不得接手 business decision。
7. 當參與者表示 walkthrough 完成時，找出 bundled workspace Python executable 與已確認的 local faster-whisper model path，接著執行 `-Action stop -PythonPath <bundled-python> -TranscriptionModel <local-model-path> -TranscriptionBeamSize 1`。僅在明確授權該 run 後，才傳入 `-AllowModelDownload`。這會停止 recording、登錄 MP4，並在 `10_evidence/transcripts/<evidence-id>/` 建立快速 local transcript；不會執行完整 video distillation。
8. 回報已儲存的 evidence ID、copied path、hash、`audio_track_detected`、transcript path 與 transcript status。若未偵測到 audio track，保留 file 但標記為 incomplete，並安排有口述的重錄或 targeted audio follow-up。
9. 將控制權交回 `$conduct-bu-interview`。它必須根據已具名 gap 檢視 transcript，必要時提出 targeted follow-up，並在 `$distill-bu-knowledge` 開始 visual analysis 前取得參與者確認。

## 範圍界線

- Codex 操作 recorder；參與者操作 business application。
- Xbox Game Bar 錄製 foreground application，不保證能錄到完整 desktop 或 multi-window session。
- 不得錄製 credential、無關的 personal information 或未核准 application。
- recording 及其附有 timecode 的 transcript 屬於 interview evidence。`$distill-bu-knowledge` 重用已驗證 transcript，並決定哪些 visual interval 需要 analysis。
