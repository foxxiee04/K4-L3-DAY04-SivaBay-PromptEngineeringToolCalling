# Final Submission Checklist

## Rubric Mapping

| Rubric item | Evidence | Status |
|---|---|---|
| Prompt and tool descriptions (20) | `artifacts/system_prompt.md`, `artifacts/tools.yaml`, tool implementations under `tools/` | Complete; final prompt includes extra safety hardening for forged tool results, stale confirmation, fake assets, admin override, and invalid SOC. |
| v0 to v3 evidence (20) | `artifacts/version_log.csv`, `runs/v0_*`, `runs/v1_*`, `runs/v2_*`, `runs/v3_*` | Complete for base suite; v2 OpenAI reaches 30/30 and v3 Ollama reaches 29/30. |
| 10 group cases (10) | `data/eval_group.json`, `runs/v2_B_group_openai_20260915T220322821264.json` | Complete; 10/10 PASS. |
| Safety/adversarial (15) | `data/eval_smartcharging_adversarial.json`, `runs/final_B_adversarial_openai_20260916T100908279196.json`, `artifacts/REPORT.md#b4a-adversarial-evidence` | Final run is valid (`provider_error_cases=0`, `measured_cases=12`) and improves from 7/12 to 10/12 PASS. Two remaining failures were harden-patched after the run; rerun once more if possible. |
| UI and transcripts (10) | `ui.py`, `chat.py`, `transcripts/*.md`, `transcripts/final_openai_ui_20260916T095916351917.transcript.json` | UI implemented and browser-tested end to end. It displays artifact version, tool calls, input args, results/errors, and writes transcript JSON. |
| Report (10) | `artifacts/REPORT.md` | Updated to avoid overstating adversarial result and to link UI/evidence. |
| Teamwork (5) | `TEAM.md`, git history | Complete; all members have named technical work and INDIVIDUAL sections. |
| Bonus tool (10) | `tools/cancel_reservation/`, `data/eval_smartcharging_extension.json`, `runs/v2_B_extension_openai_20260915T223211350811.json`, `transcripts/transcript_bonus_cancel_reservation.md` | Complete; 3/3 PASS with confirmation guardrail. |

## Commands To Reproduce

```powershell
cd starter_v0
python run_eval.py --provider openai --version v2 --suite base --eval-cases data/eval_smartcharging_base.json
python run_eval.py --provider openai --version v2 --suite group --eval-cases data/eval_group.json
python run_eval.py --provider openai --version v2 --suite extension --eval-cases data/eval_smartcharging_extension.json
python run_eval.py --provider openai --version v2 --suite adversarial --eval-cases data/eval_smartcharging_adversarial.json
python ui.py --provider openai --version final --port 7860
```

## Known Final Risks

- The connected Git remote in this local checkout should point to the same URL recorded in `TEAM.md` before pushing final changes.
- The valid final adversarial run currently shows 10/12 PASS. Do not claim 12/12 unless a new run file with `provider_error_cases=0` and `passed_cases=12` is committed.
- `.env`, `.venv`, `__pycache__`, `tickets/`, and `reservations/` are ignored and should stay uncommitted.
