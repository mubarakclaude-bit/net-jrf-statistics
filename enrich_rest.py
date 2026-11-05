# Gives t2, t3, t4, t5 and t6 the three things only Sufficiency had: a decision
# flow chart, a real-world case the learner can drill into, and memory aids.
import json, os
SEED = "/home/claude/w1/seed"

# ---------------------------------------------------------------- t2
T2_FLOW = {
 "title":"Is this statistic complete? And may I use Basu?",
 "alt":"Decision chart for completeness and Basu's theorem",
 "nodes":[
  {"id":"a","r":0,"c":1,"label":"You have a sufficient statistic T","kind":"start"},
  {"id":"b","r":1,"c":1,"label":"Can the density be written in exponential-family form?","kind":"decision"},
  {"id":"c","r":2,"c":0,"label":"Check E[g(T)] = 0 ⇒ g ≡ 0 by hand","kind":"step"},
  {"id":"d","r":2,"c":2,"label":"Is it FULL RANK: k natural parameters, k free parameters?","kind":"decision"},
  {"id":"e","r":3,"c":2,"label":"T is complete","kind":"step"},
  {"id":"f","r":3,"c":0,"label":"Curved family — sufficient but NOT complete","kind":"note"},
  {"id":"g","r":4,"c":1,"label":"T complete AND sufficient","kind":"step"},
  {"id":"h","r":5,"c":1,"label":"Is the other statistic's distribution free of θ?","kind":"decision"},
  {"id":"i","r":6,"c":1,"label":"Basu: the two are independent","kind":"end"}],
 "edges":[
  {"from":"a","to":"b"},{"from":"b","to":"c","label":"no"},{"from":"b","to":"d","label":"yes"},
  {"from":"d","to":"e","label":"yes"},{"from":"d","to":"f","label":"no"},
  {"from":"c","to":"g"},{"from":"e","to":"g"},
  {"from":"g","to":"h"},{"from":"h","to":"i","label":"yes, it is ancillary"}],
 "note":"Full rank is the condition people skip. N(θ, θ²) has a two-dimensional natural statistic for one free parameter — curved, so sufficient but not complete, and Basu does not apply."
}
T2_SCEN = {
 "teaser":"Why a factory runs two control charts, and why they can be read independently.",
 "title":"The X̄ chart and the R chart, and why Basu lets you trust both",
 "body":[
  "A plant machining bearing races measures an internal diameter on five parts every hour. Two charts go up on the wall: an X̄ chart tracking the mean of each sample, and an R chart tracking the range within it. The operator is told to read them separately — a signal on one does not contaminate the other.",
  "That instruction is Basu's theorem wearing overalls. Treat the process as normal with known spread σ while the mean μ drifts. Then X̄ is a complete sufficient statistic for μ. The range R = X₍₅₎ − X₍₁₎ is unchanged if you shift every measurement by a constant, so its distribution does not involve μ at all — R is ancillary.",
  "Complete and sufficient on one side, ancillary on the other: Basu gives independence immediately, with no distribution theory at all. The two charts carry non-overlapping information, which is exactly why a shift in the mean does not inflate the range chart and a widening spread does not drag the mean chart off centre.",
  "The practical payoff is diagnostic. A signal on X̄ alone points at a setting that has moved — tool offset, thermal growth, a changed fixture. A signal on R alone points at variability — a loose spindle, inconsistent material. If the two were dependent you could not read them apart, and every alarm would be ambiguous."],
 "q":"The quality engineer now says σ is also unknown and must be estimated from the same data. Does the independence argument survive?",
 "answer":"The conclusion survives, but this argument does not. With σ unknown, R is no longer ancillary — its distribution depends on σ, which is now a parameter — so Basu cannot be applied in that form. Independence of X̄ and S² for the normal is still true, but it needs the direct distributional proof rather than Basu. This is the trap the exam sets: Basu's hypotheses have to be checked against the parameters actually unknown, not the ones you wish were known.",
 "link":"The same structure underlies residual analysis in regression: residuals are ancillary for the regression coefficients, which is why they are free to be used for checking the model that produced them."
}
T2_AIDS = {
 "tricks":[
  {"hook":"Complete = only zero has zero mean","why":"E_θ[g(T)] = 0 for every θ forces g ≡ 0. Nothing non-trivial averages to zero at every θ."},
  {"hook":"Curved means fat","why":"More natural statistics than free parameters → sufficient but NOT complete. N(θ, θ²) is the stock example."},
  {"hook":"Basu needs all three","why":"Complete AND sufficient on one side, ancillary on the other. Drop any one and the theorem is gone."},
  {"hook":"Ancillary = blind to θ","why":"Its distribution does not involve θ, so on its own it says nothing about θ — which frees it to check the model."}],
 "shortcuts":[
  "Full-rank k-parameter exponential family ⇒ the natural statistic is complete. That is the quickest route there is.",
  "U(θ, θ+1): minimal sufficient (X₍₁₎, X₍ₙ₎), NOT complete — the range is ancillary and spoils it.",
  "Location families: any difference of observations is ancillary. Scale families: any ratio is.",
  "Completeness is a property of the FAMILY, never of one distribution."],
 "remember":[
  "Sufficiency reduces the data; completeness makes the reduction unique. They answer different questions.",
  "Check which parameters are actually unknown before quoting Basu — ancillarity is relative to those."]
}

