# Creating & Installing Your First Skill

This page walks through three ways to create skills, a hands-on example, and how to install and share them.

## Three Creation Paths

You don't need to design skills from scratch. There are three paths, ordered from lowest to highest friction:

### Path A: Convert an Existing Prompt

If you already have a prompt that works well, wrap it as a skill:

```
You: "I always start metric investigations with this prompt: [paste prompt].
     Convert this into a reusable skill."

Claude: Creates .claude/skills/metric-investigation/SKILL.md with your prompt
        as the foundation, adds structure and a Gotchas section.
```

**When to use:** You have a tried-and-tested prompt. This takes 2 minutes.

### Path B: Extract from Context (Recommended for DS)

After completing a task, capture the workflow as a skill:

```
You: "Analyze the impact of this ranking change on CTR and revenue"
Claude: [builds analysis, queries data, generates report]

You: "Extract the reusable parts of what you just did as a skill"
Claude: [creates skill with: SQL templates, metric computation, report format]
```

**When to use:** You just did something you'll do again. The agent already knows the workflow — now capture it. This is the fastest path for data scientists because you're extracting from real work, not imagining requirements.

### Path C: Interview-Driven Creation

Describe what you want and let the agent interview you:

```
You: "I need a skill for weekly metric reporting. Interview me about what it should do."

Claude: "What metrics do you track weekly?"
You: "Search CTR, NDCG@10, query success rate, zero-result rate"

Claude: "What format should the report be in?"
You: "Markdown with a summary section, metric table, week-over-week deltas, and callouts for anything that moved more than 5%"

Claude: [creates skill from your answers]
```

**When to use:** You know the goal but haven't done it manually yet. Takes longer but produces a well-structured skill.

## Hands-On: Build a "Data Quality Checker" Skill

Let's build a real skill step by step.

### Step 1: Create the Folder

```bash
mkdir -p .claude/skills/data-quality-checker/scripts
```

### Step 2: Write the SKILL.md

```markdown
---
description: "Use when the user asks to check data quality, validate a dataset,
audit a table, or says 'is this data clean?'"
---

# Data Quality Checker

## Instructions

When triggered:
1. Ask the user which table/file to check (if not specified)
2. Run the quality check script: `python scripts/check_quality.py <path>`
3. Present findings grouped by severity (blocker / warning / info)
4. Recommend next steps for any blockers

## Output Format

### Data Quality Report: {table_name}

**Overall Status:** PASS / WARN / FAIL

| Check | Status | Detail |
|-------|--------|--------|
| Null rate | ✅/⚠️/❌ | {column}: {rate}% nulls |
| Duplicates | ✅/⚠️/❌ | {count} duplicate rows on {key} |
| Freshness | ✅/⚠️/❌ | Latest record: {timestamp} |
| Outliers | ✅/⚠️/❌ | {column}: {count} values > 3σ |

**Recommended Actions:** [numbered list]

## Gotchas

- Our event tables partition by `dt` (date string), not `event_timestamp`.
  Always filter on `dt` first for performance.
- The `search_clicks` table has a known duplicate issue on the `click_id`
  column for events before 2025-06-01. Exclude those dates or deduplicate.
- Null `user_id` doesn't mean bad data — it means logged-out traffic.
  Flag it as INFO, not WARN.
```

### Step 3: Add a Helper Script

```python
# scripts/check_quality.py
"""Data quality checker — runs standard checks on a CSV or parquet file."""
import sys
import pandas as pd

def check_quality(path):
    df = pd.read_csv(path) if path.endswith('.csv') else pd.read_parquet(path)
    results = []

    # Null check
    for col in df.columns:
        null_rate = df[col].isnull().mean() * 100
        if null_rate > 10:
            results.append(('WARN', f'{col}: {null_rate:.1f}% nulls'))
        elif null_rate > 0:
            results.append(('INFO', f'{col}: {null_rate:.1f}% nulls'))

    # Duplicate check
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        results.append(('WARN', f'{dup_count} duplicate rows ({dup_count/len(df)*100:.1f}%)'))

    # Row count sanity check
    if len(df) == 0:
        results.append(('BLOCKER', 'Table is empty'))
    elif len(df) < 100:
        results.append(('WARN', f'Only {len(df)} rows — suspiciously small'))

    return results

if __name__ == '__main__':
    for severity, msg in check_quality(sys.argv[1]):
        print(f'[{severity}] {msg}')
```

### Step 4: Use It

```
You: "Check the data quality of data/experiment_results.csv"
Claude: [loads the skill, runs the script, presents formatted report]
```

That's it. The skill is live. Each time Claude makes a mistake — wrong column name, incorrect threshold — add it to the Gotchas section. The skill improves with use.

## Installation & Distribution

### Project-Level (Your Repo)

Place skills in `.claude/skills/` — they're version-controlled with the project and available to anyone who clones the repo.

```
your-repo/
├── .claude/
│   └── skills/
│       ├── metric-investigation/
│       ├── data-quality-checker/
│       └── experiment-report/
├── src/
└── ...
```

### User-Level (Your Machine)

Place skills in `~/.claude/skills/` for skills you want across all projects:

```
~/.claude/skills/
├── sql-review/         # Applies everywhere you write SQL
└── code-style/         # Your personal code style preferences
```

### Team Distribution

For larger teams, share skills via:
1. **Shared repo:** A dedicated skills repo that team members clone
2. **Internal marketplace:** At scale, a curated catalog where skills are discovered and installed

**Start with option 1.** Graduate to option 2 only when you have 20+ skills and multiple teams.

## Model Routing

Skills run on whichever model your Claude Code session uses. But when combining skills with SubAgents, you can match model to task:

| Model | Cost | Best For |
|-------|------|----------|
| **Opus** | $$$ | Complex reasoning — interpreting ambiguous questions, diagnosing anomalies |
| **Sonnet** | $$ | Standard work — running skills, generating reports, code review |
| **Haiku** | $ | Simple tasks — formatting, repetitive generation, clear-instructions execution |

**Rule of thumb:** Use Sonnet by default. Upgrade to Opus for tasks requiring judgment across multiple data sources. Downgrade to Haiku for repetitive tasks with crystal-clear instructions.

## Writing Tips (Quick Reference)

From Anthropic's official skill design guide:

| Tip | What It Means |
|-----|--------------|
| Don't state the obvious | Claude knows how to code. Teach what's specific to YOUR environment. |
| Gotchas are gold | The highest-signal content in any skill. Update after every failure. |
| Description = trigger | Write WHEN to activate, not a summary of what the skill does. |
| Avoid railroading | Give information + flexibility, not rigid step-by-step scripts. |
| Scripts > prose | For repeatable operations, put code in scripts/ instead of describing steps in prose. |
| Atomize | One skill = one job. Chain small skills for complex workflows. |

---

**Next:** [Advanced: Design Principles & Self-Improvement →](03-advanced-patterns.md)
