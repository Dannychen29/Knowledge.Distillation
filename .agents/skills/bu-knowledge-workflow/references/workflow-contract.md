# Workflow and Handoff Contract

## State machine

| Current stage | Exit gate | Required exit artifact | State update and immediate next action |
| --- | --- | --- | --- |
| `interview` | [intake-contract.md](intake-contract.md) passes | `output/intake-package.md` | `current_stage: distillation`; invoke `$distill-bu-knowledge` |
| `distillation` | [spec-contract.md](spec-contract.md) passes | `output/normalized-prd.md`, `output/implementation-spec.yaml`, `output/implementation-spec.md` | `current_stage: solution_target_confirmation`; invoke `$build-bu-solution` to obtain final scope confirmation |
| `solution_target_confirmation` | BU confirms the intended outcome, included process scope, source availability and exclusions | `solution/target-confirmation.md` | `current_stage: solution_selection`; `$build-bu-solution` presents options |
| `solution_selection` | BU selects one documented option | `solution/solution-brief.md` | `current_stage: solution_build`; `$build-bu-solution` starts the selected build in the same task |
| `solution_build` | [solution-contract.md](solution-contract.md) build gate passes | Usable artifact plus `solution/test-cases.md` | `current_stage: validation`; invoke `$validate-and-improve-solution` |
| `validation` | [feedback-contract.md](feedback-contract.md) acceptance gate passes | `evaluation/validation-record.md` | Set `status: complete`; report usable solution and validation level |

## Required routing for a failed validation

| Classification | Route | Invalidate |
| --- | --- | --- |
| `intake_evidence` | `$conduct-bu-interview` | intake package and all downstream artifacts affected by the issue |
| `distilled_knowledge` | `$distill-bu-knowledge` | implementation spec (YAML and Markdown) and all downstream artifacts affected by the issue |
| `solution_implementation` | `$build-bu-solution` | solution artifact and affected tests only |
| `environment_access` | external blocker | no business-knowledge artifact |

## Resume behavior

On every entry, read `run-state.yaml` and the artifact named for the current stage. If an exit artifact exists but the state was not advanced, validate the exit gate once, advance state, and continue. If state says a later stage but the required upstream artifact is missing or invalid, route to the earliest missing stage and record the inconsistency.

No stage may silently change a confirmed business rule. New information is either a documented correction, an unresolved gap, or out of scope.
