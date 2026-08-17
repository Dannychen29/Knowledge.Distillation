#!/usr/bin/env python3
"""Validate the minimum audio evidence package contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = ("manifest.json", "transcript.json", "transcript.txt", "quality-report.md")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package")
    args = parser.parse_args()
    root = Path(args.package).resolve()
    errors = [f"missing {name}" for name in REQUIRED if not (root / name).is_file()]
    if not errors:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        transcript = json.loads((root / "transcript.json").read_text(encoding="utf-8"))
        segments = transcript.get("segments", [])
        if manifest.get("segment_count") != len(segments):
            errors.append("manifest segment_count does not match transcript")
        previous = 0
        for index, segment in enumerate(segments, 1):
            if segment["start_ms"] < previous or segment["end_ms"] < segment["start_ms"]:
                errors.append(f"invalid timestamp order at segment {index}")
            previous = segment["end_ms"]
    if errors:
        print("INVALID: " + "; ".join(errors))
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
