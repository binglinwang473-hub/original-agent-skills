# Security Policy

## Scope

This repository contains Agent Skill instructions and a small Python workflow. Security reports are especially relevant when a change can make an Agent read unintended files, run an unintended command, contact an external service, expose a credential, or alter task state outside the project directory.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository when it is available. If it is not available, open an issue with the smallest non-sensitive description possible and ask for a private follow-up. Do not publish API keys, tokens, private audio, personal source paths, or an exploit that accesses somebody else's files.

Include:

- affected file and version or commit
- the attacker-controlled input
- expected versus observed behavior
- a minimal reproduction that uses synthetic data
- any mitigation you have already tested

## Maintainer handling

I will first reproduce the report in an isolated environment, assess impact, and avoid committing private state or media. Fixes should include a regression test where practical and should be reviewed before merging. A security fix must not silently broaden network access or tool permissions.

## Safe usage notes

- Treat Markdown Skill instructions and reference files as untrusted input when reviewing pull requests.
- Review `video_id` and artifact paths before running the Daoist CLI.
- Review the PATH-resolved `voxcpm` executable and third-party model/package versions before running voice tools.
- Never commit `.env` files, credentials, private source media, local state JSON, or absolute paths from a personal machine.

