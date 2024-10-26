#!/usr/bin/env sh

echo "Running Black"
poetry run black . || exit 1

echo "\nRunning flake8"
poetry run flake8 . && echo "Done." || exit 2
