/* Static-hosting stand-in for the Claude artifact runtime.
 * The app asks `claude.use("db")`, "user", "sample", "downloads", "permissions".
 * Here: db = the bundled data.json (read-only content) plus this browser's own writes in
 * localStorage; user = a stable anonymous learner id; AI ("sample") and downloads are off,
 * so the app hides or disables those features exactly as it does in a view without them. */
(function () {
  var LS = "njdb:";
  var bundle = null;
  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function lsDel(k) { try { localStorage.removeItem(k); } catch (e) {} }
  function lsKeys() { var out = []; try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k && k.indexOf(LS) === 0) out.push(k.slice(LS.length)); } } catch (e) {} return out; }
  var mem = {};                                  // writes that could not be persisted
  function read(p) {
    if (Object.prototype.hasOwnProperty.call(mem, p)) return mem[p];
    var s = lsGet(LS + p);
    if (s !== null) { try { return JSON.parse(s); } catch (e) {} }
    return bundle[p];
  }
  function snap(p) {
    var d = read(p);
    return { id: p.split("/").pop(), exists: d !== undefined, data: function () { return d; },
             metadata: { fromCache: false, hasPendingWrites: false } };
  }
  function mkDoc(p) {
    return {
      id: p.split("/").pop(), path: p,
      get: async function () { return snap(p); },
      set: async function (b) {
        var j = JSON.stringify(b);
        if (lsSet(LS + p, j)) delete mem[p]; else mem[p] = JSON.parse(j);
      },
      update: async function (b) {
        var cur = read(p) || {}; var n = Object.assign({}, cur, b); var j = JSON.stringify(n);
        if (lsSet(LS + p, j)) delete mem[p]; else mem[p] = JSON.parse(j);
      },
      delete: async function () { lsDel(LS + p); delete mem[p]; },
      onSnapshot: function (next) { Promise.resolve().then(function () { next(snap(p)); }); return function () {}; },
      collection: function (sub) { return mkColl(p + "/" + sub); }
    };
  }
  function mkColl(cp, filters) {
    filters = filters || [];
    var q = {
      path: cp,
      doc: function (id) { return mkDoc(cp + "/" + (id || ("auto" + Math.random().toString(36).slice(2, 9)))); },
      add: async function (d) { var r = q.doc(); await r.set(d); return r; },
      where: function (f, op, v) { return mkColl(cp, filters.concat([[f, op, v]])); },
      orderBy: function () { return q; }, limit: function () { return q; },
      get: async function () {
        var seen = {}, paths = Object.keys(bundle).concat(lsKeys(), Object.keys(mem)), out = [];
        paths.forEach(function (p) {
          if (seen[p]) return; seen[p] = 1;
          var parts = p.split("/");
          if (parts.slice(0, -1).join("/") !== cp) return;
          var d = read(p); if (d === undefined) return;
          if (!filters.every(function (x) { return x[1] === "==" ? d[x[0]] === x[2] : true; })) return;
          out.push({ id: parts[parts.length - 1], exists: true, data: function () { return d; },
                     metadata: { fromCache: false, hasPendingWrites: false } });
        });
        out.sort(function (a, b) { return a.id < b.id ? -1 : 1; });
        return { docs: out, size: out.length, empty: !out.length, docChanges: function () { return []; },
                 metadata: { fromCache: false, hasPendingWrites: false } };
      },
      onSnapshot: function (next) { q.get().then(next); return function () {}; }
    };
    return q;
  }
  function learnerId() {
    var id = lsGet("njuid");
    if (!id) { id = "l" + Math.random().toString(36).slice(2, 12) + Date.now().toString(36); lsSet("njuid", id); }
    return id;
  }
  var dbPromise = null;
  function db() {
    if (!dbPromise) dbPromise = fetch("data.json", { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error("data.json " + r.status); return r.json();
    }).then(function (j) { bundle = j; return { doc: mkDoc, collection: function (p) { return mkColl(p); } }; })
      .catch(function () { return null; });
    return dbPromise;
  }
  window.claude = {
    use: async function (n) {
      if (n === "db") return db();
      if (n === "user") return {
        id: async function () { return learnerId(); },
        me: async function () { return { id: learnerId(), name: "" }; },
        isOwner: function () { return false; }, canEdit: function () { return false; }, can: function () { return false; }
      };
      return null;     // sample (AI), downloads, permissions: off in the hosted copy
    }
  };
})();
