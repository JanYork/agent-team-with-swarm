#!/usr/bin/env python3
"""
Build a practical swarm + roundtable orchestration plan.
"""

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List


KNOWN_AGENT_TYPES = {
    "product_manager",
    "product_consultant",
    "uiux_designer",
    "experience_designer",
    "software_architect",
    "cto",
    "tech_lead",
    "frontend_engineer",
    "backend_engineer",
    "fullstack_engineer",
    "qa_engineer",
    "devops_engineer",
    "data_analyst",
}

ROLE_AGENT_TYPE_OVERRIDES: Dict[str, str] = {
    "agents_orchestrator": "tech_lead",
    "trend_researcher": "product_consultant",
    "feedback_synthesizer": "product_manager",
    "content_creator": "product_consultant",
    "visual_storyteller": "uiux_designer",
    "image_prompt_engineer": "uiux_designer",
    "social_media_strategist": "product_consultant",
    "report_distribution_agent": "backend_engineer",
    "legal_compliance_checker": "cto",
    "brand_guardian": "experience_designer",
    "analytics_reporter": "data_analyst",
    "experiment_tracker": "data_analyst",
    "evidence_collector": "qa_engineer",
    "reality_checker": "qa_engineer",
}


ROLE_LIBRARY: Dict[str, Dict[str, Any]] = {
    "product_manager": {
        "focus": "scope, acceptance criteria, prioritization",
        "default_outputs": ["scope_boundaries", "acceptance_criteria", "priority_rationale"],
    },
    "product_consultant": {
        "focus": "business model, hypothesis, opportunity sizing",
        "default_outputs": ["hypothesis", "business_impact", "go_to_market_risks"],
    },
    "uiux_designer": {
        "focus": "user flow, interaction states, UX edge cases",
        "default_outputs": ["flow_spec", "state_matrix", "handoff_notes"],
    },
    "experience_designer": {
        "focus": "end-to-end journey and cross-touchpoint friction",
        "default_outputs": ["journey_map", "friction_points", "service_blueprint_notes"],
    },
    "software_architect": {
        "focus": "system boundaries, reliability, security, tradeoffs",
        "default_outputs": ["architecture_options", "recommended_design", "api_contract_impacts"],
    },
    "cto": {
        "focus": "target-state strategy and risk-budget constraints",
        "default_outputs": ["target_state", "investment_tradeoffs", "risk_budget"],
    },
    "tech_lead": {
        "focus": "execution slicing, ownership, delivery quality",
        "default_outputs": ["execution_slices", "owner_map", "quality_gates"],
    },
    "frontend_engineer": {
        "focus": "UI implementation and browser/runtime behavior",
        "default_outputs": ["component_plan", "state_flow", "frontend_test_strategy"],
    },
    "backend_engineer": {
        "focus": "service/API and data/reliability design",
        "default_outputs": ["api_plan", "data_contracts", "reliability_controls"],
    },
    "fullstack_engineer": {
        "focus": "cross-layer delivery with integration risks",
        "default_outputs": ["end_to_end_plan", "integration_points", "release_slices"],
    },
    "qa_engineer": {
        "focus": "test matrix, release risk, go/no-go criteria",
        "default_outputs": ["test_matrix", "defect_risk_rank", "release_gate"],
    },
    "devops_engineer": {
        "focus": "CI/CD, rollout, observability, rollback",
        "default_outputs": ["deployment_plan", "rollback_plan", "observability_checks"],
    },
    "data_analyst": {
        "focus": "measurement design and analysis quality",
        "default_outputs": ["metric_definitions", "analysis_plan", "monitoring_signals"],
    },
    "agents_orchestrator": {
        "focus": "end-to-end multi-agent orchestration, phase gates, and retry policy",
        "default_outputs": ["pipeline_status_report", "handoff_decisions", "escalation_actions"],
    },
    "trend_researcher": {
        "focus": "market trend discovery and opportunity framing",
        "default_outputs": ["trend_brief", "opportunity_assessment", "signal_map"],
    },
    "feedback_synthesizer": {
        "focus": "user feedback synthesis and product signal prioritization",
        "default_outputs": ["feedback_clusters", "priority_backlog_signals", "voice_of_customer_summary"],
    },
    "content_creator": {
        "focus": "editorial strategy and multi-format content production",
        "default_outputs": ["editorial_calendar", "content_drafts", "content_distribution_plan"],
    },
    "visual_storyteller": {
        "focus": "visual narrative design and multimedia story consistency",
        "default_outputs": ["storyboard", "visual_narrative_spec", "asset_guidelines"],
    },
    "image_prompt_engineer": {
        "focus": "structured AI image prompt engineering for publication assets",
        "default_outputs": ["image_prompt_pack", "negative_prompt_pack", "style_variants"],
    },
    "social_media_strategist": {
        "focus": "cross-platform publishing strategy and campaign rhythm",
        "default_outputs": ["channel_plan", "campaign_schedule", "distribution_metrics_plan"],
    },
    "report_distribution_agent": {
        "focus": "automated distribution scheduling and delivery audit trails",
        "default_outputs": ["distribution_schedule", "delivery_log", "delivery_exceptions"],
    },
    "legal_compliance_checker": {
        "focus": "legal and regulatory compliance review for content and data operations",
        "default_outputs": ["compliance_risks", "required_controls", "approval_or_block_decision"],
    },
    "brand_guardian": {
        "focus": "brand consistency and message governance",
        "default_outputs": ["brand_compliance_report", "voice_guidelines", "message_adjustments"],
    },
    "analytics_reporter": {
        "focus": "KPI reporting, attribution, and operational insights",
        "default_outputs": ["kpi_dashboard_spec", "attribution_summary", "optimization_recommendations"],
    },
    "experiment_tracker": {
        "focus": "experiment tracking, statistical validation, and go/no-go recommendation",
        "default_outputs": ["experiment_design", "experiment_results", "decision_recommendation"],
    },
    "evidence_collector": {
        "focus": "evidence-first QA verification with screenshot/test artifacts",
        "default_outputs": ["qa_evidence_report", "pass_fail_verdict", "defect_log"],
    },
    "reality_checker": {
        "focus": "final reality-based readiness judgement and anti-fantasy gate",
        "default_outputs": ["integration_readiness_report", "release_blockers", "deployment_verdict"],
    },
}


DYNAMIC_EXPERT_CATALOG: List[Dict[str, Any]] = [
    {
        "role": "security_reviewer",
        "focus": "security architecture, threat exposure, and abuse resistance",
        "default_outputs": ["threat_model", "security_controls", "residual_risks"],
        "triggers": ["security", "auth", "permission", "abuse", "zero trust", "安全", "鉴权", "权限"],
    },
    {
        "role": "performance_engineer",
        "focus": "latency, throughput, and system bottleneck control",
        "default_outputs": ["perf_budget", "hot_path_optimizations", "load_test_plan"],
        "triggers": ["performance", "latency", "throughput", "benchmark", "性能", "延迟", "吞吐"],
    },
    {
        "role": "reliability_engineer",
        "focus": "failure modes, SLO design, and fault tolerance",
        "default_outputs": ["failure_modes", "slo_targets", "recovery_playbook"],
        "triggers": ["reliability", "slo", "sla", "resilience", "fault", "稳定性", "容灾", "可靠性"],
    },
    {
        "role": "integration_specialist",
        "focus": "cross-system contract compatibility and integration sequencing",
        "default_outputs": ["integration_map", "dependency_risks", "compatibility_matrix"],
        "triggers": ["integration", "third-party", "contract", "api gateway", "对接", "集成", "接口兼容"],
    },
    {
        "role": "cost_optimizer",
        "focus": "cost efficiency and budget-aware architecture tradeoffs",
        "default_outputs": ["cost_drivers", "optimization_actions", "budget_guardrails"],
        "triggers": ["cost", "budget", "finops", "成本", "预算", "降本"],
    },
    {
        "role": "data_governance_specialist",
        "focus": "data quality, lineage, privacy, and compliance controls",
        "default_outputs": ["data_policies", "pii_controls", "compliance_checks"],
        "triggers": ["data governance", "privacy", "gdpr", "pii", "audit", "数据治理", "隐私", "合规", "审计"],
    },
    {
        "role": "release_manager",
        "focus": "release train planning, rollout safety, and rollback readiness",
        "default_outputs": ["release_plan", "rollout_gates", "rollback_readiness"],
        "triggers": ["release", "rollout", "deploy", "上线", "发布", "灰度"],
    },
    {
        "role": "domain_specialist",
        "focus": "domain-specific constraints and edge-case rules",
        "default_outputs": ["domain_constraints", "domain_risks", "regulatory_or_business_rules"],
        "triggers": ["finance", "medical", "health", "legal", "game", "education", "金融", "医疗", "法律", "教育"],
    },
    {
        "role": "agents_orchestrator",
        "focus": "end-to-end orchestration, handoffs, and quality gates",
        "default_outputs": ["pipeline_status_report", "handoff_decisions", "escalation_actions"],
        "triggers": ["orchestrator", "multi-agent", "pipeline", "编排", "多agent", "多代理", "流程编排"],
    },
    {
        "role": "content_creator",
        "focus": "multi-platform content strategy and draft production",
        "default_outputs": ["editorial_calendar", "content_drafts", "content_distribution_plan"],
        "triggers": ["content", "article", "copywriting", "writing", "写作", "文章", "内容运营"],
    },
    {
        "role": "image_prompt_engineer",
        "focus": "ai-generated image prompt quality and consistency",
        "default_outputs": ["image_prompt_pack", "negative_prompt_pack", "style_variants"],
        "triggers": ["image", "prompt", "midjourney", "dall-e", "配图", "图片", "图像生成"],
    },
    {
        "role": "social_media_strategist",
        "focus": "distribution strategy across social channels",
        "default_outputs": ["channel_plan", "campaign_schedule", "distribution_metrics_plan"],
        "triggers": ["distribution", "channel", "campaign", "social", "发布", "投放", "传播"],
    },
    {
        "role": "legal_compliance_checker",
        "focus": "compliance checks for legal, privacy, and platform rules",
        "default_outputs": ["compliance_risks", "required_controls", "approval_or_block_decision"],
        "triggers": ["compliance", "gdpr", "privacy", "policy", "合规", "隐私", "监管", "法律风险"],
    },
    {
        "role": "analytics_reporter",
        "focus": "analytics and reporting for performance loops",
        "default_outputs": ["kpi_dashboard_spec", "attribution_summary", "optimization_recommendations"],
        "triggers": ["analytics", "report", "attribution", "roi", "复盘", "数据分析", "归因"],
    },
    {
        "role": "experiment_tracker",
        "focus": "experiment lifecycle and decision discipline",
        "default_outputs": ["experiment_design", "experiment_results", "decision_recommendation"],
        "triggers": ["experiment", "ab test", "hypothesis", "实验", "A/B", "验证"],
    },
    {
        "role": "evidence_collector",
        "focus": "evidence-based QA and proof collection",
        "default_outputs": ["qa_evidence_report", "pass_fail_verdict", "defect_log"],
        "triggers": ["evidence", "screenshot", "qa", "proof", "证据", "截图", "验收"],
    },
    {
        "role": "reality_checker",
        "focus": "final reality-based integration gate",
        "default_outputs": ["integration_readiness_report", "release_blockers", "deployment_verdict"],
        "triggers": ["integration", "readiness", "production", "上线门禁", "集成验收", "发布评审"],
    },
]


