#!/bin/bash
# Assemble the published page from src/ parts.
set -e
# Windows installs Python as `python`, and `python3` there is often a Microsoft Store alias
# that is not a working interpreter. Pick a real one rather than assuming the name.
PYBIN=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)" >/dev/null 2>&1; then
    PYBIN="$c"; break
  fi
done
[ -n "$PYBIN" ] || { echo "FAILED: no working Python 3 found (tried python3, python)"; exit 1; }
mkdir -p .cache
cd "$(dirname "$0")"
OUT=app.html
# The build stamp shown in the header was a hand-edited constant and so told the reader
# nothing about which build they were actually running. Stamp it for real on every build.
node tools/build-features.js        # scan src/features/ and write .cache/features.generated.js
STAMP="$(date -u '+%Y-%m-%d %H:%M UTC')"
sed -i "s|^const BUILD=\".*\";|const BUILD=\"$STAMP\";|" src/10-const.js
{
  # head.html ends with </style>; splice the workspace css in before it
  head -c $(($(wc -c < src/00-head.html) - 9)) src/00-head.html
  cat src/02-ws.css
  echo '</style>'
  cat src/01-body.html
  echo '<script>'
  for f in src/10-const.js src/11-state.js src/12-utils.js src/05-auth.js src/13-db.js src/14-features.js \
           src/20-metrics.js src/21-attempts.js src/22-llm.js src/23-ask.js src/30-viz.js src/31-flow.js src/32-math.js \
           src/40-render.js src/45-learn.js src/52-bank.js src/53-drill.js \
           src/54-mock.js src/60-admin.js src/62-gen.js src/65-export.js \
           src/70-wire.js .cache/features.generated.js src/80-boot.js; do
    cat "$f"; echo
  done
  echo '</script>'
} > $OUT
"$PYBIN" -c "
import re,sys
h=open('$OUT',encoding='utf-8').read()
open('.cache/app.js','w',encoding='utf-8').write(re.search(r'<script>(.*)</script>',h,re.S).group(1))
"
node --check .cache/app.js && echo "syntax ok"
echo "built $OUT: $(wc -c < $OUT) bytes, $(wc -l < $OUT) lines"
