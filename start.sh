#!/bin/bash

set -a
source .env
set +a

source .venv/bin/activate

uvicorn main:app --reload

