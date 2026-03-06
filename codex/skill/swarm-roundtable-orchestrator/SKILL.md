---
name: swarm-roundtable-orchestrator
description: Codex swarm + multi-expert roundtable orchestration with dynamic experts and topology.
---

# Swarm Roundtable Orchestrator

## Overview

Enable a repeatable collaboration pattern:
1) swarm in parallel for exploration/implementation,
2) run a structured roundtable for critique and scoring,
3) converge with explicit consensus and risk gates.

Article-aligned mode taxonomy (auto-routed):
- `roundtable`: brainstorming / complex reasoning.
- `experts`: high-quality integrated analysis.
- `debate_judgement`: logic-heavy review and adjudication.
- `swarm`: large-scale parallel execution.
- `hierarchical`: director-manager-worker decomposition.
- `dag`: dependency-aware engineering workflow.

Codex-native runtime policy:
- Prefer Codex `agent team` + `sub-agent` as primary execution runtime.
- Treat external role repos as role overlays (focus/outputs/instructions), not runtime replacement.

## Workflow

1. Frame the mission.
- Capture objective, constraints, deadline, and success criteria.
- Choose `task_type`: `feature`, `incident`, `architecture`, `research`, `growth`, or `generic`.

2. Generate the swarm + roundtable blueprint.
- Run:
```bash
python3 scripts/swarm_roundtable_plan.py \
  --task "<task statement>" \
  --context "<constraints and environment>" \
  --task-type auto \
  --complexity auto \
  --primary-mode auto \
  --force-modes "" \
  --disable-modes "" \
  --min-experts 3 \
  --max-experts 8 \
  --format markdown
```
- Use the output to decide coordinator + experts and the discussion agenda.
- Inspect `generation_log` for auto-added experts and trigger evidence.
- Inspect `swarm_topology` for dynamic cells and parallel waves.
- Inspect `collaboration_modes` for mode routing reasons and article scenario fit.
- Inspect `debate_judgement`, `hierarchical_execution`, and `dag_workflow` for execution-ready structure.
- Enforce output shape from `references/output-format-spec.md`.

2.2 Generate Symphony fusion workflow when needed.
- Use `--runner symphony` or `--runner hybrid`:
```bash
python3 scripts/swarm_roundtable_plan.py \
  --task "<task statement>" \
  --context "<constraints>" \
  --runner hybrid \
  --symphony-project-slug "<linear-project-slug>" \
  --symphony-workflow-output /path/to/WORKFLOW.md \
  --format markdown
```
- `runner=hybrid` keeps native swarm-roundtable output and also emits Symphony `WORKFLOW.md`.
- Use `--symphony-active-states` and `--symphony-terminal-states` to match your tracker workflow.
- The generated front matter includes `swarm_roundtable` extension fields for audit and policy versioning.

2.3 Emit Codex agent-team + sub-agent configs.
- The blueprint always includes a `codex_multi_agent` block:
  - `agent_teams`: role teams aligned with swarm cells, judges, debate arena/jury, hierarchy manager teams, and DAG orchestration.
  - `sub_agent_runtime`: mode-aware thread/depth/runtime limits (auto-scales by enabled modes).
  - `config_toml`: ready-to-use `.codex/config.toml` draft (`[features]` + `[agents]` + per-role agent entries).
  - `role_configs`: per-role `agents/*.toml` content for sub-agent behavior.
- Optionally write files directly:
```bash
python3 scripts/swarm_roundtable_plan.py \
  --task "<task statement>" \
  --context "<constraints>" \
  --agent-team-max-threads 10 \
  --agent-team-max-depth 2 \
  --agent-team-job-max-runtime-seconds 1800 \
  --agent-team-config-output /path/to/.codex/config.toml \
  --agent-team-roles-dir /path/to/.codex/agents \
  --format markdown
```

2.4 Force specific collaboration modes when needed.
- Example: force hierarchy + dag + debate for strict execution governance:
```bash
python3 scripts/swarm_roundtable_plan.py \
  --task "<task statement>" \
  --context "<constraints>" \
  --primary-mode hierarchical \
  --force-modes "hierarchical,dag,debate_judgement,experts" \
  --debate-rounds 2 \
  --dag-max-parallel-nodes 6 \
  --format markdown
```

2.5 Use session playbook for repeatable execution.
- Before running a large multi-agent task, load and follow:
  - `references/session-playbook-multi-agents.md`
- This gives deterministic checkpoints for activation, handoff, escalation, and gate decisions.

2.6 Agency role overlays (repository fusion).
- Mapped and integrated roles are documented in:
  - `references/agency-role-map.md`
- Use these role keys directly in `--expert` when needed, for example:
```bash
python3 scripts/swarm_roundtable_plan.py \
  --task "内容自动化运营" \
  --context "写作+配图+发布+合规+复盘" \
  --expert "content_creator::editorial strategy and long-form copy::editorial_calendar,content_drafts,distribution_plan::product_consultant" \
  --expert "image_prompt_engineer::visual prompt quality::image_prompt_pack,negative_prompt_pack,style_variants::uiux_designer" \
  --expert "legal_compliance_checker::platform and privacy compliance::compliance_risks,required_controls,approval_or_block_decision::cto" \
  --format markdown
```

