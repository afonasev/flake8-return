.DEFAULT_GOAL := help

BIN = .venv/bin/
CODE = flake8_return

.PHONY: init ## init python venv and install deps
init:
	python3 -m venv .venv
	poetry install

.PHONY: precommit ## install git precommit hook
precommit:
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

.PHONY: test ## run test
test:
	$(BIN)pytest --verbosity=2 --showlocals --strict --cov=$(CODE) -k "$(k)"

.PHONY: lint ## run linters
lint:
	$(BIN)flake8 --jobs 4 --statistics --show-source $(CODE) tests
	$(BIN)pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(BIN)mypy $(CODE) tests
	$(BIN)black --target-version py36 --skip-string-normalization --line-length=79 --check $(CODE) tests
	$(BIN)pytest --dead-fixtures --dup-fixtures

.PHONY: pretty ## run autoformat tools
pretty:
	$(BIN)isort --apply --recursive $(CODE) tests
	$(BIN)black --target-version py36 --skip-string-normalization --line-length=79 $(CODE) tests
	$(BIN)unify --in-place --recursive $(CODE) tests

.PHONY: bump_major ## bump major version
bump_major:
	$(BIN)bumpversion major

.PHONY: bump_minor ## bump minor version
bump_minor:
	$(BIN)bumpversion minor

.PHONY: bump_patch ## bump patch version
bump_patch:
	$(BIN)bumpversion patch

.PHONY: help ## Show help
help:
	@grep -E \
		'^.PHONY: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk