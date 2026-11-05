#!/usr/bin/env python3
"""Seed documents for the NET study app — written to local JSON, uploaded with ArtifactData."""
import json, os

OUT = '/home/claude/w1/seed'
os.makedirs(OUT, exist_ok=True)

# marks counted from the June 2026 paper; score is her result in that paper
P2 = [
 ("inference","Statistical inference",34,"2/17",[
   ("Sufficiency, factorisation, minimal sufficiency","Derive"),
   ("Completeness, exponential families, ancillarity, Basu","Derive"),
   ("Rao–Blackwell and Lehmann–Scheffé","Derive"),
   ("MLE: computation, invariance, properties","Derive"),
   ("Method of moments, minimum chi-square, least squares","Apply"),
   ("Cramér–Rao bound and Fisher information","Apply"),
   ("Bayesian estimation and conjugate priors","Apply"),
   ("Decision theory: loss, risk, admissibility, minimax","State"),
   ("Neyman–Pearson, MLR, UMP, when UMP fails","State"),
   ("Likelihood ratio test and Wilks","State"),
   ("SPRT","State"),
   ("Size and power computation","Derive"),
   ("Confidence intervals and pivots","Derive"),
   ("Chi-square goodness of fit","Derive"),
   ("Choosing the right test","Recall")]),
 ("probability","Probability and distributions",22,"3/11",[
   ("Order statistics","Derive"),("Conditional distributions","Derive"),
   ("Conditional expectation, total variance, mixtures","Derive"),
   ("MGFs, cumulants, central moments","Derive"),
   ("Standard discrete distributions","Recall"),("Standard continuous distributions","Apply"),
   ("Jensen, Markov, Chebyshev, Cauchy–Schwarz","State"),
   ("Independence and inclusion–exclusion","Apply"),
   ("Convergence, WLLN, SLLN, CLT","State"),
   ("Transformations and Jacobians","Derive"),("Characteristic functions","State")]),
 ("regression","Regression and linear models",22,"3/11",[
   ("Hat matrix, residual maker, quadratic forms","Derive"),
   ("Gauss–Markov, BLUE, estimability","Derive"),
   ("ANOVA decomposition and the F test from R²","Derive"),
   ("R², adjusted R², model comparison","Apply"),
   ("Multicollinearity","State"),("Autocorrelation and Durbin–Watson","Apply"),
   ("Heteroscedasticity and GLS","State"),("Endogeneity and instrumental variables","State"),
   ("Identification in simultaneous equations","Apply"),("Two-stage least squares","State")]),
 ("stochastic","Stochastic processes",20,"2/10",[
   ("Markov chains: n-step, Chapman–Kolmogorov","Derive"),
   ("Stationary distribution","Derive"),
   ("First passage and first return, mean passage time","Derive"),
   ("Classification of states","State"),("Poisson process","Derive"),
   ("Gambler's ruin and random walks","Apply"),
   ("Birth–death and M/M/1","Apply"),("Branching processes","State"),("Renewal processes","State")]),
 ("timeseries","Time series",20,"6/10",[
   ("Stationarity and invertibility","Derive"),("ACF and PACF identification","Recall"),
   ("Yule–Walker equations","Derive"),("Autocovariance of AR processes","Derive"),
   ("Unit roots, differencing, ARIMA","Derive"),("Random walk with and without drift","Apply"),
   ("Spectral density and the periodogram","Apply"),
   ("Components, moving averages, exponential smoothing","Apply")]),
 ("maths","Mathematics",18,"2/9",[
   ("Rank, nullity, Sylvester and Frobenius","Derive"),
   ("Eigenvalues, eigenvectors, Cayley–Hamilton","Derive"),
   ("Quadratic forms and positive definiteness","Apply"),
   ("Sequences, series, power series","Apply"),
   ("Continuity, differentiability, Rolle, MVT","State"),
   ("Maxima, minima, local extrema","Derive"),
   ("Riemann and improper integrals","Apply"),("Generalised inverse","State")]),
 ("multivariate","Multivariate analysis",18,"4/9",[
   ("Multivariate normal: marginals and conditionals","Derive"),
   ("Partial and multiple correlation","Derive"),
   ("Principal component analysis","Derive"),("Hotelling's T²","Derive"),
   ("Wishart distribution","State"),("Canonical correlation","Apply"),
   ("MLE of mean vector and covariance","Apply"),
   ("Mahalanobis distance, discriminant analysis, MANOVA","State"),
   ("Factor and cluster analysis","Recall")]),
 ("rprog","R programming",12,"4/6",[
   ("sort, rank, order, which, range","Apply"),
   ("Loops, functions, return values","Apply"),("Scoping rules","State"),
   ("Matrices and matrix operators","Apply"),
   ("Statement ordering questions","Apply"),("Summary functions and NA handling","Recall")]),
 ("sampling","Sampling theory",10,"2/5",[
   ("Horvitz–Thompson and varying probability sampling","Derive"),
   ("Stratified sampling and allocation","Derive"),
   ("Ratio and regression estimators","Apply"),("Cluster sampling","State"),
   ("Systematic sampling","State"),("PPS schemes and their estimators","Recall"),
   ("Two-stage, multi-stage and double sampling","State"),("Non-sampling errors","Recall")]),
 ("design","Design of experiments",10,"2/5",[
   ("ANOVA tables and degrees of freedom","Derive"),
   ("CRD, RBD, Latin square","Derive"),("Factorial experiments","Derive"),
   ("BIBD and incidence matrices","Apply"),
   ("Principles of design","Recall"),("Confounding, split-plot, PBIBD","State")]),
 ("official","Official statistics",8,"1/4",[
   ("CSO, NSSO, NSO, MoSPI, NSC","Recall"),
   ("Commissions and committees","Recall"),("Indian statisticians","Recall"),
   ("Major surveys and indices","Recall"),("Census and vital statistics","Recall")]),
 ("nonparam","Nonparametric methods",6,"0/3",[
   ("Mann–Whitney U","Derive"),("Wilcoxon signed-rank and sign test","Apply"),
   ("Kruskal–Wallis and Friedman","Apply"),("Spearman and Kendall","Derive"),
   ("Matching test to design","Recall"),("Kolmogorov–Smirnov, run test","State")]),
]

