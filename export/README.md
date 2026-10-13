# Export Pipeline

The canonical working manuscript remains the numbered Markdown chapter files in `manuscript/`.

Those source files intentionally contain YAML metadata, chapter-purpose notes, clue tracking and other production material. **Do not pass `manuscript/*.md` directly to Pandoc.** That would leak production notes into the book.

## 1. Run manuscript QA

```bash
python tools/continuity_check.py
```

This checks chapter structure, sequence, duplicate titles, banned clichés and production notation that should never appear in reader-facing prose. It also prints Draft-only chapter and total word counts.

## 2. Build the clean reader manuscript

```bash
python tools/build_manuscript.py
```

This creates:

```text
export/the-echo-of-raven-house.md
```

Only each chapter title and the prose under `## Draft` are included. YAML, clue codes, chapter-purpose notes and revision scaffolding are excluded.

You can choose another output path:

```bash
python tools/build_manuscript.py --output export/build/manuscript.md
```

## 3. Optional DOCX / EPUB export with Pandoc

If Pandoc is installed:

```bash
mkdir -p export/build
pandoc export/the-echo-of-raven-house.md \
  --metadata-file=export/metadata.yml \
  -o export/build/the-echo-of-raven-house.docx
```

```bash
pandoc export/the-echo-of-raven-house.md \
  --metadata-file=export/metadata.yml \
  -o export/build/the-echo-of-raven-house.epub
```

## 4. Publication sequence

1. Run `tools/continuity_check.py`.
2. Build the clean manuscript with `tools/build_manuscript.py`.
3. Beta-read the clean manuscript, not the production chapter files.
4. Apply copy-edit corrections in the canonical chapter sources.
5. Re-run QA and rebuild.
6. Export DOCX / EPUB as needed.
7. Inspect EPUB in Calibre or another standards-aware reader.
8. Produce KDP or print-layout assets only after copy edit and proofing.

The build script is intentionally deterministic: the numbered chapter files remain the single source of truth and the reader manuscript can always be regenerated from them.