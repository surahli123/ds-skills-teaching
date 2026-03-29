# What Are Skills & When to Use Them

## What is a Skill? (30-second recap)

A **Skill** is a packaged set of instructions, scripts, and reference material that teaches an AI agent how to perform a specific task in your environment. It lives as a folder in your project and gets loaded into the agent's context when triggered.

The key difference from a prompt: a prompt is one-time instructions you type each session. A skill **persists across sessions**, improves over time, and includes helper code the agent can execute.

### The Notebook Template Analogy

As a data scientist, you probably have analysis notebook templates — a standard structure for EDA, experiment analysis, or metric reports. You copy the template, fill in the specifics, and get consistent output.

A skill is the same idea, but for your AI agent:

| Notebook Template | Skill |
|------------------|-------|
| Standard cell structure | SKILL.md instructions |
| Shared utility functions | scripts/ directory |
| Data dictionary reference | references/ directory |
| "Always check for nulls first" | Gotchas section |
| Evolves as team adds best practices | Grows from usage |

The difference: you execute the notebook manually. The agent executes the skill autonomously.

## Folder Anatomy

Every skill follows the same structure:

```
.claude/skills/metric-investigation/
├── SKILL.md              # Main instructions (always loaded when skill triggers)
│   ├── Description       # WHEN to trigger (not what it does)
│   ├── Instructions      # What to do, in what order
│   ├── Gotchas           # Known failure modes (highest-signal section)
│   └── Output Format     # What the result should look like
│
├── scripts/              # Helper code (read/called on demand)
│   ├── pull_data.py      # Parameterized SQL query runner
│   ├── compute_stats.py  # Significance testing, effect sizes
│   └── format_report.py  # Markdown report template
│
├── references/           # Domain knowledge (read on demand)
│   ├── metric_defs.md    # Metric definitions, formulas, owners
│   └── table_schemas.md  # Column descriptions, join keys
│
└── examples/             # Example inputs/outputs (optional)
    └── sample_report.md  # "Good output looks like this"
```

**Progressive disclosure:** SKILL.md is always loaded (it's small, ~8K tokens max). Everything in subdirectories is read **only when the agent needs it** — keeping the context window lean.

> **DS analogy:** Like a dashboard — summary view loads by default, you drill down into detail on click. You don't load every raw data point on the first screen.

## The 9 Skill Categories

Every skill fits exactly one category. If it straddles multiple, it's too broad — split it.

| # | Category | What It Does | DS Example |
|---|----------|-------------|------------|
| 1 | **Library & API Reference** | How to use a library/CLI/SDK with gotchas | "Our internal metrics SDK usage guide" |
| 2 | **Product Verification** | How to test/verify output works | "Verify dashboard renders correct charts" |
| 3 | **Data Fetching & Analysis** | Connect to data/monitoring stacks | "Pull experiment results from Snowflake" |
| 4 | **Business Process Automation** | Automate repetitive workflows | "Weekly metric report generation" |
| 5 | **Code Scaffolding & Templates** | Generate framework boilerplate | "New A/B test analysis notebook scaffold" |
| 6 | **Code Quality & Review** | Enforce org code quality standards | "Review SQL for performance anti-patterns" |
| 7 | **CI/CD & Deployment** | Fetch, push, deploy pipelines | "Deploy model to staging endpoint" |
| 8 | **Runbooks** | Symptom → investigation → structured report | "Metric dropped — investigate root cause" |
| 9 | **Infrastructure Operations** | Routine maintenance with guardrails | "Rotate API keys for data pipeline" |

**DS sweet spot:** Categories 3, 4, and 8 map directly to the DS workflow — pull data → analyze → diagnose → report. Start here.

## When to Use Skills

### Use Skills When:

| Signal | Example |
|--------|---------|
| You **repeat the same workflow** across sessions | "Every metric investigation follows the same steps" |
| Your team has **institutional knowledge** not in docs | "Our CTR metric excludes bot traffic — Claude doesn't know that" |
| The agent keeps **making the same mistakes** | "It always forgets our date column is UTC, not local time" |
| You want **consistent output format** | "Metric reports should always have: summary, methodology, findings, next steps" |
| The task requires **domain-specific scripts** | "Computing NDCG requires our custom discount function" |

### Don't Use Skills When:

| Signal | Example |
|--------|---------|
| Task is **one-off** and won't recur | "Help me debug this specific SQL query" |
| Claude **already knows** how to do it | "Write a Python function to sort a list" |
| The instructions would be **huge** (>10K tokens) | Consider splitting into multiple atomic skills instead |
| The task is **highly variable** each time | Exploratory analysis where every session is different |

## Skills vs SubAgents

Skills and SubAgents solve different problems. Here's how they compare:

| Dimension | Skills | SubAgents |
|-----------|--------|----------|
| **What they add** | Knowledge (new instructions) | Workers (new execution contexts) |
| **Where they run** | In the main agent's context | In an isolated context |
| **Visibility** | White box — you see reasoning | Black box — you see only the result |
| **Context impact** | Adds to context (instructions load in) | Reduces context (noisy work isolated) |
| **Best for** | Repeatable tasks with institutional knowledge | Complex/noisy tasks needing isolation |
| **Engineering analogy** | Plugin / library imported into code | Microservice called via API |

### The Decision Framework

```
Does this task recur with the same general pattern?
  ├── YES → Is there institutional knowledge the agent needs?
  │          ├── YES → Use a SKILL
  │          └── NO  → Probably just a good prompt
  │
  └── NO  → Is it complex/noisy enough to benefit from isolation?
             ├── YES → Use a SUBAGENT
             └── NO  → Just do it directly in the main agent
```

### The Power Combo: Skills + SubAgents (1+1 > 2)

The most powerful pattern combines both: load a Skill **inside** a SubAgent.

- **SubAgent alone:** Output can be inconsistent without clear instructions
- **Skill alone in main agent:** Useful, but adds to context load
- **Skill inside SubAgent:** Skill provides step-by-step guidance + output format. SubAgent provides context isolation. You get **stable, high-quality output without context pollution.**

> This is covered in depth in [Advanced Patterns](03-advanced-patterns.md).

## DS-Specific Skill Ideas to Build First

| Skill | Category | What It Does |
|-------|----------|-------------|
| **Metric Investigation** | Runbook (8) | "This metric dropped — here's how to diagnose" |
| **Experiment Report** | Business Process (4) | "Generate a standard A/B test report with significance testing" |
| **Data Quality Checker** | Verification (2) | "Check this dataset for nulls, duplicates, outliers, freshness" |
| **SQL Review** | Code Quality (6) | "Review this query for performance and correctness issues" |
| **Weekly Metrics** | Business Process (4) | "Pull and format the weekly search metrics report" |

---

**Next:** [Creating & Installing Your First Skill →](02-setup-guide.md)
