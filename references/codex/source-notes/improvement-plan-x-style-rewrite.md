# Improvement Plan: Make The Codex Onboarding Docs Feel More Like The Bookmarked X Posts

Generated: 2026-06-02

## Goal

Improve the existing Codex onboarding package so it works better for both:

1. a live offsite/workshop;
2. written onboarding material people can read later.

The current docs are accurate, but too reference-like. The next version should be more narrative, more visual, and more artifact-driven.

Core rewrite principle:

> Start with a workflow. End with a receipt.

## What Should Change

### 1. Add A Stronger Front Door

Current `README.md` is a file index. It tells readers what exists, but not why they should care.

Improve it by adding a short opening story:

```md
# Codex Onboarding: Start With A Workflow, End With A Receipt

Most people onboard to Codex by learning features.
That is backwards.

The useful question is:

Where should this workflow live, and what evidence should it leave behind?

RovoDev CLI is the most Atlassian-native default surface.
Codex App/CLI can also connect to Atlassian MCP for Jira, Confluence, Bitbucket, and PR workflows when configured.
Cursor is best when the work belongs inside the editor.
Codex CLI/App is best when you want the GPT-model harness.
Codex App is best when the work needs visible artifacts, receipts, and handoff.
```

Then keep the existing file list below it.

### 2. Rewrite `02-offsite-codex-setup-daily-workflow.md` As A Live Script

This should be the hero doc. Right now it is a useful reference table, but it does not feel like a session people can follow.

New structure:

```md
# Live Workshop Script: Start With A Workflow, End With A Receipt

## Opening Claim
Codex is not another chat box. Codex App is a visible workflow harness.

## Act 1: Pick The Right Surface
Use RovoDev for Atlassian-native defaults.
Use Cursor for editor-native coding.
Use Codex CLI for terminal harness, including Atlassian MCP when configured.
Use Codex App for visible artifacts and handoff, including Atlassian MCP when configured.

## Act 2: Migrate One Real Workflow
Pick one RovoDev workflow participants already use.
Classify it.
Move only the parts that benefit from Codex App.

## Act 3: Produce The Artifact
Generate a worksheet / checklist / receipt.
Inspect it live.

## Act 4: Make It Repeatable
If the workflow repeats, turn it into a skill candidate for session two.
```

Keep the detailed comparison table, but move it lower or link to doc `05`.

### 3. Add One Concrete Demo Artifact

The X posts show proof. Our docs mostly show diagrams.

Add a new file:

`09-live-demo-workflow-receipt.md`

Purpose:

- One workflow participants can run during the offsite.
- One prompt.
- One expected artifact.
- One receipt.
- One handoff.

Suggested demo:

```md
Workflow: Weekly Project Review

Prompt:
Do a read-only review of this folder/project notes.
Create a markdown worksheet with:
- what this project is trying to do;
- current blockers;
- decisions needed;
- risks;
- next action;
- what evidence you used.

Then create a receipt listing files inspected, assumptions, unknowns, and next prompt.
```

This turns the session from "here is Codex" into "watch Codex create a reusable work product."

### 4. Add Two Evidence-Style Visuals

Current visuals are polished but abstract. Add visuals that look like proof.

New visual 1:

`assets/before-after-workflow.png`

Content:

- Left: one-off AI chat / terminal result / no durable artifact.
- Right: Codex App thread -> worksheet -> receipt -> handoff.

Caption:

> The value is not that Codex can answer. The value is that it can leave a reusable trail.

New visual 2:

`assets/receipt-anatomy.png`

Content:

- Goal.
- Inputs inspected.
- Tools used.
- Artifact created.
- Verification.
- Risks.
- Next prompt.

Caption:

> A receipt turns an AI answer into something a teammate can inspect.

### 5. Reframe `01-codex-101-general.md`

Keep this doc, but make it less like a glossary.

Current opening:

> Codex is a local, agentic work surface.

Better opening:

