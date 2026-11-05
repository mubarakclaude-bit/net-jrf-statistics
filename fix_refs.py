#!/usr/bin/env python3
# Replace the reference block in the four lessons that had Wikipedia-only sources.
# Every URL below was fetched and confirmed to be the page it claims to be, on the date
# in `checked`. Textbook entries carry no URL and render as a plain citation.
import io, re, json

PSU   = "https://online.stat.psu.edu/stat415/lesson/24/24.2"
PSU1  = "https://online.stat.psu.edu/stat415/lesson/24/24.1"
MIT   = "https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/"
BERK  = "https://stat210a.berkeley.edu/fall-2024/reader/bayes-estimation.html"
UW    = "https://faculty.washington.edu/yenchic/26A_stat581/Lec1_decision.html"
NPTEL = "https://archive.nptel.ac.in/noc/courses/noc21/SEM1/noc21-ma23"
D = "2026-10-14"

def ref(title, where, site, url, type, why, free=True, isbn=None):
    r = dict(title=title, where=where, site=site, url=url, type=type, free=free, checked=D, why=why)
    if isbn: r["isbn"] = isbn
    return r

def book(title, where, site, type, why, isbn=None):
    return ref(title, where, site, "", type, why, free=False, isbn=isbn)

REFS = {
"inference-t1": [
  ref("Definition of Sufficiency, and the Factorization Theorem",
      "STAT 415, Lesson 24.1 and 24.2", "Penn State online notes", PSU,
      "University course notes",
      "The cleanest statement of both definitions at exactly this level, with the Bernoulli conditional-distribution "
      "argument worked out in 24.1 and three factorisations — Poisson, normal, exponential — in 24.2. Start here if "
      "scene 5 moved too quickly."),
  ref("Mathematical Statistics 18.655 — lecture notes",
      "Session 6 Sufficiency; Sessions 7-8 Exponential Families I and II", "MIT OpenCourseWare", MIT,
      "Graduate lecture notes (PDF)",
      "The measure-theoretic treatment, and the proof that the minimal sufficient statistic is the likelihood up to "
      "proportionality. Beyond what NET asks, but it is where the exponential-family explanation in scene 4 comes from."),
  ref("Statistical Inference", "Theory of estimation and testing, taught for an Indian audience",
      "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee", NPTEL,
      "Free video course with assignments",
      "Indian, free, and pitched at exactly this syllabus. Useful if you would rather be taught this topic than read it."),
  book("Statistical Inference, 2nd edition", "Chapter 6, Principles of Data Reduction — 6.2.1 factorisation, 6.2.2 minimal sufficiency",
      "Casella and Berger", "Textbook",
      "The standard reference for this unit. Section 6.2.2 contains the ratio criterion used in scenes 8 and 10, and "
      "Exercise 6.9 is the Uniform(theta, theta+1) case that scene 12 works through.",
      isbn="978-0534243128"),
  book("An Introduction to Probability and Statistics, 3rd edition", "Chapter 8, Sufficiency and completeness",
      "Rohatgi and Saleh", "Textbook",
      "The text most Indian MSc courses set, so its notation is the one NET questions tend to follow. Worth comparing "
      "with Casella and Berger where the two differ on how minimal sufficiency is introduced.",
      isbn="978-0471348467")],

"inference-t7": [
  ref("Bayes estimation", "Bayes risk, Bayes estimators, loss functions and conjugate priors",
      "Berkeley STAT 210A course reader", BERK,
      "Graduate course reader",
      "Derives the posterior mean as the squared-error Bayes estimator and works the beta-binomial and normal-normal "
      "cases in the same order this lesson does, with the exponential-family account of why conjugacy happens."),
  ref("Mathematical Statistics 18.655 — lecture notes",
      "Session 3 Bayesian Models; Session 11 Bayes Procedures", "MIT OpenCourseWare", MIT,
      "Graduate lecture notes (PDF)",
      "Session 11 is the one to read for how a Bayes procedure relates to admissibility and minimaxity, which is the "
      "bridge from this topic into 4.8."),
  ref("Statistical Inference", "Estimation, including Bayesian estimation",
      "NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee", NPTEL,
      "Free video course with assignments",
      "Indian and free, at this syllabus's level and notation."),
  book("Statistical Inference, 2nd edition",
      "Section 7.2.3 Bayes estimators; Section 7.3.4 loss function optimality", "Casella and Berger", "Textbook",
      "Section 7.2.3 gives the conjugate updates in the form this lesson states them; 7.3.4 is where the three losses "
      "are matched to mean, median and mode.",
      isbn="978-0534243128"),
  book("Theory of Point Estimation, 2nd edition", "Chapter 4, Average risk optimality",
      "Lehmann and Casella", "Textbook",
      "The definitive treatment of Bayes estimators, including the conditions under which the posterior mean is "
      "admissible. Harder than NET requires; the right place to settle a doubt the lesson leaves open.",
      isbn="978-0387985022")],

"inference-t8": [
  ref("Elementary Decision Theory",
      "Loss, risk, Bayes risk, admissibility, minimax and least favourable priors",
      "University of Washington STAT 581, Yen-Chi Chen", UW,
      "Graduate lecture notes",
      "Covers every definition in this lesson in the same order, including the least favourable prior, which most "
      "undergraduate texts leave out. The closest free match to scenes 4 and 10."),
  ref("Mathematical Statistics 18.655 — lecture notes",
      "Session 4, The Decision Theoretic Framework", "MIT OpenCourseWare", MIT,
      "Graduate lecture notes (PDF)",
      "Sets up the decision problem formally and proves the relation this lesson leans on: a Bayes rule with constant "
      "risk is minimax."),
  book("Theory of Point Estimation, 2nd edition",
      "Chapter 1 (decision theory) and Chapter 5 (minimax estimation)", "Lehmann and Casella", "Textbook",
      "The standard source for admissibility and minimaxity. Chapter 5 derives the binomial minimax estimator "
      "(x + sqrt(n)/2)/(n + sqrt(n)) that scene 5 builds from scratch, and proves it is minimax.",
      isbn="978-0387985022"),
  book("Statistical Inference, 2nd edition", "Section 7.3.4, Loss function optimality",
      "Casella and Berger", "Textbook",
      "The gentler account, at the level NET asks. Read this first if the Lehmann and Casella treatment is heavier "
      "than you need.",
      isbn="978-0534243128"),
  book("Testing Statistical Hypotheses, 3rd edition", "Chapter 1, The general decision problem",
      "Lehmann and Romano", "Textbook",
      "Where the translation of testing into decision-theoretic language in scene 9 comes from, and why "
      "Neyman-Pearson constrains one error rather than minimising the maximum.",
      isbn="978-0387988641")],
}

# --- patch the authoring scripts so a regeneration keeps these
FILES = {"inference-t1":"lesson_t1.py","inference-t7":"lesson_t7.py","inference-t8":"lesson_t8.py"}
for tid, fn in FILES.items():
    src = io.open(fn, encoding="utf-8").read()
    # emit Python literals, not JSON: true/false/null are not Python names
    lit = json.dumps(REFS[tid], ensure_ascii=False, indent=4)
    lit = re.sub(r"\btrue\b", "True", lit)
    lit = re.sub(r"\bfalse\b", "False", lit)
    lit = re.sub(r"\bnull\b", "None", lit)
    body = "  refs=" + lit.replace("\n", "\n  ") + ",\n  revision=dict("
    new, n = re.subn(r"\n  refs=\[.*?\n  revision=dict\(", "\n" + body, src, flags=re.S)
    assert n == 1, (fn, n)
    io.open(fn, "w", encoding="utf-8").write(new)
    print("patched " + fn)
