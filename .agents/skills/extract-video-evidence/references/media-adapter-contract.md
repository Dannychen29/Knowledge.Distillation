# Media adapter contract

Keep vendor-specific endpoints outside the Skill. Provide these logical operations through an engineer API or local adapter.

## Probe

Input:

- source_uri

Output:

- source_id
- duration_ms
- video codec, dimensions, and frame rate when available
- audio codec and channels when available
- source hash or immutable version identifier

## Build timeline

Input:

- source_id
- requested signals: speech, OCR, visual change, interaction
- language hints
- privacy/redaction policy

Output:

- observations conforming to timeline-contract.md
- unprocessed intervals and failure reasons
- model or extractor versions

## Materialize evidence

Input:

- source_id
- intervals containing segment_id, start_ms, and end_ms
- requested outputs: clip, representative frames, transcript slice

Output:

- stable segment_id
- clip_uri or explicit unavailable reason
- frame URIs with timestamps
- transcript URI or inline timestamped transcript
- redaction status
- output hashes

## Operational requirements

- Make reads idempotent.
- Preserve the original recording.
- Require confirmation before any write to a business system.
- Return partial results with per-interval errors instead of failing the entire job.
- Never return credentials or unrestricted personal data in logs.