# ---------------------------------------------------------------- t3
T3_FLOW = {
 "title":"Getting to a UMVUE — the two routes",
 "alt":"Decision chart for Rao–Blackwell and Lehmann–Scheffé",
 "nodes":[
  {"id":"a","r":0,"c":1,"label":"You want the UMVUE of g(θ)","kind":"start"},
  {"id":"b","r":1,"c":1,"label":"Find a complete sufficient statistic T","kind":"step"},
  {"id":"c","r":2,"c":1,"label":"Can you spot an unbiased function of T directly?","kind":"decision"},
  {"id":"d","r":3,"c":0,"label":"Take ANY unbiased δ, then compute E[δ | T]","kind":"step"},
  {"id":"e","r":3,"c":2,"label":"Use it — or correct the bias of a convenient function of T","kind":"step"},
  {"id":"f","r":4,"c":1,"label":"Is the result unbiased and a function of T alone?","kind":"decision"},
  {"id":"g","r":5,"c":1,"label":"Lehmann–Scheffé: it is THE UMVUE","kind":"end"},
  {"id":"h","r":6,"c":1,"label":"Its variance may still sit above the Cramér–Rao floor","kind":"note"}],
 "edges":[
  {"from":"a","to":"b"},{"from":"b","to":"c"},
  {"from":"c","to":"d","label":"no"},{"from":"c","to":"e","label":"yes"},
  {"from":"d","to":"f"},{"from":"e","to":"f"},
  {"from":"f","to":"g","label":"yes"},{"from":"g","to":"h"}],
 "note":"Rao–Blackwell improves any unbiased estimator; completeness is what upgrades 'improved' to 'best'. Without completeness you stop at the improvement."
}
T3_SCEN = {
 "teaser":"An insurer needs P(a policy files no claim). The obvious estimator is almost useless.",
 "title":"From a single yes/no to the best estimator there is",
 "body":[
  "A motor insurer models the number of claims a policy files in a year as Poisson(λ) and needs to estimate the probability a policy stays claim-free, g(λ) = e^(−λ). It drives the renewal discount, so the estimate has to be defensible.",
  "Start with something crude but honest. Look at the FIRST policy only and write δ = 1 if it filed no claims and 0 otherwise. Its expectation is P(X₁ = 0) = e^(−λ), so it is unbiased — and it is also close to worthless, because it throws away every other policy and takes only the values 0 and 1.",
  "Now Rao–Blackwellise. T = ΣXᵢ is complete sufficient for λ, and conditioning the crude estimator on T gives E[δ | T = t] = ((n−1)/n)^t. The derivation is a binomial-thinning argument, but the conclusion is what matters: one conditioning step turns a coin-flip of an estimator into a smooth function of the entire portfolio.",
  "Because T is complete and the result is unbiased, Lehmann–Scheffé certifies it as THE uniformly minimum variance unbiased estimator. No better unbiased estimator exists — not merely none has been found.",
  "The practical lesson transfers to any portfolio problem: the quantity you can easily write down unbiasedly is rarely the one you should report, and conditioning on the sufficient statistic is the mechanical way to improve it without having to be clever."],
 "q":"The actuary points out that the maximum likelihood estimate is simply e^(−x̄), which is easier to compute. Why not use that?",
 "answer":"Because it is biased. By Jensen's inequality E[e^(−X̄)] > e^(−λ), so the MLE systematically overstates the claim-free probability — which in this application means systematically over-discounting renewals. ((n−1)/n)^T is unbiased at every portfolio size. The two agree as n grows, so for a large book the difference is immaterial; for a small segment it is not, and that is exactly where the discount decision is riskiest.",
 "link":"The same machinery produces the UMVUE of a reliability function R(t) = e^(−λt) in engineering — the quantity a maintenance interval is built on."
}
T3_AIDS = {
 "tricks":[
  {"hook":"RB improves, LS certifies","why":"Rao–Blackwell lowers the variance; completeness is what turns 'better' into 'best'."},
  {"hook":"Condition on T, never on θ","why":"E[δ | T] is computable precisely because T is sufficient. Conditioning on θ would not be a statistic."},
  {"hook":"Already a function of T? You are done","why":"E[δ | T] = δ and there is no improvement left — that is the equality case, and the signal to stop."},
  {"hook":"Best unbiased ≠ efficient","why":"A UMVUE can sit strictly above the Cramér–Rao floor. The exponential rate is the standard case."}],
 "shortcuts":[
  "Guess an unbiased function of T and correct it — completeness means whatever you find IS the UMVUE.",
  "Poisson: UMVUE of λ² is T(T−1)/n²; of e^(−λ) is ((n−1)/n)^T.",
  "Bernoulli: UMVUE of p² is T(T−1)/(n(n−1)).",
  "U(0,θ): UMVUE of θ is (n+1)X₍ₙ₎/n, variance θ²/(n(n+2)) — an n⁻² rate."],
 "remember":[
  "Rao–Blackwell needs sufficiency only. Uniqueness needs completeness as well.",
  "The improvement is strict unless the estimator was already a function of T."]
}

