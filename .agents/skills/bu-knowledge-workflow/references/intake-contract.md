# Intake Package Contract

`output/intake-package.md` is ready for distillation only when it identifies:

- objective, intended users, business outcome, scope and out-of-scope boundary;
- trigger, ordinary workflow, expected output and completion owner;
- known inputs, systems or sources, decision points, exceptions and controls;
- a resource inventory: each available system, URL or access method, document/template, sample case, export/download capability, and known access restriction;
- available evidence and every material evidence gap;
- at least one reviewable acceptance example or the precise reason it is unavailable;
- intake mode, participant confirmation, and a list of assumptions explicitly marked unconfirmed.

For `codex-led`, begin with one focused resource-inventory question, then ask one focused question at a time and set `awaiting_bu` only for the smallest unanswered item. For `ba-assisted`, inventory BA interview outputs, available systems, templates, exports and access paths before asking for material gaps. This is intended to minimise later back-and-forth, not to require every possible resource. A PRD and an implementation spec are downstream artifacts created during distillation, not required input material.

The package fails its gate if a material output is unknown, the scope is unconfirmed, or a required decision is described without its input or owner. Do not create a solution option during intake.
