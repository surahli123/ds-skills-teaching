# Markdown Image Insertion Pattern

Generated: 2026-06-02

This note applies the image pattern used in CodexGuide's `chrome-browser-plugin.md` recipe.

## Pattern To Reuse

1. Put screenshots or generated visuals in a nearby asset folder.
2. Reference them with relative Markdown paths.
3. Insert each image immediately after the step it illustrates.
4. Add one short sentence before or after the image to explain what the reader should notice.
5. Prefer stable capability/process wording over brittle button-position instructions.

## Basic Syntax

```md
![Short descriptive alt text](assets/image-name.png)
```

For a recipe in a nested folder, use the relative path from the markdown file:

```md
![Browser plugin setup screen](../images/image-20260511153510645.png)
```

For this onboarding package, the images live beside the docs in `assets/`, so use:

```md
![Workflow routing matrix](assets/imagegen-workflow-routing.png)
![Tool showcase map](assets/imagegen-tool-showcase.png)
```

## Recommended Tutorial Shape

Use the same rhythm as CodexGuide:

1. Explain the scenario.
2. Give the setup or task steps.
3. Insert the screenshot/infographic.
4. Explain what to verify.
5. Add risk or boundary notes.

Example:

```md
## Segment 3: Workflow Routing

Use this matrix when deciding whether a workflow belongs in RovoDev CLI, Cursor App, Codex App, or Codex CLI.

![Workflow routing matrix](assets/imagegen-workflow-routing.png)

Ask participants to pick one current workflow and mark the best starting surface.
```

## Why This Works

The image is not decoration. It is a checkpoint in the lesson:

- it shows the expected UI or decision frame;
- it anchors the spoken explanation;
- it gives async readers the same visual context as the live workshop;
- it lets future maintainers replace the asset without rewriting the lesson.

## CodexGuide Reference

- CodexGuide recipe: https://github.com/freestylefly/CodexGuide/blob/main/docs/recipes/chrome-browser-plugin.md
