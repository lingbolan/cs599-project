@echo off
cd /d D:\codex\code\autospider
set "PLAYWRIGHT_BROWSERS_PATH=D:\codex\code\autospider\.pw-browsers"
set "DATABASE_URL=sqlite:///output/autospider.db"
set "GRAPH_CHECKPOINT_ENABLED=true"
set "GRAPH_CHECKPOINT_BACKEND=memory"
set "PIPELINE_MODE=memory"
set "LOCAL_SERIAL_MODE=true"
set "PIPELINE_CONSUMER_CONCURRENCY=1"
.\.venv\Scripts\autospider.exe chat-pipeline
