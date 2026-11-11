#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lesson audit shared by addlesson.sh and CI, so an assistant that cannot run a shell gets exactly the same checks from
GitHub Actions that a local run gets.

    python tools/audit-lesson.py seed/lesson_<stem>.json

1. Every formula in the lesson goes through the layout engine (mathrender.js). A refusal means the lesson would show raw
   source to the learner, so it FAILS.
2. No pool item may cite its OWN answer as a wrong option. The key-spread relabelling rewrites "option X" references, and a
   plural list ("options B and C") once slipped through and left a check line ruling out the correct answer. It FAILS.

The question pool is the seed named by the lesson's quiz scene (seed/<setId>.json, in the same folder as the lesson).
Run from the repository root. Exit 0 means both audits passed."""
import io, json, os, re, subprocess, sys

def main(lesson_path):
    L = json.load(io.open(lesson_path, encoding='utf-8'))
    out = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'math' and isinstance(v, str): out.extend(x for x in v.split('\n') if x.strip())
                elif k == 'body' and isinstance(v, str) and o.get('t') in ('formula', 'step', 'def'):
                    out.extend(x for x in v.split('\n') if x.strip())
                else: walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(L)
    os.makedirs('.cache', exist_ok=True)
    io.open('.cache/_m.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    run = subprocess.run(['node', 'mathrender.js', '.cache/_m.json', '.cache/_mo.json'], capture_output=True)
    if run.returncode != 0 or not os.path.exists('.cache/_mo.json'):
        print('FAILED: mathrender.js did not run: ' + (run.stderr or b'').decode('utf-8', 'replace')[:200]); return 1
    r = json.load(io.open('.cache/_mo.json', encoding='utf-8'))
    bad = [k for k, v in r.items() if not v['ok']]
    print('formulas %d, stacked %d, refusals %d' % (len(r), sum(1 for v in r.values() if 'pfrac' in v['print']), len(bad)))
    for k in bad[:4]: print('  REFUSED:', k[:88])
    failed = bool(bad)
    if failed: print('FAILED: %d formula(s) would render as source; rewrite them in the supported notation' % len(bad))

    sets = [s.get('setId') for s in L.get('scenes', []) if s.get('kind') == 'quiz']
    if not sets or not sets[0]:
        print('FAILED: the lesson has no quiz scene with a setId'); return 1
    pool_path = os.path.join(os.path.dirname(lesson_path), sets[0] + '.json')
    if not os.path.exists(pool_path):
        print('FAILED: the quiz scene points at %s, which does not exist' % pool_path); return 1
    P = json.load(io.open(pool_path, encoding='utf-8'))
    selfcite = []
    for it in P.get('items', []):
        ans = it.get('answer')
        for fld in ('explanation', 'check'):
            t = it.get(fld) or ''
            if 'option' not in t.lower(): continue
            cited = set()
            for m in re.finditer(r'[Oo]ptions?\s+([ABCD](?:\s*(?:,|and|or)\s*[ABCD])*)', t):
                cited |= set(re.findall(r'[ABCD]', m.group(1)))
            if ans in cited: selfcite.append((it['id'], fld, ans))
    for x in selfcite: print('  SELF-CITED ANSWER: %s %s cites its own answer %s' % x)
    if selfcite:
        print('FAILED: pool cites its own answer as an option; fix before pushing'); failed = True
    else:
        print('option references consistent with the keys')
    # Key spread (SPEC.md, "Spreading the keys"): a letter that is never right, or almost never, lets a learner guess the
    # pattern. Every existing pool gives each letter at least 2 correct answers, so that is the floor.
    counts = dict.fromkeys('ABCD', 0)
    for it in P.get('items', []):
        if it.get('answer') in counts: counts[it['answer']] += 1
    if sum(counts.values()) >= 10:
        low = [k for k, v in counts.items() if v < 2]
        if low:
            print('  KEY SPREAD: %s; letters %s are the answer to fewer than 2 questions' % (
                ' '.join('%s=%d' % kv for kv in counts.items()), ', '.join(low)))
            print('FAILED: spread the keys with the WANT table in lessons/TEMPLATE.py (SPEC.md, "Spreading the keys")')
            failed = True
        else:
            print('answer keys spread: ' + ' '.join('%s=%d' % kv for kv in counts.items()))
    return 1 if failed else 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python tools/audit-lesson.py seed/lesson_<stem>.json'); sys.exit(2)
    sys.exit(main(sys.argv[1]))
