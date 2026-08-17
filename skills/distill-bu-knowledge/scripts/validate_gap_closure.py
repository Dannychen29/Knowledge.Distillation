#!/usr/bin/env python3
"""Validate an atomic gap-closure register."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


REQUIRED_COLUMNS = {
    "gap_id", "atom_id", "contract_id", "property", "fact", "status",
    "evidence_ids", "evidence_mode", "question", "smallest_evidence_needed",
    "owner", "impact", "closure_condition",
}
STATUSES = {"answered", "unresolved", "contradicted", "observation_missing", "out_of_scope"}
OPEN_STATUSES = {"unresolved", "contradicted", "observation_missing"}
EVIDENCE_MODES = {"observed", "stated", "corroborated", "inferred", "unresolved", "not_applicable"}


def normalized(value: str) -> str:
    return " ".join(value.casefold().split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", type=Path)
    args = parser.parse_args()
    path = args.register.resolve()
    errors: list[str] = []
    gaps: dict[str, list[tuple[int, dict[str, str]]]] = defaultdict(list)
    atom_ids: set[str] = set()
    question_rows: dict[str, list[tuple[int, str, str]]] = defaultdict(list)

    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - fields)
        if missing:
            errors.append("missing columns: " + ", ".join(missing))
        else:
            for row_number, raw in enumerate(reader, start=2):
                row = {key: (value or "").strip() for key, value in raw.items()}
                gap_id, atom_id, status = row["gap_id"], row["atom_id"], row["status"]
                if not gap_id or not atom_id:
                    errors.append(f"row {row_number}: blank gap_id or atom_id")
                    continue
                if atom_id in atom_ids:
                    errors.append(f"row {row_number}: duplicate atom_id {atom_id}")
                atom_ids.add(atom_id)
                gaps[gap_id].append((row_number, row))
                if status not in STATUSES:
                    errors.append(f"row {row_number}: unsupported status {status!r}")
                    continue
                if not row["contract_id"] or not row["property"] or not row["fact"]:
                    errors.append(f"row {row_number}: contract_id, property and fact are required")
                if row["evidence_mode"] not in EVIDENCE_MODES:
                    errors.append(f"row {row_number}: unsupported evidence_mode {row['evidence_mode']!r}")

                if status == "answered":
                    if not row["evidence_ids"]:
                        errors.append(f"row {row_number}: answered atom lacks evidence_ids")
                    if row["evidence_mode"] in {"unresolved", "not_applicable"}:
                        errors.append(f"row {row_number}: answered atom has non-evidentiary evidence_mode")
                    if row["question"] or row["smallest_evidence_needed"]:
                        errors.append(f"row {row_number}: answered atom must not ask a question or request evidence")
                elif status == "out_of_scope":
                    if row["question"] or row["smallest_evidence_needed"]:
                        errors.append(f"row {row_number}: out_of_scope atom must not ask a question or request evidence")
                else:
                    for field in ("question", "smallest_evidence_needed", "owner", "impact", "closure_condition"):
                        if not row[field]:
                            errors.append(f"row {row_number}: {status} atom lacks {field}")
                    question_key = normalized(row["question"])
                    if question_key:
                        question_rows[question_key].append((row_number, gap_id, atom_id))
                    if status == "observation_missing":
                        if not row["evidence_ids"] or row["evidence_mode"] not in {"stated", "inferred"}:
                            errors.append(
                                f"row {row_number}: observation_missing requires a stated/inferred claim and evidence_ids"
                            )

    for gap_id, rows in gaps.items():
        if not any(row["status"] in OPEN_STATUSES for _, row in rows):
            errors.append(f"{gap_id}: closed gap has no unresolved, contradicted or observation_missing atom")
    for matches in question_rows.values():
        if len(matches) > 1:
            locations = ", ".join(f"row {row} {gap}/{atom}" for row, gap, atom in matches)
            errors.append("same broad question reused across atoms: " + locations)

    if errors:
        print("INVALID")
        for error in errors:
            print("- " + error)
        return 1
    print(f"VALID: {path} ({len(gaps)} open gaps, {len(atom_ids)} atoms)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