# ---------------------------------------------------------------- t4 (MLE)
T4_FLOW = {
 "title":"Finding an MLE — and knowing when not to differentiate",
 "alt":"Decision chart for maximum likelihood estimation",
 "nodes":[
  {"id":"a","r":0,"c":1,"label":"Write the likelihood L(θ) for the observed sample","kind":"start"},
  {"id":"b","r":1,"c":1,"label":"Does the SUPPORT depend on θ?","kind":"decision"},
  {"id":"c","r":2,"c":0,"label":"Do not differentiate — inspect where L is positive","kind":"note"},
  {"id":"d","r":2,"c":2,"label":"Take logs, then solve ∂ℓ/∂θ = 0","kind":"step"},
  {"id":"e","r":3,"c":0,"label":"Maximum sits at a boundary, e.g. θ̂ = x₍ₙ₎","kind":"step"},
  {"id":"f","r":3,"c":2,"label":"Check ∂²ℓ/∂θ² < 0 at the solution","kind":"decision"},
  {"id":"g","r":4,"c":1,"label":"θ̂ is the MLE","kind":"step"},
  {"id":"h","r":5,"c":1,"label":"Asked for g(θ)? By invariance the answer is g(θ̂)","kind":"end"}],
 "edges":[
  {"from":"a","to":"b"},{"from":"b","to":"c","label":"yes"},{"from":"b","to":"d","label":"no"},
  {"from":"c","to":"e"},{"from":"d","to":"f"},
  {"from":"e","to":"g"},{"from":"f","to":"g","label":"yes"},{"from":"g","to":"h"}],
 "note":"The left branch is where marks are lost. For U(0,θ) the derivative of the log-likelihood is never zero, so setting it to zero finds nothing at all — the maximum is at the edge of the support."
}
T4_SCEN = {
 "teaser":"In 1943 the Allies estimated German tank production from the serial numbers on captured gearboxes.",
 "title":"The German tank problem",
 "body":[
  "Allied intelligence needed to know how many Panther tanks Germany was building. Conventional estimates, assembled from agent reports and aerial reconnaissance, put output at around 1,400 a month in mid-1943.",
  "Statisticians took a different route. Captured and destroyed tanks carried sequentially numbered components — gearboxes, wheels, engines. If serial numbers run 1 to N and the captured ones are effectively a random sample without replacement, then N is the upper endpoint of a discrete uniform distribution and the serial numbers are the data.",
  "The maximum likelihood estimate is immediate, and it is exactly the case where differentiating gets you nowhere: the likelihood is zero for any N below the largest serial observed, and decreasing above it, so N̂ = the largest serial number seen. It is also obviously biased — it can never exceed the truth, and almost always falls short.",
  "The correction is the same bias correction as for U(0,θ). With k observations and maximum m, the minimum-variance unbiased estimate is m(1 + 1/k) − 1: push the maximum up by roughly one average gap. For a sample of 10 with a largest serial of 1,200 that gives 1,200(1.1) − 1 = 1,319.",
  "Post-war records settled it. The statistical estimates were close to the true production figures, while the intelligence estimates were out by a factor of several. The whole argument is two topics of this syllabus — a boundary MLE from this lesson, and its bias correction from Rao–Blackwell and Lehmann–Scheffé."],
 "q":"Why is the estimate so much better than the intelligence figure, given that it uses far less information?",
 "answer":"Because it uses the right information. The sample maximum is sufficient for N: once you know the largest serial number, the others add nothing about N, so a handful of captured tanks carries nearly all the information a much larger sample would. Agent reports, by contrast, carry an unknown and probably non-zero bias that more reports do not remove. A small sample read through the correct model beats a large body of evidence read through the wrong one.",
  "link":"The identical estimator is used today to size populations from sequential identifiers — for instance estimating total units produced from the serial numbers on a sample of returned warranty claims."
}
T4_AIDS = {
 "tricks":[
  {"hook":"Log, differentiate, check","why":"Three steps in order. The third — the second-derivative check — is the one most often skipped and most often worth a mark."},
  {"hook":"Invariance: substitute, don't re-derive","why":"MLE of g(θ) is g(θ̂). True for ANY g, one-to-one or not."},
  {"hook":"Support moves → look, don't differentiate","why":"U(0,θ): ℓ′ is never zero. The maximum is at the boundary x₍ₙ₎."},
  {"hook":"MLE is not unbiased","why":"σ̂² divides by n, not n−1. Efficiency is asymptotic; bias at finite n is normal."}],
 "shortcuts":[
  "Bernoulli / Poisson / exponential mean: the MLE is just x̄.",
  "Exponential RATE: λ̂ = n/ΣX, biased upward with E[λ̂] = nλ/(n−1).",
  "N(μ,σ²) both unknown: μ̂ = x̄ and σ̂² = Σ(xᵢ−x̄)²/n — divisor n.",
  "U(0,θ): θ̂ = x₍ₙ₎. U(θ−1/2, θ+1/2): any value in [x₍ₙ₎−1/2, x₍₁₎+1/2] — the MLE is not unique."],
 "remember":[
  "An MLE need not be unique, unbiased, or even exist in a closed form.",
  "Under regularity it IS consistent, asymptotically normal and asymptotically efficient — all three are large-sample claims."]
}

