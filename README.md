# Theophylact Letters Translated

## Purpose

This folder is a working environment for translating the letters of Theophylact of Ohrid into English from Greek sources in a way a Byzantinist can audit.

The controlling index is Paul Gautier's edition of the letters. Each letter is keyed as `G001` through `G135`. That identifier should remain stable even when older numbering systems, PG columns, manuscript witnesses, or later bibliography disagree.

## What is already set up

- `03_gautier_index/gautier_index.csv`: master project index with all 135 Gautier letter slots.
- `04_letters/`: one folder per letter after running `scripts/initialize_letter_folders.ps1`.
- `05_workflow/`: editorial policy, translation SOP, and review checklist.
- `06_prompts/`: source-first AI prompts for draft translation and scholarly review.
- `02_sources/source_manifest.csv`: source acquisition and provenance tracker.
- `reference_examples/`: examples from the user's current Theophylact work.
- `scripts/`: project helpers for setup, source acquisition, checks, and volume building.

## First commands

Run these from this project folder in PowerShell:

```powershell
.\scripts\initialize_letter_folders.ps1
.\scripts\check_project.ps1
```

Optional, if internet access is available:

```powershell
.\scripts\fetch_public_sources.ps1
```

## Translation standard

The workflow assumes four layers of evidence:

1. Gautier CFHB 16/2 controls letter numbering, boundaries, page/line references, dating, recipients, and textual apparatus.
2. The Greek text controls the English. Do not translate Gautier's French into English.
3. Public-domain PG 126 and OCR are useful for access and checking, but OCR is never authoritative where sense or wording matters.
4. Secondary scholarship, especially Mullett, is used for context, network, genre, chronology, and prosopography.

## Project status vocabulary

- `needs_gautier_metadata`: index row exists, but recipient/date/pages/lines/witnesses still need to be entered from Gautier.
- `source_packet_ready`: the Greek, page/line references, PG columns, and notes are assembled.
- `drafted`: an English draft exists.
- `philology_review`: syntax, vocabulary, allusions, and textual notes are under review.
- `byzantinist_review`: a qualified reviewer could trace the translation back to evidence.
- `ready_for_volume`: translation and notes can be compiled.

## Non-negotiables

- Every translation file begins with its Gautier ID.
- Every paragraph or section should be traceable to Greek line/page references.
- Supplied English belongs in square brackets.
- Damaged, doubtful, or conjectural readings are exposed in notes.
- Do not silently harmonize biblical quotations to an English Bible.
- Do not smooth away Theophylact's rhetoric when the strangeness is doing interpretive work.
- Do not bulk-copy copyrighted Gautier text or French translation into the project. Record page/line ranges, short lemmata when needed, and your own translation.

