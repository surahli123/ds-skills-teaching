# Synthesis: Key Themes Across All Skill Design References

## Reference Index

| # | Author/Source | Title | Key Contribution |
|---|--------------|-------|-----------------|
| 01 | @trq212 (Thariq, Anthropic) | Skill Design Principles — The Anthropic Playbook | 9 skill categories + 10 writing tips — the official spec for skill design |
| 02 | @dotey (Baoyu) via @GoSailGlobal | Four Skill Design Philosophies | Iteration-first mindset: start rough, atomize, self-optimize, design for agents |
| 03 | Memento-Skills (arXiv:2603.18743) | Self-Evolving Agent Patterns | 6 transferable architecture patterns: reflect→replan loop, intent gating, bounded ReAct, 3-tier context |
| 04 | Anthropic + @berryxia + @qoder_ai_ide | Harness Engineering — 10 Principles | The harness (OS) matters more than the model (CPU). Separate generation from evaluation. |
| 05 | SMA v2 + 一泽Eze | Hybrid Skill Architecture for Domain Tools | Agent reasons + code computes. Three-layer knowledge system. Token budget discipline. |
| 06 | Internal (skill-improvement repo) | AutoRefine — Iterative Skill Improvement | Comprehension before optimization. Three Gulfs framework. Agent-as-judge eval system. |
| 07 | Internal (skill-improvement repo) | Dual-Loop Design — Usage-Driven Feedback | Edit diffs as implicit feedback. Style learning + accuracy learning as complementary loops. |

## Cross-Cutting Themes

### Theme 1: Skills Are Living Documents, Not Static Specs (Refs 1, 2, 3, 6, 7)

The strongest consensus across all references: skills improve through usage, not through upfront design.

- **Thariq (01):** "Most of ours began as a few lines and a single gotcha, and got better because people kept adding to them."
- **Baoyu (02):** Start with a prompt, extract from context, iterate continuously.
- **Memento (03):** Read → Execute → Reflect → Write loop — skills rewrite themselves after each run.
- **AutoRefine (06):** Structured improvement pipeline with experiment logs — 36% → 89% accuracy over 8 experiments.
- **Dual-Loop (07):** Style rules accumulate through normal usage — zero-investment learning.

**Teaching implication:** Don't teach skills as "things you design." Teach them as "things you grow." The v1 skill is a seed; usage is the water.

### Theme 2: Context Is the Fundamental Constraint (Refs 1, 2, 3, 4, 5)

Every reference, from different angles, identifies context window management as THE bottleneck:

- **Thariq (01):** Progressive disclosure — skills are folders, not files. Load details on demand.
- **Baoyu (02):** Atomize skills (smaller context per skill). Files as intermediate state (offload to disk).
- **Memento (03):** Three-tier context — compaction (lossy summaries), scratchpad (ephemeral), memory (durable).
- **Harness (04):** Context resets beat compression. Agents communicate via files, not dialogue.
- **SMA v2 (05):** Token budget discipline — 8,500 tokens max for SKILL.md. Every instruction earns its place.

**Teaching implication:** Frame context management as "the RAM of AI" — data scientists understand memory constraints. Skills are strategies for keeping RAM usage efficient while getting work done.

### Theme 3: Separate What Agents Do Well from What Code Does Well (Refs 4, 5)

A recurring architecture principle: let agents reason and interpret; let deterministic code route, validate, and compute.

- **Harness (04):** Separate generation from evaluation. Never let the same agent judge its own work.
- **SMA v2 (05):** Agent interprets ambiguous questions and explains results. Scripts handle metric routing, computation, and quality gates.
- **Baoyu (02):** Scripts over MCP — deterministic operations belong in code, not agent context.

**Teaching implication:** This maps directly to ML pipelines. Feature engineering code is deterministic (code does it). Model selection reasoning is judgment (the scientist does it). Skills should mirror this split.

### Theme 4: Evaluation Is a First-Class Concern (Refs 4, 5, 6, 7)

Multiple references treat skill evaluation with the same rigor as model evaluation:

- **Harness (04):** Evaluator calibration — aim for 30-40% baseline failure rate. If everything passes, evals are broken.
- **SMA v2 (05):** Golden set evaluation with LLM-as-judge for subjective quality + deterministic checks for computation.
- **AutoRefine (06):** Three-phase eval: design audit → eval audit → error analysis. Validate judges (TPR/TNR) before trusting them.
- **Dual-Loop (07):** Two eval dimensions — accuracy (automated evals) + voice (diff-based style rules).

