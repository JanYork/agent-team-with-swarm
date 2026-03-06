# Swarm + Roundtable Blueprint

- Task: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
- Task Type: growth
- Complexity: high
- Runner: native
- Coordinator: product_manager
- Context: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程

## Expert Panel
1. `product_manager` [default/template] - scope, acceptance criteria, prioritization (outputs: scope_boundaries, acceptance_criteria, priority_rationale)
2. `data_governance_specialist` [default/dynamic] - data quality, lineage, privacy, and compliance controls (outputs: data_policies, pii_controls, compliance_checks)
3. `evidence_collector` [default/dynamic] - evidence-based QA and proof collection (outputs: qa_evidence_report, pass_fail_verdict, defect_log)
4. `experiment_tracker` [default/dynamic] - experiment lifecycle and decision discipline (outputs: experiment_design, experiment_results, decision_recommendation)
5. `release_manager` [default/dynamic] - release train planning, rollout safety, and rollback readiness (outputs: release_plan, rollout_gates, rollback_readiness)
6. `content_creator` [product_consultant/template] - editorial strategy and multi-format content production (outputs: editorial_calendar, content_drafts, content_distribution_plan)
7. `image_prompt_engineer` [uiux_designer/template] - structured AI image prompt engineering for publication assets (outputs: image_prompt_pack, negative_prompt_pack, style_variants)
8. `social_media_strategist` [product_consultant/template] - cross-platform publishing strategy and campaign rhythm (outputs: channel_plan, campaign_schedule, distribution_metrics_plan)
9. `analytics_reporter` [data_analyst/template] - KPI reporting, attribution, and operational insights (outputs: kpi_dashboard_spec, attribution_summary, optimization_recommendations)
10. `legal_compliance_checker` [cto/template] - legal and regulatory compliance review for content and data operations (outputs: compliance_risks, required_controls, approval_or_block_decision)

## Dynamic Generation Log
- dynamic expert added: data_governance_specialist (hits: 合规, 审计)
- dynamic expert added: content_creator (hits: 内容运营, 写作)
- dynamic expert added: release_manager (hits: 发布)
- dynamic expert added: image_prompt_engineer (hits: 配图)
- dynamic expert added: social_media_strategist (hits: 发布)
- dynamic expert added: legal_compliance_checker (hits: 合规)
- dynamic expert added: analytics_reporter (hits: 复盘)
- dynamic expert added: experiment_tracker (hits: 实验)
- dynamic expert added: evidence_collector (hits: 证据)

## Collaboration Routing
- Primary mode: swarm
- Selected preset: nexus_full
- Enabled modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts
- Routing reasons:
  - swarm: keyword:蜂群; task_type:growth; complexity:high
  - hierarchical: keyword:流程; complexity:high
  - dag: complexity:high
  - debate_judgement: keyword:评审; keyword:审查; complexity:high
  - roundtable: task_type:growth
  - experts: base: multi-expert collaboration baseline; keyword:专家; task_type:growth
- Article scenario fit:
  - roundtable: brainstorming / 复杂推理
  - experts: 高质量综合分析
  - debate_judgement: 逻辑推理 / 审查
  - swarm: 大规模并行任务
  - hierarchical: 复杂任务管理
  - dag: 工程化流程

## Swarm Topology
- Parallel waves: 3
- `discovery_cell` (wave 1): clarify goals, business constraints, and option framing | roles: product_manager
- `design_cell` (wave 1): stress-test architecture and cross-cutting risks | roles: data_governance_specialist, content_creator, image_prompt_engineer
- `build_cell` (wave 2): plan implementation slices and integration details | roles: social_media_strategist
- `assurance_cell` (wave 3): define quality/release gates and rollback readiness | roles: evidence_collector, experiment_tracker, release_manager, analytics_reporter, legal_compliance_checker

## Phases
- `phase_0_alignment` (10m, mode=hierarchical): lock mission boundaries, non-goals, and decision rules
- `phase_1_divergent_swarm` (30m, mode=swarm): multi-cell parallel exploration and deep risk surfacing
- `phase_2b_debate_judgement` (12m, mode=debate_judgement): run structured debate and jury vote on finalists
- `phase_2_roundtable_critique` (20m, mode=roundtable): cross-cell challenge, scoring, and veto checks
- `phase_3_convergent_swarm` (40m, mode=experts): merge winner/hybrid into execution design and owners
- `phase_4_hardening_gate` (20m, mode=debate_judgement): quality/reliability/release gate review before close

## Roundtable Rules
- Consensus threshold: 0.67
- Hard veto roles: data_governance_specialist, experiment_tracker, legal_compliance_checker
- Adjudication mode: debate_judgement_jury
- Criteria weights:
  - impact: 0.25
  - feasibility: 0.25
  - risk_control: 0.2
  - time_to_value: 0.15
  - maintainability: 0.15

## Debate Judgement
- Enabled: True
- Rounds: 2
- Debaters: evidence_collector, release_manager, content_creator, image_prompt_engineer, social_media_strategist, analytics_reporter
- Jury roles: product_manager, data_governance_specialist, experiment_tracker, legal_compliance_checker
- Vote policy: method=jury_weighted_majority, jury_weight=2, debater_weight=1, jury_quorum=3, tie_breaker=product_manager

## Hierarchical Execution
- Enabled: True
- Director: product_manager
- Managers: data_governance_specialist, content_creator, image_prompt_engineer
- Workers: evidence_collector, experiment_tracker, release_manager, social_media_strategist, analytics_reporter, legal_compliance_checker
- Manager `data_governance_specialist` owns workers: evidence_collector, social_media_strategist (focus: stress-test architecture and cross-cutting risks)
- Manager `content_creator` owns workers: experiment_tracker, analytics_reporter (focus: stress-test architecture and cross-cutting risks)
- Manager `image_prompt_engineer` owns workers: release_manager, legal_compliance_checker (focus: stress-test architecture and cross-cutting risks)

