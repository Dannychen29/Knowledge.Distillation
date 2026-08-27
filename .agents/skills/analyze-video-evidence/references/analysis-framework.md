# Analysis framework

Analyze each segment using the following lenses.

## Process

- Trigger and preconditions
- Actor and responsibility
- System, screen, document, or tool
- Input data and source
- Visible action and sequence
- Output and success signal
- Next step, loop, branch, or stop condition

## Decision knowledge

- Decision question
- Rule or threshold
- Evidence used
- Missing-data behavior
- Exception and escalation
- Final decision owner
- Every decision input, its source system/location, acquisition method, field, freshness and confidence
- Rationale, counterexample and downstream effect

## Operational knowledge

- Field names, file names, search terms, and naming rules
- Manual reconciliation and cross-system transfer
- Retry, workaround, wait, and duplicate entry
- Privacy, encryption, access, approval, and retention requirements
- Exact download/export/receipt source and exact upload/delivery destination
- Source-to-target field mapping, required fields, completeness rule and validation
- Deliverable format/template/version, recipient, channel, SLA, acceptance and proof of delivery

## Depth rule

Do not stop at an end-to-end narrative. Terms such as download, upload, process, review, decide and deliver are placeholders until the object, source, destination, fields and observable completion condition are known. Record unknown material details as targeted open questions.

For meeting recordings or walkthroughs where the participant explains the process without demonstrating the application, mark workflow facts as `stated`. Do not mark screen actions, field mappings, downloads, uploads, validation results or completion states as `observed` unless they are visible in frames/clips, interaction events, screenshots, exports or equivalent artifacts.

## Evidence mode

- observed: directly visible on screen
- stated: spoken by a participant
- corroborated: visible and spoken evidence agree
- inferred: analyst interpretation; requires confirmation
- unresolved: sources conflict or are insufficient

## Automation boundary

- deterministic: fixed transform or lookup
- ai_assisted: draft, classification, extraction, or recommendation with review
- human_review: AI may prepare evidence but a person must decide
- human_only: approval, accountability, risk acceptance, or restricted judgment