**Teaching implication:** Data scientists already know model evaluation deeply. The pitch: "skill evaluation IS model evaluation — same concepts (train/test split, calibration, precision/recall), different artifact."

### Theme 5: Start Simple, Add Complexity When Proven (Refs 2, 4, 5, 7)

Anti-over-engineering appears across multiple references:

- **Baoyu (02):** A 70% skill that exists > a perfect skill in your head. Path B: extract from what you just did.
- **Harness (04):** Principle 10 — start with 1 agent. Don't build 3-agent systems when 1 works. Shed scaffolding as models improve.
- **SMA v2 (05):** Five-phase rollout — validate before copying, supervised first run before soft launch.
- **Dual-Loop (07):** Stage A (simple diff) → B (JSONL logging) → C (AutoRefine integration). Don't build Stage C first.

**Teaching implication:** Data scientists know this as regularization — prefer the simpler model until you can prove the complex one performs measurably better. Apply the same discipline to agent architecture.

### Theme 6: Two Loops Are Better Than One (Refs 2, 6, 7)

Skill improvement has two orthogonal dimensions that must both be addressed:

| Loop | Question | Signal Source | Frequency |
|------|----------|--------------|-----------|
| Eval-Driven (Accuracy) | "Did it do the right thing?" | Automated evals, test fixtures | Dedicated improvement sessions |
| Usage-Driven (Voice) | "Did it do it my way?" | Human edit diffs | Every normal use |

- **Baoyu (02):** First to identify the dual nature — evals for correctness, diffs for style.
- **AutoRefine (06):** Operationalizes the eval-driven loop with structured experiments.
- **Dual-Loop (07):** Operationalizes the usage-driven loop with `/style-learner`.

**Teaching implication:** This maps to precision (are results correct?) vs. user satisfaction (do users like the results?) in search. A system needs both — correct but robotic output loses users; stylish but wrong output loses trust.

### Theme 7: Description Is a Trigger, Not Documentation (Refs 1, 3, 4)

How a skill is discovered and activated matters as much as what it contains:

- **Thariq (01):** "The description is not a summary — it's a description of WHEN TO TRIGGER."
- **Memento (03):** Skill Gateway Protocol — skills discovered via semantic search (BM25 + embeddings).
- **Harness (04):** Intent classification gate — DIRECT vs. AGENTIC vs. INTERRUPT determines whether to invoke skills at all.

**Teaching implication:** Think of skill descriptions as search queries in reverse. In search, the user writes a query to find documents. In skill activation, the system matches a description to the user's intent. The description IS the ranking signal.

## Key Concepts for Teaching (Ordered by Complexity)

### Level 1: Fundamentals (Everyone Must Understand)

| Concept | Source | One-Sentence Definition |
|---------|--------|----------------------|
| What is a skill? | Refs 1, 2 | A reusable instruction set that teaches an AI agent how to do a specific task in your context |
| Skill vs. prompt | Ref 2 | A prompt is one-time instructions; a skill persists across sessions and improves over time |
| The 9 categories | Ref 1 | Every skill fits one category: API reference, verification, data fetching, automation, scaffolding, code quality, CI/CD, runbooks, or infrastructure |
| Atomicity | Ref 2 | One skill = one job. Chain atomic skills for complex workflows. |
| Context as working memory | Refs 1, 3, 5 | The agent can only "see" what fits in its context window — everything else must be read from files |

### Level 2: Practical Application (Active Users)

| Concept | Source | One-Sentence Definition |
|---------|--------|----------------------|
| Progressive disclosure | Ref 1 | Skill = folder, not file. Put details in subdirectories; agent reads them when needed. |
| Gotchas section | Ref 1 | Living document of known failure modes — the highest-signal content in any skill |
| Trigger descriptions | Refs 1, 3 | Write the description for retrieval (when to activate), not documentation (what it does) |
| Hybrid split | Ref 5 | Agent reasons and interprets. Code routes, validates, and computes. Neither does the other's job. |
| Agent-centric design | Ref 2 | Files as intermediate state. Analyze first, execute second. Verification criteria built in. |
| Three creation paths | Ref 2 | Convert a prompt (A), extract from context (B), or let the agent interview you (C) |

### Level 3: Advanced Patterns (Power Users)

