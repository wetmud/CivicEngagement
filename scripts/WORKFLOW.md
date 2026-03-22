# Meeting Summarizer — Workflow Notes

## The Core Pattern
**Stabilize → Commit → Iterate**
Don't iterate across the data layer, pipeline, and UI simultaneously.

---

## Rules

**1. Lock the schema before running the pipeline.**
Whisper takes 1+ hour. Before running, finalize what you want Claude to extract.
Treat the schema like a DB migration — write it, review it, commit to it.
Changing it after = full re-run.

**2. Separate build sessions from design sessions.**
- Build session: pipeline logic, schema changes, prompt upgrades
- Design session: card layout, CSS, UI iteration
Don't mix them. When you're touching the data layer, don't redesign the card.

**3. Audit before any rewrite.**
Before upgrading a prompt schema: list every current output field. Confirm each is preserved or explicitly dropped.
Before rewriting a UI component: list every feature it currently has (buttons, links, tooltips). Carry each forward intentionally.

**4. Keep a "what currently works" list at session start.**
Write down 5-6 things the current version does correctly. Treat them as protected.
Changes must explicitly address each one.

**5. Commit working states before experimenting.**
If the card looks good and pipeline runs clean → commit. Then experiment.

---

## Session Checklist

Before starting work:
- [ ] What currently works? (list it)
- [ ] What are we changing today? (data layer / pipeline / UI — pick one)
- [ ] If schema change: what fields exist now, what carries over?
- [ ] Is there a saved VTT we can re-use, or do we need a full pipeline run?

Before ending:
- [ ] Commit any working state
- [ ] Update CLAUDE.md with what changed
- [ ] Update TODO.md
