#!/usr/bin/env python3
"""Run the deterministic local audio/video preprocessing pipeline for one engagement."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".wma"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".wmv", ".m4v"}


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_engagement_id(engagement: Path) -> str:
    descriptor = engagement / "engagement.yaml"
    if not descriptor.is_file():
        raise ValueError(f"not an engagement folder: {engagement}")
    for line in descriptor.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("engagement_id:"):
            value = line.split(":", 1)[1].strip().strip('"')
            if value:
                return value
    raise ValueError("engagement.yaml has no engagement_id")


def confirmed_context(engagement: Path) -> str:
    brief = engagement / "00_intake" / "requirements-brief.md"
    if not brief.is_file():
        return ""
    lines = []
    for raw in brief.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and line not in {"- 狀態：待確認", "- 確認人：", "- 確認時間："}:
            lines.append(line)
    return " ".join(lines)[:1200]


def resolve_evidence_id(engagement: Path, source: Path, source_sha256: str) -> str:
    """Reuse the registered evidence ID for the same stored file or content."""
    manifest = engagement / "10_evidence" / "evidence-manifest.json"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8-sig"))
        source_key = str(source.resolve()).casefold()
        for item in data.get("items", []):
            stored = item.get("stored_path")
            same_path = bool(stored) and str(Path(stored).expanduser().resolve()).casefold() == source_key
            same_hash = bool(item.get("sha256")) and item.get("sha256", "").casefold() == source_sha256.casefold()
            if (same_path or same_hash) and item.get("evidence_id"):
                return item["evidence_id"]
    return f"EVD-MEDIA-{source_sha256[:12].upper()}"


def validate_captured_transcript(package: Path, evidence_id: str, source_sha256: str) -> bool:
    transcript_path = package / "transcript.json"
    manifest_path = package / "manifest.json"
    if not transcript_path.is_file():
        return False
    if not manifest_path.is_file():
        raise ValueError(f"captured transcript manifest missing: {manifest_path}")
    transcript = json.loads(transcript_path.read_text(encoding="utf-8-sig"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    transcript_evidence_id = transcript.get("evidence_id")
    transcript_sha256 = str(manifest.get("source", {}).get("sha256", ""))
    if transcript_evidence_id != evidence_id:
        raise ValueError(f"captured transcript evidence ID mismatch: {transcript_evidence_id} != {evidence_id}")
    if transcript_sha256.casefold() != source_sha256.casefold():
        raise ValueError("captured transcript source hash does not match recording")
    return True


def update_evidence_manifest(engagement: Path, result: dict) -> None:
    path = engagement / "10_evidence" / "evidence-manifest.json"
    data = json.loads(path.read_text(encoding="utf-8-sig")) if path.is_file() else {"engagement_id": result["engagement_id"], "items": []}
    items = [item for item in data.get("items", []) if item.get("evidence_id") != result["evidence_id"]]
    prior = next((item for item in data.get("items", []) if item.get("evidence_id") == result["evidence_id"]), {})
    prior.update({
        "evidence_id": result["evidence_id"],
        "type": "screen_recording" if result["media_kind"] == "video" else "audio",
        "stored_path": result["source"],
        "sha256": result["source_sha256"],
        "derived_audio_package": result["audio_package"],
        "transcript_package": result["audio_package"],
        "transcript_reused": result.get("transcript_reused", False),
        "derived_video_package": result["video_package"],
        "processing_status": result["status"],
        "processed_at": result["created_at_utc"],
    })
    items.append(prior)
    data["items"] = items
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(command: list[str]) -> None:
    print("RUN " + " ".join(command), flush=True)
    completed = subprocess.run(command, text=True)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engagement", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--evidence-id")
    parser.add_argument("--goal", default="Extract business operations, decisions, exceptions, rationale and outputs")
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="auto")
    parser.add_argument("--analysis-mode", choices=("transcript-only", "targeted", "audit"), default="targeted")
    parser.add_argument("--sample-seconds", type=float)
    parser.add_argument("--beam-size", type=int)
    parser.add_argument("--initial-prompt", default="", help="Confirmed vocabulary/context for local transcription")
    parser.add_argument("--allow-model-download", action="store_true", help="Explicitly authorize downloading a named transcription model")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    engagement = args.engagement.expanduser().resolve()
    source = args.source.expanduser().resolve()
    if not source.is_file():
        parser.error(f"source not found: {source}")
    engagement_id = read_engagement_id(engagement)
    source_sha256 = hash_file(source)
    evidence_id = args.evidence_id or resolve_evidence_id(engagement, source, source_sha256)
    kind = "video" if source.suffix.lower() in VIDEO_EXTENSIONS else "audio" if source.suffix.lower() in AUDIO_EXTENSIONS else None
    if not kind:
        parser.error(f"unsupported media extension: {source.suffix}")

    skills_root = Path(__file__).resolve().parents[2]
    transcriber = skills_root / "prepare-audio-evidence" / "scripts" / "transcribe_media.py"
    audio_validator = skills_root / "prepare-audio-evidence" / "scripts" / "validate_audio_package.py"
    timeline_builder = skills_root / "extract-video-evidence" / "scripts" / "extract_media_timeline.py"
    manifest_builder = skills_root / "extract-video-evidence" / "scripts" / "build_evidence_manifest.py"
    materializer = skills_root / "extract-video-evidence" / "scripts" / "materialize_evidence.py"
    evidence_validator = skills_root / "analyze-video-evidence" / "scripts" / "validate_evidence_package.py"

    derived = engagement / "20_distilled" / "derived"
    captured_transcript_package = engagement / "10_evidence" / "transcripts" / evidence_id
    transcript_reused = (
        not args.force
        and validate_captured_transcript(captured_transcript_package, evidence_id, source_sha256)
    )
    audio_package = captured_transcript_package if transcript_reused else derived / "audio" / evidence_id
    transcript_json = audio_package / "transcript.json"
    beam_size = args.beam_size or (5 if args.analysis_mode == "audit" else 1)
    sample_seconds = args.sample_seconds or (1.0 if args.analysis_mode == "audit" else 5.0)
    if args.force or not transcript_json.is_file():
        initial_prompt = args.initial_prompt or confirmed_context(engagement)
        transcribe_command = [
            sys.executable, str(transcriber),
            "--source", str(source),
            "--out-dir", str(audio_package),
            "--engagement-id", engagement_id,
            "--evidence-id", evidence_id,
            "--model", args.model,
            "--language", args.language,
            "--beam-size", str(beam_size),
        ]
        if initial_prompt:
            transcribe_command.extend(["--initial-prompt", initial_prompt])
        if args.allow_model_download:
            transcribe_command.append("--allow-model-download")
        run(transcribe_command)
    run([sys.executable, str(audio_validator), str(audio_package)])

    result = {
        "schema_version": "1.0",
        "engagement_id": engagement_id,
        "evidence_id": evidence_id,
        "source": str(source),
        "source_sha256": source_sha256,
        "media_kind": kind,
        "analysis_mode": args.analysis_mode,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "audio_package": str(audio_package),
        "transcript_reused": transcript_reused,
        "video_package": None,
        "next_action": "distill_audio_evidence",
        "status": "ready_for_semantic_distillation",
    }

    if kind == "video" and args.analysis_mode != "transcript-only":
        video_root = derived / "video" / evidence_id
        timeline = video_root / "timeline.json"
        package = video_root / "evidence-package"
        run([
            sys.executable, str(timeline_builder),
            "--video", str(source),
            "--transcript", str(transcript_json),
            "--out", str(timeline),
            "--sample-seconds", str(sample_seconds),
        ])
        selection = [
            sys.executable, str(manifest_builder),
            "--timeline", str(timeline),
            "--source", str(source),
            "--goal", args.goal,
            "--out", str(package),
        ]
        if args.analysis_mode == "targeted":
            selection.extend(["--min-score", "0.46", "--context-before-ms", "3000", "--context-after-ms", "5000", "--merge-gap-ms", "3000"])
        run(selection)
        materialize = [
            sys.executable, str(materializer),
            "--video", str(source),
            "--manifest", str(package / "manifest.json"),
            "--transcript", str(transcript_json),
        ]
        if args.analysis_mode == "targeted":
            materialize.extend(["--frame-interval-seconds", "10", "--max-frames-per-segment", "6"])
        run(materialize)
        run([sys.executable, str(evidence_validator), str(package / "manifest.json")])
        result["video_package"] = str(package)
        result["next_action"] = "invoke_analyze-video-evidence_then_distill-bu-knowledge"
        result["status"] = "ready_for_video_analysis"

    result_path = derived / kind / evidence_id / "pipeline-result.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    update_evidence_manifest(engagement, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
