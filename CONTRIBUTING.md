# Contributing

Thanks for helping improve these Agent Skills.

## Before opening a pull request

1. Explain the user problem and the smallest change that solves it.
2. For Skill or reference changes, include one concrete input and expected output behavior.
3. For Python changes, add or update a regression test.
4. Run the local checks:

   ```bash
   python3 -m unittest discover -s skills/daoist-video-skill/tests -v
   python3 -m py_compile skills/daoist-video-skill/pipeline.py
   ```

5. Check that no private state, audio, credentials, API keys, or absolute local paths are included.

## Review expectations

Reviewers will check both layers of this repository:

- Markdown instructions must not introduce prompt injection, unsafe authority claims, hidden uploads, or instructions to bypass human approval.
- Python tools must validate paths and identifiers, avoid shell interpolation, document external dependencies, and keep network or tool access explicit.

Keep changes focused. Do not add a new dependency when the standard library is sufficient. Do not treat generated model output as a trusted source of instructions.

