# Targeted Second-Pass Sample Audit

Created: 2026-08-18

This is not a final corpus-wide clause audit. It records the 15 source-backed checks completed in this revision layer and keeps their remaining uncertainty visible.

| G | Source | Result | Confidence |
|---|---|---|---|
| G004 | PG093 | meteorological lexical correction; status `targeted_second_pass_revised_ocr_checked_needs_gautier_collation` | C |
| G006 | PG006 | no material semantic correction; status `targeted_second_pass_checked_no_material_change_needs_gautier_collation` | C |
| G012 | PG100 | localized OCR uncertainty; status `targeted_second_pass_checked_localized_ocr_uncertainty` | C |
| G014 | PG035 | recipient metadata revised; no English correction; status `targeted_second_pass_checked_metadata_revised_needs_gautier_collation` | C |
| G045 | PG003 | truncated source preserved; status `targeted_second_pass_checked_truncated_needs_gautier_collation` | C |
| G052 | PG012 | localized OCR uncertainty; status `targeted_second_pass_checked_localized_ocr_uncertainty` | C |
| G058 | PG019 | truncated closing preserved; status `targeted_second_pass_checked_truncated_needs_gautier_collation` | C |
| G082 | PG047 | juridical terms flagged; status `targeted_second_pass_checked_juridical_terms_need_gautier_collation` | C |
| G096 | PG060 | fiscal terms flagged; status `targeted_second_pass_checked_fiscal_terms_need_gautier_collation` | C |
| G103 | PG066 | merged packet unit checked; status `targeted_second_pass_checked_no_material_change_needs_gautier_collation` | C |
| G107 | PG069 | no material semantic correction; status `targeted_second_pass_checked_no_material_change_needs_gautier_collation` | C |
| G121 | PG083 | short bereavement letter checked; status `targeted_second_pass_checked_localized_ocr_uncertainty` | C |
| G122 | PG085 | short bereavement letter checked; status `targeted_second_pass_checked_no_material_change_needs_gautier_collation` | C |
| G126 | PG088 | boundary with G127 confirmed; status `targeted_second_pass_checked_boundary_needs_gautier_collation` | C |
| G135 | PG022 | indexing and Christological phrasing corrected; status `targeted_second_pass_revised_ocr_checked_needs_gautier_collation` | C |

## Systematic Findings

- The first-pass translation is often closer to the Greek than expected in checked samples.
- The most common unresolved risk is OCR corruption around proper names, fiscal terminology, and page breaks.
- Clear hallucination was not found in the checked sample; the larger risk is overconfident smoothing of damaged or compressed Greek.
- G127 remains a high-priority long-letter audit because it shares PG088 with G126 and contains dense comic/classical material.
