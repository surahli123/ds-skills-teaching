# Tool Surface Comparison: Rovo Dev CLI vs Cursor App vs Codex App vs Codex CLI

Generated: 2026-06-02

This comparison is based on current public documentation checked during this pass plus the workshop positioning we want to teach. The correction from the earlier draft is important: **Rovo Dev CLI should not be described as merely a fast command loop.** Atlassian's docs present it as a terminal-first agent surface with sessions, planning, saved prompts, memory, MCP, Jira/Confluence context, subagents, worktree isolation, web UI mode, and server mode. Another correction is equally important: **Atlassian context is not RovoDev-only.** Codex App/CLI can also connect to Atlassian MCP for Jira, Confluence, Bitbucket, and PR workflows when configured.

## Shared Position

Use this as the verbal framing in the room:

- **Rovo Dev CLI is the most Atlassian-native default surface.** It is a natural default when the work is fundamentally Jira/Confluence/internal-Atlassian-workflow driven.
- **Codex CLI/App can also use Atlassian MCP.** When configured, Codex can read Jira, Confluence, Bitbucket, and PR context, so do not frame Atlassian access as exclusive to RovoDev.
- **Codex CLI/App has the stronger GPT-model-based agent harness.** Use it when model capability, agentic reasoning, verification loops, artifact generation, or a friendlier visual workbench matter most.
- **Codex App is the most user-friendly Codex teaching surface.** It is easier to demo because people can see threads, artifacts, images, receipts, and handoffs instead of only terminal output.
- **Connector availability is asymmetric.** Slack can be connected where approved; Gmail and some other third-party connectors may be unavailable or incomplete depending on policy.
- **Cursor App remains the editor-first surface.** It is excellent when the center of gravity is source editing inside the IDE.

## Executive Summary

| Surface | Best Fit | Why |
| --- | --- | --- |
| Rovo Dev CLI | Atlassian-native CLI agent work | Best default when Jira, Confluence, saved prompts, memory, worktrees, and CLI/web server workflows are central |
| Cursor App | Editor-first coding and codebase navigation | Strong when the work happens inside the IDE: autonomous coding, read-only exploration, focused edits, diffs, terminal commands, and MCP-backed tools |
| Codex App | User-friendly GPT-model agent workbench | Best fit when model harness quality, visible threads, local/project context, generated artifacts, images/decks, review receipts, handoff-friendly teaching material, and configured Atlassian MCP access matter |
| Codex CLI | Terminal-first GPT-model Codex harness | Strong when the workflow belongs in shell, needs explicit approval/sandbox posture, AGENTS.md rules, MCP/config, repeatable local automation, and configured Atlassian MCP access |

## Public Documentation Findings

### Rovo Dev CLI

Public Atlassian docs describe Rovo Dev CLI as an ACLI extension that brings AI development work into the terminal and is integrated with Atlassian apps for Jira work items and Confluence content. The command docs include interactive and non-interactive runs, web UI mode, server mode, restore sessions, worktree mode, YOLO mode, configuration, MCP, saved prompts, memory, Jira configuration, plan/read-only modes, research, subagents, and hooks.

Implication for the workshop: compare Codex against Rovo Dev as another mature agent workflow surface, not as "Rovo is simple CLI, Codex is the only durable system." The fair claim is that Rovo Dev is the Atlassian-native default, while Codex can also access Atlassian data through MCP and wins on GPT-model harness plus Codex App's approachable visual onboarding.

Good migration questions:

- Do you rely on Jira/Confluence/Bitbucket context? If yes, Rovo Dev may remain the native default, but Codex App/CLI can also be viable through Atlassian MCP when configured.
- Do you rely on saved prompts or memory? Transfer the workflow contract into a shared skill or prompt, not just into a one-off Codex thread.
- Do you rely on worktree/subagent execution? Compare Rovo Dev worktree mode, Codex CLI/App subagents, and your branch hygiene before picking a default.

### Cursor App

