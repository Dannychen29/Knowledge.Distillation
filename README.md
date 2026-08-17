# Knowledge Distillation Codex Skills

This repository contains Codex skills for a knowledge distillation workflow.

Knowledge distillation is the process of turning business-user expertise, operational know-how, evidence, decisions, exceptions, and workflow details into structured knowledge that Codex can review, trace, validate, and use to build downstream solutions.

The goal of this package is not just to summarize what a business user says. The goal is to help Codex collect enough approved evidence to understand how work is actually done, identify what is known or unknown, preserve source traceability, and produce implementation-ready knowledge without guessing.

## What These Skills Help Codex Do

- Conduct a structured BU interview.
- Ask one focused question at a time.
- Capture business context, workflow steps, decisions, exceptions, controls, and acceptance criteria.
- Request only the smallest evidence needed to close real knowledge gaps.
- Process authorized documents, audio, screenshots, screen recordings, and transcripts.
- Preserve evidence IDs, paths, hashes, timecodes, confidence labels, and unresolved gaps.
- Produce a canonical `BRD.html` for human review and downstream solution building.
- Build a suitable solution only after the knowledge has been reviewed and approved.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `conduct-bu-interview` | Guides a BU discovery interview from case creation through requirement confirmation, workflow mapping, adaptive questioning, evidence request, and handoff to distillation. |
| `record-bu-walkthrough` | Controls an authorized Windows screen walkthrough with microphone when a real screen operation is needed to close a material gap. |
| `distill-bu-knowledge` | Converts one confirmed interview package and authorized evidence into a traceable, solution-ready canonical `BRD.html`. |
| `prepare-audio-evidence` | Prepares authorized audio or spoken evidence as a compact timecoded evidence package. |
| `extract-video-evidence` | Reduces authorized screen recordings into selected timecoded clips, frames, transcript slices, and evidence manifests. |
| `analyze-video-evidence` | Analyzes selected video evidence packages to extract screen actions, fields, workflow steps, decisions, exceptions, pain points, and open questions. |
| `build-bu-solution` | Selects and builds the smallest suitable solution from one participant-approved knowledge version. |

## Skill Workflow

The intended workflow is:

```text
conduct-bu-interview
  -> optional record-bu-walkthrough
  -> distill-bu-knowledge
     -> optional prepare-audio-evidence
     -> optional extract-video-evidence
        -> optional analyze-video-evidence
  -> build-bu-solution
```

## Typical Usage

Start with:

```text
$conduct-bu-interview
```

Use it when a BU participant needs to explain a business need, workflow, operational process, or pain point. The interview skill should confirm the requirement, map the workflow, identify gaps, request targeted evidence, and prepare the engagement for knowledge distillation.

After the interview package is confirmed, use:

```text
$distill-bu-knowledge
```

This skill turns the confirmed interview and authorized evidence into a canonical `BRD.html`. The BRD should include workflow steps, decisions, data flows, fields, exceptions, controls, evidence links, confidence labels, open questions, and development readiness.

After the knowledge is approved, use:

```text
$build-bu-solution
```

This skill decides what kind of solution is appropriate. The result might be a Skill, Script, Prompt, guided workflow, document template, knowledge base, tool specification, API integration, or another justified deliverable.

## Evidence Handling Principles

- Use only authorized evidence.
- Do not record screen or microphone without explicit permission.
- Do not copy credentials, unnecessary personal information, or unrelated sensitive material into reusable skills.
- Treat spoken descriptions as stated evidence, not visual proof.
- Treat screenshots as visible state, not proof of a click or causal action.
- Use timecoded video evidence when screen sequence, field mapping, or visible output matters.
- Preserve uncertainty instead of inventing missing information.

## Knowledge Quality Principles

- Keep every skill domain-neutral and reusable.
- Store engagement-specific facts in engagement artifacts, not in the skill package.
- Separate observed, stated, corroborated, inferred, and unresolved claims.
- Preserve source references for material claims.
- Do not infer business rules from memory, general knowledge, folder names, test data, or unrelated engagements.
- Keep solution-building gated behind participant-approved distilled knowledge.

## Expected Folder Structure

```text
skills/
  analyze-video-evidence/
    SKILL.md
  build-bu-solution/
    SKILL.md
  conduct-bu-interview/
    SKILL.md
  distill-bu-knowledge/
    SKILL.md
  extract-video-evidence/
    SKILL.md
  prepare-audio-evidence/
    SKILL.md
  record-bu-walkthrough/
    SKILL.md
README.md
.gitignore
```

Each skill may also include supporting `references/`, `scripts/`, `agents/`, or `assets/` folders.

## Maintenance Notes

When updating this package:

1. Update only the relevant files under `skills/`.
2. Keep skill instructions generic and reusable.
3. Remove generated cache files such as `__pycache__`, `.pyc`, logs, temporary files, and test outputs.
4. Confirm every skill still has a valid `SKILL.md`.
5. Commit only the skill package and general README content.
