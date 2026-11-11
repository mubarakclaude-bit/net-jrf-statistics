#!/usr/bin/env bash
# Repository seed integrity check. Read-only and independent of authoring assistants.
set -euo pipefail
cd "$(dirname "$0")"

python3 - <<'PY'
import json, pathlib, sys
root = pathlib.Path("seed")
files = sorted(root.glob("*.json"))
data = {}
for path in files:
    try:
        data[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"INVALID JSON {path}: {exc}")
print(f"JSON syntax: {len(files)} seed documents parsed")

manifest = data.get("meta_lessons", {}).get("topics", {})
lessons = {}
for stem, obj in data.items():
    if isinstance(obj, dict) and obj.get("topicId"):
        tid = obj["topicId"]
        if tid in lessons:
            raise SystemExit(f"DUPLICATE topicId {tid}: {lessons[tid]} and {stem}")
        lessons[tid] = (stem, obj)
missing = []
for tid, meta in manifest.items():
    item = lessons.get(tid)
    if not item:
        missing.append(tid)
        continue
    stem, lesson = item
    if lesson.get("status") != meta.get("status"):
        raise SystemExit(f"STATUS mismatch for {tid}: lesson={lesson.get('status')} manifest={meta.get('status')}")
    if not isinstance(lesson.get("scenes"), list) or not lesson["scenes"]:
        raise SystemExit(f"NO SCENES for {tid} ({stem})")
    for scene in lesson["scenes"]:
        if scene.get("kind") == "quiz" and scene.get("setId"):
            pool = data.get(scene["setId"])
            if not pool or not isinstance(pool.get("items"), list):
                raise SystemExit(f"MISSING mastery pool {scene['setId']} referenced by {tid}")
if missing:
    raise SystemExit("Manifest lessons missing seed files: " + ", ".join(missing))
print(f"Lesson manifest: {len(manifest)} topics resolve to unique lesson seeds and quiz pools")
PY

# The Probability module has an explicit, independently maintained aggregate index verifier.
if [ -f verify_probability_index.py ]; then
  python3 verify_probability_index.py
fi
echo "SEED CHECK PASS"
