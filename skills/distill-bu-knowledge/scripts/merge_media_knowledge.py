#!/usr/bin/env python3
"""Merge one validated media knowledge package into engagement-level draft assets."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

CATEGORIES = (
    "processes", "operational_steps", "decisions", "exceptions", "pain_points",
    "systems", "data_objects", "data_flows", "deliverables",
)
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engagement", required=True, type=Path)
    parser.add_argument("--evidence-id", required=True)
    parser.add_argument("--knowledge", required=True, type=Path)
    args = parser.parse_args()

    engagement = args.engagement.expanduser().resolve()
    knowledge_path = args.knowledge.expanduser().resolve()
    data = json.loads(knowledge_path.read_text(encoding="utf-8-sig"))
    distilled = engagement / "20_distilled"
    media_dir = distilled / "media-knowledge"
    media_dir.mkdir(parents=True, exist_ok=True)
    target = media_dir / f"{args.evidence_id}.json"
    shutil.copy2(knowledge_path, target)

    rows = []
    counts = {}
    for category in CATEGORIES:
        items = data.get(category, [])
        counts[category] = len(items)
        for item in items:
            references = item.get("evidence", [])
            location = "; ".join(
                f"{ref.get('segment_id')}:{ref.get('start_ms')}-{ref.get('end_ms')}ms"
                for ref in references
            )
            rows.append({
                "claim_id": item.get("id", ""),
                "claim_type": category,
                "statement": item.get("statement", ""),
                "source_id": args.evidence_id,
                "source_location": location,
                "evidence_mode": item.get("evidence_mode", ""),
                "confidence": item.get("confidence", ""),
                "status": "draft",
            })

    ledger_path = distilled / "evidence-ledger.csv"
    fieldnames = ["claim_id", "claim_type", "statement", "source_id", "source_location", "evidence_mode", "confidence", "status"]
    existing = []
    if ledger_path.is_file():
        with ledger_path.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = [row for row in csv.DictReader(handle) if row.get("source_id") != args.evidence_id]
    with ledger_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing + rows)

    result = {
        "status": "merged",
        "evidence_id": args.evidence_id,
        "knowledge_asset": str(target),
        "claims_added": len(rows),
        "category_counts": counts,
        "evidence_ledger": str(ledger_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
