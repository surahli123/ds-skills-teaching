# Codex Tutorial

A standalone Codex onboarding tutorial for teaching how to use Codex App and Codex CLI as workflow surfaces, not just chat interfaces.

Core framing:

> Start with a workflow. End with a receipt.

## Start Here

1. [Codex 101 general](docs/01-codex-101-general.md)
2. [Live workshop script](docs/02-live-workshop-script.md)
3. [Live demo workflow receipt](docs/03-live-demo-workflow-receipt.md)
4. [Facilitator runbook](docs/04-facilitator-runbook.md)

## Follow-Up Material

- [Tool surface comparison](docs/05-tool-surface-comparison.md)
- [Skill management across tools](docs/06-skill-management-across-tools.md)
- [Advanced topics from X bookmarks](docs/07-advanced-topics-from-x-bookmarks.md)
- [Markdown image insertion pattern](docs/08-markdown-image-insertion-pattern.md)

## Visuals

The tutorial includes reusable SVG/PNG assets in [assets/](assets/), including:

- [Before/after workflow](assets/before-after-workflow.png)
- [Receipt anatomy](assets/receipt-anatomy.png)
- [Workflow routing matrix](assets/workflow-routing-matrix.png)
- [Codex App mental model](assets/codex-app-mental-model.png)

## Image Generation Prompts

The image prompts used for the tutorial live in [imagegen-prompts/](imagegen-prompts/). They are intentionally kept with the tutorial so future versions can regenerate or restyle the visuals.

## Source Notes

Planning and critique notes live in [references/source-notes/](references/source-notes/). They are not part of the main learner path, but they are useful for future maintainers.

## Verify

Run the local link checker from this folder:

```sh
node scripts/check-links.mjs
```

The checker validates local markdown links, image references, and `index.html` references.
