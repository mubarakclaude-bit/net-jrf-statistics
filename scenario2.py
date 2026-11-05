#!/usr/bin/env python3
# Every lesson carried one real-world scenario, on the opening intuition scene.
# The authoring standard now asks for two, so each lesson gets a second one on a
# later scene — placed where the theory has just been stated, so the drill-down
# answers "where would I ever use this" at the point the question occurs.
# No invented figures: where the real numbers are not known, the case is described
# qualitatively instead.
import json, io, sys

def P(*x): return list(x)

SC = {}

SC["lesson_t1.json"] = ("s8", dict(
  teaser="A vibration sensor on a pump sends two numbers an hour instead of 72,000.",
  title="What a condition-monitoring sensor is allowed to throw away",
  body=P(
    "A pump on a process plant carries an accelerometer sampling at 20 kHz. Sending every sample to the plant historian is out of the question — it is gigabytes a day per machine, on a network that also has to carry the control system. So the sensor computes a few features on board and sends those: typically an RMS level, a peak, a kurtosis, and a handful of band energies.",
    "The engineering question is which features to send. The statistical question is the same one, stated precisely: under the model you are using for the signal, is the feature set sufficient? If the conditional distribution of the raw waveform given the features still depends on the health parameter you are tracking, you have thrown away evidence, and no amount of cleverness downstream recovers it.",
    "Take the simplest useful model. If the vibration amplitude in a band is modelled as Gaussian with unknown variance — variance rising as a bearing degrades — then the sum of squares in that band is sufficient for the variance, and RMS is a one-to-one function of it. Sending RMS loses nothing about that parameter. Send the mean as well and you have added a number that carries nothing, because the mean is ancillary here.",
    "Change the model and the answer changes with it. If you also care about impulsiveness — the sharp repetitive hits a spalled race produces — the Gaussian model is wrong, and under a heavier-tailed model the sum of squares is no longer sufficient. That is why kurtosis is on the list: it is the extra statistic the richer model needs. Sufficiency is always relative to a model, and this is what that sentence looks like when a network budget depends on it."),
  close="The feature set is a sufficiency argument in disguise: each feature earns its bandwidth by being part of a sufficient statistic for a parameter someone is tracking."))

SC["lesson_mle.json"] = ("s9", dict(
  teaser="Why reliability software fits a Weibull by likelihood and not by least squares.",
  title="Fitting lifetimes when most units have not failed yet",
  body=P(
    "A reliability engineer has 400 units on test. Sixty have failed; the rest are still running when the test is stopped. The problem is not the sixty — it is the 340, each of which says 'longer than this', and a method that ignores them will make the product look far worse than it is.",
    "Maximum likelihood handles that in one line of bookkeeping. A failure at time t contributes its density f(t;θ); a unit still running at time t contributes its survival probability 1 − F(t;θ). The likelihood is the product of both kinds of term, and nothing else about the method changes. A least-squares fit to a probability plot has no natural way to carry the second kind of term, which is why the standard reliability packages fit by likelihood.",
    "Then invariance does the second half of the work. The quantity a warranty department actually wants is rarely a parameter: it is B10 life, the time by which 10% of units have failed, or the probability of surviving the warranty period. Each is a function of the fitted parameters, and the MLE of a function is that function of the MLE — so the answer comes straight out of the fit with no new estimation.",
    "What the method does not give you for free is a sanity check, and the checks are where the marks and the money both are. A shape parameter below 1 says the failure rate is decreasing — infant mortality, a manufacturing problem — while a shape above 1 says wear-out. Reporting a B10 life from a fit whose shape parameter contradicts the physics is the usual way this goes wrong in practice."),
  close="Censored data are the ordinary case, not the exception, and the likelihood is the estimator that takes them in its stride."))

SC["lesson_t2.json"] = ("s7", dict(
  teaser="Why a calibration lab can report a mean and a spread as two unrelated numbers.",
  title="Basu's theorem on a calibration certificate",
  body=P(
    "A calibration laboratory measures a reference mass ten times and issues a certificate with two numbers: the mean of the readings, and a spread that quantifies the repeatability of the instrument. Everyone treats those two numbers as separate pieces of information — the mean is the measurement, the spread is the uncertainty attached to it.",
    "That separation is a theorem, not a convention. For a normal sample the sample mean is a complete sufficient statistic for μ when σ is known, and the sample variance is ancillary: its distribution does not involve μ at all, since shifting every reading by the same amount leaves the deviations untouched. Basu's theorem then says the two are independent.",
    "Independence is what licenses the practice. It means the spread the lab reports is not quietly contaminated by where the mean happened to land — a high reading does not come packaged with an inflated uncertainty. If the two were dependent, the certificate would have to report a joint statement rather than two numbers, and every downstream calculation that combines uncertainties would need rewriting.",
    "It is also a genuinely normal-distribution fact, not a general one. For an exponential sample the mean and the variance of the sample move together, and no amount of wishing makes them independent. That is why the normality assumption on a calibration certificate is load-bearing rather than decorative."),
  close="Ancillary plus complete sufficient gives independence, and independence is what lets two numbers be read separately."))

