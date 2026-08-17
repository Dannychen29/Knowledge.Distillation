# Screen action register contract

Create one row per evidence-backed operation with:

`action_id, actor, trigger, system, screen, precondition, before_state, action, target_control, source_system, source_location, acquisition_method, source_object, source_fields, required_fields, transformation, destination_system, destination_location, target_fields, after_state, observed_result, completion_check, spoken_rationale, decision_id, deliverable_id, exception, gap_question_ids, evidence_mode, confidence, segment_id, start_ms, end_ms, source_refs`

Use `observed` only when visual evidence establishes the operation. A static frame may establish `screen_state_observed`, but not a click or causal result. If an action is only narrated, use `stated`; if speech and visuals independently support it, use `corroborated`.

Redact credentials and personal data. Preserve system labels and field names only when authorized and necessary.
