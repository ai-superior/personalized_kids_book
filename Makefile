export PYTHONPATH=$(PWD):$(PWD)/src:$(PWD)/tests

all: lint-black lint-flake lint-mypy
test:
	pytest tests --cov src

lint: lint-mypy lint-black lint-flake

lint-black:
	black --check .

lint-flake:
	flake8 src
	flake8 tests

lint-mypy:
	mypy src
	mypy tests
