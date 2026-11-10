#!/usr/bin/env bash
# Validate the seed set and the contracts. Read-only; safe to run any time, and it is what CI runs first.
#
#   npm ci && ./check.sh          (or: npm run check)
#
# 1. tools/gen-index.js --check      every lesson seed is valid JSON with the required fields, no duplicate topicId or
#                                    store document id; warns about a quiz pointing at a missing pool. The lesson index
#                                    and the test harness are GENERATED from seed/, so there is nothing to drift.
# 2. tools/validate-contracts.js     the contracts in contracts/ agree with the app source they mirror, accept every valid
#                                    fixture and reject every invalid one, every literal storage path in src/ is allowed,
#                                    and every lesson and question-set seed conforms (known legacy deviations are listed in
#                                    contracts/legacy-exceptions.json and reported on every run).
# 3. tests/content.test.js           the content tool (tools/content.js) against a made-up content set with known answers
#    tools/content.js check          the real seed files agree with each other (catalog, lessons, June 2026 paper, variant banks)
set -e
cd "$(dirname "$0")"
node tools/gen-index.js --check
node tools/validate-contracts.js
out=$(node tests/content.test.js) || { echo "$out"; exit 1; }   # not a pipe: a pipe would hide a failure
echo "$out" | tail -1
node tools/content.js check
out=$(node tests/changed-topics.test.js) || { echo "$out"; exit 1; }   # which lessons a pull request must click-test
echo "$out" | tail -1
out=$(node tests/check-ids.test.js) || { echo "$out"; exit 1; }   # the id-stability tool, in a throwaway git repo
echo "$out" | tail -1
