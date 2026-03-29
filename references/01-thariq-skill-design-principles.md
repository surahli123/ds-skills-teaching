# Thariq's Skill Design Principles — The Anthropic Playbook

**Source:** "Lessons from Building Claude Code: How We Use Skills" by @trq212 (Thariq, Anthropic)
**Date:** 2026-03-17
**Engagement:** 42.5K bookmarks

## Key Contribution

The definitive guide from Anthropic on how to design, categorize, and write effective Claude Code skills. Provides a taxonomy of 9 skill categories and 10 concrete writing tips — the closest thing to an "official spec" for skill design.

## The 9 Skill Categories

Every skill should fit exactly ONE category. If it straddles multiple, it's too broad — split it.

| # | Category | What It Does | DS Example |
|---|----------|-------------|------------|
| 1 | **Library & API Reference** | How to use a library/CLI/SDK with gotchas and snippets | "How to use our internal metrics SDK" |
| 2 | **Product Verification** | How to test/verify code works (pairs with Playwright, tmux) | "Verify dashboard renders correct charts" |
| 3 | **Data Fetching & Analysis** | Connect to data/monitoring stacks | "Pull experiment results from Snowflake" |
| 4 | **Business Process & Team Automation** | Automate repetitive workflows, save results to logs | "Weekly metric report generation" |
| 5 | **Code Scaffolding & Templates** | Generate framework boilerplate | "New A/B test analysis notebook scaffold" |
| 6 | **Code Quality & Review** | Enforce org code quality (hooks, GitHub Actions) | "Review SQL for query performance anti-patterns" |
| 7 | **CI/CD & Deployment** | Fetch, push, deploy pipelines | "Deploy model to staging endpoint" |
| 8 | **Runbooks** | Symptom → investigation → structured report | "Metric dropped — investigate root cause" |
| 9 | **Infrastructure Operations** | Routine maintenance with destructive-action guardrails | "Rotate API keys for data pipeline" |

**Why this matters:** Categories 2, 3, 4, and 8 are the sweet spot for data scientists. Most DS work lives in "fetch data → analyze → verify → report" — which maps directly to these four.

## The 10 Skill-Writing Tips

### 1. Don't State the Obvious

Claude already knows how to code. Teach it what's **specific to YOUR codebase/org** — internal APIs, naming conventions, team preferences.

> **DS analogy:** You wouldn't document "how to calculate a mean." You'd document "our team's NDCG implementation uses a custom discount function with this specific tiebreaker."

### 2. Build a Gotchas Section

> "The highest-signal content in any skill is the Gotchas section."

Gotchas grow from real failures. Every time Claude makes a mistake using the skill, add the fix to the Gotchas section. This is a living document.

> **DS analogy:** Like a model card's "Known Limitations" — except it gets updated every time the model fails in production.

### 3. Use the Filesystem & Progressive Disclosure

A skill is a **FOLDER**, not a file. Use subdirectories:
```
my-skill/
├── SKILL.md          # Main instructions (always loaded)
├── references/       # Detailed docs (read on demand)
├── assets/           # Images, templates
├── scripts/          # Helper code
└── examples/         # Example inputs/outputs
```

Claude reads files from subdirectories **at the right time** — not all upfront. This keeps the context window lean until detail is needed.

> **DS analogy:** Think progressive disclosure like a dashboard: summary view by default, drill-down on click. Don't dump every data point on the first screen.

### 4. Avoid Railroading

Give Claude **information + flexibility**, not overly specific step-by-step instructions. Overspecificity breaks on edge cases.

> **DS analogy:** Like a feature engineering pipeline — define the transformations available, let the model (or agent) decide which to apply. Don't hard-code the feature selection.

### 5. Think Through Setup

Store config in `config.json` in the skill directory. If the skill isn't configured yet, the agent asks the user interactively.

> **DS analogy:** Like environment config for a data pipeline — database credentials, table names, date ranges. Don't hard-code them; parameterize them so the skill works across environments (dev/staging/prod).

### 6. Description Field Is for the Model

> "The description is not a summary — it's a description of WHEN TO TRIGGER."

Write **trigger conditions**, not documentation summaries. The description tells Claude Code *when* to activate this skill.

