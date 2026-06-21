# Local Windows launcher that keeps AutoSpider output in UTF-8.
chcp.com 65001 > $null

$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $PSScriptRoot ".pw-browsers"

$autospider = Join-Path $PSScriptRoot ".venv\Scripts\autospider.exe"
& $autospider @args
exit $LASTEXITCODE
