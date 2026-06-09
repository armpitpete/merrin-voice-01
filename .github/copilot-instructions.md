# Copilot instructions

## Core working rule

Work in small, contained batches.

Do not make unrelated changes.

Preserve existing layout, tone, behaviour, file structure, and working features unless the issue explicitly says otherwise.

If a request is ambiguous, choose the smallest safe interpretation.

## Scope control

Only edit files that are clearly needed for the requested task.

Do not rename files, move routes, change architecture, add dependencies, or refactor working code unless the issue explicitly asks for that.

Do not polish beyond the stated goal.

Stop when the requested outcome is met.

## Required report after changes

After completing a task, report:

- files changed
- what changed in each file
- why each change was needed
- build/test/checks run
- any risks
- any suggested follow-up issues

## Build and test rule

Before finishing, run the project’s normal build, test, lint, or check command if one exists.

If no check command is obvious, say so.

Do not claim a check passed unless it was actually run.

## Safety rule

Never commit secrets, API keys, tokens, private files, personal data, audio masters, unpublished assets, or generated build folders unless the repo already tracks them intentionally.

## Communication style

Be direct and specific.

When something is uncertain, state the uncertainty.

Do not invent project rules. Use the files in the repository and the issue instructions as the source of truth.
