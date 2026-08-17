# Canonical HTML BRD contract

Use one self-contained `BRD.html` as the canonical business requirements artifact for both people and Codex.

## Document rules

- Emit valid HTML5 with UTF-8, a descriptive title and language attribute.
- Keep all business content as selectable text in semantic HTML. Do not encode essential facts only in images, canvas, tooltips, JavaScript state or CSS-generated content.
- Use `main`, `nav`, `section`, `article`, `table`, `dl`, headings and lists according to meaning.
- Give every canonical section and every step, decision, field, flow, deliverable, requirement, acceptance scenario, claim and gap a unique stable HTML `id` equal to its contract ID when applicable.
- Add machine-useful `data-contract-type`, `data-evidence-mode`, `data-development-ready`, `data-confidence` and `data-gap-ids` attributes where relevant.
- Use anchor links such as `href="#ST-01"` and `href="#CL-001"` for all cross-references. Never rely on prose-only references that Codex must resolve heuristically.
- Put exact schemas, fields, rules, branches, evidence locations and readiness in tables or definition lists; do not hide them in decorative cards alone.
- Render each operational step as `article[data-contract-type="step"]` with the complete `data-step-property` set defined in `executable-step-contract.md`. A workflow summary table does not satisfy the step contract.
- Include visible metadata: engagement ID, version, status, scope, source coverage, updated time and approval state.
- Include concise CSS in the file and use no external runtime dependency. JavaScript is optional and may improve navigation only; the complete BRD must remain readable with scripts disabled.
- Keep print layout usable and expose URLs/paths as text where printing would otherwise remove meaning.
- Render gap rows, remaining questions and readiness counts from the validated `gap-closure-register.csv`. Do not preserve a stale gap table merely to keep stable IDs; retain the ID while updating or closing its current status from the register.

## Required section IDs

Use these top-level IDs:

`metadata`, `outcome`, `actors-and-systems`, `workflow`, `operational-steps`, `decisions`, `data-objects`, `data-flows`, `deliverables`, `exceptions-and-controls`, `requirements`, `acceptance-scenarios`, `gaps-and-readiness`, and `traceability`.

The visible section order may optimize review, but all sections must exist and navigation must link to them.

## Codex readability gate

Fail the artifact when:

- IDs are absent, duplicated or inconsistent with evidence and gap references;
- material content requires executing JavaScript;
- tables use merged visual cells that make row/column meaning ambiguous;
- styling changes the reading order;
- the HTML contains only a summary while detailed contracts live in another file;
- separate human and machine BRDs can diverge.
- any step merges source and acquisition, input and selection, content validation and completion, or output object and destination into an ambiguous cell;

Optional CSV, JSON or Mermaid support artifacts may be generated when useful, but `BRD.html` owns the canonical meaning. They must link back to stable HTML IDs and may not introduce new business facts.
