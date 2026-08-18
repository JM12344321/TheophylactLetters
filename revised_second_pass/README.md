# Revised Second Pass

Created: 2026-08-18

This directory is a preservation layer for a philological second pass over the
first complete working translation in `04_letters/`. The original first-pass
files are not overwritten. Each `translation_v2.md` states whether it is merely
a baseline copy awaiting direct Greek audit or a corrected/revised item.

## Current Status

- A: 68
- B: 19
- C: 46
- D: 2

All Gautier numbers G001-G135 are accounted for and now have per-letter Gautier
source packets. Remaining C letters are not missing; they are complete or
mostly complete first-pass texts still awaiting full clause-by-clause audit.
The only D items are the mutilated/lacunose fragments G062 and G063.

This pass added Gautier CFHB volumes, extracted page text, built 135 source
packets, recovered missing Gautier letters, corrected major numbering errors,
and completed targeted or full short-letter Gautier checks for 95 letters.

Primary reports:

- `master_concordance.csv`
- `revision_log.csv`
- `exception_report.md`
- `sample_audit.md`
- `qc_report.md`

## Key Correction Already Applied

The local first-pass corpus filed the Tivanios/Tigranes Armenian Christological
fragment as G134. The second-pass corpus map corrects this:

- G134: genuine Demetrios/liturgy letter recovered from Gautier I; A.
- G135: Tivanios/Tigranes Armenian Christological fragment; reassigned from old
  local G134; B because the surviving excerpt is collated but prosopography and
  fragment status remain localized uncertainties.

Evidence is recorded in `revision_log.csv`, `master_concordance.csv`, and the
per-letter `translation_v2.md` files.