```md
Most failed Codex onboarding starts by teaching features.
Better onboarding starts with a repeated workflow.

If the work needs context, artifacts, verification, or handoff, Codex App is a good home.
If the work is just a quick terminal or editor loop, another surface may be better.
```

Then introduce concepts only when they support the workflow:

- Thread = where the workflow lives.
- AGENTS.md = rules for the workflow.
- Skill = what the workflow becomes when it repeats.
- Artifact = what the workflow produces.
- Receipt = why people can trust it.

### 6. Keep `03-skill-management...` Separate, But Add A Bridge

This doc is rightly separate. Do not merge it into Codex 101.

But the live workshop should end with a bridge:

```md
If three people repeat the same Codex prompt next week, that is no longer a prompt.
It is a skill candidate.
Session two is about how to manage those skills across RovoDev, Cursor, Codex, and Claude Code.
```

Add this bridge to the end of doc `02`.

### 7. Keep `05-tool-surface-comparison...` As The Source-Backed Appendix

Do not overstuff the live session with all web-researched detail.

Use doc `05` as the appendix that supports the simple live rule:

```md
RovoDev CLI: most Atlassian-native default workflow.
Cursor App: best editor-native coding.
Codex CLI: best terminal Codex harness; can use Atlassian MCP when configured.
Codex App: best user-friendly visual workflow and artifact surface; can use Atlassian MCP when configured.
```

### 8. Turn X Bookmark Insights Into "Teaching Claims"

Add a section to `04-advanced-topics-from-x-bookmarks.md`:

```md
## Claims Worth Teaching

1. Token hygiene:
   The problem is not that models read too much; it is that noisy command output pollutes context.

2. Skills:
   The hard part is not writing a skill once; it is preventing drift across tools and people.

3. Artifacts:
   AI output becomes useful when it becomes inspectable: HTML viewers, worksheets, receipts, dashboards.

4. Threads:
   Durable threads turn Codex from a chat box into a work surface.

5. Visual generation:
   Use generated images as teaching artifacts, but use real screenshots/receipts as proof.
```

This makes the X bookmark material feel like a distilled playbook, not an appendix dump.

## Proposed Final Document Set

Keep:

- `README.md`
- `01-codex-101-general.md`
- `02-offsite-codex-setup-daily-workflow.md`
- `03-skill-management-across-rovodev-cursor-codex.md`
- `04-advanced-topics-from-x-bookmarks.md`
- `05-tool-surface-comparison-web-research.md`
- `06-markdown-image-insertion-pattern.md`
- `07-ds-audience-review-x-style-gap.md`

Add:

- `09-live-demo-workflow-receipt.md`
- `10-facilitator-runbook.md`

Optional:

- `11-slide-outline.md`

## Proposed Visual Set

Keep:

- `imagegen-workflow-routing.png`
- `imagegen-tool-showcase.png`
- `imagegen-tutorial-ladder.png`

Add:

- `before-after-workflow.png`
- `receipt-anatomy.png`
- `live-demo-artifact-screenshot.png`
- `skill-promotion-loop.png`

## Concrete Rewrite Order

1. Rewrite `README.md` opening around the slogan.
2. Rewrite `02-offsite...` into a live script.
3. Add `09-live-demo-workflow-receipt.md`.
4. Generate `before-after-workflow.png` and `receipt-anatomy.png`.
5. Add a "Claims Worth Teaching" section to `04`.
6. Add a bridge from doc `02` to doc `03`.
7. Keep doc `05` as the factual appendix.

## Acceptance Criteria

The improved package is ready when:

- A first-time reader can summarize the workshop in one sentence.
- A participant knows which tool surface to use tomorrow.
- The live demo produces a visible artifact and receipt.
- The visuals show proof or decision points, not only concepts.
- Skill management remains separate but clearly becomes the second-session continuation.

## One-Sentence Target

The final onboarding package should teach:

> Use RovoDev when the Atlassian-native workflow is the center, Cursor when code editing is the center, Codex CLI when terminal harness is the center, and Codex App when workflow artifacts and receipts are the center. Codex can still use Atlassian MCP when configured.
