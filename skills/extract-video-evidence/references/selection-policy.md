# High-recall selection policy

## Retain

- Concrete UI actions: open, search, enter, select, compare, upload, download, save, submit, export, screenshot.
- Business rules and decision criteria.
- Exceptions, missing data, mismatches, errors, retries, workarounds, and escalation.
- Pain points, waiting, duplicated entry, cross-system switching, and manual reconciliation.
- Inputs, outputs, file naming, validation, approval, encryption, and archival behavior.
- Interview questions that establish the meaning of an answer.
- Results that verify whether an operation succeeded.
- Uncertain evidence whose removal could break cause-and-effect context.
- Document, form, spreadsheet, browser, terminal, dashboard or business-system surfaces even when speech is sparse.

## Usually exclude after review

- Greetings, room setup, repeated acknowledgements, and unrelated discussion.
- Long waits with no new speech, visible state change, or relevant result.
- Exact repetition that introduces no new condition, example, or correction.
- Pure meeting-gallery or participant-avatar intervals unless the speech contains a material decision, exception, correction or requirement that is not repeated elsewhere.

## Visual priority

Prefer intervals with visible working surfaces over participant-only meeting views when both carry similar speech signals. Raise priority for frames with dense text/table/form structure, application windows, document pages, spreadsheet grids, browser pages, system dialogs, pointer-driven navigation or visible before/after states. Lower priority for static meeting galleries that lack shared content, visible systems, documents, interactions or completion evidence.

## Context

- Add at least 5 seconds before a candidate and 8 seconds after it by default.
- Extend backward to include the triggering question or instruction.
- Extend forward to include the operation result or correction.
- Merge candidates separated by a short gap.

## Quality signals

Report selected coverage ratio, candidates by label, low-confidence segments, privacy-blocked segments, and unprocessed intervals caused by missing ASR, OCR, frames, or media access.

If coverage exceeds 80%, flag low_reduction. Do not shorten the package solely to improve this metric.