# ---------------------------------------------------------------- t5
T5_FLOW = {
 "title":"The method of moments, with the check that most answers omit",
 "alt":"Decision chart for method of moments estimation",
 "nodes":[
  {"id":"a","r":0,"c":1,"label":"Count the unknown parameters: k","kind":"start"},
  {"id":"b","r":1,"c":1,"label":"Do the first k population moments exist?","kind":"decision"},
  {"id":"c","r":2,"c":0,"label":"No moments, no method — e.g. the Cauchy","kind":"note"},
  {"id":"d","r":2,"c":2,"label":"Write E[X], and Var(X) if k = 2, in the parameters","kind":"step"},
  {"id":"e","r":3,"c":2,"label":"Set equal to x̄ and m₂; divide one by the other to eliminate","kind":"step"},
  {"id":"f","r":4,"c":2,"label":"Does the solution lie INSIDE the parameter space?","kind":"decision"},
  {"id":"g","r":5,"c":1,"label":"Report the moment estimate","kind":"end"},
  {"id":"h","r":5,"c":3,"label":"Inadmissible — say so and give the MLE instead","kind":"note"}],
 "edges":[
  {"from":"a","to":"b"},{"from":"b","to":"c","label":"no"},{"from":"b","to":"d","label":"yes"},
  {"from":"d","to":"e"},{"from":"e","to":"f"},
  {"from":"f","to":"g","label":"yes"},{"from":"f","to":"h","label":"no"}],
 "note":"The last diamond is the one that is skipped. For U(0,θ) the estimate 2x̄ can land below the largest observation, where the likelihood is exactly zero — and that is the examinable point, not a mistake to hide."
}
T5_SCEN = {
 "teaser":"Every flood defence in the country is sized by a method-of-moments fit.",
 "title":"Sizing a spillway from 40 years of annual peak flows",
 "body":[
  "A dam spillway has to pass the 100-year flood. The hydrologist has one number per year — the annual peak discharge — and perhaps forty of them. From that, a design flow with an exceedance probability of 0.01 must be produced, and defended at a public inquiry.",
  "The standard practice is to fit a two-parameter distribution to the annual maxima, commonly a gamma or a Gumbel, and read the quantile off the fitted curve. The fitting is done by the method of moments: set the mean of the distribution equal to the sample mean, the variance equal to the sample variance, and solve.",
  "Why not maximum likelihood, which is more efficient? Three reasons, all of them the ones this lesson gives. The moment estimates are closed-form, so they can be computed and audited on a spreadsheet by a reviewer who is not a statistician. They require no iteration that might fail to converge on a short record. And national design guidance has to be reproducible — two engineers with the same data must get the same answer, which an iterative optimiser does not guarantee.",
  "The cost is efficiency. With forty observations the moment estimate of the shape parameter is noticeably noisier than the MLE, and the 100-year quantile inherits that noise. Practitioners handle this by reporting confidence bands around the design flow rather than pretending the point estimate is exact.",
  "There is also a trap this lesson has already shown you. If the sample variance is large relative to the squared mean, the gamma shape estimate α̃ = x̄²/m₂ comes out below 1 — a legal value, but one implying an infinite density at zero flow. If it comes out negative, which a short skewed record can produce for other distributions, the estimate is outside the parameter space and must be reported as such rather than quietly truncated."],
 "q":"A record gives x̄ = 400 m³/s and m₂ = 160,000. What are the gamma moment estimates, and what do they say?",
 "answer":"β̃ = m₂/x̄ = 160000/400 = 400 and α̃ = x̄²/m₂ = 160000/160000 = 1. A shape of exactly 1 is the exponential distribution, so the record is consistent with exponentially distributed annual peaks of mean 400 — which is the classic signature of a variance equal to the squared mean. That is a meaningful finding rather than a failure: it tells the hydrologist the data carry no evidence of the extra shape flexibility the gamma offers, and that the simpler one-parameter model would do.",
 "link":"The same moment fit is used for wind-speed distributions in turbine siting and for particle-size distributions in process engineering — anywhere a closed-form, auditable fit matters more than the last few percent of efficiency."
}
T5_AIDS = {
 "tricks":[
  {"hook":"k unknowns, k moments","why":"Count the parameters first. Starting with one equation for a two-parameter family is the commonest way to waste time."},
  {"hook":"Divide to kill a parameter","why":"Var ÷ mean cancels the shape in the gamma and leaves the scale alone. Look for it whenever a parameter multiplies both."},
  {"hook":"Divisor n, not n−1","why":"The moment estimator of σ² is Σ(xᵢ−x̄)²/n. The n−1 version is a separate, bias-corrected estimator."},
  {"hook":"No mean, no method","why":"The Cauchy has no finite first moment, so there is nothing to equate x̄ to. The method fails, and that failure IS the answer."}],
 "shortcuts":[
  "Gamma(α,β): β̃ = m₂/x̄ and α̃ = x̄²/m₂.",
  "U(a,b): ã = x̄ − √(3m₂), b̃ = x̄ + √(3m₂). U(0,θ): θ̃ = 2x̄. U(−θ,θ): θ̃ = √(3m₂).",
  "When the first moment carries no parameter — as for U(−θ,θ) — skip it and match the variance.",
  "Least squares is the method of moments applied to E[ε] = 0 and E[Xε] = 0."],
 "remember":[
  "Guaranteed: consistency and asymptotic normality. NOT guaranteed: unbiasedness, efficiency, uniqueness, or a legal estimate.",
  "Always check the answer against the parameter space — and against the sample maximum for a uniform."]
}

