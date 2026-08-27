# Implementation-Ready Spec Contract

The distilled spec is the shared source for target confirmation, solution selection and later tuning. Write it in two synchronized forms:

- `output/implementation-spec.yaml` is the canonical, machine-readable source for Codex. Use stable IDs and explicit structured values; do not hide material rules only in prose.
- `output/implementation-spec.md` is a human-readable rendering of the same content, with source links and concise explanations.

`output/normalized-prd.md` remains the human-readable statement of business problem, outcome, scope, constraints and acceptance intent.

Use [implementation-spec-schema.yaml](implementation-spec-schema.yaml) as the required shape for the canonical spec; omit only sections that are demonstrably out of scope, and record the reason.

The canonical spec must include:

- objective, users, scope, and known constraints;
- source-evidence references, including BA interview process diagrams and document templates, plus the generated normalized PRD;
- numbered stages and workflow steps, each with `input`, `action`, `output`, owner or system, and validation when known;
- for each system interaction that is known: `system_id`, starting page or object, navigation path, UI action (for example button/menu/query), download or export artifact, extracted fields, and evidence location. Mark unavailable detail as `unresolved`; never invent a click path;
- structured field mappings with source field, transformation, target field or cell, evidence, status, and human control;
- decisions, exceptions, and explicit unknowns only where they materially affect a solution;
- acceptance conditions that a BU user can review.

It must also assign stable IDs to material workflow steps, decisions, data mappings, exceptions, and acceptance cases. Every material rule must be classified as confirmed, inferred, or unresolved and linked to a source or named human confirmation.

For a workbook solution, also create a target-template schema, a mapping JSON, and a reviewable mapping workbook as defined in the RMA workbook-build contract before any final-form write. Use that contract's approved openpyxl path (and, only when required, its controlled OOXML／ZIP fallback); do not treat the absence of a differently named artifact writer as a blocker. Do not declare the spec ready when a material step lacks an input or output. Ask for the smallest missing evidence or mark it as a visible blocker. Keep the current working spec editable; versioning is controlled by the user through Git when they decide it is appropriate.
