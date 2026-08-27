# Solution Contract

Before selection, `solution/solution-options.md` compares two or three materially different options. Each option states the user, usable artifact, supported scope, human controls, limitations, implementation effort, and why it fits better than alternatives.

After selection, `solution/solution-brief.md` records the selected option, approved specification version, acceptance conditions, validation level target, and test cases. The build gate passes only when:

- the requested usable artifact exists under `solution/`;
- material behavior maps to implementation-spec IDs or is explicitly human judgment;
- a representative happy-path and an invalid, exception, or stop-path check have been run when applicable;
- the actual outputs were inspected against the stated acceptance conditions;
- limitations and required human control remain visible.

Planning documents alone do not satisfy the build gate when the requested solution is an executable or reusable artifact.