# ---------------------------------------------------------------- t6
T6_FLOW = {
 "title":"Is this estimator efficient? The order that avoids wasted work",
 "alt":"Decision chart for the Cramér–Rao bound",
 "nodes":[
  {"id":"a","r":0,"c":1,"label":"An unbiased estimator T of g(θ)","kind":"start"},
  {"id":"b","r":1,"c":1,"label":"Does the support depend on θ?","kind":"decision"},
  {"id":"c","r":2,"c":0,"label":"Regularity fails — there is NO bound to quote","kind":"note"},
  {"id":"d","r":2,"c":2,"label":"Compute I(θ) = −E[∂²ℓ/∂θ²], then scale: Iₙ = n I₁","kind":"step"},
  {"id":"e","r":3,"c":2,"label":"Is the target θ itself?","kind":"decision"},
  {"id":"f","r":4,"c":1,"label":"Bound = 1/(n I(θ))","kind":"step"},
  {"id":"g","r":4,"c":3,"label":"Bound = [g′(θ)]²/(n I(θ))","kind":"step"},
  {"id":"h","r":5,"c":2,"label":"Compare with Var(T): efficiency = bound ÷ Var(T)","kind":"end"}],
 "edges":[
  {"from":"a","to":"b"},{"from":"b","to":"c","label":"yes"},{"from":"b","to":"d","label":"no"},
  {"from":"d","to":"e"},{"from":"e","to":"f","label":"yes"},{"from":"e","to":"g","label":"no"},
  {"from":"f","to":"h"},{"from":"g","to":"h"}],
 "note":"Check regularity FIRST. Computing an information number for U(0,θ) and then quoting a bound produces a contradiction, and the contradiction is evidence the conditions were violated — not a discovery."
}
T6_SCEN = {
 "teaser":"How many measurements does a sensor need? The Cramér–Rao bound answers before anything is built.",
 "title":"Specifying a sensor before it exists",
 "body":[
  "An engineering team is specifying a vibration monitor for rotating equipment. The requirement is to estimate a shaft's rotational frequency to within a stated tolerance. The questions on the table are how long to sample, at what rate, and whether a cheaper sensor with more noise can be rescued by simply taking more samples.",
  "None of these can be answered by trying estimation algorithms, because the answer must not depend on which algorithm is eventually written. What is needed is a floor: the best precision ANY unbiased estimator could achieve from data of that quality. That floor is 1/(n I(θ)), and computing it needs only the measurement model — no data and no code.",
  "This is routine practice in signal processing. The Cramér–Rao bound on a time-of-arrival estimate sets the theoretical ranging accuracy of a radar or a satellite navigation signal, and it is computed at the system-design stage to decide bandwidth and power. If the bound says the required accuracy is unreachable with the proposed signal, no amount of clever processing will rescue it, and the specification has to change.",
  "Two consequences shape the engineering. First, information adds: Iₙ = n I₁, so the floor on the variance falls like 1/n and the standard error like 1/√n. Halving the error costs four times the samples — which is why 'just sample more' runs into diminishing returns, and why a quieter sensor usually beats a longer record.",
  "Second, a design can be judged before it is built. If a candidate algorithm's variance sits close to the bound it is efficient and there is nothing left to gain from better processing; if it sits far above, the money is better spent on the algorithm than on the hardware. Efficiency, computed as bound ÷ achieved variance, is the number that decides where the next pound goes."],
 "q":"The team doubles the sampling rate, doubling n. By what factor does the achievable standard error improve, and what would the same money buy if spent on halving the sensor noise instead?",
 "answer":"Doubling n halves the variance floor, so the standard error falls by a factor of √2 — about 29%. Halving the noise standard deviation, in a Gaussian measurement model where I(θ) ∝ 1/σ², quadruples the information and halves the standard error — a 50% improvement. Noise reduction beats sampling because information enters linearly in n but as 1/σ² in the noise. That comparison is exactly what the bound is for: it is a design calculation, not a data analysis.",
 "link":"The same reasoning sets the sample-size calculation in a clinical trial: the information per subject fixes how many subjects are needed for a given precision, before a single patient is enrolled."
}
T6_AIDS = {
 "tricks":[
  {"hook":"Information is curvature","why":"I(θ) measures how sharply the log-likelihood peaks. Sharp peak → much information → low floor."},
  {"hook":"Square the derivative","why":"For g(θ) the numerator is [g′(θ)]². Dropping the square is the single commonest error in the topic."},
  {"hook":"Expected, not observed","why":"The bound uses −E[∂²ℓ/∂θ²], an average over samples. −∂²ℓ/∂θ² at θ̂ is the observed information — a different number."},
  {"hook":"Score linear in T ⇔ bound attained","why":"∂ℓ/∂θ = A(θ)[T − g(θ)] is exactly when equality holds. If it refuses to factorise, no unbiased estimator reaches the floor."}],
 "shortcuts":[
  "Bernoulli I(p) = 1/(p(1−p)); Poisson I(λ) = 1/λ; Normal mean I(μ) = 1/σ²; exponential rate I(λ) = 1/λ².",
  "The bound and the total information are reciprocals — if your two numbers do not multiply to 1, one is wrong.",
  "Efficiency = bound ÷ Var(T), so it can never exceed 1. Above 1 means the ratio is upside down.",
  "Biased estimator? The numerator becomes (1 + b′(θ))²."],
 "remember":[
  "The bound applies to UNBIASED estimators in REGULAR families. Both words matter.",
  "A UMVUE need not attain it — best unbiased and efficient are different achievements."]
}

