"""Build explicitly synthetic fixtures; no LLM or real participant validation."""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import knowledge_workflow as kw


def make_bundle():
    def obj(oid, kind, title, details, refs=(), critical=False):
        return {"id": oid, "kind": kind, "title": title, "statement": title,
                "scope": "SYNTHETIC toy card; advisory only", "evidence_refs": ["EVD-001"],
                "evidence_mode": "stated", "validation": "participant-confirmed",
                "sharing": "attributed", "expert_refs": ["EXP-001"], "refs": list(refs),
                "critical": critical, "details": details}
    bundle = {
        "manifest": {"schema_version": 1, "release_id": "toy-v1", "department": "synthetic", "domain": "toy",
                     "scope": "SYNTHETIC 卡片文字判讀", "exclusions": ["實際系統操作", "真實業務"],
                     "base_release": None, "empty_sections": {"communication": "只回覆当前提問者，無跨角色交接"}},
        "context": [obj("CTX-001", "context", "虛構示範工作", {"roles": ["Demo expert", "requestor"], "processes": ["判讀卡片"], "systems": []})],
        "domain": [obj("DOM-001", "concept", "標籤是卡片提供的文字值", {"definition": "label 是輸入文字，不自行推測缺失值"})],
        "inference": [obj("INF-001", "inference", "label=blue 時 accept，其他情況 stop", {
            "inputs": ["label"], "cues": ["是否提供 label", "是否精確等於 blue"],
            "reasoning": ["先辨認是否缺少標籤", "精確比對 blue；不做近似推測"],
            "outcomes": ["blue → accept", "missing/other → stop 並請人檢查"],
            "missing_input": "stop 並請人檢查", "conflicting_input": "stop 並請人檢查",
            "counterexamples": ["其他顏色不可類推為 blue"]}, ["DOM-001"], True)],
        "task": [obj("TASK-001", "task", "依卡片標籤提供建議", {
            "goal": "提供 accept 或 stop 建議", "trigger": "使用者提供卡片標籤",
            "inputs": ["label（可能缺失）"], "steps": ["依 INF-001 判讀", "回覆結果及缺失原因"],
            "outputs": ["accept 或 stop"], "stop_conditions": ["缺少或非 blue label"],
            "completion": "使用者收到具理由的建議；不操作系統"}, ["INF-001"])],
        "communication": [],
        "expert-perspectives": [obj("EXP-001", "expert", "虛構 Demo 專家的保守比對方法", {
            "role": "SYNTHETIC expert", "experience_scope": "這個玩具示範",
            "mental_models": ["明示值才能接受"], "heuristics": ["缺資料不猜"],
            "novice_mistakes": ["把近似值當相同"], "boundaries": ["不能推廣成真實部門政策"]}, ["INF-001"])],
        "cases": [obj("CASE-001", "case", "blue 正例", {"scenario": "label=blue", "inputs": ["blue"],
            "expected": "accept", "expected_source": "examples/synthetic/source.md#S2", "case_type": "hypothetical"}, ["INF-001", "TASK-001"]),
                  obj("CASE-002", "case", "缺值停止例", {"scenario": "label missing", "inputs": ["missing"],
            "expected": "stop 並請人檢查", "expected_source": "examples/synthetic/source.md#S2", "case_type": "hypothetical"}, ["INF-001", "TASK-001"])],
        "evidence-index": [{"id": "EVD-001", "source": "examples/synthetic/source.md", "locator": "S1-S3",
            "source_group": "synthetic-expert", "source_version": "fixture-v1", "excerpt": "blue → accept；缺失或其他 → stop。全部為虛構規格。",
            "speaker": "SYNTHETIC Demo", "availability": "available"}],
        "gaps": [], "review": {"confirmation": None, "scenarios": []},
    }
    sign_fixture(bundle)
    return bundle


def sign_fixture(bundle):
    """Only for fake test records; never use to confirm real knowledge."""
    stamp = kw.digest(bundle)
    bundle["review"] = {"confirmation": {"participant": "SYNTHETIC participant; not a real approval",
        "confirmed_at": "2026-09-30T00:00:00Z", "source": "examples/synthetic/source.md#S3", "model_digest": stamp},
        "scenarios": [{"case_ref": cid, "knowledge_refs": ["INF-001", "TASK-001"], "method": "walkthrough",
            "participant": "SYNTHETIC fixture", "actual": result, "result": "pass",
            "source": "examples/synthetic/source.md#S3 (fabricated fixture, not an executed skill)", "model_digest": stamp}
            for cid, result in [("CASE-001", "accept"), ("CASE-002", "stop 並請人檢查")]]}


def make_target():
    return {"solution_id": "toy-advisor", "release_id": "toy-v1", "product": "skill", "mode": "advisory",
            "user": "SYNTHETIC requestor", "outcome": "示範有依據的卡片建議", "required_task_refs": ["TASK-001"],
            "optional_task_refs": [], "allowed_expert_refs": ["EXP-001"], "inputs": ["label"], "outputs": ["建議"],
            "tools": [], "human_controls": ["stop 時請使用者檢查"], "exclusions": ["真實系統操作"]}


def write_bundle(path, bundle):
    for key, data in bundle.items():
        kw.write(Path(path) / f"{key}.yaml", data)


def make_solution(path, bundle):
    path = Path(path)
    artifact = path / "artifact" / "toy-advisor" / "SKILL.md"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("""---
name: toy-advisor
description: 依虛構示範來源提供卡片標籤建議，僅供測試知識到 Skill 的追溯流程。
---

# SYNTHETIC ONLY

採用虛構 EXP-001 的方法（TASK-001、INF-001、DOM-001）：檢查 label，只有精確等於 blue 回覆 accept；缺少或其他值回覆 stop 並請使用者檢查。不猜測近似值，不操作任何系統。適用於這個玩具示範。
""", encoding="utf-8")
    kw.write(path / "target.yaml", make_target())
    kw.write(path / "traceability.yaml", {"release_id": "toy-v1", "model_digest": kw.digest(bundle),
        "coverage_status": "ready", "accepted_task_refs": ["TASK-001"],
        "behaviors": [{"id": "BEH-001", "artifact": "artifact/toy-advisor/SKILL.md", "knowledge_refs": ["TASK-001", "INF-001", "DOM-001"]}],
        "tests": [{"id": "TEST-" + kind, "kind": kind, "method": "synthetic-fixture", "expected": expected,
                   "actual": expected, "result": "pass", "evidence": "SYNTHETIC contract fixture; no agent was executed"}
                  for kind, expected in [("happy", "accept"), ("stop", "stop 並請人檢查")]]})
    (path / "validation.md").write_text("# SYNTHETIC contract fixture\n\n僅驗证資料契約與映射。測試紀錄為預設假資料；未執行 Agent 或真實業務，不能宣稱 Skill 行為驗證通過。\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("Output must be a new directory; demo will not overwrite existing files")
    bundle = make_bundle()
    draft = args.out / "draft"
    write_bundle(draft, bundle)
    release = kw.publish(draft, args.out / "knowledge" / "synthetic" / "toy")
    make_solution(args.out / "solution", bundle)
    report = kw.verify_solution(release["release_path"], args.out / "solution")
    print("SYNTHETIC ONLY: fixture contract pass; not business or agent behavior validation.")
    print(release["release_path"])
    print(report["status"])


if __name__ == "__main__":
    main()
