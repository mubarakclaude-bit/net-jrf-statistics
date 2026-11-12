/* Executable form of contracts/storage-paths.json.
 *   checkDocPath("data/users/u1/p/demo/attempts") -> { ok: true, id: "progress-profile", params: {...} }
 *   checkDocPath("data/users/u1/progress-snapshots/x") -> { ok: false, reason: "forbidden path ..." }
 *
 * makeChecker() is deliberately SELF-CONTAINED (no closure over Node modules) so that exactly the same code runs in
 * three places: here in Node (tools/validate-contracts.js), inside test.js's database stub, and inside the hosted
 * app's shim (web/shim.js), which receives it through browserSource() at build time. One implementation means the
 * rule cannot drift between the validator, the tests and the product. */
const fs = require("fs"), path = require("path");
const CONTRACT = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "contracts", "storage-paths.json"), "utf8"));

function makeChecker(CONTRACT) {
  const SEG = new RegExp(CONTRACT.segmentPattern);
  const esc = s => s.replace(/[.*+?^${}()|[\]\\\/~-]/g, "\\$&");
  function compile(entry) {
    let src = "", last = 0, m;
    const re = /\{([a-z]+)\}/g;
    while ((m = re.exec(entry.pattern))) {
      src += esc(entry.pattern.slice(last, m.index));
      const p = (entry.params || {})[m[1]];
      let body = "[^/]+";
      if (Array.isArray(p)) body = p.map(esc).join("|");
      else if (p === "records") body = CONTRACT.records.map(esc).join("|");
      else if (typeof p === "string") body = p.replace(/^\^/, "").replace(/\$$/, "");
      src += "(?<" + m[1] + ">" + body + ")"; last = re.lastIndex;
    }
    return new RegExp("^" + src + esc(entry.pattern.slice(last)) + "$");
  }
  const DOCS = CONTRACT.documents.map(d => ({ id: d.id, re: compile(d) }));
  const FORBIDDEN = (CONTRACT.forbidden || []).map(d => ({ pattern: d.pattern, reason: d.reason, re: compile(d) }));
  const COLLS = CONTRACT.collections.map(c => compile({ pattern: c, params: { uid: "^[^/]+$", profile: "^[^/]+$" } }));
  function checkDocPath(p) {
    if (typeof p !== "string" || !p) return { ok: false, reason: "path is empty or not a string" };
    const segs = p.split("/");
    const bad = segs.find(s => !SEG.test(s) || s === "." || s === "..");
    if (bad !== undefined) return { ok: false, reason: "segment '" + bad + "' is not allowed (" + CONTRACT.segmentPattern + ")" };
    for (const f of FORBIDDEN) if (f.re.test(p)) return { ok: false, reason: "forbidden path " + f.pattern + ": " + f.reason };
    if (segs.length % 2) return { ok: false, reason: segs.length + " segments: an odd count is a collection path, not a document" };
    for (const d of DOCS) { const m = d.re.exec(p); if (m) return { ok: true, id: d.id, params: Object.assign({}, m.groups) }; }
    return { ok: false, reason: "no entry of contracts/storage-paths.json matches '" + p + "'" };
  }
  function checkCollectionPath(p) {
    const segs = String(p).split("/");
    if (segs.length % 2 === 0) return { ok: false, reason: segs.length + " segments: an even count is a document path, not a collection" };
    return COLLS.some(re => re.test(p)) ? { ok: true } : { ok: false, reason: "collection '" + p + "' is not listed in contracts/storage-paths.json" };
  }
  return { checkDocPath, checkCollectionPath };
}

/* JavaScript source that defines window.__NJ_PATHS = { checkDocPath, checkCollectionPath } in a browser page. */
function browserSource() { return "window.__NJ_PATHS = (" + makeChecker.toString() + ")(" + JSON.stringify(CONTRACT) + ");"; }

const bound = makeChecker(CONTRACT);
module.exports = { CONTRACT, makeChecker, browserSource, checkDocPath: bound.checkDocPath, checkCollectionPath: bound.checkCollectionPath };
