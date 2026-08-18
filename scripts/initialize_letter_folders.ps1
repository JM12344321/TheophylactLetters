[CmdletBinding()]
param(
    [string]$Root
)

if ([string]::IsNullOrWhiteSpace($Root)) {
    $scriptDir = if ($PSScriptRoot) {
        $PSScriptRoot
    } elseif ($PSCommandPath) {
        Split-Path -Parent $PSCommandPath
    } else {
        (Get-Location).Path
    }
    $Root = Split-Path -Parent $scriptDir
}

$indexPath = Join-Path $Root '03_gautier_index\gautier_index.csv'
if (!(Test-Path -LiteralPath $indexPath)) {
    throw "Missing index: $indexPath"
}

$rows = Import-Csv -LiteralPath $indexPath
foreach ($row in $rows) {
    $gid = $row.gautier_id
    if ([string]::IsNullOrWhiteSpace($gid)) { continue }

    $letterDir = Join-Path $Root ("04_letters\{0}" -f $gid)
    New-Item -ItemType Directory -Force -Path $letterDir | Out-Null

    $sourcePath = Join-Path $letterDir 'source.md'
    if (!(Test-Path -LiteralPath $sourcePath)) {
        @"
# $gid Source Packet

## Metadata

- Gautier ID: $gid
- Gautier number: $($row.gautier_number)
- Recipient as in Gautier:
- Recipient normalized:
- Date or range:
- Gautier pages:
- Gautier lines:
- PG columns:
- Old numbering:
- Primary witnesses:
- Source status: needs_gautier_metadata

## Source Notes

- Enter Gautier metadata before drafting.
- Add PG/OCR extraction notes here.
- Record any damage, conjecture, or disputed reading.

"@ | Set-Content -LiteralPath $sourcePath -Encoding UTF8
    }

    $greekPath = Join-Path $letterDir 'greek.txt'
    if (!(Test-Path -LiteralPath $greekPath)) {
        @"
$gid Greek Working Text

Paste or transcribe the Greek here with line references.

Source status:
- [ ] OCR only
- [ ] Checked against PG image
- [ ] Checked against Gautier
- [ ] Textual problems recorded in notes.md

"@ | Set-Content -LiteralPath $greekPath -Encoding UTF8
    }

    $translationPath = Join-Path $letterDir 'translation.md'
    if (!(Test-Path -LiteralPath $translationPath)) {
        @"
# $gid Translation

Status: not_started

## Metadata

- Gautier ID: $gid
- Recipient:
- Date:
- Source:

## English Translation

[Draft translation goes here.]

## Translator's Notes

[Add notes or link to notes.md.]

## Unresolved Questions

- [ ] None yet.

"@ | Set-Content -LiteralPath $translationPath -Encoding UTF8
    }

    $notesPath = Join-Path $letterDir 'notes.md'
    if (!(Test-Path -LiteralPath $notesPath)) {
        @"
# $gid Notes

## Textual Notes

## Translation Notes

## Biblical Allusions

## Classical Allusions

## Prosopography

## Historical Context

## Bibliography

"@ | Set-Content -LiteralPath $notesPath -Encoding UTF8
    }

    $reviewPath = Join-Path $letterDir 'review.md'
    if (!(Test-Path -LiteralPath $reviewPath)) {
        @"
# $gid Review

## Source Gate

- [ ] Gautier metadata entered.
- [ ] Greek text assembled.
- [ ] OCR checked where needed.
- [ ] Apparatus issues logged.

## Translation Gate

- [ ] Draft translated from Greek.
- [ ] Syntax checked.
- [ ] Names and offices checked.
- [ ] Biblical/classical allusions checked.
- [ ] Supplied words bracketed.
- [ ] Uncertainty noted.

## Final Gate

- [ ] Notes complete.
- [ ] Blocking questions resolved.
- [ ] Index row updated.

"@ | Set-Content -LiteralPath $reviewPath -Encoding UTF8
    }
}

Write-Host ("Initialized {0} Gautier letter folders under {1}" -f $rows.Count, (Join-Path $Root '04_letters'))
