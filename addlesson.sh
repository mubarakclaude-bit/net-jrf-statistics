#!/usr/bin/env bash
# One call for the mechanical half of adding a lesson, replacing four separate steps.
#   ./addlesson.sh <authoring.py> <seed-stem>                      (topic id, lesson id and pool are read from the seed it writes)
#   ./addlesson.sh <authoring.py> <seed-stem> <topicId> <lessonId> <masterySetStem>   (older form: asserts all three)
# Generates, validates, checks every formula through the renderer and asserts the lesson is wired.
# It edits NO shared file: the lesson index and the test harness are generated from seed/ by
# tools/seed-docs.js. Prints only what changed or what failed.
set -e
# pipefail matters: `"$PYBIN" "$PY" | tail -2` otherwise reports tail's exit code, so a syntax
# error in the authoring script was swallowed and the run continued on a STALE seed file.
set -o pipefail
# Windows installs Python as `python`, and `python3` there is often a Microsoft Store alias
# that is not a working interpreter. Pick a real one rather than assuming the name.
PYBIN=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)" >/dev/null 2>&1; then
    PYBIN="$c"; break
  fi
done
[ -n "$PYBIN" ] || { echo "FAILED: no working Python 3 found (tried python3, python)"; exit 1; }
[ $# -ge 2 ] || { echo "usage: ./addlesson.sh <authoring.py> <seed-stem> [<topicId> <lessonId> <masterySetStem>]"; exit 1; }
PY=$1; STEM=$2; TID=${3:-}; DOC=${4:-}; SET=${5:-}
# Once a lesson is merged, its seed JSON is the source of truth (docs/CONTENT_GUIDE.md, 3a). Running its generator script
# again would overwrite every later edit made to the JSON, so that needs an explicit REGENERATE=1. A lesson that is new in
# this branch is not on the base branch yet, so it is never blocked: the usual "run until clean" loop is unchanged.
BASEREF=${BASE_REF:-origin/multi-author-hosting}
if [ "${REGENERATE:-}" != "1" ] && git rev-parse --verify -q "$BASEREF" >/dev/null 2>&1 && git cat-file -e "$BASEREF:seed/$STEM.json" 2>/dev/null; then
  echo "FAILED: seed/$STEM.json is already merged ($BASEREF). Running $PY again would overwrite any edits made to the JSON since."
  echo "  To change an existing lesson, edit seed/$STEM.json directly (docs/CONTENT_GUIDE.md, 3a), then run:"
  echo "    python -I tools/audit-lesson.py seed/$STEM.json && node vcheck.js seed/$STEM.json && npm run check"
  echo "  If you updated the script on purpose and want it to regenerate the file: REGENERATE=1 ./addlesson.sh $*"
  exit 1
fi
mkdir -p .cache
START=$(date +%s)
"$PYBIN" "$PY" | tail -2
# The authoring script hardcodes its own output path, so a <seed-stem> that does not match it
# sends the validator to the wrong file. If a file happens to sit at that path from an earlier
# run, everything downstream validates a STALE seed and passes. Refuse both cases loudly.
mtime() { stat -c %Y "$1" 2>/dev/null || stat -f %m "$1"; }
if [ ! -f "seed/$STEM.json" ]; then
  echo "FAILED: $PY did not write seed/$STEM.json"
  echo "  The <seed-stem> argument must match the OUT constant in the script."
  echo "  $PY has: $(grep -m1 '^OUT' "$PY" || echo '(no OUT line found)')"
  exit 1
fi
if [ "$(mtime "seed/$STEM.json")" -lt "$START" ]; then
  echo "FAILED: seed/$STEM.json is STALE — this run did not write it."
  echo "  The <seed-stem> argument does not match the OUT constant in $PY."
  echo "  $PY has: $(grep -m1 '^OUT' "$PY" || echo '(no OUT line found)')"
  exit 1
fi
node vcheck.js "seed/$STEM.json" 2>&1 | grep -vE '^seed/' | head -12
# The formula-render and self-cited-answer audits live in tools/audit-lesson.py, shared with CI, so a lesson gets exactly the same
# checks from GitHub Actions as from a local run.
"$PYBIN" -I tools/audit-lesson.py "seed/$STEM.json"
# The lesson index and the test harness are GENERATED from seed/ by tools/seed-docs.js, so this script
# no longer edits test.js or seed/meta_lessons.json (the two files every parallel author used to collide
# in). It only asserts that the lesson is wired the way you said: topic id, store doc id, quiz set, 20 items.
# With only two arguments the wiring is read from the seed itself, so there is nothing to get wrong; the checks that matter
# (unique ids, quiz pool exists with 20 items, topic in the catalog) still run. Pass all five to assert a specific wiring.
if [ -z "$TID" ]; then
  eval "$(node -e 'const d=require("./seed/"+process.argv[1]+".json");const q=(d.scenes||[]).find(s=>s.kind==="quiz")||{};console.log("TID="+JSON.stringify(d.topicId||"")+"; DOC="+JSON.stringify(d.id||"")+"; SET="+JSON.stringify(q.setId||""))' "$STEM")"
fi
node tools/gen-index.js --expect "$TID" "$DOC" "$SET"
