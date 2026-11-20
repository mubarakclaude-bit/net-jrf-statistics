// Lexical topic mapper; suggestions are explicitly unverified.
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
function topicScore(text,topic){const name=(topic.name||"").toLowerCase();const words=name.split(/[^a-z0-9]+/).filter(w=>w.length>3);return words.reduce((s,w)=>s+(text.includes(w)?1:0),0)+((topic.id&&text.includes(topic.id.toLowerCase()))?2:0);}
export function mapText(text,catalog){
 const t=text.toLowerCase(),scores=Object.entries(terms).map(([module,words])=>({module,score:words.reduce((s,w)=>s+(t.includes(w)?1:0),0)})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score);
 const allowed=(catalog.modules||[]).filter(m=>m.paper===2);
 const suggestions=scores.filter(x=>allowed.some(m=>m.id===x.module)).slice(0,3).map(x=>{const m=allowed.find(m=>m.id===x.module);const topics=(m.topics||[]).map(topic=>({id:topic.id,name:topic.name,score:topicScore(t,topic)})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,3);return {...x,topic_candidates:topics};});
 return {suggestions,confidence:suggestions.length?"low":"none",warning:"Lexical module/topic suggestions only; human confirmation required."};
}
