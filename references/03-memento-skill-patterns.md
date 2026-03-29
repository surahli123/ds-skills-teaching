# Memento-Skills: Self-Evolving Agent Patterns

**Source:** Memento-Skills repo (github.com/Memento-Teams/Memento-Skills, 747 stars) + arXiv:2603.18743
**Date:** 2026-03 (paper and repo)
**Note:** Memento is a standalone Python agent framework, NOT a Claude Code skill. These are transferable architectural patterns, not installable code.

## Key Contribution

Memento's core innovation is agents that learn from deployment experience without model retraining — all adaptation happens in external memory (skills). Six architectural patterns from this framework solve common problems in agent design: infinite retry loops, context overflow, over-orchestration, and skill discovery.

## Pattern 1: Read → Execute → Reflect → Write Loop

The fundamental cycle that makes skills self-improving:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  READ    │ →  │ EXECUTE  │ →  │ REFLECT  │ →  │  WRITE   │
│ (skill)  │    │ (task)   │    │ (result) │    │ (update) │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                     │
                              ┌──────┴──────┐
                              │  3-way gate │
                              ├─────────────┤
                              │ CONTINUE    │ → next step
                              │ REPLAN      │ → new approach
                              │ FINALIZE    │ → task done
                              └─────────────┘
```

**Key insight:** The reflection step doesn't just retry on failure — `REPLAN` generates a **new plan** with a different approach. This is the critical difference between "retry the same thing" (fragile) and "adapt your strategy" (robust).

> **DS analogy:** Like hyperparameter tuning with Bayesian optimization vs. grid search. Grid search retries blindly across a fixed grid. Bayesian optimization reflects on what worked and proposes a genuinely different next experiment.

### How This Applies to Skill Design

When building skills that involve multi-step workflows (e.g., "investigate a metric drop"):
- After each step, include a reflection checkpoint
- If the step failed, don't just retry — ask "should I try a completely different approach?"
- Store what was tried and why it failed, so future runs can skip dead ends

## Pattern 2: Intent Classification Gate

Before orchestrating a complex workflow, classify the user's input:

| Intent | Action | Example |
|--------|--------|---------|
| **DIRECT** | Simple reply, no tools needed | "What does NDCG stand for?" |
| **AGENTIC** | Full plan → execute → reflect loop | "Investigate why search CTR dropped 15% last week" |
| **INTERRUPT** | User wants to change direction mid-task | "Actually, focus on mobile only" |

**Why this matters:** Without intent gating, every input triggers the full orchestration pipeline. Simple follow-up questions get the same heavy treatment as complex investigation requests.

> **DS analogy:** Like a search query classifier — navigational queries ("go to settings") vs. informational queries ("how does ranking work") vs. transactional queries ("run this experiment"). Each type needs a different retrieval strategy. Treating them all the same wastes resources on simple queries and under-serves complex ones.

### How This Applies to Skill Design

Skills that handle user interaction (like a brainstorm or analysis skill) should:
- Classify the input before deciding how much machinery to spin up
- Simple clarifications don't need sub-agents
- Only trigger the full pipeline for genuinely complex requests

## Pattern 3: Hierarchical Plan-Step + Bounded ReAct

Two-layered execution prevents infinite loops:

```
OUTER LOOP: Walk through plan steps sequentially
  └── INNER LOOP (per step): Bounded ReAct
        ├── Reason: "What should I do next?"
        ├── Act: Execute the action
        ├── Observe: Check the result
        └── Budget: Max N retries per step
              └── If exhausted → Reflect → REPLAN or ABORT
