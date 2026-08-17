#!/usr/bin/env python3
"""Validate the structural executability of a canonical BRD.html."""
from __future__ import annotations

import argparse
import csv
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_SECTIONS = {
    "metadata", "outcome", "actors-and-systems", "workflow", "operational-steps",
    "decisions", "data-objects", "data-flows", "deliverables",
    "exceptions-and-controls", "requirements", "acceptance-scenarios",
    "gaps-and-readiness", "traceability",
}
STEP_PROPERTIES = {
    "trigger", "preconditions", "actor", "source-system", "source-location",
    "acquisition-method", "selection-basis", "input-object", "input-fields",
    "action", "transformation", "output-object", "output-formation-rule",
    "destination-system", "destination-location", "content-validation",
    "completion-condition", "completion-evidence", "failure-fallback", "evidence", "gaps",
}
VAGUE = {
    "process", "handle", "review", "complete", "get the list", "create case",
    "取得名單", "建立案件", "處理資料", "確認完整", "填寫表單", "上傳檔案",
}


class ContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.steps: dict[str, dict] = {}
        self.property_counts: dict[tuple[str, str], int] = {}
        self.current_step: str | None = None
        self.current_property: str | None = None
        self.property_depth = 0
        self.lang: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html":
            self.lang = data.get("lang")
        item_id = data.get("id")
        if item_id:
            self.ids.append(item_id)
        href = data.get("href") or ""
        if href.startswith("#"):
            self.hrefs.append(href[1:])
        if tag == "article" and data.get("data-contract-type") == "step":
            self.current_step = item_id or "<step-without-id>"
            self.steps[self.current_step] = {"attrs": data, "properties": {}}
        prop = data.get("data-step-property")
        if self.current_step and prop:
            self.property_counts[(self.current_step, prop)] = self.property_counts.get((self.current_step, prop), 0) + 1
            self.current_property = prop
            self.property_depth = 1
            self.steps[self.current_step]["properties"].setdefault(prop, "")
        elif self.current_step and self.current_property:
            self.property_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "article":
            self.current_step = None
            self.current_property = None
            self.property_depth = 0
        elif self.current_property:
            self.property_depth -= 1
            if self.property_depth <= 0:
                self.current_property = None
                self.property_depth = 0

    def handle_data(self, data: str) -> None:
        if self.current_step and self.current_property:
            props = self.steps[self.current_step]["properties"]
            props[self.current_property] += " " + data.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brd", type=Path)
    parser.add_argument(
        "--expectations", type=Path,
        help="Optional CSV with step_id,property,must_contain,evidence_id. "
             "Use it to prove evidence-backed atoms survived source-to-HTML rendering.",
    )
    args = parser.parse_args()
    path = args.brd.resolve()
    document = path.read_text(encoding="utf-8")
    parsed = ContractParser()
    parsed.feed(document)
    errors: list[str] = []
    id_set = set(parsed.ids)
    if len(id_set) != len(parsed.ids):
        errors.append("duplicate HTML ids")
    missing_sections = sorted(REQUIRED_SECTIONS - id_set)
    if missing_sections:
        errors.append("missing sections: " + ", ".join(missing_sections))
    broken = sorted({ref for ref in parsed.hrefs if ref not in id_set})
    if broken:
        errors.append("broken anchors: " + ", ".join(broken))
    if not parsed.steps:
        errors.append("no article[data-contract-type=step] contracts")
    for step_id, step in parsed.steps.items():
        props = step["properties"]
        missing = sorted(STEP_PROPERTIES - set(props))
        if missing:
            errors.append(f"{step_id}: missing step properties: {', '.join(missing)}")
        extras = sorted(set(props) - STEP_PROPERTIES)
        if extras:
            errors.append(f"{step_id}: unsupported step properties: {', '.join(extras)}")
        duplicates = sorted(prop for prop in props if parsed.property_counts.get((step_id, prop), 0) != 1)
        if duplicates:
            errors.append(f"{step_id}: duplicate step properties: {', '.join(duplicates)}")
        step_gap_ids = (step["attrs"].get("data-gap-ids") or "").strip()
        for gap_id in step_gap_ids.split():
            if gap_id not in id_set:
                errors.append(f"{step_id}: data-gap-ids references missing {gap_id}")
        for prop, value in props.items():
            normalized = " ".join(value.lower().split())
            if not normalized:
                errors.append(f"{step_id}.{prop}: empty")
            if "unknown" in normalized and not step_gap_ids:
                errors.append(f"{step_id}.{prop}: unknown without data-gap-ids")
            if normalized in VAGUE:
                errors.append(f"{step_id}.{prop}: vague placeholder operation")
    if args.expectations:
        with args.expectations.resolve().open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {"step_id", "property", "must_contain", "evidence_id"}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                errors.append("expectations CSV missing columns: " + ", ".join(sorted(required)))
            else:
                for row_number, row in enumerate(reader, start=2):
                    step_id = row["step_id"].strip()
                    prop = row["property"].strip()
                    expected = " ".join(row["must_contain"].split()).lower()
                    evidence_id = row["evidence_id"].strip() or "<missing-evidence-id>"
                    actual = " ".join(parsed.steps.get(step_id, {}).get("properties", {}).get(prop, "").split()).lower()
                    if not step_id or not prop or not expected:
                        errors.append(f"expectations row {row_number}: blank step_id/property/must_contain")
                    elif expected not in actual:
                        errors.append(
                            f"{step_id}.{prop}: evidence atom {evidence_id} lost during rendering; "
                            f"expected fragment {row['must_contain']!r}"
                        )
    if errors:
        print("INVALID")
        for error in errors:
            print("- " + error)
        return 1
    print(f"VALID: {path} ({len(parsed.steps)} executable step contracts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