Cursor docs frame the app around Agent modes. Agent mode can autonomously explore, edit multiple files, run commands, and fix errors; Ask mode is read-only exploration; Manual mode is targeted editing; Custom modes allow tool and instruction configuration. Cursor tools include codebase/file search, web/fetch, edits, terminal, MCP, auto-run, guardrails, and auto-fix options.

Implication for the workshop: Cursor is not just "quick navigation." It is strongest when the work should happen inside the editor with tight code review/edit/diff loops.

Good migration questions:

- Is the user actively editing source code with human review in the IDE? Cursor may be the best surface.
- Is the output a durable handoff, worksheet, slide, image, or long-running thread? Codex App may be clearer.
- Is the workflow reusable across people/tools? Promote it to a shared skill or prompt contract.

### Codex App

OpenAI's current Codex materials emphasize broad workflow and artifact use cases: understanding codebases, building and QAing apps, producing reports/decks, managing inbox/workflows, using computer/app integrations where enabled, following long-running goals, and saving repeatable workflows as skills.

Implication for the workshop: Codex App is easiest to teach as a visible GPT-model workbench: open a local/project context, ask for a bounded task, create an artifact, verify, and leave a receipt.

Good migration questions:

- Does the session need a visible artifact for teaching or handoff?
- Does the workflow need a durable thread rather than a one-off terminal session?
- Does the audience benefit from seeing the process, not just receiving a code diff?

### Codex CLI

OpenAI Help describes Codex CLI as an open-source command-line coding agent that can read, modify, and run code locally. It emphasizes installation from npm, multimodal inputs, and approval modes. The older help-center framing calls it lightweight, but current Codex positioning also points to local/cloud handoff and IDE/CLI availability, so treat CLI as a local terminal surface rather than the whole Codex story.

Implication for the workshop: Codex CLI is the closest comparison point to Rovo Dev CLI and Cursor CLI, but with the Codex/GPT-model harness. Codex App is a different comparison point: more visual, artifact-oriented, user-friendly, and session-oriented.

## Routing Rules For The Offsite

| If the workflow needs... | Start With |
| --- | --- |
| Jira/Confluence-first context and existing Rovo habits | Rovo Dev CLI by default; Codex App/CLI if Atlassian MCP is configured and GPT-model harness/artifacts matter more |
| In-editor coding, diffs, and focused source edits | Cursor App |
| GPT-model workbench, teaching, durable threads, generated artifacts, handoff receipts, configured Atlassian MCP access | Codex App |
| GPT-model terminal harness, local automation, explicit approval/sandbox posture, configured Atlassian MCP access | Codex CLI |
| Repetition across several tools | Shared skill / canonical prompt |
| Secrets, production mutation, unclear ownership, or disabled tools | Do not automate yet |

## Source Links

- Atlassian Rovo Dev CLI quickstart: https://support.atlassian.com/rovo/docs/rovo-dev-cli-quickstart-guide/
- Atlassian Rovo Dev CLI commands: https://support.atlassian.com/rovo/docs/rovo-dev-cli-commands/
- Atlassian Rovo Dev CLI memory: https://support.atlassian.com/rovo/docs/use-memory-in-rovo-dev-cli/
- Atlassian Rovo Dev CLI MCP: https://support.atlassian.com/rovo/docs/connect-to-an-mcp-server-in-rovo-dev-cli/
- Atlassian Rovo Dev CLI subagents: https://support.atlassian.com/rovo/docs/use-subagents-in-rovo-dev-cli/
- Atlassian Rovo Dev CLI worktree mode: https://support.atlassian.com/rovo/docs/use-worktree-mode-in-rovo-dev-cli/
- Cursor Agent modes: https://docs.cursor.com/agent/custom-modes
- Cursor Agent tools: https://docs.cursor.com/agent/tools
- Cursor chat overview: https://docs.cursor.com/chat/overview
- Cursor CLI overview: https://docs.cursor.com/en/cli/overview
- OpenAI Codex use cases: https://developers.openai.com/codex/explore
- OpenAI Codex CLI help: https://help.openai.com/en/articles/11096431
