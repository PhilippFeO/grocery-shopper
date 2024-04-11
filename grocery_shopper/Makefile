# Execute all, especially Tests in the root dir of git repo
git_root_dir := $(shell git rev-parse --show-toplevel) 

.PHONY: all run test vtest install mdl


install:
	pip install -e $(git_root_dir) 

# mdl = Mandeln
mdl: install
	grocery_shopper --take ~/Documents/Kochen/recipes/Ricotta-Pasta_mit_Mandeln.yaml

# On one line, because every line is executed in it's own subshell
# ie. every line is stateless
# -q: less verbose test output
test:
	@cd $(git_root_dir) && python -m pytest -rA -s -q tests/

# Verbose tests, ie. with normal output
vtest:
	@cd $(git_root_dir) && python -m pytest -rA -s tests/
