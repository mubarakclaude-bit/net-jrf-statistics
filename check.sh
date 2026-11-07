#!/usr/bin/env bash
# Validate the seed set as a whole. Read-only; safe to run any time, and it is what CI runs.
#
# This script used to report DRIFT between the committed lesson index, the hand-edited list in
# test.js and the seeds on disk. That drift existed because every new lesson edited those two shared
# files. They are generated now (tools/seed-docs.js), so there is nothing left to drift: a lesson
# exists because its seed exists. What remains worth checking is the set itself:
#   - every lesson seed is valid JSON with the required fields
#   - no two lessons share a topicId or a store document id
#   - warnings: a quiz scene pointing at a missing question set, a topic missing from the catalog
set -e
cd "$(dirname "$0")"
node tools/gen-index.js --check
