# Run Workspace Contract

Keep each BU run separate from reusable agent instructions:

```text
runs/RUN-<timestamp>/
  input/
    prd/
    process-diagrams/
    documents/
    supporting/
    media/
    observations/
  output/
  solution/
  feedback/
  evaluation/
```

Codex creates a run only after the chosen entry mode and required intake material are confirmed. The BU user does not need to name or create a folder. In `ba-assisted` mode, Codex requests PRD, process diagrams, and case-specific supporting evidence; in `codex-led` mode, it requests those materials as the interview identifies gaps.

Treat `input/` as source material and avoid altering it. Place the normalized PRD and implementation-ready spec in `output/`; `$build-bu-solution` consumes them from there. Place usable solution artifacts in `solution/`, and human corrections or tuning notes in `feedback/`. Store case-level test evidence in `evaluation/`. Run folders are ignored by Git by default; the user decides when and how to version their work.
