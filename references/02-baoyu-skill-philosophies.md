# Baoyu's Four Skill Design Philosophies

**Source:** X article by Jason Zhu (@GoSailGlobal) summarizing Baoyu's (@dotey) D2 conference talk
**Date:** 2026-03-24
**Context:** Baoyu maintains 17 open-source Claude Code skills (~9K GitHub stars at github.com/JimLiu/baoyu-skills)

## Key Contribution

A practitioner's philosophy for skill design that prioritizes iteration speed and agent-centric thinking over upfront design rigor. Where Thariq gives you the "what" (categories, tips), Baoyu gives you the "how" — the mindset and workflow for creating skills that actually improve over time.

## The Four Philosophies

### Philosophy 1: Start with Prompts, Just Use It (先用起来)

Don't overthink the design — get a working skill fast. Three creation paths:

| Path | How It Works | When to Use |
|------|-------------|-------------|
| **A. Convert existing prompt** | Take a prompt you already use → wrap it as a skill | You already have a working prompt |
| **B. Extract from context** | After completing a task, say "extract this into a skill" | You just did something you'll repeat |
| **C. Vague idea → interview** | Describe what you want → let the agent interview you → it writes the skill | You know the goal but not the structure |

**The principle:** Low friction > high rigor for personal-use skills. A skill that exists and works 70% of the time beats a perfectly designed skill that's still in your head.

> **DS analogy:** Like prototyping a model in a notebook vs. designing a production pipeline upfront. Get the notebook working first, then refactor.

**Practical example — Path B for data scientists:**
```
You: "Analyze the impact of this ranking change on CTR and revenue"
Claude: [builds analysis, generates report]
You: "Extract the reusable parts of what you just did as a skill"
Claude: [creates a skill with: SQL templates, metric computation, report format]
```
Now you have a reusable "ranking impact analysis" skill — born from real work, not abstract design.

### Philosophy 2: Atomize Skills (原子化)

Don't make god-skills. Each skill does **one thing**. Orchestrate complex workflows by chaining atomic skills via a workflow skill or AGENTS.md.

**Why atomicity matters:**
- **Smaller context window usage** — each skill loads only what it needs
- **Focused execution** — fewer instructions = fewer ways to go wrong
- **Easier maintenance** — fix one skill without breaking others
- **Composability** — atomic skills combine in ways you didn't anticipate

**Anti-pattern:** A single "data-analysis" skill that fetches data, cleans it, analyzes it, generates visualizations, and writes a report. That's 5 skills pretending to be one.

**Atomized version of the same workflow:**
```
/pull-experiment-data    → fetches raw data, saves to file
/compute-metrics         → reads data file, outputs metric summary
/run-significance-test   → reads metric summary, outputs p-values + CIs
/generate-report         → combines all outputs into formatted report
```

Each skill is independently testable, reusable in other contexts, and maintains a small context footprint.

> **DS analogy:** Like feature engineering — one transformation per function, composed in a pipeline. You don't write a single function that does normalization + encoding + imputation + feature selection.

### Philosophy 3: Iterate Continuously, Let Agent Self-Optimize (不断迭代)

When something goes wrong, **fix the skill itself**, not just the output. The skill is the reusable artifact — the output is ephemeral.

**The diff-and-extract pattern (for writing/style skills):**
1. Agent produces a draft
2. Human edits the draft
3. Diff the AI version vs. human-edited version
4. Extract the differences as preference rules
5. Update the skill's style guide

**Real-world result:** Jason Zuo (@xxx111god) automated this loop and produced 48 style rules across 740 lines — zero hand-written. The skill learned his writing voice from his edits.

> **DS analogy:** Like online learning or active learning. The model improves from deployment feedback, not just training data. Each correction from the user is a new training signal that gets baked into the skill.

### Philosophy 4: Design from the Agent's Perspective (站在Agent角度)

Skills are instructions **for agents**, not documentation for humans. Design them the way agents work, not the way humans read.

Five principles for agent-centric design:

