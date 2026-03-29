# Skills — What Every DS Should Know

## TL;DR

A **Skill** is a reusable instruction set that teaches an AI agent how to do a specific task in your context. Think of it as a notebook template with superpowers — it includes instructions (SKILL.md), helper scripts (scripts/), and reference material (references/), organized as a folder that the agent reads on demand.

Skills solve the "Claude forgot how we do things here" problem. Instead of re-explaining your team's metric definitions, SQL conventions, and report format every session, you package that knowledge once — and the agent loads it whenever relevant.

## Why This Matters for DS

If you've used Claude Code or any AI coding agent for analysis work, you've noticed:
- You keep re-explaining the same things — metric definitions, table names, report format
- The agent makes the same mistakes across sessions — wrong column names, outdated formulas
- Quality varies wildly depending on how much context you provide upfront

Skills fix this by turning your institutional knowledge into **persistent, reusable agent instructions** that improve over time. Every mistake gets added to a Gotchas section. Every preference gets captured in a style guide. The skill gets better the more you use it.

## Concept Map

```
Skill = A folder with 3 components:

my-analysis-skill/
├── SKILL.md          # Strategic Philosophy — what to do and why
│                       (instructions, judgment calls, gotchas)
│
├── scripts/          # Minimum Complete Toolset — deterministic code
│   ├── pull_data.py    (SQL queries, data transforms)
│   └── compute.py      (metric calculations, significance tests)
│
└── references/       # Necessary Factual Statements — domain knowledge
    ├── metrics.md      (metric definitions, formulas, ownership)
    └── schemas.md      (table schemas, column descriptions)
```

**The key split:** The agent reads SKILL.md for judgment and reasoning. It calls scripts/ for deterministic computation. It reads references/ for domain knowledge — on demand, not all at once.

## What's in This Guide

| Page | Reading Time | Who It's For |
|------|-------------|-------------|
| [What Are Skills & When to Use Them](01-what-and-when.md) | 5 min | Everyone |
| [Creating & Installing Your First Skill](02-setup-guide.md) | 5 min | Active Claude Code users |
| [Advanced: Design Principles & Self-Improvement](03-advanced-patterns.md) | 5 min | Power users who want to go deeper |

## Three Things to Remember

1. **Skills are folders, not files.** A skill uses progressive disclosure — summary in SKILL.md, details in subdirectories. The agent reads what it needs, when it needs it.
2. **Skills improve through usage.** Most skills start as a few lines and a gotcha. They get better because people keep adding to them as the agent hits new edge cases.
3. **Agent reasons, code computes.** The skill tells the agent what to do; scripts handle deterministic operations like SQL queries, metric calculations, and data validation. Neither does the other's job.

---

*Last updated: 2026-03-29*
