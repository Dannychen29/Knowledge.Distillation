---
name: conduct-bu-interview
description: Conduct a domain-neutral BU discovery in Codex text chat, from case creation and requirements confirmation through adaptive deep interview and evidence collection. Use when a BU participant needs to explain a business need or workflow and Codex must find information gaps, ask one question at a time, request documents or examples, arrange an authorized screen recording with microphone, and produce a confirmed interview package for knowledge distillation.
---

# Conduct BU Interview

## Generality boundary

Keep this Skill domain-neutral and reusable across organizational units. Do not embed any participant, department, industry, system, form, policy, field, threshold, workflow or domain acronym from a specific engagement in this Skill, its references, scripts or templates. Obtain all such knowledge from the active engagement and write it only into that engagement's artifacts. Examples in this Skill must use abstract placeholders rather than recognizable business cases.

Keep the participant in the Codex conversation. Run scripts internally; never ask the participant to use a terminal or manually locate recording controls.

Read [interview-protocol.md](references/interview-protocol.md) before questioning. Read [evidence-request-policy.md](references/evidence-request-policy.md) before asking for files or recordings. Apply [completeness-gate.md](references/completeness-gate.md) before handoff.

## 1. Open or resume one engagement

1. Resume an existing engagement only when the user clearly identifies a folder containing `engagement.yaml`. Lock that absolute folder path for the task; do not ask for its storage root again.
2. For every new engagement, resolve the current Windows Documents folder internally, propose `<Documents>/BU Knowledge Engagements` as the default storage root, and ask one short confirmation before creating files. Say where the new case will be stored and allow the participant to provide another local, synced or department folder. Do not guess a localized Documents path, ask them to use a terminal, or require them to express the path in a technical format.
3. After the participant confirms the default or another unambiguous folder, resolve one absolute storage-root path and run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/new_engagement.ps1 -StorageRoot <confirmed-root> -StorageConfirmed`. The script creates a neutral `ENG-<timestamp>/` folder directly below that root and leaves `title` blank.
4. Never infer the business, case title, participant role or requirements from the current workspace, repository, folder path, package name, prior conversation outside the engagement, another engagement, or test data. Treat these only as execution context. Keep the temporary folder neutral and `title` blank until the participant confirms the requirements brief.
5. Keep the returned absolute engagement path as the single active engagement for the rest of the interview, evidence work, distillation and solution handoff. Record it in `engagement.yaml`. Do not ask about storage again during the same engagement; ask again only when the user explicitly starts another new engagement.
6. Never store engagement outputs in the Skill, Plugin, `workspace-mode` or delivery-package folder. If the confirmed destination is inside those folders, explain the separation requirement and request another destination.
7. Never import facts from another engagement, test fixture, mock or synthetic dataset, or prior solution unless the user explicitly selects it as evidence for the current engagement. Keep its provenance and non-production status visible.

## 2. Confirm the need before the deep interview

1. Confirm the business context, participant role, problem or opportunity, intended users, product goal, expected outcome, scope, constraints, authorization, available evidence, and why Codex may be suitable.
2. Ask only one short question at a time. Do not force the participant to define technical architecture or a fixed deliverable.
3. Draft `00_intake/requirements-brief.md` and present it for correction.
4. Treat this as interview preparation within the same stage. Continue only after the participant confirms the brief.
5. Only after that confirmation, derive a short case title from the participant-confirmed objective and run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/name_engagement.ps1 -EngagementPath <active-engagement-path> -Title <confirmed-title>`. Replace the locked active path with the returned renamed path. Never name or rename the case from execution context.

## 3. Map the current workflow

1. Ask the participant to describe one ordinary case from trigger to final outcome.
2. Reconstruct actors, phases, handoffs, systems, inputs, outputs, visible decisions and exceptions.
3. Show the end-to-end map and ask what is missing, out of order or performed by someone else.
4. Separate `stated_workflow` from `observed_or_supplied_evidence`. A meeting explanation may establish what the participant says happens, but it does not prove screen sequence, field mapping, file movement or completion state.
5. Do not select a narrow deep-dive area until the participant confirms the process landscape.

## 4. Run adaptive deep questioning

