# Reference 5: SMA v2 — Hybrid Skill Architecture for Domain Tools

**Source:** Internal design from Search Metric Agent (SMA) v2 refactoring project, drawing on 一泽Eze's skill design formula
**Date:** March 2026

## Key Contribution

Demonstrates a practical pattern for converting a Python-harness tool into a skill-based architecture while preserving deterministic reliability. Introduces the **hybrid split** — agents reason and interpret, scripts route and compute — as the core design principle for domain-specific AI tools.

## The Problem

The Search Metric Agent (SMA) was a Python application with 14 quality gates (C1-C14), a manifest-based routing system, and deterministic math computations. The team wanted to refactor it into Claude Code skills for flexibility, but pure skills would lose the reliability guarantees that the Python harness provided.

**The tension:** Skills are flexible but non-deterministic. Scripts are reliable but rigid. How do you get both?

## The Solution: Hybrid Architecture

### 一泽Eze's Skill Formula

A well-designed skill has exactly three components:

```
Skill = Strategic Philosophy (SKILL.md)
      + Minimum Complete Toolset (scripts/)
      + Necessary Factual Statements (references/)
```

**Strategic Philosophy** = the judgment, reasoning, and interpretation instructions (what the agent is good at). **Toolset** = the deterministic code for routing, validation, and computation (what code is good at). **Factual Statements** = the domain knowledge the agent needs to reason correctly.

### The Hybrid Split in Practice

| Responsibility | Who Handles It | Why |
|---------------|---------------|-----|
| Interpreting user questions | Agent (SKILL.md) | Requires natural language understanding, ambiguity resolution |
| Routing to the right metric/schema | Scripts (manifest lookup) | Deterministic — same input always maps to same metric |
| Computing metric values | Scripts (Python/SQL) | Math must be exact — no LLM approximation allowed |
| Explaining results to users | Agent (SKILL.md) | Requires context-aware narrative, connecting numbers to meaning |
| Validating data quality | Scripts (quality gates) | Rule-based checks — null rates, freshness thresholds |
| Diagnosing anomalies | Agent (SKILL.md) | Requires reasoning about multiple signals, forming hypotheses |

**The key decision:** Agent reasons + interprets. Scripts route + validate + compute. Neither does the other's job.

### Three-Layer Knowledge System

Domain knowledge was organized into three sub-directories, each with a specific retrieval pattern:

1. **`metric_registry/`** — Metric definitions, formulas, ownership. Used for "what is this metric?" questions.
2. **`schema_catalog/`** — Table schemas, column descriptions, join keys. Used for "where does this data live?" questions.
3. **`playbooks/`** — Diagnostic workflows for common scenarios (metric drops, A/B test interpretation). Used for "what should I do about X?" questions.

**Retrieval pattern:** Coarse filter (agent scans summaries) → Agent selects relevant files → Fetch full content. Falls back to manifest-based lookup if agent selection fails.

Each file includes `sma-metadata` headers for auto-indexing:

```yaml
# sma-metadata
metric: search_click_rate
domain: relevance
owner: search-ranking-team
last_validated: 2026-03-15
```

## Key Design Decisions

### 1. Token Budget Discipline

The SKILL.md file had a hard budget of ~8,500 tokens. Essential rules were compressed into the skill file directly — no separate `rules/` directory. This forces prioritization: every instruction must earn its place in the agent's working memory.

**DS parallel:** Like feature selection with a hard budget. You can't include every feature — you must choose the ones with the highest information gain per token.

### 2. Session State via Schema Contract

A `session.json` file tracks state across a conversation, but the agent never writes JSON directly (LLMs are unreliable at structured format generation). Instead, the harness scripts handle serialization — the agent communicates intent, the script handles format.

### 3. Three-Layer Staleness Defense

Domain knowledge goes stale. The design uses three complementary mechanisms:

| Layer | Type | How It Works |
|-------|------|-------------|
| `correct.py` script | Reactive | Users report errors → script updates the file |
| Staleness headers | Proactive | `last_validated` date in metadata → agent warns when old |
| Monthly review cadence | Organizational | Human reviews high-use files on a schedule |

**DS parallel:** Like data quality monitoring — real-time anomaly alerts (reactive), scheduled data validation jobs (proactive), and quarterly data audits (organizational).

### 4. Golden Set Evaluation

10-12 structured test scenarios validate the skill end-to-end. Each scenario has:
- A user question
- Expected routing (which metric/schema should be selected)
- Expected computation (what numbers should result)
- An LLM-as-judge assessment of explanation quality

### 5. Product Framing Matters

The CEO review reframed the project from "SMA refactoring" (internal/technical) to "Self-Service Metric Diagnosis for the Search Team" (user-facing/valuable). This changed prioritization: observability and user feedback signals moved up the roadmap.

## Rollout Strategy

A five-phase rollout reduces risk:

1. **Validate** — Confirm the agent can run the scripts in its environment
2. **Copy** — Move files into the skill directory structure
3. **Supervised first run** — Human watches the first real query end-to-end
4. **Soft launch** — Available to the team, with usage logging and feedback collection
5. **Full launch** — Default tool for metric diagnosis, with monitoring dashboards

## DS-Relevant Takeaways

- **Hybrid split (agent reasons, code computes)** is the key pattern for any domain tool where some steps require judgment and others require deterministic accuracy. Don't let the LLM do math; don't let a script interpret ambiguous questions.
- **Token budgets for skill files** are analogous to feature selection with a hard constraint — every instruction must earn its place, forcing you to prioritize high-signal content.
- **Three-layer staleness defense** (reactive + proactive + organizational) maps to data quality monitoring — you need alerts, scheduled checks, AND human audits because no single layer catches everything.
- **Product framing changes priorities.** "Refactoring an internal tool" and "building self-service diagnosis" are the same technical work but lead to different design decisions. Always name the user outcome, not the technical task.
- **Golden set evaluation with LLM-as-judge** combines deterministic checks (routing, computation) with subjective assessment (explanation quality) — a pattern directly applicable to evaluating any DS tool that produces both numbers and narratives.