TASK_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "feature": {
        "coordinator": "tech_lead",
        "experts": [
            "product_manager",
            "software_architect",
            "frontend_engineer",
            "backend_engineer",
            "qa_engineer",
        ],
    },
    "incident": {
        "coordinator": "tech_lead",
        "experts": [
            "backend_engineer",
            "devops_engineer",
            "qa_engineer",
            "data_analyst",
        ],
    },
    "architecture": {
        "coordinator": "software_architect",
        "experts": [
            "cto",
            "tech_lead",
            "backend_engineer",
            "devops_engineer",
            "qa_engineer",
        ],
    },
    "research": {
        "coordinator": "product_consultant",
        "experts": [
            "trend_researcher",
            "feedback_synthesizer",
            "software_architect",
            "tech_lead",
        ],
    },
    "growth": {
        "coordinator": "product_manager",
        "experts": [
            "content_creator",
            "social_media_strategist",
            "image_prompt_engineer",
            "analytics_reporter",
            "legal_compliance_checker",
        ],
    },
    "generic": {
        "coordinator": "tech_lead",
        "experts": [
            "software_architect",
            "backend_engineer",
            "frontend_engineer",
            "qa_engineer",
        ],
    },
}


DEFAULT_CRITERIA_WEIGHTS: Dict[str, float] = {
    "impact": 0.25,
    "feasibility": 0.25,
    "risk_control": 0.20,
    "time_to_value": 0.15,
    "maintainability": 0.15,
}


SYMPHONY_DEFAULT_ACTIVE_STATES = ["Todo", "In Progress", "Rework", "Merging"]
SYMPHONY_DEFAULT_TERMINAL_STATES = ["Closed", "Cancelled", "Canceled", "Duplicate", "Done"]
SYMPHONY_DEFAULT_CODEX_COMMAND = "codex app-server"
CODEX_DEFAULT_MODEL = "gpt-5.4"
ROUNDTABLE_MIN_EXPERTS = 3
ROUNDTABLE_MAX_EXPERTS = 10


COMPLEXITY_KEYWORDS = {
    "high": [
        "migration",
        "re-architecture",
        "distributed",
        "multi-region",
        "high availability",
        "compliance",
        "incident",
        "architecture",
        "迁移",
        "分布式",
        "多地域",
        "高可用",
        "合规",
        "故障",
        "架构",
    ],
    "medium": [
        "integration",
        "performance",
        "security",
        "rollout",
        "cross-team",
        "api",
        "集成",
        "性能",
        "安全",
        "发布",
        "跨团队",
        "接口",
    ],
}


CELL_GOALS = {
    "discovery": "clarify goals, business constraints, and option framing",
    "design": "stress-test architecture and cross-cutting risks",
    "build": "plan implementation slices and integration details",
    "assurance": "define quality/release gates and rollback readiness",
    "orchestration": "coordinate priorities, sequencing, and decision cadence",
}


INFER_KEYWORDS = {
    "incident": [
        "incident",
        "sev",
        "outage",
        "latency",
        "rollback",
        "故障",
        "事故",
        "告警",
        "应急",
        "回滚",
    ],
    "architecture": [
        "architecture",
        "scalability",
        "migration",
        "platform",
        "infra",
        "架构",
        "扩展性",
        "迁移",
        "平台升级",
    ],
    "research": [
        "research",
        "investigate",
        "benchmark",
        "study",
        "调研",
        "研究",
        "对比",
        "探索",
    ],
    "growth": [
        "growth",
        "conversion",
        "retention",
        "funnel",
        "a/b",
        "marketing",
        "campaign",
        "content",
        "social",
        "增长",
        "转化",
        "留存",
        "实验",
        "运营",
        "内容",
        "投放",
    ],
    "feature": [
        "feature",
        "product",
        "launch",
        "api",
        "ui",
        "implement",
        "build",
        "需求",
        "功能",
        "上线",
        "版本",
        "实现",
        "开发",
        "落地",
    ],
}


COLLABORATION_MODE_CATALOG: Dict[str, Dict[str, str]] = {
    "roundtable": {
        "label": "RoundTable / GroupChat",
        "summary": "Peer discussion to converge from multiple viewpoints.",
        "best_for": "brainstorming / complex reasoning",
    },
    "experts": {
        "label": "Mixture of Experts / Agents",
        "summary": "Parallel specialist analysis then synthesis.",
        "best_for": "high-quality integrated analysis",
    },
    "debate_judgement": {
        "label": "Council / Jury",
        "summary": "Structured debate with explicit judging/voting.",
        "best_for": "logical reasoning / review and audit",
    },
    "swarm": {
        "label": "Swarm Intelligence",
        "summary": "Large-scale distributed execution with local ownership.",
        "best_for": "massive parallel task execution",
    },
    "hierarchical": {
        "label": "Hierarchical Agent",
        "summary": "Director-manager-worker decomposition for complex delivery.",
        "best_for": "complex task management",
    },
    "dag": {
        "label": "DAG Workflow",
        "summary": "Dependency-aware graph orchestration with parallel nodes.",
        "best_for": "engineering process automation",
    },
}


MODE_ROUTING_KEYWORDS: Dict[str, List[str]] = {
    "roundtable": [
        "brainstorm",
        "ideation",
        "hypothesis",
        "tradeoff",
        "头脑风暴",
        "多方案",
        "复杂推理",
    ],
    "experts": [
        "expert",
        "specialist",
        "analysis",
        "cross-functional",
        "专家",
        "会诊",
        "综合分析",
    ],
    "debate_judgement": [
        "debate",
        "review",
        "audit",
        "judge",
        "argue",
        "辩论",
        "评审",
        "审查",
        "裁决",
        "投票",
    ],
    "swarm": [
        "parallel",
        "batch",
        "high volume",
        "scale",
        "swarm",
        "并行",
        "批量",
        "高并发",
        "大规模",
        "蜂群",
    ],
    "hierarchical": [
        "manager",
        "director",
        "coordination",
        "decompose",
        "流程",
        "分层",
        "拆分任务",
        "管理复杂任务",
    ],
    "dag": [
        "dag",
        "workflow",
        "dependency",
        "pipeline",
        "graph",
        "工作流",
        "依赖",
        "节点",
        "编排",
    ],
}


MODE_PRIORITY_ORDER = [
    "swarm",
    "hierarchical",
    "dag",
    "debate_judgement",
    "roundtable",
    "experts",
]


ARTICLE_SCENARIO_FIT = [
    {"mode": "roundtable", "best_for": "brainstorming / 复杂推理"},
    {"mode": "experts", "best_for": "高质量综合分析"},
    {"mode": "debate_judgement", "best_for": "逻辑推理 / 审查"},
    {"mode": "swarm", "best_for": "大规模并行任务"},
    {"mode": "hierarchical", "best_for": "复杂任务管理"},
    {"mode": "dag", "best_for": "工程化流程"},
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a swarm + roundtable orchestration blueprint."
    )
    parser.add_argument("--task", required=True, help="Task statement.")
    parser.add_argument(
        "--context",
        default="",
        help="Optional constraints, environment, and assumptions.",
    )
    parser.add_argument(
        "--task-type",
        default="auto",
        choices=["auto", "feature", "incident", "architecture", "research", "growth", "generic"],
        help="Task type classifier. Use auto for keyword-based inference.",
    )
    parser.add_argument(
        "--complexity",
        default="auto",
        choices=["auto", "low", "medium", "high"],
        help="Swarm complexity level. Use auto to infer from task/context.",
    )
    parser.add_argument(
        "--primary-mode",
        default="auto",
        choices=["auto"] + sorted(COLLABORATION_MODE_CATALOG.keys()),
        help="Primary collaboration mode. Use auto for routing.",
    )
    parser.add_argument(
        "--force-modes",
        default="",
        help="Comma-separated collaboration modes to force enable.",
    )
    parser.add_argument(
        "--disable-modes",
        default="",
        help="Comma-separated collaboration modes to disable.",
    )
    parser.add_argument(
        "--debate-rounds",
        type=int,
        default=0,
        help="Debate rounds override. 0 means auto.",
    )
    parser.add_argument(
        "--dag-max-parallel-nodes",
        type=int,
        default=0,
        help="DAG max parallel nodes override. 0 means auto.",
    )
    parser.add_argument(
        "--min-experts",
        type=int,
        default=ROUNDTABLE_MIN_EXPERTS,
        help=f"Minimum experts to include after dynamic generation (>= {ROUNDTABLE_MIN_EXPERTS}).",
    )
    parser.add_argument(
        "--max-experts",
        type=int,
        default=6,
        help=f"Maximum experts to include after dynamic generation (<= {ROUNDTABLE_MAX_EXPERTS}).",
    )
    parser.add_argument(
        "--expert",
        action="append",
        default=[],
        help=(
            "Custom expert specification. Format: "
            "'role::focus::output1,output2::agent_type'. "
            "Only role and focus are required."
        ),
    )
    parser.add_argument(
        "--disable-auto-experts",
        action="store_true",
        help="Disable keyword-driven automatic dynamic experts.",
    )
    parser.add_argument(
        "--max-auto-additions",
        type=int,
        default=3,
        help="Maximum keyword-triggered experts to add.",
    )
    parser.add_argument(
        "--force-coordinator",
        default="",
        help="Optional override coordinator role.",
    )
    parser.add_argument(
        "--runner",
        default="native",
        choices=["native", "symphony", "hybrid"],
        help="Execution target. Use symphony/hybrid to generate Symphony workflow fusion output.",
    )
    parser.add_argument(
        "--symphony-project-slug",
        default="",
        help="Linear project slug for Symphony tracker config.",
    )
    parser.add_argument(
        "--symphony-workspace-root",
        default="~/code/symphony-workspaces",
        help="Workspace root for Symphony workflow.",
    )
    parser.add_argument(
        "--symphony-poll-interval-ms",
        type=int,
        default=10000,
        help="Symphony polling interval in milliseconds.",
    )
    parser.add_argument(
        "--symphony-max-concurrent-agents",
        type=int,
        default=10,
        help="Symphony max concurrent agents.",
    )
    parser.add_argument(
        "--symphony-max-turns",
        type=int,
        default=20,
        help="Symphony max turns per worker invocation.",
    )
    parser.add_argument(
        "--symphony-active-states",
        default=",".join(SYMPHONY_DEFAULT_ACTIVE_STATES),
        help="Comma-separated active issue states for Symphony.",
    )
    parser.add_argument(
        "--symphony-terminal-states",
        default=",".join(SYMPHONY_DEFAULT_TERMINAL_STATES),
        help="Comma-separated terminal issue states for Symphony.",
    )
    parser.add_argument(
        "--symphony-codex-command",
        default=SYMPHONY_DEFAULT_CODEX_COMMAND,
        help="Codex app-server command string for Symphony workflow.",
    )
    parser.add_argument(
        "--symphony-approval-policy",
        default="on-failure",
        help="Codex approval policy to include in Symphony workflow front matter.",
    )
    parser.add_argument(
        "--symphony-thread-sandbox",
        default="workspace-write",
        help="Codex thread sandbox for Symphony workflow front matter.",
    )
    parser.add_argument(
        "--symphony-workflow-output",
        default="",
        help="Optional output file path for generated Symphony WORKFLOW.md content.",
    )
    parser.add_argument(
        "--agent-team-max-threads",
        type=int,
        default=0,
        help="Codex multi-agent max thread count. 0 means auto-size from expert count.",
    )
    parser.add_argument(
        "--agent-team-max-depth",
        type=int,
        default=1,
        help="Codex multi-agent spawn depth limit.",
    )
    parser.add_argument(
        "--agent-team-job-max-runtime-seconds",
        type=int,
        default=1800,
        help="Codex multi-agent per-job runtime budget in seconds.",
    )
    parser.add_argument(
        "--disable-agent-team-feature-flag",
        action="store_true",
        help="Do not emit [features] multi_agent=true in generated Codex config draft.",
    )
    parser.add_argument(
        "--agent-team-config-output",
        default="",
        help="Optional output path for generated .codex/config.toml multi-agent draft.",
    )
    parser.add_argument(
        "--agent-team-roles-dir",
        default="",
        help="Optional directory path to write generated role config files (*.toml).",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional path to write output content.",
    )
    return parser.parse_args()


