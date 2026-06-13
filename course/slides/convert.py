#!/usr/bin/env python3
"""Convert FDE101 courseware.md into Marp slide markdown (mlopsguru theme).

Extracts each "### Slide N — Title" block and its bullet content, dropping
speaker notes (kept as Marp HTML comments so they don't render on slides).

Usage:
    python3 convert.py <courseware.md> <output.marp.md> [--title "Deck Title"]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SLIDE_RE = re.compile(r"^###\s+Slide\s+\d+\s+[—-]\s+(.*)$")
SPEAKER_RE = re.compile(r"^\*\*Speaker notes:\*\*\s*(.*)$", re.IGNORECASE)

FRONT_MATTER = """---
marp: true
theme: mlopsguru
paginate: true
---

"""


def parse_slides(text: str) -> list[dict]:
    slides: list[dict] = []
    current: dict | None = None

    for raw in text.splitlines():
        line = raw.rstrip()
        m = SLIDE_RE.match(line)
        if m:
            if current:
                slides.append(current)
            title = m.group(1).strip()
            current = {"title": title, "body": [], "notes": []}
            continue

        if current is None:
            continue

        if line.startswith("---"):
            continue

        sm = SPEAKER_RE.match(line)
        if sm:
            current["notes"].append(sm.group(1).strip())
            continue

        current["body"].append(line)

    if current:
        slides.append(current)
    return slides


def render(slides: list[dict], deck_title: str) -> str:
    out = [FRONT_MATTER]

    out.append("<!-- _class: lead -->\n")
    out.append(f"# {deck_title}\n\n## FDE101 · mlopsguru\n\n---\n")

    for s in slides:
        title = s["title"]
        # The first source block is literally titled "Title"; relabel for a clean heading.
        if title.lower() == "title":
            title = "Welcome"

        body = "\n".join(s["body"]).strip()
        block = f"# {title}\n\n{body}\n"

        notes = " ".join(s["notes"]).strip()
        if notes:
            block += f"\n<!-- {notes} -->\n"

        out.append(block)
        out.append("\n---\n")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("output")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    src = Path(args.source)
    text = src.read_text(encoding="utf-8")

    deck_title = args.title
    if not deck_title:
        # Derive from the first H1 of the courseware, else the folder name.
        h1 = re.search(r"^#\s+(.*)$", text, re.MULTILINE)
        deck_title = h1.group(1).strip() if h1 else src.parent.name.upper()

    slides = parse_slides(text)
    if not slides:
        raise SystemExit(f"No '### Slide N — Title' blocks found in {src}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(slides, deck_title), encoding="utf-8")
    print(f"Wrote {len(slides)} slides → {out}")


if __name__ == "__main__":
    main()
