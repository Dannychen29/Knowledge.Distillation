# Solution-ready distillation contract

Use stable IDs so downstream Codex can join every section without interpreting prose.

## Canonical BRD structure

`BRD.html` must contain the semantic HTML sections and stable IDs defined in `html-brd-contract.md` for:

1. `metadata`: engagement ID, version, status, scope, source coverage and updated time.
2. `outcome`: objective, trigger, start/end boundary, exclusions and success measures.
3. `actors_and_systems`: actor/system IDs, responsibilities, locations and access constraints.
4. `operational_steps`: ordered step contracts.
5. `decisions`: decision contracts and outgoing branches.
6. `data_objects`: business objects, fields and schemas.
7. `data_flows`: directed movement between steps, systems and locations.
8. `deliverables`: output contract, destination, approval and completion proof.
9. `exceptions_and_controls`: error, retry, escalation, risk and human control.
10. `requirements`: functional, non-functional, security, audit and operational constraints supported by evidence.
11. `acceptance_scenarios`: precondition, input, action, expected result and evidence.
12. `gaps_and_readiness`: blockers and readiness by step, flow and requirement.
13. `traceability`: claim IDs and evidence locations.

## Step contract

For each material step implement every property in `executable-step-contract.md`. Keep acquisition, selection basis, output formation, content validation, completion condition and completion evidence distinct. A compact input/output row may summarize a complete step card but may not replace it.

## Decision contract

For each material decision capture:

`decision_id`, question, owner, input claim IDs, freshness, rule/threshold/heuristic, rationale, branches and target step IDs, missing/conflicting-input behavior, counterexample, exception, escalation, evidence claim IDs, and `development_ready`.

Keep policy, deterministic rule, heuristic, preference and workaround distinct.

## Data contract

For each data object and field capture:

`object_id`, `field_id`, label, type, required status, allowed values or format, source claim ID, source field, target field, transformation, validation, confidence, exception behavior and human-review requirement.

For each directed flow capture:

`flow_id`, source step/system/location, destination step/system/location, object ID, field IDs, schema/format, transport, trigger/frequency, transformation, validation, access constraint, failure/retry behavior, evidence claim IDs and `development_ready`.

## Evidence contract

Every material claim must contain:

`claim_id`, statement, knowledge type, evidence ID, exact file/page/sheet/cell/section/timecode, evidence mode, confidence, limitation and approval status.

Spoken evidence may prove stated logic or rationale. It cannot alone prove screen state, field mapping, file movement or completion.

## Gap contract

Every material unknown must contain:

`gap_id`, blocked contract IDs, missing fact, solution impact, smallest resolving question/evidence, owner, status and closure condition.

Use `unknown` plus a gap ID. Never hide missing detail behind verbs such as “process,” “handle,” “upload” or “review.”

Before emitting the gap, represent its atomic properties in `gap-closure-register.csv` as defined by `gap-closure-gate.md`. Preserve answered atoms with evidence, and ask only about unresolved, contradicted or observation-missing atoms. A gap with no such atom is closed and must not appear in open questions.

## Derived artifacts

- Generate `workflow.mmd` from step, decision and flow IDs. It must contain raw runnable Mermaid only.
- Generate implementation JSON/CSV only when exact schemas or interfaces improve downstream reliability.
- Do not generate a separate review BRD by default. `BRD.html` is both the complete review surface and canonical solution input.

## Conditional knowledge-object contract

Create `knowledge.json` only when approved content must be retrieved or reused independently of workflow execution. Each entry must contain:

`knowledge_id`, `type`, `title`, `content`, `applicability`, `keywords`, related step/decision/requirement IDs, evidence claim IDs, confidence, limitations, sensitivity/access label, owner, effective date, review date, approval status and superseded-by ID.

Allowed `type` values are `definition`, `policy`, `procedure`, `rule`, `heuristic`, `faq`, `example`, `exception` and `reference`.

Keep one business fact in one canonical location. Link from `knowledge.json` to BRD IDs instead of copying detailed step, field or flow contracts. Do not add chunks, embeddings, ranking fields, vector IDs or presentation markup; those belong to solution design.
