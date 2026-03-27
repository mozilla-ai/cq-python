PROTO_VERSION := v0.1.0
PROTO_BASE_URL := https://raw.githubusercontent.com/mozilla-ai/cq-proto/$(PROTO_VERSION)

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
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

.PHONY: install
install:
	uv sync --group dev

.PHONY: test
test:
	uv run pytest -x -q

.PHONY: lint
lint:
	uv run pre-commit run --all-files
