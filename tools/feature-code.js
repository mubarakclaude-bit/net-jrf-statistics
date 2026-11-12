/* Static check of a feature's index.js against its manifest. Used by tools/validate-contracts.js.
 *
 * THE RULE (documented in contracts/README.md and AGENTS.md):
 *   A feature may use learner storage ONLY as   ctx.store.get("key") / ctx.store.set("key", value) / ctx.store.remove("key")
 *   where "key" is a plain string literal that feature.json declares in "storage".
 *   Dynamic keys are NOT supported: a variable, a concatenation, a template with an expression, a computed member
 *   (ctx.store["set"]), an alias (const s = ctx.store), a destructured store, ctx.store passed to another function, or
 *   .call/.apply on a store method are all rejected, because none of them can be proven to stay inside the declared keys.
 *   The check also rejects direct use of the globals that reach storage or app state without going through ctx.store:
 *   S, localStorage, sessionStorage, indexedDB, FEATURES, claude, upath (also as window.X / globalThis.X).
 *
 * WHAT THIS IS, AND IS NOT: it parses the code (acorn) and walks the syntax tree, so it does not depend on how the code is
 * formatted and cannot be fooled by a regular expression's blind spots. It is a guard against mistakes and against the
 * common ways to reach around ctx.store, not a sandbox: determined obfuscation (for example building a property name from
 * pieces and indexing ctx with it) is not caught. The runtime guard is the real enforcement: ctx.store itself refuses an
 * undeclared key, and every feature's browser test runs in strict storage-path mode. Features are reviewed code. */
const acorn = require("acorn");

const METHODS = new Set(["get", "set", "remove"]);
const FORBIDDEN = new Set(["S", "localStorage", "sessionStorage", "indexedDB", "FEATURES", "claude", "upath"]);
const CODE_FROM_STRING = new Set(["eval", "Function"]);          // run code the check cannot see, so they would defeat it
const GLOBAL_OBJECTS = new Set(["window", "globalThis", "self"]);

function walk(node, stack, visit) {
  visit(node, stack);
  stack.push(node);
  for (const key of Object.keys(node)) {
    if (key === "loc" || key === "start" || key === "end" || key === "type") continue;
    const v = node[key];
    if (Array.isArray(v)) { for (const c of v) if (c && typeof c.type === "string") walk(c, stack, visit); }
    else if (v && typeof v.type === "string") walk(v, stack, visit);
  }
  stack.pop();
}
const propName = m => (!m.computed && m.property.type === "Identifier") ? m.property.name
  : (m.computed && m.property.type === "Literal" && typeof m.property.value === "string") ? m.property.value : null;

/* Returns an array of problem strings ("line N: ..."); empty means the code conforms. */
function analyzeFeatureCode(source, declared) {
  const problems = [], decl = new Set(declared || []);
  let ast;
  try { ast = acorn.parse(source, { ecmaVersion: 2022, allowReturnOutsideFunction: true, locations: true }); }
  catch (e) { return ["does not parse: " + e.message]; }
  const bad = (n, msg) => problems.push("line " + n.loc.start.line + ": " + msg);

  walk(ast, [], (node, stack) => {
    const parent = stack[stack.length - 1], grand = stack[stack.length - 2];

    // ---- ctx.store: only ctx.store.<get|set|remove>("declared literal", ...)
    if (node.type === "MemberExpression" && propName(node) === "store") {
      if (node.computed) bad(node, 'use ctx.store, not computed access like ctx["store"]');
      const asObject = parent && parent.type === "MemberExpression" && parent.object === node && !parent.computed
        && parent.property.type === "Identifier" && METHODS.has(parent.property.name);
      const asCall = asObject && grand && grand.type === "CallExpression" && grand.callee === parent;
      if (!asCall) bad(node, "ctx.store may only be used as ctx.store.get(...), ctx.store.set(...) or ctx.store.remove(...), called directly; found an alias, a computed member, a passed or destructured store, or .call/.apply");
      else {
        const key = grand.arguments[0], method = parent.property.name;
        if (!key || key.type !== "Literal" || typeof key.value !== "string") bad(grand, "ctx.store." + method + " must be called with a string literal key that feature.json declares in \"storage\"; a variable, expression or missing key is not supported because it cannot be checked");
        else if (!decl.has(key.value)) bad(grand, "ctx.store." + method + " uses storage key '" + key.value + "' which feature.json does not declare in \"storage\"");
      }
    }
    // const { store } = ctx  /  function (ctx) -> ({ store })
    if (node.type === "Property" && parent && parent.type === "ObjectPattern") {
      const k = node.key, name = k.type === "Identifier" && !node.computed ? k.name : (k.type === "Literal" ? k.value : null);
      if (name === "store") bad(node, "do not destructure store out of ctx; call ctx.store.get/set/remove directly");
    }

    // ---- globals that reach storage or app state without ctx.store
    if (node.type === "Identifier" && FORBIDDEN.has(node.name)) {
      const isPropertyName = parent && parent.type === "MemberExpression" && parent.property === node && !parent.computed;
      const isKey = parent && (parent.type === "Property" || parent.type === "MethodDefinition" || parent.type === "PropertyDefinition") && parent.key === node && !parent.computed && !(parent.shorthand);
      if (!isPropertyName && !isKey) bad(node, "'" + node.name + "' reaches storage or app state without going through ctx.store; use ctx.store (declare the key in feature.json) instead");
    }
    if (node.type === "Identifier" && CODE_FROM_STRING.has(node.name)) {
      const isPropertyName = parent && parent.type === "MemberExpression" && parent.property === node && !parent.computed;
      if (!isPropertyName) bad(node, "'" + node.name + "' runs code that this check cannot see, which would defeat the storage rule; write the code directly");
    }
    if (node.type === "MemberExpression" && node.object.type === "Identifier" && GLOBAL_OBJECTS.has(node.object.name)) {
      const n = propName(node);
      if (n && CODE_FROM_STRING.has(n)) bad(node, "'" + n + "' (as " + node.object.name + "." + n + ") runs code that this check cannot see, which would defeat the storage rule; write the code directly");
      else if (n && FORBIDDEN.has(n)) bad(node, node.object.name + "." + n + " reaches storage or app state without going through ctx.store");
    }
  });
  return problems;
}

module.exports = { analyzeFeatureCode };
