#!/usr/bin/env python3
# 10A.3 had the same Wikipedia-only problem. Each URL below was fetched and confirmed.
import io, re, json
D = "2026-10-14"
REFS = [
 dict(title="History of the Indian Statistical Institute", where="Founding date, and the 1959 Act of Parliament",
   site="Indian Statistical Institute (official)", url="https://www.isical.ac.in/~lru/history.html",
   type="Institutional page", free=True, checked=D,
   why="The Institute's own statement: founded by Mahalanobis in Kolkata on 17 December 1931, and an Institute of "
       "National Importance by an Act of Parliament in 1959. Use it in preference to any secondary summary for these "
       "two dates."),
 dict(title="C. R. Rao awarded the 2023 International Prize in Statistics",
   where="The 1945 paper, and the three results it contained",
   site="Amstat News, American Statistical Association",
   url="https://magazine.amstat.org/blog/2023/04/01/rao-awarded-2023-prize/",
   type="Professional society announcement", free=True, checked=D,
   why="The source for the claim in scene 4 that one 1945 paper in the Bulletin of the Calcutta Mathematical Society "
       "carried the Cramer-Rao bound, the Rao-Blackwell theorem and the seed of information geometry."),
 dict(title="Raj Chandra Bose", where="Biography, PBIBD with K. R. Nair, and the Euler disproof",
   site="MacTutor History of Mathematics Archive, University of St Andrews",
   url="https://mathshistory.st-andrews.ac.uk/Biographies/Bose_Raj/",
   type="Scholarly biographical archive", free=True, checked=D,
   why="A sourced biography rather than an encyclopaedia summary, including Shrikhande's own account of the Euler "
       "work and the 'Euler spoilers' episode. Note that it states the failing orders loosely; this lesson's "
       "'4k + 2, except 6' is the precise form."),
 dict(title="Sampling Theory of Surveys with Applications", where="The textbook named in the syllabus",
   site="P. V. Sukhatme", url="", type="Textbook", free=False, checked=D, isbn="978-8171641536",
   why="The book itself, rather than a description of it. Worth seeing once so that the name attaches to a real "
       "object: it is the work that carried Indian agricultural sampling into international practice."),
 dict(title="Linear Statistical Inference and Its Applications, 2nd edition",
   where="C. R. Rao's own text", site="C. R. Rao", url="", type="Textbook", free=False, checked=D,
   isbn="978-0471218753",
   why="If you want to see how the man wrote, this is the source. Chapter 5 contains his treatment of the "
       "information inequality that carries his name."),
]
src = io.open("lesson_10a3.py", encoding="utf-8").read()
lit = json.dumps(REFS, ensure_ascii=False, indent=4)
for a,b in (("true","True"),("false","False"),("null","None")): lit = re.sub(r"\b"+a+r"\b", b, lit)
body = "  refs=" + lit.replace("\n", "\n  ") + ",\n  revision=dict("
new, n = re.subn(r"\n  refs=\[.*?\n  revision=dict\(", "\n" + body, src, flags=re.S)
assert n == 1, n
io.open("lesson_10a3.py", "w", encoding="utf-8").write(new)
print("patched lesson_10a3.py")
