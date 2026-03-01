# HEARTBEAT.md - Daily Operations

> ## ⛔ HEARTBEAT RULES
> - Context at 70%+? Write checkpoint BEFORE continuing
> - Context at 85%+? Emergency checkpoint
> - Context at 95%+? Survival mode - ask user to start new session
> - Checkpoint format: `## Checkpoint [HH:MM] — Context: XX%`

---

## Daily Checklist

### Startup (Every Session)
- [ ] Read SOUL.md, USER.md, MEMORY.md
- [ ] Check for uncompleted items from yesterday
- [ ] Assess context health

### During Session
- [ ] Execute tasks proactively
- [ ] Flag risks early
- [ ] Write important decisions to memory immediately
- [ ] Check context at ~70% - checkpoint if needed

### End of Session
- [ ] Save checkpoint if context >50%
- [ ] Note uncompleted items for next session
- [ ] Update today's log

---

## Context Thresholds

| Context % | Status | Action |
|-----------|--------|--------|
| < 50% | 🟢 Normal | Continue normally |
| 50-69% | 🟡 Vigilant | Note internally |
| 70-84% | 🟠 Active | **Checkpoint NOW** |
| 85-94% | 🔴 Emergency | Emergency flush |
| 95%+ | ⚫ Critical | Ask for new session |

---

## Commands Reference

- `status` - System health dashboard
- `show persona` - View SOUL.md summary
- `health check` - Full workspace validation
- `checkpoint` - Force checkpoint

---

*AI Persona OS v1.4.0 - Jarvis Heartbeat*