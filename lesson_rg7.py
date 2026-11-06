#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression 6.7: heteroscedasticity and GLS. Numerical claims are checked by
verify_regression_t7.py. Run through addlesson.sh; do not hand-edit generated JSON.
"""
import json, io, os

OUT = "seed/lesson_rg7.json"
POOL = "seed/regression_t7_mastery.json"

S = [
 {"kind":"foundation","id":"s0","mins":7,"title":"Before the lesson — four checks",
  "objective":"Recall the conditional mean, variance, OLS variance and matrix inverse needed here.",
  "ask":{"q":"If Var(u|X)=σ²I, what does this say about the error variances and covariances?","nudge":"Read the diagonal and off-diagonal entries separately."},
  "body":["Regression does not require every observation to have the same error variance. It does require us to know what that variance assumption buys us. When the errors have unequal variances, the ordinary least-squares coefficient can still be centred on the true coefficient, but its usual standard errors and efficiency claim no longer follow.",
          "This lesson separates three questions: is OLS unbiased, is its usual variance formula correct, and can we use a more efficient estimator? Heteroscedasticity changes the second and third questions. It does not, by itself, change the first when the conditional mean is still correctly specified and the errors have conditional mean zero.",
          "You will use the same regression model as before, but replace one variance matrix by a diagonal matrix with unequal entries. The diagonal entries describe how noisy each observation is. The key is to put that information into the estimator rather than pretending all observations are equally precise."],
  "items":[
   {"ask":"What is the conditional mean assumption in the linear regression model?","recall":"E(u|X)=0, so E(y|X)=Xβ.","refresh":["Start from y=Xβ+u. Taking the conditional expectation given X gives E(y|X)=Xβ+E(u|X). If E(u|X)=0, the conditional mean is Xβ.","This is the condition that protects OLS unbiasedness. Unequal variances do not replace or contradict it. A model can have E(u|X)=0 and still have Var(u|X) depend on X."]},
   {"ask":"What does Var(u|X)=σ²I assert?","recall":"Equal conditional variances σ² and zero conditional covariances.","refresh":["The diagonal entries of σ²I are all σ², so each error has the same conditional variance. Every off-diagonal entry is zero, so distinct errors are uncorrelated conditionally on X.","Homoscedasticity is the equal-variance part. The zero off-diagonal entries are the no-correlation part. They are separate assumptions, even though both appear in σ²I."]},
   {"ask":"Write the OLS estimator and its variance under the classical covariance assumption.","recall":"β̂=(X′X)⁻¹X′y and Var(β̂|X)=σ²(X′X)⁻¹.","refresh":["Minimising the residual sum of squares gives the normal equations X′Xβ̂=X′y. If X has full column rank, solve to obtain β̂=(X′X)⁻¹X′y.","For a general error covariance Ω, the variance is (X′X)⁻¹X′ΩX(X′X)⁻¹. Only when Ω=σ²I does this simplify to σ²(X′X)⁻¹."]},
   {"ask":"What does positive definite mean for a covariance matrix?","recall":"a′Ωa>0 for every nonzero vector a.","refresh":["A covariance matrix is positive semidefinite; if every nonzero linear combination has positive variance, it is positive definite and invertible.","This lets us form Ω⁻¹ in GLS. If Ω is diagonal with positive entries, its inverse is diagonal with reciprocal entries."]}
  ]},
 {"kind":"intuition","id":"s1","mins":7,"title":"A noisy measurement should not count like a precise one",
  "objective":"Explain why unequal error variances make equal-weight least squares inefficient.",
  "body":["Imagine four instruments measuring the same underlying process. One instrument is stable; another fluctuates widely. Ordinary least squares treats each reading with the same squared-error penalty. A very noisy reading can therefore pull the fitted line as strongly as a precise reading.",
          "Heteroscedasticity means the conditional variance changes across observations or with a predictor. The conditional mean can still be correct. The problem is that OLS does not use the known pattern of precision, and the familiar homoscedastic standard-error formula is no longer valid."],
  "scenario":{"teaser":"Four sensors have different measurement precision.","title":"The four-sensor calibration",
   "body":["A laboratory calibrates four sensors against a known input. The mean response follows a straight line, but sensor 1 is carefully shielded while sensor 4 is exposed to vibration. Repeated measurements show that the spread of sensor 4 is much larger. The average response at each input can still follow the same line; it is the scatter around that line that changes. Giving every sensor the same squared-error weight wastes information. If the relative variances are known, the noisier sensor should contribute less to the fit. If they are unknown, the analyst should still protect inference by using a heteroscedasticity-consistent covariance estimate rather than the homoscedastic formula."],
   "q":"Does unequal variance alone imply that OLS is biased?","answer":"No. If E(u|X)=0 remains true and the model is correctly specified, OLS remains conditionally unbiased. Its usual covariance formula and efficiency claim are what fail."},
  "ask":{"q":"What changed in the sensor example: the conditional mean or the conditional variance?","nudge":"The line can stay the same while the scatter changes."}},
 {"kind":"explore","id":"s2","mins":7,"title":"Read the variance pattern",
  "objective":"Distinguish constant spread from spread that changes with the predictor.",
  "viz":{"type":"ineq-bounds","caption":"Treat the widening band as changing conditional variance, not a changing conditional mean."},
  "body":["Plot residuals against fitted values after fitting the mean model. A roughly constant vertical spread is compatible with homoscedasticity. A fan or funnel, where the spread widens or narrows, is a warning of heteroscedasticity.","The plot is a diagnostic, not a proof. A curved mean, an omitted variable or a few influential observations can also create patterns. Always inspect whether the conditional mean model is adequate before interpreting the variance pattern."],
  "ask":{"q":"A residual plot forms a widening fan but remains centred around zero. What assumption is most directly questioned?","nudge":"Look at the spread, not the centre."}},
 {"kind":"theory","id":"s3","mins":9,"title":"What heteroscedasticity changes — and what it does not",
  "objective":"State the general covariance formula and the Gauss–Markov consequence.",
  "blocks":[
   {"t":"formula","h":"General OLS covariance","body":"Var(β̂|X) = (X′X)⁻¹ X′ΩX (X′X)⁻¹, where Ω = Var(u|X)."},
   {"t":"step","h":"The homoscedastic special case","body":"If Ω=σ²I, then X′ΩX=σ²X′X. The two outer inverses reduce the expression to σ²(X′X)⁻¹. If Ω is not proportional to I, this simplification is not valid."},
   {"t":"def","h":"Heteroscedasticity","body":"The conditional error variance differs across observations: Var(uᵢ|X)=σ²ᵢ. Errors may still have zero conditional means and be mutually uncorrelated."},
   {"t":"step","h":"Gauss–Markov boundary","body":"With E(u|X)=0 and full-rank X, OLS remains linear and unbiased. Under unequal variances it is generally not BLUE among all linear unbiased estimators. The homoscedastic standard-error formula is generally wrong."}],
  "table":{"caption":"Effect of heteroscedasticity when the conditional mean is correct","head":["Property","What happens"],"rows":[["OLS unbiasedness","Retained if E(u|X)=0"],["OLS consistency","Retained under standard regularity conditions"],["Usual OLS variance formula","Generally invalid"],["OLS efficiency / BLUE","Generally lost"],["Homoscedastic t and F standard errors","Not reliable without correction"]]},
  "flow":{"title":"Choose the right response","alt":"First check the mean model, then determine whether the variance pattern is known, then choose GLS or robust inference.",
   "nodes":[{"id":"a","r":0,"c":1,"label":"Check E(u|X)=0","kind":"start"},{"id":"b","r":1,"c":1,"label":"Assess variance pattern","kind":"step"},{"id":"c","r":2,"c":0,"label":"Known Ω: GLS","kind":"step"},{"id":"d","r":2,"c":2,"label":"Unknown Ω: robust SE","kind":"step"},{"id":"e","r":3,"c":1,"label":"Check specification","kind":"end"}],
   "edges":[{"from":"a","to":"b"},{"from":"b","to":"c"},{"from":"b","to":"d"},{"from":"c","to":"e"},{"from":"d","to":"e"}],
   "note":"Robust standard errors change estimated uncertainty, not the OLS coefficients."},
  "ask":{"q":"If heteroscedasticity is present but E(u|X)=0 holds, what property of OLS survives?","nudge":"Separate the expected value from the variance."}},
 {"kind":"worked","id":"s4","mins":8,"title":"Compute OLS and GLS on a small model",
  "objective":"Calculate the OLS and GLS covariance matrices for a diagonal variance pattern.",
  "ask":{"q":"Which estimator has the smaller covariance matrix in this verified example?","nudge":"Compare the two matrices through their difference."},
  "problem":"Let X have rows (1,0), (1,1), (1,2), (1,3), and let Ω=diag(1,2,3,4). Find the OLS and GLS covariance matrices, omitting the common factor σ².",
  "steps":[
   {"say":"Write the design cross-product and its inverse.","math":"X′X=[[4,6],[6,14]],  (X′X)⁻¹=[[0.7,−0.3],[−0.3,0.2]].","why":"The determinant is 4×14−6×6=20, so the inverse is (1/20)[[14,−6],[−6,4]]."},
   {"say":"Use the general covariance formula for OLS.","math":"X′ΩX=[[10,20],[20,50]].  Var(β̂_OLS)=(X′X)⁻¹X′ΩX(X′X)⁻¹=[[1,−0.5],[−0.5,0.5]].","why":"This is not σ²(X′X)⁻¹ because Ω is not σ²I. The covariance values are independently checked in verify_regression_t7.py."},
   {"say":"Use the GLS covariance formula.","math":"Var(β̂_GLS)=(X′Ω⁻¹X)⁻¹=[[0.7,−0.3],[−0.3,0.2]].","why":"The GLS covariance is smaller in the positive-semidefinite ordering for this example. The difference is [[0.3,−0.2],[−0.2,0.3]], whose eigenvalues are 0.1 and 0.5."}],
  "after":"The OLS estimate is not automatically biased. It simply fails to use the known precision pattern. GLS weights each observation according to its variance."},
 {"kind":"recall","id":"s5","mins":2,"title":"Pause and recall","objective":"Retrieve the core distinctions before moving to the GLS derivation.",
  "intro":"Answer each before revealing it.",
  "items":[{"q":"Does heteroscedasticity alone bias OLS?","a":"No, not if E(u|X)=0 and the mean model is correctly specified."},
           {"q":"What is the general OLS covariance formula?","a":"(X′X)⁻¹X′ΩX(X′X)⁻¹."},
           {"q":"What does GLS use that OLS ignores?","a":"The error covariance matrix Ω, through Ω⁻¹."},
           {"q":"What do robust standard errors change?","a":"The estimated covariance of OLS, not the OLS coefficient estimates."},
           {"q":"When does GLS reduce to OLS?","a":"When Ω is proportional to the identity matrix."}]},
 {"kind":"completion","id":"s6","mins":8,"title":"Your turn — finish the GLS estimator",
  "objective":"Construct GLS from the weighted least-squares objective.",
  "problem":"Assume Var(u|X)=Ω, where Ω is known and positive definite. Derive the GLS estimator from the objective function.",
  "steps":[
   {"say":"Write the criterion to minimise.","blank":{"prompt":"The weighted residual criterion is…","answer":"(y−Xβ)′Ω⁻¹(y−Xβ)","accept":["(y-Xβ)' Omega inverse (y-Xβ)"],"hint":"Use the inverse covariance as the weight matrix."},"why":"An observation with a large error variance receives a smaller precision weight."},
   {"say":"Differentiate with respect to β and set equal to zero.","blank":{"prompt":"The normal equation is…","answer":"X′Ω⁻¹X β̂ = X′Ω⁻¹y","accept":["X transpose Omega inverse X beta hat equals X transpose Omega inverse y"],"hint":"Expand the quadratic and collect the terms containing β."},"why":"This is the weighted analogue of the OLS normal equation."},
   {"say":"Solve when X has full column rank.","blank":{"prompt":"The GLS estimator is…","answer":"β̂_GLS=(X′Ω⁻¹X)⁻¹X′Ω⁻¹y","accept":["(X' Omega inverse X) inverse X' Omega inverse y"],"hint":"Premultiply by the inverse of the weighted cross-product."},"why":"The expression is linear in y and uses the known covariance pattern."}],
  "after":"GLS is OLS after transforming the data by a factor that whitens the errors."},
 {"kind":"theory","id":"s7","mins":7,"title":"The GLS theorem and feasible GLS",
  "objective":"Explain why GLS is BLUE when Ω is known and why feasible GLS is different.",
  "blocks":[
   {"t":"formula","h":"GLS estimator","body":"β̂_GLS=(X′Ω⁻¹X)⁻¹X′Ω⁻¹y."},
   {"t":"step","h":"Its covariance","body":"Var(β̂_GLS|X)=(X′Ω⁻¹X)⁻¹ when Var(u|X)=Ω. Under the stated assumptions, GLS is BLUE."},
   {"t":"step","h":"Whitening interpretation","body":"Choose C so C′C=Ω⁻¹. Transform y*=Cy and X*=CX. Then Var(Cu|X)=CΩC′=I when C is chosen as a symmetric inverse square root. OLS on the transformed model is GLS in the original model."},
   {"t":"def","h":"Feasible GLS","body":"When Ω is unknown, estimate its structure first and substitute the estimate. This is feasible GLS (FGLS). Its finite-sample properties depend on how well the variance model is estimated."}],
  "ask":{"q":"Why is feasible GLS not exactly the same as GLS with known Ω?","nudge":"One estimator uses the true covariance; the other estimates it."}},
 {"kind":"guided","id":"s8","mins":8,"title":"Choose between robust OLS and feasible GLS",
  "objective":"Select an inference method when the variance pattern is not known.",
  "problem":"A cross-sectional study has a credible linear conditional mean but the error variance rises with household income. The variance function is not known in advance. What should the analyst do first?",
  "hints":["Identify whether the conditional mean assumption is still plausible.","Distinguish a correction to standard errors from a reweighted estimator.","Use a heteroscedasticity-consistent covariance estimate for OLS inference; consider FGLS only with a defensible variance model."],
  "answer":"Keep OLS as the coefficient estimator if the mean model is correct, and report heteroscedasticity-robust standard errors. FGLS is an option only after specifying and estimating a credible variance structure.",
  "check":"Do not claim that robust standard errors make OLS more efficient or change its coefficients.",
  "scenario":{"teaser":"A bank models loan balances across households.","title":"Income-dependent variation",
   "body":["A bank models average loan balance as a function of income, age and household size. The mean relationship is approximately linear over the observed range, but the dispersion of balances grows with income. The analyst does not know whether variance is proportional to income, income squared, or another function. Replacing OLS with arbitrary weights would introduce an unsupported variance model. A defensible first analysis retains the conditional mean model, checks the residual pattern and uses a heteroscedasticity-consistent covariance estimator. If later work supports a variance function, feasible GLS can be compared as a sensitivity analysis."],
   "q":"What is the safe first inferential adjustment?","answer":"Use heteroscedasticity-consistent standard errors with OLS, while checking the mean specification."},
  "solution":[{"say":"Keep the mean model separate from the variance model.","math":"E(y|X)=Xβ; Var(u|X)=Ω(X), with Ω not yet specified.","why":"The first equation can remain correct while the second changes with income."},
             {"say":"Protect inference without inventing weights.","math":"Use a sandwich covariance estimate: (X′X)⁻¹ [Σᵢ xᵢxᵢ′ êᵢ²] (X′X)⁻¹.","why":"The robust estimator estimates the covariance of OLS without requiring a parametric variance function."}]},
 {"kind":"trapcheck","id":"s9","mins":6,"title":"Six statements to test",
  "objective":"Reject common false claims about heteroscedasticity, GLS and robust inference.",
  "intro":"Decide true or false on all six before revealing them.",
  "items":[
   {"claim":"Heteroscedasticity necessarily makes OLS biased.","tf":False,"why":"It does not if E(u|X)=0 and the conditional mean model is correct."},
   {"claim":"Under heteroscedasticity, σ²(X′X)⁻¹ is generally the correct OLS covariance matrix.","tf":False,"why":"Use the sandwich form with Ω between the two inverse cross-products."},
   {"claim":"Heteroscedasticity can make OLS inefficient among linear unbiased estimators.","tf":True,"why":"The Gauss–Markov BLUE result relies on spherical error covariance."},
   {"claim":"Robust standard errors change the fitted OLS coefficients.","tf":False,"why":"They change estimated uncertainty, not the least-squares minimiser."},
   {"claim":"If Ω is known and positive definite, GLS weights by Ω⁻¹.","tf":True,"why":"The inverse covariance is the precision matrix in the GLS criterion."},
   {"claim":"If Ω=σ²I, GLS and OLS give the same coefficient estimate.","tf":True,"why":"The common scalar factor cancels from the GLS normal equations."}]},
 {"kind":"guided","id":"s10","mins":8,"title":"Transfer — a two-group variance model",
  "objective":"Recognise a variance ratio and construct the corresponding WLS weights.",
  "problem":"A study has two groups. Each observation in group A has error variance 4σ²; each in group B has error variance σ². Errors are conditionally uncorrelated. State the relative WLS weights and explain which group receives more weight.",
  "hints":["Write Ω as a diagonal matrix with the group-specific variances.","GLS uses the inverse of Ω.","Compare the diagonal entries of Ω⁻¹; do not confuse variance with precision."],
  "answer":"Group A receives weight 1/4 and group B weight 1, up to a common factor. Group B is four times as precise and receives four times the weight.",
  "check":"Weights are inversely proportional to variances, not proportional to them.",
  "solution":[{"say":"Write the covariance and its inverse.","math":"Ω=σ² diag(4,…,4,1,…,1); Ω⁻¹=σ⁻² diag(1/4,…,1/4,1,…,1).","why":"The common σ⁻² factor cancels from the weighted minimisation, leaving relative weights 1/4 and 1."},
             {"say":"Interpret the weights as precision.","math":"w_A:w_B=(1/4):1=1:4.","why":"The lower-variance group contributes four times as much precision per observation."}]},
 {"kind":"theory","id":"s11","mins":6,"title":"Testing and diagnosing heteroscedasticity",
  "objective":"Describe residual-based tests and state their limits.",
  "blocks":[
   {"t":"step","h":"Breusch–Pagan idea","body":"Regress squared OLS residuals on the variables thought to explain the variance. The LM statistic is nR² from the auxiliary regression and is compared approximately with χ² degrees of freedom equal to the number of nonconstant variance regressors under the null."},
   {"t":"step","h":"White test idea","body":"Regress squared residuals on the original regressors, their squares and cross-products. The auxiliary model can become large; use it only when the sample supports it."},
   {"t":"def","h":"Limitations","body":"These tests detect patterns, not causes. A misspecified conditional mean can look like changing variance. Large samples support the asymptotic reference distributions."},
   {"t":"step","h":"What to report","body":"Show the residual-versus-fitted plot, state the covariance estimator used for inference, and explain any variance model used for GLS or FGLS."}],
  "ask":{"q":"Why should a variance test follow a check of the conditional mean model?","nudge":"A misspecified mean can leave a pattern in squared residuals."}},
 {"kind":"recall","id":"s12","mins":2,"title":"Second recall","objective":"Retrieve the formulas and decision rule most likely to fade.",
  "intro":"Answer, then reveal.",
  "items":[{"q":"OLS covariance with general Ω?","a":"(X′X)⁻¹X′ΩX(X′X)⁻¹."},
           {"q":"GLS estimator?","a":"(X′Ω⁻¹X)⁻¹X′Ω⁻¹y."},
           {"q":"GLS covariance?","a":"(X′Ω⁻¹X)⁻¹."},
           {"q":"Robust standard errors change what?","a":"The estimated covariance of OLS, not its coefficients."}]},
 {"kind":"summary","id":"s13","mins":3,"title":"What you should now be able to do",
  "objective":"Summarise the decisions and calculations you can perform unaided.",
  "body":["Separate unbiasedness from efficiency: heteroscedasticity alone does not bias OLS when E(u|X)=0 holds.",
          "Replace the homoscedastic covariance formula with (X′X)⁻¹X′ΩX(X′X)⁻¹.",
          "Derive GLS by minimising (y−Xβ)′Ω⁻¹(y−Xβ).",
          "Use robust standard errors when the variance pattern is unknown; use GLS or FGLS only when a defensible covariance structure is available.",
          "Treat Breusch–Pagan and White tests as diagnostics, not as proof of a causal variance mechanism."]},
 {"kind":"theory","id":"s14","mins":8,"ext":True,"title":"JRF extension — the sandwich estimator",
  "objective":"Recognise the HC0 covariance estimator and its finite-sample variants.",
  "blocks":[{"t":"formula","h":"HC0 sandwich","body":"V̂_HC0=(X′X)⁻¹[Σᵢ xᵢxᵢ′ êᵢ²](X′X)⁻¹."},
           {"t":"step","h":"Small-sample corrections","body":"HC1 multiplies HC0 by n/(n−k). HC2 divides each squared residual by 1−hᵢᵢ. HC3 divides by (1−hᵢᵢ)². These are different finite-sample corrections; state which one software reports."},
           {"t":"step","h":"Do not overclaim","body":"Robust covariance estimation does not repair omitted variables, endogeneity, serial correlation, or a wrong conditional mean. It addresses heteroscedasticity in the covariance estimate."}],
  "ask":{"q":"Which part of the OLS output does HC3 replace?","nudge":"It is a covariance estimator, not a coefficient estimator."}},
 {"kind":"quiz","id":"s15","mins":12,"title":"Mastery test",
  "objective":"Demonstrate independent understanding with unseen questions.",
  "setId":"regression_t7_mastery"}
]

CORE=[s for s in S if not s.get("ext")]
objectives=[
 "Distinguish heteroscedasticity from a nonzero conditional error mean.",
 "Derive the OLS covariance matrix under a general error covariance Ω.",
 "Explain why OLS can remain unbiased but lose BLUE efficiency under heteroscedasticity.",
 "Derive the GLS estimator and covariance matrix from weighted least squares.",
 "Choose between robust OLS inference, GLS and feasible GLS in a practical case.",
 "Explain the purpose and limits of Breusch–Pagan and White diagnostics."
]
LES={
 "id":"regressiont7","topicId":"regression-t7","moduleId":"regression",
 "title":"Heteroscedasticity and GLS",
 "breadcrumb":"Regression → Linear model assumptions → Heteroscedasticity and GLS",
 "engine":"B","engineName":"Separate the conditional mean from the variance; weight by inverse covariance when it is known.",
 "version":"1.0","status":"approved","estMin":sum(s["mins"] for s in CORE),
 "objectives":objectives,
 "prereq":[{"id":"p1","name":"Conditional expectation in the linear model","why":"Unbiasedness depends on E(u|X)=0."},
           {"id":"p2","name":"Variance of a linear transformation","why":"The general OLS covariance is a matrix transformation of Ω."},
           {"id":"p3","name":"Positive definite matrices and inverses","why":"GLS uses Ω⁻¹ and the inverse weighted cross-product."}],
 "traps":["Heteroscedasticity does not automatically bias OLS.","Do not use σ²(X′X)⁻¹ when Ω is not σ²I.","Robust standard errors do not change OLS coefficients.","GLS weights by inverse variance, not variance.","A residual pattern can reflect a misspecified mean."],
 "revision":{"sheet":["E(u|X)=0 protects OLS unbiasedness.","Var(β̂_OLS|X)=(X′X)⁻¹X′ΩX(X′X)⁻¹.","GLS=(X′Ω⁻¹X)⁻¹X′Ω⁻¹y.","Var(β̂_GLS|X)=(X′Ω⁻¹X)⁻¹.","Unknown variance pattern: robust OLS covariance; defensible variance model: FGLS."],
 "cards":[["Does heteroscedasticity alone bias OLS?","No, if the conditional mean is correctly specified and E(u|X)=0."],
          ["General OLS covariance?","(X′X)⁻¹X′ΩX(X′X)⁻¹."],
          ["GLS estimator?","(X′Ω⁻¹X)⁻¹X′Ω⁻¹y."],
          ["What do robust SEs change?","The estimated covariance, not the coefficients."]],
 "tricks":["Mean first, variance second: bias and efficiency are different questions.","GLS uses precision: inverse covariance.","Robust SEs revise uncertainty, not the fitted line."],
 "shortcuts":["Ω=σ²I implies GLS=OLS.","For diagonal Ω, WLS weights are 1/σᵢ².","Breusch–Pagan LM is approximately nR²."],
 "remember":["Unequal variance can leave OLS unbiased but inefficient.","Never report the homoscedastic standard errors without defending the variance assumption."]},
 "howto":"Work through scenes 0–10 for the main lesson. Scene 11 covers diagnostic tests; the optional extension covers HC0–HC3. This topic does not cover serial correlation (regression-t6) or endogeneity (regression-t8).",
 "refs":[{"title":"Introductory Econometrics: A Modern Approach","where":"Chapter 8, Heteroskedasticity","site":"Jeffrey M. Wooldridge","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"For the distinction between OLS, robust covariance estimation and feasible GLS."}],
 "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},"diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":True,"retestDays":7,
 "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints."},
 "provenance":"No dedicated June 2026 anchor is assigned to regression-t7. The regression variant bank contains Q38 variant 02 on heteroscedasticity; it is covered in the diagnostic and inference sections. Numerical matrix example and covariance values are computed in verify_regression_t7.py. The lesson assumes a correctly specified conditional mean and conditionally uncorrelated errors for the diagonal WLS examples. Scope excludes autocorrelation and endogeneity.",
 "scenes":S
}

def item(i,fmt,diff,stem,opts,ans,exp,**kw):
 d={"id":"regression-t7-m-%02d"%i,"format":fmt,"topic":"regression-t7","diff":diff,"stem":stem,"options":opts,"answer":ans,"explanation":exp}
 d.update(kw); return d
I=[
 item(1,"single","easy","Heteroscedasticity is present when:",["Var(uᵢ|X) differs across observations","E(uᵢ|X) differs from zero","the regressors are correlated","the sample size is small"],"A","Heteroscedasticity concerns unequal conditional error variances; it does not define bias or multicollinearity."),
 item(2,"single","easy","If E(u|X)=0 but Var(u|X)=Ω≠σ²I, OLS is generally:",["biased and inconsistent","conditionally unbiased but not generally BLUE","nonlinear","undefined"],"B","The conditional mean restriction preserves unbiasedness; the spherical covariance needed for BLUE is absent."),
 item(3,"numeric","easy","For Ω=diag(4,9), what are the relative WLS precision weights?",["4 and 9","1/4 and 1/9","1/2 and 1/3","9 and 4"],"B","GLS uses inverse variances, so the weights are 1/4 and 1/9, up to a common scale.",check:"The larger variance 9 must receive the smaller weight 1/9."),
 item(4,"single","easy","Which covariance formula is valid for OLS with general Ω?",["σ²(X′X)⁻¹","(X′X)⁻¹X′ΩX(X′X)⁻¹","(X′Ω⁻¹X)⁻¹","X′ΩX"],"B","Apply Var(Ay)=A Var(y) A′ to A=(X′X)⁻¹X′."),
 item(5,"numeric","easy","If Var(uᵢ|X)=σ²(1+xᵢ²), what is the WLS weight apart from the common factor σ⁻²?",["1+xᵢ²","1/(1+xᵢ²)","xᵢ²","1/xᵢ²"],"B","The precision weight is the reciprocal of the variance multiplier.",check:"A larger xᵢ² increases variance and must reduce the weight."),
 item(6,"single","easy","Heteroscedasticity-robust standard errors:",["change the OLS coefficients","make OLS BLUE","replace the estimated covariance of OLS","remove omitted-variable bias"],"C","A sandwich estimator changes estimated uncertainty, not the OLS minimiser or the mean-model assumptions."),
 item(7,"numeric","moderate","For X′X inverse [[0.7,−0.3],[−0.3,0.2]] and Ω=diag(1,2,3,4), the verified OLS covariance matrix (per common σ² factor) is:",["[[0.7,−0.3],[−0.3,0.2]]","[[1,−0.5],[−0.5,0.5]]","[[1,0],[0,1]]","[[0.5,−0.2],[−0.2,0.3]]"],"B","Substitution into (X′X)⁻¹X′ΩX(X′X)⁻¹ gives [[1,−0.5],[−0.5,0.5]].",check:"The computed covariance is symmetric and differs from the homoscedastic shortcut."),
 item(8,"single","moderate","The GLS estimator minimises:",["Σeᵢ²","(y−Xβ)′Ω⁻¹(y−Xβ)","(y−Xβ)′Ω(y−Xβ)","|y−Xβ|"],"B","GLS weights residuals by the precision matrix Ω⁻¹."),
 item(9,"numeric","moderate","For the model in the verification script, what is the GLS covariance matrix per common σ² factor?",["[[1,−0.5],[−0.5,0.5]]","[[0.7,−0.3],[−0.3,0.2]]","[[0.2,0],[0,0.7]]","[[1,0],[0,1]]"],"B","The GLS covariance is (X′Ω⁻¹X)⁻¹, computed as [[0.7,−0.3],[−0.3,0.2]].",check:"The GLS covariance is positive definite and no larger than OLS in this example."),
 item(10,"multi","moderate","Which statements about heteroscedasticity are correct?",["OLS may remain unbiased","The usual homoscedastic SE formula is generally invalid","Robust SEs change OLS coefficients","OLS may lose BLUE efficiency"],"A","A, B and D are correct. C is false: robust covariance estimation changes inference, not the fitted coefficients.",statements:["If E(u|X)=0 holds, OLS can remain unbiased.","The homoscedastic covariance formula is generally invalid.","Robust standard errors alter the OLS coefficient estimates.","OLS may lose BLUE efficiency."],verdicts:{"A":{"tf":True,"why":"Zero conditional error mean preserves OLS unbiasedness."},"B":{"tf":True,"why":"The general covariance uses Ω, not σ²I."},"C":{"tf":False,"why":"The coefficients are unchanged; only the estimated covariance changes."},"D":{"tf":True,"why":"Unequal variances remove the spherical covariance condition for BLUE."}}),
 item(11,"single","moderate","If Ω=σ²I, the GLS coefficient estimator:",["differs from OLS","equals OLS","is biased","requires normal errors"],"B","The scalar σ⁻² cancels from the GLS normal equations, giving the OLS estimator."),
 item(12,"numeric","moderate","In the two-group example, group A variance is 4σ² and group B variance is σ². The relative weights A:B are:",["4:1","1:4","1:2","2:1"],"B","Weights are inverse variances: 1/4 to 1, or 1:4.",check:"The less noisy group B receives four times the weight."),
 item(13,"single","moderate","The Breusch–Pagan LM statistic is based on:",["n times the R² from an auxiliary regression of squared residuals","the OLS slope t statistic","the Durbin–Watson statistic","the determinant of X′X"],"A","The auxiliary regression explains squared residuals using variables associated with variance; LM is approximately nR²."),
 item(14,"single","moderate","A residual-versus-fitted plot with a fan shape is:",["proof of endogeneity","evidence consistent with heteroscedasticity","proof that OLS is biased","evidence of perfect multicollinearity"],"B","A fan indicates changing residual spread, but it is a diagnostic and not proof of the cause."),
 item(15,"multi","moderate","Which are appropriate statements about feasible GLS?",["It estimates an unknown variance structure","It is identical in finite samples to GLS with known Ω","Its quality depends on the variance model","It should be justified rather than applied with arbitrary weights"],"A","A, C and D are correct. B is false because estimated weights add uncertainty.",statements:["FGLS estimates an unknown covariance structure.","FGLS is exactly the same in finite samples as known-Ω GLS.","FGLS depends on the adequacy of its variance model.","Arbitrary weights are not a substitute for a defensible variance model."],verdicts:{"A":{"tf":True,"why":"The covariance structure is estimated before weighting."},"B":{"tf":False,"why":"Estimated weights are not the true known covariance matrix."},"C":{"tf":True,"why":"Misspecifying the variance function can harm its performance."},"D":{"tf":True,"why":"Weights need a statistical basis."}}),
 item(16,"single","hard","A correctly specified mean model has E(u|X)=0 and unequal conditional variances. Which statement is most accurate?",["OLS is necessarily biased","OLS is unbiased but its conventional SEs may be wrong","GLS is always available without estimating Ω","normality restores homoscedasticity"],"B","The mean restriction protects unbiasedness; unequal variance changes the covariance and efficiency conclusions."),
 item(17,"numeric","hard","For a model with n=40 observations and k=3 parameters, the HC1 multiplier applied to HC0 is:",["40/3","3/40","40/37","37/40"],"C","HC1 multiplies HC0 by n/(n−k)=40/37.",check:"The correction is slightly above one because n exceeds n−k."),
 item(18,"single","hard","Which condition is needed for the usual GLS covariance (X′Ω⁻¹X)⁻¹?",["Ω known and positive definite","errors normally distributed","X has orthogonal columns","the response is binary"],"A","Known positive definite Ω permits the inverse covariance weighting; normality is not required for the BLUE result."),
 item(19,"numeric","hard","If Var(uᵢ|X)=σ²·4 for every observation, the GLS relative weight for each observation is:",["4","1/4","σ²","1"],"B","All observations receive the same inverse-variance weight, so GLS is coefficient-equivalent to OLS.",check:"A common positive weight cancels from the normal equations."),
 item(20,"single","hard","A White test auxiliary regression typically includes:",["only the fitted values","original regressors, their squares and cross-products","the response ranks only","lagged residuals only"],"B","White's general auxiliary regression includes squares and cross-products to detect broad variance patterns.")
]
POOLD={"moduleId":"regression","topicId":"regression-t7","source":"mastery","label":"Heteroscedasticity and GLS — mastery test (unseen)","count":20,"items":I}

# Structural checks before serialisation; addlesson.sh performs the full app validator.
assert len(CORE)==15 and LES["estMin"]==100
assert len(I)==20 and sum(x["diff"]=="easy" for x in I)==6 and sum(x["diff"]=="moderate" for x in I)==10 and sum(x["diff"]=="hard" for x in I)==4
assert sum(x["format"]=="numeric" for x in I)>=4 and sum(x["format"]=="multi" for x in I)>=2
for x in I:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert len(x.get("check",""))>=20
os.makedirs("seed",exist_ok=True)
with io.open(OUT,"w",encoding="utf-8") as f: json.dump(LES,f,ensure_ascii=False,indent=1)
with io.open(POOL,"w",encoding="utf-8") as f: json.dump(POOLD,f,ensure_ascii=False,indent=1)
print("wrote",OUT,"and",POOL,"; scenes",len(S),"core minutes",LES["estMin"],"; mastery items",len(I))