SC["lesson_t3.json"] = ("s7", dict(
  teaser="An SLA promises 99.9% uptime. Someone has to estimate the probability of no crash.",
  title="Estimating a survival probability you will be held to",
  body=P(
    "A platform team runs a service under a contract that specifies availability. The quantity in the contract is a probability — the chance the service survives the next hour without an incident — and the data are the intervals between past incidents, modelled as exponential with unknown rate.",
    "The obvious estimator is the obvious one for a reason: count how many of the past hours had no incident and take the proportion. It is unbiased and it is almost useless, because it throws away the actual times and reduces a continuous record to a handful of zeros and ones. With only a few incidents on record its variance is enormous.",
    "Rao–Blackwell repairs it without changing the target. Condition the crude indicator on the total time on test, which is sufficient for the rate, and the result is a smooth function of that total — an estimator with the same expectation and a strictly smaller variance. Completeness then promotes 'smaller' to 'smallest': by Lehmann–Scheffé no unbiased estimator of that probability does better.",
    "The practical difference is visible in the number the team can defend. The crude estimator is forced into coarse steps and can return exactly zero or exactly one from a short record, which is indefensible in a contract negotiation. The conditioned version moves smoothly with the evidence, which is what a figure in a service agreement has to do."),
  close="Rao–Blackwell is not a theoretical refinement here: it is the difference between a number you can defend and one you cannot."))

SC["lesson_t5.json"] = ("s8", dict(
  teaser="Why an actuary fits claim sizes by moments first and by likelihood second.",
  title="The starting value problem, and who solves it",
  body=P(
    "An actuary models claim sizes on a motor portfolio as gamma with unknown shape and rate. The likelihood for the gamma shape has no closed-form maximum — it involves the digamma function — so the fit is numerical, and a numerical maximiser has to start somewhere.",
    "The method of moments gives the starting point in one line. Set the first two sample moments equal to their population values and solve: the shape comes out as x̄² divided by the sample variance, and the rate as x̄ divided by the sample variance. No iteration, no derivative, no software beyond a calculator.",
    "Those values are usually close enough that the likelihood maximiser converges in a few steps, and far enough from the boundary that it does not wander off into a region where the shape goes negative. Starting a gamma fit from an arbitrary value is how you get a maximiser that fails to converge, or converges to something a long way from the data.",
    "The division of labour is the point. Moment estimates are consistent, instantaneous and usually less efficient than the MLE; the MLE is efficient but needs a sensible place to begin. The textbook treats them as rival methods; practice treats them as the first and second step of one procedure."),
  close="Consistency gets you into the right neighbourhood; the likelihood finds the right house once you are there."))

SC["lesson_t6.json"] = ("s9", dict(
  teaser="Why a satellite receiver quotes a position accuracy before it has taken a reading.",
  title="Dilution of precision is a Fisher information calculation",
  body=P(
    "A satellite navigation receiver reports a position and, alongside it, a figure for how good that position can be. The figure is available before the fix is computed — it depends on which satellites are visible and where they sit in the sky, not on the measurements themselves.",
    "That is the Cramér–Rao bound doing its work. The ranging error on each satellite signal enters the likelihood through the geometry of the satellite directions, and the Fisher information for position is built from those directions. Inverting it gives the smallest variance any unbiased position estimate can have, and the square root of the relevant diagonal entry is what the receiver displays.",
    "The geometry dominates. Satellites spread widely across the sky give an information matrix that is well conditioned and a tight bound; satellites bunched together give a nearly singular one, and the bound blows up in the direction the geometry cannot resolve. This is why accuracy is poor in an urban canyon even when every signal is strong: the bound is set by where the satellites are, not by how clean the signals look.",
    "The practical consequence is the one the bound is for. A receiver can tell you in advance that no processing will achieve the accuracy you want with the satellites currently in view, so the choice is to wait for the constellation to move or to add another source. That is a planning decision made from the bound alone, before any estimator exists."),
  close="The bound is a statement about the experiment, not the estimator — which is why it can be computed before any data arrive."))

SC["lesson_t9.json"] = ("s8", dict(
  teaser="A regulator fixes the false-positive rate, and the sponsor sizes the trial around it.",
  title="Why a trial protocol names α first and n last",
  body=P(
    "A clinical trial protocol fixes the significance level before anything else. The regulator's interest is asymmetric: approving a drug that does not work is a different kind of failure from missing one that does, and the first is the one the fixed level controls.",
    "That asymmetry is exactly the Neyman–Pearson framing. The Type I error rate is a constraint, not a quantity to be traded off; subject to it, the sponsor wants the most powerful test available against the alternative that matters clinically. For the comparison the protocol specifies, the likelihood ratio gives that test, and it reduces to a critical value on a single summary statistic.",
    "Sample size is then the only remaining lever. With α fixed by the regulator and the clinically relevant effect fixed by the question being asked, power is a function of n alone, and the protocol solves for the n that reaches the power the committee requires — typically 80% or 90%. Everything in a power calculation is this one rearrangement.",
    "Where this gets misread is in what a non-significant result then means. The test was built to control false positives, not to make absence of evidence into evidence of absence, and a trial that failed to reach significance at a sample size chosen for 80% power had, by construction, a one-in-five chance of missing a real effect of that size."),
  close="Fix the error you care most about, then buy power with sample size — the whole protocol is that sentence with numbers in it."))

changed = []
for fn, (sid, sc) in SC.items():
    p = "seed/" + fn
    d = json.load(io.open(p, encoding="utf-8"))
    tgt = [s for s in d["scenes"] if s["id"] == sid]
    if not tgt:
        sys.exit("%s has no scene %s" % (fn, sid))
    s = tgt[0]
    if s.get("scenario") and s["scenario"].get("title") != sc["title"]:
        sys.exit("%s scene %s already carries a different scenario" % (fn, sid))
    s["scenario"] = sc
    n = len([x for x in d["scenes"] if x.get("scenario")])
    maj, mnr = d.get("version", "1.1").split(".")
    d["version"] = "%s.%d" % (maj, int(mnr) + 1)
    json.dump(d, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    changed.append((fn, d["topicId"], sid, s["kind"], n, d["version"]))
for c in changed:
    print("%-18s %-14s %s (%s) -> %d scenarios, v%s" % c)
