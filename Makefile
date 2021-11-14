.PHONY: \
	all install run

all: .make-install

install: .make-install

.make-install-pipenv:
	@if ! which pipenv &> /dev/null; then \
		pip install pipenv; \
	fi
	@touch $@

.make-install: Pipfile .make-install-pipenv
	pipenv install -d
	@touch $@

run: .make-install
	uvicorn src.skill_buy_elephant.application:app --reload

flake:
	flake8 src/skill_buy_elephant
	flake8 src/tests

mypy:
	mypy src/skill_buy_elephant

isort:
	isort setup.py
	isort src/skill_buy_elephant
	isort src/tests

test:
	pytest -q src/tests
