"""Local helpers for evidence-backed knowledge. No model calls or business decisions."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {
    "context": {"context"}, "domain": {"concept", "fact", "policy"},
    "inference": {"inference"}, "task": {"task"},
    "communication": {"handoff"}, "expert-perspectives": {"expert"},
    "cases": {"case", "lesson"},
}
FILES = ["manifest", *SECTIONS, "evidence-index", "gaps", "review"]
DETAILS = {
    "context": {"roles": list, "processes": list, "systems": list},
    "concept": {"definition": str}, "fact": {"value": str},
    "policy": {"condition": str, "rule": str, "exceptions": list},
    "inference": {"inputs": list, "cues": list, "reasoning": list,
                  "outcomes": list, "missing_input": str, "conflicting_input": str,
                  "counterexamples": list},
    "task": {"goal": str, "trigger": str, "inputs": list, "steps": list,
             "outputs": list, "stop_conditions": list, "completion": str},
    "handoff": {"sender": str, "receiver": str, "payload": list,
                "trigger": str, "channel": str, "check": str},
    "expert": {"role": str, "experience_scope": str, "mental_models": list,
               "heuristics": list, "novice_mistakes": list, "boundaries": list},
    "case": {"scenario": str, "inputs": list, "expected": str,
             "expected_source": str, "case_type": str},
    "lesson": {"expected": str, "actual": str, "reason": str, "next_time": str},
}


class ContractError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys rather than silently discarding source knowledge."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ContractError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read(path):
    with Path(path).open(encoding="utf-8-sig") as stream:
        return yaml.load(stream, Loader=UniqueLoader)


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def schema_check(name, data):
    schema = read(ROOT / "schemas" / f"{name}.yaml")
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: str(e.path))
    if errors:
        raise ContractError("\n".join(f"{name}:{'/'.join(map(str, e.path))}: {e.message}" for e in errors))


def load_bundle(path):
    path = Path(path)
    return {name: read(path / f"{name}.yaml") for name in FILES}


def objects(bundle):
    return [obj for section in SECTIONS for obj in bundle[section]]


def digest(bundle):
    # Exclude review itself so confirmation does not change its own subject.
    payload = {key: value for key, value in bundle.items() if key != "review"}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def unknown(value):
    if isinstance(value, dict):
        return any(unknown(v) for v in value.values())
    if isinstance(value, list):
        return any(unknown(v) for v in value)
    return isinstance(value, str) and value.strip().lower() == "unknown"


def validate(bundle, release=False):
    schema_check("knowledge-release", bundle)
    schema_check("evidence", bundle["evidence-index"])
    errors = []
    items = objects(bundle)
    by_id = {obj["id"]: obj for obj in items}
    evidence = {ev["id"]: ev for ev in bundle["evidence-index"]}
    all_ids = [obj["id"] for obj in items] + [ev["id"] for ev in bundle["evidence-index"]] + [g["id"] for g in bundle["gaps"]]
    if len(all_ids) != len(set(all_ids)):
        errors.append("IDs must be unique across the entire bundle")
    for section, kinds in SECTIONS.items():
        if not bundle[section]:
            if section in {"context", "domain", "task"}:
                errors.append(f"{section}: at least one object required")
            elif not bundle["manifest"]["empty_sections"].get(section, "").strip():
                errors.append(f"{section}: empty section requires an explicit reason")
        for obj in bundle[section]:
            if obj["kind"] not in kinds:
                errors.append(f"{obj['id']}: kind does not belong in {section}")
    for obj in items:
        oid = obj["id"]
        for key, value_type in DETAILS[obj["kind"]].items():
            value = obj["details"].get(key)
            if not isinstance(value, value_type) or (value_type is str and not value.strip()):
                errors.append(f"{oid}: details.{key} requires {value_type.__name__}")
            elif value_type is list and any(not isinstance(v, str) or not v.strip() for v in value):
                errors.append(f"{oid}: details.{key} must contain nonempty strings")
        required_lists = {"inference": ["inputs", "reasoning", "outcomes"],
                          "task": ["inputs", "steps", "outputs", "stop_conditions"],
                          "handoff": ["payload"]}.get(obj["kind"], [])
        for key in required_lists:
            if not obj["details"].get(key):
                errors.append(f"{oid}: details.{key} cannot be empty; use unknown plus a gap when missing")
        if obj["kind"] == "case" and obj["details"].get("case_type") not in {"actual", "hypothetical"}:
            errors.append(f"{oid}: case_type must be actual or hypothetical")
        for ref in obj["refs"]:
            if ref not in by_id:
                errors.append(f"{oid}: missing knowledge reference {ref}")
        for ref in obj["expert_refs"]:
            if ref not in by_id or by_id[ref]["kind"] != "expert":
                errors.append(f"{oid}: missing expert reference {ref}")
        for ref in obj["evidence_refs"]:
            if ref not in evidence:
                errors.append(f"{oid}: missing evidence reference {ref}")
        if obj["sharing"] == "attributed" and not obj["expert_refs"]:
            errors.append(f"{oid}: attributed knowledge needs expert_refs")
        if obj["sharing"] == "shared":
            groups = {evidence[r]["source_group"] for r in obj["evidence_refs"] if r in evidence}
            if len(groups) < 2:
                errors.append(f"{oid}: shared requires at least two independent source groups")
        needs_gap = unknown(obj["details"]) or obj["evidence_mode"] in {"inferred", "conflicting", "unresolved"} or obj["sharing"] == "contested"
        if needs_gap and not any(oid in g["affects"] and g["status"] == "open" for g in bundle["gaps"]):
            errors.append(f"{oid}: uncertainty requires a linked open gap")
    for gap in bundle["gaps"]:
        for ref in gap["affects"]:
            if ref not in by_id:
                errors.append(f"{gap['id']}: missing affected object {ref}")
        if gap["status"] == "resolved" and not gap["resolution"]:
            errors.append(f"{gap['id']}: resolved gap needs resolution")
    current_digest = digest(bundle)
    tested = set()
    for scenario in bundle["review"]["scenarios"]:
        case = by_id.get(scenario["case_ref"])
        if not case or case["kind"] != "case":
            errors.append(f"scenario: missing case {scenario['case_ref']}")
        for ref in scenario["knowledge_refs"]:
            if ref not in by_id:
                errors.append(f"scenario: missing knowledge {ref}")
            if case and ref not in case["refs"]:
                errors.append(f"scenario: {ref} is not covered by case.refs")
        if scenario["model_digest"] == current_digest and scenario["result"] == "pass":
            tested.update(scenario["knowledge_refs"])
        if release and scenario["model_digest"] == current_digest and scenario["result"] == "fail":
            errors.append(f"release: failed scenario {scenario['case_ref']} requires correction or explicit scope revision")
    confirmation = bundle["review"]["confirmation"]
    confirmed = bool(confirmation and confirmation["model_digest"] == current_digest)
    if release and not confirmed:
        errors.append("release: missing or stale participant confirmation")
    for obj in items:
        if obj["validation"] == "scenario-tested" and obj["id"] not in tested:
            errors.append(f"{obj['id']}: scenario-tested has no passing scenario for this model")
        if release and obj["critical"]:
            if obj["id"] not in tested:
                errors.append(f"{obj['id']}: critical knowledge requires scenario walkthrough")
            if obj["validation"] == "draft" or obj["evidence_mode"] not in {"observed", "stated"} or obj["sharing"] == "contested":
                errors.append(f"{obj['id']}: critical knowledge remains uncertain")
            if unknown(obj["details"]) or any(g["blocking"] and g["status"] == "open" and obj["id"] in g["affects"] for g in bundle["gaps"]):
                errors.append(f"{obj['id']}: critical knowledge has a blocking gap")
        if release and obj["sharing"] == "shared" and obj["validation"] == "draft":
            errors.append(f"{obj['id']}: shared knowledge needs participant confirmation")
    if errors:
        raise ContractError("\n".join(errors))
    return {"objects": len(items), "evidence": len(evidence), "model_digest": current_digest,
            "open_gaps": sum(g["status"] == "open" for g in bundle["gaps"]),
            "level": "release-contract" if release else "structure-only"}


def verify_lock(path):
    path = Path(path)
    lock = path / "release-lock.yaml"
    if lock.exists():
        hashes = read(lock)
        expected = {f"{name}.yaml" for name in FILES} | {"handbook.md", "coverage.md"}
        if not isinstance(hashes, dict) or set(hashes) != expected:
            raise ContractError("Release lock file list is incomplete")
        for name, value in hashes.items():
            file = path / name
            if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != value:
                raise ContractError(f"Published snapshot was changed: {name}")


def readiness(bundle, target):
    validate(bundle, release=True)
    schema_check("solution-target", target)
    if target["release_id"] != bundle["manifest"]["release_id"]:
        raise ContractError("Target release_id does not match")
    by_id = {obj["id"]: obj for obj in objects(bundle)}
    for expert in target["allowed_expert_refs"]:
        if expert not in by_id or by_id[expert]["kind"] != "expert":
            raise ContractError(f"Unknown allowed expert: {expert}")
    if set(target["required_task_refs"]) & set(target["optional_task_refs"]):
        raise ContractError("Required and optional tasks overlap")
    results = {}
    for task_id in target["required_task_refs"] + target["optional_task_refs"]:
        reasons, closure, todo = [], set(), [task_id]
        if task_id not in by_id or by_id[task_id]["kind"] != "task":
            raise ContractError(f"Target references unknown task: {task_id}")
        while todo:
            oid = todo.pop()
            if oid in closure:
                continue
            closure.add(oid)
            obj = by_id[oid]
            todo.extend(obj["refs"])
            if obj["validation"] == "draft" or obj["evidence_mode"] not in {"observed", "stated"}:
                reasons.append(f"{oid}: unconfirmed or uncertain")
            if unknown(obj["details"]) or obj["sharing"] == "contested":
                reasons.append(f"{oid}: unresolved detail or conflict")
            if obj["sharing"] == "attributed" and not set(obj["expert_refs"]).issubset(target["allowed_expert_refs"]):
                reasons.append(f"{oid}: expert attribution not selected in target")
            for gap in bundle["gaps"]:
                if gap["status"] == "open" and gap["blocking"] and oid in gap["affects"]:
                    reasons.append(f"{oid}: blocking gap {gap['id']}")
        results[task_id] = {"ready": not reasons, "knowledge_refs": sorted(closure), "reasons": reasons}
    required_ready = all(results[t]["ready"] for t in target["required_task_refs"])
    optional_ready = all(results[t]["ready"] for t in target["optional_task_refs"])
    status = "knowledge-gap" if not required_ready else "ready" if optional_ready else "limited-scope"
    return {"status": status, "tasks": results,
            "accepted_task_refs": [t for t, r in results.items() if r["ready"]],
            "runtime_readiness": "not-assessed"}


def render(path):
    path = Path(path)
    if (path / "release-lock.yaml").exists():
        raise ContractError("Render a draft; published snapshots cannot be overwritten")
    bundle = load_bundle(path)
    report = validate(bundle)
    manifest = bundle["manifest"]
    lines = [f"# {manifest['release_id']} 知識手冊", "", f"範圍：{manifest['scope']}", "",
             f"排除：{'；'.join(manifest['exclusions']) or '無另外列出'}", "",
             f"模型指紋：`{report['model_digest']}`", "", "此文件由 YAML 產生；修正請回到模型，重新產生手冊。", ""]
    for section in SECTIONS:
        lines += [f"## {section}", ""]
        if not bundle[section]:
            lines += [bundle["manifest"]["empty_sections"].get(section, "無項目"), ""]
        for obj in bundle[section]:
            lines += [f"### {obj['id']} {obj['title']}", "", obj["statement"], "",
                      f"適用：{obj['scope']}", "",
                      f"證據：{obj['evidence_mode']}；確認：{obj['validation']}；歸屬：{obj['sharing']}", "",
                      f"專家：{', '.join(obj['expert_refs']) or '無'}；依賴：{', '.join(obj['refs']) or '無'}", ""]
            for key, value in obj["details"].items():
                lines += [f"**{key}**", ""]
                lines += ([f"- {item}" for item in value] or ["無／不適用"]) if isinstance(value, list) else [str(value)]
                lines.append("")
            lines += [f"來源：{', '.join(obj['evidence_refs'])}", ""]
    lines += ["## Evidence index", ""]
    for ev in bundle["evidence-index"]:
        lines += [f"### {ev['id']}", "", f"來源：{ev['source']}；定位：{ev['locator']}；版本：{ev['source_version']}", "",
                  f"可取得性：{ev['availability']}；speaker：{ev['speaker'] or '不適用'}", "", ev["excerpt"], ""]
    lines += ["## 已知缺口", ""]
    for gap in bundle["gaps"]:
        lines += [f"- {gap['id']} ({gap['status']}) {gap['question']}；影響 {', '.join(gap['affects'])}；blocking={gap['blocking']}"]
    lines += ["", "## 確認與案例紀錄", "", "```yaml", yaml.safe_dump(bundle["review"], allow_unicode=True, sort_keys=False).strip(), "```", ""]
    (path / "handbook.md").write_text("\n".join(lines), encoding="utf-8")
    coverage = ["# 知識涵蓋說明", "", f"範圍：{manifest['scope']}", "",
                f"物件 {report['objects']}；證據 {report['evidence']}；未解缺口 {report['open_gaps']}。", "",
                "數量是盤點，不能代表整個部門的涵蓋率。Skill 可用性另依 target 執行 coverage。", "",
                "| ID | 類型 | 證據 | 確認 | 歸屬 | 核心 |", "| --- | --- | --- | --- | --- | --- |"]
    coverage += [f"| {o['id']} | {o['kind']} | {o['evidence_mode']} | {o['validation']} | {o['sharing']} | {o['critical']} |" for o in objects(bundle)]
    coverage += ["", "## 未解缺口", ""] + [f"- {g['id']}: {g['question']} ({', '.join(g['affects'])})" for g in bundle["gaps"] if g["status"] == "open"]
    (path / "coverage.md").write_text("\n".join(coverage) + "\n", encoding="utf-8")
    return report


def publish(draft, library):
    draft, library = Path(draft).resolve(), Path(library).resolve()
    bundle = load_bundle(draft)
    validate(bundle, release=True)
    manifest = bundle["manifest"]
    if library.name != manifest["domain"] or library.parent.name != manifest["department"]:
        raise ContractError("Library must end with <department>/<domain> matching manifest")
    destination = library / "releases" / manifest["release_id"]
    if destination.exists():
        raise ContractError(f"Release already exists: {destination}")
    index_path = library / "index.yaml"
    index = read(index_path) if index_path.exists() else {"department": manifest["department"], "domain": manifest["domain"], "releases": []}
    if any(r["release_id"] == manifest["release_id"] for r in index["releases"]):
        raise ContractError("Release ID already exists in index")
    if manifest["base_release"] and not any(r["release_id"] == manifest["base_release"] for r in index["releases"]):
        raise ContractError("base_release not found in this library")
    render(draft)
    destination.mkdir(parents=True, exist_ok=False)
    names = [f"{name}.yaml" for name in FILES] + ["handbook.md", "coverage.md"]
    for name in names:
        shutil.copyfile(draft / name, destination / name)
    write(destination / "release-lock.yaml", {n: hashlib.sha256((destination / n).read_bytes()).hexdigest() for n in names})
    index["releases"].append({"release_id": manifest["release_id"], "path": f"releases/{manifest['release_id']}", "model_digest": digest(bundle)})
    write(index_path, index)
    return {"release_path": str(destination), "model_digest": digest(bundle)}


def verify_solution(release_path, solution):
    verify_lock(release_path)
    bundle = load_bundle(release_path)
    solution = Path(solution).resolve()
    target = read(solution / "target.yaml")
    coverage = readiness(bundle, target)
    if coverage["status"] == "knowledge-gap":
        raise ContractError("Required scope contains knowledge gaps")
    trace = read(solution / "traceability.yaml")
    if trace.get("release_id") != bundle["manifest"]["release_id"] or trace.get("model_digest") != digest(bundle):
        raise ContractError("Solution references a different release or model digest")
    if trace.get("coverage_status") != coverage["status"] or set(trace.get("accepted_task_refs", [])) != set(coverage["accepted_task_refs"]):
        raise ContractError("Solution scope does not match coverage")
    needed = set().union(*(set(coverage["tasks"][t]["knowledge_refs"]) for t in coverage["accepted_task_refs"]))
    mapped = set()
    for behavior in trace.get("behaviors", []):
        if not behavior.get("id") or not behavior.get("knowledge_refs"):
            raise ContractError("Each behavior needs id and knowledge_refs")
        artifact = (solution / behavior["artifact"]).resolve()
        if not artifact.is_relative_to(solution) or not artifact.is_file():
            raise ContractError(f"Artifact missing or outside solution: {artifact}")
        if not set(behavior["knowledge_refs"]).issubset(needed):
            raise ContractError("Behavior uses knowledge outside accepted scope")
        mapped.update(behavior["knowledge_refs"])
    if not needed.issubset(mapped):
        raise ContractError(f"Unmapped knowledge: {sorted(needed - mapped)}")
    tests = trace.get("tests", [])
    for test in tests:
        for field in ["id", "kind", "method", "expected", "actual", "result", "evidence"]:
            if not isinstance(test.get(field), str) or not test[field].strip():
                raise ContractError(f"Test missing {field}")
        if test["result"] != "pass":
            raise ContractError("Solution has unpassed tests")
        if target["mode"] == "execution" and test["method"] != "execution":
            raise ContractError("Execution solution requires actual execution tests")
    if not {"happy", "stop"}.issubset({t["kind"] for t in tests}):
        raise ContractError("Solution needs happy and stop tests")
    if not (solution / "validation.md").is_file():
        raise ContractError("Missing human-readable validation.md")
    return {"status": "traceability-contract-pass", "coverage": coverage,
            "limitation": "Does not prove behavior or truth of test records; inspect artifacts and recorded evidence."}


def initialize(runs_root, department, domain, entry_mode):
    if not all(re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug) for slug in [department, domain]):
        raise ContractError("Department and domain must be lowercase slugs")
    run_id = "RUN-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    path = Path(runs_root).resolve() / run_id
    path.mkdir(parents=True, exist_ok=False)
    for directory in ["input", "evidence", "draft", "review"]:
        (path / directory).mkdir()
    write(path / "state.yaml", {"schema_version": 1, "run_id": run_id, "stage": "frame", "status": "active",
                               "next_action": "confirm_scope_and_priority_task", "pending": [], "solution_requested": False,
                               "base_release": None, "release_path": None, "completion": None})
    write(path / "engagement.yaml", {"schema_version": 1, "run_id": run_id, "department": department, "domain": domain,
                                    "entry_mode": entry_mode, "objective": "", "users": [], "included": [], "excluded": [],
                                    "participants": [], "resources": [], "priority_reason": "", "scope_confirmation": ""})
    draft = path / "draft"
    write(draft / "manifest.yaml", {"schema_version": 1, "release_id": f"{domain}-v1", "department": department,
                                   "domain": domain, "scope": "", "exclusions": [], "base_release": None, "empty_sections": {}})
    for section in [*SECTIONS, "evidence-index", "gaps"]:
        write(draft / f"{section}.yaml", [])
    write(draft / "review.yaml", {"confirmation": None, "scenarios": []})
    return {"run_path": str(path), "note": "Empty draft is intentionally not releasable."}


def check_repo():
    from urllib.parse import unquote
    errors, count = [], 0
    for path in (ROOT / ".agents" / "skills").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8-sig")
        meta = yaml.safe_load(text.split("---", 2)[1])
        if meta.get("name") != path.parent.name or not meta.get("description"):
            errors.append(f"Bad skill frontmatter: {path}")
        count += 1
    for folder in [ROOT / ".agents", ROOT / "docs"]:
        for path in folder.rglob("*.md"):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8-sig")):
                if "://" in target or target.startswith("#"):
                    continue
                target = unquote(target.split("#")[0])
                if not (path.parent / target).exists():
                    errors.append(f"Broken link {path.relative_to(ROOT)} → {target}")
    for schema in (ROOT / "schemas").glob("*.yaml"):
        Draft202012Validator.check_schema(read(schema))
    if count != 10:
        errors.append(f"Expected 6 core + 4 media skills; found {count}")
    if errors:
        raise ContractError("\n".join(errors))
    return {"status": "pass", "skills": count}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--runs-root", type=Path, default=ROOT / "runs")
    init.add_argument("--department", required=True)
    init.add_argument("--domain", required=True)
    init.add_argument("--entry-mode", choices=["department-first", "expert-first"], default="department-first")
    for cmd in ["validate", "digest", "render", "publish"]:
        p = sub.add_parser(cmd)
        p.add_argument("path", type=Path)
        if cmd == "validate":
            p.add_argument("--release", action="store_true")
        if cmd == "publish":
            p.add_argument("--library", type=Path, required=True)
    for cmd in ["coverage", "verify-solution"]:
        p = sub.add_parser(cmd)
        p.add_argument("path", type=Path)
        p.add_argument("target", type=Path)
    sub.add_parser("check-repo")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.runs_root, args.department, args.domain, args.entry_mode)
        elif args.command == "check-repo":
            result = check_repo()
        elif args.command == "publish":
            result = publish(args.path, args.library)
        elif args.command == "render":
            result = render(args.path)
        elif args.command == "verify-solution":
            result = verify_solution(args.path, args.target)
        else:
            verify_lock(args.path)
            bundle = load_bundle(args.path)
            if args.command == "validate":
                result = validate(bundle, args.release)
            elif args.command == "digest":
                result = {"model_digest": digest(bundle)}
            else:
                result = readiness(bundle, read(args.target))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if isinstance(result, dict) and result.get("status") == "knowledge-gap" else 0
    except (ContractError, OSError, yaml.YAMLError, TypeError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
