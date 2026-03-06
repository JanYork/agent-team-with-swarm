# Security Policy

## Scope
This project contains reusable multi-agent configuration assets for Codex and Claude Code.

## What is checked before publish
- Secret-pattern scan (common API token and private key formats).
- Personal absolute path scan (`/Users/<name>`, `/home/<name>`, `C:\Users\<name>`).
- Structural validation for required files and agent metadata.

## Reporting a security issue
Please open a private report with:
- A minimal reproduction
- Impact scope
- Suggested fix (if available)

If private channels are unavailable, open a GitHub issue with prefix `[SECURITY]` and avoid posting secrets.

## Maintainer safeguards
- Do not commit live credentials, keys, cookies, or personal tokens.
- Keep examples synthetic and non-production.
- Replace machine-specific paths with placeholders.
