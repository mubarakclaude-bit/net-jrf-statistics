# UGC NET Statistics (Subject Code 107) — syllabus alignment reference

Source of authority: the user-provided UGC / NET Bureau PDF, `Syllabus_Statistics_UGC_NET_English.pdf`, titled “NET Syllabus”, Subject Statistics, Code 107. It states a total of ten units. This document is a transcription-oriented map for lesson scope checks; the attached PDF and `seed/meta_syllabus.json` remain the source records.

## Official ten-unit sequence and content

### Unit I — Probability and Distributions
Basic concepts of probability; conditional probability; Bayes theorem; independent events; random variables and distribution functions; expectation and moments; moment generating function; standard discrete and continuous univariate distributions; jointly distributed random variables; marginal and conditional distributions; Chebyshev inequality; sampling distributions; transformation of random variables; characteristic function and its properties; modes of convergence of random variables; weak and strong laws of large numbers; central limit theorems (i.i.d. case).

Repository module label: `1` / `probability`.

### Unit II — Real Analysis and Matrix Algebra
**Real analysis:** finite, countable and uncountable sets; sequences of real numbers; convergence, bounded and monotonic sequences; Cauchy criterion; series and tests of convergence; alternating series; absolute and conditional convergence; power series and radius of convergence; functions of a real variable: limit, continuity, monotone functions, uniform continuity, differentiability, Rolle’s theorem, mean value theorems, Taylor’s theorem, L’Hospital’s rule, Riemann integration and its properties, improper integrals; functions of two real variables: limit, continuity, partial derivatives, total derivative, maxima and minima, saddle point, Lagrange multipliers, double and triple integrals and applications.

**Matrix algebra:** vector spaces, subspaces, span, linear independence, basis and dimension; row and column spaces; rank and nullity; row reduced echelon form; trace and determinant; inverse; systems of linear equations; Gram–Schmidt orthogonalization; characteristic roots/vectors and characteristic polynomial; Cayley–Hamilton theorem; symmetric, skew-symmetric and orthogonal matrices and their characteristic roots; positive definite and positive semi-definite matrices and properties; quadratic forms.

Repository module label: `2` / `maths`.

### Unit III — Sampling Methods and Design of Experiments
**Sampling methods:** simple random sampling; stratified random sampling; systematic sampling; ratio and regression methods of estimation; cluster sampling for equal and unequal clusters; double sampling; sampling with varying probabilities with and without replacement; nonnegative variance estimation; ordered and unordered estimators.

**Design of experiments:** ANOVA in one-way and two-way classification (with and without interaction) in fixed effects model; principles of design of experiments; completely randomized design; randomized block design; Latin square design; missing plot techniques; factorial experiments; confounding in factorial experiments; incomplete block designs and intra-block/inter-block analysis; connectedness and orthogonality of block designs; BIBD; inter-block analysis and recovery of intra-block information of BIBD.

Repository splits this single official unit into labels `3A` / `sampling` and `3B` / `design`.

### Unit IV — Estimation Theory
**Point estimation:** unbiasedness; consistency; method of moments and maximum likelihood estimators; efficiency; UMVUE; Rao–Cramer lower bound; sufficiency; factorisation theorem; minimal sufficiency; ancillary statistic; completeness; Rao–Blackwell theorem; Lehmann–Scheffé theorem; Basu’s theorem.

**Interval estimation:** method of pivoting; confidence intervals for parameters in one-sample and two-sample normal populations; large-sample confidence intervals.

**Nonparametric inference named in this unit:** distributions of order statistics; empirical distribution function and properties; Spearman and Kendall rank correlation coefficients.

Repository label: `4` / `inference` for estimation; the catalog separately maps nonparametric testing topics to Unit V label `5`. Preserve the PDF's wording and flag any local catalog classification difference rather than silently moving topics.

### Unit V — Testing of Hypotheses
Basic concepts; construction of tests; Neyman–Pearson lemma; families with monotone likelihood ratio; UMP, UMP unbiased and UMP invariant tests; likelihood ratio tests and applications to one- and two-sample problems; Wald sequential probability ratio test; operating characteristic and average sample number.

