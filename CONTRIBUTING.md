# Contributing

## Principles
- Keep orchestration deterministic and auditable.
- Keep role boundaries explicit.
- Enforce evidence-first gate decisions.

## Changes
1. Update relevant files under `codex/` or `claude/`.
2. Update `docs/SOURCES.md` when adding external references.
3. Run your local validation checks (structure, syntax, and secret scan).
4. Include change summary in pull request.

## Compatibility
- Preserve Codex runtime compatibility (`config.swarm-roundtable.toml` + role files).
- Preserve Claude frontmatter (`name`, `description`, `tools`, `color`).
