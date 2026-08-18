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
$expected = 1..135 | ForEach-Object { 'G{0:D3}' -f $_ }
$ids = @($rows | ForEach-Object { $_.gautier_id })
$missing = @($expected | Where-Object { $_ -notin $ids })
$extra = @($ids | Where-Object { $_ -notin $expected })
$dupes = @($ids | Group-Object | Where-Object { $_.Count -gt 1 })

Write-Host ("Index rows: {0}" -f $rows.Count)
Write-Host ("Missing Gautier IDs: {0}" -f $(if ($missing.Count) { $missing -join ', ' } else { 'none' }))
Write-Host ("Unexpected Gautier IDs: {0}" -f $(if ($extra.Count) { $extra -join ', ' } else { 'none' }))
Write-Host ("Duplicate Gautier IDs: {0}" -f $(if ($dupes.Count) { ($dupes | ForEach-Object { $_.Name }) -join ', ' } else { 'none' }))

$requiredFiles = @('source.md', 'greek.txt', 'translation.md', 'notes.md', 'review.md')
$folderProblems = New-Object System.Collections.Generic.List[string]
foreach ($gid in $expected) {
    $dir = Join-Path $Root ("04_letters\{0}" -f $gid)
    if (!(Test-Path -LiteralPath $dir)) {
        $folderProblems.Add("$gid missing folder")
        continue
    }
    foreach ($file in $requiredFiles) {
        $path = Join-Path $dir $file
        if (!(Test-Path -LiteralPath $path)) {
            $folderProblems.Add("$gid missing $file")
        }
    }
}

if ($folderProblems.Count -eq 0) {
    Write-Host "Letter folder audit: pass"
} else {
    Write-Host "Letter folder audit: problems"
    $folderProblems | ForEach-Object { Write-Host " - $_" }
}

$ready = @($rows | Where-Object { $_.status -eq 'ready_for_volume' })
$metadataOpen = @($rows | Where-Object { $_.status -eq 'needs_gautier_metadata' })
Write-Host ("Ready for volume: {0}" -f $ready.Count)
Write-Host ("Needs Gautier metadata: {0}" -f $metadataOpen.Count)
