.PHONY: all run

all: run test

run:
	pip install -e ..
	grocery-shopper -n 2

test:
	pytest -rA -s ../tests/
