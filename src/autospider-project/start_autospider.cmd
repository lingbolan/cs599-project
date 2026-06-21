@echo off
chcp 65001 > nul
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PLAYWRIGHT_BROWSERS_PATH=%~dp0.pw-browsers"
set "DATABASE_URL=sqlite:///output/autospider.db"
set "GRAPH_CHECKPOINT_ENABLED=true"
set "GRAPH_CHECKPOINT_BACKEND=memory"
set "PIPELINE_MODE=memory"
set "LOCAL_SERIAL_MODE=true"
set "PIPELINE_CONSUMER_CONCURRENCY=1"
.\.venv\Scripts\autospider.exe chat-pipeline
