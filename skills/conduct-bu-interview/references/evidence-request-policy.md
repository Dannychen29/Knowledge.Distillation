# Evidence request policy

Request evidence only when it closes a named gap.

Use this escalation order and stop as soon as the gap is resolved:

1. Targeted follow-up question.
2. Existing document, template, example or export.
3. Screenshot or short audio explanation.
4. Short, scoped screen walkthrough with microphone.

Recording is not a default interview deliverable. Use it only when time-dependent actions or visible state changes are material and lower-cost evidence is insufficient.

Spoken explanation alone is enough only for stated business intent, rationale or constraints. It is not enough to prove a screen action, field mapping, download source, upload destination, validation result or completion state when those details affect downstream development.

| Gap | Preferred evidence | Fallback |
|---|---|---|
| Required inputs or output format | Blank template plus one redacted completed example | Field list and annotated screenshot |
| Screen sequence or field mapping | Authorized screen recording with spoken explanation | Before/after screenshots plus narration |
| Spoken process with no operational proof | Smallest artifact or walkthrough that proves only the missing source, action, destination or completion state | Redacted screenshots, examples, templates, exports or logs |
| Decision rationale | Concrete case and counterexample | Follow-up interview with decision owner |
| Policy or threshold | Current approved document and section | Owner statement marked `stated`, not policy |
| Exception handling | Actual redacted exception case | Hypothetical walkthrough marked as such |

Before recording, state the target application, intended actions, expected duration, microphone requirement, storage location and sensitive-data precautions. Require an explicit yes in the conversation.
