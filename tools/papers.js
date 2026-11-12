/* Past papers: how the repository finds them and how the public build keeps the candidate's own answers out of them.
 *
 * A past paper is a question set whose file is  seed/pyq_<paperId>_full.json  and whose "source" is "pyq" (for example
 * pyq_j26_full.json is paper "j26", the June 2026 Paper 2). There is no separate list: a paper exists because its file
 * exists, exactly as a lesson exists because its seed does, so two people adding two papers never edit a shared file.
 *
 * Question numbers are read from the item (topic "... · Q9", or an id ending -q09). A variant bank item names the question it
 * was made from with srcQ and, when that is not the original paper, srcPaper. A lesson names the questions it is built on in an
 * optional  "anchors": [ { "paper": "j26", "q": 38 } ]  field. Older lessons name them only in prose ("Anchor: Q38"); that prose
 * is read as the original paper, DEFAULT_PAPER, because it predates any other.
 *
 * Standard library only; used by build_site.js, tools/content.js and the tests. */

const PAPER_FILE = /^pyq_([a-z0-9]+)_full$/;
const DEFAULT_PAPER = "j26";

/** "pyq_j26_full" -> "j26"; anything else -> null */
const paperIdOf = stem => (PAPER_FILE.exec(String(stem)) || [])[1] || null;

/** The question's number within its paper, or 0 when it cannot be read. */
const questionNumber = item => +((/Q(\d+)\s*$/.exec((item && item.topic) || "") || /-q0*(\d+)$/.exec((item && item.id) || "") || [0, 0])[1]);

/** Remove the candidate's own answers from a past paper, in place: what was marked, the response-sheet note, and the
 *  "Response sheet Qn; ..." tail some explanations carry. Returns how many items it changed. */
function scrubPaper(doc) {
  let changed = 0;
  for (const it of (doc && doc.items) || []) {
    const had = "youMarked" in it || "responseSheet" in it || (typeof it.explanation === "string" && /Response sheet Q\d+/.test(it.explanation));
    delete it.youMarked; delete it.responseSheet;
    if (typeof it.explanation === "string") it.explanation = it.explanation.replace(/\s*Response sheet Q\d+;[^]*$/, "").trim();
    if (had) changed++;
  }
  return changed;
}

module.exports = { PAPER_FILE, DEFAULT_PAPER, paperIdOf, questionNumber, scrubPaper };
