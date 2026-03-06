# Multi-Agent Output Format Spec

## Goal
Provide deterministic, clean, auditable outputs for multi-agent collaboration.

## Required Top-Level Sections
1. `Summary`: one-screen conclusion and current decision.
2. `Task Context`: constraints, assumptions, objective.
3. `Collaboration Routing`: selected preset, primary mode, enabled modes, routing reasons.
4. `Execution Plan`: phases, owners, and dependency chain.
5. `Quality & Risk Gates`: veto decisions, evidence links, gate status.
6. `Next Actions`: explicit tasks with owner and deadline.
7. `Machine JSON`: exact machine-readable object used for downstream automation.

## Required Field Discipline
- Every decision must include `evidence` or `test_reference`.
- Split statements into `facts`, `assumptions`, `risks`.
- Timestamps must be `ISO 8601 UTC`.
- Cross-agent handoffs must include `from`, `to`, `phase`, `task_reference`, `acceptance_criteria`.

## Templates
- `handoff`: metadata + context + deliverable request + quality expectations.
- `pipeline_status`: phase, completed/total tasks, qa pass rate, blocked tasks, health.
- `qa_verdict`: task id, attempt, verdict, evidence, issue list, fix instructions.
- `decision_log`: options, scores, vetoes, winner, owner, timestamp.

## Render Rules
- Use flat bullets only.
- Prefer tables for scorecards and gate status.
- Keep each section concise and deterministic in ordering.
