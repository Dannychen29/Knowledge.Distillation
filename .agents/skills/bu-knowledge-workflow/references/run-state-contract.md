# Run State Contract

Each run has one current `run-state.yaml` at its root. It is the workflow control plane; artifacts are the source of truth for business content.

```yaml
run_id: RUN-<timestamp>
status: active # active | awaiting_bu | blocked | complete
intake_mode: codex-led # codex-led | ba-assisted
current_stage: interview # interview | distillation | solution_target_confirmation | solution_selection | solution_build | validation | complete
next_skill: conduct-bu-interview
next_action: collect_intake
iteration: 0
artifacts:
  intake_package: null
  normalized_prd: null
  implementation_spec: null
  implementation_spec_yaml: null
  solution_brief: null
  solution: null
  validation_record: null
open_item:
  kind: none # none | question | decision | evidence | external_blocker
  id: null
  prompt: null
invalidated_artifacts: []
```

## State rules

- `next_skill` is always one of `conduct-bu-interview`, `distill-bu-knowledge`, `build-bu-solution`, or `validate-and-improve-solution`; it is `null` only when `status: complete` or an external blocker prevents progress.
- `next_action` names the next concrete action, not a vague stage label. Examples: `ask_intake_mode`, `close_gap_GAP-003`, `select_solution_option`, `run_validation_case_VAL-001`.
- A stage writing an exit artifact must update state in the same turn. A stage may not claim handoff without this update.
- `awaiting_bu` requires exactly one `open_item` with a concrete prompt. On reply, clear it, restore `active`, and resume `next_skill`.
- `blocked` is reserved for a named external dependency, permission boundary, or unavailable material. It must include a resume condition in `open_item.prompt`.
- Upstream correction increments `iteration`, records invalidated artifact paths, and sets the earliest affected `current_stage` and `next_skill`.

## Workbook build state rule

When a selected solution writes an `.xlsx`, the RMA workbook-build contract's openpyxl path is a normal supported build path. Do not set `status: blocked` merely because a separately named spreadsheet or artifact writer is absent. After the schema, mapping JSON, reviewable mapping workbook and filled workbook copy pass that contract's verification, set `current_stage: validation`, `next_skill: validate-and-improve-solution` and a concrete validation `next_action`.

For workbook generation, `blocked` is permitted only when the input template is missing, the output location is not writable, the input/output file is corrupt, or validation fails and neither openpyxl nor the contract's controlled OOXML/ZIP fallback can repair it. In all other cases keep the workflow active and route to the next concrete action.