| Concept | Source | One-Sentence Definition |
|---------|--------|----------------------|
| Reflect → Replan loop | Ref 3 | After failure, generate a NEW plan — don't retry the same approach |
| Intent classification gate | Ref 3 | Classify input as DIRECT/AGENTIC/INTERRUPT before deciding how much machinery to invoke |
| Bounded ReAct | Ref 3 | Hard retry cap per step — prevents infinite loops, forces escalation to reflection |
| Separate generation from evaluation | Ref 4 | Never let the same agent generate AND judge its own work (GAN analogy) |
| Evaluator calibration | Refs 4, 6 | Target 30-40% baseline failure rate. If evals always pass, they're broken. |
| Three Gulfs | Ref 6 | Comprehension → Specification → Generalization. Understand failures before optimizing. |
| Dual-loop improvement | Refs 2, 6, 7 | Eval-driven (accuracy) + usage-driven (voice). Both feed back into the skill. |
| Token budget discipline | Ref 5 | Hard cap on SKILL.md size — forces prioritization of high-signal content |
| Three-tier context | Ref 3 | Compaction (lossy summaries) + scratchpad (ephemeral) + memory (durable) |
| Self-evolution | Refs 3, 4 | Skills improve from deployment experience without model retraining — all adaptation in external memory |

## Recurring Analogies (DS-Audience Teaching Aids)

| Analogy | Concept It Teaches | Source |
|---------|-------------------|--------|
| **Feature selection with budget** | Token budget for SKILL.md — every instruction must earn its place | Ref 5 |
| **Model card "Known Limitations"** | Gotchas section — updated every time the skill fails in production | Ref 1 |
| **Dashboard drill-down** | Progressive disclosure — summary by default, details on demand | Ref 1 |
| **Bayesian optimization vs. grid search** | Reflect → Replan — adapt strategy vs. retry blindly | Ref 3 |
| **Query classifier (nav/info/transactional)** | Intent classification gate — different input types need different handling | Ref 3 |
| **Data warehouse tiers (hot/warm/cold)** | Three-tier context — recent vs. summarized vs. archived | Ref 3 |
| **Airflow DAG orchestrator** | Star topology — central coordinator, tasks just do their job and report back | Ref 4 |
| **Never evaluate on training data** | Separate generation from evaluation — held-out evaluator for agent output | Ref 4 |
| **Classification threshold calibration** | Evaluator tuning — 30-40% failure rate target, not 0% | Ref 4 |
| **Checkpointing in training** | Context resets — save structured output, not process history | Ref 4 |
| **A/B test protocol** | Sprint contracts — define metrics, thresholds, and success criteria BEFORE running | Ref 4 |
| **Feature engineering pipeline** | Atomized skills — one transformation per function, composed in a pipeline | Ref 2 |
| **ML pipeline (Airflow/Prefect)** | Agent-centric design — optimize for the executor, not human readability | Ref 2 |
| **Online/active learning** | Iterative skill improvement — model improves from deployment feedback | Ref 2 |
| **Cold-start → warm-start** | Style learning upgrade path — start simple, graduate with data | Ref 7 |
| **Precision vs. user satisfaction** | Dual-loop — accuracy (correct results) + voice (results users like) | Ref 7 |
| **Implicit recommendation signals** | Edit diffs as feedback — behavior reveals preferences, not surveys | Ref 7 |
| **EDA before modeling** | Comprehension before optimization — understand failures before tuning | Ref 6 |
| **Model registry (MLflow)** | Skill schema — name, version, input/output schema, tags, metadata | Ref 3 |
| **Feature store** | Skill gateway — skills registered in catalog, discovered by query, retrieved at runtime | Ref 3 |

## Narrative Arc for Teaching

The references build naturally into a learning progression:

```
WHAT are skills?              → Refs 1, 2 (Thariq categories + Baoyu philosophies)
     ↓
HOW do you design them?       → Refs 1, 2, 5 (Writing tips + atomicity + hybrid split)
     ↓
HOW do you make them robust?  → Refs 3, 4 (Reflect/replan + harness principles)
     ↓
HOW do you improve them?      → Refs 6, 7 (AutoRefine pipeline + dual-loop feedback)
     ↓
HOW do you evaluate them?     → Refs 4, 5, 6 (Evaluator calibration + golden sets + Three Gulfs)
```

This mirrors how data scientists learn ML: what are models → how to train → how to make robust → how to improve → how to evaluate. The same arc, applied to AI agent skills.
