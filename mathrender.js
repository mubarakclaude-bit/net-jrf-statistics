/* Render authored formulas for the exported documents, reusing the app's parser.
 *
 * The app lays formulas out properly but the PDF, Word and Markdown exports still showed
 * them as the one-line source — "∂²ℓ/∂p² = − x/p² − (1 − x)/(1 − p)²" — which is the form
 * that is hard to read and the form people actually review. This renders the SAME parse
 * tree three more ways, so there is one parser and no second implementation to drift:
 *
 *   print  HTML using inline-table rather than flexbox, because WeasyPrint lays tables
 *          out reliably and flex only partly;
 *   latex  for the Markdown export, where stacking is impossible but \frac{}{} is exact
 *          and unambiguous for a reader or a model;
 *   text   a plain fallback, unchanged, for anything the parser refuses.
 *
 * Usage: node mathrender.js <in.json> <out.json>
 *   in:  ["formula string", ...]
 *   out: {"formula string": {"print": "<...>", "latex": "...", "ok": true}, ...}
 *
 * Every rendering is checked character by character against the input before it is
 * returned; a formula that fails the check is returned as plain text instead.
 */
const fs = require("fs");

const esc = s => String(s == null ? "" : s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const ctx = {};
new Function("ctx", "const esc=ctx.esc;" + fs.readFileSync("src/32-math.js", "utf8") +
  ";ctx.mathTree=mathTree;ctx.mathBare=mathBare;ctx.mathVis=mathVis;ctx.MOPEN=MOPEN;ctx.richText=richText;")(
  Object.assign(ctx, { esc }));
const { mathTree, mathBare, mathVis, MOPEN } = ctx;

/* ---- print HTML: inline-table fractions, which WeasyPrint stacks correctly ---- */
function printHTML(nodes) {
  return nodes.map(n => {
    if (n.t === "id" || n.t === "op") return esc(n.v);
    if (n.t === "app") return printHTML(n.kids);
    if (n.t === "grp") {
      const inner = printHTML(n.kids);
      return (n.kids.length === 1 && n.kids[0].t === "frac") ? inner
        : esc(n.open) + inner + esc(n.close);
    }
    if (n.t === "sup") {
      const e = n.sup;
      return printHTML([n.base]) + "<sup>" + (e.t === "grp" ? printHTML(e.kids) : printHTML([e])) + "</sup>";
    }
    if (n.t === "frac")
      return '<span class="pfrac"><span class="pnum">' + printHTML([n.num]) +
             '</span><span class="pden">' + printHTML([n.den]) + "</span></span>";
    return "";
  }).join("");
}

/* ---- LaTeX ---- */
function latex(nodes) {
  return nodes.map(n => {
    if (n.t === "id" || n.t === "op") return n.v;
    if (n.t === "app") return latex(n.kids);
    if (n.t === "grp") {
      const inner = latex(n.kids);
      return (n.kids.length === 1 && n.kids[0].t === "frac") ? inner : n.open + inner + n.close;
    }
    if (n.t === "sup") {
      const e = n.sup;
      return latex([n.base]) + "^{" + (e.t === "grp" ? latex(e.kids) : latex([e])) + "}";
    }
    if (n.t === "frac") return "\\frac{" + latex([n.num]) + "}{" + latex([n.den]) + "}";
    return "";
  }).join("");
}

const visText = h => mathVis(h);
const latexBare = t => String(t).replace(/\\frac|[{}()[\]\s^/\\]/g, "");

/* a spaced slash at bracket depth zero, exactly one of them: whole-side fraction */
function splitSeg(seg) {
  const cuts = [];
  let d = 0;
  for (let i = 0; i < seg.length; i++) {
    const c = seg[i];
    if (MOPEN[c]) d++;
    else if (c === ")" || c === "]" || c === "}") d--;
    else if (c === "/" && d === 0) cuts.push(i);
  }
  if (cuts.length !== 1) return null;
  const at = cuts[0];
  if (!/\s/.test(seg[at - 1] || "") || !/\s/.test(seg[at + 1] || "")) return null;
  const num = seg.slice(0, at).trim(), den = seg.slice(at + 1).trim();
  return (num && den) ? [num, den] : null;
}

function piece(seg, mode) {
  const t = mathTree(seg);
  if (!t) return mode === "print" ? esc(seg) : seg;
  const out = mode === "print" ? printHTML(t) : latex(t);
  const bare = mode === "print" ? mathBare(visText(out)) : latexBare(out);
  return bare === mathBare(seg) ? out : (mode === "print" ? esc(seg) : seg);
}

const PBREAK = 30;            // plain characters before a chain is worth breaking
function render(src, mode) {
  const parts = String(src).split(/(\s(?:=|⟺|⟹|⇒|≡|≈|≤|≥|∝)\s)/);
  const lines = [];
  let cur = "", plain = "";
  parts.forEach((p, i) => {
    if (i % 2 === 1) {
      if (plain.length >= PBREAK) { if (cur.trim()) lines.push(cur); cur = ""; plain = "" }
      cur += (cur ? " " : "") +
             (mode === "print" ? '<span class="prel">' + esc(p.trim()) + "</span> " : p.trim() + " ");
      plain += p;
    } else {
      plain += p;
      const sp = splitSeg(p);
      if (sp) {
        const [num, den] = sp;
        cur += mode === "print"
          ? '<span class="pfrac wide"><span class="pnum">' + piece(num, mode) +
            '</span><span class="pden">' + piece(den, mode) + "</span></span>"
          : "\\frac{" + piece(num, mode) + "}{" + piece(den, mode) + "}";
      } else cur += piece(p, mode);
    }
  });
  if (cur.trim()) lines.push(cur);
  return mode === "print"
    ? '<div class="pmath">' + lines.map(l => '<div class="pline">' + l + "</div>").join("") + "</div>"
    : lines.join("\n    ");
}

const input = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const out = {};
let laid = 0, plain = 0;
for (const s of input) {
  const pr = render(s, "print"), la = render(s, "latex");
  const okp = mathBare(visText(pr)) === mathBare(s);
  const okl = latexBare(la) === mathBare(s);
  out[s] = {
    print: okp ? pr : '<div class="pmath"><div class="pline">' + esc(s) + "</div></div>",
    latex: okl ? la : null,
    rich: ctx.richText(s),
    ok: okp && okl,
  };
  if (okp && /pfrac|<sup>/.test(pr)) laid++; else plain++;
}
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
console.error("rendered %d formulas: %d laid out, %d plain", input.length, laid, plain);
