# Research Grounding For Swarm + Roundtable

## Core Principles Used In This Skill

1. Swarm systems rely on local interactions and self-organization.
- Practical translation: keep experts autonomous with clear local ownership, then converge through lightweight coordination.

2. Agent orchestration works best with explicit handoffs and a central manager pattern when tasks branch.
- Practical translation: use a coordinator for topology and gates, but let specialists run parallel deep work.

3. Structured consensus methods improve decision quality over free-form discussion.
- Practical translation: enforce shared criteria, numeric scoring, and veto semantics.

4. Large all-hands incident or design calls can become anti-patterns.
- Practical translation: cap panel size, separate divergence and convergence, and keep strict timeboxes.

5. Multi-agent reasoning quality improves with critique/debate loops, but needs a final reconciliation step.
- Practical translation: run at least one critique round and then force deterministic aggregation.

6. Collaboration architecture should be routed by scenario, not fixed as one pattern.
- Practical translation: expose explicit routing across
  `roundtable`, `experts`, `debate_judgement`, `swarm`, `hierarchical`, and `dag`,
  then align agent-team topology with selected modes.

## Source Links

- Swarm intelligence and collective behavior context:
  - https://pubmed.ncbi.nlm.nih.gov/9115526/
- Agile swarming signal (focus WIP bottlenecks by teaming up):
  - https://www.atlassian.com/agile/kanban/wip-limits
- Incident anti-patterns for over-broad calls:
  - https://response.pagerduty.com/oncall/incident-antipatterns/
- OpenAI Swarm (legacy) and handoff concept:
  - https://github.com/openai/swarm
- OpenAI Agents SDK handoffs and manager/handoff patterns:
  - https://openai.github.io/openai-agents-python/handoffs/
  - https://openai.github.io/openai-agents-python/multi_agent/
- LangChain multi-agent pattern framing (tool-calling vs handoffs):
  - https://docs.langchain.com/oss/python/langchain/multi-agent
- Structured consensus method references:
  - https://www.ndsu.edu/agriculture/extension/publications/facilitating-groups-nominal-group-technique
  - https://pubmed.ncbi.nlm.nih.gov/29403193/
- LLM roundtable / debate evidence:
  - https://www.alphaxiv.org/abs/2501.11092
  - https://www.alphaxiv.org/abs/2502.01703
- Symphony orchestration spec and workflow contract:
  - https://github.com/openai/symphony
  - https://github.com/openai/symphony/blob/main/SPEC.md
  - https://github.com/openai/symphony/blob/main/elixir/WORKFLOW.md
- Codex native multi-agent / sub-agent docs:
  - https://developers.openai.com/codex/multi-agent
  - https://developers.openai.com/codex/concepts/multi-agents
- Agency role design corpus used for role overlays:
  - https://github.com/msitarzewski/agency-agents

## What Not To Copy Blindly

- Do not copy "everyone comments on everything" behavior.
- Do not force 10+ experts into one round.
- Do not finalize without visible scoring and risk gate status.
