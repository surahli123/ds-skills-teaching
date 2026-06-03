# Live Demo: From RovoDev Workflow To Codex Receipt

Generated: 2026-06-02

Use this as the concrete demo inside the offsite. The point is not to prove that Codex replaces RovoDev CLI. The point is to show when a workflow benefits from Codex App's visible thread, artifact, receipt, and handoff.

Workshop slogan:

> Start with a workflow. End with a receipt.

## What This Demo Proves

By the end, participants should see one complete transformation:

1. an existing RovoDev-style workflow;
2. a decision about which surface should own it;
3. a Codex App worksheet;
4. a hallucination/risk check;
5. a receipt;
6. a next-session handoff.

This is a workshop-friendly demo because it turns "AI helped me" into inspectable evidence: sources, assumptions, claims, risk flags, and a next action.

## What This Demo Does Not Prove

Do not overclaim this live demo.

- It does not prove that Codex App should replace every RovoDev CLI workflow.
- It does not prove that Atlassian context is RovoDev-only. Codex App/CLI can also use Atlassian MCP when configured.
- It does not prove that every connector is available. Slack may be available where approved; Gmail and other third-party connectors may be limited, unavailable, or policy-blocked.
- It does not prove that a polished worksheet is correct. Correctness comes from the receipt and claim-level source checks.

## Demo Setup

Use one real workflow that participants already understand:

> Weekly project review: collect project context, identify blockers, decide next action, and leave a teammate-readable handoff.

Recommended input sources:

| Source | Use In Demo | Notes |
| --- | --- | --- |
| Local project folder or notes | Primary | Always safe for the demo if permissions are clear |
| Jira issue | Optional | Use RovoDev by default, or Codex App/CLI via Atlassian MCP when configured |
| Confluence page | Optional | Same caveat as Jira |
| Bitbucket or PR context | Optional | Use only if configured and relevant |
| Slack thread | Optional | Use only where approved and available |
| Gmail | Avoid for live demo | Treat as unavailable unless the actual workspace confirms it |

## Opening Script

Use this framing before the first prompt:

```text
Most people think Codex onboarding means learning features.
That is backwards.

The useful question is: where should this workflow live, and what evidence should it leave behind?

RovoDev CLI remains the most Atlassian-native default when the workflow starts from Jira or Confluence.
Codex App/CLI can also use Atlassian MCP when configured.
Cursor is strongest when the work belongs inside the editor.
Codex App is strongest when the work needs visible artifacts, receipts, and handoff.

For this demo, we will move only the artifact-and-handoff part into Codex App.
```

## Step 1: Classify The Existing Workflow

Ask participants to name a current RovoDev workflow. Then classify it before running Codex.

| Question | If Yes | Demo Decision |
| --- | --- | --- |
| Does the task start from Jira/Confluence and mostly stay there? | RovoDev CLI is likely the default | Keep source-gathering in RovoDev or Atlassian MCP |
| Does it need a visible worksheet, artifact, or handoff? | Codex App is useful | Move the artifact step into Codex App |
| Does it require source edits in an IDE? | Cursor may be better | Do not force the demo into Codex App |
| Does it require terminal automation or scripted checks? | Codex CLI may be better | Use CLI when the shell is the natural surface |
| Does it touch secrets, production mutation, or unclear ownership? | Stop | Do not automate during the workshop |

Facilitator line:

```text
We are not migrating the whole workflow. We are migrating the part that needs an inspectable artifact and a receipt.
```

## Step 2: Generate The Worksheet

Paste this prompt into Codex App with the relevant local folder open. Add optional Jira/Confluence/Slack references only if those tools are actually configured.

```text
Do a read-only weekly project review for this workspace.

Context:
- This workflow currently happens in a RovoDev-style terminal flow.
- For this demo, use Codex App to create a visible worksheet and receipt.
- Use local files first.
- If Atlassian MCP is configured, you may use Jira, Confluence, Bitbucket, or PR context that I explicitly provide.
- If Slack is configured and approved, you may use the Slack thread I explicitly provide.
- Do not use Gmail or other third-party connectors unless they are visibly enabled in this environment.
- Do not modify files until I explicitly ask.

Create a markdown worksheet with these sections:
1. Project goal
2. Current status
3. Evidence inspected
4. Blockers
5. Decisions needed
6. Risks and unknowns
7. Recommended next action
8. What would make this recommendation wrong

For every important claim, include a source anchor:
- local file path;
- Jira issue key or Confluence page title if used;
- Bitbucket/PR identifier if used;
- Slack thread reference if used;
- or "unsourced assumption" if no source supports it.

End with a short "Needs Human Check" list.
```

Expected worksheet shape:

```md
# Weekly Project Review Worksheet

## Project Goal

## Current Status

## Evidence Inspected

| Source | What It Supports | Confidence |
| --- | --- | --- |

## Blockers

## Decisions Needed

## Risks And Unknowns

## Recommended Next Action

## What Would Make This Wrong

## Needs Human Check
```

Audience checkpoint:

```text
Before trusting the worksheet, do not ask "does it sound good?"
Ask "which claims have source anchors, and which ones are guesses?"
```

## Step 3: Run The Hallucination And Risk Check

After Codex creates the worksheet, ask it to audit its own output.

