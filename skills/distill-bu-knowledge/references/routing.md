# Evidence routing

| Input | Worker | Result used by distillation |
|---|---|---|
| Interview record, text, CSV, JSON | Direct analysis | Statements, structures, examples and gaps |
| PDF, Word, spreadsheet, image | Appropriate document tool | Page/sheet/cell/section-linked evidence |
| Audio file | `$prepare-audio-evidence` | Timecoded speaker-aware transcript and uncertainty |
| Screen recording or video | `$extract-video-evidence` -> `$analyze-video-evidence` | Selected timecoded actions, screens, rationale and gaps |

Route by actual content when extension and content disagree. Preserve originals and create derived files outside the source file's location.

For mixed sources, never collapse provenance. Agreement raises corroboration; disagreement becomes an explicit contradiction.
