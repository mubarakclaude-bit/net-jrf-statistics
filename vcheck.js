/* Static validation of a lesson seed against the app's own vScene, without a browser.
   Pulls VIZ_OK and vScene straight out of src/62-gen.js so the check cannot drift. */
const fs = require("fs");
const src = fs.readFileSync("src/62-gen.js", "utf8");

function grab(name, kind) {
  const i = src.indexOf((kind === "fn" ? "function " : "const ") + name);
  if (i < 0) throw new Error("cannot find " + name);
  if (kind !== "fn") {
    const semi = src.indexOf(";", i);
    return src.slice(i, semi + 1);
  }
  // walk braces from the first { after the signature
  let b = src.indexOf("{", i), d = 0, j = b;
  for (; j < src.length; j++) {
    if (src[j] === "{") d++;
    else if (src[j] === "}") { d--; if (!d) break; }
  }
  return src.slice(i, j + 1);
}

const ctx = {};
// Everything vScene CALLS has to be grabbed too, or the eval'd copy throws
// "X is not defined" at validation time. Adding a helper call inside vScene in
// src/62-gen.js without adding it here breaks addlesson.sh — which is exactly what
// happened when the fabricated-evidence check was introduced.
const NEEDED = [["VIZ_OK", null], ["vScene", "fn"]];
try {
  new Function("ctx", NEEDED.map(([n, k]) => grab(n, k)).join("\n") +
    "ctx.vScene=vScene;ctx.VIZ_OK=VIZ_OK;")(ctx);
} catch (e) {
  console.error("vcheck could not assemble vScene from src/62-gen.js: " + e.message);
  console.error("If vScene now calls a new helper, add it to the NEEDED list above.");
  process.exit(1);
}

const path = process.argv[2] || "seed/lesson_t1.json";
const L = JSON.parse(fs.readFileSync(path, "utf8"));
let errs = [];
L.scenes.forEach((s, i) => { errs = errs.concat(ctx.vScene(s, i) || []); });

// house-standard checks the plan validator applies, run against the finished lesson
const kinds = L.scenes.map(s => s.kind);
const house = [];
if (kinds[0] !== "foundation") house.push("scene 1 is not the foundation drill");
const needKinds = ["foundation", "intuition", "theory", "guided", "trapcheck", "summary", "quiz"]
  .concat(L.engine === "A" ? [] : ["worked"]);   // engine A has no worked scene by design
needKinds.forEach(k => { if (kinds.indexOf(k) < 0) house.push("no " + k + " scene"); });
if (kinds.filter(k => k === "guided").length < 2) house.push("fewer than 2 guided scenes");
// The 11-16 house range governs the CORE path. Scenes marked ext:true are optional
// "JRF extension" material and sit outside it; the whole lesson is capped at 18.
const core = L.scenes.filter(s => !s.ext), extn = L.scenes.filter(s => s.ext);
if (core.length < 11 || core.length > 16)
  house.push(core.length + " core scenes, wanted 11-16");
if (L.scenes.length > 18) house.push(L.scenes.length + " scenes in all, cap is 18");
if (extn.some(s => s.kind === "quiz")) house.push("the mastery test cannot be an optional extension");
if (extn.some(s => ["foundation", "summary"].indexOf(s.kind) >= 0))
  house.push("the foundation and summary scenes cannot be optional");
// a quick check on every teaching scene that is not itself a check
const SELFCHECK = ["recall", "completion", "trapcheck", "guided", "summary", "quiz"];
const atV41 = parseFloat(L.version || "0") >= 4.1, advisory = [];
L.scenes.forEach((s, i) => {
  if (SELFCHECK.indexOf(s.kind) < 0 && !(s.ask && s.ask.q && s.ask.nudge))
    (atV41 ? house : advisory).push("scene " + (i + 1) + " (" + s.kind + ") has no quick check");
});
// reference tables must be rectangular
L.scenes.forEach((s, i) => {
  if (!s.table) return;
  const w = (s.table.head || []).length;
  if (w < 2) house.push("scene " + (i + 1) + " table has fewer than 2 columns");
  (s.table.rows || []).forEach((r, k) => {
    if (r.length !== w) house.push("scene " + (i + 1) + " table row " + (k + 1) +
      " has " + r.length + " cells, header has " + w);
  });
  if (!(s.table.rows || []).length) house.push("scene " + (i + 1) + " table has no rows");
});
if (!L.howto) (atV41 ? house : advisory).push("no 'how to use this lesson' note");
if (!L.scenes.filter(s => s.flow).length) house.push("no flow diagram anywhere");
if (L.scenes.filter(s => s.scenario).length < 2) house.push("fewer than 2 scenarios");
if ((L.objectives || []).length < 4) house.push("fewer than 4 objectives");
if ((L.prereq || []).length < 3) house.push("fewer than 3 prerequisites");
if ((L.refs || []).length < 3) house.push("fewer than 3 references");
const R = L.revision || {};
if ((R.sheet || []).length < 8) house.push("revision sheet under 8 lines");
if ((R.cards || []).length < 6) house.push("fewer than 6 cards");
if ((R.tricks || []).length < 3) house.push("fewer than 3 tricks");
if ((R.shortcuts || []).length < 3) house.push("fewer than 3 shortcuts");
if ((R.remember || []).length < 2) house.push("fewer than 2 remember lines");
(R.cards || []).forEach((c, i) => {
  if (!Array.isArray(c) || c.length !== 2) house.push("card " + (i + 1) + " is not a pair");
});
if (!L.provenance) house.push("no provenance");

