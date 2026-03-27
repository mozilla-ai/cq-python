.DEFAULT_GOAL := help

PROTO_VERSION := v0.1.0
PROTO_BASE_URL := https://raw.githubusercontent.com/mozilla-ai/cq-proto/$(PROTO_VERSION)

SKILL_VERSION := 0.4.0
SKILL_URL := https://raw.githubusercontent.com/mozilla-ai/cq/$(SKILL_VERSION)/plugins/cq/skills/cq/SKILL.md

.PHONY: help
help:
	@echo "cq-sdk — Python SDK for the shared agent knowledge commons"
	@echo ""
	@echo "Development:"
	@echo "  make setup          Install all dependencies"
	@echo "  make test           Run all tests"
	@echo "  make lint           Run pre-commit hooks (format, lint, detect-secrets)"
	@echo "  make format         Auto-format Python files"
	@echo "  make format-check   Check formatting without modifying files"
	@echo "  make clean          Remove fetched artifacts and build output"
	@echo ""
	@echo "Fetch:"
	@echo "  make fetch-protos   Download proto definitions from cq-proto"
	@echo "  make fetch-skill    Download cq skill prompt from mozilla-ai/cq"
	@echo "  make generate       Generate _pb2 stubs from fetched protos"

.PHONY: setup
setup:
	uv sync --group dev

.PHONY: test
test:
	uv run pytest -x -q

.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: format
format:
	uv run ruff format .

.PHONY: format-check
format-check:
	uv run ruff format --check .

.PHONY: fetch-skill
fetch-skill:
	@if [ ! -f src/cq/protocol/skill.md ]; then \
		mkdir -p src/cq/protocol; \
		curl -sSfL $(SKILL_URL) -o src/cq/protocol/skill.md; \
	fi

.PHONY: fetch-protos
fetch-protos:
	mkdir -p tmp/cq/v1
	curl -sSfL $(PROTO_BASE_URL)/cq/v1/knowledge_unit.proto -o tmp/cq/v1/knowledge_unit.proto
	curl -sSfL $(PROTO_BASE_URL)/cq/v1/scoring.proto -o tmp/cq/v1/scoring.proto
	curl -sSfL $(PROTO_BASE_URL)/cq/v1/api.proto -o tmp/cq/v1/api.proto
	curl -sSfL $(PROTO_BASE_URL)/cq/v1/review.proto -o tmp/cq/v1/review.proto

.PHONY: generate
generate:
	mkdir -p src/cq/cqpb
	uv run python -m grpc_tools.protoc --proto_path=tmp \
		--python_out=src/cq/cqpb \
		--pyi_out=src/cq/cqpb \
		tmp/cq/v1/*.proto

.PHONY: clean
clean:
	rm -rf tmp/
	rm -f src/cq/protocol/skill.md
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
