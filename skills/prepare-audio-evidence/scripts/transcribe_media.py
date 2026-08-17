#!/usr/bin/env python3
"""Transcribe audio from an audio/video file locally with faster-whisper."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def timestamp(ms: int) -> str:
    seconds, millis = divmod(max(0, ms), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"


def media_duration_ms(path: Path) -> int | None:
    try:
        import av

        with av.open(str(path)) as container:
            if container.duration is not None:
                return round(container.duration / 1000)
            durations = []
            for stream in container.streams:
                if stream.duration is not None and stream.time_base is not None:
                    durations.append(float(stream.duration * stream.time_base))
            return round(max(durations) * 1000) if durations else None
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--engagement-id", required=True)
    parser.add_argument("--evidence-id", required=True)
    parser.add_argument(
        "--model",
        default=os.environ.get("BU_KNOWLEDGE_WHISPER_MODEL", "small"),
        help="Local faster-whisper model path. A model name is accepted only with --allow-model-download.",
    )
    parser.add_argument("--model-cache", type=Path)
    parser.add_argument(
        "--allow-model-download",
        action="store_true",
        help="Explicitly authorize faster-whisper to download a named model from its configured model hub.",
    )
    parser.add_argument("--language", default="auto", help="Language code such as zh/en, or auto")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--initial-prompt", default="", help="Confirmed domain terms or context; do not pass unverified facts")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        parser.error(f"source not found: {source}")
    out = args.out_dir.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit("faster-whisper is required in the selected Python runtime") from exc

    model_path = Path(args.model).expanduser()
    model_is_local = model_path.exists()
    if not model_is_local and not args.allow_model_download:
        raise SystemExit(
            "The configured faster-whisper model is not a local path. Stage the model locally and pass "
            "--model <path> (or set BU_KNOWLEDGE_WHISPER_MODEL), or explicitly authorize network access "
            "with --allow-model-download."
        )

    model_reference = str(model_path.resolve()) if model_is_local else args.model
    model_kwargs = {"device": args.device, "compute_type": args.compute_type}
    if args.model_cache:
        model_kwargs["download_root"] = str(args.model_cache.expanduser().resolve())
    model = WhisperModel(model_reference, **model_kwargs)
    language = None if args.language.lower() == "auto" else args.language
    segment_iter, info = model.transcribe(
        str(source),
        language=language,
        beam_size=args.beam_size,
        vad_filter=True,
        word_timestamps=True,
        condition_on_previous_text=True,
        initial_prompt=args.initial_prompt or None,
    )

    segments = []
    uncertain_count = 0
    for index, item in enumerate(segment_iter, 1):
        start_ms = max(0, round(float(item.start) * 1000))
        end_ms = max(start_ms, round(float(item.end) * 1000))
        uncertainty = []
        if getattr(item, "avg_logprob", 0.0) < -1.0:
            uncertainty.append("low_average_log_probability")
        if getattr(item, "no_speech_prob", 0.0) > 0.6:
            uncertainty.append("high_no_speech_probability")
        if uncertainty:
            uncertain_count += 1
        words = []
        for word in getattr(item, "words", None) or []:
            words.append({
                "start_ms": max(0, round(float(word.start) * 1000)),
                "end_ms": max(0, round(float(word.end) * 1000)),
                "text": word.word,
                "probability": round(float(word.probability), 4),
            })
        segments.append({
            "segment_id": f"AUD-{index:05d}",
            "start_ms": start_ms,
            "end_ms": end_ms,
            "speaker": "speaker_unknown",
            "text": item.text.strip(),
            "confidence": None,
            "uncertainty": uncertainty,
            "adapter_metrics": {
                "avg_logprob": round(float(getattr(item, "avg_logprob", 0.0)), 4),
                "no_speech_probability": round(float(getattr(item, "no_speech_prob", 0.0)), 4),
            },
            "words": words,
        })

    detected_language = getattr(info, "language", None) or args.language
    language_probability = getattr(info, "language_probability", None)
    duration_ms = media_duration_ms(source)
    transcript = {
        "schema_version": "1.0",
        "evidence_id": args.evidence_id,
        "language": detected_language,
        "segments": segments,
    }
    (out / "transcript.json").write_text(
        json.dumps(transcript, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    readable = [
        f"[{timestamp(item['start_ms'])}–{timestamp(item['end_ms'])}] "
        f"{item['speaker']}: {item['text']}"
        for item in segments
    ]
    (out / "transcript.txt").write_text("\n".join(readable) + "\n", encoding="utf-8")

    vtt = ["WEBVTT", ""]
    for index, item in enumerate(segments, 1):
        vtt.extend([
            str(index),
            f"{timestamp(item['start_ms'])} --> {timestamp(item['end_ms'])}",
            item["text"],
            "",
        ])
    (out / "transcript.vtt").write_text("\n".join(vtt), encoding="utf-8")

    limitations = [
        "Speaker diarization is unavailable; all speakers are speaker_unknown.",
        "Segment confidence is not fabricated; adapter metrics are retained instead.",
        "Audio alone does not prove screen actions.",
    ]
    manifest = {
        "schema_version": "1.0",
        "engagement_id": args.engagement_id,
        "evidence_id": args.evidence_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": str(source),
            "sha256": hash_file(source),
            "size_bytes": source.stat().st_size,
            "duration_ms": duration_ms,
        },
        "language": detected_language,
        "language_probability": round(float(language_probability), 4) if language_probability is not None else None,
        "transcription": {
            "engine": "faster-whisper",
            "model": model_reference,
            "model_is_local": model_is_local,
            "model_download_authorized": args.allow_model_download,
            "device": args.device,
            "compute_type": args.compute_type,
            "data_transfer_boundary": "local_processing_only",
            "word_timestamps": True,
            "diarization": False,
            "initial_prompt_used": bool(args.initial_prompt),
        },
        "segment_count": len(segments),
        "speaker_label_method": "speaker_unknown",
        "authorization": "inherited_from_source_evidence",
        "limitations": limitations,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report = [
        "# Audio evidence quality report",
        "",
        f"- Source: `{source}`",
        f"- Engine/model: `faster-whisper/{model_reference}`",
        f"- Detected language: `{detected_language}`",
        f"- Segments: {len(segments)}",
        f"- Segments flagged uncertain: {uncertain_count}",
        "- Speaker diarization: unavailable",
        "- Data processing: local; source audio is not sent to a transcription API",
        "- Visual evidence: unavailable from this package",
        "",
        "## Limitations",
        "",
        *[f"- {item}" for item in limitations],
    ]
    (out / "quality-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"status": "completed", "package": str(out), "segments": len(segments)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
