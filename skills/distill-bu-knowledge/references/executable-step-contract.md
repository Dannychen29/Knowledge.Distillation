# Executable step contract

A step is executable only when a qualified person or downstream solution can locate its source, acquire the input, perform the action, create the output and prove completion without guessing.

## Required step properties

Represent each property separately. Never merge them into an `input → output` summary.

1. `trigger`: event or state that starts the step.
2. `preconditions`: permissions, prior outputs, versions and states required before starting.
3. `actor`: accountable role; distinguish operator, decision owner and approver.
4. `source_system`: exact application, report, email, shared folder, website or document.
5. `source_location`: screen, menu path, URL class, mailbox, folder path, sheet, table, column, cell or section.
6. `acquisition_method`: ordered actions used to open, query, filter, download, export, receive or copy the source.
7. `selection_basis`: why a record belongs in scope; include list membership, status, date, amount, account type, review cycle and exclusion rules.
8. `input_object`: exact object and version.
9. `input_fields`: field IDs, labels, types, required status, allowed values and freshness.
10. `action`: ordered operator or system actions; identify controls, searches, comparisons, calculations and decisions.
11. `transformation`: source-to-target mapping, formulas, normalization, defaults and conditional derivation. Renaming an input object is not a transformation.
12. `output_object`: exact file, record, folder, decision or state created or updated.
13. `output_formation_rule`: conditions for creating versus updating the output, naming/key rules, folder or record creation rules, copy count and template/version.
14. `destination_system` and `destination_location`: exact save, upload or handoff target.
15. `content_validation`: checks on values, fields, mappings, formulas, completeness and consistency.
16. `process_completion_condition`: observable state that means the action finished successfully.
17. `completion_evidence`: screenshot, log, status, file hash, saved record, approval, receipt or audit entry proving completion.
18. `failure_and_fallback`: not-found, missing, stale, conflicting, access-denied, retry, escalation and manual fallback behavior.
19. `evidence_claim_ids`, `gap_ids` and `development_ready`.

## Precision rules

- Treat phrases such as “get the list,” “create a record,” “download the source document,” “fill the form,” “check completeness,” “process,” “review,” “upload” and “complete” as placeholders until the exact object, location, actions, conditions and proof are stated.
- Do not invent a folder, record, case or output merely because the workflow needs one. If evidence does not say whether an output is a folder, system record, spreadsheet row or document, record `unknown` and link a gap.
- Separate three different questions:
  - input eligibility: is this the correct and current input?
  - content validation: are the output values and mappings correct?
  - process completion: is the output saved, delivered, approved or otherwise proven complete?
- When a source is only described generally, retain the stated detail and mark only the missing location or acquisition property unknown. Do not reduce the entire step to unknown.
- A step with any material unknown property is `development_ready: false`, but its evidenced properties must remain explicit.

## HTML representation

Use one `article[data-contract-type="step"]` per step. Inside it include elements carrying all of these `data-step-property` values:

`trigger`, `preconditions`, `actor`, `source-system`, `source-location`, `acquisition-method`, `selection-basis`, `input-object`, `input-fields`, `action`, `transformation`, `output-object`, `output-formation-rule`, `destination-system`, `destination-location`, `content-validation`, `completion-condition`, `completion-evidence`, `failure-fallback`, `evidence`, and `gaps`.

Use the literal `unknown` only with a non-empty `data-gap-ids` attribute and a visible link to the corresponding gap.

## Source-to-HTML schema round-trip gate

The extraction model, renderer and HTML must use one canonical property vocabulary. If an authoring language requires safe aliases such as `source_system`, normalize them explicitly to `source-system` before rendering.

- Reject unsupported source keys; never let a dictionary update silently add an unused alias.
- Reject two source keys that normalize to the same HTML property.
- Render every required property exactly once.
- Maintain a compact expectations CSV for material evidence atoms with `step_id,property,must_contain,evidence_id`.
- Validate that each expected fragment appears in the named HTML property. A structurally complete step that fell back to default or `unknown` while evidence already supplied the fact is invalid.
- Negative-test the renderer by misspelling or changing one canonical property and prove validation fails.
