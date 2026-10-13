# Project Status

## Foundation
Complete:
- Master story bible and canon rules
- Full core cast and family tree
- Celeste historical timeline and death-night reconstruction
- 23-clue ledger and 10-red-herring ledger
- Evidence chains and reveal ladder
- Romance architecture
- Reader-belief and character-knowledge tracking
- Object, plot-thread and scene-dependency trackers
- Raven House location canon and diagrams
- Thirty-five canonical chapter sources
- Style / Vale starter rules
- Manuscript QA and clean-build tooling
- Export guidance

## Manuscript status

**Chapters 1–35: complete.**

**Serious developmental revision: complete on branch `serious-revision`.**

The revision covered the full manuscript rather than adding new plot. Major work included:
- restoring the intended Mercer / Claire reveal ladder;
- strengthening clue seed-to-payoff fairness and independent corroboration;
- separating Felix’s present-day sabotage from the 1931 historical guilt;
- correcting English property/title, civil-record, guardianship, police and evidence-handling logic;
- making the acoustic and service-space architecture physically plausible;
- repairing Claire’s safety logic in the passage sequence;
- deepening Talia, Evelyn and Sebastian without excusing their choices;
- rebuilding Adrian’s betrayal around informed consent and professional integrity;
- preserving the breakup through the climax and earning reconciliation through costly action plus sustained changed behaviour;
- rationalising the earlier apparent hauntings while reserving one final unclassified auditory event for Chapter 35;
- expanding underdeveloped investigation, relationship and aftermath scenes;
- removing known production-code leakage and generic gothic shortcuts;
- fixing the export pipeline so production notes cannot enter the reader manuscript.

Detailed findings: `continuity/SERIOUS_REVISION_AUDIT.md`.

## Reader build / QA

- `python tools/continuity_check.py` — structural/prose QA and Draft-only word-count reporting.
- `python tools/build_manuscript.py` — compiles only chapter headings + `## Draft` prose into `export/the-echo-of-raven-house.md`.
- Pull-request QA runs both steps before the serious revision is merged to `main`.

## Story endpoint preserved

The final historical mechanism is supported across multiple evidence classes:
- architecture and surviving fixing marks;
- photographs;
- civil records;
- carpenter’s daybook;
- coroner’s notes;
- Evelyn’s authenticated tape;
- Celeste’s final solicitor letter;
- Sebastian’s 1956 confession;
- historic title papers.

The ending remains **truth without annihilation**: the Raven family survives, the false family myth does not, Celeste regains authorship, the title question enters independent legal/preservation process, and Claire remains legally, professionally and residentially independent.

## Current production stage

**Developmental manuscript work is complete.**

Next publication-stage sequence:
1. Merge `serious-revision` into `main` after repository QA passes.
2. Generate the clean reader manuscript.
3. External beta read.
4. Copy edit.
5. Proofread.
6. DOCX / EPUB / print-layout production and final device/page proofing.

Do not add new plot unless beta reading exposes a genuine story problem.