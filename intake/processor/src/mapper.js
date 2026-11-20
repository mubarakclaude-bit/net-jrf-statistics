// Lexical topic mapper; returns suggestions only and uses the Paper 2 seed catalogue.
const terms={
 probability:["probability","distribution","conditional","expectation","variance","moment generating","characteristic function","order statistic","bayes theorem","convergence","clt","jacobian"],
 maths:["matrix","rank","eigen","vector","linear algebra","real analysis","limit","continuity","differentiable"],
 sampling:["sampling","sample survey","stratified","cluster","systematic","population proportion","finite population","srs","sampling variance"],
 design:["design of experiment","factorial","latin square","block","treatment","anova","randomized"],
 inference:["estimator","estimate","likelihood","maximum likelihood","sufficient","complete","cramer","fisher information","confidence interval","bayesian","prior","posterior","method of moments","unbiased","consistent"],
 nonparam:["hypothesis","test statistic","sign test","rank test","wilcoxon","mann-whitney","kolmogorov","nonparametric","power","size"],
 regression:["regression","least squares","blue","residual","leverage","r-squared","heteroscedastic","correlation","gls","estimable"],
 timeseries:["time series","autocorrelation","forecast","arima","stationary","seasonal","trend","moving average"],
 multivariate:["multivariate","principal component","factor analysis","discriminant","canonical","covariance matrix","mahalanobis"],
 stochastic:["markov","poisson process","renewal","queue","birth-death","transition matrix","stochastic process"],
 official:["official statistics","census","national sample","statistical system","economic statistics","methodology"],
 rprog:["r programming","r language","r function","data frame","r studio","programming"]
};
export function mapText(text,catalog){
 const t=text.toLowerCase(),scores=Object.entries(terms).map(([module,words])=>({module,score:words.reduce((s,w)=>s+(t.includes(w)?1:0),0)})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score);
 const allowed=new Set((catalog.modules||[]).filter(m=>m.paper===2).map(m=>m.id));
 const suggestions=scores.filter(x=>allowed.has(x.module)).slice(0,3).map(x=>({...x,topic_ids:(catalog.modules.find(m=>m.id===x.module)?.topics||[]).map(t=>t.id)}));
 return {suggestions,confidence:suggestions.length?"low":"none",warning:"Module-level lexical mapping only. Topic IDs are listed for manual selection; exact topic assignment is not inferred."};
}
