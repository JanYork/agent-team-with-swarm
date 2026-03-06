# Stigmergy Signal Design

## 1) Goal
Enable swarm collaboration through environment footprints instead of direct chat coupling.

Core loop:
1. Agent autonomously writes a signal to shared environment.
2. Other agents autonomously discover environment state.
3. Agents decide next action and write new signals.

This is the software form of stigmergy (pheromone-like indirect coordination).

Default policy:
- Signal emission is automatic.
- Signal discovery is automatic.
- Manual signal writing is debug-only and should not be part of normal execution.

## 2) Signal Storage Layout

Required runtime-local paths:
- `.codex/project/signal/<project_id>/<yyyy-mm-dd>/`
- `.claude/project/signal/<project_id>/<yyyy-mm-dd>/`

Recommended filename:
- `<ts_utc_ms>__<signal_type>__<agent_id>__<signal_id>.json`

Example:
- `.codex/project/signal/agentteam-demo/2026-03-06/1772812345123__task.claim__release_manager__sig_01J....json`

## 3) Signal Envelope (JSON)

Every signal should follow one envelope:

```json
{
  "signal_id": "sig_01JEXAMPLE",
  "project_id": "agentteam-demo",
  "run_id": "run_20260306_01",
  "timestamp_utc": "2026-03-06T15:22:00Z",
  "runtime": "codex",
  "agent_id": "release_manager",
  "signal_type": "task.claim",
  "emission_mode": "auto",
  "topic": "publish_pipeline",
  "priority": "high",
  "confidence": 0.84,
  "ttl_seconds": 1800,
  "tags": ["swarm", "assurance"],
  "refs": {
    "parent_signal_id": "sig_01JPREV",
    "trace_id": "trace_01JTRACE"
  },
  "pheromone": {
    "key": "publish_pipeline",
    "strength": 0.78,
    "evaporation_half_life_seconds": 3600
  },
  "payload": {}
}
```

## 4) Signal Types

Minimal required set:
- `run.started`: session boot and initial constraints.
- `task.offer`: a task slot is announced.
- `task.claim`: an agent takes ownership.
- `task.progress`: partial status and checkpoint.
- `task.blocked`: blocker + dependency + needed action.
- `artifact.published`: output artifact written and where.
- `vote.cast`: roundtable/debate scoring vote.
- `verdict.final`: READY/NEEDS_WORK decision with evidence refs.
- `run.closed`: final summary and closure reason.

## 5) Pheromone Semantics

`pheromone.strength` guides priority and routing:
- Increase when repeated confirmations/evidence exist.
- Decrease over time via `evaporation_half_life_seconds`.
- Remove stale trails when signal TTL expires.

Decision heuristic (suggested):
- High strength + fresh TTL -> prioritize.
- Low strength + repeated block -> escalate.
- Conflicting high-strength trails -> trigger debate/judgement.

## 6) Coordination Rules

1. Append-only write; do not edit historical signals.
2. Use atomic write (`tmp` then rename).
3. Use `signal_id` for idempotency and de-dup.
4. Ownership transfer must be explicit:
- `task.claim` by next agent
- optional `task.release` by previous owner
5. Always include evidence refs in `verdict.final`.

Autonomy rules:
6. Agents must auto-emit on phase transitions and ownership changes.
7. Agents must auto-read latest signals before every planning/execution step.
8. Human-triggered `signal.write` is debug-only and must mark `emission_mode=manual_debug`.

## 7) Retention

Recommended retention:
- Hot signals: 7 days
- Archived signals: 30 days
- Keep `verdict.final` and `run.closed` for audit

Ephemeral mode (default for this project):
- After task completion, run closure should cleanup footprints.
- Use `close` operation to emit `run.closed` then remove run signals.
- Keep closed signal only when explicit audit retention is requested.

## 8) Runtime Integration

Codex and Claude should both:
1. Read latest signals before planning a new action.
2. Emit at least one signal for each phase transition.
3. Emit `verdict.final` before ending execution.
4. Keep a periodic discovery loop (recommended poll interval: 2-5 seconds while active).

## 9) Machine Schema

Validation schema:
- `docs/schemas/stigmergy-signal.schema.json`

Examples:
- `docs/signal-examples/task_claim.json`
- `docs/signal-examples/vote_cast.json`

## 10) Runtime Helper (Minimal Implementation)

Helper script:
- `codex/skill/swarm-roundtable-orchestrator/scripts/stigmergy_signal_bus.py`

Typical usage:

```bash
# Observe latest signals
python3 codex/skill/swarm-roundtable-orchestrator/scripts/stigmergy_signal_bus.py \
  tail --runtime codex --project-id agentteam-demo --run-id run_20260306_01 --limit 20

# Watch live signals (poll every 3s)
python3 codex/skill/swarm-roundtable-orchestrator/scripts/stigmergy_signal_bus.py \
  watch --runtime codex --project-id agentteam-demo --run-id run_20260306_01 --interval-seconds 3

# Inspect one trace
python3 codex/skill/swarm-roundtable-orchestrator/scripts/stigmergy_signal_bus.py \
  trace --runtime codex --project-id agentteam-demo --trace-id trace_run_20260306_01 --limit 50

# Close run and cleanup footprints (default behavior)
python3 codex/skill/swarm-roundtable-orchestrator/scripts/stigmergy_signal_bus.py \
  close --runtime codex --project-id agentteam-demo --run-id run_20260306_01 --agent-id agents_orchestrator
```
