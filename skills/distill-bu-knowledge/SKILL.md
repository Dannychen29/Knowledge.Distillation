---
name: distill-bu-knowledge
description: Transform one confirmed BU interview package and its authorized text, document, audio, image, spreadsheet or video evidence into a traceable, solution-ready canonical BRD.html for human review and downstream Codex solution building. Use after conduct-bu-interview when operational steps, decisions, fields, data flows, exceptions, controls, acceptance criteria and development blockers must be distilled without guessing.
---

# Distill BU Knowledge

## Generality boundary

Keep this Skill domain-neutral and reusable across organizational units. Do not embed any participant, department, industry, system, form, policy, field, threshold, workflow or domain acronym from a specific engagement in this Skill, its references, scripts or templates. Obtain all such knowledge from the active engagement and write it only into that engagement's distilled and approved artifacts. Examples in this Skill must use abstract placeholders rather than recognizable business cases.

Produce the development knowledge contract consumed by `$build-bu-solution`. Treat human-readable narrative as secondary.

Read [routing.md](references/routing.md), [distillation-contract.md](references/distillation-contract.md), [executable-step-contract.md](references/executable-step-contract.md), [html-brd-contract.md](references/html-brd-contract.md), [evidence-saturation-gate.md](references/evidence-saturation-gate.md), [gap-closure-gate.md](references/gap-closure-gate.md), [brd-quality-gate.md](references/brd-quality-gate.md), and [approval-gate.md](references/approval-gate.md).

## 1. Lock and route evidence

1. Select one engagement with a confirmed interview package.
2. Use only its authorized `00_intake/` and `10_evidence/` sources.
3. Run `scripts/inventory_evidence.py <engagement-path>`.
4. Route only evidence needed to resolve the required business and development contracts:
   - analyze text, documents, spreadsheets, PDFs and images directly with exact locations;
   - invoke `$prepare-audio-evidence` for required spoken evidence;
   - invoke `$extract-video-evidence`, then `$analyze-video-evidence`, when screen actions, fields or visible results must be proven;
   - reuse trustworthy transcripts after verifying their source and timestamps.
5. Preserve source IDs, paths, hashes, locations, timecodes and limitations. Never fill a gap from model memory or unrelated cases.

Do not trigger unapproved external downloads. If one evidence route is unavailable, mark only the affected claims unresolved and continue with the remaining evidence.

## 2. Saturate the evidence before synthesis

Apply [evidence-saturation-gate.md](references/evidence-saturation-gate.md) before writing BRD prose.

1. Extract atomic claims from every in-scope source before merging them. Preserve exact labels, source locations, field coordinates, allowed values, thresholds, conditionality, example values, template text, exceptions and corrections.
2. Build a coverage matrix keyed by source and knowledge type: trigger, actor, system/location, acquisition, input field, output field, transformation, decision, exception, control, deliverable and completion proof.
3. For timecoded media, account for every high-information interval. Mark it `consumed`, `duplicate`, `out_of_scope` or `unresolved`; never silently skip a dense field walkthrough because the end-to-end process is already understandable.
4. Keep `stated` field and rule knowledge when speech is explicit. Missing visual proof lowers evidence mode and development readiness; it does not erase the business detail or justify replacing it with a generic summary.
5. Run a second pass for enumerations and conditional language such as field numbers, columns, question numbers, required/optional, if/then, all/any, only, except, above/below and fallback. Link every retained atom to the contract ID that consumes it.

Do not begin canonical BRD synthesis until the saturation gate passes or every remaining omission is recorded as a targeted gap.

## 3. Build the canonical BRD

Write `20_distilled/BRD.html` as the single canonical BRD for both human review and solution building. Follow [html-brd-contract.md](references/html-brd-contract.md), use stable IDs and preserve the schema in [distillation-contract.md](references/distillation-contract.md). Do not maintain a separate Markdown BRD or review-only HTML with divergent content.

Render every operational step as a full step card conforming to [executable-step-contract.md](references/executable-step-contract.md). Never compress source, acquisition, input, action, output formation, destination, validation and completion proof into one `input → output` phrase or a shared “validation/completion” cell.

Cover:

- objective, scope, trigger, boundaries and success conditions;
- actors, systems, source and destination locations;
- operational steps with inputs, fields, actions, transformations, outputs and validation;
- decisions with evidence inputs, rules or heuristics, rationale, branches and missing-data behavior;
- data objects, schemas, field mappings and directed data flows;
- exceptions, retries, escalation, controls and human-only boundaries;
- deliverables, approvals, completion proof and retention requirements;
- functional and non-functional requirements relevant to solution design;
- scenario-based acceptance criteria;
- evidence links, confidence, gaps and development readiness.

Classify every material claim as `observed`, `stated`, `corroborated`, `inferred` or `unresolved`. Do not turn an inference or heuristic into a confirmed rule.

When the approved scope contains reusable knowledge that must be retrieved independently of the workflow, also produce `knowledge.json` using the knowledge-object contract. Typical signals are FAQs, policies, definitions, decision guidance, reusable cases or content expected to be searched across tasks. Do not create it when the BRD contracts already represent all required knowledge without duplication.

## 4. Close solution-blocking gaps

Apply [gap-closure-gate.md](references/gap-closure-gate.md) before emitting any open question. Treat each proposed gap as a hypothesis to disprove from all authorized evidence, not as a conclusion inherited from an earlier draft.

1. Split each proposed gap into atomic properties. Preserve answered atoms separately from unresolved, contradicted and observation-missing atoms.
2. Revisit every source, including later answers, corrections, demonstrations and examples. For timecoded evidence, link the initiating question to all answer intervals across the complete evidence set rather than only the nearest reply.
3. Keep explicit spoken facts as `stated`. If implementation still needs a screen or artifact, create a separate observation or UAT gap for that proof; never re-ask the business fact.
4. Maintain `gap-closure-register.csv` and run `scripts/validate_gap_closure.py` on it. Remove a gap when all of its atoms are answered or out of scope.
5. Generate the BRD gap table, readiness counts and `open-questions.md` from the same validated register. Do not hand-maintain divergent gap states in multiple artifacts.

For each remaining material unknown, record:

- stable gap ID;
- blocked step, decision, field, flow, requirement or acceptance test;
- impact on solution design;
- exact question or smallest evidence needed;
- owner and closure condition.

Ask only for the unresolved atom. Do not include answered context in the question except the minimum needed to identify the boundary being resolved.

Invoke `$conduct-bu-interview` only for targeted follow-up. Update only affected BRD contracts when new evidence arrives. Keep affected items `development_ready: false` until resolved.

## 5. Emit the minimal artifact set

Always produce:

- `BRD.html`: canonical semantic HTML containing the complete human-readable and Codex-readable BRD;
- `evidence-ledger.csv`: material claim-to-evidence mapping;

Produce only when needed:

- `workflow.mmd` for an operational workflow;
- `open-questions.md` when unresolved material gaps exist;
- `gap-closure-register.csv` when any proposed or open gap was evaluated;
- `knowledge.json` when reusable knowledge must be independently retrieved;
- other JSON or CSV contracts when exact fields, interfaces, decision tables or data mappings are required for solution implementation.

## 6. Validate and hand off

Apply [brd-quality-gate.md](references/brd-quality-gate.md). Verify that all stable IDs and facts agree across generated files.

Create a material-atom expectations CSV (`step_id,property,must_contain,evidence_id`) from the evidence ledger, then run `scripts/validate_brd_html.py <engagement-path>/20_distilled/BRD.html --expectations <engagement-path>/20_distilled/contract-evidence-expectations.csv`. When gaps were evaluated, also run `scripts/validate_gap_closure.py <engagement-path>/20_distilled/gap-closure-register.csv`. Fix every structural, schema-round-trip, vague-operation, unknown-without-gap, stale-gap, duplicated-question and broken-reference error before presenting the BRD. A plain structural `VALID` is not sufficient when a renderer or intermediate schema is used.

When `knowledge.json` exists, include it in the approval scope and verify that every entry is evidence-linked, non-duplicative, access-labelled and usable without adding unstated business rules. Do not design search, retrieval infrastructure, user interface or deployment in this Skill.

Present only `BRD.html`, material gaps and readiness blockers for confirmation. On approval, version and hash the approved machine artifacts under `30_approved/` according to [approval-gate.md](references/approval-gate.md).

Invoke `$build-bu-solution` only from the approved version and only after explicit authorization.

## Stop conditions

- Stop approval when a contradiction or gap would materially change the solution.
- Never mark screen actions or field mappings observed from speech alone.
- Never mark a contract development-ready when implementation would require guessing.
- Never build a solution from raw evidence or an unapproved BRD.