```markdown
# Bad
description: "A skill for analyzing search metrics"

# Good
description: "Use when the user asks to investigate a metric drop,
compare search relevance across time periods, or generate a metric report"
```

### 7. Memory via Data Storage

Skills can persist state: append-only text logs, JSON files, or SQLite databases. Example: a standup-post skill keeps `standups.log` to remember past entries.

> **DS analogy:** Like experiment tracking (MLflow/W&B). The skill accumulates its own run history.

### 8. Store Scripts & Generate Code

> "One of the most powerful tools you can give Claude is code."

Give composable helper functions in the skill's `scripts/` directory. Claude spends its turns on **composition**, not writing boilerplate from scratch.

> **DS analogy:** Like shared utility functions in a team's Python package. Instead of every notebook re-writing the same metric calculation, import it from a shared module. The skill's `scripts/` directory IS that shared module for the agent.

**Example structure for a DS skill:**
```
metric-investigation/
├── SKILL.md
├── scripts/
│   ├── pull_metric_data.py     # Parameterized SQL query runner
│   ├── compute_significance.py # Two-sample t-test with effect size
│   └── format_report.py        # Markdown report template
└── references/
    └── metric_definitions.md   # Team's metric glossary
```

### 9. On-Demand Hooks

Skills can register hooks that activate only when the skill is invoked. Useful for opinionated hooks that would be too aggressive if always-on.

> **DS analogy:** Like conditional validation in a pipeline — run expensive data quality checks only when processing financial data, not on every routine query.

### 10. Distribution: Repo vs Marketplace

- **Small teams:** `./.claude/skills` in the repo (version-controlled with the project)
- **At scale:** Internal plugin marketplace with organic curation

> **DS analogy:** Like the progression from shared notebooks on a team drive → internal PyPI package → company-wide feature store. Start local, graduate to shared when others need it.

## Meta-Insights (Between the Lines)

These aren't stated as tips but emerge from Thariq's examples:

- **Skills grow from usage, not from design.** "Most of ours began as a few lines and a single gotcha, and got better because people kept adding to them as Claude hit new edge cases."
- **Verification skills are worth disproportionate investment.** Thariq specifically calls out spending "an engineer's full week" making verification skills excellent.
- **Skills that compose with other skills multiply their value.** A data-fetching skill + a verification skill = an automated analysis pipeline.

## Putting It Together: A DS Skill Design Checklist

When creating a new skill, walk through this checklist (derived from the 10 tips):

```
□ Which of the 9 categories does this fit? (If >1, split)
□ What does Claude NOT already know? (Tip 1: skip the obvious)
□ What breaks? (Tip 2: seed the Gotchas section with known failures)
□ What's the folder structure? (Tip 3: SKILL.md + references/ + scripts/)
□ Am I over-specifying steps? (Tip 4: information > rigid instructions)
□ What config is needed? (Tip 5: parameterize environment-specific values)
□ Does the description say WHEN to trigger? (Tip 6: trigger conditions, not summaries)
□ Does the skill need to remember anything? (Tip 7: logs, JSON, or SQLite)
□ What helper scripts would save tokens? (Tip 8: composable code > prose instructions)
□ Should hooks activate only on-demand? (Tip 9: aggressive checks gated to skill invocation)
```

## DS-Relevant Takeaways

- **Categories 3, 4, and 8 are your starting point.** Data Fetching, Business Process Automation, and Runbooks map directly to the DS workflow: pull data → analyze → diagnose → report.
- **Gotchas sections are your highest-ROI investment.** Every failed query, wrong metric definition, or pipeline quirk that Claude encounters should become a gotcha. This is how institutional knowledge compounds.
- **Progressive disclosure prevents context pollution.** Don't dump your entire data dictionary into the skill prompt. Put it in `references/` and let Claude read it when relevant — same principle as not loading all features into a model when only 5 matter.
- **Trigger descriptions are ranking signals.** Think of the description field like a search query — it determines whether the right skill gets surfaced at the right moment. Write it for recall, not for documentation.
- **Scripts > prose for repeatable operations.** If you find yourself writing "run this SQL to get X, then format it as Y" — put the SQL in a script and let Claude call it. Tokens saved, errors reduced.
