/* ===================== formula layout =====================
   Formulas were authored on one line, with exponents as ^(...) and denominators as a
   slash: "f = θ^(−n) · I(max ≤ θ)", "x/p − (1 − x)/(1 − p)". Readable to someone fluent,
   hard work for everyone else, which is the wrong way round for this app. This renders
   them as they look on paper: exponents raised, denominators under a rule.

   Two passes. The first lexes the string into atoms — a balanced bracket group, a run of
   identifier characters, or a single other character. The second folds ^ onto the atom
   before it (tighter), then / into a fraction of the atoms either side. Anything that
   does not lex cleanly is returned in the old one-line form: showing a formula plainly
   costs little, showing a rearranged formula costs a mark.

   Two checks guard it, because one was not enough. Character preservation catches dropped
   or duplicated symbols. It does NOT catch regrouping: an early version rendered p/p² as
   (p/p)², losing no characters while changing the formula. So the atom rules below keep a
   trailing exponent attached to its base, and mathtest.js asserts the exact structure of
   a set of known formulas rather than only their characters.
*/
const MATHCACHE = {};

/* identifier characters: letters, digits, Greek, the operators that bind to a symbol
   rather than separate it, Unicode sub/superscripts, primes and accents */
const MIDENT = /[A-Za-z0-9α-ωΑ-Ω∂ℓΣ∏√θλμσπβγδεζηικνξορτυφχψ₀-₉ᵢⱼₙₖₜ⁰-⁹¹²³ⁿ̄̂'′!]/;
const MOPEN = { "(": ")", "[": "]", "{": "}" };

function mathLex(s) {
  const out = [];
  let i = 0;
  while (i < s.length) {
    const c = s[i];
    if (MOPEN[c]) {
      let d = 0, j = i;
      for (; j < s.length; j++) {
        if (MOPEN[s[j]]) d++;
        else if (s[j] === ")" || s[j] === "]" || s[j] === "}") { d--; if (!d) break }
      }
      if (j >= s.length) return null;                       // unbalanced
      const inner = mathLex(s.slice(i + 1, j));
      if (!inner) return null;
      out.push({ t: "grp", open: c, close: s[j], kids: inner });
      i = j + 1;
    } else if (c === ")" || c === "]" || c === "}") {
      return null;                                           // stray close
    } else if (MIDENT.test(c)) {
      let v = "";
      while (i < s.length && MIDENT.test(s[i])) { v += s[i]; i++ }
      out.push({ t: "id", v: v });
    } else {
      out.push({ t: "op", v: c });
      i++;
    }
  }
  return out;
}

const isAtom = n => n && (n.t === "grp" || n.t === "id" || n.t === "sup" ||
                          n.t === "frac" || n.t === "app");

function mathFold(toks) {
  // pass 1 — ^ binds to the single atom immediately before it
  let a = [];
  for (let i = 0; i < toks.length; i++) {
    const t = toks[i];
    if (t.t === "op" && t.v === "^") {
      const base = a[a.length - 1], nxt = toks[i + 1];
      if (!isAtom(base) || !isAtom(nxt)) return null;
      a.pop();
      a.push({ t: "sup", base: base, sup: nxt });
      i++;
    } else a.push(t);
  }
  // pass 2 — juxtaposition: atoms written side by side with nothing between them are one
  // atom, so p(1−p), C(n,t) and ∏xᵢ! each go whole into a numerator or denominator
  let j = [];
  for (let i = 0; i < a.length; i++) {
    const t = a[i];
    if (isAtom(t) && isAtom(j[j.length - 1])) {
      const prev = j.pop();
      j.push({ t: "app", kids: (prev.t === "app" ? prev.kids : [prev]).concat([t]) });
    } else j.push(t);
  }
  // pass 3 — / makes a fraction of the atoms either side
  let b = [];
  for (let i = 0; i < j.length; i++) {
    const t = j[i];
    if (t.t === "op" && t.v === "/") {
      const num = b[b.length - 1], den = j[i + 1];
      if (!isAtom(num) || !isAtom(den)) return null;
      b.pop();
      b.push({ t: "frac", num: num, den: den });
      i++;
    } else b.push(t);
  }
  return b;
}

function mathRender(nodes) {
  return nodes.map(n => {
    if (n.t === "id" || n.t === "op") return esc(n.v);
    if (n.t === "grp") {
      const inner = mathRender(n.kids);
      // brackets whose only job was to delimit a fraction can go
      return (n.kids.length === 1 && n.kids[0].t === "frac")
        ? inner : esc(n.open) + inner + esc(n.close);
    }
    if (n.t === "app") return mathRender(n.kids);
    if (n.t === "sup") {
      const e = n.sup;
      const inner = (e.t === "grp") ? mathRender(e.kids) : mathRender([e]);
      return mathRender([n.base]) + "<sup>" + inner + "</sup>";
    }
    if (n.t === "frac")
      return '<span class="frac"><span class="fnum">' + mathRender([n.num]) +
             '</span><span class="fden">' + mathRender([n.den]) + "</span></span>";
    return "";
  }).join("");
}

function mathWalk(nodes) {                 // fold inside groups too
  return nodes.map(n => {
    if (n.t !== "grp") return n;
    const k = mathFold(mathWalk(n.kids));
    return k ? { t: "grp", open: n.open, close: n.close, kids: k } : null;
  });
}

const mathBare = t => String(t).replace(/[()[\]{}\s^/]/g, "");
const mathVis = h => h.replace(/<[^>]*>/g, "").replace(/&amp;/g, "&")
  .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");

/* The parsed tree, or null when the string does not parse. Exposed so the document
   exporters can render the SAME tree to print HTML and to LaTeX without a second parser
   that could drift away from this one. */
function mathTree(src) {
  const lex = mathLex(String(src));
  if (!lex) return null;
  const walked = mathWalk(lex);
  if (walked.indexOf(null) >= 0) return null;
  return mathFold(walked);
}

function mathHTML(src) {
  const key = String(src);
  if (MATHCACHE[key] !== undefined) return MATHCACHE[key];
  let html = '<span class="mplain">' + esc(key) + "</span>";
  if (/[\^/]/.test(key)) {
    const tree = mathTree(key);
    if (tree) {
      const rich = mathRender(tree);
      if (mathBare(mathVis(rich)) === mathBare(key)) html = rich;
    }
  }
  MATHCACHE[key] = html;
  return html;
}

/* A spaced slash — "λ̂ = n / Σxᵢ" — is division too, but the atoms around it are whole
   expressions rather than single symbols, so the rule above will not touch it. Handle it
   only where the split is unambiguous: exactly ONE slash at bracket depth zero in this
   side of the equation, in which case everything left of it is the numerator and
   everything right of it the denominator. A segment with two or more, such as
   "CPI (Rural / Urban / Combined)", is a list and is left alone. */
function segHTML(seg) {
  const cuts = [];
  let d = 0;
  for (let i = 0; i < seg.length; i++) {
    const c = seg[i];
    if (MOPEN[c]) d++;
    else if (c === ")" || c === "]" || c === "}") d--;
    else if (c === "/" && d === 0) cuts.push(i);
  }
  if (cuts.length === 1) {
    const at = cuts[0];
    const num = seg.slice(0, at).trim(), den = seg.slice(at + 1).trim();
    if (num && den && /\s/.test(seg[at - 1] || "") && /\s/.test(seg[at + 1] || "")) {
      const html = '<span class="frac wide"><span class="fnum">' + mathHTML(num) +
                   '</span><span class="fden">' + mathHTML(den) + "</span></span>";
      if (mathBare(mathVis(html)) === mathBare(seg)) return html;
    }
  }
  return mathHTML(seg);
}

/* A chain of equalities is long enough to wrap awkwardly, so break it at the relation
   symbols: each step starts its own line instead of folding mid-expression. */
const FBREAK = 30;            // plain characters before a chain is worth breaking
function formulaHTML(src) {
  const parts = String(src).split(/(\s(?:=|⟺|⟹|⇒|≡|≈|≤|≥|∝)\s)/);
  let out = "", line = "", plain = "";
  const flush = () => {
    if (line.trim()) out += '<span class="fline">' + line + "</span>";
    line = ""; plain = "";
  };
  parts.forEach((p, i) => {
    if (i % 2 === 1) {
      if (plain.length >= FBREAK) flush();
      line += (line ? " " : "") + '<span class="frel">' + esc(p.trim()) + "</span> ";
      plain += p;
    } else { line += segHTML(p); plain += p }
  });
  flush();
  return '<div class="fmath">' + out + "</div>";
}

/* ---- maths inside running prose ----
   Most formulas in this app are not standalone: they sit inside a sentence — "Bernoulli:
   f = p^Σx(1−p)^(n−Σx) = [p/(1−p)]^Σx (1−p)ⁿ · 1, so T = Σxᵢ with h = 1/∏xᵢ!". Those were
   showing the caret and the slash as typed, which is the thing that makes a line of
   mathematics unreadable.

   This finds the mathematical fragments inside the prose and sets them properly, with
   denominators under a rule and exponents raised, leaving the English untouched. A
   fragment is a run with no spaces in it that contains ^ or / and whose brackets balance;
   it is handed to the same parser the display formulas use, so prose and display can
   never disagree about what a formula means.

   An earlier version raised exponents but left fractions slashed, on the grounds that a
   stacked fraction mid-sentence disturbs the line spacing. It does, and the fix for that
   is line-height on the paragraph, not leaving the mathematics harder to read. */

/* "and/or" is not a fraction. Reject a fragment where either side of the slash is an
   ordinary English word, while allowing the function names that really do appear. */
const MFUNC = /^(log|ln|exp|max|min|var|cov|sup|inf|lim|det|sin|cos|tan|arg)$/i;
function proseMath(run) {
  if (!/[\^/]/.test(run)) return null;
  // A word of three letters or more is prose unless it is a known function, is applied to
  // brackets — Multinomial(t, 1/n), Var(T) — or is a short all-capitals symbol such as
  // CRLB. Without this "and/or" and "yes/no" would be set as fractions.
  const re = /[A-Za-z]{3,}/g;
  let w;
  while ((w = re.exec(run))) {
    const word = w[0], after = run[w.index + word.length];
    if (MFUNC.test(word)) continue;
    if (after === "(" || after === "[") continue;
    if (/^[A-Z]{2,6}$/.test(word)) continue;
    return null;
  }
  // A slash between two bare words is "or", not division: at least one side must carry a
  // digit, bracket or symbol. This keeps CSO/NSSO and moment/variance as they were.
  let d = 0;
  for (let i = 0; i < run.length; i++) {
    const c = run[i];
    if (MOPEN[c]) d++;
    else if (c === ")" || c === "]" || c === "}") d--;
    else if (c === "/" && d === 0) {
      const left = (run.slice(0, i).match(/[A-Za-z]+$/) || [""])[0];
      const right = (run.slice(i + 1).match(/^[A-Za-z]+/) || [""])[0];
      if (left && right && left === run.slice(0, i) && right === run.slice(i + 1) &&
          Math.max(left.length, right.length) >= 3) return null;
    }
  }
  const tree = mathTree(run);
  if (!tree) return null;
  const html = mathRender(tree);
  return mathBare(mathVis(html)) === mathBare(run) ? html : null;
}

function richText(src) {
  const s = String(src == null ? "" : src);
  if (!/[\^/]/.test(s)) return esc(s);
  // Split on whitespace, but only whitespace OUTSIDE brackets: "f(x | θ)/f(y | θ)" is one
  // fragment even though it contains spaces, because they are inside the brackets.
  const parts = [];
  let d = 0, cur = "";
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (MOPEN[c]) d++;
    else if (c === ")" || c === "]" || c === "}") d = Math.max(0, d - 1);
    if (/\s/.test(c) && d === 0) { parts.push(cur); parts.push(c); cur = "" }
    else cur += c;
  }
  parts.push(cur);
  let out = "";
  for (const part of parts) {
    if (!part || /^\s*$/.test(part) || !/[\^/]/.test(part)) { out += esc(part); continue }
    const m = proseMath(part);
    if (m) { out += '<span class="imath">' + m + "</span>"; continue }
    if (MOPEN[part[0]]) {
      // The run is a whole bracketed clause — "(posterior Beta(9,6), mean 8/13, ...);" —
      // which picked up prose because its spaces sit at bracket depth 1. Peel the brackets
      // and treat the inside as prose again, which finds the fragments within it. Any
      // punctuation after the closing bracket is handled the same way.
      let d = 0, j = 0;
      for (; j < part.length; j++) {
        if (MOPEN[part[j]]) d++;
        else if (part[j] === ")" || part[j] === "]" || part[j] === "}") { d--; if (!d) break }
      }
      if (j < part.length && j > 1) {
        out += esc(part[0]) + richText(part.slice(1, j)) + esc(part[j]) +
               (j + 1 < part.length ? richText(part.slice(j + 1)) : "");
        continue;
      }
    }
    out += esc(part);
  }
  return mathBare(mathVis(out)) === mathBare(s) ? out : esc(s);
}
