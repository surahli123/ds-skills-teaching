# Advanced: Design Principles & Self-Improvement

This page is for power users who want to build skills that are robust, self-improving, and production-grade. We cover 10 synthesized design principles, the self-improvement loop, verification as a high-ROI investment, and a real-world architecture example.

## 10 Synthesized Design Principles

These principles are distilled from 7 references — Anthropic's official guide, open-source skill builders, agent framework research, and production implementations.

### Principle 1: Agent Reasons, Code Computes

The most important architectural decision in any skill: **what does the agent handle vs. what does deterministic code handle?**

| Responsibility | Who Handles It | Why |
|---------------|---------------|-----|
| Interpreting ambiguous questions | Agent (SKILL.md) | Requires natural language understanding |
| Routing to the right metric/data source | Scripts (deterministic) | Same input → same output, every time |
| Computing metric values | Scripts (Python/SQL) | Math must be exact — no LLM approximation |
| Explaining results to users | Agent (SKILL.md) | Requires context-aware narrative |
| Validating data quality | Scripts (rule-based) | Null checks, freshness thresholds |
| Diagnosing anomalies | Agent (SKILL.md) | Requires reasoning about multiple signals |

> **DS parallel:** This is the ML pipeline split. Feature engineering code is deterministic (code does it). Model interpretation is judgment (the scientist does it).

### Principle 2: Separate Generation from Evaluation

Never let the same agent generate AND judge its own work. AI consistently rates its own output too highly.

> **DS parallel:** Never evaluate a model on its training data. You need a held-out evaluator — a different agent, a human review, or a structured test suite.

The **GAN analogy:** A generator creates output; a discriminator judges it. Neither improves without the other pushing back. Build this dynamic into your skill workflows.

### Principle 3: Evaluator Calibration (30-40% Baseline Failure)

If your skill's quality checks pass everything, they're not catching real problems. Target **30-40% failure rate on baseline outputs**.

> **DS parallel:** Like choosing a classification threshold. An eval that always passes is predicting the majority class — zero discriminative power. You need enough "signal" to detect real changes.

### Principle 4: Context Resets Beat Compression

When an agent's context fills up, clearing it with structured handoffs works better than summarizing. Summaries lose critical details and introduce bias.

**Design natural reset points** between skill phases. Each phase starts clean, receiving only the structured output from the previous phase.

> **DS parallel:** Checkpointing in a training pipeline. Save the model weights (structured output), not a summary of training. The next phase picks up from the checkpoint.

### Principle 5: Communicate via Files, Not Dialogue

When agents pass information through conversation, word choices influence how the next step interprets the task (framing bias). Structured files — JSON, markdown with defined schemas — prevent this.

> **DS parallel:** Feature pipelines write to intermediate tables, not chat messages. Each step reads a defined schema. The pipeline doesn't care about "tone."

### Principle 6: Define "Done" Before Starting

Before any skill execution, define testable success criteria. This prevents scope drift and makes evaluation objective.

> **DS parallel:** This is your experiment protocol. Define the metric, threshold, sample size, and success criteria BEFORE running the A/B test. Not after seeing results.

### Principle 7: Match Model to Task

Use the strongest model for complex reasoning, a fast model for simple lookups, and specialized models for domain tasks.

> **DS parallel:** Different compute tiers — GPU for training, CPU for inference, spot instances for batch jobs. Don't run everything on the most expensive hardware.

### Principle 8: Token Budget Discipline

Set a hard limit on SKILL.md size (~8,500 tokens). Every instruction must earn its place.

> **DS parallel:** Feature selection with a hard budget. You can't include every feature — choose the ones with the highest information gain per token of context consumed.

### Principle 9: Start Simple, Add Complexity When Proven

Don't build a 5-script skill when 1 script works. Start with the minimal version and add complexity only when you have validated evidence it's needed.

> **DS parallel:** Start with logistic regression. Add gradient boosting only when you've proven the linear model can't capture the signal. This is regularization for architecture.

### Principle 10: Shed Scaffolding as Models Improve

Complexity that was necessary for older models may become unnecessary for newer ones. Each model upgrade should trigger re-testing — not just a model name swap.

> **DS parallel:** BERT made many hand-crafted NLP features obsolete. Don't carry forward complexity that the new model handles natively. Re-evaluate your skill's scaffolding with each model generation.

## The Self-Improvement Loop

Skills don't have to be static. Two complementary loops make them better over time:

### Loop 1: Eval-Driven (AutoRefine)

A structured pipeline that improves skill **accuracy** through:

```
Gulf 1: COMPREHENSION          Gulf 2: SPECIFICATION        Gulf 3: GENERALIZATION
├── Design Audit               ├── Expand Test Fixtures     └── Experiment Loop
│   (score against rubric)     │   (30-40 diverse cases)        (mutate → eval → keep/discard)
├── Eval Audit                 ├── Write Judges
│   (are evals good enough?)   │   (code + agent-as-judge)
└── Error Analysis             └── Validate Judges
    (8 traces, categorize)         (TPR/TNR on dev set)
```

**Why the order matters:** Comprehension → Specification → Generalization. If you jump to experiments without understanding failures, you're optimizing blindly — like tuning hyperparameters on a model with data leakage.

