# AgentTeamWithSwarm

> Roundtable + Swarm 多智能体协作模板（Codex + Claude 双栈）

## Install by Repo URL (Recommended)

把仓库链接直接发给 Codex / Claude Code，让它自动完成安装。

仓库地址：`git@github.com:JanYork/agent-team-with-swarm.git`

### 发给 Codex 的指令模板

```text
请安装这个仓库到我的 Codex 环境：git@github.com:JanYork/agent-team-with-swarm.git
要求：
1) 克隆仓库并进入目录
2) 安装 skill 到 ~/.codex/skills/
3) 安装 agents 到 ~/.codex/agents/
4) 将 codex/runtime/config.swarm-roundtable.toml 合并到 ~/.codex/config.toml
5) 返回安装结果与实际变更文件列表
```

### 发给 Claude Code 的指令模板

```text
请安装这个仓库到我的 Claude Code 环境：git@github.com:JanYork/agent-team-with-swarm.git
要求：
1) 克隆仓库并进入目录
2) 安装 agents/swarm-roundtable 到 ~/.claude/agents/
3) 安装 agents/root-agent-shortcuts/*.md 到 ~/.claude/agents/
4) 返回安装结果与实际变更文件列表
```

一个可直接复用的开源模板：帮助你用 `agent teams + subagents` 落地多专家协作、圆桌评审、辩论裁决、蜂群执行与发布门禁。

## Why

大多数多智能体项目卡在三件事：
- 角色很多，但职责边界不清
- 讨论很多，但无法收敛决策
- 输出很多，但缺少可审计发布门禁

本项目的目标是提供一套可复用、可验证、可公开发布的工程化基线。

## What You Get

- Codex 侧完整运行时配置（`[agents]` + `subagents`）
- Claude 侧完整 orchestrator + specialist agents
- 现成蓝图（team 拓扑 + roundtable/swarm 流程）
- 原理与架构文档（便于二次扩展与团队协作）

## Key Capabilities

- Roundtable：结构化评分与收敛
- Experts：专家并行产出
- Debate Judgement：冲突仲裁与 veto
- Swarm：并行执行波次
- Hierarchical：分层委派
- DAG：依赖驱动流程

硬约束：圆桌专家数量 `3..10`。

## Quick Start

### 1) 安装到 Codex

```bash
cp -R codex/skill/swarm-roundtable-orchestrator ~/.codex/skills/
cp codex/runtime/agents/*.toml ~/.codex/agents/
# 将 codex/runtime/config.swarm-roundtable.toml 合并到 ~/.codex/config.toml
```

### 2) 安装到 Claude Code

```bash
cp -R claude/agents/swarm-roundtable ~/.claude/agents/
cp claude/agents/root-agent-shortcuts/*.md ~/.claude/agents/
```

## Commands (Codex / Claude Code)

说明：
- 下面的 `/<command>` 是本仓库定义的统一命令层，由 skill/agent 解释执行。
- 不是平台内置固定命令。
- Stigmergy 信号默认自动发出与自动发现；`/signal` 主要用于观察。

### 通用命令与作用

| 命令 | 作用 |
| --- | --- |
| `/help` | 显示命令列表与默认模式 |
| `/plan <task>` | 生成标准多智能体蓝图 |
| `/roundtable <task>` | 强化专家评分与收敛 |
| `/swarm <task>` | 强化并行分解与执行拓扑 |
| `/debate <task>` | 触发辩论裁决流程 |
| `/full <task>` | 运行全模式融合流程 |
| `/experts list` | 查看当前专家与职责 |
| `/experts add ...` | 动态追加专家 |
| `/experts remove <role>` | 移除指定专家 |
| `/experts bounds <min> <max>` | 调整专家数量边界（3..10） |
| `/consensus <scores_json_path>` | 执行确定性加权共识计算 |
| `/status` | 查看当前模式/门禁/下一步 |
| `/finalize` | 输出 READY/NEEDS_WORK 结论与证据，并自动触发 `/signal close` 清理足迹 |
| `/signal tail [limit]` | 查看最近信号足迹 |
| `/signal topic <topic> [limit]` | 查看某主题信号 |
| `/signal trace <trace_id>` | 查看一次完整执行轨迹 |
| `/signal stats` | 查看信号统计与热点 |
| `/signal close [run_id]` | 结束任务并清理信号足迹（默认） |

### Codex 用法

1. 按 Quick Start 安装 skill 与 agents 配置。
2. 在任务输入中直接使用上述 `/<command>`。
3. 需要离线生成蓝图时，可使用：

```bash
python3 codex/skill/swarm-roundtable-orchestrator/scripts/swarm_roundtable_plan.py --task "<task>" --context "<context>" --format markdown
```

### Claude Code 用法

1. 激活 `Swarm Roundtable Orchestrator`。
2. 在会话输入中直接使用上述 `/<command>`。
3. 需要子代理并行时，orchestrator 会用 `Task` 自动拉起专家协作。

## Repository Map

```text
AgentTeamWithSwarm/
├── codex/
│   ├── skill/swarm-roundtable-orchestrator/
│   ├── runtime/
│   │   ├── config.swarm-roundtable.toml
│   │   └── agents/*.toml
│   └── blueprints/
│       ├── roundtable-swarm-demo.final.blueprint.md
│       ├── roundtable-swarm-demo.final.codex-config.toml
│       └── roundtable-swarm-demo.final-agents/*.toml
├── claude/agents/
│   ├── swarm-roundtable/*.md
│   └── root-agent-shortcuts/*.md
└── docs/
```

## Documentation

- 原理说明：[docs/PRINCIPLES.md](docs/PRINCIPLES.md)
- 架构映射：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 命令规范：[docs/COMMANDS.md](docs/COMMANDS.md)
- 蜂群信号机制：[docs/STIGMERGY_SIGNALS.md](docs/STIGMERGY_SIGNALS.md)
- 来源说明：[docs/SOURCES.md](docs/SOURCES.md)
- 开源审查：[docs/OPEN_SOURCE_REVIEW.md](docs/OPEN_SOURCE_REVIEW.md)

## License

Apache-2.0, see [LICENSE](LICENSE).
