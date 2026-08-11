# Changelog

## [0.1.0] - 2026-08-11

### Added

- Initial public release of the original Daoist Video Skill.
- Resumable Python state machine for briefs, scripts, storyboards, voice previews, assets, rendering, QA, and publish-ready work.
- Human approval checkpoints before script, storyboard, and voice progression.
- MIT licensing, contribution guidance, security policy, tests, and GitHub Actions checks.

### Safety

- Restricted task IDs and artifact paths to reduce path traversal and accidental external-file access.
- Added explicit trust-boundary guidance for Markdown, subprocesses, local models, remote tasks, credentials, and private media.
