from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def media_paths(segment: dict[str, Any]) -> list[str]:
    media = segment.get("media") or {}
    paths = []
    if media.get("clip"):
        paths.append(media["clip"])
    if media.get("transcript"):
        paths.append(media["transcript"])
    paths.extend(media.get("frames") or [])
    return [str(path) for path in paths]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an extract-video-evidence package.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 1

    if data.get("schema_version") != "1.0":
        errors.append("unsupported schema_version")
    segments = data.get("segments")
    if not isinstance(segments, list):
        errors.append("segments must be an array")
        segments = []

    ids: set[str] = set()
    previous_end = -1
    root = args.manifest.parent
    for index, segment in enumerate(segments):
        segment_id = segment.get("segment_id")
        if not isinstance(segment_id, str) or not segment_id:
            errors.append(f"segment {index} has no segment_id")
        elif segment_id in ids:
            errors.append(f"duplicate segment_id: {segment_id}")
        else:
            ids.add(segment_id)

        start = segment.get("start_ms")
        end = segment.get("end_ms")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            errors.append(f"{segment_id or index}: invalid time bounds")
        elif previous_end > start:
            warnings.append(f"{segment_id}: overlaps previous segment")
        if isinstance(end, int):
            previous_end = max(previous_end, end)

        if not segment.get("reasons"):
            errors.append(f"{segment_id or index}: missing selection reasons")
        if not isinstance(segment.get("confidence"), (int, float)):
            errors.append(f"{segment_id or index}: missing confidence")

        for path_text in media_paths(segment):
            path = Path(path_text)
            resolved = path if path.is_absolute() else root / path
            if not resolved.exists():
                errors.append(f"{segment_id or index}: missing media path {path_text}")

    unselected = data.get("unselected_intervals")
    if not isinstance(unselected, list):
        errors.append("unselected_intervals must be an array")
    else:
        for index, interval in enumerate(unselected):
            start = interval.get("start_ms")
            end = interval.get("end_ms")
            if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
                errors.append(f"unselected_intervals[{index}]: invalid time bounds")

    warnings.extend(str(item) for item in data.get("warnings", []) if item)
    result = {
        "valid": not errors,
        "segment_count": len(segments),
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