**Real result:** The ds-trace skill went from 36% → 89% accuracy over 8 experiments using this pipeline.

### Loop 2: Usage-Driven (Dual-Loop Feedback)

Captures **voice and style preferences** through normal usage:

```
Agent generates output → User edits it → Diff captured →
Agent extracts preference rules → Rules added to style-rules.md →
Next run reads style-rules.md → Output matches preferences better
```

**Example rules that emerge:**
- "Use 'we found' not 'the analysis reveals' — active voice, team attribution"
- "Lead metric sections with the business impact number, not the methodology"
- "Never use bullet points for key findings — use numbered lists with bold headers"

One practitioner automated this loop and accumulated 48 style rules across 740 lines — zero hand-written. The skill learned their writing voice from their edits.

### Why Two Loops?

| Dimension | Loop 1 (Accuracy) | Loop 2 (Voice) |
|-----------|-------------------|----------------|
| What it catches | Correctness, completeness | Tone, structure, preferences |
| Signal source | Automated evals | Human edit diffs |
| When it runs | Dedicated improvement sessions | After every normal use |
| Investment | Moderate (run the pipeline) | Zero (learning from work) |

> **DS parallel:** Precision vs. user satisfaction in search. A search engine can return perfectly relevant results that users hate because of poor snippet formatting. You need both relevance (accuracy) and presentation (voice).

## Verification Skills: Disproportionate ROI

Anthropic's internal guidance: **"It's worth having an engineer spend a full week making verification skills excellent."**

Verification skills check whether output actually works — not just whether it looks right. This is the highest-leverage skill category for data scientists.

### What a Verification Skill Does

```
Skill generates report → Verification skill checks:
  ├── Do the numbers add up? (deterministic check)
  ├── Are all required sections present? (structural check)
  ├── Does the methodology match the question? (LLM judge)
  ├── Are confidence intervals computed correctly? (script check)
  └── Does the conclusion follow from the data? (LLM judge)
```

### Why It's High-ROI

Without verification, you're the only quality gate. With a verification skill:
- **Errors caught before you see them** — saves your review time
- **Consistent quality bar** — every run is checked the same way
- **Composable** — verification skill works with ANY analysis skill

> **DS parallel:** Like automated data validation in a pipeline (Great Expectations, dbt tests). You don't manually check every table load — automated tests catch the problems.

## Real Example: Search Metric Agent (SMA v2) Architecture

A production skill architecture for a domain-specific DS tool — investigating search metric changes.

### The Hybrid Architecture

```
.claude/skills/search-metric-agent/
├── SKILL.md                    # Agent reasoning: interpret questions, explain results
├── scripts/
│   ├── route_metric.py         # Deterministic: question → metric mapping
│   ├── compute_metric.py       # Deterministic: metric calculations
│   └── check_quality.py        # Deterministic: data quality gates
└── references/
    ├── metric_registry/        # Metric definitions, formulas, ownership
    │   └── search_ctr.md       # sma-metadata headers for auto-indexing
    ├── schema_catalog/         # Table schemas, join keys
    └── playbooks/              # Diagnostic workflows for common scenarios
```

### Three-Layer Knowledge System

| Layer | Contains | Retrieval Pattern |
|-------|---------|------------------|
| **metric_registry/** | Definitions, formulas, ownership | "What is this metric?" questions |
| **schema_catalog/** | Table schemas, columns, joins | "Where does this data live?" questions |
| **playbooks/** | Diagnostic workflows | "What should I do about X?" questions |

**Retrieval:** Agent scans summaries (coarse filter) → selects relevant files → fetches full content. Falls back to manifest-based lookup if agent selection fails.

### Three-Layer Staleness Defense

Domain knowledge goes stale. Three complementary mechanisms:

| Layer | Type | How It Works |
|-------|------|-------------|
| `correct.py` script | Reactive | Users report errors → script updates the file |
| Staleness headers | Proactive | `last_validated` date → agent warns when old |
| Monthly review | Organizational | Human reviews high-use files on schedule |

> **DS parallel:** Data quality monitoring — real-time anomaly alerts (reactive), scheduled validation jobs (proactive), quarterly data audits (organizational). No single layer catches everything.

### Golden Set Evaluation

10-12 test scenarios validate the skill end-to-end:
- A user question
- Expected routing (which metric/schema should be selected)
- Expected computation (what numbers should result)
- An LLM-as-judge assessment of explanation quality

This combines **deterministic checks** (routing, math) with **subjective assessment** (explanation quality) — a pattern directly applicable to any DS tool that produces both numbers and narratives.

## Key Takeaways

1. **Agent reasons, code computes** — the fundamental split for any domain skill. Don't let the LLM do math; don't let a script interpret ambiguous questions.
2. **Separate generation from evaluation** — build in verification as a distinct pass, not an afterthought.
3. **Skills improve through two loops** — eval-driven (accuracy) + usage-driven (voice). Both feed back into the skill.
4. **Verification skills are your highest-ROI investment** — they compound across every other skill you build.
5. **Start minimal, prove the need** — a 3-file skill that works beats a 15-file architecture that doesn't.

---

**Back to:** [Skills — What Every DS Should Know](00-parent-skills-for-ds.md)
