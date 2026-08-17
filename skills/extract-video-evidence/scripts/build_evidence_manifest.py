from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ACTION = {
    "操作", "點", "按", "輸入", "選擇", "開啟", "切換", "查詢", "搜尋", "下載", "上傳",
    "儲存", "送出", "匯出", "截圖", "比對", "登入", "貼上", "建立", "填寫",
    "click", "press", "enter", "select", "open", "switch", "search", "download", "upload",
    "save", "submit", "export", "screenshot", "compare", "login", "paste", "create", "fill",
}
DECISION = {
    "判斷", "依據", "如果", "否則", "需要確認", "規則", "門檻", "適用", "例外", "決定",
    "為什麼", "為何", "原因", "理由", "考量", "取捨", "建議", "初衷", "不一定", "比較適合",
    "循環", "迭代", "驗收", "方法論", "跑完一圈", "七成", "三成", "可行性",
    "why", "because", "if", "otherwise", "rule", "criteria", "threshold", "exception", "decide",
}
PAIN = {
    "痛點", "麻煩", "耗時", "手動", "重複", "容易錯", "漏掉", "等待", "卡住", "無法", "不一致",
    "pain", "manual", "duplicate", "error-prone", "miss", "wait", "blocked", "cannot", "mismatch",
}
OUTPUT = {
    "產出", "完成", "成功", "結果", "檔案", "報告", "清單", "草稿", "公文", "歸檔",
    "output", "complete", "success", "result", "file", "report", "list", "draft", "archive",
}

VISUAL_WORK_SURFACE_TAGS = {"document_surface", "form_surface", "spreadsheet_surface", "system_surface", "browser_surface"}