// every scene id must be unique, and no scene may reference a viz the app lacks
const ids = {};
L.scenes.forEach(s => { if (ids[s.id]) house.push("duplicate scene id " + s.id); ids[s.id] = 1; });

const all = errs.concat(house);
if (advisory.length)
  console.log("below the v4.1 standard (" + advisory.length + ", not failures — this lesson is v" +
    (L.version || "?") + "): " + advisory.join("; "));
console.log(path + ": " + L.scenes.length + " scenes, v" + L.version + ", est " + L.estMin + " min");
if (!all.length) console.log("VALIDATORS PASS — no structural errors");
else { console.log("FAILURES (" + all.length + "):"); all.forEach(e => console.log("  - " + e)); process.exit(1); }

/* ---- the mastery pool, when one is named by a quiz scene ---- */
(function () {
  const fs2 = require("fs");
  const qs = L.scenes.filter(s => s.kind === "quiz" && s.setId);
  qs.forEach(sc => {
    const f = "seed/" + sc.setId + ".json";
    if (!fs2.existsSync(f)) { console.log("pool " + sc.setId + ": FILE MISSING"); process.exitCode = 1; return; }
    const P = JSON.parse(fs2.readFileSync(f, "utf8"));
    const items = P.items || [];
    const e = [];
    if (items.length !== 20) e.push(items.length + " items, wanted 20");
    const by = k => items.reduce((a, q) => (a[q[k]] = (a[q[k]] || 0) + 1, a), {});
    const d = by("diff"), keys = by("answer"), fmt = by("format");
    if (d.easy !== 6 || d.moderate !== 10 || d.hard !== 4)
      e.push("difficulty mix " + JSON.stringify(d) + ", wanted 6/10/4");
    "ABCD".split("").forEach(k => {
      if ((keys[k] || 0) > Math.ceil(items.length * 0.4))
        e.push("answer " + k + " used " + keys[k] + " times, over the 40% cap");
    });
    if ((fmt.numeric || 0) < 4) e.push("fewer than 4 numeric items");
    if ((fmt.multi || 0) < 2) e.push("fewer than 2 multi items");
    items.forEach(q => {
      const at = q.id;
      if (!q.stem || !q.answer || (q.options || []).length !== 4) e.push(at + " malformed");
      if ("ABCD".indexOf(q.answer) < 0) e.push(at + " key is not A-D");
      if (q.format === "numeric" && !q.check) e.push(at + " numeric with no arithmetic check");
      if (q.format === "multi") {
        if ((q.statements || []).length !== 4) e.push(at + " multi needs 4 statements");
        const v = q.verdicts || {};
        "ABCD".split("").forEach(k => {
          if (!v[k] || typeof v[k].tf !== "boolean" || !v[k].why)
            e.push(at + " statement " + k + " has no verdict or reason");
        });
      }
      if (q.format === "order" && (q.items || []).length !== 4) e.push(at + " order needs 4 steps");
      if (!q.explanation && !q.check) e.push(at + " has no explanation");
      // Two related defects, both found by review rather than by a validator.
      // (a) a stem asking only for "sufficient" while a distractor is itself sufficient:
      //     a pair containing a sufficient statistic is sufficient, so there are two keys.
      const st = (q.stem || "").toLowerCase();
      if (/sufficient statistic/.test(st) && !/minimal/.test(st) &&
          (q.options || []).some(o => /^\(.*,.*\)$/.test(o.trim())))
        e.push(at + " asks for 'a sufficient statistic' but offers a pair as an option — " +
                    "a pair containing a sufficient statistic is itself sufficient, so the item has two keys");
      // (b) the confession check. A one-to-one function of a minimal sufficient statistic
      //     IS minimal sufficient, so an item whose own explanation concedes a distractor
      //     is "a one-to-one transform" has a second key whenever the stem asks loosely
      //     for "the minimal sufficient statistic". The admission in the explanation is
      //     the reliable tell; the fix is to name the statistic in the stem.
      const blob = (q.explanation || "") + " " + (q.check || "");
      if (/one-to-one (transform|function)/i.test(blob) &&
          /minimal sufficient statistic/i.test(st) &&
          !/\bT = |\btaking t\b/i.test(q.stem || ""))
        e.push(at + " concedes in its explanation that a distractor is a one-to-one transform, " +
                    "but the stem asks loosely for 'the minimal sufficient statistic' — a one-to-one " +
                    "transform of it is also minimal sufficient, so name the statistic in the stem");
    });
    console.log("pool " + sc.setId + ": " + items.length + " items, keys " +
      "ABCD".split("").map(k => k + "=" + (keys[k] || 0)).join(" ") + ", formats " + JSON.stringify(fmt));
    if (e.length) { console.log("  POOL FAILURES:"); e.forEach(x => console.log("   - " + x)); process.exitCode = 1; }
    else console.log("  pool passes");
  });
})();
