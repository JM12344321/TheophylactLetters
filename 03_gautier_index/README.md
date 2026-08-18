# Gautier Index

`gautier_index.csv` is the project spine.

The rows are already seeded as `G001` through `G135`, following the count reported for Gautier's reference edition. Do not renumber them. Add metadata only after checking Gautier directly.

## Minimum metadata before drafting a letter

- `recipient_as_in_gautier`
- `recipient_normalized`
- `date_or_range`
- `gautier_pages`
- `gautier_lines`
- `pg_columns`, if the letter is also in PG 126
- `old_numbering`, if applicable
- `primary_witnesses`

## Review rule

If any of these remain blank, the letter can be drafted, but it cannot be marked `ready_for_volume`.

