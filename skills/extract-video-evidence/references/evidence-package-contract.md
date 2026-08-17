# Evidence package producer contract

This Skill owns the evidence package schema. Emit schema_version 1.0.

## Required manifest fields

- schema_version
- selection_policy
- goal
- source
- timeline
- parameters
- stats
- warnings
- segments
- unselected_intervals

## Required segment fields

- segment_id: stable chronological identifier
- start_ms and end_ms: valid source-video bounds
- duration_ms
- confidence and mean_signal_score
- labels and reasons
- evidence: normalized observations that triggered selection
- media: clip, frames, and transcript paths or explicit null/empty values
- review_status

## Ownership

- Keep detailed producer rules in this Skill.
- Increment the major schema version for breaking field or semantic changes.
- Preserve original source identity and unselected intervals.
- Update downstream consumer validation in $analyze-video-evidence before releasing a breaking version.

Do not use the project overview document as an executable schema source.

