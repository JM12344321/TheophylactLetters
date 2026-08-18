# Translation SOP

## Stage 0: Identify

1. Open `03_gautier_index/gautier_index.csv`.
2. Select the next `G###` row.
3. Enter recipient, date, Gautier page/line range, PG columns if available, old numbering, and witnesses from Gautier.
4. Run `scripts/initialize_letter_folders.ps1` to refresh the letter scaffold.

## Stage 1: Assemble source packet

For each letter folder:

```text
04_letters/G###/
  source.md
  greek.txt
  translation.md
  notes.md
  review.md
```

`source.md` must identify:

- Gautier number;
- recipient;
- date;
- Gautier pages and lines;
- PG columns or reason PG is absent;
- witnesses;
- source status;
- unresolved textual problems.

`greek.txt` should contain a working Greek transcription with line references. If the Greek comes from OCR, mark it as OCR. If it is corrected against page images or Gautier, mark the correction.

## Stage 2: First translation

Draft from Greek only. Use `06_prompts/translation_prompt.md` if using an AI assistant.

Output in `translation.md`:

- short metadata block;
- English translation;
- translator's notes;
- unresolved questions.

## Stage 3: Philological review

Check:

- syntax and particles;
- voice, tense, aspect, and agency;
- names and titles;
- biblical and classical allusions;
- technical vocabulary;
- rhetorical structure;
- damaged or suspicious readings.

Enter results in `review.md` and `notes.md`.

## Stage 4: Byzantine context review

Check against Mullett and other secondary literature:

- correspondent identification;
- network position;
- chronology;
- historical events;
- ecclesiastical geography;
- genre and letter type.

This stage may change the notes, but it should not override the Greek.

## Stage 5: Mark ready

Update the index row:

- `status`: `ready_for_volume`
- `review_status`: `reviewed`

Only do this when `review.md` has no unresolved blocking items.

## Stage 6: Build volume

Run:

```powershell
.\scripts\build_volume.ps1
```

The draft volume is written to `07_exports/theophylact_letters_volume.md`.

