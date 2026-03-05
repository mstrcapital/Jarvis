# HEARTBEAT.md - Daily Operations

> ## ⛔ HEARTBEAT RULES
> - Context at 70%+? Write checkpoint BEFORE continuing
> - Context at 85%+? Emergency checkpoint
> - Context at 95%+? Survival mode - ask user to start new session
> - Checkpoint format: `## Checkpoint [HH:MM] — Context: XX%`
>
> ## 🦞 PROACTIVE AGENT RULES (v3.1.0)
> - **WAL Protocol:** Scan every message for corrections/decisions/proper nouns → WRITE to SESSION-STATE.md first, THEN respond
> - **Working Buffer:** At 60% context → activate buffer, log every exchange
> - **Compaction Recovery:** On startup with `<summary>` or truncated context → read working-buffer.md FIRST
> - **Relentless Resourcefulness:** Try 10 approaches before saying "can't"
> - **Verify Implementation:** Change the mechanism, not just the text

---

## Daily Checklist

### Startup (Every Session)
- [ ] Read SOUL.md, USER.md, MEMORY.md
- [ ] Check for uncompleted items from yesterday
- [ ] Assess context health
- [ ] **Compaction Recovery:** Read `memory/working-buffer.md` if session starts with context gap

### During Session
- [ ] Execute tasks proactively
- [ ] Flag risks early
- [ ] **WAL Protocol:** Write corrections/decisions/proper nouns to SESSION-STATE.md immediately
- [ ] **Working Buffer:** Check context % - activate buffer at 60%+
- [ ] Check context at ~70% - checkpoint if needed

### End of Session
- [ ] Save checkpoint if context >50%
- [ ] Note uncompleted items for next session
- [ ] Update today's log
- [ ] Flush working buffer if active

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