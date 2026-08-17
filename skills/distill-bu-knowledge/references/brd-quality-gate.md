# BRD quality gate

Reject the BRD as solution-ready if any material contract requires downstream Codex to guess.

## Contract checks

- Saturation: every high-information interval and material evidence atom is consumed, explicitly excluded, deduplicated or linked to a gap; exact fields, enumerations and conditions are not replaced by generic summaries.
- Scope: trigger, boundary, actors, systems, exclusions and success conditions are explicit.
- Workflow: every material step, branch, loop, handoff and terminal state has a stable ID.
- Operations: every step passes `executable-step-contract.md`, including acquisition, selection basis, ordered actions, output formation, separate content validation, completion condition and completion evidence.
- Decisions: each decision identifies owner, evidence inputs, rule or heuristic, rationale, outcomes, missing-data behavior and escalation.
- Data: material fields have types, required status, source-to-target mapping, transformation and validation.
- Exceptions: errors, retries, manual boundaries, risks and controls are represented.
- Delivery: output format, destination, recipient, approval and proof of completion are known.
- Acceptance: material requirements have testable scenarios and expected results.
- Traceability: every material claim links to exact evidence and an evidence mode.
- Evidence/content separation: precise stated knowledge is retained as `stated` even when missing visual proof keeps the related contract non-ready.
- Consistency: the same stable ID and fact have the same meaning in every artifact.
- Evidence-to-field round trip: material facts already present in transcripts, forms or spreadsheets survive rendering into their exact step property; defaults and `unknown` cannot overwrite them silently.
- Gap closure: every proposed gap was atomized and reverse-checked against all authorized evidence; answered atoms are not repeated in open questions, and missing observation proof is separate from the stated business fact.
- Gap consistency: the BRD, readiness counts, `open-questions.md` and audit references are generated from one validated gap register and use identical IDs, statuses and remaining questions.
- Reusable knowledge: when `knowledge.json` exists, each entry is independently understandable, evidence-linked, access-labelled, lifecycle-labelled and linked rather than duplicated where the BRD owns the fact.

## Readiness rules

Mark a step, decision, flow or requirement `development_ready: true` only when its material inputs, outputs, rules, error behavior and acceptance condition are known.

Mark it `development_ready: false` and link a gap ID when:

- a source, destination, field, rule or completion check is unknown;
- evidence conflicts;
- screen behavior or field mapping is supported only by speech;
- an exception could materially change implementation;
- acceptance cannot be tested without assumption.

Reject the entire BRD structure, regardless of readiness labels, when a step hides a missing property inside a broad `input → output` phrase, treats a renamed input as an output, or uses a vague operation without a linked gap.

The package is ready for solution building only when no unresolved development blocker affects the approved solution scope.

## Canonical HTML review and machine-reading gate

Generate one complete `BRD.html` containing:

- concise scope and readiness summary;
- navigable workflow;
- expandable step, decision, field and exception details;
- visible evidence mode and gap markers;
- acceptance scenarios and approval scope.

Validate it against `html-brd-contract.md`. The same semantic HTML must contain the complete canonical contracts; do not maintain separate human and machine BRDs.

Run the validator with a material-atom expectations CSV. Structural `VALID` without this content-alignment check is insufficient whenever BRD.html was generated from intermediate dictionaries, JSON, templates or code.

When gaps were evaluated, also run `validate_gap_closure.py`. Reject a package whose gap register contains a closed gap, a question on an answered atom, a broad question reused across atoms or unresolved rows without a smallest resolving evidence request.
