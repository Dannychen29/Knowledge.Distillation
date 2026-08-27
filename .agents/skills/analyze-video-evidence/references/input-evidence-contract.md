# Accepted evidence package input

Accept evidence packages with schema_version 1.0.

Require:

- source identity and timeline duration;
- segments with unique segment_id values and valid start_ms/end_ms bounds;
- selection reasons, labels, confidence, normalized evidence, and review status;
- media paths when populated;
- unselected_intervals for completeness review;
- warnings for unavailable source media, ASR, OCR, redaction, or low reduction.

Treat the producer contract in $extract-video-evidence as authoritative. This consumer file records only the accepted version and validation boundary.

Reject unsupported major versions. Update scripts/validate_evidence_package.py and this file together when accepting a new producer version.

