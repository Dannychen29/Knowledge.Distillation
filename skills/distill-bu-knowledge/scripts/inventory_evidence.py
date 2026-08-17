#!/usr/bin/env python3
"""Inventory evidence files and emit a deterministic routing plan."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

KINDS = {
    "text": {".txt", ".md", ".csv", ".tsv", ".json", ".yaml", ".yml", ".xml"},
    "document": {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"},
    "audio": {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".wma"},
    "video": {".mp4", ".mov", ".mkv", ".avi", ".webm", ".wmv", ".m4v"},
    "image": {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"},
}
ROUTES = {
    "text": ["direct-text-extraction"],
    "document": ["document-extraction"],
    "audio": ["prepare-audio-evidence"],
    "video": ["extract-video-evidence", "analyze-video-evidence"],
    "image": ["direct-visual-inspection"],
    "unsupported": ["manual-review"],
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    return next((kind for kind, suffixes in KINDS.items() if suffix in suffixes), "unsupported")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("engagement", help="Engagement folder containing engagement.yaml")
    parser.add_argument("--out", help="Output JSON path; defaults to 20_distilled/evidence-inventory.json")
    args = parser.parse_args()

    engagement = Path(args.engagement).expanduser().resolve()
    descriptor = engagement / "engagement.yaml"
    if not descriptor.is_file():
        parser.error(f"not an engagement folder: {engagement}")
    engagement_id = ""
    for line in descriptor.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("engagement_id:"):
            engagement_id = line.split(":", 1)[1].strip().strip('"')
            break
    if not engagement_id:
        parser.error("engagement.yaml has no engagement_id")

    roots = [engagement / "00_intake", engagement / "10_evidence"]
    files: set[Path] = set()
    missing: list[str] = []
    for path in roots:
        if not path.exists():
            missing.append(str(path))
        else:
            files.update(item for item in path.rglob("*") if item.is_file() and item.name != ".gitkeep")

    records = []
    counts: Counter[str] = Counter()
    for path in sorted(files, key=lambda item: str(item).casefold()):
        kind = classify(path)
        counts[kind] += 1
        records.append({
            "path": str(path), "kind": kind, "routes": ROUTES[kind],
            "size_bytes": path.stat().st_size, "sha256": sha256(path),
        })

    result = {
        "schema_version": "1.0",
        "engagement_id": engagement_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "counts": dict(sorted(counts.items())),
        "files": records,
        "warnings": [f"missing input: {item}" for item in missing],
    }
    output = Path(args.out).resolve() if args.out else engagement / "20_distilled" / "evidence-inventory.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0 if records and not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
