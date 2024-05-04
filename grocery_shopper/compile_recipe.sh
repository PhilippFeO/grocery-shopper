#!/bin/bash
# Compile CLI provided tex file of a recipes.

if [ $# -ne 2 ]; then
    echo "Usage: $0 .tex-file outdir"
    exit 1
fi

tex_file="$1"
outdir="$2"

mkdir -p "$outdir"
latexmk -verbose -file-line-error -interaction=nonstopmode -outdir="$outdir" "$tex_file"
