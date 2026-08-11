# Original Agent Skills

A small, inspectable repository for original Agent Skills and resumable creative workflows.

本仓库目前只发布一个原创 Skill：`skills/daoist-video-skill/`。项目处于早期公开阶段，不声称拥有下载量或广泛采用数据；重点是提供可阅读、可测试、可恢复的 Agent 工作流，并明确文件、网络、凭证和人工确认边界。

## What it does

Daoist Video Skill turns a Chinese short-video idea about Daoist inspiration, Eastern philosophy, relationships, or emotions into a staged production task:

- brief and script development
- storyboard and voice-preview checkpoints
- asset, render, QA, and publish-ready tracking
- resumable JSON state with attempts, artifacts, remote task IDs, and cost points
- human approval before paid or remote work

The repository intentionally does not publish to social platforms automatically. External TTS, image, video, and FFmpeg tools are optional integrations and remain subject to human review.

## Install for Codex

From a local clone, copy the skill directory into the Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/daoist-video-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then invoke it in Codex with `$daoist-video-skill`. The skill's `SKILL.md` is the agent-facing contract; the bundled Python CLI is an optional local workflow helper.

## Run the local workflow

```bash
cd skills/daoist-video-skill
python3 pipeline.py init demo-video
python3 pipeline.py status demo-video
python3 pipeline.py set-artifact brief \
  content/2026-08-09-first-video/brief.md \
  --video-id demo-video
python3 pipeline.py approve plan --video-id demo-video
python3 pipeline.py status demo-video
```

State files are written under `skills/daoist-video-skill/state/` and are ignored by Git. Do not commit state that contains local absolute paths, private media locations, credentials, or transient audio.

## Safety boundaries

- Task IDs are restricted to safe filename characters.
- Artifacts must stay inside the skill directory unless `--allow-external-path` is explicitly provided.
- Paid or remote tasks require a budget check and human approval.
- VoxCPM helpers invoke a local executable or load a third-party model; review the environment, package, model source, and output path first.
- Markdown instructions, model output, and third-party contributions are untrusted input.

## Development checks

```bash
python3 -m unittest discover -s skills/daoist-video-skill/tests -v
python3 -m py_compile skills/daoist-video-skill/pipeline.py
```

Before opening a change, read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Release history is recorded in [CHANGELOG.md](CHANGELOG.md).

## License and scope

The repository and the included Daoist Video Skill are released under the MIT License. This repository currently contains only the original Daoist skill; it does not claim ownership of unrelated material.
