---
name: prepare-audio-evidence
description: Prepare an authorized interview or business audio file for one BU engagement as a compact, timecoded and speaker-aware evidence package. Use as a worker invoked by distill-bu-knowledge for pure audio inputs or when a video's spoken track must be handled separately; preserve uncertainty and never claim screen actions from audio alone.
---

# Prepare Audio Evidence

Read [audio-evidence-contract.md](references/audio-evidence-contract.md) and [transcription-adapter-contract.md](references/transcription-adapter-contract.md).

1. Verify engagement, evidence ID, authorization, source hash, language and available transcription adapter.
2. Resolve the bundled workspace Python runtime and a confirmed local faster-whisper model path, then run `scripts/transcribe_media.py --model <local-model-path>` to create a local, timecoded transcript. The script rejects a non-local model name by default. Pass `--allow-model-download` only after the user explicitly authorizes network access for that run. If the configured model is absent, record the exact model, revision, expected files and offline staging requirement in the parent engagement's `download-ledger.csv`, then stop the transcription route.
3. Mark inaudible spans, uncertain words, overlapping speech, speaker uncertainty and adapter limitations.
4. Retain surrounding question context for decisions, exceptions and corrections.
5. For a walkthrough captured during `$conduct-bu-interview`, write the first validated package under `10_evidence/transcripts/<evidence-id>/` so the interview can review gaps before distillation. For externally supplied standalone media, write derived output under `20_distilled/derived/audio/<evidence-id>/`. Run `scripts/validate_audio_package.py` in both cases. Use `build_audio_manifest.py` only when normalizing an externally supplied transcript instead of running local transcription.
6. Preserve questions and statements about decision inputs, source and destination locations, download/export/upload/delivery methods, field requirements, output format, recipients and acceptance checks. Return these facts plus targeted gaps to `$distill-bu-knowledge` with timecodes. Spoken evidence remains `stated`; it does not prove the visible location or action.

Audio may support what a participant stated or explained. It cannot prove which screen, field, click or visible result occurred.

The post-recording transcript is final enough for gap review but is not a live streaming transcript. Preserve corrections in the interview record; do not silently rewrite raw evidence.

Default to a locally staged multilingual `small` model, CPU and `int8`. Pass only confirmed vocabulary from the Requirements Brief or supplied documents as `--initial-prompt` to improve domain-term recognition. Use a smaller model only for smoke tests or constrained machines. Do not claim speaker diarization; the local V1 adapter labels speakers as `speaker_unknown`.

Record the selected Python runtime, faster-whisper/CT2/AV dependency versions, model revision, cache/local path, size, hashes when available and whether the current run downloaded or reused them in `20_distilled/download-ledger.csv`.
