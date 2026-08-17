#!/usr/bin/env python3
"""Build a low-cost timeline from video frames and a timecoded transcript."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def load_transcript(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return list(data.get("segments", [])) if isinstance(data, dict) else list(data)


def speech_for_interval(segments: list[dict], start_ms: int, end_ms: int) -> tuple[str, list[str]]:
    matches = [
        item for item in segments
        if int(item.get("end_ms", 0)) > start_ms and int(item.get("start_ms", 0)) < end_ms
    ]
    text = " ".join(str(item.get("text", "")).strip() for item in matches if item.get("text"))
    refs = [str(item.get("segment_id")) for item in matches if item.get("segment_id")]
    return text, refs


def frame_context(gray: np.ndarray) -> dict[str, float]:
    white_ratio = float(np.mean(gray >= 215.0))
    dark_ratio = float(np.mean(gray <= 45.0))
    if gray.shape[0] > 1 and gray.shape[1] > 1:
        horizontal = np.abs(np.diff(gray, axis=1))
        vertical = np.abs(np.diff(gray, axis=0))
        edge_density = float((np.mean(horizontal > 18.0) + np.mean(vertical > 18.0)) / 2.0)
    else:
        edge_density = 0.0

    document_score = max(0.0, min(1.0, white_ratio * 0.75 + edge_density * 2.4 - dark_ratio * 0.35))
    meeting_score = max(0.0, min(1.0, dark_ratio * 0.85 + (1.0 - white_ratio) * 0.10 - edge_density * 1.1))
    return {
        "white_ratio": round(white_ratio, 4),
        "dark_ratio": round(dark_ratio, 4),
        "edge_density": round(edge_density, 4),
        "document_score": round(document_score, 4),
        "meeting_score": round(meeting_score, 4),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--sample-seconds", type=float, default=1.0)
    parser.add_argument("--preview-width", type=int, default=320)
    args = parser.parse_args()

    source = args.video.expanduser().resolve()
    if not source.is_file():
        parser.error(f"video not found: {source}")
    transcript = load_transcript(args.transcript.expanduser().resolve())

    try:
        import av
    except ImportError as exc:
        raise SystemExit("PyAV is required in the selected Python runtime") from exc

    observations = []
    previous_gray = None
    next_sample = 0.0
    duration_ms = 0
    stream_meta = {}
    with av.open(str(source)) as container:
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        stream_meta = {
            "codec": stream.codec_context.name,
            "width": stream.codec_context.width,
            "height": stream.codec_context.height,
            "average_rate": float(stream.average_rate) if stream.average_rate else None,
        }
        if container.duration is not None:
            duration_ms = round(container.duration / 1000)
        for frame in container.decode(stream):
            time_sec = frame.time
            if time_sec is None or time_sec + 1e-6 < next_sample:
                continue
            image = frame.to_image().convert("L")
            height = max(1, round(image.height * args.preview_width / image.width))
            gray = np.asarray(image.resize((args.preview_width, height), Image.Resampling.BILINEAR), dtype=np.float32)
            context = frame_context(gray)
            visual_change = 0.0 if previous_gray is None else float(np.mean(np.abs(gray - previous_gray)) / 255.0)
            start_ms = max(0, round(time_sec * 1000))
            end_ms = start_ms + max(1, round(args.sample_seconds * 1000))
            speech, transcript_refs = speech_for_interval(transcript, start_ms, end_ms)
            tags = []
            if speech:
                tags.append("answer")
            if visual_change >= 0.08:
                tags.append("visual_change")
            if context["document_score"] >= 0.35:
                tags.append("document_surface")
            if context["meeting_score"] >= 0.55 and context["document_score"] < 0.25:
                tags.append("meeting_grid")
            observations.append({
                "start_ms": start_ms,
                "end_ms": end_ms,
                "speech_text": speech,
                "ocr_text": "",
                "visual_change": round(min(visual_change, 1.0), 4),
                "interaction": False,
                "visual_context": context,
                "manual_keep": False,
                "privacy_blocked": False,
                "source_refs": [f"transcript:{item}" for item in transcript_refs],
                "tags": tags,
            })
            previous_gray = gray
            next_sample = time_sec + args.sample_seconds

    if observations:
        duration_ms = max(duration_ms, observations[-1]["end_ms"])
        observations[-1]["end_ms"] = max(observations[-1]["start_ms"] + 1, duration_ms)
    result = {
        "schema_version": "1.0",
        "source": str(source),
        "duration_ms": duration_ms,
        "sample_seconds": args.sample_seconds,
        "signals": {
            "speech": True,
            "visual_change": True,
            "ocr": False,
            "interaction_events": False,
        },
        "video": stream_meta,
        "warnings": ["ocr_unavailable", "interaction_events_unavailable"],
        "observations": observations,
    }
    out = args.out.expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "completed", "timeline": str(out), "observations": len(observations)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