P1 = [
 ("p1-highered","Higher education and national integration",20,"6/10",[
   ("Governance, UGC, AICTE, NAAC, NCTE","Recall"),("Types of universities","Recall"),
   ("NEP 2020 and HECI","Recall"),("Schemes, platforms, institutions","Recall"),
   ("Commissions and policies","Recall"),("National integration","Recall")]),
 ("p1-mathreason","Mathematical reasoning and aptitude",12,"3/6",[
   ("Number series","Derive"),("Percentages, profit and loss","Derive"),
   ("Interest and ratios","Derive"),("Basic statistics in Paper 1","Apply")]),
 ("p1-logical","Logical reasoning",12,"4/6",[
   ("Syllogisms","Apply"),("Indian logic","Recall"),
   ("Analogies and classification","Apply"),("Coding and decoding","Apply"),
   ("Fallacies","State")]),
 ("p1-ict","ICT",12,"4/6",[
   ("Generations and hardware","Recall"),("Networking and internet","Recall"),
   ("Security terms","Recall"),("E-governance and digital initiatives","Recall")]),
 ("p1-di","Data interpretation",10,"2/5",[
   ("Tables","Apply"),("Bar and line charts","Apply"),
   ("Pie charts","Apply"),("Speed drills","Apply")]),
 ("p1-teaching","Teaching aptitude",10,"3/5",[
   ("Learner characteristics","State"),("Methods of teaching","State"),
   ("Evaluation systems","Recall"),("Theories of learning","Recall")]),
 ("p1-environment","People, development and environment",10,"1/5",[
   ("Pollution types and effects","Recall"),("Natural hazards and disasters","Recall"),
   ("Energy resources","Recall"),("Environmental protocols","Recall")]),
 ("p1-communication","Communication",8,"3/4",[
   ("Types and barriers","Recall"),("Mass media","Recall"),
   ("Classroom communication","State")]),
 ("p1-research","Research aptitude",6,"1/3",[
   ("Types and methods of research","State"),("Research ethics","Recall"),
   ("Thesis and paper writing","Recall"),("Sampling in research","State")]),
]

