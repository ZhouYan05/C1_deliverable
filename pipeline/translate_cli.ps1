# translate_cli.ps1 -- machine translation pipeline (local Claude CLI backend)
# =============================================================================
# Same shape as translate.py: injects the glossary, translates each article whole,
# preserves Markdown. Difference: the backend is the local `claude -p` print mode
# instead of an OpenAI-compatible HTTP endpoint, so it runs on machines that have
# no LLM_API_KEY but do have the Claude Code CLI installed.
#
# Usage : powershell -ExecutionPolicy Bypass -File pipeline\translate_cli.ps1
# Resume: files already present in translated\ are skipped; delete one to redo it.
# Reuse : change $src / $out for another course.
# Smoke : -Limit N processes only the first N files.
# =============================================================================
param([int]$Limit = 0)
chcp 65001 | Out-Null
$ErrorActionPreference = "Continue"

$PipelineDir = $PSScriptRoot
$src = Join-Path $PipelineDir "..\source"
$out = Join-Path $PipelineDir "..\translated"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$log = Join-Path $out "_translate_log.txt"
$nl = [string][char]10
$utf8 = New-Object System.Text.UTF8Encoding($false)

# Build the glossary block (the C1 "glossary injection" requirement)
$glossRows = Import-Csv (Join-Path $PipelineDir "glossary.csv") |
    Where-Object { $_.en -and $_.zh } |
    ForEach-Object { "- " + $_.en + " -> " + $_.zh }
$gloss = $glossRows -join $nl

$rules = @"
翻译要求：
1) 把「待翻译正文」中的英文 Markdown 忠实翻译成简体中文，不遗漏、不增删；
2) 代码块、命令、URL、专有名词、文件名保持原样；
3) 严格使用「术语对照表」的译法；未列出的术语首次出现用「中文（English）」标注；
4) 保留 Markdown 结构（标题、列表、表格、引用、代码块）；
5) 只输出「待翻译正文」的译文，不要输出本要求或术语表，不要任何解释与前后缀。
"@
$instr = "把标准输入中「待翻译正文」部分的英文翻译成简体中文，严格遵守其中的翻译要求与术语表，只输出译文。"

Push-Location $env:TEMP

$files = Get-ChildItem -Path $src -Filter *.md |
    Where-Object { $_.Name -notlike "_*" } |
    Sort-Object Name
if ($Limit -gt 0) { $files = $files | Select-Object -First $Limit }

("[" + (Get-Date -Format s) + "] start, files=" + $files.Count) | Add-Content -Path $log -Encoding utf8

foreach ($f in $files) {
    $target = Join-Path $out $f.Name
    if (Test-Path $target) {
        ("[skip] " + $f.Name + " already present") | Add-Content -Path $log -Encoding utf8
        continue
    }
    $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $text = [regex]::Replace($raw, '^<!-- source: .*? -->\r?\n', '')
    $payload = "# 翻译要求" + $nl + $rules + $nl + "# 术语对照表" + $nl + $gloss + $nl + "# 待翻译正文" + $nl + $text

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $res = $null
    for ($attempt = 1; $attempt -le 2; $attempt++) {
        try { $res = $payload | & claude -p $instr --output-format text --no-session-persistence 2>$null } catch { $res = $null }
        $joined = ($res -join $nl)
        if ($joined -and $joined.Trim().Length -gt 0) { break }
        Start-Sleep -Seconds 3
    }
    $sw.Stop()
    $body = ($res -join $nl)
    if ($body -and $body.Trim().Length -gt 0) {
        [System.IO.File]::WriteAllText($target, $body, $utf8)
        ("[ok]   " + $f.Name + "  " + [int]$sw.Elapsed.TotalSeconds + "s  in=" + $payload.Length + " out=" + $body.Length) |
            Add-Content -Path $log -Encoding utf8
    } else {
        ("[FAIL] " + $f.Name + "  empty result") | Add-Content -Path $log -Encoding utf8
    }
}

("[" + (Get-Date -Format s) + "] done") | Add-Content -Path $log -Encoding utf8
Pop-Location
