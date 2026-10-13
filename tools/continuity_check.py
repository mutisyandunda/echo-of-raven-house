#!/usr/bin/env python3
"""Structural and prose QA for The Echo of Raven House manuscript."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"

BANNED_CLICHES = [
    r"a chill ran down (?:her|his|their) spine",
    r"(?:her|his|their) blood ran cold",
    r"heart skipped a beat",
    r"breath (?:she|he|they) didn['’]t know (?:she|he|they) (?:was|were) holding",
    r"deafening silence",
    r"if these walls could talk",
    r"secrets buried in the walls",
    r"time stood still",
    r"like a moth to a flame",
    r"she shivered, though not from the cold",
]

# Production notation that should never leak into reader-facing prose.
PRODUCTION_LEAKS = [
    (r"\bC(?:[1-9]|1\d|2[0-3])\b", "clue code"),
    (r"\bR(?:10|[1-9])\b", "red-herring code"),
    (r"\bChapter\s+(?:\d+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty|Twenty-One|Twenty-Two|Twenty-Three|Twenty-Four|Twenty-Five|Twenty-Six|Twenty-Seven|Twenty-Eight|Twenty-Nine|Thirty|Thirty-One|Thirty-Two|Thirty-Three|Thirty-Four|Thirty-Five)\b", "authorial chapter reference"),
]

TITLE_RE = re.compile(r"^#\s+Chapter\s+(\d+)\s*:\s*(.+?)\s*$", re.MULTILINE)
YAML_TITLE_RE = re.compile(r'^title:\s*["\']?(.*?)["\']?\s*$', re.MULTILINE)


def chapter_files() -> list[Path]:
    return sorted(MANUSCRIPT.glob("[0-9][0-9]-*.md"))


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def main() -> int:
    files = chapter_files()
    failures: list[str] = []
    warnings: list[str] = []

    if len(files) != 35:
        failures.append(f"Expected 35 chapter files; found {len(files)}")

    seen_numbers: dict[int, str] = {}
    seen_titles: dict[str, str] = {}
    total_words = 0
    counts: list[tuple[int, str, int]] = []

    for expected, path in enumerate(files, start=1):
        text = path.read_text(encoding="utf-8")
        filename_number = int(path.name[:2])

        if filename_number in seen_numbers:
            failures.append(
                f"Duplicate chapter number {filename_number}: "
                f"{seen_numbers[filename_number]} and {path.name}"
            )
        seen_numbers[filename_number] = path.name

        heading = TITLE_RE.search(text)
        if not heading:
            failures.append(f"{path.name}: missing '# Chapter N: Title' heading")
            heading_number = filename_number
            heading_title = path.stem
        else:
            heading_number = int(heading.group(1))
            heading_title = heading.group(2).strip()

        if filename_number != expected or heading_number != expected:
            failures.append(
                f"{path.name}: sequence mismatch "
                f"(filename={filename_number}, heading={heading_number}, expected={expected})"
            )

        yaml_title = YAML_TITLE_RE.search(text)
        title = yaml_title.group(1).strip() if yaml_title else heading_title
        if title in seen_titles:
            failures.append(f"Duplicate title '{title}': {seen_titles[title]} and {path.name}")
        seen_titles[title] = path.name

        if "## Draft" not in text:
            failures.append(f"{path.name}: missing '## Draft' section")
            continue

        draft = text.split("## Draft", 1)[1].strip()
        if not draft:
            failures.append(f"{path.name}: empty Draft section")
            continue

        count = words(draft)
        total_words += count
        counts.append((filename_number, title, count))
        if count < 1500:
            warnings.append(f"{path.name}: short chapter ({count:,} Draft words)")

        for pattern in BANNED_CLICHES:
            match = re.search(pattern, draft, re.IGNORECASE)
            if match:
                failures.append(
                    f"{path.name}:{line_number(text, text.index('## Draft') + match.start())} "
                    f"banned cliché /{pattern}/"
                )

        for pattern, label in PRODUCTION_LEAKS:
            match = re.search(pattern, draft)
            if match:
                failures.append(
                    f"{path.name}: {label} leaked into Draft: {match.group(0)!r}"
                )

    print("MANUSCRIPT QA")
    print(f"Chapters: {len(files)}")
    print(f"Draft prose words: {total_words:,}")
    if counts:
        shortest = min(counts, key=lambda item: item[2])
        longest = max(counts, key=lambda item: item[2])
        print(f"Shortest: Ch {shortest[0]:02d} — {shortest[1]} ({shortest[2]:,})")
        print(f"Longest:  Ch {longest[0]:02d} — {longest[1]} ({longest[2]:,})")

    if warnings:
        print("\nWARNINGS")
        for warning in warnings:
            print("-", warning)

    if failures:
        print("\nFAILURES")
        for failure in failures:
            print("-", failure)
        return 1

    print("\nPASS: structural, production-leak and banned-cliché checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
