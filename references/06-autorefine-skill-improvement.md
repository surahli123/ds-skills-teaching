# Reference 6: AutoRefine — Iterative Skill Improvement via Automated Research

**Source:** Internal project (skill-improvement repo), drawing on Karpathy's AutoResearch methodology and the Three Gulfs framework
**Date:** March 2026

## Key Contribution

A meta-skill that systematically improves any Claude Code skill through automated auditing, error analysis, and experiment loops. Its unique value is **comprehension before optimization** — most auto-improvement tools skip straight to mutation; AutoRefine first builds a deep understanding of why a skill fails.

## The Core Idea

Most people try to improve AI skills by tweaking the prompt and re-running. AutoRefine structures this into a disciplined pipeline with three phases, inspired by the "Three Gulfs" from interaction design:

```
Gulf 1: Comprehension   → Do I understand why this skill fails?
Gulf 2: Specification   → Can I measure failure precisely?
Gulf 3: Generalization  → Can I fix it and prove the fix works?
```

**Why this order matters:** If you jump to Gulf 3 (running experiments) without Gulf 1 (understanding failures), you're optimizing blindly. You might improve the metric while missing the real problem — like tuning hyperparameters on a model with a data leakage bug.

## The Pipeline (7 Phases)

### Gulf 1: Comprehension (Phases 1-3)

**Phase 1 — Design Audit:** Read the SKILL.md and score it against a rubric. Is the skill missing gotchas (edge cases the agent should know about)? Is the voice inconsistent? Are instructions ambiguous? This is a structural review, not a test run.

**Phase 2 — Eval Audit:** Examine the existing evaluation suite. Are there enough test cases? Is there a train/test split? Are the judges validated? A 100% pass rate on 5 test cases means nothing — it means the evals are too easy.

**Phase 3 — Error Analysis:** Generate 8 synthetic test traces and run them. Categorize failures into patterns. This phase often discovers failure modes that the skill author never anticipated.

*Example from ds-trace validation:* Phase 3 found that 75% of failures were "Analytical Artifact Absence" (the skill described analysis but never produced a concrete artifact) and 13% were "Missing Verification Step." Neither category existed before the analysis.

**HUMAN GATE:** After Gulf 1, a human reviews findings and decides whether to proceed. This prevents the system from "improving" a skill in the wrong direction.

### Gulf 2: Specification (Phases 4-6)

**Phase 4 — Expand Inputs:** Generate 30-40 test fixtures across multiple dimensions (input complexity, edge cases, domain variations). Split into Hamel Husain's recommended ratio: 15 dev / 42 train / 43 test.

**Phase 5 — Write Judges:** Create evaluation functions. Code-based judges for objective criteria (did it produce a file? is the format correct?). Agent-as-judge for subjective criteria (is the explanation clear? is the tone appropriate?).

**Key design choice:** Agent-as-judge means the coding agent itself evaluates — no external API calls needed. The agent reads a judge prompt + fixture and produces a verdict inline. This makes AutoRefine portable to any coding agent environment.

**Phase 6 — Validate Judges:** Test judges against dev set for True Positive Rate and True Negative Rate. Iterate judge prompts until they reliably catch known-good and known-bad outputs. Only then run on test set.

### Gulf 3: Generalization (Phase 7)

**Phase 7 — AutoResearch Loop:** Systematically mutate the SKILL.md, run evals, keep improvements, discard regressions. Each experiment is a single targeted change with before/after measurement.

**Budget tiers:**
- Quick: 3 experiments (fast validation)
- Standard: 5 experiments (default)
- Deep: 8-10 experiments (thorough optimization)

## Architecture Decisions

### Karpathy-Simple: 3 Core Files

Following AutoResearch's philosophy of minimal file count:

| File | Purpose |
|------|---------|
| `SKILL.md` | Orchestrator — all phase instructions inline |
| `dashboard.html` | Visual progress — step graph + bar charts + experiment details |
| `references.md` | Three Gulfs framework + audit rubric |

### Portability First

AutoRefine works on any coding agent with Read/Write/Bash — no TaskCreate, no Skill tool, no external APIs required. Enhanced features activate when Hamel's evals-skills are detected, but the core pipeline runs anywhere.

### Main-Context Execution

Critical thinking (auditing, error analysis, experiment design) stays in the main agent context. Subagents are only used for simple parallel tasks like running multiple test fixtures. This prevents the "lost nuance" problem where important reasoning gets compressed in a subagent handoff.

## Validation Results (ds-trace skill)

End-to-end test results from improving the `ds-trace` skill:

| Phase | Key Finding |
|-------|-------------|
| Phase 1 (Design Audit) | Gotchas=Missing (HIGH severity), Voice=Partial (MEDIUM) |
| Phase 2 (Eval Audit) | 4 gaps: no judge validation, no train/test split, low labeled data, no maintenance plan |
| Phase 3 (Error Analysis) | 8 traces, 100% fail rate. 6 failure categories — 2 completely new |
| Phase 7 (AutoResearch) | 8 experiments, 8/8 kept. Score: 36.1% → 88.9% (+52.8 percentage points) |

The eval suite expanded from 5 → 9 evals based on Phase 3 discoveries.

## v2.0: The Feedback Spine

The next version adds a **session log** (`session-log.json`) — a shared accumulator that captures decisions, overrides, and outcomes across runs. This enables:

- **Override logging:** When a human disagrees with the evaluator, the reason is captured and persisted
- **Judge gap detection:** Phase 7 overrides flag blind spots in the evaluation suite
- **Confidence-weighted scoring:** Weight experiment evals by their validated TPR/TNR
- **Loop-back mechanism:** When scores regress, the system explicitly routes back to Phase 5 (judge improvement) before retrying Phase 7

**Philosophy:** Two-phase improvement loop. Phase 1 (Gulfs 1-2) builds the scorer. Phase 2 (Gulf 3) uses it. Most auto-improvement tools only do Phase 2. AutoRefine's advantage is comprehension.

## DS-Relevant Takeaways

- **Comprehension before optimization** is the agent equivalent of EDA before modeling. You wouldn't tune hyperparameters without understanding your data distribution — don't tune a skill prompt without understanding its failure modes.
- **Evaluator validation (TPR/TNR)** directly parallels classifier evaluation. A judge that always says "pass" has perfect TPR but zero TNR — useless for catching regressions. Validate your judges the same way you validate your models.
- **The 30-40% baseline failure rate** is a calibration principle: if your evals pass >80% of baseline outputs, the evals are too lenient to detect regressions. Like designing an A/B test with sufficient statistical power — you need enough "signal" in the eval to detect real changes.
- **Agent-as-judge** (no external API) makes the evaluation self-contained, like having your test suite run alongside your code — no external dependencies, instant feedback, portable across environments.
- **Structured experiment logs** (session-log.json) mirror experiment tracking in ML (MLflow, W&B). Every mutation is a logged experiment with before/after metrics, enabling retrospective analysis of what types of changes work.
