# Customer Support AI Agent

## Current Status
- Phase 1 complete (problem framing and success definition)
- Phase 2 baseline implemented (rule/template agent)

## Setup
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```

## Run Baseline CLI
```bash
python -m src.cli
```

## Run Baseline API
```bash
uvicorn src.app:app --reload
```

## Run Forced Demo Cases
```bash
python scripts/run_phase2_demo.py
```

## Logs
- `logs/phase2_interactions.jsonl`
- `logs/phase2_api_interactions.jsonl`
- `logs/phase2_forced_demo.jsonl`
- `logs/phase2_forced_demo_outputs.json`
