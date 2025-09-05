.PHONY: fmt lint test unit integration
fmt:
	black src tests && isort src tests
lint:
	ruff check src tests
unit:
	pytest -q tests/unit
integration:
	pytest -q tests/integration
test: unit
