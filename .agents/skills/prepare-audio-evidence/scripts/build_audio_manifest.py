#!/usr/bin/env python3
"""Normalize timecoded transcript JSON into an audio evidence package."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stamp(ms: int) -> str:
    seconds, milli = divmod(ms, 1000)
    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    return f"{hour:02d}:{minute:02d}:{second:02d}.{milli:03d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--transcript", required=True, help="JSON list or object containing segments")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--engagement-id", required=True)
    parser.add_argument("--language", default="unknown")
    parser.add_argument("--method", default="existing_transcript")
    args = parser.parse_args()

    audio = Path(args.audio).resolve()
    source = json.loads(Path(args.transcript).read_text(encoding="utf-8-sig"))
    raw_segments = source.get("segments", []) if isinstance(source, dict) else source
    segments = []
    last_end = 0
    for index, raw in enumerate(raw_segments, 1):
        start = int(raw["start_ms"])
        end = int(raw["end_ms"])
        if start < 0 or end < start or start < last_end:
            raise ValueError(f"Invalid or non-monotonic time range at segment {index}")
        last_end = end
        segments.append({
            "segment_id": raw.get("segment_id", f"A{index:05d}"),
            "start_ms": start,
            "end_ms": end,
            "speaker": raw.get("speaker", "speaker_unknown"),
            "text": str(raw.get("text", "")).strip(),
            "confidence": raw.get("confidence"),
            "uncertainty": raw.get("uncertainty", []),
        })

    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcript.json").write_text(json.dumps({"segments": segments}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"[{stamp(s['start_ms'])}–{stamp(s['end_ms'])}] {s['speaker']}: {s['text']}" for s in segments]
    (out / "transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "1.0", "engagement_id": args.engagement_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"path": str(audio), "sha256": hash_file(audio), "size_bytes": audio.stat().st_size},
        "language": args.language, "transcription_method": args.method,
        "segment_count": len(segments), "speaker_label_method": "provided_or_unknown",
        "limitations": ["Audio provides no visual evidence.", "Speaker identity is not inferred."],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "quality-report.md").write_text(
        "# Audio evidence quality report\n\n"
        f"- Segments: {len(segments)}\n- Language: {args.language}\n- Method: {args.method}\n"
        "- Visual evidence: unavailable\n- Speaker identities: provided labels or unknown; not inferred\n",
        encoding="utf-8",
    )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
