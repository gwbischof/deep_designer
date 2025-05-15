# CLAUDE.md

## General
- Write concise code, comments, and docstrings
- Design from broad structures to specific details

## Git
- Commit/push only when requested
- Use `git add .` to add all files when committing
- Single-sentence commit messages
- Do not add co-author to commits

## Commands
- Lint: `pixi run ruff check .`
- Type check: `pixi run mypy .`
- Tests: `pixi run pytest`
- Format: `pixi run black .`
- Run: `pixi run deep_designer`
- Validate DESIGN.json: `pixi run validate`
- Dependencies: `pixi add <pkg>`, `pixi install`

## Style
- **Format**: Black
- **Imports**: isort (stdlib → third-party → first-party)
- **Naming**: snake_case (variables/functions), PascalCase (classes), UPPER_SNAKE_CASE (constants)
- **Errors**: Specific exceptions with context (`raise ... from`)
- **Docs**: Concise Google-style docstrings
- **Structure**: One class/function group per file, relative imports
