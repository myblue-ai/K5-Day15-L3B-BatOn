#!/bin/sh
set -eu

cd "$(dirname "$0")/.."
context=$(mktemp)
trap 'rm -f "$context"' EXIT

# Docker must only receive app files. TLS storage may be unreadable to the build user.
tar -cf "$context" Dockerfile .dockerignore requirements.txt \
    codebase/*.py codebase/index.html codebase/admin.html data/a1_demo_lesson.json
docker build -t "${1:-mini-hackathon-agent:demo}" - < "$context"