## DAG Workflow
- Enabled: True
- Nodes: 9
- Edges: 9
- Max parallel nodes: 2
- Critical path: alignment_gate -> discovery_cell_wave_1 -> build_cell_wave_2 -> assurance_cell_wave_3 -> roundtable_critique -> debate_judgement -> convergent_execution -> hardening_gate
- Parallel group: discovery_cell_wave_1, design_cell_wave_1

## Output Format Contract
- Version: 1.1.0
- Goal: deterministic, auditable, and readable outputs for multi-agent collaboration
- Global rules:
  - facts_assumptions_risks_must_be_explicit
  - all_decisions_require_evidence_or_test_reference
  - handoff_payload_is_mandatory_for_cross-agent_edges
  - timestamp_in_iso8601_utc
- Document layout:
  - 01_summary
  - 02_task_context
  - 03_collaboration_routing
  - 04_execution_plan
  - 05_quality_and_risk_gates
  - 06_next_actions
  - 07_machine_readable_json
- Templates:
  - handoff: from, to, phase, task_reference, priority, timestamp
  - pipeline_status: current_phase, tasks_total, tasks_completed, qa_pass_rate, blocked_tasks, pipeline_health, next_action
  - qa_verdict: task_id, attempt, verdict, evidence, issues, fix_instructions
  - decision_log: decision_id, options_compared, scores, vetoes, final_decision, owner, timestamp

## Codex Agent Team
- Sub-agent runtime: max_threads=14, max_depth=2, job_max_runtime_seconds=1800
- Mode-aware autoscaling: True
- Feature flag multi_agent: True
### Agent Teams
- `discovery_team` (wave 1): clarify goals, business constraints, and option framing | roles: product_manager
- `design_team` (wave 1): stress-test architecture and cross-cutting risks | roles: data_governance_specialist, content_creator, image_prompt_engineer
- `build_team` (wave 2): plan implementation slices and integration details | roles: social_media_strategist
- `assurance_team` (wave 3): define quality/release gates and rollback readiness | roles: evidence_collector, experiment_tracker, release_manager, analytics_reporter, legal_compliance_checker
- `roundtable_judges_team` (wave 4): score options, apply veto policy, and finalize consensus | roles: product_manager, data_governance_specialist, experiment_tracker, legal_compliance_checker
- `debate_arena_team` (wave 4): challenge finalist options through structured counter-arguments | roles: evidence_collector, release_manager, content_creator, image_prompt_engineer, social_media_strategist, analytics_reporter
- `debate_judgement_team` (wave 5): jury voting and final adjudication | roles: product_manager, data_governance_specialist, experiment_tracker, legal_compliance_checker
- `director_team` (wave 0): mission steering and escalation decisions | roles: product_manager
- `manager_data_governance_specialist_team` (wave 1): task decomposition and dependency management | roles: data_governance_specialist, evidence_collector, social_media_strategist
- `manager_content_creator_team` (wave 1): task decomposition and dependency management | roles: content_creator, experiment_tracker, analytics_reporter
- `manager_image_prompt_engineer_team` (wave 1): task decomposition and dependency management | roles: image_prompt_engineer, release_manager, legal_compliance_checker
- `dag_orchestrator_team` (wave 6): enforce node dependencies and orchestrate parallel execution windows | roles: product_manager
- `reality_gate_team` (wave 5): evidence-first QA and release readiness certification | roles: evidence_collector
### .codex/config.toml Draft
```toml
[features]
multi_agent = true

[agents]
max_threads = 14
max_depth = 2
job_max_runtime_seconds = 1800

[agents.product_manager]
description = "Swarm+roundtable sub-agent for discovery_team. Focus: scope, acceptance criteria, prioritization."
config_file = "agents/product_manager.toml"

[agents.data_governance_specialist]
description = "Swarm+roundtable sub-agent for design_team. Focus: data quality, lineage, privacy, and compliance controls."
config_file = "agents/data_governance_specialist.toml"

[agents.evidence_collector]
description = "Swarm+roundtable sub-agent for assurance_team. Focus: evidence-based QA and proof collection."
config_file = "agents/evidence_collector.toml"

[agents.experiment_tracker]
description = "Swarm+roundtable sub-agent for assurance_team. Focus: experiment lifecycle and decision discipline."
config_file = "agents/experiment_tracker.toml"

[agents.release_manager]
description = "Swarm+roundtable sub-agent for assurance_team. Focus: release train planning, rollout safety, and rollback readiness."
config_file = "agents/release_manager.toml"

[agents.content_creator]
description = "Swarm+roundtable sub-agent for design_team. Focus: editorial strategy and multi-format content production."
config_file = "agents/content_creator.toml"

[agents.image_prompt_engineer]
description = "Swarm+roundtable sub-agent for design_team. Focus: structured AI image prompt engineering for publication assets."
config_file = "agents/image_prompt_engineer.toml"

[agents.social_media_strategist]
description = "Swarm+roundtable sub-agent for build_team. Focus: cross-platform publishing strategy and campaign rhythm."
config_file = "agents/social_media_strategist.toml"

[agents.analytics_reporter]
description = "Swarm+roundtable sub-agent for assurance_team. Focus: KPI reporting, attribution, and operational insights."
config_file = "agents/analytics_reporter.toml"

[agents.legal_compliance_checker]
description = "Swarm+roundtable sub-agent for assurance_team. Focus: legal and regulatory compliance review for content and data operations."
config_file = "agents/legal_compliance_checker.toml"
```
### Role Config Files
- `agents/product_manager.toml` (gpt-5.4, reasoning=medium, sandbox=read-only)
- `agents/data_governance_specialist.toml` (gpt-5.4, reasoning=high, sandbox=read-only)
- `agents/evidence_collector.toml` (gpt-5.4, reasoning=medium, sandbox=read-only)
- `agents/experiment_tracker.toml` (gpt-5.4, reasoning=high, sandbox=read-only)
- `agents/release_manager.toml` (gpt-5.4, reasoning=medium, sandbox=read-only)
- `agents/content_creator.toml` (gpt-5.4, reasoning=medium, sandbox=read-only)
- `agents/image_prompt_engineer.toml` (gpt-5.4, reasoning=medium, sandbox=read-only)
- `agents/social_media_strategist.toml` (gpt-5.4, reasoning=medium, sandbox=inherit)
- `agents/analytics_reporter.toml` (gpt-5.4, reasoning=medium, sandbox=read-only)
- `agents/legal_compliance_checker.toml` (gpt-5.4, reasoning=high, sandbox=read-only)

