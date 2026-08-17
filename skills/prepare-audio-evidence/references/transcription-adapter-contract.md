# Transcription adapter contract

An adapter may use a local or approved external speech-to-text engine. It must disclose engine/model, language settings, diarization support, timestamps, confidence availability, data-transfer boundary, and failures.

Normalize adapter output to the audio evidence contract. Do not fabricate confidence values or speaker identities. If diarization is unavailable, use `speaker_unknown`; if timestamps are approximate, record that limitation.
