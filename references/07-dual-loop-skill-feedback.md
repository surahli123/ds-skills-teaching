# Reference 7: Dual-Loop Design — Usage-Driven Feedback for Skill Improvement

**Source:** Internal design (skill-improvement repo), approach named "The Jason Zuo" after the diff-based learning pattern
**Date:** March 2026

## Key Contribution

Introduces a **usage-driven feedback loop** that captures the gap between AI-generated output and human-edited output, then distills that gap into reusable style rules. Complements AutoRefine's eval-driven accuracy loop with a voice/preference loop that improves through normal usage rather than dedicated improvement sessions.

## The Problem

AutoRefine (Reference 6) improves skill *accuracy* — does the skill produce correct, complete output? But accuracy isn't everything. Users also care about *voice* — does it sound like me? Does it match my preferences for tone, structure, and emphasis?

Voice preferences are:
- **Hard to specify upfront.** Users can't articulate all their preferences before seeing output. ("I'll know it when I see it.")
- **Revealed through edits.** When a user edits AI output, the diff IS the feedback signal.
- **Cumulative.** Each editing session reveals a few rules. After 10 sessions, you have a style guide.

**DS parallel:** This is the cold-start problem. You can't build a user preference model before you have interaction data. You need to deploy, observe, and adapt.

## The Solution: Two Feedback Loops

### Loop 1: Style Learning (Usage-Driven)

```
AI generates output → User edits it → Diff captured →
Agent extracts rules → Rules added to style-rules.md →
Next run reads style-rules.md → Output matches preferences better
```

**The mechanism:**
1. The skill saves its output to a temp file (`/tmp/ds-review-latest.md`)
2. The user edits the output in their final document
3. Running `/style-learner` diffs the AI output against the edited version
4. An agent analyzes the diff and extracts preference rules
5. Rules append to `style-rules.md` — a persistent, growing preference file

**Example rules that emerge:**
- "Use 'we found' not 'the analysis reveals' — active voice, team attribution"
- "Lead metrics sections with the business impact number, not the methodology"
- "Never use bullet points for key findings — use numbered lists with bold headers"

### Loop 2: Accuracy Improvement (Eval-Driven)

This is AutoRefine (Reference 6) — structured auditing, eval creation, and experiment loops. It catches **correctness** problems: missing sections, wrong methodology, incomplete analysis.

### Why Two Loops?

| Dimension | Loop 1 (Style) | Loop 2 (Accuracy) |
|-----------|----------------|-------------------|
| What it catches | Voice, tone, structure preferences | Correctness, completeness, methodology |
| Signal source | Human edits (diffs) | Automated evals (judges) |
| When it runs | After every normal use | Dedicated improvement sessions |
| Investment | Zero — learning happens during work | Moderate — requires running the AutoRefine pipeline |
| Speed of learning | 1-3 rules per session | 5-10 improvements per AutoRefine run |

**The key insight:** These loops are complementary, not competitive. Accuracy improvements make the base output better. Style learning makes it *yours*. A skill needs both to feel genuinely useful.

## Architecture

### Deliverable 1: Style Learner

**`/style-learner` command** — A Claude Code slash command that:
1. Reads the AI's last output (from temp file)
2. Reads the user's edited version (user provides path)
3. Diffs them
4. Agent analyzes the diff and extracts generalizable rules
5. Appends rules to `style-rules.md`

**`style-rules.md`** — A plain-text file of accumulated preferences:
```markdown
# Style Rules for ds-review

## Voice
- Use "we" not "the analysis" — active, team-oriented
- Lead with the number, then explain methodology

## Structure
- Key findings: numbered list with bold headers, not bullets
- Always end with "Next Steps" section, max 3 items

## Tone
- Direct, not hedging. "Revenue dropped 12%" not "Revenue appears to have potentially decreased"
```

**SKILL.md integration** — The skill reads `style-rules.md` at the start of every run and applies accumulated preferences. Auto-saves output to temp for the next learning cycle.

### Deliverable 2: Skill Extraction

**`/extract-skill` meta-prompt** — After any productive Claude Code session, invoke this to capture the workflow as a draft skill. This is independent of the style loop — it captures *new capabilities* rather than *preference refinement*.

## The Upgrade Path

The design explicitly plans for growing sophistication:

| Stage | Trigger | What Changes |
|-------|---------|-------------|
| **A: Diff Script** (now) | First 10 runs | Simple diff → rule extraction. Manual trigger. |
| **B: JSONL Logging + Replay** | After 10+ runs | Structured logs of every AI output + human edit. Enables pattern analysis across sessions. |
| **C: AutoRefine Phase 8** | When proven | Style rules feed into AutoRefine's eval loop. Voice becomes a measured dimension, not just accumulated rules. |

**Why start simple:** Stage A requires zero infrastructure — just a diff command and a text file. It starts delivering value on the first use. Stages B and C add sophistication only when there's enough data to justify it.

## Success Criteria

The design defines concrete success metrics:

- **5+ rules** accumulated after 5 ds-review runs
- **Noticeably fewer manual edits** by run 10 (qualitative, user-reported)
- **At least 1 skill extracted** via `/extract-skill` in the first week

## DS-Relevant Takeaways

- **Edit diffs as implicit feedback** is the same principle behind implicit recommendation signals. Users don't fill out preference surveys — but their behavior (edits, clicks, dwell time) reveals preferences. Capture the behavioral signal, not the stated preference.
- **Cold-start → warm-start progression** (Stage A → B → C) mirrors recommendation system maturity. Start with simple rules, graduate to logged data analysis, eventually integrate into the formal evaluation loop. Don't build the sophisticated version first.
- **Complementary feedback loops** (accuracy + voice) map to precision + user satisfaction in search. A search engine can return perfectly relevant results that users hate because of poor snippet formatting. You need both relevance (accuracy) and presentation (voice).
- **Zero-investment learning** (rules accumulate through normal work) is the agent equivalent of online learning — the model improves from production traffic without dedicated retraining sessions. The key is designing the feedback capture to be frictionless.
- **Explicit upgrade triggers** (>10 runs → Stage B) prevent premature optimization. Don't build the JSONL logging infrastructure until you've proven the basic diff approach works and generates useful rules. This is validated learning, not speculative architecture.
