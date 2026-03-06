# Swarm Roundtable For Claude Code

## What this pack provides
- Dynamic swarm + roundtable orchestration without Python runtime scripts.
- Agent-team style collaboration using Claude subagents (`Task`) and structured handoffs.
- Agency-agents role overlays for end-to-end automation workflows (ideation -> creation -> media -> publish -> compliance -> analytics).

## Agent roster
- Swarm Roundtable Orchestrator
- Trend Researcher
- Feedback Synthesizer
- Content Creator
- Visual Storyteller
- Image Prompt Engineer
- Social Media Strategist
- Report Distribution Agent
- Legal Compliance Checker
- Brand Guardian
- Analytics Reporter
- Experiment Tracker
- Evidence Collector
- Reality Checker

## Quick start in Claude Code
1. Activate `Swarm Roundtable Orchestrator`.
2. Provide mission + constraints + deadline.
3. Orchestrator spawns subagents with `Task` and uses templates in `templates/`.
4. Gate decisions must include evidence and explicit verdict (`PASS/FAIL/NEEDS_WORK`).

## Recommended first prompt
Use playbook: `playbooks/roundtable-swarm-session.md`.
