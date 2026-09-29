# translate_pdf.ps1 -- chunked machine translation for PDF-derived markdown sources
# =============================================================================
# Backend: the local `claude -p` print mode (same as translate_cli.ps1), so it
# needs no LLM_API_KEY. Difference: PDF text is much longer than a blog post, so
# the body is split on paragraph boundaries into ~ChunkChars pieces and each
# piece is translated separately, then joined. Resume-friendly: an output file
# that already exists is skipped; for a bad chunk add "<!-- TRANSLATION_MISSING".
# =============================================================================
param([int]$Limit = 0, [int]$ChunkChars = 12000)
chcp 65001 | Out-Null
$ErrorActionPreference = "Continue"

$Root = "C:\Users\35586\Desktop\Challenge\cs146s-vibe-coding-zh"
$src = Join-Path $Root "pdf_source"
$out = Join-Path $Root "pdf_translated"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$log = Join-Path $out "_translate_log.txt"
$nl = [string][char]10
$utf8 = New-Object System.Text.UTF8Encoding($false)

$glossRows = Import-Csv (Join-Path $Root "pipeline\glossary.csv") |
    Where-Object { $_.en -and $_.zh } |
    ForEach-Object { "- " + $_.en + " -> " + $_.zh }
$gloss = $glossRows -join $nl

$rules = @"
翻译要求：
1) 把「待翻译正文」中的英文忠实翻译成简体中文，不遗漏、不增删；
2) 代码块、命令、URL、专有名词、文件名保持原样；
3) 严格使用「术语对照表」的译法；未列出的术语首次出现用「中文（English）」标注；
4) 保留 Markdown 结构（标题、列表、表格、引用、代码块）；
5) 保留形如 <!-- page N --> 的 HTML 注释标记，原样输出；
6) 只输出「待翻译正文」的译文，不要输出本要求或术语表，不要任何解释、前言或结语；
7) 正文可能是长文的一个片段，只翻译给出的片段，不要补写、不要总结、不要省略。
"@
$instr = "把标准输入中「待翻译正文」部分的英文翻译成简体中文，严格遵守其中的翻译要求与术语表，只输出译文。"

function Get-Chunks([string]$text, [int]$size) {
    $paras = [regex]::Split($text, "(?:\r?\n){2,}")
    $chunks = New-Object System.Collections.ArrayList
    $buf = New-Object System.Text.StringBuilder
    foreach ($p in $paras) {
        $pieces = New-Object System.Collections.ArrayList
        if ($p.Length -gt $size) {
            $i = 0
            while ($i -lt $p.Length) {
                $len = [Math]::Min($size, $p.Length - $i)
                [void]$pieces.Add($p.Substring($i, $len))
                $i += $len
            }
        } else { [void]$pieces.Add($p) }
        foreach ($pc in $pieces) {
            if ($buf.Length -gt 0 -and ($buf.Length + $pc.Length) -gt $size) {
                [void]$chunks.Add($buf.ToString()); [void]$buf.Clear()
            }
            if ($buf.Length -gt 0) { [void]$buf.Append($nl + $nl) }
            [void]$buf.Append($pc)
        }
    }
    if ($buf.Length -gt 0) { [void]$chunks.Add($buf.ToString()) }
    return $chunks
}

Push-Location $env:TEMP
$files = Get-ChildItem -Path $src -Filter *.md |
    Where-Object { $_.Name -notlike "_*" } |
    Sort-Object Name
if ($Limit -gt 0) { $files = $files | Select-Object -First $Limit }
("[" + (Get-Date -Format s) + "] pdf start, files=" + $files.Count + ", chunkChars=" + $ChunkChars) | Add-Content -Path $log -Encoding utf8

foreach ($f in $files) {
    $target = Join-Path $out $f.Name
    if (Test-Path $target) {
        ("[skip] " + $f.Name + " already present") | Add-Content -Path $log -Encoding utf8
        continue
    }
    $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $chunks = Get-Chunks $raw $ChunkChars
    $parts = New-Object System.Collections.ArrayList
    $failed = New-Object System.Collections.ArrayList
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    for ($ci = 0; $ci -lt $chunks.Count; $ci++) {
        $payload = "# 翻译要求" + $nl + $rules + $nl + "# 术语对照表" + $nl + $gloss + $nl + "# 待翻译正文" + $nl + $chunks[$ci]
        $res = $null
        for ($attempt = 1; $attempt -le 2; $attempt++) {
            try { $res = $payload | & claude -p $instr --output-format text --no-session-persistence 2>$null } catch { $res = $null }
            $joined = ($res -join $nl)
            if ($joined -and $joined.Trim().Length -gt 0) { break }
            Start-Sleep -Seconds 5
        }
        $body = ($res -join $nl)
        if ($body -and $body.Trim().Length -gt 0) {
            [void]$parts.Add($body)
            ("[chunk] " + $f.Name + " " + ($ci + 1) + "/" + $chunks.Count + " in=" + $chunks[$ci].Length + " out=" + $body.Length) |
                Add-Content -Path $log -Encoding utf8
        } else {
            [void]$parts.Add("<!-- TRANSLATION_MISSING chunk " + ($ci + 1) + " -->")
            [void]$failed.Add($ci + 1)
        }
    }
    $sw.Stop()
    $final = ($parts -join ($nl + $nl))
    [System.IO.File]::WriteAllText($target, $final, $utf8)
    if ($failed.Count -eq 0) {
        ("[ok]   " + $f.Name + "  " + [int]$sw.Elapsed.TotalSeconds + "s  chunks=" + $chunks.Count + " out=" + $final.Length) |
            Add-Content -Path $log -Encoding utf8
    } else {
        ("[PART] " + $f.Name + "  failed chunks=" + ($failed -join ",")) | Add-Content -Path $log -Encoding utf8
    }
}
("[" + (Get-Date -Format s) + "] pdf done") | Add-Content -Path $log -Encoding utf8
Pop-Location