def parse_csv_list(raw: str, defaults: List[str]) -> List[str]:
    if raw is None:
        return defaults[:]
    tokens = [item.strip() for item in raw.split(",")]
    filtered = [item for item in tokens if item]
    return filtered or defaults[:]


def parse_mode_csv(raw: str, arg_name: str) -> List[str]:
    if not raw:
        return []
    tokens = [normalize_role_key(item) for item in raw.split(",")]
    modes = [item for item in tokens if item]
    invalid = [item for item in modes if item not in COLLABORATION_MODE_CATALOG]
    if invalid:
        supported = ", ".join(sorted(COLLABORATION_MODE_CATALOG.keys()))
        raise ValueError(f"{arg_name} has invalid mode(s): {', '.join(invalid)}. Supported: {supported}")
    deduped: List[str] = []
    for item in modes:
        if item not in deduped:
            deduped.append(item)
    return deduped


def yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def sanitize_inline_text(value: str) -> str:
    return " ".join(value.split())


def infer_task_type(task: str) -> str:
    lowered = task.lower()
    scores: Dict[str, int] = {k: 0 for k in TASK_TEMPLATES if k != "generic"}

    for task_type, words in INFER_KEYWORDS.items():
        for word in words:
            if word in lowered:
                scores[task_type] += 1

    best_type = "generic"
    best_score = 0
    for task_type, score in scores.items():
        if score > best_score:
            best_type = task_type
            best_score = score
    return best_type


def infer_complexity(task: str, context: str, task_type: str) -> str:
    text = (task + " " + context).lower()
    score = 0

    if len(text) > 180:
        score += 1
    if task_type in {"incident", "architecture"}:
        score += 1

    for word in COMPLEXITY_KEYWORDS["high"]:
        if word in text:
            score += 2
    for word in COMPLEXITY_KEYWORDS["medium"]:
        if word in text:
            score += 1

    if score <= 1:
        return "low"
    if score <= 4:
        return "medium"
    return "high"


def mode_priority(mode: str) -> int:
    try:
        return MODE_PRIORITY_ORDER.index(mode)
    except ValueError:
        return len(MODE_PRIORITY_ORDER)


def infer_collaboration_mode_scores(
    task: str,
    context: str,
    task_type: str,
    complexity: str,
) -> Dict[str, Any]:
    text = (task + " " + context).lower()
    scores: Dict[str, int] = {mode: 0 for mode in COLLABORATION_MODE_CATALOG}
    reasons: Dict[str, List[str]] = {mode: [] for mode in COLLABORATION_MODE_CATALOG}

    scores["experts"] += 1
    reasons["experts"].append("base: multi-expert collaboration baseline")

    for mode, words in MODE_ROUTING_KEYWORDS.items():
        for word in words:
            if word in text:
                scores[mode] += 1
                reasons[mode].append(f"keyword:{word}")

    task_bias: Dict[str, Dict[str, int]] = {
        "feature": {"experts": 1, "swarm": 1, "dag": 1},
        "incident": {"swarm": 2, "hierarchical": 2, "debate_judgement": 2, "dag": 1},
        "architecture": {"experts": 2, "debate_judgement": 1, "dag": 2, "roundtable": 1},
        "research": {"roundtable": 2, "experts": 2, "debate_judgement": 1},
        "growth": {"roundtable": 2, "experts": 2, "swarm": 1},
        "generic": {"roundtable": 1, "experts": 1},
    }
    for mode, delta in task_bias.get(task_type, {}).items():
        scores[mode] += delta
        reasons[mode].append(f"task_type:{task_type}")

    if complexity == "high":
        for mode in ["swarm", "hierarchical", "dag", "debate_judgement"]:
            scores[mode] += 2
            reasons[mode].append("complexity:high")
    elif complexity == "medium":
        for mode in ["swarm", "dag", "debate_judgement"]:
            scores[mode] += 1
            reasons[mode].append("complexity:medium")
    else:
        for mode in ["roundtable", "experts"]:
            scores[mode] += 1
            reasons[mode].append("complexity:low")

    ranked_modes = sorted(
        scores.keys(),
        key=lambda item: (-scores[item], mode_priority(item), item),
    )
    return {
        "scores": scores,
        "reasons": reasons,
        "ranked_modes": ranked_modes,
    }


def build_collaboration_router(
    task: str,
    context: str,
    task_type: str,
    complexity: str,
    primary_mode: str,
    forced_modes: List[str],
    disabled_modes: List[str],
) -> Dict[str, Any]:
    inferred = infer_collaboration_mode_scores(
        task=task,
        context=context,
        task_type=task_type,
        complexity=complexity,
    )
    scores = inferred["scores"]
    reasons = inferred["reasons"]
    ranked_modes = inferred["ranked_modes"]

    if primary_mode != "auto":
        resolved_primary = primary_mode
        reasons[resolved_primary].append("manual:primary-mode override")
    else:
        resolved_primary = ranked_modes[0]
        reasons[resolved_primary].append("auto:top-ranked mode")

    enabled = {"experts", resolved_primary}
    for mode, score in scores.items():
        if score >= 2:
            enabled.add(mode)

    if task_type in {"research", "growth"}:
        enabled.add("roundtable")
    if task_type in {"incident", "architecture"}:
        enabled.update({"debate_judgement", "dag"})
    if complexity == "high":
        enabled.update({"swarm", "hierarchical", "dag"})
    elif complexity == "medium":
        enabled.update({"swarm", "roundtable"})

    enabled.update(forced_modes)
    enabled -= set(disabled_modes)
    if not enabled:
        enabled = {"experts"}

    if resolved_primary not in enabled:
        fallback = sorted(enabled, key=lambda item: (mode_priority(item), item))
        resolved_primary = fallback[0]
        reasons[resolved_primary].append("auto:fallback primary after mode filters")

    ordered_enabled = sorted(enabled, key=lambda item: (mode_priority(item), item))
    presets = {
        "nexus_full": ["swarm", "hierarchical", "dag", "debate_judgement", "experts"],
        "nexus_sprint": ["swarm", "roundtable", "experts", "dag"],
        "nexus_micro": ["roundtable", "experts"],
    }
    selected_preset = "nexus_sprint"
    if complexity == "high":
        selected_preset = "nexus_full"
    elif complexity == "low":
        selected_preset = "nexus_micro"

    routing_log: List[str] = []
    for mode in ordered_enabled:
        excerpt = reasons.get(mode, [])
        reason_text = "; ".join(excerpt[:3]) if excerpt else "policy:default"
        routing_log.append(f"{mode}: {reason_text}")

    return {
        "primary_mode": resolved_primary,
        "enabled_modes": ordered_enabled,
        "mode_scores": scores,
        "mode_reasons": reasons,
        "routing_log": routing_log,
        "presets": presets,
        "selected_preset": selected_preset,
        "article_scenario_fit": ARTICLE_SCENARIO_FIT,
    }


