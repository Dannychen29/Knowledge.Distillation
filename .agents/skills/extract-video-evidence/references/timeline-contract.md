# Normalized timeline contract

Use UTF-8 JSON containing either an array of observations or an object with an observations array.

## Observation fields

| Field | Required | Meaning |
|---|---:|---|
| start_ms | Yes | Inclusive start time in milliseconds |
| end_ms | Yes | Exclusive end time in milliseconds |
| speech_text | No | Timestamped ASR or supplied transcript text |
| ocr_text | No | Visible UI text detected in this interval |
| visual_change | No | Normalized 0–1 state-change signal |
| interaction | No | true when mouse, keyboard, touch, or UI action occurs |
| visual_context | No | Low-cost frame classification signals, such as document_score, meeting_score, white_ratio, dark_ratio and edge_density |
| manual_keep | No | Force retention after a human or upstream rule marks it |
| privacy_blocked | No | Evidence exists but cannot be exposed without redaction |
| source_refs | No | Frame, audio, transcript, or event references |
| tags | No | Upstream labels such as question, answer, error, output |

## Example

    {
      "duration_ms": 2400000,
      "observations": [
        {
          "start_ms": 612000,
          "end_ms": 626000,
          "speech_text": "我現在用案件識別碼到業務系統查詢。",
          "ocr_text": "Record Search",
          "visual_change": 0.72,
          "interaction": true,
          "visual_context": {"document_score": 0.82, "meeting_score": 0.04},
          "source_refs": ["frames/frame_0612.jpg"],
          "tags": ["operation"]
        }
      ]
    }

## Adapter requirements

An engineer API or local extractor may produce richer data, but normalize it to this contract before selection. Preserve unknown vendor fields outside the core record if needed; do not replace the required time bounds.
