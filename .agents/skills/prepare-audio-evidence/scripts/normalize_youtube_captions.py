#!/usr/bin/env python3
"""Normalize a YouTube json3 caption track to the BU transcript contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--captions", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    source = json.loads(args.captions.read_text(encoding="utf-8-sig"))
    segments = []
    for event in source.get("events", []):
        start = int(event.get("tStartMs", 0))
        duration = int(event.get("dDurationMs", 0))
        text = "".join(str(item.get("utf8", "")) for item in event.get("segs", []))
        text = " ".join(text.replace("\n", " ").split()).strip()
        if not text or duration <= 0:
            continue
        segments.append({
            "segment_id": f"YTC-{len(segments) + 1:05d}",
            "start_ms": start,
            "end_ms": start + duration,
            "speaker": "speaker_unknown",
            "text": text,
            "confidence": None,
            "uncertainty": [],
        })

    segments.sort(key=lambda item: (item["start_ms"], item["end_ms"]))
    # Caption events may touch or slightly overlap. Preserve content while making
    # bounds monotonic for the shared audio evidence contract.
    normalized = []
    last_end = 0
    for item in segments:
        start = max(item["start_ms"], last_end)
        end = max(start + 1, item["end_ms"])
        item["start_ms"], item["end_ms"] = start, end
        normalized.append(item)
        last_end = end

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"schema_version": "1.0", "segments": normalized}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"segments": len(normalized), "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
