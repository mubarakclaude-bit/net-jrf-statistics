# UGC NET Statistics (JRF) — study-content pipeline

Authoring pipeline for a personalised UGC NET Statistics Paper 2 preparation app.
The app itself is a Claude artifact; this repo holds everything that *builds* it.

**Read [`SPEC.md`](SPEC.md) before authoring anything.** It carries the house standard,
the pool rules, the registered visualisation names and the store layout.

## Layout

| Path | What it is |
|---|---|
| `src/*.js`, `src/*.html`, `src/*.css` | The app, in build order. `build.sh` concatenates these into `app.html`. |
| `build.sh` | Concatenate `src/` → `app.html`, then `node --check`. |
| `addlesson.sh` | The one command that generates, validates, renders, audits, wires and indexes a lesson. |
| `vcheck.js` | Structural validators for a lesson and its question pool. |
| `mathrender.js` | Renders every formula in a seed file, to catch anything the app cannot display. |
| `test.js`, `clicktest.js` | Headless suites. `test.js` first (it rebuilds the harness), then `clicktest.js`. |
| `lesson_*.py` | One authoring script per lesson. `lessons/EXAMPLE.py` is the pattern to copy. |
| `seed/` | Generated lesson JSON, question pools, the catalog, and the previous-year question banks. |
| `docs/` | Build state, priority order, and lessons learned the hard way. |

## Authoring a lesson

```sh
./addlesson.sh lesson_xx1.py lesson_xx1 module-t1 modulet1 module_t1_mastery
node test.js && node clicktest.js
```

`addlesson.sh` refuses to proceed on a structural failure, a formula that will not render,
or a pool item whose explanation cites its own answer as a distractor. Do not push a lesson
it has not passed clean.

## Current state

See [`docs/app-build-state.md`](docs/app-build-state.md) for the live inventory and
[`docs/pyq-priority.md`](docs/pyq-priority.md) for what to build next and why.
