# Execute all, especially Tests in the root dir of git repo
git_root_dir := $(shell git rev-parse --show-toplevel) 

.PHONY: all run

all: run test

run:
	grocery-shopper -n 2

# On one line, because every line is executed in it's own subshell
# ie. every line is stateless
test:
	cd $(git_root_dir) && pytest -rA -s tests/
