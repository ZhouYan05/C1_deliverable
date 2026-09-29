$ErrorActionPreference = "Continue"
$root = "C:\Users\35586\Desktop\Challenge\cs146s-vibe-coding-zh"
$log  = Join-Path $root "pipeline\run_remaining.log"
function Log([string]$m){ $m | Out-File -LiteralPath $log -Append -Encoding utf8 }

Log ("=== START " + (Get-Date -Format s) + " ===")

Log "--- phase 1: markdown  source\ -> translated\ ---"
& powershell -ExecutionPolicy Bypass -File (Join-Path $root "pipeline\translate_cli.ps1") 2>&1 | Out-File -LiteralPath $log -Append -Encoding utf8
Log ("phase 1 exit=" + $LASTEXITCODE)

Log "--- phase 2: pdf  pdf_source\ -> pdf_translated\ ---"
& powershell -ExecutionPolicy Bypass -File (Join-Path $root "pipeline\translate_pdf.ps1") 2>&1 | Out-File -LiteralPath $log -Append -Encoding utf8
Log ("phase 2 exit=" + $LASTEXITCODE)

Log ("=== END " + (Get-Date -Format s) + " ===")
