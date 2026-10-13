#!/usr/bin/env python3
"""Compile the Raven House chapter files into a clean reader manuscript.

Only the chapter heading and prose under each chapter's ``## Draft`` heading are
included. YAML metadata, production notes, clue labels, revision notes and other
working material remain in the source files but never enter the compiled book.

Usage:
    python tools/build_manuscript.py
    python tools/build_manuscript.py --output export/the-echo-of-raven-house.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "manuscript"
DEFAULT_OUTPUT = ROOT / "export" / "the-echo-of-raven-house.md"
CHAPTER_RE = re.compile(r"^(\d{2})-.*\.md$")
TITLE_RE = re.compile(r"^#\s+Chapter\s+(\d+)\s*:\s*(.+?)\s*$", re.MULTILINE)
DRAFT_MARKER = "## Draft"


def chapter_files() -> list[Path]:
    files: list[tuple[int, Path]] = []
    for path in MANUSCRIPT_DIR.glob("[0-9][0-9]-*.md"):
        match = CHAPTER_RE.match(path.name)
        if match:
            files.append((int(match.group(1)), path))
    return [path for _, path in sorted(files)]


def extract_chapter(path: Path) -> tuple[int, str, str]:
    text = path.read_text(encoding="utf-8")
    title_match = TITLE_RE.search(text)
    if not title_match:
        raise ValueError(f"Missing '# Chapter N: Title' heading in {path}")
    if DRAFT_MARKER not in text:
        raise ValueError(f"Missing '{DRAFT_MARKER}' section in {path}")

    heading_number = int(title_match.group(1))
    title = title_match.group(2).strip()
    draft = text.split(DRAFT_MARKER, 1)[1].strip()
    if not draft:
        raise ValueError(f"Empty draft section in {path}")
    return heading_number, title, draft


def count_words(text: str) -> int:
    # Treat curly apostrophes and hyphenated compounds as part of words.
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def build(output: Path) -> tuple[int, int]:
    files = chapter_files()
    if len(files) != 35:
        raise ValueError(f"Expected 35 chapter files, found {len(files)}")

    parts = ["# The Echo of Raven House", ""]
    total_words = 0

    for expected_number, path in enumerate(files, start=1):
        number, title, draft = extract_chapter(path)
        filename_number = int(path.name[:2])
        if number != expected_number or filename_number != expected_number:
            raise ValueError(
                f"Chapter sequence mismatch at {path}: "
                f"filename={filename_number}, heading={number}, expected={expected_number}"
            )

        total_words += count_words(draft)
        parts.extend([f"# Chapter {number}: {title}", "", draft, ""])

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return len(files), total_words


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output Markdown path (default: {DEFAULT_OUTPUT.relative_to(ROOT)})",
    )
    args = parser.parse_args()

    output = args.output
    if not output.is_absolute():
        output = ROOT / output

    chapters, words = build(output)
    print(f"Built {chapters} chapters → {output.relative_to(ROOT)}")
    print(f"Draft prose word count: {words:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
