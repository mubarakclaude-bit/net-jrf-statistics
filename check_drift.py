#!/usr/bin/env python3
"""Warn when a lesson's authoring script is behind its seed.

Six of the nine Module 4 scripts declare version 1.0 while their seeds are at 1.3: the
seeds were enriched after generation and the scripts never caught up. Running one of those
scripts would overwrite the seed with older content and lose the enrichment silently — the
JSON would still be valid and every validator would still pass. Run this before running any
lesson_*.py.
"""
import glob, io, json, os, re, sys

bad = 0
for script in sorted(glob.glob("lesson_*.py")):
    src = io.open(script, encoding="utf-8").read()
    m = re.search(r'"version":\s*"([0-9.]+)"|version="([0-9.]+)"', src)
    sv = (m.group(1) or m.group(2)) if m else None
    seed = "seed/%s.json" % os.path.splitext(script)[0]
    if not os.path.exists(seed):
        print("%-18s script v%-5s  no seed yet" % (script, sv)); continue
    jv = json.load(io.open(seed, encoding="utf-8")).get("version")
    try:
        stale = sv is not None and jv is not None and float(sv) < float(jv)
    except ValueError:
        stale = sv != jv
    if stale:
        bad += 1
        print("%-18s script v%-5s  seed v%-5s  STALE — running it would revert the lesson"
              % (script, sv, jv))
    else:
        print("%-18s script v%-5s  seed v%-5s  ok" % (script, sv, jv))
if bad:
    print("\n%d script(s) behind their seed. Do not run those until they are regenerated "
          "from the seed, or the enrichment they are missing will be lost." % bad)
    sys.exit(1)
