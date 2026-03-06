# Principles: Roundtable + Swarm Multi-Agent System

## 1. 文档目标
这份文档解释本仓库的设计原理，不讲“怎么拷文件”，而讲“为什么这样设计能稳定落地”。

适用范围：
- Codex `agent team + subagents`
- Claude Code `orchestrator + Task subagents`

## 2. 系统边界与目标
目标不是“尽可能多代理同时说话”，而是以下四件事：
1. 高质量方案生成（divergent exploration）
2. 可审计收敛决策（roundtable + debate judgement）
3. 可执行交付编排（swarm + hierarchical + DAG）
4. 证据驱动发布门禁（evidence-first release gates）

非目标：
- 不追求单次输出篇幅最大化
- 不允许无证据“拍脑袋通过”
- 不允许角色越权重写他人职责

## 3. 核心对象模型
1. `Role`：专家能力边界（如 content_creator、legal_compliance_checker）。
2. `Subagent`：角色在运行时的具体执行体（带独立提示词与交付要求）。
3. `Team`：一组为同一阶段目标服务的角色集合（discovery/design/build/assurance）。
4. `Wave`：并行执行批次（先并行发散，再并行收敛）。
5. `Gate`：阶段闸门（未满足证据条件不得推进）。
6. `Verdict`：最终判定（默认 `NEEDS_WORK`，证据充分才 `READY`）。

## 4. 六个一等公民机制

### 4.1 Roundtable（圆桌）
作用：把“并行观点”变成“可比较选项”。
方法：统一评分维度、显式 veto、记录分歧来源。
价值：避免“谁声音大谁赢”，转为结构化决策。

### 4.2 Experts（多专家）
作用：让问题在不同专业视角下并行求解。
方法：每个角色只对自己责任域负责，输出结构化卡片。
价值：降低单模型单视角偏差。

### 4.3 Debate Judgement（辩论裁决）
作用：当圆桌仍有高分歧或硬冲突时触发仲裁。
方法：陪审团角色投票 + hard-veto 规则。
价值：把“争论”变成可追溯裁决。

### 4.4 Swarm（蜂群）
作用：以任务网格并行推进，而不是串行等待。
方法：按 wave 调度多个 team 并行执行。
价值：在保持质量门禁的同时提升吞吐。

### 4.5 Hierarchical（层级）
作用：控制复杂度。
方法：director/manager/worker 分层，避免所有角色平铺互相覆盖。
价值：提升协调效率，减少提示词冲突。

### 4.6 DAG（依赖图）
作用：明确先后依赖，避免“未完成即下游开工”。
方法：关键路径 + 节点依赖 + 失败回滚策略。
价值：保证流程可预测、可恢复。

## 5. 动态创建机制（专家与蜂群）
动态不是随机扩张，而是“规则驱动扩缩容”：
1. 基于任务语义触发角色（如合规词触发 `legal_compliance_checker`）。
2. 基于阶段目标装配 team（design/build/assurance）。
3. 基于风险等级提高审查密度（触发 debate_judgement）。
4. 保持圆桌专家数量边界：`3 <= experts <= 10`。

结论：动态创建必须受约束，核心是“可解释的触发规则”。

## 6. 端到端执行流程
1. `Intake`：任务目标、约束、成功标准。
2. `Divergent Swarm`：多 team 并行产出候选方案。
3. `Roundtable Critique`：统一评分 + veto 检查。
4. `Debate Judgement`（条件触发）：冲突仲裁并给出判决。
5. `Convergent Execution`：把胜出方案收敛为实施计划。
6. `Hardening Gate`：证据、测试、合规、回滚方案齐备才放行。

## 7. 可靠性与安全原则
1. 默认不通过：证据不足时输出 `NEEDS_WORK`。
2. 明确假设：不确定结论必须标记为 assumption。
3. 角色隔离：每个 subagent 只产出职责内结论。
4. 审计留痕：评分、veto、交接单、最终 verdict 都要记录。
5. 最小泄露：文档与配置避免个人路径与敏感凭证。

## 8. Codex/Claude 落地映射

### Codex
- 运行时注册：`codex/runtime/config.swarm-roundtable.toml`
- 角色定义：`codex/runtime/agents/*.toml`
- 业务蓝图：`codex/blueprints/roundtable-swarm-demo.final.blueprint.md`

### Claude
- 总控编排器：`claude/agents/swarm-roundtable/swarm-roundtable-orchestrator.md`
- 专家代理：`claude/agents/swarm-roundtable/*.md`
- 交接模板：`claude/agents/swarm-roundtable/templates/*.md`

## 9. 设计取舍
1. 选择结构化输出而非自由长文：便于机器校验与回放。
2. 选择多阶段门禁而非一次性结论：降低“看似完整但不可执行”的风险。
3. 选择角色专精而非全能代理：提高结论可解释性与责任清晰度。
4. 选择动态扩缩容而非固定人数：在成本和质量间取得平衡。

## 10. 可验收标准
系统符合本原理时，应满足：
1. 任一结论都能追溯到角色、证据、时间点。
2. 冲突决策都能追溯到评分、veto、裁决记录。
3. 发布结论都能追溯到 hardening gate 证据。
4. 整体流程可重放，可复核，可替换角色而不改核心机制。
