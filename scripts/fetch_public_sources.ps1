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

$pgDir = Join-Path $Root '02_sources\pg126'
New-Item -ItemType Directory -Force -Path $pgDir | Out-Null

$ocrUrl = 'https://raw.githubusercontent.com/calfa-co/Patrologia-Graeca/main/PG126/PG126_text.txt'
$ocrOut = Join-Path $pgDir 'PG126_text.txt'
if (!(Test-Path -LiteralPath $ocrOut)) {
    Write-Host "Downloading Calfa-GREgORI PG126 OCR..."
    Invoke-WebRequest -Uri $ocrUrl -OutFile $ocrOut
}

$pdfUrl = 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Patrologia_Graeca_Vol._126.pdf'
$pdfOut = Join-Path $pgDir 'Patrologia_Graeca_Vol_126.pdf'
if (!(Test-Path -LiteralPath $pdfOut)) {
    Write-Host "Downloading PG 126 public-domain PDF..."
    Invoke-WebRequest -Uri $pdfUrl -OutFile $pdfOut
}

Write-Host "Public source fetch complete."
Write-Host $pgDir
