# Architecture Mapping

See also:
- `docs/PRINCIPLES.md` for design rationale and execution principles.

## Pattern mapping
- Roundtable -> scored expert discussion for convergence.
- Experts -> role-specialized parallel generation.
- Debate Judgement -> jury-based adjudication and veto control.
- Swarm -> parallel task execution waves.
- Hierarchical -> director-manager-worker decomposition.
- DAG -> dependency-aware phase orchestration.

## Runtime mapping
### Codex
- Agent team runtime: `codex/runtime/config.swarm-roundtable.toml`
- Subagent definitions: `codex/runtime/agents/*.toml`
- Skill + planner: `codex/skill/swarm-roundtable-orchestrator`

### Claude
- Orchestrator and specialists: `claude/agents/swarm-roundtable/*.md`
- Structured templates: `claude/agents/swarm-roundtable/templates/*.md`
- Session playbook: `claude/agents/swarm-roundtable/playbooks/roundtable-swarm-session.md`