```

**The budget is critical.** Without a hard retry cap, agents can burn tokens retrying a failing approach indefinitely. The cap forces escalation to the reflection layer.

> **DS analogy:** Like early stopping in model training. You set a patience parameter — if validation loss hasn't improved in N epochs, stop training and either adjust the architecture or accept the result. Without early stopping, you waste compute on a converging-to-nowhere run.

### How This Applies to Skill Design

For skills with iterative steps (data cleaning, investigation, report drafting):
- Set explicit retry limits per step (e.g., "try 3 different SQL approaches before escalating")
- When the limit hits, don't just fail — reflect on what's been tried and either replan or ask the user
- Track attempt count in the skill's working memory

## Pattern 4: Skill Gateway Protocol

Skills aren't hard-coded — they're discovered and retrieved at runtime:

```python
discover()              # → list available skills
search(query, k=5)      # → semantic retrieval (BM25 + embeddings)
execute(name, params)    # → SkillExecutionResponse
```

**Why runtime discovery matters:** New skills become available without changing the orchestrator's code. The agent finds the right skill the same way a search engine finds the right document — through relevance matching.

> **DS analogy:** Like a feature store. Features aren't hard-coded into the model — they're registered in a catalog, discovered by name or tag, and retrieved at training/inference time. New features slot in without retraining the model.

### How This Applies to Skill Design

- Write skill descriptions optimized for **retrieval**, not human documentation (mirrors Thariq's Tip #6)
- Tag skills with semantic keywords so search can find them
- Design skills with clean input/output contracts so the orchestrator can chain them without custom glue code

## Pattern 5: Three-Tier Context Management

Separate context into three layers with different lifecycles:

| Tier | Purpose | Lifecycle | DS Analogy |
|------|---------|-----------|------------|
| **Compaction** | Summarizes old conversation when context fills | Lossy, auto-evicted | Data aggregation — raw logs → daily summaries |
| **Scratchpad** | Working memory for current task | Ephemeral, structured | Notebook variables — exist during the run, gone after |
| **Memory** | Persistent facts across sessions | Durable, explicit writes | Feature store — curated, versioned, long-lived |

**Key insight:** Most agents dump everything into one context window and wonder why performance degrades. Separating tiers lets you keep the working context lean while preserving important information.

> **DS analogy:** Like a data warehouse architecture — hot storage (recent, frequently accessed), warm storage (summarized, queryable), cold storage (archived, durable). You don't query raw event logs for a dashboard; you query pre-aggregated tables.

### How This Applies to Skill Design

For skills that handle long-running tasks:
- Use files (scratchpad) for intermediate work, not context
- Summarize completed phases before starting new ones
- Store learned patterns in persistent memory for future runs

## Pattern 6: Skill Schema (Structured Contracts)

Each skill has a formal schema:

```yaml
name: metric-investigation
description: "Use when a key metric has dropped unexpectedly..."
version: 1.2.0
tags: [metrics, investigation, search-relevance]
input_schema:
  metric_name: string
  time_range: string
  comparison_baseline: string (optional)
output_schema:
  root_causes: list[string]
  confidence: float
  recommended_actions: list[string]
```

Structured schemas make skills **composable** — the output of one skill can be programmatically fed as input to another, without the orchestrator needing to understand the content.

> **DS analogy:** Like a model registry (MLflow). Each model has: name, version, signature (input/output schema), tags, and metadata. This lets you swap models, chain them, and discover them — all without knowing their internals.

## DS-Relevant Takeaways

- **The Reflect → REPLAN pattern is the single most transferable idea.** Any multi-step DS skill (investigation, analysis, report generation) benefits from asking "should I try a different approach?" instead of blindly retrying. Build reflection checkpoints into your skills.
- **Intent classification prevents over-engineering every interaction.** Not every user message to your analysis skill needs the full pipeline. A simple clarification should get a simple answer.
- **Bounded retries save tokens and sanity.** Set explicit limits on how many times a skill step can retry. Three failed SQL queries with different approaches is learning; ten retries of the same broken query is waste.
- **Three-tier context keeps long analyses coherent.** When investigating a metric drop across multiple dimensions, separate "what I've tried" (scratchpad) from "what I've concluded" (memory) from "the full conversation history" (compaction). This prevents the agent from losing its thread mid-analysis.
- **Skill schemas enable pipeline composition.** If your skills have typed inputs and outputs, you can chain "pull data" → "compute metrics" → "run significance test" → "generate report" programmatically — like a data pipeline DAG.
