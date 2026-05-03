# Phase Artifacts Index

This folder is the canonical, single location for all phase documentation and phase outputs.

## Structure
- phase1/documentation
- phase2/documentation
- phase2/outputs
- phase3/documentation
- phase3/outputs
- phase4/documentation
- phase4/outputs
- phase5/documentation
- phase5/outputs
- phase6/documentation
- phase6/outputs
- phase7/documentation
- phase7/outputs
- phase8/documentation
- phase8/outputs
- phase9/documentation
- phase9/outputs

## Notes
- Original files remain in their source folders (`docs`, `reports`, `outputs`, `logs`) so scripts continue to work.
- This folder stores synchronized copies for review/submission convenience.
- After each new run, sync fresh outputs into this folder by running:
	- `pwsh -File scripts/sync_phase_artifacts.ps1`
