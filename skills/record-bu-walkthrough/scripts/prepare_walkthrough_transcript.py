#!/usr/bin/env python3
"""Create and validate a fast post-recording transcript for interview gap review."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> None:
    completed = subprocess.run(command, text=True)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engagement", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--evidence-id", required=True)
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="auto")
    parser.add_argument("--beam-size", type=int, default=1)
    parser.add_argument("--initial-prompt", default="")
    parser.add_argument("--allow-model-download", action="store_true")
    args = parser.parse_args()

    engagement = args.engagement.expanduser().resolve()
    source = args.source.expanduser().resolve()
    if not (engagement / "engagement.yaml").is_file():
        parser.error("engagement.yaml not found")
    if not source.is_file():
        parser.error("recording source not found")

    skills_root = Path(__file__).resolve().parents[2]
    transcriber = skills_root / "prepare-audio-evidence" / "scripts" / "transcribe_media.py"
    validator = skills_root / "prepare-audio-evidence" / "scripts" / "validate_audio_package.py"
    package = engagement / "10_evidence" / "transcripts" / args.evidence_id

    command = [
        sys.executable,
        str(transcriber),
        "--source",
        str(source),
        "--out-dir",
        str(package),
        "--engagement-id",
        engagement.name,
        "--evidence-id",
        args.evidence_id,
        "--model",
        args.model,
        "--language",
        args.language,
        "--beam-size",
        str(args.beam_size),
    ]
    if args.initial_prompt:
        command.extend(["--initial-prompt", args.initial_prompt])
    if args.allow_model_download:
        command.append("--allow-model-download")
    run(command)
    run([sys.executable, str(validator), str(package)])

    result = {
        "status": "transcript_ready_for_interview_review",
        "evidence_id": args.evidence_id,
        "source": str(source),
        "transcript_package": str(package),
        "transcript_json": str(package / "transcript.json"),
        "transcript_text": str(package / "transcript.txt"),
        "next_action": "return_to_conduct-bu-interview_for_gap_review",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
