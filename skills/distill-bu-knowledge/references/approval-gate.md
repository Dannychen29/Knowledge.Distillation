# Knowledge approval gate

Ask the participant to review only the canonical `BRD.html`, unresolved material gaps and the proposed approval scope.

On approval:

1. Copy the canonical machine artifacts to a new immutable version under `30_approved/`.
2. Record approver, time, scope, limitations, asset paths and SHA-256 hashes in `approval.yaml`.
3. Set the engagement status to `knowledge_approved` and the current gate to `solution_selection`.
4. Ask whether to invoke `$build-bu-solution` from that approved version.

On revision, update `20_distilled/` and repeat review. On pause, retain the approved version without starting solution production.