modules = []
for order, (mid, name, marks, score, topics) in enumerate(P2 + P1, 1):
    paper = 1 if mid.startswith('p1-') else 2
    modules.append(dict(
        id=mid, paper=paper, name=name, marks=marks, order=order, baseline=score,
        passPct=80, targetQ=marks * 5,
        topics=[dict(id=f"{mid}-t{i+1}", name=t[0], extent=t[1]) for i, t in enumerate(topics)]))

json.dump(dict(modules=modules, updated="2026-10-11"),
          open(f'{OUT}/catalog.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('catalog:', len(modules), 'modules;  paper2 marks',
      sum(m['marks'] for m in modules if m['paper'] == 2),
      ' paper1 marks', sum(m['marks'] for m in modules if m['paper'] == 1))

# ---- week-1 question sets from the module bank ----
bank = json.load(open('/home/claude/w1/bank.json', encoding='utf-8'))
LET = ['A', 'B', 'C', 'D']

def mk(prefix, items):
    out = []
    for q in items:
        out.append(q)
    return out

multi = [dict(id=f"w1m{q['n']}", format="multi", topic=q['day'],
              stem=q['stem'], statements=q['sts'], options=q['opts'],
              answer=q['ans'],
              verdicts={k: dict(tf=v['tf'], why=v['why']) for k, v in q['v'].items()},
              explanation=" · ".join(f"{k} {'true' if v['tf'] else 'false'} — {v['why']}"
                                     for k, v in q['v'].items()))
         for q in bank['multi']]
numeric = [dict(id=f"w1n{q['n']}", format="numeric", stem=q['stem'], answer=q['ans'],
                explanation=q['work'], check=q['check'], options=[])
           for q in bank['numerical']]
concept = [dict(id=f"w1c{q['n']}", format="single", stem=q['stem'], options=q['opts'],
                answer=q['ans'], explanation=q['expl'])
           for q in bank['conceptual']]

sets = [
    ("inference_multi_1", "inference", "variant", "Week 1 — multi-statement", multi),
    ("inference_numeric_1", "inference", "variant", "Week 1 — numerical", numeric),
    ("inference_concept_1", "inference", "variant", "Week 1 — conceptual", concept),
]
for sid, mid, src, label, items in sets:
    json.dump(dict(moduleId=mid, source=src, label=label, count=len(items), items=items),
              open(f'{OUT}/{sid}.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{sid}: {len(items)} items')

# ---- the six June 2026 PYQ worked in week 1 ----
pyq = [
 dict(id="j26-q40", format="multi", paper=2, year="June 2026", pno=40,
      stem="x₁, …, xₙ is a random sample from f(x, θ) = θe^(−θx), θ > 0, x > 0.",
      statements=["Σxᵢ/n is the maximum likelihood estimate of θ",
                  "(n − 1)/Σxᵢ is the UMVUE of θ",
                  "Σxᵢ is the sufficient statistic for θ",
                  "Σxᵢ follows a Gamma distribution with parameter (1, θ)"],
      options=["A, B, D only", "B, C, D only", "A, B, C only", "A, C only"], answer="C",
      explanation="B and C are true, D is false — ΣXᵢ ~ Gamma(n, θ), not Gamma(1, θ). A is false as written (the MLE of θ is n/Σxᵢ), so this item is flawed; the only option containing both B and C without D is (C). When a multi-statement question has no perfect option, eliminate on the statement you are surest about.",
      verdicts={"A": dict(tf=True, why="keyed true, though strictly the MLE of θ is n/Σxᵢ — a flaw in the question"),
                "B": dict(tf=True, why="unbiased and a function of the complete sufficient statistic"),
                "C": dict(tf=True, why="the likelihood factorises through Σxᵢ"),
                "D": dict(tf=False, why="Gamma(n, θ); Gamma(1, θ) is a single exponential")}),
 dict(id="j26-q41", format="single", paper=2, year="June 2026", pno=41,
      stem="X₍₁₎ ≤ … ≤ X₍ᵣ₎ are the first r order statistics of a sample of size n from an exponential distribution with mean θ. With T₁ = (1/r)ΣX₍ᵢ₎ and T₂ = X₍ᵣ₎/r, which is unbiased for θ?",
      options=["T₁", "T₁ + (r − 1)T₂", "T₁ + (n − 1)T₂", "T₁ + (n − r)T₂"], answer="D",
      explanation="Type II censoring. The total time on test is ΣX₍ᵢ₎ + (n − r)X₍ᵣ₎, with expectation rθ, so dividing by r gives an unbiased estimator. Check it at r = n: the correction vanishes and it becomes X̄."),
 dict(id="j26-q57", format="multi", paper=2, year="June 2026", pno=57,
      stem="X₁, …, Xₙ iid with pdf f(x|θ) = e^(−(x−θ)) for x ≥ θ.",
      statements=["X̄ₙ → θ + 1 in probability",
                  "If Y = min(X₁,…,Xₙ) then f(y) = n·e^(−n(y−θ)), y ≥ θ",
                  "V(X̄ₙ) = n", "X̄ₙ → θ in distribution"],
      options=["A, B only", "B, C, D only", "A, C, D only", "A, B, C only"], answer="A",
      explanation="E(X) = θ + 1 and V(X) = 1, so A is true and D false. V(X̄) = 1/n, so C is false. The minimum of n exponentials is exponential at n times the rate, so B is true.",
      verdicts={"A": dict(tf=True, why="E(X) = θ + 1, so the WLLN gives this limit"),
                "B": dict(tf=True, why="the minimum of n exponentials has n times the rate"),
                "C": dict(tf=False, why="V(X̄) = 1/n, not n"),
                "D": dict(tf=False, why="the limit is θ + 1, not θ")}),
 dict(id="j26-q61", format="multi", paper=2, year="June 2026", pno=61,
      stem="h is an unbiased estimator of θ with E(h²) < ∞, and T is sufficient for Fθ. Which are TRUE?",
      statements=["E(h|T) is unbiased for θ", "Var{E(h|T)} ≤ Var(h)",
                  "E(h|T) is the unique UMVUE of θ", "E(h|T) is independent of θ"],
      options=["A, B only", "A, B, C only", "B, C, D only", "A, B, D only"], answer="D",
      explanation="A and B are Rao–Blackwell. D is true because sufficiency is exactly what makes E(h|T) free of θ. C is false — uniqueness as UMVUE needs completeness, which the question never assumes. That single missing word is the whole item.",
      verdicts={"A": dict(tf=True, why="the tower property"),
                "B": dict(tf=True, why="law of total variance"),
                "C": dict(tf=False, why="needs completeness, not just sufficiency"),
                "D": dict(tf=True, why="sufficiency makes the conditional distribution free of θ")}),
 dict(id="j26-q74", format="single", paper=2, year="June 2026", pno=74,
      stem="X₁, …, Xₙ iid exponential with mean θ, T_S = ΣXᵢ, and T(x₁) = 1 if X₁ > x₀, else 0. Then E[T(X₁)|T_S] is the UMVUE of:",
      options=["θ", "1/θ", "e^(−x₀/θ)", "1 − e^(−x₀/θ)"], answer="C",
      explanation="E[T(X₁)] = P(X₁ > x₀) = e^(−x₀/θ). Rao–Blackwell changes the estimator, never the estimand — so read E(h) first and the answer follows with no computation."),
 dict(id="j26-q78", format="multi", paper=2, year="June 2026", pno=78,
      stem="X₁, …, Xₙ is a random sample from Poisson(λ), with X̄ the sample mean and S² the sample variance (divisor n − 1).",
      statements=["X̄ is unbiased for λ", "S² is unbiased for λ",
                  "X̄ + S² is unbiased for λ", "0.3X̄ + 0.7S² is unbiased for λ"],
      options=["A only", "A, B only", "A, C, D only", "A, B, D only"], answer="D",
      explanation="Mean and variance both equal λ, so A and B hold. X̄ + S² has expectation 2λ, so C fails. Any weights summing to one preserve unbiasedness, so D holds for 0.3 and 0.7 or any other such pair.",
      verdicts={"A": dict(tf=True, why="E(X̄) = λ"),
                "B": dict(tf=True, why="for a Poisson the variance equals the mean"),
                "C": dict(tf=False, why="expectation is 2λ"),
                "D": dict(tf=True, why="weights sum to one")}),
]
json.dump(dict(moduleId="inference", source="pyq", label="UGC NET June 2026 — estimation items",
               count=len(pyq), items=pyq),
          open(f'{OUT}/inference_pyq_j26.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('inference_pyq_j26:', len(pyq), 'items')
print('files:', sorted(os.listdir(OUT)))
