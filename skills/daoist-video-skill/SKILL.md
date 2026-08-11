---
name: daoist-video-skill
description: Use when the user wants to create, plan, review, or resume a Chinese short video about Daoist inspiration, Eastern philosophy, daily relationships, or emotional insight through a staged workflow with human approval checkpoints, scripts, storyboards, voice previews, asset tracking, QA, and publish-ready output.
license: Proprietary — original user-authored workflow
---

# Daoist Video Skill

## Purpose

Use this skill to turn an idea for a Chinese Eastern-philosophy short video into a traceable, recoverable production task. The workflow favors deliberate checkpoints over unattended publishing.

Default creative direction:

- Daoist-inspired reflection, relationships, emotions, and everyday insight
- Hook → point of view → open-ended closing
- Five-shot visual structure with a consistent persona and visual language
- Read `pipeline_config.json` as the source of truth for aspect ratio, resolution, duration, and stage order

## Non-negotiable workflow

1. Create or inspect a task with `pipeline.py`.
2. Prepare a brief and move to plan review.
3. Stop for human approval before script development continues.
4. Prepare the script and five-shot storyboard.
5. Stop for human storyboard approval.
6. Prepare a voice preview and stop for human voice approval.
7. Lock the voice, then prepare image assets, render, QA, and a publish-ready package.
8. Never publish to a platform automatically unless the user explicitly requests a separate, authorized publishing workflow.

Every paid or remote task requires a budget check and explicit human approval before submission. Record remote task IDs and estimated cost with `set-remote-task` so an interrupted task can resume without losing context.

## Command workflow

Run commands from the skill directory:

```bash
python3 pipeline.py init 2026-08-09-first-video
python3 pipeline.py status 2026-08-09-first-video
python3 pipeline.py set-artifact script content/2026-08-09-first-video/script.md
python3 pipeline.py set-artifact storyboard content/2026-08-09-first-video/storyboard.md
python3 pipeline.py approve plan --video-id 2026-08-09-first-video
python3 pipeline.py approve storyboard --video-id 2026-08-09-first-video
python3 pipeline.py approve voice --video-id 2026-08-09-first-video
python3 pipeline.py set-remote-task assets provider-task-123 --cost 0
```

Use `status` before changing a task. Do not bypass a checkpoint by editing the JSON manually. If a stage is not ready, explain which artifact or approval is missing. Task IDs are deliberately restricted to safe filename characters so state cannot escape the `state/` directory.

Artifacts must live inside the skill directory by default. For a reviewed external file, use `--allow-external-path` explicitly and do not commit the resulting state file if it contains a local path:

```bash
python3 pipeline.py set-artifact voice_preview /path/to/preview.wav \
  --allow-external-path
```

The optional VoxCPM helpers invoke a locally installed executable or load a third-party model. Review the environment, package version, model source, and output path before running them.

## Output contract

For a new task, produce:

- concise creative brief and audience promise
- original Chinese voiceover script
- five-shot storyboard with image-generation prompts
- voice direction and preview notes
- asset checklist and file paths
- render specification, subtitle plan, and QA checklist
- title, cover direction, description, and publish copy

Keep the language concrete and human. Avoid generic mystical claims, fabricated quotations, medical or financial promises, and ungrounded attribution to Laozi, Zhuangzi, or other historical figures.

## State and recovery

The pipeline stores one JSON record per video under `state/`. Each stage tracks status, timestamps, attempts, remote task ID, cost points, artifacts, and errors. When resuming:

1. Run `python3 pipeline.py status <video-id>`.
2. Read the current stage and existing artifacts.
3. Continue from the first missing artifact or approval.
4. Preserve completed work and do not resubmit completed paid tasks.

When committing a task state to a shared repository, remove local absolute paths, private source-media locations, credentials, and transient audio before publishing.
