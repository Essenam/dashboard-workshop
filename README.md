# Dashboard workshop starter

The starting point for **Building a Live Data Quality Dashboard with Claude Code**, a hands-on
workshop by [Exagrow](https://exagrow.com) at [DAMA Days 2026](https://www.dama-mn.org/DAMA-Days-2026).

There is almost nothing here on purpose. You and Claude build the dashboard together during
the workshop. What is here is the groundwork:

- [`CLAUDE.md`](CLAUDE.md), the ground rules Claude follows while you work.
- [`PLAN.md`](PLAN.md), the plan for your dashboard. Claude fills it in with you before
  building: who it is for, the questions it answers, the data, the quality checks and how
  you will know it is done.
- [`docs/data-quality-dimensions.md`](docs/data-quality-dimensions.md), the categories of data
  quality and where they come from. Copy it into your own projects and adapt it.
- [`.claude/skills/analyze-data-quality/`](.claude/skills/analyze-data-quality/SKILL.md), a
  skill you run as `/analyze-data-quality`. It takes a dataset from picking dimensions through
  to a dashboard built on the results.
- Three more skills Claude reaches for while it builds:
  [`jobs-quote-ux`](.claude/skills/jobs-quote-ux/SKILL.md) (start from the person and work
  backwards to the technology),
  [`closed-loop-visual-feedback`](.claude/skills/closed-loop-visual-feedback/SKILL.md) (render
  it, look at it, fix it, repeat) and
  [`ux-heuristics`](.claude/skills/ux-heuristics/SKILL.md) (a usability check against Nielsen's
  ten heuristics).
- [`design-system/`](design-system/README.md), a plain default style: fonts, light and dark
  colors, a placeholder logo and icons. Claude will ask whether you have your company's own.

## Before the workshop

1. A Claude Pro account, and Claude Desktop installed.
2. Git installed.
3. A free GitHub account.
4. A personal laptop, or a work laptop where you have local admin rights.

We will take it from there together in the room.