Chi-square goodness-of-fit, independence of attributes and homogeneity in contingency tables; sign test; Wilcoxon signed-rank test; Mann–Whitney U-test; linear rank tests for location and scale; Kruskal–Wallis test.

Repository label: `5` / `nonparam` for the nonparametric testing module; estimation topics retain `4`.

### Unit VI — Linear Estimation, Regression Analysis and Econometrics
Simple and multiple linear regression; Gauss–Markov model; least squares and maximum likelihood estimation; tests of regression parameters; ANOVA for linear model; adjusted coefficient of determination (the PDF text extraction leaves the symbol blank); tests of linear hypotheses; generalized and weighted least squares; indicator/dummy variables; multicollinearity; heteroscedasticity; autocorrelation; Durbin–Watson test; logistic regression.

Restricted regression under exact, stochastic and mixed restrictions; stochastic regressors and errors-in-variables; instrumental-variable estimator; simultaneous equations; identification; two-stage least squares; k-class estimator.

Repository label: `6` / `regression`.

### Unit VII — Time Series
Time-series data and descriptive measures; autocovariance; ACF and PACF; correlogram; strong and weak stationarity; ergodicity; general linear process and Wold decomposition; MA, AR and ARMA processes; stationarity and invertibility conditions; Yule–Walker equations; identification, estimation and order selection of AR, MA and ARMA; forecasting with stationary and invertible processes.

Non-stationary time series: random walk; ARIMA(p,d,q) and parameter estimation. Frequency domain: spectral representation; spectral density of AR, MA and ARMA; periodogram and spectral-density estimation.

Repository label: `7` / `timeseries`.

### Unit VIII — Multivariate Analysis
Multivariate normal distribution and properties; estimation of mean vector and covariance matrix under multivariate normality; sample mean vector distribution; Wishart distribution and properties; distributions of simple, partial and multiple correlation coefficients and related tests; inference for parameters; hypothesis tests related to mean vector and generalized statistic (the symbol is blank in the PDF text extraction); discriminant analysis; principal component analysis; canonical correlation analysis.

Repository label: `8` / `multivariate`.

### Unit IX — Stochastic Processes
Markov chains with finite and countable state spaces; classification of states; Chapman–Kolmogorov equations; limiting behaviour of n-step transition probabilities; stationary distribution; Gambler’s ruin; simple random walk; Poisson process; inter-arrival and waiting-time distributions; birth and death processes; M/M/1 queues.

Repository label: `9` / `stochastic`.

### Unit X — Indian Statistical System and Research Methodology
**Indian Statistical System:** Ministry of Statistics and Programme Implementation and its wings; National Statistical Commission; National Statistics Office; census and large sample surveys; contributions of P. C. Mahalanobis, P. V. Sukhatme, R. C. Bose, S. N. Roy, C. R. Rao and other prominent Indian statisticians.

**Research methodology / R:** R as a calculator; functions and matrix operations; built-in functions; missing data and logical operators; conditional execution and loops; data management with sequences, repeats, sorting, ordering and strings; lists, factors, display and formatting; data frames; data input/output; graphics and plots; basics of programming, scripts and functions; word-processing software.

Repository splits this official unit into `10A` / `official` and `10B` / `rprog`.

## Mapping and scope rules

1. Use the exact official unit title and topic wording above when mapping lessons. A lesson may teach prerequisites not explicitly named, but must label them as prerequisites rather than claiming extra syllabus coverage.
2. Repository labels are not a one-to-one Roman-numeral sequence: Unit III splits into 3A/3B and Unit X splits into 10A/10B. Unit IV also has the nonparametric inference topics listed in the PDF; compare catalog ownership and flag discrepancies.
3. Paper 1 is outside this attached Statistics subject syllabus. Do not present Paper 1 content as one of these ten Statistics units.
4. Do not infer missing mathematical symbols from the PDF extraction. The printed PDF should be inspected if the exact symbol matters.
5. A topic is not “covered” merely because a lesson title mentions it. Coverage requires a mapped objective, teaching scene and suitable assessment item, plus relevant PYQ-variant mapping where a bank exists.
6. Do not claim complete syllabus coverage from the index alone. Report uncovered subtopics and source ambiguity explicitly.
