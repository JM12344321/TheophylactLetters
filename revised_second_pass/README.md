# Revised Second Pass

Created: 2026-08-18

This directory is a preservation layer for a philological second pass over the
first complete working translation in `04_letters/`. The original first-pass
files are not overwritten. Each `translation_v2.md` states whether it is merely
a baseline copy awaiting direct Greek audit or a corrected/revised item.

## Current Status

- A: 0
- B: 0
- C: 129
- D: 6

Most complete first-pass translations remain C because they have not yet been
fully rechecked clause by clause against Greek in this layer. That is
intentional: the revision layer distinguishes existence from verification.

As of this pass, 15 letters have received targeted source-backed checks against
local Greek extractions: G004, G006, G012, G014, G045, G052, G058, G082, G096,
G103, G107, G121, G122, G126, and G135. None has been raised above C, because
Gautier collation has not been completed.

Primary reports:

- `master_concordance.csv`
- `revision_log.csv`
- `exception_report.md`
- `sample_audit.md`
- `qc_report.md`

## Key Correction Already Applied

The local first-pass corpus filed the Tivanios/Tigranes Armenian Christological
fragment as G134 and left G135 empty. The second-pass corpus map corrects this:

- G134: genuine Demetrios/liturgy letter; Greek not recovered locally; D.
- G135: Tivanios/Tigranes Armenian Christological fragment; reassigned from old
  local G134; C pending direct Gautier collation.

Evidence recorded in `revision_log.csv` cites Pinakes and Mullett.
