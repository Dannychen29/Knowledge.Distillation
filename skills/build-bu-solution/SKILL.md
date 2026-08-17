---
name: build-bu-solution
description: Select and build a fit-for-purpose BU solution from one participant-approved knowledge version. Use after distill-bu-knowledge when Codex must decide whether the need is best met by a Skill, Script, Prompt, guided workflow, document template, tool specification, API or system integration, then build only the justified deliverables without forcing a Skill or a fixed output bundle.
---

# Build BU Solution

Read [solution-selection.md](references/solution-selection.md) and [solution-contract.md](references/solution-contract.md).

## Generality boundary

Keep this Skill domain-neutral and reusable across organizational units. Do not embed any participant, department, industry, system, form, policy, field, threshold, workflow or domain acronym from a specific engagement in this Skill, its references, scripts or templates. Obtain all such knowledge from the selected approved engagement version. Put engagement-specific instructions, mappings, terminology, examples and tests only in that engagement's final Solution under `40_solution/build/`.

## 1. Verify the knowledge gate

1. Select one engagement and one version under `30_approved/`.
2. Verify approval scope and artifact hashes.
3. Stop and return to `$distill-bu-knowledge` when approval is missing, stale or outside the intended task.
4. Never build from raw evidence or silently add business rules from general knowledge.
5. For software, integration or automation work, verify the approved knowledge includes development-ready operational steps and directed data flows with stable IDs, source/destination locations, payload fields/schema, transport, validation and failure behavior. Return unresolved nodes or edges to `$distill-bu-knowledge`; do not infer interfaces from a narrative flowchart.

## 2. Choose the smallest sufficient solution

Assess the task's repeatability, variability, data volume, deterministic logic, judgment, tool access, risk, auditability, maintenance owner and human controls.

Possible solution types include:

- Skill for reusable judgment or guided work that benefits from managed instructions and references;
- Script for deterministic transformation or repetitive file handling;
- Prompt for a narrow, low-risk, low-maintenance interaction;
- guided workflow or template for structured human execution;
- knowledge base when approved knowledge must be searched, browsed, reused or governed across users or tasks;
- tool/API/system integration when live data or controlled actions are required;
- a justified combination of the above.

Do not choose a Skill merely because Skills are easy to manage. Record why the selected type fits better than the rejected alternatives.

When considering a knowledge base, read [knowledge-base-selection.md](references/knowledge-base-selection.md). Treat an approved `knowledge.json` as source content, not as a finished knowledge base. Select a knowledge base only when retrieval or knowledge lifecycle needs justify a product beyond direct BRD use.

For regulated, template-driven or repeated form-filling and document-generation work, use structured data as the canonical intermediate. Default to a machine-readable schema and values plus an Excel review workbook when fields require comparison, correction, validation or batch processing. Add a Word renderer only when the participant explicitly requests Word or a controlled template, legal process or external submission requires it. Do not make direct `.docx` editing the primary data layer.

## 3. Specify before building

Complete `40_solution/solution-brief.yaml` with the user, problem, inputs, outputs, approved knowledge version, chosen solution type, human controls, limitations and acceptance conditions.

For software, integration or automation solutions, derive interfaces, modules and acceptance tests from approved step IDs, decision IDs, data-object IDs, data-flow edges and deliverable contracts. Preserve those IDs in implementation requirements and tests.

For a knowledge-base solution, define the approved corpus, user questions, retrieval method, access controls, source citations, freshness and update workflow, versioning, fallback behavior, evaluation set and human ownership before building.

Ask for confirmation when different solution types would materially change cost, risk, ownership or user experience.

After writing the proposed brief, set `engagement.yaml.current_gate: solution_selection` and immediately present the smallest required selection question. Do not return a brief link without guiding the participant to the decision.

## 4. Build only approved deliverables

1. Create outputs under `40_solution/build/` using the appropriate creator or implementation workflow.
2. When the selected solution type includes a Skill, invoke `$skill-creator` to create or update it under `40_solution/build/`, following its initialization, resource design, metadata and validation workflow. Do not invoke `$skill-creator` when another solution type is sufficient.
3. Keep approved business knowledge in references or data files and operational instructions in the solution logic.
4. Preserve claim IDs or source mappings for material rules and decisions.
5. Validate inputs, expose assumptions, stop on unsupported exceptions and retain required human approvals.
6. Do not copy raw recordings, credentials or unnecessary personal information into reusable solutions.
7. When producing Word, validate the structured values first, render into the identified template version, then inspect the resulting document for missing fields, overflow, broken tables, pagination and unsupported controls before delivery.
8. When producing a knowledge base, ingest only approved knowledge artifacts; preserve knowledge and claim IDs through indexing and responses; enforce access labels before retrieval; return citations and uncertainty; and test representative questions, unsupported questions, conflicting content and stale content.

### Deliverable-first contract

Treat the participant's requested usable artifact as the deliverable. A solution brief, plan, gap report, readiness report, blocker report, test log or validation note is supporting process evidence and never satisfies a request to produce a Solution.

Before building, write one sentence internally in the form: `The participant will use <artifact> to <outcome>.` The artifact named there must exist under `40_solution/build/` and be the first item reported at handoff. Do not mark the build complete when only YAML, Markdown, specifications or diagnostics exist unless one of those formats is itself the participant-requested Solution.

