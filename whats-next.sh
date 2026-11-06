#!/usr/bin/env bash
# Before authoring anything, run this. It answers, from the repo alone: what is built, what is
# in progress on other branches, and what is next, so two authors do not write the same lesson.
#
#   ./whats-next.sh              read-only; uses the remote-tracking branches you already have
#   ./whats-next.sh --fetch      git fetch first, so in-progress branches are up to date
#   ./whats-next.sh --live       also compare with the deployed snapshot (needs network)
#
# It trusts, in this order: seed/meta_lessons.json (what is built), other branches (what is in
# progress), BACKLOG.md (what is queued). Branches that are not merged are checked too, because
# `main` alone can be behind: finished lessons sit on feature branches until their PR merges.
set -e
set -o pipefail
PYBIN=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)" >/dev/null 2>&1; then
    PYBIN="$c"; break
  fi
done
[ -n "$PYBIN" ] || { echo "FAILED: no working Python 3 found (tried python3, python)"; exit 1; }
cd "$(dirname "$0")"
FETCH=0; LIVE=0
for a in "$@"; do [ "$a" = "--fetch" ] && FETCH=1; [ "$a" = "--live" ] && LIVE=1; done
if [ "$FETCH" = 1 ]; then git fetch -q --all --prune 2>/dev/null || echo "(fetch failed; using what is already local)"; fi
mkdir -p .cache

# What each other branch adds: topic ids from the lesson seeds it contains and main does not.
BASE=origin/main; git rev-parse -q --verify "$BASE" >/dev/null || BASE=main
HERE=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")
: > .cache/_branches.txt
for b in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin 2>/dev/null | grep -v -E '/(HEAD|main)$' || true); do
  # A lesson branch is an in-progress reservation even before its JSON seed exists.
  case "$b" in
    origin/lesson/*)
      tid="${b#origin/lesson/}"
      [ -n "$tid" ] && printf '%s\t%s\n' "$tid" "$b" >> .cache/_branches.txt
      ;;
  esac
  files=$(git diff --name-only --diff-filter=A "$BASE"..."$b" -- 'seed/lesson_*.json' 2>/dev/null || true)
  for f in $files; do
    tid=$(git show "$b:$f" 2>/dev/null | "$PYBIN" -c "import sys,json;print(json.load(sys.stdin).get('topicId',''))" 2>/dev/null || true)
    [ -n "$tid" ] && printf '%s\t%s\n' "$tid" "$b" >> .cache/_branches.txt
  done
done
case "$HERE" in
  lesson/*)
    tid="${HERE#lesson/}"
    [ -n "$tid" ] && printf '%s\t%s\n' "$tid" "$HERE" >> .cache/_branches.txt
    ;;
esac

PYTHONIOENCODING=utf-8 LIVE="$LIVE" HERE="$HERE" BASE="$BASE" "$PYBIN" -I - <<'PYEOF'
import io, json, os, re, sys, urllib.request

def load(path):
    return json.load(io.open(path, encoding='utf-8'))

built = load('seed/meta_lessons.json').get('topics', {})
order = []                      # backlog order, with done flag
for line in io.open('BACKLOG.md', encoding='utf-8'):
    m = re.match(r'^- \[( |x)\] \**([a-z0-9]+-[a-z0-9]+)\**', line)
    if m: order.append((m.group(2), m.group(1) == 'x', line.strip()))

elsewhere = {}                  # topic id -> branches that add it
for l in io.open('.cache/_branches.txt', encoding='utf-8'):
    tid, _, br = l.rstrip('\n').partition('\t')
    elsewhere.setdefault(tid, []).append(br)

print("on branch %s, compared with %s" % (os.environ['HERE'], os.environ['BASE']))
print()
mods = {}
for tid in built: mods.setdefault(tid.rsplit('-', 1)[0], []).append(tid)
print("BUILT (%d lessons in seed/meta_lessons.json on this branch)" % len(built))
for m in sorted(mods): print("  %-14s %2d  %s" % (m, len(mods[m]), ' '.join(sorted(t.rsplit('-', 1)[1] for t in mods[m]))))

print()
stale = [t for t, done, _ in order if t in built and not done]
if stale:
    print("BACKLOG SAYS UNBUILT BUT THE INDEX HAS IT (tick these off): " + ', '.join(stale))
    print()
other = {t: b for t, b in elsewhere.items() if t not in built}
if other:
    print("IN PROGRESS ON OTHER BRANCHES, not in this branch's index (do NOT start these):")
    for t in sorted(other): print("  %-16s on %s" % (t, ', '.join(sorted(set(other[t])))))
    print()
elif os.path.exists('.cache/_branches.txt'):
    print("No other remote branch adds a lesson that this branch lacks.")
    print()

queue = [(t, line) for t, done, line in order if not done and t not in built and t not in other]
print("NEXT FROM BACKLOG.md (top unchecked, not built, not in progress elsewhere)")
for t, line in queue[:5]:
    print("  " + re.sub(r'\*', '', line)[6:130])
if not queue: print("  nothing left in the queue")
print()
print("Before you start: pick the top item, open a branch named lesson/<topic-id>, and say so in a")
print("draft pull request, so the next person's run of this script sees it.")

if os.environ.get('LIVE') == '1':
    print()
    try:
        d = json.load(urllib.request.urlopen('https://net-jrf-statistics.vercel.app/data.json', timeout=20))
        deployed = set(d.get('meta/lessons', {}).get('topics', {}))
        print("DEPLOYED SNAPSHOT: %d lessons" % len(deployed))
        miss = sorted(set(built) - deployed); extra = sorted(deployed - set(built))
        if miss: print("  built here but not deployed yet: " + ', '.join(miss))
        if extra: print("  deployed but not in this branch: " + ', '.join(extra))
        if not miss and not extra: print("  identical to this branch's index")
    except Exception as e:
        print("DEPLOYED SNAPSHOT: could not be fetched (%s)" % e.__class__.__name__)
PYEOF
