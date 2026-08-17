---
name: extract-video-evidence
description: Reduce an authorized business screen recording or video into a traceable, timecoded evidence package for one BU engagement. Use as a worker invoked by distill-bu-knowledge before deep video analysis, especially for long recordings where Codex should select high-value operations, decisions, exceptions and before/action/after states without analyzing the entire video at maximum cost.
---

# Extract Video Evidence

Operate as a media-reduction worker for `$distill-bu-knowledge`.

Read [selection-policy.md](references/selection-policy.md), [timeline-contract.md](references/timeline-contract.md), [media-adapter-contract.md](references/media-adapter-contract.md), and [evidence-package-contract.md](references/evidence-package-contract.md) when processing a recording.

1. Verify the source evidence ID, authorization, hash, engagement and analysis goal.
2. Run `scripts/extract_media_timeline.py` on the source video and local transcript to build a low-cost timeline from speech and visual changes. Report OCR and interaction events as unavailable when no approved adapter exists.
3. Select high-recall segments for operations, decision inputs and rationale, source acquisition/download, field entry and validation, destination upload/handoff, deliverable acceptance, exceptions, errors, outputs and explicit participant emphasis. Include before/action/after context around system transitions and handoffs.
4. Preserve the question or context that caused an important answer and the result that confirms an action.
5. Run `scripts/materialize_evidence.py` to create timecoded transcript slices, representative frames and contact sheets for each selected segment. Use the original video plus timecodes when motion review is required.
6. Write the package under `20_distilled/derived/video/<evidence-id>/evidence-package/`, run `scripts/build_evidence_manifest.py`, materialize its evidence, and validate its manifest.
7. Hand the package to `$analyze-video-evidence`.

Never discard an interval merely because it is silent, visually static or lacks transcript. Mark privacy-blocked and low-confidence intervals explicitly.
