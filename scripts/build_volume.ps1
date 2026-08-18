[CmdletBinding()]
param(
    [string]$Root,
    [switch]$OnlyReady
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
$outDir = Join-Path $Root '07_exports'
$outPath = Join-Path $outDir 'theophylact_letters_volume.md'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$rows = Import-Csv -LiteralPath $indexPath | Sort-Object sort_key
$selected = if ($OnlyReady) {
    $rows | Where-Object { $_.status -eq 'ready_for_volume' }
} else {
    $rows
}

$parts = New-Object System.Collections.Generic.List[string]
$parts.Add('# Theophylact of Ohrid: Letters')
$parts.Add('')
$parts.Add('Working English translation arranged by Gautier number.')
$parts.Add('')
$parts.Add('Editorial note: this compiled file is generated from per-letter Markdown files. Check each letter folder for source packets, Greek text, notes, and review status.')
$parts.Add('')

foreach ($row in $selected) {
    $translationPath = Join-Path $Root $row.translation_path
    $parts.Add('')
    $parts.Add(('---'))
    $parts.Add('')
    if (Test-Path -LiteralPath $translationPath) {
        $parts.Add((Get-Content -LiteralPath $translationPath -Raw))
    } else {
        $parts.Add(("# {0} Translation" -f $row.gautier_id))
        $parts.Add('')
        $parts.Add('Missing translation file.')
    }
}

$parts -join "`r`n" | Set-Content -LiteralPath $outPath -Encoding UTF8
Write-Host "Built volume:"
Write-Host $outPath
