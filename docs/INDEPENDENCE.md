# Independence: the exact point at which it is achieved

The owner's requirement: after the shared foundation is complete, the owner can ask GPT to create a lesson or an
application feature directly in GitHub, and can ask Claude to do the same, independently. Neither needs the other's
session, files, instructions or availability.

This document says exactly when that is true, and how each condition is demonstrated by a command, not by argument.

## The four scenarios (GPT's wording, adopted)

| # | Scenario | Proven by |
|---|---|---|
| 1 | One author creates a new lesson while the other independently creates another; both merge in either order | `npm run acceptance`, scenario 1 |
| 2 | One author modifies an existing lesson while the other adds a different lesson; neither contribution is lost | scenario 2 |
| 3 | One author creates a new application feature without modifying the other's feature files or any shared wiring | scenario 3 |
| 4 | One author modifies an existing feature while the other creates a different feature; both integrate and build | scenario 4 |

Two more scenarios guard the boundary: **5**, a lesson or a feature that breaks its contract is rejected with a reason;
**6**, everything above runs from a clean copy of the repository's tracked files, with no session state, no private
tool and no Claude artifact.

Each scenario runs on a scratch copy of the repository (yours is never touched), with each "author" on their own branch,
touching only their own files, merging in **both orders**, then validating, building, running the features' own browser
tests, and requiring a **byte-identical** build whichever order was used.

## The point at which independence is achieved

It is achieved when **all five** of these are true, and not before:

1. **Foundation merged.** The contracts (`contracts/`), the generated index, the feature host and the storage façade
   (`ctx.store`), the CI workflow, and this acceptance test are on the production branch.
2. **Scenarios 1 to 6 pass** (`npm run acceptance` prints `0 failed`) on that branch, in CI, on a clean runner.
3. **CI is required.** Branch protection requires the `Validate` workflow (jobs `validate`, `browser`, `acceptance`)
   before a merge. This is a setting only the repository owner can change; until it is on, CI advises but does not stop.
4. **One real round trip each.** The owner has asked GPT to create a lesson and a feature in GitHub, and Claude to do
   the same, using only `AGENTS.md`; each PR passed CI and was merged without the other author's involvement. This is
   the only condition a command cannot prove, because it tests that the instructions work for a fresh session.
5. **No open exceptions that defeat it.** `contracts/legacy-exceptions.json` may list known content defects, but nothing
   in it may be a reason a conforming contribution would be rejected.

Conditions 1 to 3 are objective. Condition 4 is a one-time confirmation. After it, the claim is simply true.

## What independence covers, and what it does not yet

**Covered:** new and modified lessons and question pools; new features; modifications to features that exist as feature
modules (`src/features/<id>/`); changes to a feature's own storage keys, as long as they are declared in its manifest.

**Not covered, and said plainly:** the application's remaining built-in views (Home, Learn, Question bank, Mock tests,
Admin) are still the original single bundle, wired through `src/70-wire.js`. A change to one of them edits shared files,
so two authors changing the same built-in view can still conflict. They become independent as each is extracted into a
feature module; every extraction is an ordinary feature PR, and until a view is extracted the honest rule is
*one author at a time on that view*. **Progress was extracted first** (`src/features/progress/`, with `"replaces"`, and
proved byte-identical by `tools/golden-view.js`). The five still to extract are: Home, Learn, Question bank, Mock tests
and Admin.

**Storage backends:** the hosted browser backend is the supported one and is tested on every PR. The Claude artifact
backend is generated output; it shares the same interface and is checked only when someone runs a Claude session with
the `ArtifactData` tool. It is not required for independence.

## Reading the result

`npm run acceptance` ends with `N steps, 0 failed` when scenarios 1 to 6 hold. Any failure names the scenario and the
step. A failing scenario means independence is **not** achieved for that kind of contribution, regardless of how the
rest of the repository looks.