def load_timeline(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".jsonl":
        observations = [json.loads(line) for line in text.splitlines() if line.strip()]
        return {"observations": observations}
    data = json.loads(text)
    if isinstance(data, list):
        return {"observations": data}
    if not isinstance(data, dict) or not isinstance(data.get("observations"), list):
        raise ValueError("timeline must be an array or an object with observations[]")
    return data


def contains_any(text: str, terms: set[str]) -> bool:
    low = text.lower()
    return any(term.lower() in low for term in terms)


def goal_overlap(text: str, goal: str) -> bool:
    tokens = {t.lower() for t in re.findall(r"[A-Za-z0-9_]{2,}", goal)}
    for run in re.findall(r"[\u4e00-\u9fff]+", goal):
        if len(run) <= 4:
            tokens.add(run)
        else:
            for width in (2, 3, 4):
                tokens.update(run[index:index + width] for index in range(len(run) - width + 1))
    low = text.lower()
    return bool(tokens and any(t in low for t in tokens))


def score_observation(obs: dict[str, Any], goal: str) -> tuple[float, list[str], list[str]]:
    text = f"{obs.get('speech_text', '')} {obs.get('ocr_text', '')}"
    score = 0.0
    reasons: list[str] = []
    labels: list[str] = []

    if obs.get("manual_keep"):
        score = 1.0
        reasons.append("manual_keep")
        labels.append("manual")
    if contains_any(text, ACTION) or obs.get("interaction"):
        score += 0.34
        reasons.append("operation_signal")
        labels.append("operation")
    if contains_any(text, DECISION):
        score += 0.38
        reasons.append("decision_signal")
        labels.append("decision")
    if contains_any(text, PAIN):
        score += 0.42
        reasons.append("pain_or_exception_signal")
        labels.extend(["pain_point", "exception"])
    if contains_any(text, OUTPUT):
        score += 0.30
        reasons.append("output_signal")
        labels.append("output")
    if goal and goal_overlap(text, goal):
        score += 0.16
        reasons.append("goal_overlap")
    visual = obs.get("visual_change", 0)
    if isinstance(visual, (int, float)) and visual > 0:
        score += min(max(float(visual), 0.0), 1.0) * 0.22
        if visual >= 0.45:
            reasons.append("visual_state_change")
    if obs.get("privacy_blocked"):
        reasons.append("privacy_blocked")
        labels.append("privacy")

    tags = {str(tag).lower() for tag in obs.get("tags", []) or []}
    visual_context = obs.get("visual_context") if isinstance(obs.get("visual_context"), dict) else {}
    document_score = float(visual_context.get("document_score", 0.0) or 0.0)
    meeting_score = float(visual_context.get("meeting_score", 0.0) or 0.0)
    if tags & VISUAL_WORK_SURFACE_TAGS or document_score >= 0.35:
        score += 0.30
        reasons.append("visual_work_surface")
        labels.append("visual_evidence")
    if "meeting_grid" in tags and not (tags & VISUAL_WORK_SURFACE_TAGS) and document_score < 0.25:
        score -= 0.28
        reasons.append("meeting_grid_downranked")
        labels.append("meeting_only")
    if meeting_score >= 0.65 and document_score < 0.20:
        score -= 0.12
        reasons.append("low_operational_visual_context")

    for tag in obs.get("tags", []) or []:
        tag_text = str(tag).lower()
        if tag_text in {"question", "answer", "error", "output", "operation", "decision", "exception"}:
            score += 0.12
            reasons.append(f"upstream_tag:{tag_text}")
            labels.append(tag_text)

    return min(score, 1.0), sorted(set(reasons)), sorted(set(labels))


def validate_observations(observations: list[dict[str, Any]]) -> None:
    previous = -1
    for index, obs in enumerate(observations):
        start = obs.get("start_ms")
        end = obs.get("end_ms")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            raise ValueError(f"invalid time bounds at observation {index}")
        if start < previous:
            raise ValueError("observations must be sorted by start_ms")
        previous = start


def merge_candidates(
    candidates: list[dict[str, Any]],
    duration: int,
    before: int,
    after: int,
    gap: int,
) -> list[dict[str, Any]]:
    expanded = []
    for item in candidates:
        item = dict(item)
        item["start_ms"] = max(0, item["start_ms"] - before)
        item["end_ms"] = min(duration, item["end_ms"] + after) if duration else item["end_ms"] + after
        expanded.append(item)

    merged: list[dict[str, Any]] = []
    for item in expanded:
        if not merged or item["start_ms"] > merged[-1]["end_ms"] + gap:
            merged.append({
                "start_ms": item["start_ms"],
                "end_ms": item["end_ms"],
                "scores": [item["score"]],
                "reasons": set(item["reasons"]),
                "labels": set(item["labels"]),
                "evidence": [item["observation"]],
            })
            continue
        current = merged[-1]
        current["end_ms"] = max(current["end_ms"], item["end_ms"])
        current["scores"].append(item["score"])
        current["reasons"].update(item["reasons"])
        current["labels"].update(item["labels"])
        current["evidence"].append(item["observation"])
    return merged


def source_identity(path_text: str | None) -> dict[str, Any]:
    if not path_text:
        return {"path": None, "exists": False, "sha256": None, "size_bytes": None}
    path = Path(path_text)
    result = {"path": str(path), "exists": path.exists(), "sha256": None, "size_bytes": None}
    if path.is_file():
        result["size_bytes"] = path.stat().st_size
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        result["sha256"] = digest.hexdigest()
    return result


def complement_intervals(segments: list[dict[str, Any]], duration: int) -> list[dict[str, int]]:
    intervals: list[dict[str, int]] = []
    cursor = 0
    for segment in segments:
        if segment["start_ms"] > cursor:
            intervals.append({"start_ms": cursor, "end_ms": segment["start_ms"]})
        cursor = max(cursor, segment["end_ms"])
    if duration > cursor:
        intervals.append({"start_ms": cursor, "end_ms": duration})
    return intervals


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a high-recall video evidence manifest.")
    parser.add_argument("--timeline", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--goal", default="")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--min-score", type=float, default=0.34)
    parser.add_argument("--context-before-ms", type=int, default=5000)
    parser.add_argument("--context-after-ms", type=int, default=8000)
    parser.add_argument("--merge-gap-ms", type=int, default=5000)
    args = parser.parse_args()

    timeline = load_timeline(args.timeline)
    observations = timeline["observations"]
    validate_observations(observations)
    duration = int(timeline.get("duration_ms") or max((o["end_ms"] for o in observations), default=0))

    candidates = []
    for obs in observations:
        score, reasons, labels = score_observation(obs, args.goal)
        if score >= args.min_score or obs.get("manual_keep") or obs.get("privacy_blocked"):
            candidates.append({
                "start_ms": obs["start_ms"],
                "end_ms": obs["end_ms"],
                "score": score,
                "reasons": reasons,
                "labels": labels,
                "observation": obs,
            })

    merged = merge_candidates(
        candidates,
        duration,
        args.context_before_ms,
        args.context_after_ms,
        args.merge_gap_ms,
    )
    segments = []
    for index, item in enumerate(merged, start=1):
        scores = item["scores"]
        segments.append({
            "segment_id": f"SEG-{index:04d}",
            "start_ms": item["start_ms"],
            "end_ms": item["end_ms"],
            "duration_ms": item["end_ms"] - item["start_ms"],
            "confidence": round(max(scores), 3),
            "mean_signal_score": round(sum(scores) / len(scores), 3),
            "labels": sorted(item["labels"]),
            "reasons": sorted(item["reasons"]),
            "evidence": item["evidence"],
            "media": {"clip": None, "frames": [], "transcript": None},
            "review_status": "required" if max(scores) < 0.55 or "privacy" in item["labels"] else "recommended",
        })

    selected_ms = sum(segment["duration_ms"] for segment in segments)
    coverage = selected_ms / duration if duration else 0.0
    warnings = []
    if not observations:
        warnings.append("empty_timeline")
    if not segments:
        warnings.append("no_candidates_selected")
    if coverage > 0.8:
        warnings.append("low_reduction")
    if not any(obs.get("speech_text") for obs in observations):
        warnings.append("missing_timestamped_transcript")
    if not any(obs.get("ocr_text") for obs in observations):
        warnings.append("missing_ocr")
    source = source_identity(args.source)
    if not source["exists"]:
        warnings.append("source_media_unavailable")

    label_counts: dict[str, int] = {}
    for segment in segments:
        for label in segment["labels"]:
            label_counts[label] = label_counts.get(label, 0) + 1

    manifest = {
        "schema_version": "1.0",
        "selection_policy": "high_recall",
        "goal": args.goal,
        "source": source,
        "timeline": {
            "path": str(args.timeline),
            "duration_ms": duration,
            "observation_count": len(observations),
        },
        "parameters": {
            "min_score": args.min_score,
            "context_before_ms": args.context_before_ms,
            "context_after_ms": args.context_after_ms,
            "merge_gap_ms": args.merge_gap_ms,
        },
        "stats": {
            "segment_count": len(segments),
            "selected_ms": selected_ms,
            "coverage_ratio": round(coverage, 4),
            "label_counts": label_counts,
        },
        "warnings": warnings,
        "segments": segments,
        "unselected_intervals": complement_intervals(segments, duration),
    }

    args.out.mkdir(parents=True, exist_ok=True)
    for folder in ("clips", "frames", "transcript", "source"):
        (args.out / folder).mkdir(exist_ok=True)
    manifest_path = args.out / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    review = [
        "# Evidence selection review",
        "",
        f"- Segments: {len(segments)}",
        f"- Selected coverage: {coverage:.1%}",
        f"- Warnings: {', '.join(warnings) if warnings else 'none'}",
        f"- Unselected intervals: {len(manifest['unselected_intervals'])}",
        "",
        "Review every segment marked required and every unprocessed interval before downstream analysis.",
    ]
    (args.out / "review.md").write_text("\n".join(review) + "\n", encoding="utf-8")
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
