# Gap closure gate

Prevent known evidence from surviving as a broad or stale open question.

## Atomic gap register

Create `gap-closure-register.csv` before writing the BRD gap table or `open-questions.md`. Use one row per atomic property with these columns:

`gap_id,atom_id,contract_id,property,fact,status,evidence_ids,evidence_mode,question,smallest_evidence_needed,owner,impact,closure_condition`

Allowed status values:

- `answered`: evidence resolves the atom; retain the fact and evidence but ask no question.
- `unresolved`: evidence does not resolve the atom.
- `contradicted`: authorized sources materially disagree.
- `observation_missing`: a business fact is stated, but a screen, artifact, field mapping, movement or completion state still needs proof.
- `out_of_scope`: the atom is explicitly outside approved scope.

Use engagement-local terminology only in the engagement register. Never add engagement terms or aliases to this Skill.

## Disprove gaps before asking

For every proposed gap:

1. Split broad concepts into the smallest independently answerable properties, such as source system, source location, acquisition action, eligibility rule, fallback, version policy, approver and completion proof.
2. Search all authorized evidence for each atom. Do not stop after the first interview answer or the segment that created the gap.
3. For timecoded interviews, revisit the initiating question, later answers, corrections, demonstrations, counterexamples and end-of-session recaps. Link every consumed interval.
4. Build a temporary engagement-local alias register for transcription variants when needed. Preserve the original transcript and record the alias as an analysis aid, not evidence or reusable domain knowledge.
5. Mark an explicit spoken answer `answered` with evidence mode `stated`. If visual proof is needed, add a separate `observation_missing` atom; do not change the spoken fact back to unresolved.
6. Remove any gap whose atoms are all `answered` or `out_of_scope`.

## Minimal-question rules

- Ask one independently closable question per unresolved, contradicted or observation-missing atom.
- Do not reuse one broad question for multiple atoms.
- State only the missing boundary. Do not ask the participant to repeat a known source, rule, fallback or deliverable.
- Request the smallest evidence that closes the atom, such as one redacted screen, one policy clause, one boundary example or one completion receipt.
- Separate business-rule, policy-boundary, control, observation/UI, UAT-asset and document-governance gaps. A missing UI path alone is not a missing business rule.
- Set priority from the unresolved atom's effect on behavior or acceptance, not from the total amount of missing detail in the parent step.

## Cross-artifact consistency

Generate all gap representations from the validated register:

- BRD gap rows and readiness counts;
- `data-gap-ids` references and development readiness;
- `open-questions.md`;
- audit and comparison references.

Fail the gate if an artifact retains a closed question, uses a different status for the same gap ID, or asks for an answered atom.

## Required validation

Run:

`scripts/validate_gap_closure.py <engagement-path>/20_distilled/gap-closure-register.csv`

The validator is structural. Human or model review must still confirm semantic atomization and evidence sufficiency, but a structural pass is required before presenting questions.