def build_debate_judgement(
    experts: List[Dict[str, Any]],
    coordinator: str,
    hard_veto_roles: List[str],
    complexity: str,
    mode_router: Dict[str, Any],
    rounds_override: int,
) -> Dict[str, Any]:
    enabled = "debate_judgement" in mode_router["enabled_modes"]
    expert_roles = [expert["role"] for expert in experts]
    jury_roles = [role for role in hard_veto_roles if role in expert_roles]
    if coordinator in expert_roles and coordinator not in jury_roles:
        jury_roles.insert(0, coordinator)

    debaters = [role for role in expert_roles if role not in jury_roles]
    if len(debaters) < 2:
        debaters = [role for role in expert_roles if role != coordinator]
    if len(debaters) < 2:
        debaters = expert_roles[:]

    auto_rounds = 2 if complexity == "high" else 1
    if mode_router["primary_mode"] in {"debate_judgement", "roundtable"} and complexity != "low":
        auto_rounds = max(auto_rounds, 2)
    rounds = max(1, rounds_override) if rounds_override > 0 else auto_rounds
    jury_quorum = max(1, (len(jury_roles) * 2 + 2) // 3) if jury_roles else 1

    return {
        "enabled": enabled,
        "rounds": rounds if enabled else 0,
        "debaters": debaters if enabled else [],
        "jury_roles": jury_roles if enabled else [],
        "evidence_required": enabled,
        "inconclusive_default": "FAIL" if enabled else "N/A",
        "vote_policy": {
            "method": "jury_weighted_majority",
            "jury_vote_weight": 2,
            "debaters_vote_weight": 1,
            "jury_quorum": jury_quorum if enabled else 0,
            "tie_breaker": coordinator,
        },
        "final_gate": {
            "judge": "reality_checker" if enabled else "",
            "default_verdict": "NEEDS_WORK" if enabled else "N/A",
            "allowed_verdicts": ["READY", "NEEDS_WORK", "NOT_READY"] if enabled else [],
        },
        "authorization_checks": [
            "identity_valid",
            "credential_current",
            "scope_sufficient",
            "delegation_chain_valid",
        ] if enabled else [],
        "trigger_condition": (
            "enable when roundtable disagreement remains high, hard veto conflicts exist, or audit-style scrutiny is required"
        ),
        "output_schema": {
            "claim": "string",
            "evidence": ["string"],
            "counter_argument": "string",
            "jury_verdict": "accept/reject/rework",
        },
    }


def build_hierarchical_execution(
    experts: List[Dict[str, Any]],
    topology: Dict[str, Any],
    coordinator: str,
    mode_router: Dict[str, Any],
) -> Dict[str, Any]:
    enabled = "hierarchical" in mode_router["enabled_modes"]
    expert_roles = [expert["role"] for expert in experts]
    if not expert_roles:
        return {
            "enabled": enabled,
            "director": "",
            "managers": [],
            "workers": [],
            "manager_assignments": [],
            "handoff_contract": {},
        }

    director = coordinator if coordinator in expert_roles else expert_roles[0]
    manager_candidates: List[str] = []
    for cell in topology.get("cells", []):
        if cell.get("parallel_wave", 0) > 1:
            continue
        for role in cell.get("roles", []):
            if role != director and role not in manager_candidates:
                manager_candidates.append(role)

    manager_cap = 3 if topology.get("complexity") in {"medium", "high"} else 2
    managers = manager_candidates[:manager_cap]
    if not managers:
        managers = [role for role in expert_roles if role != director][:1]

    workers = [role for role in expert_roles if role not in set([director] + managers)]
    manager_assignments = [{"manager": role, "workers": []} for role in managers]
    if manager_assignments:
        for idx, worker in enumerate(workers):
            owner = manager_assignments[idx % len(manager_assignments)]
            owner["workers"].append(worker)
    for item in manager_assignments:
        cell_name = role_cell(item["manager"])
        item["focus"] = CELL_GOALS.get(cell_name, "task decomposition and execution coordination")

    return {
        "enabled": enabled,
        "director": director if enabled else "",
        "managers": managers if enabled else [],
        "workers": workers if enabled else [],
        "manager_assignments": manager_assignments if enabled else [],
        "escalation_chain": ["agents_orchestrator", "studio_producer", director] if enabled else [],
        "delegation": {
            "require_chain": enabled,
            "must_include": ["from", "to", "scope", "expires_at"],
        },
        "handoff_contract": {
            "director_to_manager": "mission boundaries, priorities, and completion gates",
            "manager_to_worker": "concrete tasks, expected outputs, and test/evidence requirements",
            "worker_to_manager": "execution artifacts, blockers, and verification evidence",
        },
    }


def build_dag_workflow(
    topology: Dict[str, Any],
    phases: List[Dict[str, Any]],
    mode_router: Dict[str, Any],
    debate_plan: Dict[str, Any],
    max_parallel_nodes_override: int,
) -> Dict[str, Any]:
    enabled = "dag" in mode_router["enabled_modes"]
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, str]] = []
    edge_keys = set()

    def add_edge(src: str, dst: str) -> None:
        key = (src, dst)
        if key in edge_keys:
            return
        edge_keys.add(key)
        edges.append({"from": src, "to": dst})

    wave_nodes: Dict[int, List[str]] = {}
    for cell in topology.get("cells", []):
        node_id = f"{cell['cell']}_wave_{cell['parallel_wave']}"
        nodes.append(
            {
                "id": node_id,
                "kind": "swarm_cell",
                "wave": cell["parallel_wave"],
                "team_hint": cell["cell"].replace("_cell", "_team"),
                "parallelizable": True,
            }
        )
        wave_nodes.setdefault(cell["parallel_wave"], []).append(node_id)

    has_alignment = any(phase["phase"] == "phase_0_alignment" for phase in phases)
    if has_alignment:
        nodes.append(
            {
                "id": "alignment_gate",
                "kind": "gate",
                "wave": 0,
                "team_hint": "director_team",
                "parallelizable": False,
            }
        )
        for node_id in wave_nodes.get(1, []):
            add_edge("alignment_gate", node_id)

    sorted_waves = sorted(wave_nodes.keys())
    for idx in range(len(sorted_waves) - 1):
        current_wave = wave_nodes[sorted_waves[idx]]
        next_wave = wave_nodes[sorted_waves[idx + 1]]
        for src in current_wave:
            for dst in next_wave:
                add_edge(src, dst)

    nodes.append(
        {
            "id": "roundtable_critique",
            "kind": "decision_gate",
            "wave": (max(sorted_waves) + 1) if sorted_waves else 1,
            "team_hint": "roundtable_judges_team",
            "parallelizable": False,
        }
    )
    for wave in sorted_waves[-1:] or []:
        for src in wave_nodes.get(wave, []):
            add_edge(src, "roundtable_critique")

    previous_decision_node = "roundtable_critique"
    if debate_plan.get("enabled"):
        nodes.append(
            {
                "id": "debate_judgement",
                "kind": "decision_gate",
                "wave": (max(sorted_waves) + 2) if sorted_waves else 2,
                "team_hint": "debate_judgement_team",
                "parallelizable": False,
            }
        )
        add_edge("roundtable_critique", "debate_judgement")
        previous_decision_node = "debate_judgement"

    nodes.append(
        {
            "id": "convergent_execution",
            "kind": "execution",
            "wave": (max(sorted_waves) + 3) if sorted_waves else 3,
            "team_hint": "delivery_team",
            "parallelizable": False,
        }
    )
    add_edge(previous_decision_node, "convergent_execution")

    if any(phase["phase"] == "phase_4_hardening_gate" for phase in phases):
        nodes.append(
            {
                "id": "hardening_gate",
                "kind": "gate",
                "wave": (max(sorted_waves) + 4) if sorted_waves else 4,
                "team_hint": "roundtable_judges_team",
                "parallelizable": False,
            }
        )
        add_edge("convergent_execution", "hardening_gate")

    parallel_groups = [wave_nodes[wave] for wave in sorted_waves if len(wave_nodes[wave]) > 1]
    auto_parallel_cap = max([len(group) for group in parallel_groups], default=1)
    max_parallel_nodes = (
        max(1, max_parallel_nodes_override)
        if max_parallel_nodes_override > 0
        else auto_parallel_cap
    )

    critical_path: List[str] = []
    if has_alignment:
        critical_path.append("alignment_gate")
    for wave in sorted_waves:
        if wave_nodes[wave]:
            critical_path.append(wave_nodes[wave][0])
    critical_path.append("roundtable_critique")
    if debate_plan.get("enabled"):
        critical_path.append("debate_judgement")
    critical_path.append("convergent_execution")
    if any(node["id"] == "hardening_gate" for node in nodes):
        critical_path.append("hardening_gate")

    return {
        "enabled": enabled,
        "nodes": nodes if enabled else [],
        "edges": edges if enabled else [],
        "parallel_groups": parallel_groups if enabled else [],
        "critical_path": critical_path if enabled else [],
        "max_parallel_nodes": max_parallel_nodes if enabled else 0,
        "gates": {"required": enabled},
        "parallel_join_policy": "barrier" if enabled else "none",
        "dependency_policy": {
            "start_condition": "upstream.qa==PASS",
            "merge_order": "dependency_order",
            "allow_independent_parallel": True,
        } if enabled else {},
        "loops": {
            "dev_qa": {"max_retries": 3, "on_exhausted": "escalate"},
        } if enabled else {},
    }


def build_output_format_contract(
    mode_router: Dict[str, Any],
    complexity: str,
) -> Dict[str, Any]:
    enabled_modes = mode_router.get("enabled_modes", [])
    return {
        "version": "1.1.0",
        "goal": "deterministic, auditable, and readable outputs for multi-agent collaboration",
        "global_rules": [
            "facts_assumptions_risks_must_be_explicit",
            "all_decisions_require_evidence_or_test_reference",
            "handoff_payload_is_mandatory_for_cross-agent_edges",
            "timestamp_in_iso8601_utc",
        ],
        "document_layout": [
            "01_summary",
            "02_task_context",
            "03_collaboration_routing",
            "04_execution_plan",
            "05_quality_and_risk_gates",
            "06_next_actions",
            "07_machine_readable_json",
        ],
        "templates": {
            "handoff": {
                "required_sections": [
                    "metadata",
                    "context",
                    "deliverable_request",
                    "quality_expectations",
                ],
                "required_fields": [
                    "from",
                    "to",
                    "phase",
                    "task_reference",
                    "priority",
                    "timestamp",
                ],
            },
            "pipeline_status": {
                "required_fields": [
                    "current_phase",
                    "tasks_total",
                    "tasks_completed",
                    "qa_pass_rate",
                    "blocked_tasks",
                    "pipeline_health",
                    "next_action",
                ],
                "pipeline_health_enum": ["ON_TRACK", "AT_RISK", "BLOCKED"],
            },
            "qa_verdict": {
                "required_fields": [
                    "task_id",
                    "attempt",
                    "verdict",
                    "evidence",
                    "issues",
                    "fix_instructions",
                ],
                "verdict_enum": ["PASS", "FAIL", "NEEDS_WORK"],
            },
            "decision_log": {
                "required_fields": [
                    "decision_id",
                    "options_compared",
                    "scores",
                    "vetoes",
                    "final_decision",
                    "owner",
                    "timestamp",
                ],
            },
        },
        "rendering": {
            "bullet_style": "flat",
            "table_preferred_for_scorecards": True,
            "top_n_list_limit": 7 if complexity == "high" else 5,
            "include_mode_badges": enabled_modes,
        },
    }


def normalize_role_key(role: str) -> str:
    key = re.sub(r"[^a-z0-9_]+", "_", role.strip().lower()).strip("_")
    if key:
        return key
    fallback = hashlib.md5(role.encode("utf-8")).hexdigest()[:8]
    return f"custom_expert_{fallback}"


def build_expert(role: str, focus: str = "", outputs: List[str] = None, origin: str = "template", agent_type: str = "") -> Dict[str, Any]:
    key = normalize_role_key(role)
    role_info = ROLE_LIBRARY.get(key)
    role_agent_default = ROLE_AGENT_TYPE_OVERRIDES.get(key, "default")

    if role_info:
        resolved_focus = focus or role_info["focus"]
        resolved_outputs = outputs or role_info["default_outputs"]
        resolved_agent = agent_type or role_agent_default
    else:
        resolved_focus = focus or "domain-specific constraints, risks, and practical guidance"
        resolved_outputs = outputs or ["key_constraints", "risks", "recommended_actions"]
        resolved_agent = agent_type or role_agent_default

    if resolved_agent not in KNOWN_AGENT_TYPES:
        resolved_agent = "default"

    return {
        "role": key,
        "focus": resolved_focus,
        "expected_outputs": resolved_outputs,
        "origin": origin,
        "agent_type": resolved_agent,
    }


def parse_custom_expert(spec: str) -> Dict[str, Any]:
    parts = [part.strip() for part in spec.split("::")]
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError(
            f"Invalid --expert spec '{spec}'. Expected 'role::focus::output1,output2::agent_type'."
        )

    role = parts[0]
    focus = parts[1]
    outputs = [item.strip() for item in parts[2].split(",")] if len(parts) >= 3 and parts[2] else []
    agent_type = parts[3].strip() if len(parts) >= 4 and parts[3] else ""
    return build_expert(role=role, focus=focus, outputs=outputs, origin="custom", agent_type=agent_type)


def infer_dynamic_candidates(task: str, context: str, max_auto_additions: int) -> List[Dict[str, Any]]:
    text = (task + " " + context).lower()
    hits: List[Dict[str, Any]] = []

    for candidate in DYNAMIC_EXPERT_CATALOG:
        matched = [word for word in candidate["triggers"] if word in text]
        if matched:
            expert = build_expert(
                role=candidate["role"],
                focus=candidate["focus"],
                outputs=candidate["default_outputs"],
                origin="dynamic",
                agent_type="default",
            )
            expert["trigger_hits"] = matched
            hits.append(expert)

    hits.sort(key=lambda item: len(item.get("trigger_hits", [])), reverse=True)
    return hits[: max(0, max_auto_additions)]


