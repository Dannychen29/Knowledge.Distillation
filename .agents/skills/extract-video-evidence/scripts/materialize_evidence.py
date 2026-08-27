#!/usr/bin/env python3
"""Materialize representative frames and transcript slices for selected video segments."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


def load_segments(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return list(data.get("segments", [])) if isinstance(data, dict) else list(data)


def frame_targets(segment: dict, interval_ms: int, max_frames: int) -> list[int]:
    start = int(segment["start_ms"])
    end = int(segment["end_ms"])
    margin = min(1000, max(0, (end - start) // 10))
    targets = [start + margin, end - margin]
    cursor = start + interval_ms
    while cursor < end and len(targets) < max_frames:
        targets.append(cursor)
        cursor += interval_ms
    targets.append((start + end) // 2)
    return sorted(set(max(start, min(end - 1, value)) for value in targets))[:max_frames]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--frame-interval-seconds", type=float, default=5.0)
    parser.add_argument("--max-frames-per-segment", type=int, default=12)
    parser.add_argument("--jpeg-quality", type=int, default=88)
    args = parser.parse_args()

    video = args.video.expanduser().resolve()
    manifest_path = args.manifest.expanduser().resolve()
    package = manifest_path.parent
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    transcript = load_segments(args.transcript.expanduser().resolve())
    frame_dir = package / "frames"
    transcript_dir = package / "transcript"
    source_dir = package / "source"
    for folder in (frame_dir, transcript_dir, source_dir):
        folder.mkdir(parents=True, exist_ok=True)
    (source_dir / "source-pointer.txt").write_text(str(video) + "\n", encoding="utf-8")

    target_map: list[tuple[int, dict, int]] = []
    for segment in manifest.get("segments", []):
        for order, target in enumerate(frame_targets(
            segment,
            round(args.frame_interval_seconds * 1000),
            args.max_frames_per_segment,
        ), 1):
            target_map.append((target, segment, order))
    target_map.sort(key=lambda item: item[0])

    try:
        import av
    except ImportError as exc:
        raise SystemExit("PyAV is required in the selected Python runtime") from exc

    pending = 0
    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        for frame in container.decode(stream):
            if pending >= len(target_map):
                break
            time_sec = frame.time
            if time_sec is None:
                continue
            current_ms = round(time_sec * 1000)
            while pending < len(target_map) and current_ms >= target_map[pending][0]:
                target, segment, order = target_map[pending]
                name = f"{segment['segment_id']}_{order:02d}_{target:010d}.jpg"
                output = frame_dir / name
                image = frame.to_image().convert("RGB")
                image.save(output, quality=args.jpeg_quality, optimize=True)
                segment.setdefault("media", {}).setdefault("frames", []).append(f"frames/{name}")
                pending += 1

    for segment in manifest.get("segments", []):
        start, end = int(segment["start_ms"]), int(segment["end_ms"])
        items = [item for item in transcript if int(item.get("end_ms", 0)) > start and int(item.get("start_ms", 0)) < end]
        name = f"{segment['segment_id']}.txt"
        lines = [f"[{item.get('start_ms')}–{item.get('end_ms')}] {item.get('speaker', 'speaker_unknown')}: {item.get('text', '')}" for item in items]
        (transcript_dir / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
        segment.setdefault("media", {})["transcript"] = f"transcript/{name}"

    manifest["materialization"] = {
        "frames_extracted": sum(len(item.get("media", {}).get("frames", [])) for item in manifest.get("segments", [])),
        "clips_created": 0,
        "clip_limitation": "Physical clips are not created by the local V1 adapter; use source timecodes when motion evidence is required.",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sheets = []
    for segment in manifest.get("segments", []):
        frame_paths = [package / item for item in segment.get("media", {}).get("frames", [])]
        if not frame_paths:
            continue
        thumbs = []
        for path in frame_paths:
            image = Image.open(path).convert("RGB")
            image.thumbnail((320, 180), Image.Resampling.LANCZOS)
            thumbs.append((path.name, image.copy()))
        width = 640
        cell_h = 220
        rows = (len(thumbs) + 1) // 2
        sheet = Image.new("RGB", (width, max(cell_h, rows * cell_h)), "white")
        draw = ImageDraw.Draw(sheet)
        for index, (name, image) in enumerate(thumbs):
            x = (index % 2) * 320
            y = (index // 2) * cell_h
            sheet.paste(image, (x, y))
            draw.text((x + 4, y + 184), name, fill="black")
        sheet_path = frame_dir / f"{segment['segment_id']}_contact-sheet.jpg"
        sheet.save(sheet_path, quality=90)
        segment["media"]["contact_sheet"] = f"frames/{sheet_path.name}"
        sheets.append(str(sheet_path))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "completed", "manifest": str(manifest_path), "contact_sheets": sheets}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
