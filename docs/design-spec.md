# Design Spec: Teaching DS About Claude Code Skills

**Project:** ds-skills-teaching
**Date:** 2026-03-28 | **Status:** IN PROGRESS

---

## Problem

DS team members repeat the same prompts, context-setting, and workflow instructions every session. They know what agents are but don't know about Skills — the reusable, version-controlled knowledge modules that encode domain expertise, workflows, and tribal knowledge into Claude Code. Without skills, every session starts from scratch.

## Goal

Prepare teaching materials (Confluence pages + HTML slides) to teach all DS about Claude Code Skills:
- **What** they are and how they work
- **When** to use them (vs SubAgents, vs CLAUDE.md)
- **How** to create and set up their first skill
- **How** to design great skills (principles from Thariq, Baoyu, Memento, and real-world projects)

## Target Audience

All DS, mixed levels of AI agent understanding. Most know what an agent is, many have used SubAgents (from the prior teaching session), but few have created or used Skills intentionally.

## Time Budget

| Deliverable | Time |
|---|---|
| Slide deck (Loom video) | 10 min |
| Parent page | 2-3 min |
| Child 1: What & When | 5 min |
| Child 2: Setup Guide | 5 min |
| Child 3: Design Principles | 5 min |
| **Total** | **~15 min max reading** |

## Approach

### Content Sources

**Internal (memory files — already distilled):**
1. Thariq's Skill Design Principles — 9 categories, 10 writing tips
2. Baoyu's 4 Philosophies — start with prompts, atomize, iterate, agent perspective
3. Memento-Skills Patterns — reflect→write loop, intent gate, bounded ReAct
4. Harness Engineering Principles — 10 principles for multi-agent systems
5. SMA v2 Skill Architecture — Philosophy + Toolset + Facts pattern
6. AutoRefine — meta-skill for iterative improvement
7. Dual-Loop Design — usage-driven + eval-driven feedback

**External (new research — 3-5 sources):**
- Twitter/X: skill examples, antipatterns, practitioner tips
- GitHub: popular skill repos, patterns
- Blog posts: practical tutorials

### Slide Generation

Two complementary tools:
1. **`/frontend-slides`** — self-contained HTML presentation (primary deck)
2. **AAAAAJ's `/slides` prompts** — styled slide images via **Novita AI** (FLUX 2 Pro or Seedream 4.5)

### Deliverable Structure

```
ds-skills-teaching/
├── docs/design-spec.md           # This file
├── references/                    # 11-12 distilled source files
│   ├── 00-synthesis.md           # Cross-cutting themes + teaching levels
│   └── 01-11 numbered sources
├── pages/                         # 4 Confluence-ready markdown
│   ├── 00-parent-skills-for-ds.md
│   ├── 01-what-and-when.md
│   ├── 02-setup-guide.md
│   └── 03-advanced-patterns.md
├── slides/
│   └── skills-for-ds.html        # 11-slide HTML deck
└── images/                        # Novita AI generated slide images
```

## Narrative Arc (Slides)

Problem → Root Cause → Solution → Architecture → Real Example → Decision Framework → Getting Started

## Page Structure

- **Page 00 (Parent):** TL;DR + navigation hub + concept map
- **Page 01 (What & When):** Definition + folder anatomy + 9 categories + decision framework + Skills vs SubAgents
- **Page 02 (Setup Guide):** Three creation paths + step-by-step tutorial + installation
- **Page 03 (Design Principles):** 10 synthesized principles + self-improvement loop + real examples

## Checkpoints

1. ✅ Design spec approved
2. ⬜ References + synthesis reviewed
3. ⬜ Slide style picked (3 prototypes)
4. ⬜ Confluence pages reviewed
5. ⬜ HTML deck reviewed
6. ⬜ Novita AI image bake-off (FLUX 2 Pro vs Seedream 4.5)
