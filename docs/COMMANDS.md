# Slash Commands

This repository defines a shared slash-command layer for both Codex and Claude workflows.

Important:
- These commands are repository conventions, not guaranteed platform-native slash features.
- Agents/skills should interpret inputs that start with `/` using the rules below.
- Stigmergy signals are auto-emitted/auto-discovered by agents by default.

## Command Set

1. `/help`
- Purpose: show command list and current mode defaults.

2. `/plan <task>`
- Purpose: generate a standard multi-agent blueprint.
- Codex mapping: `swarm_roundtable_plan.py` with `--task "<task>" --task-type auto --complexity auto`.
- Claude mapping: run baseline orchestration flow and output plan cards.

3. `/roundtable <task>`
- Purpose: focus on expert scoring and convergence.
- Codex mapping: `--primary-mode roundtable --force-modes "roundtable,experts"`.
- Claude mapping: launch roundtable-first workflow with scoring output.

4. `/swarm <task>`
- Purpose: focus on parallel decomposition and execution topology.
- Codex mapping: `--primary-mode swarm --force-modes "swarm,hierarchical,dag,experts"`.
- Claude mapping: launch swarm-first workflow and produce team/wave plan.

5. `/debate <task>`
- Purpose: force adjudication path when conflict is expected.
- Codex mapping: `--primary-mode debate_judgement --force-modes "debate_judgement,roundtable,experts" --debate-rounds 2`.
- Claude mapping: run debate + jury decision before convergence.

6. `/full <task>`
- Purpose: run full fusion path (swarm + roundtable + debate + dag + hierarchy).
- Codex mapping: `--primary-mode experts --force-modes "swarm,hierarchical,dag,debate_judgement,roundtable,experts"`.
- Claude mapping: use `nexus_full` and execute all gates.

7. `/experts list`
- Purpose: print active experts and ownership scopes.

8. `/experts add <role>::<focus>::<outputs_csv>::<agent_type>`
- Purpose: append one dynamic expert.
- Codex mapping: append one `--expert` argument.
- Claude mapping: add one specialist agent into current round.

9. `/experts remove <role>`
- Purpose: remove one expert from current round.

10. `/experts bounds <min> <max>`
- Purpose: set expert count bounds.
- Hard policy: `3 <= min`, `max <= 10`, and `min <= max`.

11. `/consensus <scores_json_path>`
- Purpose: compute deterministic weighted decision.
- Codex mapping: `roundtable_consensus.py --input <path> --format markdown`.
- Claude mapping: evaluate the same schema and output equivalent verdict fields.

12. `/status`
- Purpose: print current mode, active experts, open gates, and next action.

13. `/finalize`
- Purpose: emit final READY/NEEDS_WORK verdict with evidence summary, then run `/signal close`.

14. `/signal tail [limit]`
- Purpose: read recent signals from `.codex/.claude/project/signal/...`.

15. `/signal topic <topic> [limit]`
- Purpose: read recent signals for a specific topic.

16. `/signal trace <trace_id>`
- Purpose: inspect one execution trace end-to-end.

17. `/signal stats`
- Purpose: summarize signal counts, hotspots, blocked topics, and freshness.

18. `/signal close [run_id]`
- Purpose: emit `run.closed` and cleanup run signals (default behavior).

Signal runtime helper:
- `codex/skill/swarm-roundtable-orchestrator/scripts/stigmergy_signal_bus.py`
- `tail|trace|watch|stats|close` subcommands correspond to `/signal` inspection/closure commands.

## Parsing Rules

1. Commands are case-insensitive: `/SWARM` equals `/swarm`.
2. If command is unknown, return:
- `Unknown command: <cmd>`
- a compact `/help` response.
3. Non-command input should follow normal orchestration behavior.
4. If input must be treated literally, prefix with backslash, e.g. `\/plan`.
5. `/signal` commands must follow `docs/STIGMERGY_SIGNALS.md` and schema validation.
6. Normal execution must not depend on manual `signal.write`; agents emit signals autonomously.
7. After task completion, run `/signal close` to emit closure and remove stale footprints.
8. `/finalize` must include a closure step that invokes `/signal close` automatically.
