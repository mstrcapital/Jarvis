# Agent Vault Skill

## Overview

This skill teaches agents to use agent-vault for secure secret management.

## Usage

### Read config files securely

```bash
# Use agent-vault read instead of cat
agent-vault read .env
agent-vault read config.yaml
agent-vault read polymarket-scanner/config/.env
```

### Write config files

```bash
# Use agent-vault write to create/update config
agent-vault write config.yaml --content '
api_key: <agent-vault:my-key>
token: <agent-vault:my-token>
'
```

### Check if keys exist

```bash
agent-vault has polymarket-private-key
agent-vault has twitter-api-key
```

### Scan for leaks

```bash
agent-vault scan config.yaml
```

## Important Rules

1. **Never execute**: `set`, `get --reveal`, `rm`, `import` - tell user to run these
2. **Always use read**: Use `agent-vault read` instead of `cat` for secret files
3. **Always use write**: Use `agent-vault write` when creating configs with secrets
4. **Check first**: Use `agent-vault has <key>` before trying to access

## Secrets Reference

| Key | Description | Location |
|-----|-------------|----------|
| polymarket-private-key | Polymarket wallet private key | polymarket-scanner/config/.env |
| twitter-api-key | Twitter/X API key | agents/mustafa/config |

---

*This skill prevents secret leakage to AI agent providers.*