def dedupe_experts(experts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    deduped: List[Dict[str, Any]] = []
    seen = set()
    for expert in experts:
        role = normalize_role_key(expert["role"])
        if role in seen:
            continue
        seen.add(role)
        normalized = dict(expert)
        normalized["role"] = role
        deduped.append(normalized)
    return deduped


def build_experts(
    task: str,
    context: str,
    task_type: str,
    min_experts: int,
    max_experts: int,
    custom_specs: List[str],
    enable_auto_experts: bool,
    max_auto_additions: int,
    forced_coordinator: str,
) -> Dict[str, Any]:
    template = TASK_TEMPLATES[task_type]
    coordinator = normalize_role_key(forced_coordinator) if forced_coordinator else template["coordinator"]

    generated: List[Dict[str, Any]] = []
    generation_log: List[str] = []

    for role in [coordinator] + template["experts"]:
        generated.append(build_expert(role=role, origin="template"))

    for spec in custom_specs:
        custom_expert = parse_custom_expert(spec)
        generated.append(custom_expert)
        generation_log.append(f"custom expert added: {custom_expert['role']}")

    if enable_auto_experts:
        auto_experts = infer_dynamic_candidates(task=task, context=context, max_auto_additions=max_auto_additions)
        for expert in auto_experts:
            generated.append(expert)
            hits = ", ".join(expert.get("trigger_hits", []))
            generation_log.append(f"dynamic expert added: {expert['role']} (hits: {hits})")

    deduped = dedupe_experts(generated)

    hard_floor = max(ROUNDTABLE_MIN_EXPERTS, min_experts)
    hard_cap = min(ROUNDTABLE_MAX_EXPERTS, max(hard_floor, max_experts))
    if coordinator not in [item["role"] for item in deduped]:
        deduped.insert(0, build_expert(role=coordinator, origin="coordinator"))

    if len(deduped) < hard_floor:
        for role in template["experts"]:
            if len(deduped) >= hard_floor:
                break
            deduped.append(build_expert(role=role, origin="fallback"))
        deduped = dedupe_experts(deduped)

    origin_priority = {
        "coordinator": 0,
        "custom": 1,
        "dynamic": 2,
        "template": 3,
        "fallback": 4,
    }
    coordinator_entry = next((item for item in deduped if item["role"] == coordinator), None)
    remaining = [item for item in deduped if item["role"] != coordinator]
    remaining.sort(
        key=lambda item: (
            origin_priority.get(item.get("origin", "template"), 5),
            {
                "orchestration": 0,
                "design": 1,
                "discovery": 2,
                "build": 3,
                "assurance": 4,
            }.get(role_cell(item["role"]), 9),
            item["role"],
        )
    )
    selected: List[Dict[str, Any]] = []
    if coordinator_entry:
        selected.append(coordinator_entry)
    for item in remaining:
        if len(selected) >= hard_cap:
            break
        selected.append(item)
    dropped = [item["role"] for item in deduped if item["role"] not in {x["role"] for x in selected}]
    if dropped:
        generation_log.append(
            f"selection cap applied ({hard_cap}); dropped roles: {', '.join(dropped)}"
        )

    if not generation_log:
        generation_log.append("no dynamic additions triggered; used template experts only")

    return {
        "experts": selected,
        "coordinator": coordinator,
        "generation_log": generation_log,
    }


def role_cell(role: str) -> str:
    discovery = {
        "product_manager",
        "product_consultant",
        "uiux_designer",
        "experience_designer",
        "data_analyst",
        "domain_specialist",
        "trend_researcher",
        "feedback_synthesizer",
    }
    design = {
        "software_architect",
        "cto",
        "security_reviewer",
        "performance_engineer",
        "reliability_engineer",
        "data_governance_specialist",
        "content_creator",
        "visual_storyteller",
        "image_prompt_engineer",
        "brand_guardian",
    }
    build = {
        "frontend_engineer",
        "backend_engineer",
        "fullstack_engineer",
        "integration_specialist",
        "social_media_strategist",
        "report_distribution_agent",
    }
    assurance = {
        "qa_engineer",
        "devops_engineer",
        "release_manager",
        "cost_optimizer",
        "legal_compliance_checker",
        "analytics_reporter",
        "experiment_tracker",
        "evidence_collector",
        "reality_checker",
    }

    if role in {"tech_lead", "agents_orchestrator"}:
        return "orchestration"
    if role in discovery:
        return "discovery"
    if role in design:
        return "design"
    if role in build:
        return "build"
    if role in assurance:
        return "assurance"
    if "architect" in role or "security" in role:
        return "design"
    if "engineer" in role:
        return "build"
    return "discovery"


def build_swarm_topology(experts: List[Dict[str, Any]], complexity: str) -> Dict[str, Any]:
    bucketed: Dict[str, List[str]] = {
        "discovery": [],
        "design": [],
        "build": [],
        "assurance": [],
        "orchestration": [],
    }
    for expert in experts:
        cell = role_cell(expert["role"])
        bucketed[cell].append(expert["role"])

    cells: List[Dict[str, Any]] = []

    if complexity == "low":
        strategy_roles = bucketed["discovery"] + bucketed["design"] + bucketed["orchestration"]
        delivery_roles = bucketed["build"] + bucketed["assurance"]
        if strategy_roles:
            cells.append(
                {
                    "cell": "strategy_cell",
                    "parallel_wave": 1,
                    "goal": "option framing and architecture sanity checks",
                    "roles": strategy_roles,
                }
            )
        if delivery_roles:
            cells.append(
                {
                    "cell": "delivery_cell",
                    "parallel_wave": 2,
                    "goal": "implementation and quality rollout plan",
                    "roles": delivery_roles,
                }
            )
    else:
        for name in ["orchestration", "discovery", "design", "build", "assurance"]:
            roles = bucketed[name]
            if not roles:
                continue
            wave = 1 if name in {"orchestration", "discovery", "design"} else 2
            if complexity == "high" and name == "assurance":
                wave = 3
            cells.append(
                {
                    "cell": f"{name}_cell",
                    "parallel_wave": wave,
                    "goal": CELL_GOALS[name],
                    "roles": roles,
                }
            )

    max_wave = 1
    for cell in cells:
        max_wave = max(max_wave, cell["parallel_wave"])

    return {
        "complexity": complexity,
        "cells": cells,
        "parallel_waves": max_wave,
    }


def resolve_agent_team_max_threads(
    requested: int,
    expert_count: int,
    mode_router: Dict[str, Any],
    dag_workflow: Dict[str, Any],
) -> int:
    if requested and requested > 0:
        return max(1, requested)
    enabled_modes = set(mode_router.get("enabled_modes", []))
    auto_threads = expert_count + 1
    if "swarm" in enabled_modes:
        auto_threads += 2
    if "hierarchical" in enabled_modes:
        auto_threads += 1
    if "dag" in enabled_modes:
        auto_threads = max(auto_threads, int(dag_workflow.get("max_parallel_nodes", 1)) + 2)
    return max(4, min(24, auto_threads))


def build_agent_teams(
    topology: Dict[str, Any],
    coordinator: str,
    hard_veto_roles: List[str],
    expert_roles: List[str],
    mode_router: Dict[str, Any],
    debate_plan: Dict[str, Any],
    hierarchy_plan: Dict[str, Any],
) -> List[Dict[str, Any]]:
    teams: List[Dict[str, Any]] = []
    existing_teams = set()

    def append_team(team: Dict[str, Any]) -> None:
        key = team["team"]
        if key in existing_teams:
            return
        roles = [role for role in team.get("roles", []) if role in expert_roles]
        if not roles:
            return
        normalized = dict(team)
        normalized["roles"] = roles
        teams.append(normalized)
        existing_teams.add(key)

    for cell in topology.get("cells", []):
        team_name = cell["cell"].replace("_cell", "_team")
        append_team(
            {
                "team": team_name,
                "wave": cell["parallel_wave"],
                "goal": cell["goal"],
                "roles": cell["roles"],
            }
        )

    judge_roles = [role for role in hard_veto_roles if role in expert_roles]
    if coordinator in expert_roles and coordinator not in judge_roles:
        judge_roles = [coordinator] + judge_roles
    if judge_roles:
        append_team(
            {
                "team": "roundtable_judges_team",
                "wave": topology.get("parallel_waves", 1) + 1,
                "goal": "score options, apply veto policy, and finalize consensus",
                "roles": judge_roles,
            }
        )

    enabled_modes = set(mode_router.get("enabled_modes", []))
    if "debate_judgement" in enabled_modes and debate_plan.get("enabled"):
        append_team(
            {
                "team": "debate_arena_team",
                "wave": topology.get("parallel_waves", 1) + 1,
                "goal": "challenge finalist options through structured counter-arguments",
                "roles": debate_plan.get("debaters", []),
            }
        )
        append_team(
            {
                "team": "debate_judgement_team",
                "wave": topology.get("parallel_waves", 1) + 2,
                "goal": "jury voting and final adjudication",
                "roles": debate_plan.get("jury_roles", []),
            }
        )

    if "hierarchical" in enabled_modes and hierarchy_plan.get("enabled"):
        director = hierarchy_plan.get("director")
        if director:
            append_team(
                {
                    "team": "director_team",
                    "wave": 0,
                    "goal": "mission steering and escalation decisions",
                    "roles": [director],
                }
            )
        for item in hierarchy_plan.get("manager_assignments", []):
            manager = item.get("manager")
            if not manager:
                continue
            manager_team = f"manager_{manager}_team"
            append_team(
                {
                    "team": manager_team,
                    "wave": 1,
                    "goal": "task decomposition and dependency management",
                    "roles": [manager] + item.get("workers", []),
                }
            )

    if "dag" in enabled_modes:
        append_team(
            {
                "team": "dag_orchestrator_team",
                "wave": topology.get("parallel_waves", 1) + 3,
                "goal": "enforce node dependencies and orchestrate parallel execution windows",
                "roles": [coordinator],
            }
        )

    qa_evidence_roles = [role for role in ["evidence_collector", "reality_checker"] if role in expert_roles]
    if qa_evidence_roles:
        append_team(
            {
                "team": "reality_gate_team",
                "wave": topology.get("parallel_waves", 1) + 2,
                "goal": "evidence-first QA and release readiness certification",
                "roles": qa_evidence_roles,
            }
        )
    return teams


def build_role_instruction_block(
    expert: Dict[str, Any],
    primary_team: str,
    is_hard_veto: bool,
    enabled_modes: List[str],
    hierarchy_plan: Dict[str, Any],
    debate_plan: Dict[str, Any],
) -> str:
    role = expert["role"]
    hierarchy_role = "peer"
    if hierarchy_plan.get("enabled"):
        if role == hierarchy_plan.get("director"):
            hierarchy_role = "director"
        elif role in hierarchy_plan.get("managers", []):
            hierarchy_role = "manager"
        else:
            hierarchy_role = "worker"
    jury_role = role in debate_plan.get("jury_roles", [])

    lines = [
        f"You are the `{role}` sub-agent in swarm + roundtable mode.",
        f"Primary team: {primary_team}.",
        f"Enabled collaboration modes: {', '.join(enabled_modes) if enabled_modes else 'experts'}.",
        f"Hierarchy role: {hierarchy_role}.",
        f"Ownership focus: {sanitize_inline_text(expert['focus'])}.",
        "Output must be concise, structured, and evidence-backed.",
        "Stay within your ownership boundary and avoid rewriting other roles.",
        "Tag uncertain statements as assumptions.",
    ]
    if is_hard_veto:
        lines.append(
            "You are a hard-veto reviewer for safety/reliability gates and must block unsafe proposals."
        )
    if jury_role:
        lines.append("You are part of the jury in debate mode and must issue a clear verdict.")
    return "\n".join(lines)


def build_codex_multi_agent_bundle(
    blueprint: Dict[str, Any],
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    experts = blueprint["experts"]
    expert_roles = [expert["role"] for expert in experts]
    hard_veto_roles = blueprint["roundtable"]["hard_veto_roles"]
    teams = build_agent_teams(
        topology=blueprint["swarm_topology"],
        coordinator=blueprint["coordinator"],
        hard_veto_roles=hard_veto_roles,
        expert_roles=expert_roles,
        mode_router=blueprint["collaboration_modes"],
        debate_plan=blueprint["debate_judgement"],
        hierarchy_plan=blueprint["hierarchical_execution"],
    )

    role_to_team: Dict[str, str] = {}
    for team in teams:
        for role in team["roles"]:
            role_to_team.setdefault(role, team["team"])

    max_threads = resolve_agent_team_max_threads(
        cfg["max_threads"],
        expert_count=len(experts),
        mode_router=blueprint["collaboration_modes"],
        dag_workflow=blueprint["dag_workflow"],
    )
    max_depth = max(1, int(cfg["max_depth"]))
    if (
        cfg["max_depth"] <= 1
        and any(
            mode in blueprint["collaboration_modes"]["enabled_modes"]
            for mode in ["hierarchical", "dag"]
        )
    ):
        max_depth = 2
    job_runtime = max(300, int(cfg["job_max_runtime_seconds"]))
    emit_feature_flag = bool(cfg["emit_feature_flag"])

    role_configs: List[Dict[str, Any]] = []
    for expert in experts:
        role = expert["role"]
        primary_team = role_to_team.get(role, "swarm_team")
        is_hard_veto = role in hard_veto_roles
        reasoning_effort = "high" if is_hard_veto else "medium"
        sandbox_mode = "read-only" if "build" not in primary_team else ""

        role_file_lines: List[str] = [
            f'model = {json.dumps(CODEX_DEFAULT_MODEL)}',
            f'model_reasoning_effort = {json.dumps(reasoning_effort)}',
        ]
        if sandbox_mode:
            role_file_lines.append(f'sandbox_mode = {json.dumps(sandbox_mode)}')
        role_file_lines.append('developer_instructions = """')
        role_file_lines.append(
            build_role_instruction_block(
                expert=expert,
                primary_team=primary_team,
                is_hard_veto=is_hard_veto,
                enabled_modes=blueprint["collaboration_modes"]["enabled_modes"],
                hierarchy_plan=blueprint["hierarchical_execution"],
                debate_plan=blueprint["debate_judgement"],
            )
        )
        role_file_lines.append('"""')
        role_content = "\n".join(role_file_lines) + "\n"

        role_configs.append(
            {
                "role": role,
                "team": primary_team,
                "description": (
                    f"Swarm+roundtable sub-agent for {primary_team}. "
                    f"Focus: {sanitize_inline_text(expert['focus'])}."
                ),
                "config_file": f"agents/{role}.toml",
                "model": CODEX_DEFAULT_MODEL,
                "model_reasoning_effort": reasoning_effort,
                "sandbox_mode": sandbox_mode or "inherit",
                "content": role_content,
            }
        )

    toml_lines: List[str] = []
    if emit_feature_flag:
        toml_lines.extend(["[features]", "multi_agent = true", ""])
    toml_lines.extend(
        [
            "[agents]",
            f"max_threads = {max_threads}",
            f"max_depth = {max_depth}",
            f"job_max_runtime_seconds = {job_runtime}",
            "",
        ]
    )
    for item in role_configs:
        toml_lines.extend(
            [
                f"[agents.{item['role']}]",
                f"description = {json.dumps(item['description'], ensure_ascii=False)}",
                f"config_file = {json.dumps(item['config_file'], ensure_ascii=False)}",
                "",
            ]
        )

    return {
        "sub_agent_runtime": {
            "max_threads": max_threads,
            "max_depth": max_depth,
            "job_max_runtime_seconds": job_runtime,
            "feature_flag_enabled": emit_feature_flag,
            "mode_aware_autoscaling": cfg["max_threads"] == 0,
        },
        "agent_teams": teams,
        "role_configs": role_configs,
        "config_toml": "\n".join(toml_lines).rstrip() + "\n",
    }


def build_phases(
    complexity: str,
    mode_router: Dict[str, Any],
    debate_enabled: bool,
) -> List[Dict[str, Any]]:
    enabled_modes = set(mode_router.get("enabled_modes", []))

    if complexity == "low":
        phases = [
            {
                "phase": "phase_1_divergent_swarm",
                "goal": "parallel exploration and solution cards",
                "timebox_minutes": 12,
                "mode": "swarm" if "swarm" in enabled_modes else "experts",
            },
            {
                "phase": "phase_2_roundtable_critique",
                "goal": "cross-scoring, veto capture, shortlist decision",
                "timebox_minutes": 10,
                "mode": "roundtable",
            },
            {
                "phase": "phase_3_convergent_swarm",
                "goal": "final implementation slice with quality checks",
                "timebox_minutes": 18,
                "mode": "experts",
            },
        ]
    elif complexity == "high":
        phases = [
            {
                "phase": "phase_0_alignment",
                "goal": "lock mission boundaries, non-goals, and decision rules",
                "timebox_minutes": 10,
                "mode": "hierarchical" if "hierarchical" in enabled_modes else "roundtable",
            },
            {
                "phase": "phase_1_divergent_swarm",
                "goal": "multi-cell parallel exploration and deep risk surfacing",
                "timebox_minutes": 30,
                "mode": "swarm",
            },
            {
                "phase": "phase_2_roundtable_critique",
                "goal": "cross-cell challenge, scoring, and veto checks",
                "timebox_minutes": 20,
                "mode": "roundtable",
            },
            {
                "phase": "phase_3_convergent_swarm",
                "goal": "merge winner/hybrid into execution design and owners",
                "timebox_minutes": 40,
                "mode": "experts",
            },
            {
                "phase": "phase_4_hardening_gate",
                "goal": "quality/reliability/release gate review before close",
                "timebox_minutes": 20,
                "mode": "debate_judgement" if debate_enabled else "roundtable",
            },
        ]
    else:
        phases = [
            {
                "phase": "phase_1_divergent_swarm",
                "goal": "parallel solution exploration and proposal generation",
                "timebox_minutes": 20,
                "mode": "swarm" if "swarm" in enabled_modes else "experts",
            },
            {
                "phase": "phase_2_roundtable_critique",
                "goal": "cross-expert critique, scoring, veto capture",
                "timebox_minutes": 15,
                "mode": "roundtable",
            },
            {
                "phase": "phase_3_convergent_swarm",
                "goal": "implement winner/hybrid with execution owners and gates",
                "timebox_minutes": 30,
                "mode": "experts",
            },
        ]

    if debate_enabled:
        insert_idx = 2
        phases.insert(
            insert_idx,
            {
                "phase": "phase_2b_debate_judgement",
                "goal": "run structured debate and jury vote on finalists",
                "timebox_minutes": 8 if complexity == "low" else 12,
                "mode": "debate_judgement",
            },
        )

    return phases


def derive_hard_veto_roles(experts: List[Dict[str, Any]]) -> List[str]:
    default_set = {"qa_engineer", "devops_engineer", "software_architect", "cto"}
    dynamic_hard = {
        "security_reviewer",
        "reliability_engineer",
        "data_governance_specialist",
        "legal_compliance_checker",
        "experiment_tracker",
        "reality_checker",
        "agents_orchestrator",
    }
    roles = {expert["role"] for expert in experts}
    selected = sorted((default_set | dynamic_hard) & roles)
    return selected or sorted(default_set)


def build_spawn_prompt(expert: Dict[str, Any], task: str, context: str) -> str:
    output_keys = expert["expected_outputs"]
    role = expert["role"]
    return (
        f"You are acting as {role}. "
        f"Mission: {task}\n"
        f"Context/constraints: {context or 'N/A'}\n"
        f"Ownership focus: {expert['focus']}\n"
        "Return exactly one JSON object:\n"
        "{\n"
        '  "proposal_id": "Option-X",\n'
        '  "summary": "...",\n'
        '  "plan": ["..."],\n'
        '  "risks": ["..."],\n'
        '  "assumptions": ["..."],\n'
        '  "evidence_or_tests": ["..."],\n'
        f'  "role_specific_outputs": {json.dumps(output_keys)}\n'
        "}\n"
        "Do not produce extra sections outside JSON."
    )


def build_roundtable_prompt(task: str) -> str:
    criteria = ", ".join(DEFAULT_CRITERIA_WEIGHTS.keys())
    return (
        "You are in roundtable review.\n"
        f"Task: {task}\n"
        "Input: all proposal cards from experts.\n"
        f"Score each option on 1-5 for criteria: {criteria}.\n"
        "Output JSON only:\n"
        "{\n"
        '  "expert": "<role>",\n'
        '  "scores": {\n'
        '    "Option-A": {"impact": 0, "feasibility": 0, "risk_control": 0, "time_to_value": 0, "maintainability": 0}\n'
        "  },\n"
        '  "veto": [{"option": "Option-X", "reason": "..."}],\n'
        '  "notes": "..."\n'
        "}\n"
        "Only use veto for severe blockers."
    )


def build_symphony_workflow(
    task: str,
    context: str,
    blueprint: Dict[str, Any],
    symphony_cfg: Dict[str, Any],
) -> Dict[str, Any]:
    project_slug = symphony_cfg["project_slug"] or "replace-with-linear-project-slug"
    active_states = symphony_cfg["active_states"]
    terminal_states = symphony_cfg["terminal_states"]
    max_concurrent = max(1, int(symphony_cfg["max_concurrent_agents"]))
    max_turns = max(1, int(symphony_cfg["max_turns"]))
    poll_interval_ms = max(1000, int(symphony_cfg["poll_interval_ms"]))
    workspace_root = symphony_cfg["workspace_root"]
    codex_command = symphony_cfg["codex_command"]
    approval_policy = symphony_cfg["approval_policy"]
    thread_sandbox = symphony_cfg["thread_sandbox"]

    lines: List[str] = []
    lines.append("---")
    lines.append("tracker:")
    lines.append("  kind: linear")
    lines.append(f"  project_slug: {yaml_scalar(project_slug)}")
    lines.append("  active_states:")
    for state in active_states:
        lines.append(f"    - {yaml_scalar(state)}")
    lines.append("  terminal_states:")
    for state in terminal_states:
        lines.append(f"    - {yaml_scalar(state)}")
    lines.append("polling:")
    lines.append(f"  interval_ms: {poll_interval_ms}")
    lines.append("workspace:")
    lines.append(f"  root: {yaml_scalar(workspace_root)}")
    lines.append("agent:")
    lines.append(f"  max_concurrent_agents: {max_concurrent}")
    lines.append(f"  max_turns: {max_turns}")
    lines.append("codex:")
    lines.append(f"  command: {yaml_scalar(codex_command)}")
    lines.append(f"  approval_policy: {yaml_scalar(approval_policy)}")
    lines.append(f"  thread_sandbox: {yaml_scalar(thread_sandbox)}")
    lines.append("  turn_sandbox_policy:")
    lines.append("    type: workspaceWrite")
    lines.append("swarm_roundtable:")
    lines.append("  enabled: true")
    lines.append(f"  task_type: {yaml_scalar(blueprint['task_type'])}")
    lines.append(f"  complexity: {yaml_scalar(blueprint['complexity'])}")
    lines.append(f"  primary_mode: {yaml_scalar(blueprint['collaboration_modes']['primary_mode'])}")
    lines.append(f"  selected_preset: {yaml_scalar(blueprint['collaboration_modes']['selected_preset'])}")
    lines.append("  enabled_modes:")
    for mode in blueprint["collaboration_modes"]["enabled_modes"]:
        lines.append(f"    - {yaml_scalar(mode)}")
    lines.append(f"  consensus_threshold: {blueprint['roundtable']['consensus_threshold']}")
    lines.append(f"  debate_enabled: {yaml_scalar(blueprint['debate_judgement']['enabled'])}")
    lines.append(f"  hierarchical_enabled: {yaml_scalar(blueprint['hierarchical_execution']['enabled'])}")
    lines.append(f"  dag_enabled: {yaml_scalar(blueprint['dag_workflow']['enabled'])}")
    lines.append(f"  output_format_version: {yaml_scalar(blueprint['output_format']['version'])}")
    lines.append("  hard_veto_roles:")
    for role in blueprint["roundtable"]["hard_veto_roles"]:
        lines.append(f"    - {yaml_scalar(role)}")
    lines.append("  experts:")
    for expert in blueprint["experts"]:
        lines.append(f"    - role: {yaml_scalar(expert['role'])}")
        lines.append(f"      focus: {yaml_scalar(sanitize_inline_text(expert['focus']))}")
        lines.append(f"      agent_type: {yaml_scalar(expert['agent_type'])}")
    lines.append("---")

    expert_panel = "\n".join(
        f"- `{expert['role']}` ({expert['focus']})" for expert in blueprint["experts"]
    )
    criteria_block = "\n".join(
        f"- `{criterion}` weight `{weight}`"
        for criterion, weight in blueprint["roundtable"]["criteria_weights"].items()
    )

    prompt_lines: List[str] = [
        "You are working on Linear issue `{{ issue.identifier }}`.",
        "",
        "Ticket context:",
        "- Title: `{{ issue.title }}`",
        "- State: `{{ issue.state }}`",
        "- URL: `{{ issue.url }}`",
        "- Description: `{{ issue.description }}`",
        "",
        "Mission:",
        f"- Primary task: {task}",
        f"- Extra context: {context or 'N/A'}",
        "",
        "Swarm + Roundtable fusion policy (must follow):",
        "1. Follow front matter `primary_mode` + `enabled_modes` for routing and handoffs.",
        "2. Run a divergent swarm phase and produce at least 2 concrete implementation options.",
        "3. Evaluate options with explicit expert viewpoints:",
    ]
    prompt_lines.extend(expert_panel.splitlines())
    prompt_lines.extend(
        [
            "4. Run a structured roundtable scorecard over criteria:",
        ]
    )
    prompt_lines.extend(criteria_block.splitlines())
    prompt_lines.extend(
        [
            "5. Respect hard veto roles from front matter `swarm_roundtable.hard_veto_roles`.",
            "6. If debate mode is enabled, run jury adjudication before final convergence.",
            "7. If top options are too close or vetoed, run a second short roundtable on finalists.",
            "8. Converge to one plan (or justified hybrid), execute, then report evidence.",
            "",
            "Required output discipline:",
            "- Keep an auditable decision log in repo artifacts or ticket comments.",
            "- Distinguish `facts`, `assumptions`, and `risks`.",
            "- Include tests/verification before requesting Human Review.",
            "- If blocked by missing permissions/secrets, report blocker precisely.",
        ]
    )
    prompt = "\n".join(prompt_lines)

    workflow_md = "\n".join(lines) + "\n\n" + prompt + "\n"
    warnings = []
    if not symphony_cfg["project_slug"]:
        warnings.append("symphony_project_slug_missing: set --symphony-project-slug before production use")

    return {
        "workflow_md": workflow_md,
        "warnings": warnings,
        "summary": {
            "project_slug": project_slug,
            "poll_interval_ms": poll_interval_ms,
            "max_concurrent_agents": max_concurrent,
            "max_turns": max_turns,
        },
    }


def build_blueprint(
    task: str,
    context: str,
    task_type: str,
    complexity: str,
    min_experts: int,
    max_experts: int,
    custom_specs: List[str],
    enable_auto_experts: bool,
    max_auto_additions: int,
    forced_coordinator: str,
    runner: str,
    symphony_cfg: Dict[str, Any],
    agent_team_cfg: Dict[str, Any],
    mode_cfg: Dict[str, Any],
) -> Dict[str, Any]:
    resolved_complexity = complexity if complexity != "auto" else infer_complexity(task, context, task_type)

    expert_bundle = build_experts(
        task=task,
        context=context,
        task_type=task_type,
        min_experts=min_experts,
        max_experts=max_experts,
        custom_specs=custom_specs,
        enable_auto_experts=enable_auto_experts,
        max_auto_additions=max_auto_additions,
        forced_coordinator=forced_coordinator,
    )
    experts = expert_bundle["experts"]
    coordinator = expert_bundle["coordinator"]
    topology = build_swarm_topology(experts, resolved_complexity)
    hard_veto_roles = derive_hard_veto_roles(experts)
    mode_router = build_collaboration_router(
        task=task,
        context=context,
        task_type=task_type,
        complexity=resolved_complexity,
        primary_mode=mode_cfg["primary_mode"],
        forced_modes=mode_cfg["forced_modes"],
        disabled_modes=mode_cfg["disabled_modes"],
    )
    debate_plan = build_debate_judgement(
        experts=experts,
        coordinator=coordinator,
        hard_veto_roles=hard_veto_roles,
        complexity=resolved_complexity,
        mode_router=mode_router,
        rounds_override=mode_cfg["debate_rounds"],
    )
    phases = build_phases(
        complexity=resolved_complexity,
        mode_router=mode_router,
        debate_enabled=debate_plan["enabled"],
    )
    hierarchy_plan = build_hierarchical_execution(
        experts=experts,
        topology=topology,
        coordinator=coordinator,
        mode_router=mode_router,
    )
    dag_workflow = build_dag_workflow(
        topology=topology,
        phases=phases,
        mode_router=mode_router,
        debate_plan=debate_plan,
        max_parallel_nodes_override=mode_cfg["dag_max_parallel_nodes"],
    )
    output_format = build_output_format_contract(
        mode_router=mode_router,
        complexity=resolved_complexity,
    )

    spawn_prompts = [
        {
            "role": expert["role"],
            "agent_type": expert["agent_type"],
            "origin": expert["origin"],
            "prompt": build_spawn_prompt(expert, task, context),
        }
        for expert in experts
    ]

    blueprint = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "context": context,
        "task_type": task_type,
        "complexity": resolved_complexity,
        "runner": runner,
        "coordinator": coordinator,
        "experts": experts,
        "collaboration_modes": mode_router,
        "swarm_topology": topology,
        "swarm_phases": phases,
        "generation_log": expert_bundle["generation_log"],
        "roundtable": {
            "criteria_weights": DEFAULT_CRITERIA_WEIGHTS,
            "consensus_threshold": 0.67,
            "hard_veto_roles": hard_veto_roles,
            "round2_condition": "trigger if top option approval_ratio < threshold or hard veto exists",
            "adjudication_mode": "debate_judgement_jury" if debate_plan["enabled"] else "scorecard_only",
        },
        "debate_judgement": debate_plan,
        "hierarchical_execution": hierarchy_plan,
        "dag_workflow": dag_workflow,
        "output_format": output_format,
        "spawn_prompts": spawn_prompts,
        "roundtable_prompt": build_roundtable_prompt(task),
    }
    blueprint["codex_multi_agent"] = build_codex_multi_agent_bundle(
        blueprint=blueprint,
        cfg=agent_team_cfg,
    )

    if runner in {"symphony", "hybrid"}:
        blueprint["symphony_fusion"] = build_symphony_workflow(
            task=task,
            context=context,
            blueprint=blueprint,
            symphony_cfg=symphony_cfg,
        )

    return blueprint


def to_markdown(blueprint: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Swarm + Roundtable Blueprint")
    lines.append("")
    lines.append(f"- Task: {blueprint['task']}")
    lines.append(f"- Task Type: {blueprint['task_type']}")
    lines.append(f"- Complexity: {blueprint['complexity']}")
    lines.append(f"- Runner: {blueprint['runner']}")
    lines.append(f"- Coordinator: {blueprint['coordinator']}")
    if blueprint["context"]:
        lines.append(f"- Context: {blueprint['context']}")
    lines.append("")
    lines.append("## Expert Panel")
    for idx, expert in enumerate(blueprint["experts"], start=1):
        lines.append(
            f"{idx}. `{expert['role']}` [{expert['agent_type']}/{expert['origin']}] - "
            f"{expert['focus']} (outputs: {', '.join(expert['expected_outputs'])})"
        )
    lines.append("")
    lines.append("## Dynamic Generation Log")
    for line in blueprint.get("generation_log", []):
        lines.append(f"- {line}")
    lines.append("")
    lines.append("## Collaboration Routing")
    lines.append(f"- Primary mode: {blueprint['collaboration_modes']['primary_mode']}")
    lines.append(f"- Selected preset: {blueprint['collaboration_modes']['selected_preset']}")
    lines.append(
        f"- Enabled modes: {', '.join(blueprint['collaboration_modes']['enabled_modes'])}"
    )
    lines.append("- Routing reasons:")
    for item in blueprint["collaboration_modes"].get("routing_log", []):
        lines.append(f"  - {item}")
    lines.append("- Article scenario fit:")
    for item in blueprint["collaboration_modes"].get("article_scenario_fit", []):
        lines.append(f"  - {item['mode']}: {item['best_for']}")
    lines.append("")
    lines.append("## Swarm Topology")
    lines.append(f"- Parallel waves: {blueprint['swarm_topology']['parallel_waves']}")
    for cell in blueprint["swarm_topology"]["cells"]:
        lines.append(
            f"- `{cell['cell']}` (wave {cell['parallel_wave']}): {cell['goal']} | roles: {', '.join(cell['roles'])}"
        )
    lines.append("")
    lines.append("## Phases")
    for phase in blueprint["swarm_phases"]:
        lines.append(
            f"- `{phase['phase']}` ({phase['timebox_minutes']}m, mode={phase.get('mode', 'n/a')}): {phase['goal']}"
        )
    lines.append("")
    lines.append("## Roundtable Rules")
    lines.append(
        f"- Consensus threshold: {blueprint['roundtable']['consensus_threshold']}"
    )
    lines.append(
        f"- Hard veto roles: {', '.join(blueprint['roundtable']['hard_veto_roles'])}"
    )
    lines.append(f"- Adjudication mode: {blueprint['roundtable']['adjudication_mode']}")
    lines.append("- Criteria weights:")
    for key, value in blueprint["roundtable"]["criteria_weights"].items():
        lines.append(f"  - {key}: {value}")
    lines.append("")
    lines.append("## Debate Judgement")
    debate = blueprint["debate_judgement"]
    lines.append(f"- Enabled: {debate['enabled']}")
    lines.append(f"- Rounds: {debate['rounds']}")
    lines.append(f"- Debaters: {', '.join(debate['debaters']) if debate['debaters'] else 'N/A'}")
    lines.append(f"- Jury roles: {', '.join(debate['jury_roles']) if debate['jury_roles'] else 'N/A'}")
    vote_policy = debate["vote_policy"]
    lines.append(
        "- Vote policy: "
        f"method={vote_policy['method']}, "
        f"jury_weight={vote_policy['jury_vote_weight']}, "
        f"debater_weight={vote_policy['debaters_vote_weight']}, "
        f"jury_quorum={vote_policy['jury_quorum']}, "
        f"tie_breaker={vote_policy['tie_breaker']}"
    )
    lines.append("")
    lines.append("## Hierarchical Execution")
    hierarchy = blueprint["hierarchical_execution"]
    lines.append(f"- Enabled: {hierarchy['enabled']}")
    lines.append(f"- Director: {hierarchy['director'] or 'N/A'}")
    lines.append(f"- Managers: {', '.join(hierarchy['managers']) if hierarchy['managers'] else 'N/A'}")
    lines.append(f"- Workers: {', '.join(hierarchy['workers']) if hierarchy['workers'] else 'N/A'}")
    for item in hierarchy.get("manager_assignments", []):
        workers = ", ".join(item["workers"]) if item["workers"] else "none"
        lines.append(
            f"- Manager `{item['manager']}` owns workers: {workers} (focus: {item['focus']})"
        )
    lines.append("")
    lines.append("## DAG Workflow")
    dag_workflow = blueprint["dag_workflow"]
    lines.append(f"- Enabled: {dag_workflow['enabled']}")
    lines.append(f"- Nodes: {len(dag_workflow.get('nodes', []))}")
    lines.append(f"- Edges: {len(dag_workflow.get('edges', []))}")
    lines.append(f"- Max parallel nodes: {dag_workflow.get('max_parallel_nodes', 0)}")
    if dag_workflow.get("critical_path"):
        lines.append(f"- Critical path: {' -> '.join(dag_workflow['critical_path'])}")
    for group in dag_workflow.get("parallel_groups", []):
        lines.append(f"- Parallel group: {', '.join(group)}")
    lines.append("")
    lines.append("## Output Format Contract")
    output_format = blueprint["output_format"]
    lines.append(f"- Version: {output_format['version']}")
    lines.append(f"- Goal: {output_format['goal']}")
    lines.append("- Global rules:")
    for item in output_format.get("global_rules", []):
        lines.append(f"  - {item}")
    lines.append("- Document layout:")
    for item in output_format.get("document_layout", []):
        lines.append(f"  - {item}")
    lines.append("- Templates:")
    for key, value in output_format.get("templates", {}).items():
        required_fields = ", ".join(value.get("required_fields", []))
        lines.append(f"  - {key}: {required_fields}")
    lines.append("")
    if "codex_multi_agent" in blueprint:
        codex_ma = blueprint["codex_multi_agent"]
        runtime = codex_ma["sub_agent_runtime"]
        lines.append("## Codex Agent Team")
        lines.append(
            "- Sub-agent runtime: "
            f"max_threads={runtime['max_threads']}, "
            f"max_depth={runtime['max_depth']}, "
            f"job_max_runtime_seconds={runtime['job_max_runtime_seconds']}"
        )
        lines.append(f"- Mode-aware autoscaling: {runtime['mode_aware_autoscaling']}")
        lines.append(
            f"- Feature flag multi_agent: {runtime['feature_flag_enabled']}"
        )
        lines.append("### Agent Teams")
        for team in codex_ma["agent_teams"]:
            lines.append(
                f"- `{team['team']}` (wave {team['wave']}): "
                f"{team['goal']} | roles: {', '.join(team['roles'])}"
            )
        lines.append("### .codex/config.toml Draft")
        lines.append("```toml")
        lines.append(codex_ma["config_toml"].rstrip())
        lines.append("```")
        lines.append("### Role Config Files")
        for item in codex_ma["role_configs"]:
            lines.append(
                f"- `{item['config_file']}` ({item['model']}, "
                f"reasoning={item['model_reasoning_effort']}, "
                f"sandbox={item['sandbox_mode']})"
            )
        lines.append("")
    lines.append("## Spawn Prompts")
    for item in blueprint["spawn_prompts"]:
        lines.append(f"### `{item['role']}`")
        lines.append("```text")
        lines.append(item["prompt"])
        lines.append("```")
    lines.append("")
    lines.append("## Roundtable Prompt")
    lines.append("```text")
    lines.append(blueprint["roundtable_prompt"])
    lines.append("```")
    lines.append("")
    if "symphony_fusion" in blueprint:
        fusion = blueprint["symphony_fusion"]
        lines.append("## Symphony Fusion")
        for warning in fusion.get("warnings", []):
            lines.append(f"- Warning: {warning}")
        summary = fusion.get("summary", {})
        if summary:
            lines.append(f"- Project Slug: {summary.get('project_slug')}")
            lines.append(f"- Poll Interval: {summary.get('poll_interval_ms')} ms")
            lines.append(f"- Max Concurrent Agents: {summary.get('max_concurrent_agents')}")
            lines.append(f"- Max Turns: {summary.get('max_turns')}")
        lines.append("### WORKFLOW.md Draft")
        lines.append("```md")
        lines.append(fusion["workflow_md"].rstrip())
        lines.append("```")
        lines.append("")
    lines.append("## Machine Readable JSON")
    lines.append("```json")
    lines.append(json.dumps(blueprint, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    if args.min_experts < ROUNDTABLE_MIN_EXPERTS:
        raise ValueError(f"--min-experts must be >= {ROUNDTABLE_MIN_EXPERTS}")
    if args.max_experts > ROUNDTABLE_MAX_EXPERTS:
        raise ValueError(f"--max-experts must be <= {ROUNDTABLE_MAX_EXPERTS}")
    if args.min_experts > args.max_experts:
        raise ValueError("--min-experts must be <= --max-experts")
    if args.agent_team_max_threads < 0:
        raise ValueError("--agent-team-max-threads must be >= 0")
    if args.agent_team_max_depth < 1:
        raise ValueError("--agent-team-max-depth must be >= 1")
    if args.agent_team_job_max_runtime_seconds < 300:
        raise ValueError("--agent-team-job-max-runtime-seconds must be >= 300")
    if args.debate_rounds < 0:
        raise ValueError("--debate-rounds must be >= 0")
    if args.dag_max_parallel_nodes < 0:
        raise ValueError("--dag-max-parallel-nodes must be >= 0")

    task_type = infer_task_type(args.task) if args.task_type == "auto" else args.task_type
    forced_modes = parse_mode_csv(args.force_modes, "--force-modes")
    disabled_modes = parse_mode_csv(args.disable_modes, "--disable-modes")
    if args.primary_mode != "auto" and args.primary_mode in disabled_modes:
        raise ValueError("--primary-mode cannot also appear in --disable-modes")
    symphony_cfg = {
        "project_slug": args.symphony_project_slug.strip(),
        "workspace_root": args.symphony_workspace_root.strip(),
        "poll_interval_ms": args.symphony_poll_interval_ms,
        "max_concurrent_agents": args.symphony_max_concurrent_agents,
        "max_turns": args.symphony_max_turns,
        "active_states": parse_csv_list(args.symphony_active_states, SYMPHONY_DEFAULT_ACTIVE_STATES),
        "terminal_states": parse_csv_list(args.symphony_terminal_states, SYMPHONY_DEFAULT_TERMINAL_STATES),
        "codex_command": args.symphony_codex_command.strip(),
        "approval_policy": args.symphony_approval_policy.strip(),
        "thread_sandbox": args.symphony_thread_sandbox.strip(),
    }
    agent_team_cfg = {
        "max_threads": args.agent_team_max_threads,
        "max_depth": args.agent_team_max_depth,
        "job_max_runtime_seconds": args.agent_team_job_max_runtime_seconds,
        "emit_feature_flag": not args.disable_agent_team_feature_flag,
    }
    mode_cfg = {
        "primary_mode": args.primary_mode,
        "forced_modes": forced_modes,
        "disabled_modes": disabled_modes,
        "debate_rounds": args.debate_rounds,
        "dag_max_parallel_nodes": args.dag_max_parallel_nodes,
    }
    blueprint = build_blueprint(
        task=args.task.strip(),
        context=args.context.strip(),
        task_type=task_type,
        complexity=args.complexity,
        min_experts=args.min_experts,
        max_experts=args.max_experts,
        custom_specs=args.expert,
        enable_auto_experts=not args.disable_auto_experts,
        max_auto_additions=args.max_auto_additions,
        forced_coordinator=args.force_coordinator.strip(),
        runner=args.runner,
        symphony_cfg=symphony_cfg,
        agent_team_cfg=agent_team_cfg,
        mode_cfg=mode_cfg,
    )

    rendered = (
        json.dumps(blueprint, ensure_ascii=False, indent=2)
        if args.format == "json"
        else to_markdown(blueprint)
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered)
            if not rendered.endswith("\n"):
                f.write("\n")
    else:
        print(rendered)

    if args.symphony_workflow_output:
        fusion = blueprint.get("symphony_fusion")
        if not fusion:
            raise ValueError(
                "--symphony-workflow-output requires --runner symphony or --runner hybrid."
            )
        with open(args.symphony_workflow_output, "w", encoding="utf-8") as f:
            f.write(fusion["workflow_md"])
            if not fusion["workflow_md"].endswith("\n"):
                f.write("\n")

    if args.agent_team_config_output:
        codex_bundle = blueprint["codex_multi_agent"]
        with open(args.agent_team_config_output, "w", encoding="utf-8") as f:
            f.write(codex_bundle["config_toml"])
            if not codex_bundle["config_toml"].endswith("\n"):
                f.write("\n")

    if args.agent_team_roles_dir:
        codex_bundle = blueprint["codex_multi_agent"]
        os.makedirs(args.agent_team_roles_dir, exist_ok=True)
        for item in codex_bundle["role_configs"]:
            role_path = os.path.join(args.agent_team_roles_dir, f"{item['role']}.toml")
            with open(role_path, "w", encoding="utf-8") as f:
                f.write(item["content"])
                if not item["content"].endswith("\n"):
                    f.write("\n")


if __name__ == "__main__":
    main()
