BIN = .venv/bin/
CODE = flake8_return

init:
	python3 -m venv .venv
	poetry install

test:
	$(BIN)pytest -vv --cov=$(CODE) $(args)

lint:
	$(BIN)flake8 --jobs 4 --statistics --show-source $(CODE) tests
	$(BIN)pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(BIN)mypy $(CODE) tests
	$(BIN)black --py36 --skip-string-normalization --line-length=79 --check $(CODE) tests

pretty:
	$(BIN)isort --apply --recursive $(CODE) tests
	$(BIN)black --py36 --skip-string-normalization --line-length=79 $(CODE) tests
	$(BIN)unify --in-place --recursive $(CODE) tests

precommit_install:
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

publish:
ifeq ($(version),)
	$(error `version` argument missing! (example: make publish version='0.1.0'))
else
	poetry version $(version)
	poetry build
	poetry publish
	git add pyproject.toml
	git commit -m "release $(version)"
	git tag -a $(version)
	git push origin master --tags
endif

ci: BIN =
ci: lint test
