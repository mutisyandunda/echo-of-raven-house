# Export Pipeline

Canonical manuscript source remains Markdown.

Recommended publishing pipeline:

1. Compile chapter files in numeric order.
2. Run continuity checks.
3. Run prose linting (Vale / proselint / LanguageTool).
4. Compile with Pandoc to DOCX and EPUB.
5. Inspect EPUB in Calibre.
6. Produce KDP-ready assets only after copy edit.

Example:

```bash
pandoc manuscript/*.md --metadata-file=export/metadata.yml   -o export/build/the-echo-of-raven-house.docx
```

```bash
pandoc manuscript/*.md --metadata-file=export/metadata.yml   -o export/build/the-echo-of-raven-house.epub
```
