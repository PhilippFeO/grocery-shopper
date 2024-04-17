# Execute all, especially Tests in the root dir of git repo
git_root_dir := $(shell git rev-parse --show-toplevel) 

.PHONY: all run test vtest einstall install build tup tpypi mdl 

all: einstall run

# Do a local/editable install
einstall:
	pip install -e $(git_root_dir) 

# Installation from test.pypi.org ([t]est [install])
tinstall:
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

# make run NUMBER
run: install
	grocery_shopper -n $(filter-out $@, $(MAKECMDGOALS))

# ─── Test ──────────

# On one line, because every line is executed in it's own subshell
# ie. every line is stateless
# -q: less verbose test output
test:
	@cd $(git_root_dir) && python -m pytest -rA -s -q tests/

# Verbose tests, ie. with normal output
vtest:
	@cd $(git_root_dir) && python -m pytest -rA -s tests/

# ─── pdf ──────────
pdf:
	grocery_shopper --make-pdf ./recipes/Testgericht.yaml
	okular ./recipes/pdf/Testgericht.pdf
