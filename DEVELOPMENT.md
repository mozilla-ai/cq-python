# Development

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Initial Setup

```bash
git clone https://github.com/mozilla-ai/cq-python.git
cd cq-python
make setup
```

## Common Tasks

```bash
make test           # Run all tests.
make lint           # Run pre-commit hooks (format, lint, detect-secrets).
make format         # Auto-format Python files.
make format-check   # Check formatting without modifying files.
make clean          # Remove fetched files and build artifacts.
make help           # Show all available targets.
```

## Clean Rebuild

```bash
make clean && make test
```

`make clean` removes fetched protos, the skill prompt, and build artifacts.
Committed files (generated proto stubs) are not affected.

## Regenerating Protos

After updating `PROTO_VERSION` in the Makefile:

```bash
make fetch-protos
make generate
```

Proto-generated `_pb2.py` files are committed to the repo. They only need
regeneration when the proto definitions change.

## Updating the Skill Prompt

After updating `SKILL_VERSION` in the Makefile:

```bash
make clean
make fetch-skill
```

The skill prompt (`src/cq/protocol/skill.md`) is committed to the repo
and ships baked into the PyPI package.
