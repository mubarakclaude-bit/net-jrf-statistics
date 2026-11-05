"""Turn the parsed variants into question-bank sets, one per module.

Each parent question of the June 2026 paper is assigned to a module by the
vocabulary of its own variants. Anything the rules cannot place confidently is
put in a 'mixed' set rather than filed under a module it may not belong to.
"""
import json, re, collections, os

V = json.load(open("/tmp/claude-0/variants_raw.json", encoding="utf-8"))
OUT = "/home/claude/w1/seed"

RULES = [
 ("maths",       r"matri|eigen|rank|nullity|trace|determinant|vector space|sherman|frobenius|sylvester|"
                 r"converge|series|sequence|continuous|differentiab|interval of convergence|riemann"),
 ("multivariate",r"principal component|canonical|wishart|hotelling|mahalanobis|discriminant|factor analysis|"
                 r"multivariate normal|equicorrelation|schur complement|\bpc\b|covariance matrix"),
 ("timeseries",  r"\bar\(|\bma\(|arma|arima|autocorrelation|\bacf\b|\bpacf\b|stationar|random walk|"
                 r"spectral|periodogram|yule|white noise|lag\b|trend"),
 ("regression",  r"ols\b|least squares|regression|hat matrix|heterosced|multicollinear|gauss.?markov|"
                 r"residual|r-squared|\bblue\b|\bglsb?\b|durbin|dummy variable|anova"),
 ("sampling",    r"srswor|srswr|stratified|cluster sampl|systematic sampl|ratio estimator|regression estimator|"
                 r"horvitz|yates.{0,3}grundy|des raj|inclusion probab|sampling (?:design|scheme|fraction)|"
                 r"finite population"),
 ("design",      r"randomi[sz]ed block|latin square|factorial (?:design|experiment)|\brbd\b|\bcrd\b|"
                 r"confounding|split.?plot|bibd|main effect|interaction effect|replication"),
 ("nonparam",    r"kendall|spearman|mann.?whitney|wilcoxon|kruskal|sign test|run test|kolmogorov|"
                 r"nonparametric|rank correlation|median test"),
 ("stochastic",  r"markov chain|transition (?:matrix|probab)|poisson process|birth.?death|queue|renewal|"
                 r"branching process|martingale|recurrent|absorbing state|brownian"),
 ("rprog",       r"\bfunction\(|cumsum|\br code\b|\bin r\b|rnorm|data.?frame|\bapply\b|for ?\(i|"
                 r"returns:|\bvector\b.{0,20}\bc\("),
 ("official",    r"census|national income|cpi\b|index number|vital statistics|registrar|nsso|"
                 r"official statistic|price index"),
 ("probability", r"distribution|density|moment generating|characteristic function|expectation|variance of|"
                 r"binomial|poisson|exponential|gamma|beta|chi.?square|order statistic|convergence in|"
                 r"central limit|chebyshev|jensen|conditional expectation|independen"),
 ("inference",   r"estimator|unbiased|sufficien|likelihood|cram[eé]r|rao.?blackwell|lehmann|umvue|"
                 r"neyman|hypothesi|null hypothes|power of|significance|confidence interval|"
                 r"consistent|efficien|bayes|prior|posterior|test\b"),
]

byq = collections.defaultdict(list)
for it in V: byq[it["q"]].append(it)

def classify(q, group):
    blob = " ".join((i["stem"] + " " + " ".join(i["options"])) for i in group).lower()
    best, score = None, 0
    for mod, pat in RULES:
        n = len(re.findall(pat, blob))
        if n > score: best, score = mod, n
    return (best, score) if score >= 2 else (None, score)

assign, unplaced = {}, []
for q, group in byq.items():
    mod, sc = classify(q, group)
    if mod: assign[q] = mod
    else: unplaced.append(q)

print("parent questions placed:", len(assign), " unplaced:", len(unplaced), unplaced or "")
dist = collections.Counter(assign.values())
print("by module:", dict(dist))

# build one set per module, plus a mixed set for the unplaced
sets = collections.defaultdict(list)
n = 0
for q, group in sorted(byq.items()):
    mod = assign.get(q, "mixed")
    for k, it in enumerate(group, 1):
        n += 1
        sets[mod].append({
            "id": "j26v-q%02d-%02d" % (q, k),
            "format": "single",
            "topic": "June 2026 paper · Q%d" % q,
            "stem": it["stem"],
            "options": it["options"],
            "answer": it["answer"],
            "explanation": it["why"],
            "srcQ": q,
        })

written = []
for mod, items in sorted(sets.items()):
    if mod == "mixed":
        mid, label = "inference", "June 2026 paper — practice variants (unclassified)"
        fn = "pyq_variants_mixed"
    else:
        mid, label = mod, "June 2026 paper — practice variants"
        fn = "%s_pyq_variants" % mod
    body = {"moduleId": mid, "source": "variant", "label": label,
            "count": len(items), "items": items}
    p = os.path.join(OUT, fn + ".json")
    json.dump(body, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    written.append((fn, mid, len(items)))

print()
for fn, mid, c in written: print("  %-28s -> module %-13s %3d items" % (fn, mid, c))
print("total items written:", sum(c for _, _, c in written))
