.PHONY: install
install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install -r requirements-dev.txt
	python setup.py develop

.PHONY: build
build:
	python setup.py build

.PHONY: lint
lint:
	flake8 chaosgcp/ tests/
	isort --check-only --profile black chaosgcp/ tests/
	black --check --diff --line-length=80 chaosgcp/ tests/

.PHONY: format
format:
	isort --profile black chaosgcp/ tests/
	black --line-length=80 chaosgcp/ tests/

.PHONY: tests
tests:
	pytest
