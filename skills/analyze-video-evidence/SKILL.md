---
name: analyze-video-evidence
description: Analyze a selected timecoded video evidence package for one BU engagement and return traceable screen actions, fields, workflow steps, decision rationale, heuristics, exceptions, pain points and open questions. Use after extract-video-evidence as a worker invoked by distill-bu-knowledge; do not analyze unrelated full recordings or approve business knowledge.
---

# Analyze Video Evidence

Read [input-evidence-contract.md](references/input-evidence-contract.md), [analysis-framework.md](references/analysis-framework.md), [screen-action-contract.md](references/screen-action-contract.md), and [knowledge-contract.md](references/knowledge-contract.md).

1. Run `scripts/validate_evidence_package.py` on the selected package and record missing clips, frames, transcript, OCR or interaction events.
2. Inspect each coherent segment using transcript plus before/action/after visual states.
3. Extract structured operational steps, not only a screen sequence. For each step separately capture trigger, preconditions, actor, exact source system/location, ordered acquisition method, selection basis, input object/fields, ordered action, transformation, output object, output formation rule, destination system/location, content validation, completion condition, completion evidence, failure/fallback, exception and escalation. Never collapse these into a generic `input → output` sentence.
4. For each decision capture the decision question and owner, all inputs with provenance, freshness, rule/threshold/heuristic, rationale, missing/conflicting-input behavior, counterexamples and downstream effect. For each deliverable capture output schema, required fields, format/template, recipient, delivery channel/destination, timing, acceptance check and proof of delivery. Connect steps, systems and deliverables with directed `data_flows` that identify the payload fields, schema, transport, trigger, validation and failure behavior.
5. If a material detail is not evidenced, set it to `unknown` and create a linked targeted open question. Generic verbs such as "download", "upload", "process" and "deliver" are incomplete without source, destination, object and verification. Treat transcript-only descriptions as `stated`; they do not prove screen sequence, field mapping, file movement, validation or completion unless corroborated by frames, clips, interaction events or equivalent artifacts.
6. Classify claims as `observed`, `stated`, `corroborated`, `inferred` or `unresolved`.
7. A static frame proves visible state, not a click or causal result. Require a sequence, clip or interaction event for action claims.
8. Preserve loops, retries, alternatives, contradictions and missing information.
9. Before synthesis, create an evidence-atom pass over every selected segment. Preserve every exact field/question identifier, enumerated value, threshold, conditional phrase, source fallback, required screenshot or retained attachment. Give each selected segment a disposition of `consumed`, `duplicate`, `out_of_scope` or `unresolved`; a generic workflow step does not count as consuming its field-level atoms.
10. Keep explicit transcript facts as `stated` when visuals are absent. Do not replace a stated field, source, rule or deliverable component with `unknown`; record the stated value plus a linked observation gap when visual proof is required for readiness.
11. Write results under `20_distilled/derived/video/<evidence-id>/analysis/` with stable segment IDs and timecodes, then run `scripts/validate_knowledge_package.py`.
12. Return structured knowledge and targeted gaps to `$distill-bu-knowledge`. When visual evidence is insufficient for development-relevant I/O, request the smallest specific follow-up evidence rather than inventing the action.

After producing `analysis/knowledge.json`, always run `scripts/validate_knowledge_package.py`. Only a valid package may be merged into engagement knowledge.
