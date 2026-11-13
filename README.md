# UGC NET Statistics (JRF) — study-content pipeline

Authoring pipeline and source for a personalised UGC NET Statistics Paper 2 preparation app. This repository is the
source of truth: the hosted site (Vercel) is built from it, and the Claude artifact is retired as a publishing target.
The current lesson count is `counts.lessons` in `site/manifest.json` (written by `npm run build`, served at `/manifest.json`);
no count in a document is kept current.

**Start with [`AGENTS.md`](AGENTS.md)** (what you may do and how a pull request is verified), then
[`docs/CONTENT_GUIDE.md`](docs/CONTENT_GUIDE.md) (what content exists, where it lives, how to tune it). The live content map is
on the `content-map` branch, or run `npm run content -- map`.

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
| `docs/` | `CONTENT_GUIDE.md` (learn and tune the content), independence and contract notes, and older build notes. |
| `tools/content.js` | The content map: what lessons, pools and previous-year material exist, where they live, and what is missing. |

## Authoring a lesson

```sh
./addlesson.sh lesson_xx1.py lesson_xx1 module-t1 modulet1 module_t1_mastery
node test.js && node clicktest.js
```

`addlesson.sh` refuses to proceed on a structural failure, a formula that will not render,
or a pool item whose explanation cites its own answer as a distractor. Do not push a lesson
it has not passed clean.

## What to build next

**[`BACKLOG.md`](BACKLOG.md) is the queue.** Take the top unchecked item, build it, tick it off,
commit. It is ordered by marks still exposed, and it records which previous-year questions were
answered wrongly — those anchors are worth more, because the variant bank doubles as a diagnosis.

## Authoring from a phone

Three routes, in increasing order of what they can do:

1. **In the app** — Admin tab, pick module and topic, press *Author it here*. Drafts, validates and
   previews without leaving the page. It cannot check a number, so it is for conceptual topics;
   the validator now rejects any draft claiming a figure was verified or simulated.
2. **A fresh chat** — Admin tab, *Copy prompt for a chat*, paste into a **new** chat. The prompt
   bootstraps from this repo, so each lesson is a self-contained conversation.
3. **An issue here** — open one from the *Author a lesson* template, then paste the one-line
   instruction it contains into a new chat.

Any session that can write to this repository can finish a lesson: it commits the seed files, CI verifies
them, and merging publishes them through Vercel. No artifact or store write is involved.
`npm run lesson -- brief <topicId>` prints the work order for a topic.

## Current state

See [`docs/app-build-state.md`](docs/app-build-state.md) for the live inventory and
[`docs/pyq-priority.md`](docs/pyq-priority.md) for the scoring analysis behind the ordering.
