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
set -e
cd "$(dirname "$0")"
node tools/gen-index.js --check
node tools/validate-contracts.js
