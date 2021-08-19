#!/bin/bash

POETRY=`pip list | grep poetry`
if [[ -z POETRY ]]; then
    pip install poetry
fi
poetry install
poetry run uvicorn backend.main:app --reload