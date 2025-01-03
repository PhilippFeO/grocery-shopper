# Execute all, especially Tests in the root dir of git repo
git_root_dir := $(shell git rev-parse --show-toplevel) 

.PHONY: all run runarg test vtest einstall build tup tpypi venv

all: run

# Do a local/editable install
# Only necessary once
einstall:
	pip install -e $(git_root_dir) 

# Installation from test.pypi.org ([t]est [install])
tinstall: build tup
	python3 -m pip uninstall grocery_shopper
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps grocery_shopper

# Build package
build:
	python -m build

# Upload package to test.pypi.org ([t]est [up])
tup:
	python3 -m twine upload --repository testpypi dist/*

# Build and upload to test.pypi.org ([t]est [pypi])
tpypi: build tup


# ─── Run ──────────
# venv:
# 	cd .venv && source bin/activate

run:
	grocery_shopper -n 2

# make run NUMBER
runarg:
	grocery_shopper -n $(filter-out $@, $(MAKECMDGOALS))


# ─── Test ──────────
# On one line, because every line is executed in it's own subshell
# ie. every line is stateless
# -q: less verbose test output
test:
	@cd $(git_root_dir) && python3 -m pytest -rA -s -q tests/

# Verbose tests, ie. with normal output
vtest:
	@cd $(git_root_dir) && python3 -m pytest -rA -s tests/