## Spawn Prompts
### `product_manager`
```text
You are acting as product_manager. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: scope, acceptance criteria, prioritization
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["scope_boundaries", "acceptance_criteria", "priority_rationale"]
}
Do not produce extra sections outside JSON.
```
### `data_governance_specialist`
```text
You are acting as data_governance_specialist. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: data quality, lineage, privacy, and compliance controls
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["data_policies", "pii_controls", "compliance_checks"]
}
Do not produce extra sections outside JSON.
```
### `evidence_collector`
```text
You are acting as evidence_collector. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: evidence-based QA and proof collection
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["qa_evidence_report", "pass_fail_verdict", "defect_log"]
}
Do not produce extra sections outside JSON.
```
### `experiment_tracker`
```text
You are acting as experiment_tracker. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: experiment lifecycle and decision discipline
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["experiment_design", "experiment_results", "decision_recommendation"]
}
Do not produce extra sections outside JSON.
```
### `release_manager`
```text
You are acting as release_manager. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: release train planning, rollout safety, and rollback readiness
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["release_plan", "rollout_gates", "rollback_readiness"]
}
Do not produce extra sections outside JSON.
```
### `content_creator`
```text
You are acting as content_creator. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: editorial strategy and multi-format content production
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["editorial_calendar", "content_drafts", "content_distribution_plan"]
}
Do not produce extra sections outside JSON.
```
### `image_prompt_engineer`
```text
You are acting as image_prompt_engineer. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: structured AI image prompt engineering for publication assets
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["image_prompt_pack", "negative_prompt_pack", "style_variants"]
}
Do not produce extra sections outside JSON.
```
### `social_media_strategist`
```text
You are acting as social_media_strategist. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: cross-platform publishing strategy and campaign rhythm
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["channel_plan", "campaign_schedule", "distribution_metrics_plan"]
}
Do not produce extra sections outside JSON.
```
### `analytics_reporter`
```text
You are acting as analytics_reporter. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: KPI reporting, attribution, and operational insights
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["kpi_dashboard_spec", "attribution_summary", "optimization_recommendations"]
}
Do not produce extra sections outside JSON.
```
### `legal_compliance_checker`
```text
You are acting as legal_compliance_checker. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Context/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程
Ownership focus: legal and regulatory compliance review for content and data operations
Return exactly one JSON object:
{
  "proposal_id": "Option-X",
  "summary": "...",
  "plan": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "evidence_or_tests": ["..."],
  "role_specific_outputs": ["compliance_risks", "required_controls", "approval_or_block_decision"]
}
Do not produce extra sections outside JSON.
```

## Roundtable Prompt
```text
You are in roundtable review.
Task: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代
Input: all proposal cards from experts.
Score each option on 1-5 for criteria: impact, feasibility, risk_control, time_to_value, maintainability.
Output JSON only:
{
  "expert": "<role>",
  "scores": {
    "Option-A": {"impact": 0, "feasibility": 0, "risk_control": 0, "time_to_value": 0, "maintainability": 0}
  },
  "veto": [{"option": "Option-X", "reason": "..."}],
  "notes": "..."
}
Only use veto for severe blockers.
```