When the participant narrows or corrects scope, immediately realign `solution-brief.yaml`, remove or clearly archive agent-created out-of-scope draft artifacts, and build the corrected deliverable in the same task. Do not make the participant restate the correction.

### Runtime preflight and fallback

Perform a minimal runtime and dependency preflight before writing substantial implementation code. Distinguish between:

- authoring the participant's final artifact now; and
- building a runnable Solution that will author or transform the artifact in the participant's intended runtime.

If a format-specific creator cannot author the final artifact in the current environment, follow that creator's restrictions for the final artifact. Still build a runnable Solution for the participant's available target runtime when this remains within the confirmed solution type and can be tested without inventing business behavior. For example, a script intended to run against a controlled local application may be a valid Solution even when the current environment cannot use that application to author the final business file. Record the unexecuted end-to-end validation honestly.

Stop with only a blocker report only when no in-scope implementation path can produce a usable artifact. State the exact missing capability and the smallest resume condition. Do not let a missing preferred tool hide an available, policy-compliant implementation path.

### Mandatory implementation verification

For every executable deliverable:

1. Run the language parser, compiler, type checker or linter before the first smoke test. For PowerShell, parse the script or invoke it with a minimal safe fixture; do not assume generated syntax is valid.
2. Run at least one representative happy-path smoke test and one unsupported, invalid or stop-path test when the Solution contains validation or business controls.
3. Inspect the actual output, not only the process exit code. Verify key values, formulas, files, states or API results against the acceptance conditions.
4. If parsing, execution or output verification fails, fix the implementation and rerun the affected checks in the same task. A first failure is work in progress, not a handoff condition.
5. Never describe an executable as built, runnable, completed or validated while its latest parser, smoke or output check is failing.

For artifact-producing Solutions, verify a representative generated artifact when the runtime is available. When it is unavailable, deliver the tested implementation with an explicit `end_to_end_validation_pending` limitation; do not substitute planning documents for the implementation.

### Source-grounded validation gate

Do not confuse executable-code validation with business-solution validation. Before claiming that a Solution can produce a business deliverable:

1. Inventory the registered current-engagement source artifacts and test fixtures. If a relevant real, anonymized or participant-provided fake artifact exists, use it in the end-to-end test. Do not replace it with model-invented values.
2. Build a field-level coverage map from each material output field to its evidence ID, source file, page/question/cell or source field, transformation, target field, and validation result. Mark fields supplied by human judgment separately.
3. Use registered fake data or an anonymized case for at least one end-to-end validation when production data cannot be used. Preserve provenance showing who supplied or derived it and which source structure it represents.
4. Treat model-invented data only as a structural fixture for parser, schema or formula smoke tests. Label it `synthetic_structural_only`; it cannot satisfy source mapping, business-rule or end-to-end acceptance conditions.
5. Exercise the actual source-to-output path. Parse the registered source artifact or registered fake equivalent, map supported source fields to the target deliverable, combine explicitly required additional sources or human inputs, generate the output, and inspect mapped fields and calculated results.
6. When required sources are missing, produce a partially completed artifact with explicit unresolved fields when safe and useful. Do not fabricate values to make the happy path pass.

Record validation level explicitly:

- `structural_smoke_passed`: syntax, schema or formula mechanism passed using model-invented or minimal structural values;
- `registered_fake_data_passed`: a registered fake or anonymized source traversed the actual source-to-output path;
- `source_grounded_passed`: registered engagement evidence traversed the actual path and material mappings were checked;
- `business_validated`: the participant or named owner compared the output with an expected completed case and accepted it.

Never report a higher level than the evidence supports. A generated final-format file is not proof of source-grounded correctness by itself.

## 5. Report status without inventing validation

Report what was built, its knowledge version, supported scope, limitations, required human controls and what still needs validation. Mark the solution `draft` or `validation_pending`; do not claim that it passed formal validation because that mechanism is intentionally deferred.

Lead the report with the usable Solution artifact. Link process metadata only after the deliverable and only when it helps the participant act. If no usable Solution artifact exists, say the build is incomplete; do not present supporting documents as the requested result.

## Mandatory continuation contract

1. Verify that the invoked engagement is at `current_gate: solution_selection` or `solution_build` and that its approved knowledge version is immutable and hash-valid.
2. If the participant has already confirmed the proposed solution type, update `solution-brief.yaml.status: confirmed`, set `current_gate: solution_build`, and begin building in the same task. Do not ask for the same confirmation again.
3. If confirmation is still required, ask exactly one decision question that explains the material trade-off; do not stop with a recommendation-only report.
4. After building, set `engagement.yaml.status: solution_draft` and `current_gate: solution_validation`, then guide the participant to the smallest next validation action.
5. Stop without building only for a precise knowledge gap, permission boundary or participant-requested pause. Record the reason and route back to the named upstream gate.

## Loop rule

If building reveals missing or contradictory business knowledge, create a precise gap report and return to `$conduct-bu-interview` for targeted confirmation, then re-run affected distillation. Do not patch uncertain logic directly into the solution.
