#!/bin/bash
# Compile CLI provided tex file of a recipes.

if [ $# -ne 2 ]; then
    echo "Usage: $0 .tex-file resource-dir"
    exit 1
fi

latexmk -verbose -file-line-error -interaction=nonstopmode -outdir="$2"/out "$1"