| Principle | What It Means | Why |
|-----------|--------------|-----|
| **Files as intermediate state** | Agents read/write files instead of holding everything in context | Context is expensive; disk is free |
| **Analyze first, then execute** | Research pass before action pass | Prevents acting on wrong assumptions |
| **Write verification criteria** | Agent self-checks its own output | Catches errors before the user sees them |
| **Sub-agent parallelism** | Split large tasks across parallel workers | Faster execution, cleaner context per worker |
| **Scripts over MCP** | Shell scripts > MCP tool servers for stable operations | MCP is context-heavy; scripts are token-efficient and more reliable |

> **DS analogy:** Like designing a ML pipeline — you don't optimize for human readability of the DAG, you optimize for the executor (Airflow, Prefect). Config files, intermediate artifacts on disk, validation checks between stages.

**"Scripts over MCP" deserves special attention:** MCP tool servers are powerful but load large tool descriptions into context. For stable operations (SQL queries, data transforms, file formatting), a Python or shell script in `scripts/` is:
- **Cheaper:** No tool description overhead per invocation
- **More reliable:** No server connection issues
- **Easier to debug:** Just a file you can read and run locally
- **Versionable:** Lives in git with the skill

Reserve MCP for dynamic tool discovery or external service integration where scripts can't reach.

## Comparing the Four Philosophies

| Philosophy | Core Question | When to Apply |
|-----------|--------------|---------------|
| Start with prompts | "How do I get this working fastest?" | Creating a new skill |
| Atomize | "Is this skill doing too many things?" | Reviewing/refactoring a skill |
| Iterate continuously | "Why did the output disappoint me?" | After a skill produces subpar results |
| Agent's perspective | "Am I writing this for a human or an agent?" | Writing any skill instruction |

## The Dual-Loop Insight

Most skill improvement focuses on one dimension. Baoyu's framework implies two orthogonal improvement loops:

```
┌─────────────────────────────────────────┐
│          DUAL-LOOP IMPROVEMENT          │
│                                         │
│  Loop 1: Eval-Driven (Correctness)      │
│  "Did the skill do the right thing?"    │
│  → Automated evals, test fixtures       │
│                                         │
│  Loop 2: Usage-Driven (Voice/Style)     │
│  "Did the skill do it the way I would?" │
│  → Diff-and-extract from human edits    │
│                                         │
│  Both loops feed back into the skill.   │
│  Correctness without voice = generic.   │
│  Voice without correctness = wrong.     │
└─────────────────────────────────────────┘
```

This maps to a concept data scientists already know: **precision vs. recall** (or accuracy vs. calibration). You need both dimensions — optimizing one while ignoring the other produces a skill that's either correct but robotic, or stylish but wrong.

## How Baoyu Complements Thariq

Thariq (Reference 01) provides the **taxonomy and tips** — the structural "what." Baoyu provides the **workflow and mindset** — the iterative "how." They're complementary:

| Dimension | Thariq's Answer | Baoyu's Answer |
|-----------|----------------|----------------|
| How to categorize a skill | 9 categories taxonomy | Single-responsibility (atomize) |
| How to write the skill | 10 writing tips | Start rough, iterate from usage |
| How to improve over time | Add to Gotchas section | Dual-loop: evals + diff-and-extract |
| How to structure files | Folder with progressive disclosure | Files as intermediate state for agents |
| How to distribute | Repo vs marketplace | Not addressed (personal-use focus) |

Use Thariq's framework to **design** the skill. Use Baoyu's philosophy to **evolve** it.

## DS-Relevant Takeaways

- **Path B ("extract from context") is the fastest skill creation method for DS work.** After you build an analysis notebook, tell Claude "extract the reusable parts as a skill." You already did the hard thinking — now capture it.
- **Atomize your analysis workflow.** Don't build one mega-skill for "experiment analysis." Build separate skills for: pull data, compute metrics, run significance tests, generate report. Chain them. You'll reuse the metric computation skill in contexts you didn't plan for.
- **The diff-and-extract pattern works for analysis templates.** If you always edit Claude's metric reports the same way (adding caveats, changing tone, restructuring sections), that's a signal to extract those preferences into the skill.
- **"Analyze first, then execute" prevents wasted compute.** In DS terms: don't run the full pipeline before checking if the data looks right. Build a research/validation phase into every skill.
- **Scripts > MCP for data operations.** If you have SQL queries, Python transforms, or CLI commands that your skills need — put them in `scripts/` as callable files. More reliable and cheaper than MCP tool servers for stable operations.