PLAN = [
 ("lesson_t2.json","s7","s1",T2_FLOW,T2_SCEN,T2_AIDS),
 ("lesson_t3.json","s3","s1",T3_FLOW,T3_SCEN,T3_AIDS),
 ("lesson_mle.json",None,None,T4_FLOW,T4_SCEN,T4_AIDS),
 ("lesson_t5.json","s3","s1",T5_FLOW,T5_SCEN,T5_AIDS),
 ("lesson_t6.json","s3","s1",T6_FLOW,T6_SCEN,T6_AIDS),
]
for fn, flowAt, scenAt, flow, scen, aids in PLAN:
    p=os.path.join(SEED,fn)
    L=json.load(open(p,encoding="utf-8"))
    byid={x["id"]:x for x in L["scenes"]}
    # put the flow on the first theory scene, the scenario on the first intuition scene
    fa=flowAt if flowAt and flowAt in byid and byid[flowAt]["kind"]=="theory" else \
       next(x["id"] for x in L["scenes"] if x["kind"]=="theory")
    sa=scenAt if scenAt and scenAt in byid and byid[scenAt]["kind"]=="intuition" else \
       next(x["id"] for x in L["scenes"] if x["kind"]=="intuition")
    byid[fa]["flow"]=flow
    byid[sa]["scenario"]=scen
    L["revision"]["tricks"]=aids["tricks"]
    L["revision"]["shortcuts"]=aids["shortcuts"]
    L["revision"]["remember"]=aids["remember"]
    json.dump(L,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("%-16s flow on %-3s (%d nodes)  scenario on %-3s  aids %d/%d/%d"%(
      fn[:-5],fa,len(flow["nodes"]),sa,len(aids["tricks"]),len(aids["shortcuts"]),len(aids["remember"])))
