# Evidence saturation gate

Prevent a detailed interview or walkthrough from collapsing into a plausible but shallow process summary.

## Required working registers

Before BRD synthesis, maintain:

- an evidence-atom register containing exact terms, values, field or question identifiers, conditions, examples, corrections and precise evidence locations;
- a coverage matrix joining each evidence atom to a step, decision, field, flow, deliverable, exception, requirement or gap ID;
- a media-interval disposition register for every selected or high-information interval: `consumed`, `duplicate`, `out_of_scope` or `unresolved`.
- a question-answer register for material interview questions, including the initiating question, all later answer, correction and example intervals, and the atomic contracts they resolve.

These may be temporary working data, but the material atoms and their traceability must survive in canonical artifacts.

## Extraction order

1. Extract without merging. Preserve the participant's granularity and do not normalize several fields into a broad object too early.
2. Reconcile duplicates and corrections while retaining separate provenance.
3. Classify evidence mode independently from information content. A precise spoken field rule remains `stated`; it is not converted to `unknown` merely because the screen was not visible.
4. Synthesize steps and flows only after field, rule, exception and deliverable inventories are complete.
5. Before finalizing gaps, run a reverse pass from every proposed open question to all sources. Consume later answers, corrections, demonstrations and examples; do not assume the nearest reply is the final answer.

## Enumeration pass

Search each source for enumerations and conditional markers, including:

- field, cell, column, sheet, question and section identifiers;
- named documents, systems, screens, lists, reports and templates;
- exact allowed values, thresholds, formulas, all/any conditions and override rules;
- required, optional, conditional, evidence-retention and screenshot requirements;
- source fallback, missing-data, no-result, retry, rejection and escalation behavior;
- output copies, attachments, naming, encryption, destination, approval and completion proof.

Every material item must be represented in a canonical contract or linked to a gap with a reason for exclusion.

## Saturation tests

Fail the gate when any condition is true:

- a high-information interval has no disposition;
- an exact field, question number, threshold or conditional rule appears in evidence but only a generic noun survives in the BRD;
- a named source or destination is replaced with `unknown` without recording the explicit stated detail and its evidence limitation;
- an exception, correction, fallback or override disappears during merging;
- a deliverable is named but its copies, components, conditional attachments or protection requirements are not inventoried;
- more detailed evidence is summarized away solely because it is transcript-only.
- an open question asks for a fact already retained as `stated`, `observed` or `corroborated`.

Passing saturation does not imply development readiness. Evidence strength, missing visual proof and unresolved implementation contracts are evaluated separately by the BRD quality gate.
