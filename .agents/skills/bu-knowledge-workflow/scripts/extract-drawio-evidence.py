"""Extract diagrams.net (.drawio) text and links without lossy console decoding."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET


def plain_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(value))).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # .drawio diagrams.net files are UTF-8 XML. Strict decoding fails closed
    # rather than silently producing mojibake.
    root = ET.fromstring(args.input.read_bytes().decode("utf-8", errors="strict"))
    pages = []
    for diagram in root.findall("diagram"):
        cells = []
        for cell in diagram.findall(".//mxCell"):
            value = cell.get("value", "")
            text = plain_text(value) if value else ""
            if text or cell.get("edge") == "1":
                cells.append(
                    {
                        "id": cell.get("id"),
                        "text": text,
                        "source": cell.get("source"),
                        "target": cell.get("target"),
                        "is_edge": cell.get("edge") == "1",
                    }
                )
        pages.append({"name": diagram.get("name"), "cells": cells})

    result = {"format": "drawio-evidence-v1", "source": str(args.input), "pages": pages}
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
