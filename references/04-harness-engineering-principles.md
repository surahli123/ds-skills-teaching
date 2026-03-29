# Reference 4: Harness Engineering — 10 Principles for AI Agent Systems

**Source:** Synthesized from three authors:
- Anthropic Engineering Blog (Prithvi Rajasekaran) — "Harness Design for Long-Running Applications"
- @berryxia — GAN analogy, QA rationalization problem, "faster ships" metaphor
- @qoder_ai_ide — Production multi-agent implementation with benchmarks

**Date:** March 2026

## Key Contribution

Establishes that the **harness** (the code surrounding the model) is the real product — not the model itself. Provides 10 actionable design principles for building reliable AI agent systems, drawn from production experience at Anthropic and validated by independent practitioners.

## The Core Mental Model

Think of an AI agent system like a computer:

| Component | Computer Analogy | What It Does |
|-----------|-----------------|--------------|
| Model (LLM) | CPU | Raw processing power — generates text, reasons |
| Context window | RAM | Working memory — everything the model can "see" right now |
| Harness | Operating System | Manages resources, routes tasks, enforces rules |
| Agent | Application | The end-user experience built on top of everything else |

The insight: upgrading from Sonnet to Opus (better CPU) helps, but redesigning your harness (better OS) helps more. Most quality problems are harness problems, not model problems.

## The 10 Principles

### Principle 1: Separate Generation from Evaluation

Never let the same agent generate AND judge its own work. AI consistently rates its own output too highly (self-evaluation bias).

**The GAN analogy (berryxia):** Think of GANs in deep learning — a generator creates images and a discriminator judges them. Neither improves without the other pushing back. The same dynamic applies to agent systems: one agent writes, a different agent evaluates.

**DS parallel:** This is why you never evaluate a model on its training data. The generator has seen its own reasoning — it can't objectively assess it. You need a held-out evaluator.

### Principle 2: Evaluator Tuning is the Hidden Bottleneck

QA agents tend to "rationalize away" bugs — finding explanations for why flawed output is acceptable. This mirrors a known problem in human QA: reviewers who work closely with the code start accepting its quirks.

**Fix:** Systematically review QA agent logs, compare against human judgment, and iterate the evaluator prompt. Aim for 30-40% failure rate on baseline outputs — if your evaluator passes everything, it's not catching real problems.

**DS parallel:** Like calibrating a classifier threshold. An eval that always passes (100% accuracy) is useless — it's just predicting the majority class. You need discriminative power.

### Principle 3: Context Resets Beat Compression

When an agent's context window fills up, clearing it entirely with structured handoffs works better than trying to summarize. Summaries lose critical details and introduce the summarizer's biases.

**What to do instead:** Design natural "reset points" between pipeline stages. Each stage starts with a clean context, receiving only the structured output from the previous stage — not a summary of what happened.

**DS parallel:** Like checkpointing in a training pipeline. You save the model weights (structured output), not a summary of the training process. The next stage picks up from the checkpoint without needing to know the full history.

### Principle 4: Agents Communicate via Files, Not Dialogue

When agents pass information through conversation, one agent's word choices influence how the next agent interprets the task (framing bias). Structured file artifacts — JSON, markdown with defined schemas — prevent this.

**DS parallel:** Feature engineering pipelines write to intermediate tables, not chat messages. Each step reads a defined schema and writes a defined schema. The pipeline doesn't care about the "tone" of the previous step.

### Principle 5: Define "Done" Before Starting (Sprint Contracts)

Before any work begins, the evaluator and generator agree on testable success criteria. This prevents scope drift and makes evaluation objective rather than subjective.

**DS parallel:** This is your experiment protocol. Before running an A/B test, you define: what metric, what threshold, what sample size, what counts as success. You don't decide after seeing the results.

### Principle 6: Star Topology Over Peer-to-Peer

Route all multi-agent communication through a central orchestrator. Agents never talk directly to each other.

**Why:** Peer-to-peer creates exponential state tracking (every agent must know every other agent's state). Star topology keeps one entity holding the complete picture, preventing contradictory decisions.

**DS parallel:** Like an Airflow DAG orchestrator vs. scripts calling scripts. The DAG runner knows the full dependency graph; individual tasks just do their job and report back.

### Principle 7: Match Model to Task (Cross-Model Scheduling)

Use the strongest model for complex reasoning, a fast model for simple lookups, and a multimodal model for visual verification. Quality and cost improve simultaneously.

**DS parallel:** Like using different compute tiers — GPU for training, CPU for inference, spot instances for batch jobs. You don't run everything on the most expensive hardware.

### Principle 8: Self-Evolution via Skill Extraction

When the system detects corrections, failures, or repeated user instructions, it should extract reusable patterns and persist them for future runs. The system gets better the more it's used.

**DS parallel:** Like automated feature engineering. Each model failure triggers feature analysis — what signal was missing? The next iteration includes that signal. The pipeline self-improves.

### Principle 9: Shed Scaffolding as Models Improve

Harness complexity that was necessary for older models may become unnecessary for newer ones. Each model upgrade should trigger re-testing of the system, not just a model name swap.

**The practical impact:** Anthropic found that Opus 4.6 eliminated the need for sprint decomposition and context resets that Opus 4.5 required. Entire pipeline stages became unnecessary.

**DS parallel:** Like re-evaluating your feature engineering when a more powerful model architecture arrives. BERT made many hand-crafted NLP features obsolete. Don't carry forward complexity that the new model handles natively.

### Principle 10: Complexity Follows the Task, Not the Architecture

Don't build a 3-agent system when 1 agent works fine. Start with the simplest version and add complexity only when you have validated evidence that it's needed.

**DS parallel:** Start with logistic regression. Add gradient boosting only when you've proven the linear model can't capture the signal. The Anthropic team literally REMOVED their sprint mechanism when the model proved capable enough without it.

## Qoder's 5 Limits of Single-Agent Systems

Qoder's production system identified why single agents fail at scale:

| Limit | Problem | Solution |
|-------|---------|----------|
| Context is zero-sum | More tools = less room for actual work | Role isolation (separate context per expert) |
| Cognitive switching | Asking one agent to be coder + reviewer + tester degrades all three | Specialized experts with different toolsets |
| Drift in long chains | Output quality degrades over many sequential steps | Star topology with central coordinator |
| No functional verification | "It looks right" ≠ "it works" | Dedicated verification experts (E2E, QA, code review) |
| Terminal execution risk | Agents running shell commands can cause damage | Multi-layer safety (parser + blocklist + rules + LLM check) |

**Benchmark result:** 67% higher quality than single-agent, 16% higher than Claude Code Agent Teams, at 2/3 the cost.

## DS-Relevant Takeaways

- **Separate generation from evaluation** maps directly to ML practice: never evaluate on training data, always use held-out test sets. Apply the same discipline to AI agent outputs.
- **Evaluator calibration** (30-40% baseline failure rate) is the agent equivalent of choosing a classification threshold — too lenient and you miss all the bugs; too strict and nothing ships.
- **Context resets with structured handoffs** mirror data pipeline checkpointing — save the artifact, not the process. Each stage reads a clean schema, not a chat transcript.
- **Start simple, add complexity when validated** (Principle 10) is regularization for agent architecture. Prefer the simpler system unless you can prove the complex one performs measurably better.
- **Star topology** is the Airflow/orchestrator pattern applied to agents — central coordination prevents the exponential state tracking that kills peer-to-peer pipelines.
