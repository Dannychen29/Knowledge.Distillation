# Audio evidence package contract

`manifest.json` records schema version, engagement, source path and SHA-256, duration when available, language, transcript provenance, segment count, speaker-label method, authorization, created time, and limitations.

`transcript.json` contains ordered segments with `segment_id`, `start_ms`, `end_ms`, `speaker`, `text`, `confidence`, `uncertainty`, and optional source metadata. Time ranges must be monotonic and non-negative.

`transcript.txt` is a readable rendering with `[HH:MM:SS.mmm–HH:MM:SS.mmm] speaker:` prefixes.

`quality-report.md` identifies inaudible spans, overlaps, uncertain speakers, language issues, transcription method, and unavailable capabilities. It must explicitly state that audio supplies no visual evidence.
