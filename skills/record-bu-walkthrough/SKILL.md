---
name: record-bu-walkthrough
description: Control an authorized Windows business screen walkthrough from Codex, including preflight, microphone-enabled start, stop, file discovery, audio-track check, hashing and attachment to the active BU engagement. Use when an interview identifies a gap that requires observing actual screen operations or spoken decision rationale. Do not use without explicit screen and microphone consent.
---

# Record BU Walkthrough

Use this worker only for a named information gap in one active engagement.

This worker is optional. Do not invoke it for every interview, every process, or merely because recording is available. Invoke it only after `$conduct-bu-interview` determines that a short screen walkthrough is the smallest reliable way to close a material gap.

Read [windows-game-bar.md](references/windows-game-bar.md) before the first recording on a machine.

## Workflow

1. State what application and operation need recording, what gap it resolves, that microphone narration is required, and where the file will be stored.
2. Ask the participant to close unrelated sensitive applications, open the target app and explicitly approve screen plus microphone recording.
3. Run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/recording_control.ps1 -Action check -EngagementPath <path>`.
4. If `ready` is false, explain the failed checks and request the smallest fallback evidence. Do not simulate success.
5. After explicit approval, run `-Action start -Confirmed`. Tell the participant recording has been requested and give only the first operation prompt.
6. Let the participant operate and narrate why each important choice is made. Do not take over the business decision.
7. When the participant says the walkthrough is complete, resolve the bundled workspace Python executable and a confirmed local faster-whisper model path, then run `-Action stop -PythonPath <bundled-python> -TranscriptionModel <local-model-path> -TranscriptionBeamSize 1`. Pass `-AllowModelDownload` only after explicit authorization for that run. This stops recording, registers the MP4 and creates a fast local transcript under `10_evidence/transcripts/<evidence-id>/`. It does not run full video distillation.
8. Report the saved evidence ID, copied path, hash, `audio_track_detected`, transcript path and transcript status. If no audio track is detected, retain the file but mark it incomplete and arrange a narrated redo or targeted audio follow-up.
9. Return control to `$conduct-bu-interview`. It must inspect the transcript against the named gap, ask a targeted follow-up when needed and obtain participant confirmation before `$distill-bu-knowledge` starts visual analysis.

## Boundaries

- Codex operates the recorder; the participant operates the business application.
- Xbox Game Bar records the foreground application, not a guaranteed full-desktop or multi-window session.
- Never record credentials, unrelated personal information or unapproved applications.
- A recording and its timecoded transcript are interview evidence. `$distill-bu-knowledge` reuses the validated transcript and decides which visual intervals require analysis.
