# Phase 8 local deployment run script

$ErrorActionPreference = 'Stop'

Write-Host "Starting Phase 8 service on http://127.0.0.1:8010"
d:/IITM/CustomerSupport/.venv/Scripts/python.exe -m uvicorn src.phase8.service:app --host 127.0.0.1 --port 8010
