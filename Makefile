.PHONY: install
install:
	pip install --prefer-binary --upgrade pip setuptools wheel
	pip install --prefer-binary -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install --prefer-binary -r requirements-dev.txt
	python setup.py develop

.PHONY: build
build:
	python setup.py build

.PHONY: lint
lint:
	ruff chaosgcp/ tests/
	isort --check-only --profile black chaosgcp/ tests/
	black --check --diff --line-length=80 chaosgcp/ tests/

.PHONY: format
format:
	isort --profile black chaosgcp/ tests/
	black --line-length=80 chaosgcp/ tests/
	ruff chaosgcp/ tests/ --fix

.PHONY: tests
tests:
	pytest