1. Use the latest answer and coverage record to decide the next question.
2. Probe decision cues, rationale, heuristics, thresholds, counterexamples, exceptions, workarounds, escalation, controls and acceptance conditions.
3. Distinguish facts, participant statements, assumptions, hypotheses and unresolved items.
4. Update `00_intake/interview-record.md` and `coverage.yaml` throughout the interview. For each material gap, record a stable gap ID, gap type, affected step or data-flow ID when known, blocking impact, smallest evidence needed, evidence requested, evidence received and whether the participant accepted it as a limitation. Reference transcript segment IDs for any post-recording follow-up.
5. Stop repeating a topic when another person or a piece of evidence is required; request that evidence instead.

## 5. Choose the smallest evidence needed for each gap

- First decide whether the current answers are already sufficient for the confirmed task. Do not request more evidence merely because another evidence type is available.
- For each material gap, choose the least burdensome evidence that can resolve it: a targeted answer, existing document, blank template, completed example, export, screenshot, short audio explanation, or screen walkthrough.
- Request the exact evidence needed and explain which named gap it resolves. Never follow a fixed evidence checklist.
- Treat a spoken end-to-end process with no supporting artifact or observation as incomplete when the intended outcome requires software development, automation, form filling, field mapping, cross-system handoff or UI guidance. Ask for the smallest targeted proof of the missing I/O, such as a focused walkthrough, screenshot set, source artifact, target artifact or system export for only the missing step.
- Request a screen recording only when dynamic screen sequence, field mapping, visible result, cross-system handoff, exception handling, or tacit judgment cannot be reconstructed reliably from conversation and existing artifacts.
- When recording is justified, ask for explicit permission to record only the target application and microphone. Prefer a short targeted recording over a full-day or full-process recording.
- After the participant agrees and brings the target application to the foreground, invoke `$record-bu-walkthrough`. Codex must start and stop the recorder, save the recording to the engagement and report whether an audio track was detected.
- When the recorder stops, wait for its fast timecoded transcript package. Review that transcript against the named gap while the participant is still available. Ask only the smallest follow-up needed; do not begin full video distillation yet.
- If the transcript shows enough information, summarize the observed operation and spoken rationale for participant correction. If it does not, return to a targeted question, document request or short additional walkthrough instead of restarting the interview.
- If recording is unavailable, request the smallest viable substitute and record the limitation. Never claim an action was observed from a verbal description alone.

## 6. Confirm and hand off

1. Present a concise summary of the need, process, decisions, exceptions, collected files and remaining gaps.
2. Ask the participant to correct or confirm the interview package.
3. Mark `ready_for_distillation: true` only after confirmation and when every material gap is either resolved or explicitly accepted as a limitation. If a remaining gap blocks development-ready I/O, field mapping, decision input provenance, delivery destination or completion proof, keep `ready_for_distillation: false` unless the participant explicitly accepts that distillation will carry a non-development-ready limitation.
4. Invoke `$distill-bu-knowledge` on the current engagement. The confirmed recording transcript is already interview evidence and must be reused rather than retranscribed.

## Mandatory continuation contract

After the participant confirms the interview package:

1. Set `ready_for_distillation: true` and `engagement.yaml.current_gate: distillation`.
2. Invoke `$distill-bu-knowledge` in the same Codex task. Do not end with an interview-complete status message.
3. Keep the same absolute engagement path and pass only the confirmed package and registered evidence.
4. When distillation reaches participant approval, let `$distill-bu-knowledge` continue the closed-loop handoff. Do not treat knowledge approval as the end of the workflow.
5. If a participant decision is required, ask the single smallest next question and name the next gate. A completion report alone is not a valid handoff.

## Required handoff

- Confirmed `requirements-brief.md`
- `interview-record.md` with questions, answers and corrections
- `coverage.yaml` with resolved and unresolved gaps
- `evidence-manifest.json`
- Any documents, examples, audio or video actually needed and supplied under `10_evidence/`; none of these media types is mandatory by default

These files are interview outputs and knowledge-distillation inputs. Label them as collected evidence rather than final knowledge assets.

## Stop conditions

- Stop before recording when screen or microphone permission is missing.
- Stop when the active engagement is ambiguous.
- Stop before creating a new engagement when its storage root has not been confirmed once for that engagement.
- Do not record credentials, unrelated personal data or applications outside the agreed scope.
- Do not invent missing business knowledge or silently fill it from test fixtures.
- Do not build a solution during the interview.