2.1 Inject custom experts when needed.
- Use one or more `--expert` arguments:
```bash
python3 scripts/swarm_roundtable_plan.py \
  --task "..." \
  --context "..." \
  --expert "business_domain_expert::industry constraints and monetization model::domain_constraints,revenue_risks::default" \
  --expert "red_team_critic::actively challenge weak assumptions::critical_failures,challenge_cases::default" \
  --format markdown
```
- Expert format: `role::focus::output1,output2::agent_type`.
- If `agent_type` is one of built-in role agents, that subagent type is used; otherwise fallback is `default`.
- Disable automatic expert augmentation with `--disable-auto-experts` when you need strict manual control.

## Slash Command Layer

If the user starts input with `/`, treat it as a command and map it using `../../../../docs/COMMANDS.md`.

Supported commands:
- `/help`
- `/plan <task>`
- `/roundtable <task>`
- `/swarm <task>`
- `/debate <task>`
- `/full <task>`
- `/experts list`
- `/experts add <role>::<focus>::<outputs_csv>::<agent_type>`
- `/experts remove <role>`
- `/experts bounds <min> <max>`
- `/consensus <scores_json_path>`
- `/signal tail [limit]`
- `/signal topic <topic> [limit]`
- `/signal trace <trace_id>`
- `/signal stats`
- `/signal close [run_id]`
- `/status`
- `/finalize`

Codex execution mapping:
- `/plan`: run `scripts/swarm_roundtable_plan.py` with auto mode.
- `/roundtable`: force `roundtable,experts`.
- `/swarm`: force `swarm,hierarchical,dag,experts`.
- `/debate`: force `debate_judgement,roundtable,experts` with `--debate-rounds 2`.
- `/full`: force all modes.
- `/consensus`: run `scripts/roundtable_consensus.py --input <path>`.
- `/signal ...`: use `scripts/stigmergy_signal_bus.py` for inspection and closure.

Rules:
- Parse commands case-insensitively.
- For unknown command, return compact help.
- Enforce expert bounds `3..10`.
- `/finalize` must output READY/NEEDS_WORK with evidence and trigger `/signal close` automatically.
- Agents must auto-emit and auto-discover signals under `.codex/project/signal/<project_id>/...`.
- `/signal` commands are for observation/inspection, not primary emission path.
- Signal structure must follow `../../../../docs/STIGMERGY_SIGNALS.md`.
- After task completion, signal cleanup is mandatory (normally via `/finalize` -> `/signal close`).

3. Spawn experts in parallel (swarm stage).
- Use `spawn_agent` for each suggested role.
- Send each expert its ownership slice and a strict output schema.
- Require each expert to return one proposal card:
```json
{
  "proposal_id": "Option-A",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."]
}
```

4. Run roundtable critique and scoring.
- Share all proposal cards with every expert.
- Ask each expert to score every option on common criteria and optionally issue vetoes:
```json
{
  "expert": "software_architect",
  "scores": {
    "Option-A": {"impact": 4, "feasibility": 5, "risk_control": 3, "time_to_value": 3, "maintainability": 4}
  },
  "veto": [{"option": "Option-B", "reason": "high rollback risk"}],
  "notes": "..."
}
```

5. Compute consensus deterministically.
- Aggregate expert scoring with:
```bash
python3 scripts/roundtable_consensus.py \
  --input /path/to/scores.json \
  --format markdown
```
- If consensus is below threshold, run a second round focused on top 2 options.

6. Execute convergence swarm.
- Convert the winning option (or hybrid) into concrete work slices.
- Assign owners by role and run execution agents in parallel.
- Keep a QA/reliability gate before final delivery.

## Guardrails

- Keep swarm size focused: 3-8 experts by default.
- Roundtable expert count hard limit: minimum 3, maximum 10.
- Enforce explicit ownership per expert to avoid overlap churn.
- Use a timebox for each phase (explore, critique, converge).
- Require evidence (tests, traces, links, or metrics), not opinions only.
- Treat `qa_engineer`, `devops_engineer`, `software_architect`, and `cto` vetoes as hard blockers by default.
- For fused workflows, also treat `legal_compliance_checker`, `experiment_tracker`, and `reality_checker` as hard-veto candidates when present.
- Avoid anti-pattern: call everyone into all discussions.
- Avoid anti-pattern: start execution before convergence.
- Avoid anti-pattern: ignore disagreement metrics.

## Resources

- `scripts/swarm_roundtable_plan.py`: build role topology, phase plan, scoring rules, and ready-to-send prompts.
- `scripts/roundtable_consensus.py`: compute weighted scores, approvals, disagreement index, and recommendation.
- `references/research-grounding.md`: distilled implementation principles and sources.
- `references/consensus-input-example.json`: starter JSON schema for consensus calculation.
- `references/output-format-spec.md`: deterministic output contract for readable and machine-safe results.
- `references/session-playbook-multi-agents.md`: session-level execution template for roundtable + swarm.
- `references/agency-role-map.md`: fused role mappings from `agency-agents`.