## Machine Readable JSON
```json
{
  "generated_at": "2026-03-06T11:50:46.224653+00:00",
  "task": "设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代",
  "context": "必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程",
  "task_type": "growth",
  "complexity": "high",
  "runner": "native",
  "coordinator": "product_manager",
  "experts": [
    {
      "role": "product_manager",
      "focus": "scope, acceptance criteria, prioritization",
      "expected_outputs": [
        "scope_boundaries",
        "acceptance_criteria",
        "priority_rationale"
      ],
      "origin": "template",
      "agent_type": "default"
    },
    {
      "role": "data_governance_specialist",
      "focus": "data quality, lineage, privacy, and compliance controls",
      "expected_outputs": [
        "data_policies",
        "pii_controls",
        "compliance_checks"
      ],
      "origin": "dynamic",
      "agent_type": "default",
      "trigger_hits": [
        "合规",
        "审计"
      ]
    },
    {
      "role": "evidence_collector",
      "focus": "evidence-based QA and proof collection",
      "expected_outputs": [
        "qa_evidence_report",
        "pass_fail_verdict",
        "defect_log"
      ],
      "origin": "dynamic",
      "agent_type": "default",
      "trigger_hits": [
        "证据"
      ]
    },
    {
      "role": "experiment_tracker",
      "focus": "experiment lifecycle and decision discipline",
      "expected_outputs": [
        "experiment_design",
        "experiment_results",
        "decision_recommendation"
      ],
      "origin": "dynamic",
      "agent_type": "default",
      "trigger_hits": [
        "实验"
      ]
    },
    {
      "role": "release_manager",
      "focus": "release train planning, rollout safety, and rollback readiness",
      "expected_outputs": [
        "release_plan",
        "rollout_gates",
        "rollback_readiness"
      ],
      "origin": "dynamic",
      "agent_type": "default",
      "trigger_hits": [
        "发布"
      ]
    },
    {
      "role": "content_creator",
      "focus": "editorial strategy and multi-format content production",
      "expected_outputs": [
        "editorial_calendar",
        "content_drafts",
        "content_distribution_plan"
      ],
      "origin": "template",
      "agent_type": "product_consultant"
    },
    {
      "role": "image_prompt_engineer",
      "focus": "structured AI image prompt engineering for publication assets",
      "expected_outputs": [
        "image_prompt_pack",
        "negative_prompt_pack",
        "style_variants"
      ],
      "origin": "template",
      "agent_type": "uiux_designer"
    },
    {
      "role": "social_media_strategist",
      "focus": "cross-platform publishing strategy and campaign rhythm",
      "expected_outputs": [
        "channel_plan",
        "campaign_schedule",
        "distribution_metrics_plan"
      ],
      "origin": "template",
      "agent_type": "product_consultant"
    },
    {
      "role": "analytics_reporter",
      "focus": "KPI reporting, attribution, and operational insights",
      "expected_outputs": [
        "kpi_dashboard_spec",
        "attribution_summary",
        "optimization_recommendations"
      ],
      "origin": "template",
      "agent_type": "data_analyst"
    },
    {
      "role": "legal_compliance_checker",
      "focus": "legal and regulatory compliance review for content and data operations",
      "expected_outputs": [
        "compliance_risks",
        "required_controls",
        "approval_or_block_decision"
      ],
      "origin": "template",
      "agent_type": "cto"
    }
  ],
  "collaboration_modes": {
    "primary_mode": "swarm",
    "enabled_modes": [
      "swarm",
      "hierarchical",
      "dag",
      "debate_judgement",
      "roundtable",
      "experts"
    ],
    "mode_scores": {
      "roundtable": 2,
      "experts": 4,
      "debate_judgement": 4,
      "swarm": 4,
      "hierarchical": 3,
      "dag": 2
    },
    "mode_reasons": {
      "roundtable": [
        "task_type:growth"
      ],
      "experts": [
        "base: multi-expert collaboration baseline",
        "keyword:专家",
        "task_type:growth"
      ],
      "debate_judgement": [
        "keyword:评审",
        "keyword:审查",
        "complexity:high"
      ],
      "swarm": [
        "keyword:蜂群",
        "task_type:growth",
        "complexity:high",
        "auto:top-ranked mode"
      ],
      "hierarchical": [
        "keyword:流程",
        "complexity:high"
      ],
      "dag": [
        "complexity:high"
      ]
    },
    "routing_log": [
      "swarm: keyword:蜂群; task_type:growth; complexity:high",
      "hierarchical: keyword:流程; complexity:high",
      "dag: complexity:high",
      "debate_judgement: keyword:评审; keyword:审查; complexity:high",
      "roundtable: task_type:growth",
      "experts: base: multi-expert collaboration baseline; keyword:专家; task_type:growth"
    ],
    "presets": {
      "nexus_full": [
        "swarm",
        "hierarchical",
        "dag",
        "debate_judgement",
        "experts"
      ],
      "nexus_sprint": [
        "swarm",
        "roundtable",
        "experts",
        "dag"
      ],
      "nexus_micro": [
        "roundtable",
        "experts"
      ]
    },
    "selected_preset": "nexus_full",
    "article_scenario_fit": [
      {
        "mode": "roundtable",
        "best_for": "brainstorming / 复杂推理"
      },
      {
        "mode": "experts",
        "best_for": "高质量综合分析"
      },
      {
        "mode": "debate_judgement",
        "best_for": "逻辑推理 / 审查"
      },
      {
        "mode": "swarm",
        "best_for": "大规模并行任务"
      },
      {
        "mode": "hierarchical",
        "best_for": "复杂任务管理"
      },
      {
        "mode": "dag",
        "best_for": "工程化流程"
      }
    ]
  },
  "swarm_topology": {
    "complexity": "high",
    "cells": [
      {
        "cell": "discovery_cell",
        "parallel_wave": 1,
        "goal": "clarify goals, business constraints, and option framing",
        "roles": [
          "product_manager"
        ]
      },
      {
        "cell": "design_cell",
        "parallel_wave": 1,
        "goal": "stress-test architecture and cross-cutting risks",
        "roles": [
          "data_governance_specialist",
          "content_creator",
          "image_prompt_engineer"
        ]
      },
      {
        "cell": "build_cell",
        "parallel_wave": 2,
        "goal": "plan implementation slices and integration details",
        "roles": [
          "social_media_strategist"
        ]
      },
      {
        "cell": "assurance_cell",
        "parallel_wave": 3,
        "goal": "define quality/release gates and rollback readiness",
        "roles": [
          "evidence_collector",
          "experiment_tracker",
          "release_manager",
          "analytics_reporter",
          "legal_compliance_checker"
        ]
      }
    ],
    "parallel_waves": 3
  },
  "swarm_phases": [
    {
      "phase": "phase_0_alignment",
      "goal": "lock mission boundaries, non-goals, and decision rules",
      "timebox_minutes": 10,
      "mode": "hierarchical"
    },
    {
      "phase": "phase_1_divergent_swarm",
      "goal": "multi-cell parallel exploration and deep risk surfacing",
      "timebox_minutes": 30,
      "mode": "swarm"
    },
    {
      "phase": "phase_2b_debate_judgement",
      "goal": "run structured debate and jury vote on finalists",
      "timebox_minutes": 12,
      "mode": "debate_judgement"
    },
    {
      "phase": "phase_2_roundtable_critique",
      "goal": "cross-cell challenge, scoring, and veto checks",
      "timebox_minutes": 20,
      "mode": "roundtable"
    },
    {
      "phase": "phase_3_convergent_swarm",
      "goal": "merge winner/hybrid into execution design and owners",
      "timebox_minutes": 40,
      "mode": "experts"
    },
    {
      "phase": "phase_4_hardening_gate",
      "goal": "quality/reliability/release gate review before close",
      "timebox_minutes": 20,
      "mode": "debate_judgement"
    }
  ],
  "generation_log": [
    "dynamic expert added: data_governance_specialist (hits: 合规, 审计)",
    "dynamic expert added: content_creator (hits: 内容运营, 写作)",
    "dynamic expert added: release_manager (hits: 发布)",
    "dynamic expert added: image_prompt_engineer (hits: 配图)",
    "dynamic expert added: social_media_strategist (hits: 发布)",
    "dynamic expert added: legal_compliance_checker (hits: 合规)",
    "dynamic expert added: analytics_reporter (hits: 复盘)",
    "dynamic expert added: experiment_tracker (hits: 实验)",
    "dynamic expert added: evidence_collector (hits: 证据)"
  ],
  "roundtable": {
    "criteria_weights": {
      "impact": 0.25,
      "feasibility": 0.25,
      "risk_control": 0.2,
      "time_to_value": 0.15,
      "maintainability": 0.15
    },
    "consensus_threshold": 0.67,
    "hard_veto_roles": [
      "data_governance_specialist",
      "experiment_tracker",
      "legal_compliance_checker"
    ],
    "round2_condition": "trigger if top option approval_ratio < threshold or hard veto exists",
    "adjudication_mode": "debate_judgement_jury"
  },
  "debate_judgement": {
    "enabled": true,
    "rounds": 2,
    "debaters": [
      "evidence_collector",
      "release_manager",
      "content_creator",
      "image_prompt_engineer",
      "social_media_strategist",
      "analytics_reporter"
    ],
    "jury_roles": [
      "product_manager",
      "data_governance_specialist",
      "experiment_tracker",
      "legal_compliance_checker"
    ],
    "evidence_required": true,
    "inconclusive_default": "FAIL",
    "vote_policy": {
      "method": "jury_weighted_majority",
      "jury_vote_weight": 2,
      "debaters_vote_weight": 1,
      "jury_quorum": 3,
      "tie_breaker": "product_manager"
    },
    "final_gate": {
      "judge": "reality_checker",
      "default_verdict": "NEEDS_WORK",
      "allowed_verdicts": [
        "READY",
        "NEEDS_WORK",
        "NOT_READY"
      ]
    },
    "authorization_checks": [
      "identity_valid",
      "credential_current",
      "scope_sufficient",
      "delegation_chain_valid"
    ],
    "trigger_condition": "enable when roundtable disagreement remains high, hard veto conflicts exist, or audit-style scrutiny is required",
    "output_schema": {
      "claim": "string",
      "evidence": [
        "string"
      ],
      "counter_argument": "string",
      "jury_verdict": "accept/reject/rework"
    }
  },
  "hierarchical_execution": {
    "enabled": true,
    "director": "product_manager",
    "managers": [
      "data_governance_specialist",
      "content_creator",
      "image_prompt_engineer"
    ],
    "workers": [
      "evidence_collector",
      "experiment_tracker",
      "release_manager",
      "social_media_strategist",
      "analytics_reporter",
      "legal_compliance_checker"
    ],
    "manager_assignments": [
      {
        "manager": "data_governance_specialist",
        "workers": [
          "evidence_collector",
          "social_media_strategist"
        ],
        "focus": "stress-test architecture and cross-cutting risks"
      },
      {
        "manager": "content_creator",
        "workers": [
          "experiment_tracker",
          "analytics_reporter"
        ],
        "focus": "stress-test architecture and cross-cutting risks"
      },
      {
        "manager": "image_prompt_engineer",
        "workers": [
          "release_manager",
          "legal_compliance_checker"
        ],
        "focus": "stress-test architecture and cross-cutting risks"
      }
    ],
    "escalation_chain": [
      "agents_orchestrator",
      "studio_producer",
      "product_manager"
    ],
    "delegation": {
      "require_chain": true,
      "must_include": [
        "from",
        "to",
        "scope",
        "expires_at"
      ]
    },
    "handoff_contract": {
      "director_to_manager": "mission boundaries, priorities, and completion gates",
      "manager_to_worker": "concrete tasks, expected outputs, and test/evidence requirements",
      "worker_to_manager": "execution artifacts, blockers, and verification evidence"
    }
  },
  "dag_workflow": {
    "enabled": true,
    "nodes": [
      {
        "id": "discovery_cell_wave_1",
        "kind": "swarm_cell",
        "wave": 1,
        "team_hint": "discovery_team",
        "parallelizable": true
      },
      {
        "id": "design_cell_wave_1",
        "kind": "swarm_cell",
        "wave": 1,
        "team_hint": "design_team",
        "parallelizable": true
      },
      {
        "id": "build_cell_wave_2",
        "kind": "swarm_cell",
        "wave": 2,
        "team_hint": "build_team",
        "parallelizable": true
      },
      {
        "id": "assurance_cell_wave_3",
        "kind": "swarm_cell",
        "wave": 3,
        "team_hint": "assurance_team",
        "parallelizable": true
      },
      {
        "id": "alignment_gate",
        "kind": "gate",
        "wave": 0,
        "team_hint": "director_team",
        "parallelizable": false
      },
      {
        "id": "roundtable_critique",
        "kind": "decision_gate",
        "wave": 4,
        "team_hint": "roundtable_judges_team",
        "parallelizable": false
      },
      {
        "id": "debate_judgement",
        "kind": "decision_gate",
        "wave": 5,
        "team_hint": "debate_judgement_team",
        "parallelizable": false
      },
      {
        "id": "convergent_execution",
        "kind": "execution",
        "wave": 6,
        "team_hint": "delivery_team",
        "parallelizable": false
      },
      {
        "id": "hardening_gate",
        "kind": "gate",
        "wave": 7,
        "team_hint": "roundtable_judges_team",
        "parallelizable": false
      }
    ],
    "edges": [
      {
        "from": "alignment_gate",
        "to": "discovery_cell_wave_1"
      },
      {
        "from": "alignment_gate",
        "to": "design_cell_wave_1"
      },
      {
        "from": "discovery_cell_wave_1",
        "to": "build_cell_wave_2"
      },
      {
        "from": "design_cell_wave_1",
        "to": "build_cell_wave_2"
      },
      {
        "from": "build_cell_wave_2",
        "to": "assurance_cell_wave_3"
      },
      {
        "from": "assurance_cell_wave_3",
        "to": "roundtable_critique"
      },
      {
        "from": "roundtable_critique",
        "to": "debate_judgement"
      },
      {
        "from": "debate_judgement",
        "to": "convergent_execution"
      },
      {
        "from": "convergent_execution",
        "to": "hardening_gate"
      }
    ],
    "parallel_groups": [
      [
        "discovery_cell_wave_1",
        "design_cell_wave_1"
      ]
    ],
    "critical_path": [
      "alignment_gate",
      "discovery_cell_wave_1",
      "build_cell_wave_2",
      "assurance_cell_wave_3",
      "roundtable_critique",
      "debate_judgement",
      "convergent_execution",
      "hardening_gate"
    ],
    "max_parallel_nodes": 2,
    "gates": {
      "required": true
    },
    "parallel_join_policy": "barrier",
    "dependency_policy": {
      "start_condition": "upstream.qa==PASS",
      "merge_order": "dependency_order",
      "allow_independent_parallel": true
    },
    "loops": {
      "dev_qa": {
        "max_retries": 3,
        "on_exhausted": "escalate"
      }
    }
  },
  "output_format": {
    "version": "1.1.0",
    "goal": "deterministic, auditable, and readable outputs for multi-agent collaboration",
    "global_rules": [
      "facts_assumptions_risks_must_be_explicit",
      "all_decisions_require_evidence_or_test_reference",
      "handoff_payload_is_mandatory_for_cross-agent_edges",
      "timestamp_in_iso8601_utc"
    ],
    "document_layout": [
      "01_summary",
      "02_task_context",
      "03_collaboration_routing",
      "04_execution_plan",
      "05_quality_and_risk_gates",
      "06_next_actions",
      "07_machine_readable_json"
    ],
    "templates": {
      "handoff": {
        "required_sections": [
          "metadata",
          "context",
          "deliverable_request",
          "quality_expectations"
        ],
        "required_fields": [
          "from",
          "to",
          "phase",
          "task_reference",
          "priority",
          "timestamp"
        ]
      },
      "pipeline_status": {
        "required_fields": [
          "current_phase",
          "tasks_total",
          "tasks_completed",
          "qa_pass_rate",
          "blocked_tasks",
          "pipeline_health",
          "next_action"
        ],
        "pipeline_health_enum": [
          "ON_TRACK",
          "AT_RISK",
          "BLOCKED"
        ]
      },
      "qa_verdict": {
        "required_fields": [
          "task_id",
          "attempt",
          "verdict",
          "evidence",
          "issues",
          "fix_instructions"
        ],
        "verdict_enum": [
          "PASS",
          "FAIL",
          "NEEDS_WORK"
        ]
      },
      "decision_log": {
        "required_fields": [
          "decision_id",
          "options_compared",
          "scores",
          "vetoes",
          "final_decision",
          "owner",
          "timestamp"
        ]
      }
    },
    "rendering": {
      "bullet_style": "flat",
      "table_preferred_for_scorecards": true,
      "top_n_list_limit": 7,
      "include_mode_badges": [
        "swarm",
        "hierarchical",
        "dag",
        "debate_judgement",
        "roundtable",
        "experts"
      ]
    }
  },
  "spawn_prompts": [
    {
      "role": "product_manager",
      "agent_type": "default",
      "origin": "template",
      "prompt": "You are acting as product_manager. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: scope, acceptance criteria, prioritization\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"scope_boundaries\", \"acceptance_criteria\", \"priority_rationale\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "data_governance_specialist",
      "agent_type": "default",
      "origin": "dynamic",
      "prompt": "You are acting as data_governance_specialist. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: data quality, lineage, privacy, and compliance controls\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"data_policies\", \"pii_controls\", \"compliance_checks\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "evidence_collector",
      "agent_type": "default",
      "origin": "dynamic",
      "prompt": "You are acting as evidence_collector. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: evidence-based QA and proof collection\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"qa_evidence_report\", \"pass_fail_verdict\", \"defect_log\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "experiment_tracker",
      "agent_type": "default",
      "origin": "dynamic",
      "prompt": "You are acting as experiment_tracker. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: experiment lifecycle and decision discipline\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"experiment_design\", \"experiment_results\", \"decision_recommendation\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "release_manager",
      "agent_type": "default",
      "origin": "dynamic",
      "prompt": "You are acting as release_manager. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: release train planning, rollout safety, and rollback readiness\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"release_plan\", \"rollout_gates\", \"rollback_readiness\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "content_creator",
      "agent_type": "product_consultant",
      "origin": "template",
      "prompt": "You are acting as content_creator. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: editorial strategy and multi-format content production\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"editorial_calendar\", \"content_drafts\", \"content_distribution_plan\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "image_prompt_engineer",
      "agent_type": "uiux_designer",
      "origin": "template",
      "prompt": "You are acting as image_prompt_engineer. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: structured AI image prompt engineering for publication assets\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"image_prompt_pack\", \"negative_prompt_pack\", \"style_variants\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "social_media_strategist",
      "agent_type": "product_consultant",
      "origin": "template",
      "prompt": "You are acting as social_media_strategist. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: cross-platform publishing strategy and campaign rhythm\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"channel_plan\", \"campaign_schedule\", \"distribution_metrics_plan\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "analytics_reporter",
      "agent_type": "data_analyst",
      "origin": "template",
      "prompt": "You are acting as analytics_reporter. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: KPI reporting, attribution, and operational insights\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"kpi_dashboard_spec\", \"attribution_summary\", \"optimization_recommendations\"]\n}\nDo not produce extra sections outside JSON."
    },
    {
      "role": "legal_compliance_checker",
      "agent_type": "cto",
      "origin": "template",
      "prompt": "You are acting as legal_compliance_checker. Mission: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nContext/constraints: 必须使用Codex agent teams + sub-agents，支持动态专家和动态蜂群，要求证据化评审与可审计流程\nOwnership focus: legal and regulatory compliance review for content and data operations\nReturn exactly one JSON object:\n{\n  \"proposal_id\": \"Option-X\",\n  \"summary\": \"...\",\n  \"plan\": [\"...\"],\n  \"risks\": [\"...\"],\n  \"assumptions\": [\"...\"],\n  \"evidence_or_tests\": [\"...\"],\n  \"role_specific_outputs\": [\"compliance_risks\", \"required_controls\", \"approval_or_block_decision\"]\n}\nDo not produce extra sections outside JSON."
    }
  ],
  "roundtable_prompt": "You are in roundtable review.\nTask: 设计一个AI自动化运营系统：选题、写作、配图、自动发布、合规审查、数据复盘、实验迭代\nInput: all proposal cards from experts.\nScore each option on 1-5 for criteria: impact, feasibility, risk_control, time_to_value, maintainability.\nOutput JSON only:\n{\n  \"expert\": \"<role>\",\n  \"scores\": {\n    \"Option-A\": {\"impact\": 0, \"feasibility\": 0, \"risk_control\": 0, \"time_to_value\": 0, \"maintainability\": 0}\n  },\n  \"veto\": [{\"option\": \"Option-X\", \"reason\": \"...\"}],\n  \"notes\": \"...\"\n}\nOnly use veto for severe blockers.",
  "codex_multi_agent": {
    "sub_agent_runtime": {
      "max_threads": 14,
      "max_depth": 2,
      "job_max_runtime_seconds": 1800,
      "feature_flag_enabled": true,
      "mode_aware_autoscaling": true
    },
    "agent_teams": [
      {
        "team": "discovery_team",
        "wave": 1,
        "goal": "clarify goals, business constraints, and option framing",
        "roles": [
          "product_manager"
        ]
      },
      {
        "team": "design_team",
        "wave": 1,
        "goal": "stress-test architecture and cross-cutting risks",
        "roles": [
          "data_governance_specialist",
          "content_creator",
          "image_prompt_engineer"
        ]
      },
      {
        "team": "build_team",
        "wave": 2,
        "goal": "plan implementation slices and integration details",
        "roles": [
          "social_media_strategist"
        ]
      },
      {
        "team": "assurance_team",
        "wave": 3,
        "goal": "define quality/release gates and rollback readiness",
        "roles": [
          "evidence_collector",
          "experiment_tracker",
          "release_manager",
          "analytics_reporter",
          "legal_compliance_checker"
        ]
      },
      {
        "team": "roundtable_judges_team",
        "wave": 4,
        "goal": "score options, apply veto policy, and finalize consensus",
        "roles": [
          "product_manager",
          "data_governance_specialist",
          "experiment_tracker",
          "legal_compliance_checker"
        ]
      },
      {
        "team": "debate_arena_team",
        "wave": 4,
        "goal": "challenge finalist options through structured counter-arguments",
        "roles": [
          "evidence_collector",
          "release_manager",
          "content_creator",
          "image_prompt_engineer",
          "social_media_strategist",
          "analytics_reporter"
        ]
      },
      {
        "team": "debate_judgement_team",
        "wave": 5,
        "goal": "jury voting and final adjudication",
        "roles": [
          "product_manager",
          "data_governance_specialist",
          "experiment_tracker",
          "legal_compliance_checker"
        ]
      },
      {
        "team": "director_team",
        "wave": 0,
        "goal": "mission steering and escalation decisions",
        "roles": [
          "product_manager"
        ]
      },
      {
        "team": "manager_data_governance_specialist_team",
        "wave": 1,
        "goal": "task decomposition and dependency management",
        "roles": [
          "data_governance_specialist",
          "evidence_collector",
          "social_media_strategist"
        ]
      },
      {
        "team": "manager_content_creator_team",
        "wave": 1,
        "goal": "task decomposition and dependency management",
        "roles": [
          "content_creator",
          "experiment_tracker",
          "analytics_reporter"
        ]
      },
      {
        "team": "manager_image_prompt_engineer_team",
        "wave": 1,
        "goal": "task decomposition and dependency management",
        "roles": [
          "image_prompt_engineer",
          "release_manager",
          "legal_compliance_checker"
        ]
      },
      {
        "team": "dag_orchestrator_team",
        "wave": 6,
        "goal": "enforce node dependencies and orchestrate parallel execution windows",
        "roles": [
          "product_manager"
        ]
      },
      {
        "team": "reality_gate_team",
        "wave": 5,
        "goal": "evidence-first QA and release readiness certification",
        "roles": [
          "evidence_collector"
        ]
      }
    ],
    "role_configs": [
      {
        "role": "product_manager",
        "team": "discovery_team",
        "description": "Swarm+roundtable sub-agent for discovery_team. Focus: scope, acceptance criteria, prioritization.",
        "config_file": "agents/product_manager.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "medium",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"medium\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `product_manager` sub-agent in swarm + roundtable mode.\nPrimary team: discovery_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: director.\nOwnership focus: scope, acceptance criteria, prioritization.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\nYou are part of the jury in debate mode and must issue a clear verdict.\n\"\"\"\n"
      },
      {
        "role": "data_governance_specialist",
        "team": "design_team",
        "description": "Swarm+roundtable sub-agent for design_team. Focus: data quality, lineage, privacy, and compliance controls.",
        "config_file": "agents/data_governance_specialist.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "high",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"high\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `data_governance_specialist` sub-agent in swarm + roundtable mode.\nPrimary team: design_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: manager.\nOwnership focus: data quality, lineage, privacy, and compliance controls.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\nYou are a hard-veto reviewer for safety/reliability gates and must block unsafe proposals.\nYou are part of the jury in debate mode and must issue a clear verdict.\n\"\"\"\n"
      },
      {
        "role": "evidence_collector",
        "team": "assurance_team",
        "description": "Swarm+roundtable sub-agent for assurance_team. Focus: evidence-based QA and proof collection.",
        "config_file": "agents/evidence_collector.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "medium",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"medium\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `evidence_collector` sub-agent in swarm + roundtable mode.\nPrimary team: assurance_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: worker.\nOwnership focus: evidence-based QA and proof collection.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\n\"\"\"\n"
      },
      {
        "role": "experiment_tracker",
        "team": "assurance_team",
        "description": "Swarm+roundtable sub-agent for assurance_team. Focus: experiment lifecycle and decision discipline.",
        "config_file": "agents/experiment_tracker.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "high",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"high\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `experiment_tracker` sub-agent in swarm + roundtable mode.\nPrimary team: assurance_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: worker.\nOwnership focus: experiment lifecycle and decision discipline.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\nYou are a hard-veto reviewer for safety/reliability gates and must block unsafe proposals.\nYou are part of the jury in debate mode and must issue a clear verdict.\n\"\"\"\n"
      },
      {
        "role": "release_manager",
        "team": "assurance_team",
        "description": "Swarm+roundtable sub-agent for assurance_team. Focus: release train planning, rollout safety, and rollback readiness.",
        "config_file": "agents/release_manager.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "medium",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"medium\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `release_manager` sub-agent in swarm + roundtable mode.\nPrimary team: assurance_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: worker.\nOwnership focus: release train planning, rollout safety, and rollback readiness.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\n\"\"\"\n"
      },
      {
        "role": "content_creator",
        "team": "design_team",
        "description": "Swarm+roundtable sub-agent for design_team. Focus: editorial strategy and multi-format content production.",
        "config_file": "agents/content_creator.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "medium",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"medium\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `content_creator` sub-agent in swarm + roundtable mode.\nPrimary team: design_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: manager.\nOwnership focus: editorial strategy and multi-format content production.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\n\"\"\"\n"
      },
      {
        "role": "image_prompt_engineer",
        "team": "design_team",
        "description": "Swarm+roundtable sub-agent for design_team. Focus: structured AI image prompt engineering for publication assets.",
        "config_file": "agents/image_prompt_engineer.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "medium",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"medium\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `image_prompt_engineer` sub-agent in swarm + roundtable mode.\nPrimary team: design_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: manager.\nOwnership focus: structured AI image prompt engineering for publication assets.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\n\"\"\"\n"
      },
      {
        "role": "social_media_strategist",
        "team": "build_team",
        "description": "Swarm+roundtable sub-agent for build_team. Focus: cross-platform publishing strategy and campaign rhythm.",
        "config_file": "agents/social_media_strategist.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "medium",
        "sandbox_mode": "inherit",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"medium\"\ndeveloper_instructions = \"\"\"\nYou are the `social_media_strategist` sub-agent in swarm + roundtable mode.\nPrimary team: build_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: worker.\nOwnership focus: cross-platform publishing strategy and campaign rhythm.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\n\"\"\"\n"
      },
      {
        "role": "analytics_reporter",
        "team": "assurance_team",
        "description": "Swarm+roundtable sub-agent for assurance_team. Focus: KPI reporting, attribution, and operational insights.",
        "config_file": "agents/analytics_reporter.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "medium",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"medium\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `analytics_reporter` sub-agent in swarm + roundtable mode.\nPrimary team: assurance_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: worker.\nOwnership focus: KPI reporting, attribution, and operational insights.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\n\"\"\"\n"
      },
      {
        "role": "legal_compliance_checker",
        "team": "assurance_team",
        "description": "Swarm+roundtable sub-agent for assurance_team. Focus: legal and regulatory compliance review for content and data operations.",
        "config_file": "agents/legal_compliance_checker.toml",
        "model": "gpt-5.4",
        "model_reasoning_effort": "high",
        "sandbox_mode": "read-only",
        "content": "model = \"gpt-5.4\"\nmodel_reasoning_effort = \"high\"\nsandbox_mode = \"read-only\"\ndeveloper_instructions = \"\"\"\nYou are the `legal_compliance_checker` sub-agent in swarm + roundtable mode.\nPrimary team: assurance_team.\nEnabled collaboration modes: swarm, hierarchical, dag, debate_judgement, roundtable, experts.\nHierarchy role: worker.\nOwnership focus: legal and regulatory compliance review for content and data operations.\nOutput must be concise, structured, and evidence-backed.\nStay within your ownership boundary and avoid rewriting other roles.\nTag uncertain statements as assumptions.\nYou are a hard-veto reviewer for safety/reliability gates and must block unsafe proposals.\nYou are part of the jury in debate mode and must issue a clear verdict.\n\"\"\"\n"
      }
    ],
    "config_toml": "[features]\nmulti_agent = true\n\n[agents]\nmax_threads = 14\nmax_depth = 2\njob_max_runtime_seconds = 1800\n\n[agents.product_manager]\ndescription = \"Swarm+roundtable sub-agent for discovery_team. Focus: scope, acceptance criteria, prioritization.\"\nconfig_file = \"agents/product_manager.toml\"\n\n[agents.data_governance_specialist]\ndescription = \"Swarm+roundtable sub-agent for design_team. Focus: data quality, lineage, privacy, and compliance controls.\"\nconfig_file = \"agents/data_governance_specialist.toml\"\n\n[agents.evidence_collector]\ndescription = \"Swarm+roundtable sub-agent for assurance_team. Focus: evidence-based QA and proof collection.\"\nconfig_file = \"agents/evidence_collector.toml\"\n\n[agents.experiment_tracker]\ndescription = \"Swarm+roundtable sub-agent for assurance_team. Focus: experiment lifecycle and decision discipline.\"\nconfig_file = \"agents/experiment_tracker.toml\"\n\n[agents.release_manager]\ndescription = \"Swarm+roundtable sub-agent for assurance_team. Focus: release train planning, rollout safety, and rollback readiness.\"\nconfig_file = \"agents/release_manager.toml\"\n\n[agents.content_creator]\ndescription = \"Swarm+roundtable sub-agent for design_team. Focus: editorial strategy and multi-format content production.\"\nconfig_file = \"agents/content_creator.toml\"\n\n[agents.image_prompt_engineer]\ndescription = \"Swarm+roundtable sub-agent for design_team. Focus: structured AI image prompt engineering for publication assets.\"\nconfig_file = \"agents/image_prompt_engineer.toml\"\n\n[agents.social_media_strategist]\ndescription = \"Swarm+roundtable sub-agent for build_team. Focus: cross-platform publishing strategy and campaign rhythm.\"\nconfig_file = \"agents/social_media_strategist.toml\"\n\n[agents.analytics_reporter]\ndescription = \"Swarm+roundtable sub-agent for assurance_team. Focus: KPI reporting, attribution, and operational insights.\"\nconfig_file = \"agents/analytics_reporter.toml\"\n\n[agents.legal_compliance_checker]\ndescription = \"Swarm+roundtable sub-agent for assurance_team. Focus: legal and regulatory compliance review for content and data operations.\"\nconfig_file = \"agents/legal_compliance_checker.toml\"\n"
  }
}
```

