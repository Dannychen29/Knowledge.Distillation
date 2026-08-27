from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

CATEGORIES = (
    "processes", "operational_steps", "decisions", "exceptions", "pain_points",
    "systems", "data_objects", "data_flows", "deliverables",
)
MODES = {"observed", "stated", "corroborated", "inferred", "unresolved"}
CONFIDENCE = {"high", "medium", "low"}
BOUNDARIES = {"deterministic", "ai_assisted", "human_review", "human_only"}


def contains_unknown(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().casefold() == "unknown"
    if isinstance(value, dict):
        return any(contains_unknown(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_unknown(item) for item in value)
    return False


def validate_object_fields(
    errors: list[str], label: str, value: Any, required_fields: tuple[str, ...]
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label}: expected an object")
        return
    for field in required_fields:
        if field not in value or value[field] is None or value[field] == "":
            errors.append(f"{label}: missing executable detail {field}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an evidence-linked BU knowledge package.")
    parser.add_argument("knowledge", type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    knowledge = json.loads(args.knowledge.read_text(encoding="utf-8-sig"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    segment_bounds = {
        item.get("segment_id"): (item.get("start_ms"), item.get("end_ms"))
        for item in manifest.get("segments", [])
        if item.get("segment_id")
    }
    valid_segments = set(segment_bounds)

    if knowledge.get("schema_version") != "1.1":
        errors.append("unsupported schema_version")
    required = {
        "source_manifest", "analysis_limits", "processes", "operational_steps", "decisions",
        "exceptions", "pain_points", "systems", "data_objects", "data_flows", "deliverables",
        "open_questions", "evidence_index",
    }
    for field in sorted(required):
        if field not in knowledge:
            errors.append(f"missing top-level field: {field}")

    ids: set[str] = set()
    for category in CATEGORIES:
        items = knowledge.get(category, [])
        if not isinstance(items, list):
            errors.append(f"{category} must be an array")
            continue
        for index, item in enumerate(items):
            label = item.get("id") or f"{category}[{index}]"
            if not item.get("id") or not item.get("statement"):
                errors.append(f"{label}: missing id or statement")
            elif item["id"] in ids:
                errors.append(f"duplicate claim id: {item['id']}")
            else:
                ids.add(item["id"])
            if item.get("evidence_mode") not in MODES:
                errors.append(f"{label}: invalid evidence_mode")
            if item.get("confidence") not in CONFIDENCE:
                errors.append(f"{label}: invalid confidence")
            if item.get("automation_boundary") not in BOUNDARIES:
                errors.append(f"{label}: invalid automation_boundary")
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{label}: substantive claim has no evidence")
                continue
            for ref in evidence:
                segment_id = ref.get("segment_id")
                if segment_id not in valid_segments:
                    errors.append(f"{label}: unknown segment_id {segment_id}")
                start = ref.get("start_ms")
                end = ref.get("end_ms")
                if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
                    errors.append(f"{label}: invalid evidence time bounds")
                elif segment_id in segment_bounds:
                    segment_start, segment_end = segment_bounds[segment_id]
                    if start < segment_start or end > segment_end:
                        errors.append(f"{label}: evidence time bounds exceed {segment_id}")

    open_questions = knowledge.get("open_questions", [])
    if not isinstance(open_questions, list):
        errors.append("open_questions must be an array")
    else:
        for index, item in enumerate(open_questions):
            for field in ("id", "question", "reason", "owner", "blocking_impact", "smallest_evidence_needed"):
                if not item.get(field):
                    errors.append(f"open_questions[{index}]: missing {field}")

    question_ids = {
        item.get("id") for item in open_questions if isinstance(item, dict) and item.get("id")
    } if isinstance(open_questions, list) else set()

    detailed_requirements = {
        "operational_steps": (
            "sequence", "actor", "trigger", "preconditions", "source", "action",
            "destination", "required_fields", "validation", "completion_evidence",
            "decision_ids", "deliverable_ids", "exception_ids", "gap_question_ids",
        ),
        "decisions": (
            "question", "owner", "inputs", "rule_or_heuristic", "rationale",
            "missing_input_behavior", "conflicting_input_behavior", "counterexamples",
            "downstream_effect", "exception_ids", "escalation", "gap_question_ids",
        ),
        "deliverables": (
            "name", "content_schema", "required_fields", "completeness_rule", "format",
            "template_version", "recipient", "delivery_channel", "destination",
            "timing_or_sla", "approval_owner", "acceptance_check", "naming_rule",
            "retention_rule", "proof_of_delivery", "gap_question_ids",
        ),
        "data_flows": (
            "from_node_id", "from_system", "from_location", "to_node_id", "to_system",
            "to_location", "data_object_id", "fields", "format_or_schema", "transport",
            "trigger", "frequency", "transformation", "validation", "access_constraints",
            "failure_or_retry", "development_ready", "gap_question_ids",
        ),
    }
    for category, fields in detailed_requirements.items():
        for index, item in enumerate(knowledge.get(category, [])):
            label = item.get("id") or f"{category}[{index}]"
            for field in fields:
                if field not in item or item[field] is None or item[field] == "":
                    errors.append(f"{label}: missing executable detail {field}")

            gap_ids = item.get("gap_question_ids", [])
            if not isinstance(gap_ids, list):
                errors.append(f"{label}: gap_question_ids must be an array")
                gap_ids = []
            for gap_id in gap_ids:
                if gap_id not in question_ids:
                    errors.append(f"{label}: unknown gap question {gap_id}")
            if contains_unknown(item) and not gap_ids:
                errors.append(f"{label}: unknown detail has no linked open question")
            if category == "data_flows" and contains_unknown(item) and item.get("development_ready") is not False:
                errors.append(f"{label}: flow with unknown I/O cannot be development_ready")
            if category == "data_flows" and not isinstance(item.get("development_ready"), bool):
                errors.append(f"{label}: development_ready must be boolean")
            if category == "data_flows" and item.get("development_ready") is True and item.get("evidence_mode") not in {"observed", "corroborated"}:
                errors.append(f"{label}: development_ready flow requires observed or corroborated evidence")
            if category == "operational_steps" and item.get("evidence_mode") in {"stated", "inferred", "unresolved"} and not gap_ids:
                errors.append(f"{label}: screen operation not proven by evidence mode {item.get('evidence_mode')}; link a targeted open question")

    for index, step in enumerate(knowledge.get("operational_steps", [])):
        label = step.get("id") or f"operational_steps[{index}]"
        validate_object_fields(errors, label, step.get("source"), (
            "system", "location", "acquisition_method", "object", "version_or_freshness", "fields",
        ))
        validate_object_fields(errors, label, step.get("action"), (
            "system", "screen", "control", "operation", "transformations",
        ))
        validate_object_fields(errors, label, step.get("destination"), (
            "system", "location", "object", "fields",
        ))

    for index, decision in enumerate(knowledge.get("decisions", [])):
        label = decision.get("id") or f"decisions[{index}]"
        inputs = decision.get("inputs")
        if not isinstance(inputs, list) or not inputs:
            errors.append(f"{label}: decision inputs must be a non-empty array")
            continue
        for input_index, decision_input in enumerate(inputs):
            validate_object_fields(errors, f"{label}.inputs[{input_index}]", decision_input, (
                "name", "source_system", "source_location", "acquisition_method",
                "field", "freshness", "required",
            ))

    result = {
        "valid": not errors,
        "claim_count": sum(len(knowledge.get(category, [])) for category in CATEGORIES if isinstance(knowledge.get(category), list)),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
