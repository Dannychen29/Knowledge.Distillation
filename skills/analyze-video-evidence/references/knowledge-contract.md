# Knowledge package contract

Use UTF-8 JSON with schema version `1.1`.

## Required top-level fields

- `schema_version`
- `source_manifest`
- `analysis_limits`
- `processes`
- `operational_steps`
- `decisions`
- `exceptions`
- `pain_points`
- `systems`
- `data_objects`
- `data_flows`
- `deliverables`
- `open_questions`
- `evidence_index`

`processes` is a navigational overview. The executable knowledge is held in `operational_steps`, `decisions`, `data_objects`, `data_flows` and `deliverables`; these must not be replaced by narrative prose.

## Common claim shape

Every substantive item must contain `id`, `statement`, `evidence_mode`, `confidence`, `automation_boundary` and one or more evidence references. Each evidence reference contains `segment_id`, `start_ms`, `end_ms`, and optional `source_refs`.

## Operational step

Each item in `operational_steps` additionally requires:

- `sequence`, `actor`, `trigger`, `preconditions`;
- `source`: `system`, `location`, `acquisition_method`, `object`, `version_or_freshness`, `fields`;
- `action`: `system`, `screen`, `control`, `operation`, `transformations`;
- `destination`: `system`, `location`, `object`, `fields`;
- `required_fields`, `validation`, `completion_evidence`;
- `decision_ids`, `deliverable_ids`, `exception_ids`, `gap_question_ids`.

For workflow or development-handoff analysis, every step must also be reducible to a diagram label with `actor`, `action`, `input_object`, `output_object`, `evidence_mode` and `gap_status`. If any of these values is missing, the step is incomplete even when the narrative is understandable.

## Decision

Each item in `decisions` additionally requires `question`, `owner`, `inputs`, `rule_or_heuristic`, `rationale`, `missing_input_behavior`, `conflicting_input_behavior`, `counterexamples`, `downstream_effect`, `exception_ids`, `escalation`, and `gap_question_ids`. Every decision input requires `name`, `source_system`, `source_location`, `acquisition_method`, `field`, `freshness`, and `required`.

## Deliverable

Each item in `deliverables` additionally requires `name`, `content_schema`, `required_fields`, `completeness_rule`, `format`, `template_version`, `recipient`, `delivery_channel`, `destination`, `timing_or_sla`, `approval_owner`, `acceptance_check`, `naming_rule`, `retention_rule`, `proof_of_delivery`, and `gap_question_ids`.

## Data flow

Each directed item in `data_flows` additionally requires `from_node_id`, `from_system`, `from_location`, `to_node_id`, `to_system`, `to_location`, `data_object_id`, `fields`, `format_or_schema`, `transport`, `trigger`, `frequency`, `transformation`, `validation`, `access_constraints`, `failure_or_retry`, `development_ready`, and `gap_question_ids`. `development_ready` must be `false` when any material I/O contract detail is `unknown`.

`development_ready` also requires evidence strong enough for implementation. A data flow supported only by `stated`, `inferred` or `unresolved` evidence is not development-ready unless equivalent artifacts prove the source, destination, payload, schema, transport, validation and completion contract.

Every flow must have a diagram edge label that names the moved data object or decision output. Do not allow unlabeled arrows in workflow diagrams. If the payload, source, destination or transport is unknown, the edge label must contain `unknown` and the linked gap ID.

## Unknowns and gaps

Use the literal string `unknown` only when evidence is insufficient. If any required operational, decision or deliverable detail is `unknown`, `gap_question_ids` must reference an item in `open_questions`. Each open question requires `id`, `question`, `reason`, `owner`, `blocking_impact`, and `smallest_evidence_needed`.

When a participant describes an operation but the screen or equivalent artifact is absent, create an `open_questions` item for the missing observation. The `smallest_evidence_needed` should be targeted, such as a short walkthrough, redacted screenshot pair, blank template plus completed example, export, field dictionary or audit log.

An empty array is valid only when the agreed scope genuinely has no item of that type. Do not use an empty array to avoid documenting an observed decision, handoff or deliverable.
