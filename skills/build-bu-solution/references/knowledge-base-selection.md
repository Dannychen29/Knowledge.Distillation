# Knowledge-base selection

Build a knowledge base only when approved knowledge must be searched, browsed or reused beyond a single bounded Solution task.

## Selection gate

Choose a knowledge base when at least one material need exists:

- many users or solutions require the same approved knowledge;
- the corpus is too large or variable for reliable direct-context use;
- users need search, filtering, navigation or question answering;
- knowledge has distinct access, freshness, review, version or retirement rules;
- retrieval quality and citations require repeatable evaluation.

Prefer direct use of `BRD.md`, `knowledge.json` or approved files when none of these needs applies.

## Design choices

Choose the smallest sufficient retrieval design:

- Markdown/HTML collection for small, stable, browsable knowledge;
- structured JSON/database lookup for exact fields, rules or filters;
- full-text search for keyword-driven discovery;
- retrieval-augmented generation only when semantic question answering is required and can be evaluated;
- API or managed platform when live access control, shared updates or integration is required.

Do not select embeddings or RAG by default.

## Required controls

Define:

- canonical approved corpus and stable knowledge IDs;
- chunking/index mapping without losing claim IDs or access labels;
- authorization before retrieval;
- citation to approved source and version;
- no-answer behavior for unsupported questions;
- conflict and stale-content handling;
- update, reapproval, reindex and retirement workflow;
- representative retrieval and answer evaluation cases;
- operational owner, logs and human escalation.
