import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "examples" / "synthetic"))
import knowledge_workflow as kw
from build_demo import make_bundle, make_target, make_solution, sign_fixture, write_bundle


class KnowledgeWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.bundle = make_bundle()
        self.target = make_target()

    def test_complete_release_and_dependency_closure(self):
        report = kw.validate(self.bundle, release=True)
        self.assertEqual(report["level"], "release-contract")
        coverage = kw.readiness(self.bundle, self.target)
        self.assertEqual(coverage["status"], "ready")
        self.assertEqual(set(coverage["tasks"]["TASK-001"]["knowledge_refs"]), {"TASK-001", "INF-001", "DOM-001"})

    def test_missing_evidence_and_duplicate_ids_rejected(self):
        self.bundle["inference"][0]["evidence_refs"] = ["EVD-missing"]
        with self.assertRaisesRegex(kw.ContractError, "missing evidence"):
            kw.validate(self.bundle)
        self.bundle = make_bundle()
        self.bundle["domain"].append(copy.deepcopy(self.bundle["domain"][0]))
        with self.assertRaisesRegex(kw.ContractError, "unique"):
            kw.validate(self.bundle)

    def test_unknown_requires_linked_gap(self):
        self.bundle["task"][0]["details"]["completion"] = "unknown"
        with self.assertRaisesRegex(kw.ContractError, "linked open gap"):
            kw.validate(self.bundle)

    def test_stale_confirmation_rejected(self):
        self.bundle["inference"][0]["details"]["outcomes"][0] = "blue → stop"
        with self.assertRaisesRegex(kw.ContractError, "stale participant confirmation"):
            kw.validate(self.bundle, release=True)

    def test_critical_without_scenario_rejected(self):
        self.bundle["review"]["scenarios"] = []
        with self.assertRaisesRegex(kw.ContractError, "requires scenario"):
            kw.validate(self.bundle, release=True)

    def test_noncritical_uncertainty_blocks_transitive_product(self):
        self.bundle["domain"][0]["evidence_mode"] = "inferred"
        self.bundle["gaps"] = [{"id": "GAP-001", "question": "Confirm concept", "affects": ["DOM-001"],
                                "blocking": True, "status": "open", "resolution": None}]
        sign_fixture(self.bundle)
        kw.validate(self.bundle, release=True)
        self.assertEqual(kw.readiness(self.bundle, self.target)["status"], "knowledge-gap")

    def test_failed_scenario_cannot_be_hidden_by_another_pass(self):
        self.bundle["review"]["scenarios"][1]["result"] = "fail"
        with self.assertRaisesRegex(kw.ContractError, "failed scenario"):
            kw.validate(self.bundle, release=True)

    def test_attribution_requires_selected_expert(self):
        self.target["allowed_expert_refs"] = []
        report = kw.readiness(self.bundle, self.target)
        self.assertEqual(report["status"], "knowledge-gap")
        self.assertIn("attribution", str(report))

    def test_shared_cannot_count_copies_as_independent_sources(self):
        obj = self.bundle["domain"][0]
        obj["sharing"] = "shared"
        ev = copy.deepcopy(self.bundle["evidence-index"][0])
        ev["id"] = "EVD-002"
        self.bundle["evidence-index"].append(ev)
        obj["evidence_refs"].append("EVD-002")
        with self.assertRaisesRegex(kw.ContractError, "independent"):
            kw.validate(self.bundle)

    def test_optional_gap_is_limited_scope(self):
        optional = copy.deepcopy(self.bundle["task"][0])
        optional.update(id="TASK-002", validation="draft")
        self.bundle["task"].append(optional)
        sign_fixture(self.bundle)
        self.target["optional_task_refs"] = ["TASK-002"]
        report = kw.readiness(self.bundle, self.target)
        self.assertEqual(report["status"], "limited-scope")
        self.assertEqual(report["accepted_task_refs"], ["TASK-001"])

    def test_dangling_reference_and_incorrect_case_target_rejected(self):
        self.bundle["task"][0]["refs"].append("DOM-unknown")
        with self.assertRaisesRegex(kw.ContractError, "missing knowledge"):
            kw.validate(self.bundle)
        self.bundle = make_bundle()
        self.bundle["review"]["scenarios"][0]["knowledge_refs"].append("EXP-001")
        with self.assertRaisesRegex(kw.ContractError, "not covered by case"):
            kw.validate(self.bundle)

    def test_publish_render_and_immutable_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            draft = root / "draft"
            write_bundle(draft, self.bundle)
            library = root / "synthetic" / "toy"
            result = kw.publish(draft, library)
            release = Path(result["release_path"])
            kw.verify_lock(release)
            self.assertIn("counterexamples", (release / "handbook.md").read_text(encoding="utf-8"))
            with self.assertRaisesRegex(kw.ContractError, "already exists"):
                kw.publish(draft, library)
            with self.assertRaisesRegex(kw.ContractError, "cannot be overwritten"):
                kw.render(release)
            (release / "handbook.md").write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(kw.ContractError, "was changed"):
                kw.verify_lock(release)

    def test_solution_traceability_and_missing_artifact(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_bundle(root / "draft", self.bundle)
            release = kw.publish(root / "draft", root / "synthetic" / "toy")["release_path"]
            make_solution(root / "solution", self.bundle)
            result = kw.verify_solution(release, root / "solution")
            self.assertEqual(result["status"], "traceability-contract-pass")
            (root / "solution" / "artifact" / "toy-advisor" / "SKILL.md").unlink()
            with self.assertRaisesRegex(kw.ContractError, "Artifact missing"):
                kw.verify_solution(release, root / "solution")

    def test_execution_cannot_pass_with_synthetic_records(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_bundle(root / "draft", self.bundle)
            make_solution(root / "solution", self.bundle)
            target = make_target()
            target["mode"] = "execution"
            kw.write(root / "solution" / "target.yaml", target)
            with self.assertRaisesRegex(kw.ContractError, "actual execution"):
                kw.verify_solution(root / "draft", root / "solution")

    def test_init_leaves_unconfirmed_draft(self):
        with tempfile.TemporaryDirectory() as temp:
            result = kw.initialize(temp, "demo", "area", "expert-first", ["form", "process-map"])
            path = Path(result["run_path"])
            self.assertEqual(kw.read(path / "state.yaml")["stage"], "frame")
            self.assertEqual(kw.read(path / "engagement.yaml")["source_types"], ["form", "process-map"])
            self.assertIsNone(kw.read(path / "draft" / "review.yaml")["confirmation"])
            with self.assertRaises(kw.ContractError):
                kw.validate(kw.load_bundle(path / "draft"), release=True)
            with self.assertRaises(kw.ContractError):
                kw.initialize(temp, "../escape", "area", "expert-first")
            with self.assertRaises(kw.ContractError):
                kw.initialize(temp, "demo", "area", "expert-first", ["form", "form"])

    def test_init_without_materials_has_empty_source_types(self):
        with tempfile.TemporaryDirectory() as temp:
            result = kw.initialize(temp, "demo", "area", "department-first")
            self.assertEqual(kw.read(Path(result["run_path"]) / "engagement.yaml")["source_types"], [])

    def test_duplicate_yaml_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.yaml"
            path.write_text("rule: first\nrule: second\n", encoding="utf-8")
            with self.assertRaisesRegex(kw.ContractError, "Duplicate YAML"):
                kw.read(path)

    def test_schemas_and_skill_links(self):
        self.assertEqual(kw.check_repo()["skills"], 10)


if __name__ == "__main__":
    unittest.main()