```text
Audit the worksheet you just created.

Create a claim ledger with one row per important claim.

Columns:
- Claim
- Source anchor
- Evidence strength: direct / inferred / unsupported
- Hallucination risk: low / medium / high
- Operational risk: low / medium / high
- Human check required
- How to verify or correct it

Then list:
1. claims that must be removed or softened;
2. claims that need better source evidence;
3. decisions a human must make before action.

Do not make the worksheet look more certain than the evidence allows.
```

Expected claim-ledger shape:

```md
| Claim | Source Anchor | Evidence Strength | Hallucination Risk | Operational Risk | Human Check Required | Verification Path |
| --- | --- | --- | --- | --- | --- | --- |
```

Facilitator line:

```text
The risk check is the lesson. A good Codex artifact should show its uncertainty, not hide it.
```

## Step 4: Create The Receipt

Ask Codex to create a receipt that a teammate can inspect after the live session.

```text
Create a short workflow receipt for this demo.

Include:
- Goal
- Workflow surface decision
- Inputs inspected
- Tools or connectors used
- Tools or connectors intentionally not used
- Artifact created
- Verification performed
- Claims softened or removed after risk review
- Remaining risks
- Next action
- Next-session prompt

Keep it concise and teammate-readable.
```

Expected receipt shape:

```md
# Workflow Receipt

## Goal

## Surface Decision

## Inputs Inspected

## Tools Used

## Tools Not Used

## Artifact Created

## Verification

## Claims Changed After Risk Review

## Remaining Risks

## Next Action

## Next-Session Prompt
```

The receipt should explicitly say one of these:

- "Atlassian MCP was used in Codex App/CLI."
- "Atlassian MCP was available but not needed for this demo."
- "Atlassian MCP was not available in this environment, so the demo used local files only."

It should also say one of these:

- "Slack was used."
- "Slack was available but not needed."
- "Slack was not available or not approved for this demo."

For Gmail and similar third-party connectors, the safe default is:

```text
Gmail was not used. Connector availability is workspace-policy dependent and was not assumed for this demo.
```

## Step 5: Create The Handoff

End with a handoff prompt. This makes the artifact reusable instead of theatrical.

```text
Create a next-session handoff for someone who did not attend the demo.

Include:
- what workflow we tested;
- where the worksheet is;
- where the receipt is;
- what sources were inspected;
- what claims still need human validation;
- what the next person should do first;
- the exact next prompt they can paste into Codex App or Codex CLI.
```

Expected handoff shape:

```md
# Next-Session Handoff

## Workflow Tested

## Artifacts

## Sources Inspected

## Open Validation Items

## First Next Step

## Paste-Ready Next Prompt
```

## Live Facilitation Timing

| Minute | Action | Output |
| --- | --- | --- |
| 0-2 | State the routing thesis | Participants know this is a workflow demo, not a feature tour |
| 2-5 | Classify the RovoDev workflow | Surface decision |
| 5-9 | Generate worksheet | Visible Codex App artifact |
| 9-12 | Run claim ledger | Hallucination/risk check |
| 12-14 | Generate receipt | Evidence trail |
| 14-15 | Generate handoff | Repeatable next step |

## What To Inspect On Screen

Inspect these live:

- Does the worksheet cite source anchors for important claims?
- Does it separate facts, inferences, and unsupported assumptions?
- Does it avoid claiming unavailable connectors were used?
- Does it state that RovoDev CLI remains the Atlassian-native default for many Jira/Confluence-first workflows?
- Does it state that Codex App/CLI can use Atlassian MCP when configured?
- Does it name Gmail or similar third-party connectors as policy-dependent rather than assumed?
- Does the receipt identify remaining risks instead of hiding them?
- Does the handoff give the next person a concrete first step?

## Common Failure Modes

| Failure | What It Looks Like | Repair Prompt |
| --- | --- | --- |
| Overclaiming tool access | "Codex read Jira" when no Jira source was used | "Rewrite the receipt to distinguish configured tools, used tools, and unavailable tools." |
| Polished hallucination | The worksheet sounds plausible but has weak source anchors | "Downgrade every unsupported claim to an assumption or remove it." |
| RovoDev strawman | The demo implies RovoDev is only a simple CLI | "Rewrite the surface decision to say RovoDev is the Atlassian-native default." |
| Connector confusion | Gmail appears in the plan without being enabled | "Remove Gmail from the live path and list it as policy-dependent." |
| No reusable artifact | The output is only a chat answer | "Create a worksheet, receipt, and handoff as separate markdown artifacts." |

## Close The Demo

End with this:

```text
The win is not that Codex answered a question.
The win is that the workflow now leaves a worksheet, a risk ledger, a receipt, and a handoff.

If this workflow repeats next week, it is no longer just a prompt.
It is a skill candidate.
```

## Source Positioning

This demo follows the positioning in:

- [Live workshop script](02-live-workshop-script.md)
- [Tool surface comparison](05-tool-surface-comparison.md)
- [DS audience review and X-style gap analysis](../references/source-notes/ds-audience-review-x-style-gap.md)
- [Improvement plan for X-style rewrite](../references/source-notes/improvement-plan-x-style-rewrite.md)

External reference anchors:

- Atlassian Rovo Dev CLI docs: https://support.atlassian.com/rovo/docs/use-rovo-dev-cli/
- Atlassian Rovo Dev CLI MCP docs: https://support.atlassian.com/rovo/docs/connect-to-an-mcp-server-in-rovo-dev-cli/
- OpenAI Codex use cases: https://developers.openai.com/codex/use-cases
- OpenAI Codex Slack integration: https://developers.openai.com/codex/integrations/slack
