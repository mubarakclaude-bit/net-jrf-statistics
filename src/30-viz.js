/* ===================== visualisations =====================
   Deterministic maths, drawn from the real formulas — no simulation, no decoration.
   Each component: init(cfg) -> state, controls(st) -> sliders, draw(st) -> {svg, read, note}
*/
function lgamma(z){
  if(z<0.5)return Math.log(Math.PI/Math.sin(Math.PI*z))-lgamma(1-z);
  const g=[676.5203681218851,-1259.1392167224028,771.32342877765313,-176.61502916214059,
           12.507343278686905,-0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];
  z-=1;let x=0.99999999999980993;
  for(let i=0;i<8;i++)x+=g[i]/(z+i+1);
  const t=z+7.5;
  return 0.5*Math.log(2*Math.PI)+(z+0.5)*Math.log(t)-t+Math.log(x);
}
const VW=620,VH=210,VP={l:46,r:14,t:14,b:30};
function plot(fn,x0,x1,opts){
  opts=opts||{};
  const N=240,pts=[];let ymax=opts.ymax!==undefined?opts.ymax:-Infinity,ymin=opts.ymin!==undefined?opts.ymin:Infinity;
  for(let i=0;i<=N;i++){const x=x0+(x1-x0)*i/N;let y=fn(x);
    if(!isFinite(y))y=null;pts.push([x,y]);
    if(y!==null&&opts.ymax===undefined&&y>ymax)ymax=y;
    if(y!==null&&opts.ymin===undefined&&y<ymin)ymin=y;}
  if(!isFinite(ymax))ymax=1;if(!isFinite(ymin))ymin=0;
  if(opts.pad)ymax=ymin+(ymax-ymin)*opts.pad;
  if(ymax===ymin)ymax=ymin+1;
  const W=VW-VP.l-VP.r,H=VH-VP.t-VP.b;
  const X=x=>VP.l+W*(x-x0)/(x1-x0), Y=y=>VP.t+H*(1-(y-ymin)/(ymax-ymin));
  let d="",open=false;
  pts.forEach(([x,y])=>{if(y===null){open=false;return}
    d+=(open?"L":"M")+X(x).toFixed(1)+" "+Y(y).toFixed(1)+" ";open=true});
  return {d:d.trim(),X:X,Y:Y,ymin:ymin,ymax:ymax,x0:x0,x1:x1};
}
function axes(p,xlab,ylab,xticks){
  const W=VW-VP.r,H=VH-VP.b;
  let s='<line x1="'+VP.l+'" y1="'+H+'" x2="'+W+'" y2="'+H+'" stroke="var(--line2)" stroke-width="1"/>'+
        '<line x1="'+VP.l+'" y1="'+VP.t+'" x2="'+VP.l+'" y2="'+H+'" stroke="var(--line2)" stroke-width="1"/>';
  (xticks||[]).forEach(t=>{const x=p.X(t);if(x<VP.l-1||x>W+1)return;
    s+='<line x1="'+x.toFixed(1)+'" y1="'+H+'" x2="'+x.toFixed(1)+'" y2="'+(H+4)+'" stroke="var(--line2)"/>'+
       '<text x="'+x.toFixed(1)+'" y="'+(H+16)+'" text-anchor="middle" class="vt">'+(+t.toFixed(2))+'</text>'});
  s+='<text x="'+((VP.l+W)/2)+'" y="'+(VH-2)+'" text-anchor="middle" class="vt">'+esc(xlab)+'</text>';
  s+='<text x="12" y="'+((VP.t+H)/2)+'" text-anchor="middle" class="vt" transform="rotate(-90 12 '+((VP.t+H)/2)+')">'+esc(ylab)+'</text>';
  return s;
}
function vline(p,x,cls,label){
  const px=p.X(x);if(px<VP.l-1||px>VW-VP.r+1)return"";
  return '<line x1="'+px.toFixed(1)+'" y1="'+VP.t+'" x2="'+px.toFixed(1)+'" y2="'+(VH-VP.b)+'" class="'+cls+'"/>'+
    (label?'<text x="'+px.toFixed(1)+'" y="'+(VP.t+10)+'" text-anchor="middle" class="vt vl">'+esc(label)+'</text>':"");
}
function ticks(a,b,k){const o=[];for(let i=0;i<=k;i++)o.push(a+(b-a)*i/k);return o}

const VIZ={};

VIZ["exp-likelihood"]={
 title:"Likelihood of an exponential sample",
 init:c=>({n:c.n||2,S:c.sumx||12,lam:0.1}),
 controls:st=>[
   {k:"n",label:"sample size n",min:1,max:20,step:1,val:st.n,fmt:v=>v},
   {k:"S",label:"Σxᵢ (total of the observations)",min:2,max:60,step:0.5,val:st.S,fmt:v=>v.toFixed(1)},
   {k:"lam",label:"candidate rate λ",min:0.02,max:1.5,step:0.005,val:st.lam,fmt:v=>v.toFixed(3)}],
 draw(st){
   const n=st.n,S=st.S,hat=n/S;
   const lmax=n*Math.log(hat)-n;
   const rel=l=>l<=0?0:Math.exp(n*Math.log(l)-l*S-lmax);
   const ll=l=>l<=0?NaN:n*Math.log(l)-l*S;
   const x1=Math.min(1.5,Math.max(hat*3.2,0.12));
   const p=plot(rel,0.001,x1,{ymin:0,ymax:1.24});
   const tk=ticks(0,x1,5);
   const cur=cl(st.lam,0.001,x1);
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Normalised likelihood against the rate parameter">'+
     axes(p,"candidate rate λ","likelihood ÷ its peak",tk)+
     '<path d="'+p.d+'" class="vcurve"/>'+
     vline(p,hat,"vmark","λ̂ = "+hat.toFixed(3))+
     '<circle cx="'+p.X(cur).toFixed(1)+'" cy="'+p.Y(rel(cur)).toFixed(1)+'" r="4.5" class="vdot"/>'+
     '<line x1="'+p.X(cur).toFixed(1)+'" y1="'+p.Y(rel(cur)).toFixed(1)+'" x2="'+p.X(cur).toFixed(1)+'" y2="'+(VH-VP.b)+'" class="vdrop"/>'+
     '</svg>';
   return {svg:svg,
     read:[["λ̂ = n/Σxᵢ",hat.toFixed(4)],
           ["your λ",cur.toFixed(3)],
           ["likelihood vs peak",(100*rel(cur)).toFixed(1)+"%"],
           ["ℓ(λ) = n·log λ − λΣx",ll(cur).toFixed(3)],
           ["ℓ at the peak",lmax.toFixed(3)]],
     note:cur>hat*1.02?"You are to the right of the peak: this λ says failures should have come sooner than they did."
         :cur<hat*0.98?"You are to the left of the peak: this λ says the bulbs should have lasted longer than they did."
         :"You are at the maximum. No other rate makes this sample more plausible."}
 }};

VIZ["mle-sampling"]={
 title:"Exact sampling distribution of λ̂ = n/ΣX",
 init:c=>({n:c.n||3,lam:c.lam||0.5}),
 controls:st=>[
   {k:"n",label:"sample size n",min:2,max:60,step:1,val:st.n,fmt:v=>v},
   {k:"lam",label:"true rate λ",min:0.2,max:2,step:0.05,val:st.lam,fmt:v=>v.toFixed(2)}],
 draw(st){
   const n=st.n,lam=st.lam;
   // ΣX ~ Gamma(n, rate λ); λ̂ = n/ΣX has density λⁿnⁿ t^(−n−1) e^(−λn/t) / Γ(n)
   const dens=t=>{if(t<=0)return 0;
     const lf=n*Math.log(lam)+n*Math.log(n)-(n+1)*Math.log(t)-lam*n/t-lgamma(n);
     return Math.exp(lf)};
   const mean=n>=2?n*lam/(n-1):NaN;
   const sd=n>=3?n*lam/((n-1)*Math.sqrt(n-2)):NaN;
   const x1=Math.max(lam*3.2,(isFinite(mean)?mean:lam)*2.2);
   const p=plot(dens,0.0001,x1,{ymin:0,pad:1.22});
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Density of the maximum likelihood estimator">'+
     axes(p,"value of λ̂","density",ticks(0,x1,5))+
     '<path d="'+p.d+'" class="vcurve"/>'+
     vline(p,lam,"vmark2","true λ")+
     (isFinite(mean)?vline(p,mean,"vmark3","E[λ̂]"):"")+
     '</svg>';
   const bias=isFinite(mean)?mean-lam:NaN;
   const crsd=lam/Math.sqrt(n);          // √CRLB for an unbiased estimator of λ: CRLB = λ²/n
   const ratio=isFinite(sd)?sd/crsd:NaN;
   return {svg:svg,
     read:[["true λ",lam.toFixed(2)],
           ["E[λ̂] = nλ/(n−1)",isFinite(mean)?mean.toFixed(4):"—"],
           ["bias",isFinite(bias)?"+"+bias.toFixed(4):"—"],
           ["bias as % of λ",isFinite(bias)?(100*bias/lam).toFixed(1)+"%":"—"],
           ["SD of λ̂",isFinite(sd)?sd.toFixed(4):"undefined for n<3"],
           ["√CRLB = λ/√n",crsd.toFixed(4)],
           ["SD ÷ √CRLB",isFinite(ratio)?ratio.toFixed(3):"—"]],
     note:n<=3?"At this sample size the estimator expects to return far more than the truth, and the distribution has a long right tail. Nothing is broken — this is what 'biased' looks like."
         :n<12?"The two lines are closing but still apart, and the shape is clearly skewed. The normal approximation would mislead you here. SD is "+(isFinite(ratio)?ratio.toFixed(2)+"×":"—")+" the Cramér–Rao floor."
         :"Bias under "+(100*bias/lam).toFixed(1)+"% and the shape is nearly symmetric. SD is now "+(isFinite(ratio)?ratio.toFixed(2)+"×":"—")+" the floor and still above it — the MLE approaches the bound without reaching it."}
 }};

VIZ["unif-likelihood"]={
 title:"Likelihood for U(0, θ) — the boundary case",
 init:c=>({n:c.n||5,m:c.xmax||4.2,th:6.0}),
 controls:st=>[
   {k:"n",label:"sample size n",min:1,max:20,step:1,val:st.n,fmt:v=>v},
   {k:"m",label:"largest observation x₍ₙ₎",min:1,max:8,step:0.1,val:st.m,fmt:v=>v.toFixed(1)},
   {k:"th",label:"candidate θ",min:0.5,max:12,step:0.05,val:st.th,fmt:v=>v.toFixed(2)}],
 draw(st){
   const n=st.n,m=st.m;
   const rel=t=>t<m?0:Math.pow(m/t,n);          // normalised so the peak is 1
   const x1=Math.max(12,m*2.2);
   const p=plot(rel,0.01,x1,{ymin:0,ymax:1.24});
   const cur=cl(st.th,0.01,x1);
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Likelihood for the uniform model, a cliff then a decreasing curve">'+
     axes(p,"candidate θ","likelihood ÷ its peak",ticks(0,x1,6))+
     '<path d="'+p.d+'" class="vcurve"/>'+
     vline(p,m,"vmark","θ̂ = x₍ₙ₎ = "+m.toFixed(1))+
     '<circle cx="'+p.X(cur).toFixed(1)+'" cy="'+p.Y(rel(cur)).toFixed(1)+'" r="4.5" class="vdot"/>'+
     '<line x1="'+p.X(cur).toFixed(1)+'" y1="'+p.Y(rel(cur)).toFixed(1)+'" x2="'+p.X(cur).toFixed(1)+'" y2="'+(VH-VP.b)+'" class="vdrop"/>'+
     '</svg>';
   const slope=cur<m?0:-n*Math.pow(m,n)/Math.pow(cur,n+1);
   return {svg:svg,
     read:[["θ̂ = x₍ₙ₎",m.toFixed(2)],
           ["your θ",cur.toFixed(2)],
           ["likelihood vs peak",(100*rel(cur)).toFixed(1)+"%"],
           ["dL/dθ here",cur<m?"0 (L is flat at zero)":slope.toFixed(4)],
           ["E[θ̂] = nθ/(n+1)",(n/(n+1)).toFixed(3)+" × θ"]],
     note:cur<m?"Exactly zero. A θ below your largest observation would have made that observation impossible, so the data rule it out outright."
         :Math.abs(cur-m)<0.06?"You are on the cliff edge. This is the maximum, and the derivative here does not exist — which is why calculus cannot find it."
         :"Still decreasing. The derivative is negative everywhere to the right of the cliff, so setting it to zero can never locate this maximum."}
 }};

/* Two simple hypotheses about a normal mean, with the critical value, α and β drawn.
   The whole Neyman–Pearson trade-off in one picture. */
function nphi(z){ // standard normal cdf, Zelen & Severo 26.2.17 — error < 7.5e-8
  const s=z<0?-1:1,x=Math.abs(z)/Math.SQRT2;
  const t=1/(1+0.3275911*x);
  const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x);
  return 0.5*(1+s*y);
}
function nqnt(p){ // inverse cdf by bisection — exact enough for a drawing, and dependency-free
  let lo=-9,hi=9;
  for(let i=0;i<80;i++){const m=(lo+hi)/2;if(nphi(m)<p)lo=m;else hi=m}
  return (lo+hi)/2;
}
VIZ["np-power"]={
 title:"Two hypotheses, one cut-off: α against power",
 init:c=>({n:c.n||16,d:c.d||1.0,alpha:c.alpha||0.05,sd:c.sd||4}),
 controls:st=>[
   {k:"n",label:"sample size n",min:4,max:120,step:1,val:st.n,fmt:v=>v},
   {k:"d",label:"true gap μ₁ − μ₀",min:0,max:6,step:0.1,val:st.d,fmt:v=>v.toFixed(1)},
   {k:"alpha",label:"size α",min:0.01,max:0.2,step:0.005,val:st.alpha,fmt:v=>v.toFixed(3)}],
 draw(st){
   const se=st.sd/Math.sqrt(st.n);            // standard error of the sample mean
   const c=nqnt(1-st.alpha)*se;               // reject when x̄ − μ₀ > c
   const pow=1-nphi((c-st.d)/se);             // power at the stated gap
   const beta=1-pow;
   const f0=x=>Math.exp(-0.5*(x/se)*(x/se))/(se*Math.sqrt(2*Math.PI));
   const f1=x=>Math.exp(-0.5*((x-st.d)/se)*((x-st.d)/se))/(se*Math.sqrt(2*Math.PI));
   const lo=Math.min(-4*se,st.d-4*se),hi=Math.max(4*se,st.d+4*se);
   const p0=plot(f0,lo,hi,{ymin:0,pad:1.18});
   const p1=plot(f1,lo,hi,{ymin:0,ymax:p0.ymax,pad:1.18});
   const area=(f,a,b)=>{ // filled region under a curve, as a closed path
     const N=90,pts=[];
     for(let i=0;i<=N;i++){const x=a+(b-a)*i/N;pts.push(p0.X(x).toFixed(1)+" "+p0.Y(f(x)).toFixed(1))}
     return "M"+p0.X(a).toFixed(1)+" "+p0.Y(0).toFixed(1)+" L"+pts.join(" L")+
            " L"+p0.X(b).toFixed(1)+" "+p0.Y(0).toFixed(1)+" Z";
   };
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Null and alternative distributions of the sample mean with the rejection region shaded">'+
     axes(p0,"x̄ − μ₀","density",ticks(lo,hi,5))+
     '<path d="'+area(f0,c,hi)+'" class="aErr"/>'+
     '<path d="'+area(f1,lo,c)+'" class="bErr"/>'+
     '<path d="'+p0.d+'" class="vcurve"/>'+
     '<path d="'+p1.d+'" class="vcurve alt"/>'+
     vline(p0,c,"vmark","c")+
     '</svg>';
   return {svg:svg,
     read:[["cut-off c",c.toFixed(3)],
           ["α — reject a true H₀",st.alpha.toFixed(3)],
           ["β — miss a true H₁",beta.toFixed(3)],
           ["power 1 − β",pow.toFixed(3)],
           ["standard error σ/√n",se.toFixed(3)]],
     note:st.d===0?"With no gap at all the two curves coincide, power equals α, and the test cannot tell the hypotheses apart. That is the floor: a test is never worse than its own size."
       :pow<0.5?"Power under 50%: this test is more likely to miss the effect than to find it. Raise n, or accept a larger α — the red and blue areas trade against each other and cannot both shrink at fixed n."
       :pow<0.8?"Power climbing but under the 80% convention. Notice α is unchanged — only n and the gap move power."
       :"Power above 80%. The curves have separated far enough that one cut-off serves both errors well."}
 }};

/* ---- further helpers: the chi-square family, and log binomial coefficients ---- */
function gammap(s,x){ // regularised lower incomplete gamma P(s,x); series below s+1, continued fraction above
  if(x<=0)return 0;
  if(x<s+1){                                   // Abramowitz & Stegun 6.5.29 series
    let sum=1/s,term=sum;
    for(let k=1;k<300;k++){term*=x/(s+k);sum+=term;if(term<sum*1e-15)break}
    return sum*Math.exp(-x+s*Math.log(x)-lgamma(s));
  }
  let b=x+1-s,c=1e300,d=1/b,h=d;               // Lentz's continued fraction for Q(s,x)
  for(let i=1;i<300;i++){
    const an=-i*(i-s);b+=2;
    d=an*d+b;if(Math.abs(d)<1e-300)d=1e-300;
    c=b+an/c;if(Math.abs(c)<1e-300)c=1e-300;
    d=1/d;const del=d*c;h*=del;
    if(Math.abs(del-1)<1e-15)break;
  }
  return 1-Math.exp(-x+s*Math.log(x)-lgamma(s))*h;
}
function chi2cdf(x,k){return x<=0?0:gammap(k/2,x/2)}
function chi2pdf(x,k){return x<=0?0:Math.exp((k/2-1)*Math.log(x)-x/2-lgamma(k/2)-(k/2)*Math.LN2)}
function chi2qnt(p,k){ // bisection; the range is generous enough for the df this app uses
  let lo=0,hi=Math.max(40,4*k+40);
  for(let i=0;i<120;i++){const m=(lo+hi)/2;if(chi2cdf(m,k)<p)lo=m;else hi=m}
  return (lo+hi)/2;
}
function lchoose(n,k){return lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)}
function binpmf(k,n,p){
  if(p<=0)return k===0?1:0;
  if(p>=1)return k===n?1:0;
  return Math.exp(lchoose(n,k)+k*Math.log(p)+(n-k)*Math.log(1-p));
}

/* A conjugate pair, drawn: a Beta prior meets a binomial sample and the posterior
   sits between the prior mean and the MLE. The whole of 4.7 in one picture. */
VIZ["beta-posterior"]={
 title:"Beta prior × binomial likelihood = Beta posterior",
 init:c=>({a:c.a||2,b:c.b||2,n:c.n||10,x:c.x===undefined?7:c.x}),
 controls:st=>[
   {k:"a",label:"prior α (prior successes + 1)",min:0.5,max:20,step:0.5,val:st.a,fmt:v=>v.toFixed(1)},
   {k:"b",label:"prior β (prior failures + 1)",min:0.5,max:20,step:0.5,val:st.b,fmt:v=>v.toFixed(1)},
   {k:"n",label:"sample size n",min:1,max:60,step:1,val:st.n,fmt:v=>v},
   {k:"x",label:"successes observed x",min:0,max:60,step:1,val:st.x,fmt:v=>v}],
 draw(st){
   const n=st.n,x=Math.min(st.x,n),a=st.a,b=st.b;
   const A=a+x,B=b+n-x;                        // the conjugate update, in one line
   const bden=(p,u,v)=>p<=0||p>=1?0:Math.exp((u-1)*Math.log(p)+(v-1)*Math.log(1-p)+lgamma(u+v)-lgamma(u)-lgamma(v));
   const prior=p=>bden(p,a,b), post=p=>bden(p,A,B);
   const mle=n?x/n:0.5, pm=a/(a+b), postm=A/(A+B);
   // the likelihood, rescaled to the plot so its shape can be compared with the two densities
   const lik=p=>binpmf(x,n,p);
   let lmax=0;for(let i=1;i<200;i++){const v=lik(i/200);if(v>lmax)lmax=v}
   const pp=plot(post,0,1,{ymin:0,pad:1.12});
   const pr=plot(prior,0,1,{ymin:0,ymax:pp.ymax});
   const pl=plot(p=>lmax?lik(p)/lmax*pp.ymax*0.92:0,0,1,{ymin:0,ymax:pp.ymax});
   const w=(a+b)/(a+b+n);                      // weight the posterior mean puts on the prior mean
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Beta prior, rescaled binomial likelihood and Beta posterior densities on the unit interval">'+
     axes(pp,"θ","density",ticks(0,1,5))+
     '<path d="'+pr.d+'" class="vcurve alt"/>'+
     '<path d="'+pl.d+'" class="vcurve aux"/>'+
     '<path d="'+pp.d+'" class="vcurve"/>'+
     vline(pp,pm,"vmark alt","prior mean")+
     vline(pp,mle,"vmark aux","MLE")+
     vline(pp,postm,"vmark","posterior mean")+
     '</svg>';
   return {svg:svg,
     read:[["posterior","Beta("+A.toFixed(1)+", "+B.toFixed(1)+")"],
           ["prior mean a/(a+b)",pm.toFixed(4)],
           ["MLE x/n",mle.toFixed(4)],
           ["posterior mean A/(A+B)",postm.toFixed(4)],
           ["weight on the prior mean",w.toFixed(4)],
           ["posterior mode (A,B>1)",(A>1&&B>1)?((A-1)/(A+B-2)).toFixed(4):"—"]],
     note:Math.abs(a-1)<1e-9&&Math.abs(b-1)<1e-9
       ?"With α = β = 1 the prior is uniform and contributes nothing but a count of one success and one failure: the posterior mode equals the MLE exactly, which is the sense in which a flat prior recovers maximum likelihood."
       :w>0.5?"The prior still outweighs the data: a + b exceeds n, so the posterior mean sits nearer the prior mean than the MLE. Raise n and watch the weight fall."
       :w<0.1?"The data have taken over. The posterior mean is within a whisker of the MLE, which is what consistency of the Bayes estimator means in practice — the prior washes out."
       :"The posterior mean is a weighted average of the prior mean and the MLE, with weight (a+b)/(a+b+n) on the prior. Every conjugate pair in the syllabus has a formula of exactly this shape."}
 }};

/* The chi-square tail: one density, one critical value, one observed statistic.
   Serves the likelihood ratio test, goodness of fit and contingency tables alike. */
VIZ["chisq-tail"]={
 title:"Chi-square: degrees of freedom, critical value and p-value",
 init:c=>({k:c.k||3,alpha:c.alpha||0.05,obs:c.obs===undefined?7.8:c.obs}),
 controls:st=>[
   {k:"k",label:"degrees of freedom",min:1,max:30,step:1,val:st.k,fmt:v=>v},
   {k:"alpha",label:"size α",min:0.005,max:0.2,step:0.005,val:st.alpha,fmt:v=>v.toFixed(3)},
   {k:"obs",label:"observed statistic",min:0,max:60,step:0.1,val:st.obs,fmt:v=>v.toFixed(1)}],
 draw(st){
   const k=st.k,crit=chi2qnt(1-st.alpha,k),pval=1-chi2cdf(st.obs,k);
   const hi=Math.max(crit*1.6,st.obs*1.25,chi2qnt(0.999,k));
   const f=x=>chi2pdf(x,k);
   const p=plot(f,0,hi,{ymin:0,pad:1.15});
   const area=(a,b)=>{const N=110,pts=[];
     for(let i=0;i<=N;i++){const x=a+(b-a)*i/N;pts.push(p.X(x).toFixed(1)+" "+p.Y(f(x)).toFixed(1))}
     return "M"+p.X(a).toFixed(1)+" "+p.Y(0).toFixed(1)+" L"+pts.join(" L")+" L"+p.X(b).toFixed(1)+" "+p.Y(0).toFixed(1)+" Z"};
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Chi-square density with the rejection region and the observed statistic marked">'+
     axes(p,"statistic","density",ticks(0,hi,5))+
     '<path d="'+area(crit,hi)+'" class="aErr"/>'+
     '<path d="'+p.d+'" class="vcurve"/>'+
     vline(p,crit,"vmark","χ²"+String.fromCharCode(0x2090)+" crit")+
     vline(p,st.obs,"vmark aux","observed")+
     '</svg>';
   return {svg:svg,
     read:[["degrees of freedom",k],
           ["critical value at α",crit.toFixed(3)],
           ["observed statistic",st.obs.toFixed(3)],
           ["p-value",pval<1e-4?"< 0.0001":pval.toFixed(4)],
           ["mean of the null distribution",k],
           ["standard deviation √(2k)",Math.sqrt(2*k).toFixed(3)],
           ["decision at α",st.obs>crit?"reject H₀":"do not reject H₀"]],
     note:st.obs>crit
       ?"The observed value is in the shaded tail, so H₀ is rejected at this α. Raise the degrees of freedom and the critical value rises with them — the same statistic can be significant on few df and unremarkable on many."
       :st.obs<k*0.3
       ?"Far into the left of the distribution: the fit is closer than chance would normally produce. A chi-square that is suspiciously small is worth a second look at the model, not a celebration — it can mean the expected frequencies were fitted to the data."
       :"The observed value lies outside the rejection region. Note that the null distribution has mean k and standard deviation √(2k), so a statistic near its degrees of freedom is exactly what H₀ predicts."}
 }};

/* Risk as a function of the parameter, for three estimators of a normal mean.
   Admissibility and the minimax criterion both become visible in one frame. */
VIZ["risk-curves"]={
 title:"Risk functions: what admissible and minimax actually look like",
 init:c=>({n:c.n||9,sd:c.sd||3,m:c.m===undefined?0:c.m,w:c.w===undefined?0.5:c.w}),
 controls:st=>[
   {k:"n",label:"sample size n",min:1,max:60,step:1,val:st.n,fmt:v=>v},
   {k:"m",label:"the constant guess, and the shrinkage target",min:-4,max:4,step:0.1,val:st.m,fmt:v=>v.toFixed(1)},
   {k:"w",label:"shrinkage weight on the sample mean",min:0,max:1,step:0.02,val:st.w,fmt:v=>v.toFixed(2)}],
 draw(st){
   const v=st.sd*st.sd/st.n;                   // variance of the sample mean
   // squared-error risk = variance + bias²
   const rMean=()=>v;                                           // x̄: unbiased, constant risk
   const rConst=th=>(th-st.m)*(th-st.m);                        // ignore the data entirely
   const rShrink=th=>st.w*st.w*v+(1-st.w)*(1-st.w)*(th-st.m)*(th-st.m);
   const lo=st.m-4*Math.sqrt(v)-1,hi=st.m+4*Math.sqrt(v)+1;
   let ymax=v*1.1;for(let i=0;i<=120;i++){const th=lo+(hi-lo)*i/120;ymax=Math.max(ymax,rShrink(th))}
   ymax=Math.min(ymax,v*4);
   const pM=plot(rMean,lo,hi,{ymin:0,ymax:ymax});
   const pC=plot(rConst,lo,hi,{ymin:0,ymax:ymax});
   const pS=plot(rShrink,lo,hi,{ymin:0,ymax:ymax});
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Risk functions of the sample mean, a constant estimator and a shrinkage estimator against the parameter">'+
     axes(pM,"θ","risk  E(θ̂ − θ)²",ticks(lo,hi,5))+
     '<path d="'+pC.d+'" class="vcurve alt"/>'+
     '<path d="'+pS.d+'" class="vcurve aux"/>'+
     '<path d="'+pM.d+'" class="vcurve"/>'+
     vline(pM,st.m,"vmark alt","target m")+
     '</svg>';
   const sup=Math.max(rShrink(lo),rShrink(hi));
   return {svg:svg,
     read:[["risk of x̄, at every θ",v.toFixed(4)],
           ["risk of the constant m, at θ = m","0.0000"],
           ["risk of the shrinkage rule at θ = m",(st.w*st.w*v).toFixed(4)],
           ["its risk at the edge of the frame",sup.toFixed(4)],
           ["worst-case risk of x̄ (minimax value)",v.toFixed(4)]],
     note:st.w>=0.999
       ?"At weight 1 the shrinkage rule IS the sample mean: flat risk, equal to σ²/n everywhere. That flat line is what makes x̄ minimax — no other rule has a smaller worst case over the whole line."
       :st.w<=0.001
       ?"At weight 0 the rule ignores the data and always answers m. Its risk is zero when θ happens to equal m and unbounded as θ moves away. Unbeatable at one point, catastrophic elsewhere — which is why no estimator dominates another everywhere."
       :"The shrinkage rule beats x̄ near the target and loses to it far away, so neither dominates: both are admissible. But its worst case over the whole line is larger, so x̄ is the minimax choice. Admissible and minimax are different questions, and this picture is the difference."}
 }};

/* The SPRT's two boundaries, with the log-likelihood-ratio path that a given
   observed success rate would trace. Shows why the stopping time is random. */
VIZ["sprt"]={
 title:"The SPRT: two boundaries and a random walk between them",
 init:c=>({p0:c.p0||0.3,p1:c.p1||0.6,alpha:c.alpha||0.05,beta:c.beta||0.1,phat:c.phat===undefined?0.45:c.phat}),
 controls:st=>[
   {k:"p0",label:"p₀ under H₀",min:0.05,max:0.9,step:0.01,val:st.p0,fmt:v=>v.toFixed(2)},
   {k:"p1",label:"p₁ under H₁",min:0.1,max:0.95,step:0.01,val:st.p1,fmt:v=>v.toFixed(2)},
   {k:"alpha",label:"α",min:0.01,max:0.2,step:0.005,val:st.alpha,fmt:v=>v.toFixed(3)},
   {k:"beta",label:"β",min:0.01,max:0.3,step:0.005,val:st.beta,fmt:v=>v.toFixed(3)},
   {k:"phat",label:"observed success rate in the data",min:0,max:1,step:0.01,val:st.phat,fmt:v=>v.toFixed(2)}],
 draw(st){
   const p0=st.p0,p1=Math.max(st.p1,st.p0+0.01),al=st.alpha,be=st.beta;
   const A=Math.log((1-be)/al), B=Math.log(be/(1-al));          // accept H₁ above A, accept H₀ below B
   // each observation adds log(p1/p0) for a success and log((1-p1)/(1-p0)) for a failure
   const gs=Math.log(p1/p0), gf=Math.log((1-p1)/(1-p0));
   const drift=st.phat*gs+(1-st.phat)*gf;                       // expected step at the observed rate
   const nmax=Math.max(10,Math.ceil(Math.max(Math.abs(A),Math.abs(B))/Math.max(1e-6,Math.abs(drift)))*1.6);
   const path=n=>n*drift;
   const p=plot(path,0,nmax,{ymin:Math.min(B,0)*1.35-0.2,ymax:Math.max(A,0)*1.35+0.2});
   const hline=(y,cls,lab)=>{const py=p.Y(y);
     return '<line x1="'+VP.l+'" y1="'+py.toFixed(1)+'" x2="'+(VW-VP.r)+'" y2="'+py.toFixed(1)+'" class="'+cls+'"/>'+
            '<text x="'+(VW-VP.r-4)+'" y="'+(py-4).toFixed(1)+'" text-anchor="end" class="vt vl">'+esc(lab)+'</text>'};
   const hit=Math.abs(drift)<1e-9?null:(drift>0?A/drift:B/drift);
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Cumulative log likelihood ratio against sample size, with the SPRT acceptance and rejection boundaries">'+
     axes(p,"observations n","cumulative log likelihood ratio",ticks(0,nmax,5))+
     hline(A,"vhline","accept H₁  (A)")+
     hline(B,"vhline alt","accept H₀  (B)")+
     '<path d="'+p.d+'" class="vcurve"/>'+
     (hit!==null&&hit>0&&hit<nmax?vline(p,hit,"vmark","stop"):"")+
     '</svg>';
   return {svg:svg,
     read:[["upper boundary A = log((1−β)/α)",A.toFixed(4)],
           ["lower boundary B = log(β/(1−α))",B.toFixed(4)],
           ["step on a success",gs.toFixed(4)],
           ["step on a failure",gf.toFixed(4)],
           ["expected step at the observed rate",drift.toFixed(4)],
           ["n at which the path would stop",hit===null||hit<=0?"never":Math.ceil(hit)],
           ["decision it would reach",Math.abs(drift)<1e-9?"neither":(drift>0?"H₁":"H₀")]],
     note:Math.abs(drift)<0.004
       ?"The expected step is almost zero, so the path drifts nowhere and the test can run a very long time. This is the SPRT's real weakness: the sample size is random and, at a rate between p₀ and p₁, its expectation can be large."
       :drift>0
       ?"The path rises towards A, so this success rate accumulates evidence for H₁ and the test stops as soon as the boundary is crossed — typically on a smaller sample than a fixed-n test of the same α and β, which is the whole point of sequential testing."
       :"The path falls towards B, accumulating evidence for H₀. Note that both boundaries depend only on α and β, not on the data: Wald's approximation is what makes the SPRT usable with no distribution theory at the boundary."}
 }};

/* Nominal against actual coverage for a binomial proportion. The honest picture of
   what a stated confidence level does and does not guarantee. */
VIZ["ci-coverage"]={
 title:"Stated confidence against actual coverage",
 init:c=>({n:c.n||30,conf:c.conf||0.95,p:c.p===undefined?0.2:c.p}),
 controls:st=>[
   {k:"n",label:"sample size n",min:5,max:120,step:1,val:st.n,fmt:v=>v},
   {k:"conf",label:"stated confidence level",min:0.8,max:0.995,step:0.005,val:st.conf,fmt:v=>(v*100).toFixed(1)+"%"},
   {k:"p",label:"the true p to read off",min:0.01,max:0.99,step:0.01,val:st.p,fmt:v=>v.toFixed(2)}],
 draw(st){
   const n=st.n,z=nqnt(1-(1-st.conf)/2);
   // exact coverage of the Wald interval: sum the binomial probabilities of every x whose interval covers p
   const cover=p=>{let s=0;
     for(let x=0;x<=n;x++){const ph=x/n,se=Math.sqrt(ph*(1-ph)/n);
       if(p>=ph-z*se&&p<=ph+z*se)s+=binpmf(x,n,p)}
     return s};
   const p=plot(cover,0.01,0.99,{ymin:0,ymax:1.04});
   const at=cover(st.p);
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Actual coverage probability of the Wald interval for a binomial proportion against the true proportion, with the stated level marked">'+
     axes(p,"true p","actual coverage",ticks(0,1,5))+
     '<line x1="'+VP.l+'" y1="'+p.Y(st.conf).toFixed(1)+'" x2="'+(VW-VP.r)+'" y2="'+p.Y(st.conf).toFixed(1)+'" class="vhline alt"/>'+
     '<path d="'+p.d+'" class="vcurve"/>'+
     vline(p,st.p,"vmark aux","p")+
     '</svg>';
   let worst=1;for(let i=1;i<99;i++){const c=cover(i/100);if(c<worst)worst=c}
   return {svg:svg,
     read:[["stated level",(st.conf*100).toFixed(1)+"%"],
           ["z for that level",z.toFixed(4)],
           ["actual coverage at this p",(at*100).toFixed(1)+"%"],
           ["worst coverage over p",(worst*100).toFixed(1)+"%"],
           ["shortfall at this p",((st.conf-at)*100).toFixed(1)+" points"]],
     note:at<st.conf-0.02
       ?"Actual coverage is materially below the stated level at this p. A confidence level is a property of the PROCEDURE under repeated sampling, and for a discrete distribution it is only approximate — here the approximation is failing."
       :worst<st.conf-0.05
       ?"Coverage is close to the stated level at the p you have selected, but drag p towards 0 or 1 and it collapses. The guarantee is not uniform in p, which is why the Wald interval is not recommended near the boundaries."
       :"Coverage tracks the stated level reasonably across p at this sample size. The sawtooth is inherent: a discrete statistic cannot deliver an exactly 95% interval for every p, so the level is attained only approximately."}
 }};

/* The ACF and PACF of an AR(1) or AR(2), drawn from the recursions rather than simulated.
   Serves the whole time-series module: geometric decay, the sign alternation a negative
   coefficient produces, the PACF cut-off that identifies the order, and the boundary of the
   stationarity triangle, where the ACF ceases to exist at all. */
VIZ["ar-acf"]={
 title:"The ACF of an AR process: decay, alternation and the stationarity boundary",
 init:c=>({p1:c.p1===undefined?0.8:c.p1,p2:c.p2===undefined?0:c.p2,K:c.K||14}),
 controls:st=>[
   {k:"p1",label:"φ₁",min:-1.9,max:1.9,step:0.05,val:st.p1,fmt:v=>v.toFixed(2)},
   {k:"p2",label:"φ₂  (set to 0 for an AR(1))",min:-0.95,max:0.95,step:0.05,val:st.p2,fmt:v=>v.toFixed(2)}],
 draw(st){
   const p1=st.p1,p2=st.p2,K=st.K;
   // the three AR(2) stationarity conditions; an AR(1) is the p2 = 0 slice of the same triangle
   const c1=p1+p2<1, c2=p2-p1<1, c3=Math.abs(p2)<1, stat=c1&&c2&&c3;
   const sum=p1+p2;
   const W=VW-VP.l-VP.r, H=VH-VP.t-VP.b;
   const x0=0,x1=K,ymin=-1.08,ymax=1.08;
   const X=x=>VP.l+W*(x-x0)/(x1-x0), Y=y=>VP.t+H*(1-(y-ymin)/(ymax-ymin));
   const p={X:X,Y:Y,ymin:ymin,ymax:ymax,x0:x0,x1:x1,d:""};
   const zero='<line x1="'+VP.l+'" y1="'+Y(0).toFixed(1)+'" x2="'+(VW-VP.r)+'" y2="'+Y(0).toFixed(1)+
              '" stroke="var(--line2)" stroke-width="1"/>';
   const frame=axes(p,"lag k","ρ(k)",ticks(0,K,7));
   if(!stat){
     // No ACF exists: say so on the chart rather than drawing a sequence that does not converge.
     const fail=!c1?"φ₁ + φ₂ = "+sum.toFixed(2)+(Math.abs(sum-1)<1e-9?" — a unit root":" ≥ 1")
                :!c2?"φ₂ − φ₁ = "+(p2-p1).toFixed(2)+" ≥ 1":"|φ₂| = "+Math.abs(p2).toFixed(2)+" ≥ 1";
     const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="No autocorrelation function: the process is not stationary">'+
       frame+zero+
       '<text x="'+(VP.l+W/2)+'" y="'+(VP.t+H/2-6)+'" text-anchor="middle" class="vt vl" style="font-size:13px">'+
         'not stationary — no ACF exists</text>'+
       '<text x="'+(VP.l+W/2)+'" y="'+(VP.t+H/2+12)+'" text-anchor="middle" class="vt">'+esc(fail)+'</text>'+
       '</svg>';
     return {svg:svg,
       read:[["φ₁",p1.toFixed(2)],["φ₂",p2.toFixed(2)],["φ₁ + φ₂",sum.toFixed(2)],
             ["φ₁ + φ₂ < 1",c1?"yes":"NO"],["φ₂ − φ₁ < 1",c2?"yes":"NO"],["|φ₂| < 1",c3?"yes":"NO"],
             ["stationary",'no']],
       note:Math.abs(sum-1)<1e-9
         ?"The coefficients sum to exactly 1, so z = 1 is a root of the AR polynomial — a unit root. The variance grows without limit and there is no autocorrelation function to draw. Factor out (1 − B) and the DIFFERENCED series has an ACF; that is the whole content of the unit-roots topic."
         :"At least one stationarity condition fails, so no autocorrelation function exists. Note that it is not enough to keep |φ₁| below 1: the three conditions act together, and φ₁ may legitimately reach 2 provided φ₂ compensates."}
   }
   const r=[1,p1/(1-p2)];
   for(let k=2;k<=K;k++)r.push(p1*r[k-1]+p2*r[k-2]);
   // Durbin-Levinson: the last coefficient at each order IS the partial autocorrelation
   const pac=[];let prev=[];
   for(let k=1;k<=4;k++){
     let pkk;
     if(k===1)pkk=r[1];
     else{let num=r[k],den=1;
       for(let j=1;j<k;j++){num-=prev[j-1]*r[k-j];den-=prev[j-1]*r[j]}
       pkk=Math.abs(den)>1e-12?num/den:0}
     const cur=new Array(k).fill(0);cur[k-1]=pkk;
     for(let j=1;j<k;j++)cur[j-1]=prev[j-1]-pkk*prev[k-j-1];
     prev=cur;pac.push(pkk)}
   let stems="",dots="";
   for(let k=0;k<=K;k++){
     const x=X(k).toFixed(1);
     stems+="M"+x+" "+Y(0).toFixed(1)+"L"+x+" "+Y(r[k]).toFixed(1)+" ";
     dots+='<circle cx="'+x+'" cy="'+Y(r[k]).toFixed(1)+'" r="3" class="vdot"/>'}
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Autocorrelation function of an autoregressive process, drawn as stems at each lag">'+
     frame+zero+
     '<path d="'+stems.trim()+'" class="vcurve"/>'+dots+
     '</svg>';
   const alt=r[1]<0||(r[1]>0&&r[2]<0);
   const half=(()=>{for(let k=1;k<=K;k++)if(Math.abs(r[k])<0.05)return k;return null})();
   return {svg:svg,
     read:[["φ₁",p1.toFixed(2)],["φ₂",p2.toFixed(2)],
           ["ρ₁",r[1].toFixed(4)],["ρ₂",r[2].toFixed(4)],["ρ₃",r[3].toFixed(4)],
           ["PACF at lag 1",pac[0].toFixed(4)],
           ["PACF at lag 2",pac[1].toFixed(4)],
           ["PACF at lag 3",Math.abs(pac[2])<5e-5?"0.0000":pac[2].toFixed(4)],
           ["Var(yₜ)/σ²ε  (AR(1) only)",Math.abs(p2)<1e-9?(1/(1-p1*p1)).toFixed(4):"—"],
           ["first lag with |ρ| < 0.05",half===null?"beyond "+K:half]],
     note:Math.abs(p2)<1e-9&&p1<0
       ?"An AR(1) with a negative coefficient: the ACF alternates in sign while its magnitudes decay as |φ₁|ᵏ. The even lags are positive — ρ₂ = φ₁² — which is why a negative coefficient does not mean negative correlation at every lag. This is the pattern June 2026 Q18 turned on."
       :Math.abs(p2)<1e-9
       ?"An AR(1): one coefficient determines the whole ACF, ρₖ = φ₁ᵏ, decaying geometrically. Read the PACF below — it is non-zero at lag 1 and zero beyond, which is the signature that identifies the order as 1."
       :sum>0.93
       ?"Close to the stationarity boundary. The ACF decays so slowly that a sample of moderate length would be hard to distinguish from a unit-root series — which is exactly why the Dickey–Fuller test has little power against a φ near 1. Push the sum to 1 and the ACF disappears."
       :alt
       ?"A mixed-sign ACF. With φ₂ negative the recursion ρₖ = φ₁ρₖ₋₁ + φ₂ρₖ₋₂ can drive the sequence below zero and back, so the ACF need not be monotone. The PACF still cuts off after lag 2, which is how the order is identified whatever the ACF looks like."
       :"An AR(2): the ACF follows the recursion ρₖ = φ₁ρₖ₋₁ + φ₂ρₖ₋₂ from ρ₀ = 1 and ρ₁ = φ₁/(1 − φ₂). Note the PACF below — it returns φ₁ and φ₂ at lags 1 and 2 and is zero at lag 3, which is both the identification rule and a check on the Yule–Walker solution."}
 }};

VIZ["r-null"]={
 title:"The sampling distribution of r: U-shaped at n = 3, flat at n = 4, skewed when ρ is large",
 init:c=>({n:c.n||4,rho:c.rho===undefined?0:c.rho}),
 controls:st=>[
   {k:"n",label:"sample size n (pairs)",min:3,max:60,step:1,val:st.n,fmt:v=>v},
   {k:"rho",label:"true ρ  (0 = the null density, exact)",min:-0.95,max:0.95,step:0.05,val:st.rho,fmt:v=>v.toFixed(2)}],
 draw(st){
   const n=Math.round(st.n), rho=st.rho, e=(n-4)/2;
   // exact null density of r: c(n)(1-r^2)^((n-4)/2); (1+r)/2 ~ Beta((n-2)/2,(n-2)/2)
   const lc=lgamma((n-1)/2)-0.5*Math.log(Math.PI)-lgamma((n-2)/2), C=Math.exp(lc);
   const f0=r=>{const u=1-r*r; if(u<=0) return e<0?0:(e===0?C:0); return C*Math.exp(e*Math.log(u));};
   // 5% two-sided critical |r|, by bisecting the exact null cdf (Simpson, 2000 panels)
   // Integrate under r = sin(theta): f(r)dr = C cos^(n-3)(theta) dtheta, smooth for every n >= 3
   // (at n = 3 the exponent is 0, i.e. theta is uniform — which IS the arcsine law for r).
   const cdf=x=>{const a=-Math.PI/2,b=Math.asin(Math.max(-1,Math.min(1,x))); if(b<=a) return 0;
     const g=th=>C*Math.pow(Math.cos(th),n-3), m=2000,h=(b-a)/m; let s=g(a)+g(b);
     for(let i=1;i<m;i++) s+=g(a+i*h)*(i%2?4:2); return s*h/3;};
   let lo=0,hi=1-1e-9; for(let i=0;i<60;i++){const mid=(lo+hi)/2; if(cdf(mid)<0.975) lo=mid; else hi=mid;}
   const rc=(lo+hi)/2;
   const shape = n===3?"U-shaped (arcsine)" : n===4?"flat — Uniform(−1, 1)" : n===5?"semicircle" : "unimodal, bell-like";
   const L=0.995;
   const p0=plot(f0,-L,L,{ymin:0,pad:1.15});
   let parts='<path d="'+p0.d+'" class="vcurve"/>', read=[
     ["shape of the null density", shape],
     ["Var(r) when ρ = 0", "1/(n−1) = "+(1/(n-1)).toFixed(4)],
     ["5% two-sided critical |r|", rc.toFixed(4)]];
   let note="At ρ = 0 the density is exactly c(n)(1 − r²)^((n−4)/2), so the exponent (n−4)/2 decides the shape: negative at n = 3 gives the U-shaped arcsine, zero at n = 4 gives a flat Uniform(−1, 1), positive from n = 5 on gives a single peak at 0. Substituting u = (1 + r)/2 turns all three into one fact: u is Beta((n−2)/2, (n−2)/2).";
   if(n>=5 && Math.abs(rho)>1e-9){
     // Fisher's z is near-normal, so r = tanh(Z) with Z ~ N(atanh rho, 1/(n-3)):
     // a symmetric density in z, pushed into a skewed one in r because tanh compresses near +/-1
     const s=1/Math.sqrt(n-3), ze=0.5*Math.log((1+rho)/(1-rho));
     const fz=r=>{const u=1-r*r; if(u<=1e-12) return 0; const z=0.5*Math.log((1+r)/(1-r));
       return Math.exp(-(z-ze)*(z-ze)/(2*s*s))/(Math.sqrt(2*Math.PI)*s*u);};
     const pz=plot(fz,-L,L,{ymin:0,ymax:Math.max(p0.ymax,0)});
     parts+='<path d="'+pz.d+'" class="vcurve alt"/>'+vline(p0,rho,"vmark alt","ρ");
     read.push(["Fisher's z of ρ", ze.toFixed(4)+"  (sd "+s.toFixed(4)+")"]);
     note="The teal curve is the density of r when ρ = "+rho.toFixed(2)+", obtained from Fisher's z: z = ½ln((1+r)/(1−r)) is near-normal with mean ½ln((1+ρ)/(1−ρ)) and variance 1/(n−3), and r = tanh(z). The curve is skewed even though the density of z is symmetric, because tanh squeezes the upper tail against the hard boundary at 1 — which is why the skew grows as ρ approaches 1, and why z, not r, is the right scale for a confidence interval.";
   }
   parts+=vline(p0,rc,"vmark","+r crit")+vline(p0,-rc,"vmark","−r crit");
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Density of the sample correlation coefficient on minus one to one, with the five percent critical values marked">'+
     axes(p0,"r","density",ticks(-1,1,5))+parts+'</svg>';
   return {svg:svg, read:read, note:note};
 }};

VIZ["ord-beta"]={
 title:"Order statistics from U(0, 1): each one is a Beta, evenly spaced and unequally spread",
 init:c=>{const n=c.n||5; return {n:n, r:Math.min(c.r||Math.ceil(n/2),n)};},
 controls:st=>[
   {k:"n",label:"sample size n",min:2,max:30,step:1,val:st.n,fmt:v=>v},
   {k:"r",label:"which order statistic, r  (1 = smallest, n = largest)",
    min:1,max:st.n,step:1,val:Math.min(st.r,st.n),fmt:v=>v}],
 draw(st){
   const n=Math.round(st.n), r=Math.max(1,Math.min(Math.round(st.r),n));
   // X_(r) ~ Beta(r, n-r+1); mean r/(n+1), var r(n-r+1)/((n+1)^2 (n+2))
   const bd=(x,a,b)=>x<=0||x>=1?0:Math.exp((a-1)*Math.log(x)+(b-1)*Math.log(1-x)
                                            +lgamma(a+b)-lgamma(a)-lgamma(b));
   const A=r,B=n-r+1;
   const f=x=>bd(x,A,B), fmin=x=>bd(x,1,n), fmax=x=>bd(x,n,1);
   const mean=r/(n+1), vr=r*(n-r+1)/((n+1)*(n+1)*(n+2));
   const med=Math.ceil(n/2), vmed=med*(n-med+1)/((n+1)*(n+1)*(n+2));
   const vend=1*n/((n+1)*(n+1)*(n+2));
   const p=plot(f,0,1,{ymin:0,pad:1.12});
   let parts='<path d="'+p.d+'" class="vcurve"/>';
   if(r!==1) parts+='<path d="'+plot(fmin,0,1,{ymin:0,ymax:p.ymax}).d+'" class="vcurve aux"/>';
   if(r!==n) parts+='<path d="'+plot(fmax,0,1,{ymin:0,ymax:p.ymax}).d+'" class="vcurve alt"/>';
   parts+=vline(p,mean,"vmark","E = "+mean.toFixed(3));
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Density of the r-th order statistic from a uniform sample on the unit interval, with the smallest and largest shown faintly for contrast">'+
     axes(p,"x","density",ticks(0,1,5))+parts+'</svg>';
   return {svg:svg,
     read:[["distribution of X₍"+r+"₎","Beta("+A+", "+B+")"],
           ["mean  r/(n+1)",mean.toFixed(4)],
           ["variance",vr.toFixed(5)],
           ["spacing between consecutive means","1/(n+1) = "+(1/(n+1)).toFixed(4)]],
     note:"X₍ᵣ₎ ~ Beta(r, n − r + 1), so its mean is r/(n+1): the n order statistics sit at equally spaced points 1/(n+1) apart, whatever n is. The spread is NOT equal, and for the uniform it runs the way most people expect backwards — the variance "+
       vmed.toFixed(5)+" at the middle exceeds "+vend.toFixed(5)+" at either end, because the uniform has hard boundaries at 0 and 1 that pin the extremes down while the middle is free to move. For a normal population the ordering reverses, since its tails are unbounded. Move r from 1 to n and watch the peak sweep across while the shape turns from a decaying curve, through symmetric, to a rising one."};
 }};

VIZ["disc-pmf"]={
 title:"The four discrete families, and the variance-to-mean ratio that tells them apart",
 init:c=>({fam:c.fam===undefined?0:c.fam, sz:c.sz||12, p:c.p===undefined?0.3:c.p}),
 controls(st){
   const F=["Binomial","Poisson","Geometric","Negative binomial"], f=Math.round(st.fam);
   const szlab=["n, the number of trials","λ, the mean","(not used by the geometric)","r, the number of successes wanted"][f];
   const plab=f===1?"(not used by the Poisson)":"p, the success probability";
   return [
    {k:"fam",label:"family",min:0,max:3,step:1,val:f,fmt:v=>F[Math.round(v)]},
    {k:"sz",label:szlab,min:1,max:30,step:1,val:st.sz,fmt:v=>v},
    {k:"p",label:plab,min:0.05,max:0.95,step:0.05,val:st.p,fmt:v=>v.toFixed(2)}];
 },
 draw(st){
   const f=Math.round(st.fam), sz=Math.round(st.sz), p=st.p, q=1-p;
   const lf=n=>lgamma(n+1);                       // log factorial
   let pmf,mean,vari,name,support0;
   if(f===0){                                     // Binomial(n, p): k = 0..n
     name="Binomial("+sz+", "+p.toFixed(2)+")"; mean=sz*p; vari=sz*p*q; support0=0;
     pmf=k=>(k<0||k>sz)?0:Math.exp(lf(sz)-lf(k)-lf(sz-k)+k*Math.log(p)+(sz-k)*Math.log(q));
   }else if(f===1){                               // Poisson(lambda), lambda = sz
     name="Poisson("+sz+")"; mean=sz; vari=sz; support0=0;
     pmf=k=>k<0?0:Math.exp(-sz+k*Math.log(sz)-lf(k));
   }else if(f===2){                               // Geometric(p), counting TRIALS: k = 1,2,...
     name="Geometric("+p.toFixed(2)+"), counting trials"; mean=1/p; vari=q/(p*p); support0=1;
     pmf=k=>k<1?0:p*Math.exp((k-1)*Math.log(q));
   }else{                                         // NegBin(r, p), counting FAILURES: k = 0,1,...
     name="Negative binomial(r = "+sz+", "+p.toFixed(2)+"), counting failures";
     mean=sz*q/p; vari=sz*q/(p*p); support0=0;
     pmf=k=>k<0?0:Math.exp(lf(k+sz-1)-lf(k)-lf(sz-1)+sz*Math.log(p)+k*Math.log(q));
   }
   const K=Math.max(support0+4,Math.min(60,Math.ceil(mean+4*Math.sqrt(vari))+1));
   let ymax=0; const pts=[];
   for(let k=support0;k<=K;k++){const y=pmf(k); pts.push([k,y]); if(y>ymax)ymax=y;}
   if(!(ymax>0)) ymax=1;
   const p0=plot(()=>0,support0-0.5,K+0.5,{ymin:0,ymax:ymax*1.12});
   const X=x=>VP.l+(x-(support0-0.5))/((K+0.5)-(support0-0.5))*(VW-VP.l-VP.r);
   const Y=y=>VH-VP.b-(y/(ymax*1.12))*(VH-VP.t-VP.b);
   let stems="";
   for(const [k,y] of pts){
     stems+='<line x1="'+X(k).toFixed(1)+'" y1="'+Y(0).toFixed(1)+'" x2="'+X(k).toFixed(1)+
            '" y2="'+Y(y).toFixed(1)+'" stroke="var(--accent)" stroke-width="'+(K-support0>40?1.4:2.6)+'"/>';
     if(K-support0<=30) stems+='<circle cx="'+X(k).toFixed(1)+'" cy="'+Y(y).toFixed(1)+'" r="2.6" class="vdot"/>';
   }
   const ratio=vari/mean;
   // A geometric with p = 0.5 also has ratio 1, so only the Poisson may be called its signature.
   const verdict = Math.abs(ratio-1)<1e-9
                 ? (f===1 ? "exactly 1 — the Poisson signature"
                          : "exactly 1 here, which for the geometric happens only at p = 0.5")
                 : ratio<1 ? "below 1 — underdispersed" : "above 1 — overdispersed";
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Probability mass function of the selected discrete distribution, drawn as stems, with the mean marked">'+
     axes(p0,"k","P(X = k)",ticks(support0,K,Math.min(6,K-support0+1)))+stems+
     vline(p0,mean,"vmark","mean "+mean.toFixed(2))+'</svg>';
   return {svg:svg,
     read:[["distribution",name],
           ["mean",mean.toFixed(4)],
           ["variance",vari.toFixed(4)],
           ["variance ÷ mean",ratio.toFixed(4)]],
     note:"The variance-to-mean ratio is "+ratio.toFixed(4)+", "+verdict+". The ratio is the cleanest way to tell these families apart: it is q for the binomial (always below 1), exactly 1 for the Poisson, and 1/p for the negative binomial (always above 1). The geometric is the awkward one — its ratio is q/p, so it is overdispersed when p < 0.5, exactly equal at p = 0.5, and underdispersed above. Set the family to Binomial with a large n and a small p and watch the shape settle onto the Poisson with the same mean, which is the limit the exam question describes."};
 }};

VIZ["series-conv"]={
 title:"Partial sums of a power series: inside the radius they settle, outside they run away",
 init:c=>({ser:c.ser===undefined?0:c.ser, N:c.N||8}),
 controls(st){
   const L=["Σ|x−5|ⁿ/((n+1)(n+2))","Σ(x−2)ⁿ/n","Σxⁿ/n!","Σ(x+3)ⁿ/2ⁿ"];
   return [{k:"ser",label:"series",min:0,max:3,step:1,val:Math.round(st.ser),fmt:v=>L[Math.round(v)]},
           {k:"N",label:"terms kept, N",min:1,max:60,step:1,val:st.N,fmt:v=>v}];
 },
 draw(st){
   const s=Math.round(st.ser), N=Math.round(st.N);
   const SER=[
     {name:"Σ |x−5|ⁿ / ((n+1)(n+2))", x0:2, x1:8, lo:4, hi:6, open:false, R:"1 about x = 5",
      iv:"converges on [4, 6] — the radius gives (4, 6) and the endpoints converge too",
      term:(x,n)=>Math.pow(Math.abs(x-5),n)/((n+1)*(n+2)), n0:0},
     {name:"Σ (x−2)ⁿ / n", x0:0, x1:4, lo:1, hi:3, open:"right", R:"1 about x = 2",
      iv:"converges on [1, 3) — alternating harmonic at x = 1, harmonic at x = 3",
      term:(x,n)=>Math.pow(x-2,n)/n, n0:1},
     {name:"Σ xⁿ / n!  (= eˣ)", x0:-3, x1:3, lo:null, hi:null, open:false, R:"infinite",
      iv:"converges for every real x", term:(x,n)=>Math.pow(x,n)/gfact(n), n0:0},
     {name:"Σ (x+3)ⁿ / 2ⁿ", x0:-6, x1:0, lo:-5, hi:-1, open:true, R:"2 about x = −3",
      iv:"converges on (−5, −1) — diverges at both endpoints, where the terms are ±1",
      term:(x,n)=>Math.pow((x+3)/2,n), n0:0}][s];
   const SN=x=>{let t=0; for(let n=SER.n0;n<SER.n0+N;n++){const v=SER.term(x,n); if(!isFinite(v))return NaN; t+=v;} return t;};
   // Scale to what happens INSIDE the interval, then clamp, so the inside stays readable
   // while a divergent tail visibly leaves the frame instead of flattening everything.
   const a=SER.lo===null?SER.x0:SER.lo, b=SER.hi===null?SER.x1:SER.hi;
   let lo=Infinity, hi=-Infinity;
   for(let i=0;i<=200;i++){const x=a+(b-a)*i/200, y=SN(x); if(isFinite(y)){if(y<lo)lo=y; if(y>hi)hi=y;}}
   if(!isFinite(lo)||!isFinite(hi)||hi-lo<1e-9){lo=0;hi=1;}
   const pad=(hi-lo)*0.45, YL=lo-pad, YH=hi+pad;
   const clamp=y=>!isFinite(y)?YH:Math.max(YL,Math.min(YH,y));
   const p=plot(x=>clamp(SN(x)),SER.x0,SER.x1,{ymin:YL,ymax:YH});
   let marks="";
   if(SER.lo!==null) marks+=vline(p,SER.lo,"vmark","x = "+SER.lo)+vline(p,SER.hi,"vmark","x = "+SER.hi);
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Partial sum of the selected power series plotted against x, with the endpoints of the interval of convergence marked">'+
     axes(p,"x","S_N(x)",ticks(SER.x0,SER.x1,5))+
     '<path d="'+p.d+'" class="vcurve"/>'+marks+'</svg>';
   return {svg:svg,
     read:[["series",SER.name],["radius of convergence",SER.R],["terms kept",String(N)],
           ["S_N at the centre",(SER.lo===null?SN(0):SN((SER.lo+SER.hi)/2)).toFixed(5)]],
     note:"The curve is the partial sum of the first "+N+" terms. "+SER.iv+". Raise N and watch the two behaviours separate: between the marked endpoints the curve stops moving, while outside them it climbs away and is clipped at the top of the frame — the clipping IS the divergence, not a drawing artefact. The radius is decided by the coefficients alone; what happens AT the endpoints has to be checked separately, series by series, which is why two series with the same radius can have different intervals."};
 }};

// factorial via lgamma, for series whose terms carry n!
function gfact(n){ return Math.exp(lgamma(n+1)); }

VIZ["gamma-sum"]={
 title:"Adding exponentials: Gamma(n, λ), and the shape changing as n grows",
 init:c=>({n:c.n||1, lam:c.lam||1.5}),
 controls:st=>[
   {k:"n",label:"how many exponentials are added, n",min:1,max:30,step:1,val:st.n,fmt:v=>v},
   {k:"lam",label:"rate λ of each exponential",min:0.25,max:4,step:0.25,val:st.lam,fmt:v=>v.toFixed(2)}],
 draw(st){
   const n=Math.round(st.n), lam=st.lam;
   // S_n = sum of n iid exponential(lam) ~ Gamma(n, lam): mean n/lam, var n/lam^2
   const mean=n/lam, vr=n/(lam*lam), sd=Math.sqrt(vr);
   const g=x=>x<=0?0:Math.exp(n*Math.log(lam)+(n-1)*Math.log(x)-lam*x-lgamma(n));
   const nrm=x=>Math.exp(-(x-mean)*(x-mean)/(2*vr))/(Math.sqrt(2*Math.PI)*sd);
   const hi=mean+4.5*sd, p=plot(g,0,hi,{ymin:0,pad:1.15});
   let parts='<path d="'+p.d+'" class="vcurve"/>';
   if(n>1) parts+='<path d="'+plot(nrm,0,hi,{ymin:0,ymax:p.ymax}).d+'" class="vcurve alt"/>';
   parts+=vline(p,mean,"vmark","mean "+mean.toFixed(2));
   // skewness of a Gamma is 2/sqrt(n): the CLT arriving, at a rate you can watch
   const skew=2/Math.sqrt(n);
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Density of the sum of n independent exponential variables, with a normal curve of the same mean and variance for comparison">'+
     axes(p,"s","density",ticks(0,hi,5))+parts+'</svg>';
   return {svg:svg,
     read:[["distribution of the sum", n===1?("Exponential("+lam.toFixed(2)+")"):("Gamma("+n+", "+lam.toFixed(2)+")")],
           ["mean  n/λ",mean.toFixed(4)],
           ["variance  n/λ²",vr.toFixed(4)],
           ["skewness  2/√n",skew.toFixed(4)]],
     note:(n===1
       ? "At n = 1 the sum is just one exponential: the density is highest at 0 and decays, with skewness 2. Raise n and watch a peak form and move away from the origin."
       : "The teal curve is the normal with the same mean and variance. The Gamma's skewness is 2/√n = "+skew.toFixed(3)+", so it falls as n grows and the two curves converge — this is the central limit theorem happening at a rate you can read off the control. ")+
       " Note that the mean n/λ and the variance n/λ² both grow linearly in n, so the relative spread sd/mean = 1/√n shrinks. A sum of n exponentials is Gamma(n, λ) exactly, for every n — the Gamma shape parameter counts how many exponentials went in, which is why waiting for the nth event of a Poisson process has a Gamma distribution."};
 }};

VIZ["spectral"]={
 title:"The spectral density: where a process keeps its variance, by frequency",
 init:c=>({kind:c.kind===undefined?1:c.kind, phi:c.phi===undefined?0.8:c.phi}),
 controls(st){
   const L=["White noise","AR(1)","MA(1)"];
   const k=Math.round(st.kind);
   return [{k:"kind",label:"process",min:0,max:2,step:1,val:k,fmt:v=>L[Math.round(v)]},
           {k:"phi",label:k===0?"(not used by white noise)":(k===1?"φ, the AR coefficient":"θ, the MA coefficient"),
            min:-0.95,max:0.95,step:0.05,val:st.phi,fmt:v=>v.toFixed(2)}];
 },
 draw(st){
   const k=Math.round(st.kind), a=st.phi;
   // sigma^2 = 1 throughout. MA uses the MINUS convention y_t = e_t - theta e_{t-1},
   // which is the convention this question bank's answer keys use.
   let f,name,g0,note;
   if(k===0){
     name="White noise"; g0=1;
     f=()=>1/(2*Math.PI);
     note="Flat: a white-noise process holds equal variance at every frequency, which is where the name comes from. Its total area is γ₀ = 1, the variance.";
   }else if(k===1){
     name="AR(1), φ = "+a.toFixed(2); g0=1/(1-a*a);
     f=w=>1/(2*Math.PI*(1-2*a*Math.cos(w)+a*a));
     note=(a>0
       ? "A positive φ puts the mass at LOW frequencies — slow, smooth wandering. At φ = 0.8 the density is 3.979 at ω = 0 against 0.049 at ω = π, a ratio of 81."
       : a<0
       ? "A negative φ puts the mass at HIGH frequencies — rapid alternation, because the process tends to reverse sign each step."
       : "At φ = 0 the AR(1) IS white noise, so the density is flat.");
   }else{
     name="MA(1), θ = "+a.toFixed(2); g0=1+a*a;
     f=w=>(1+a*a-2*a*Math.cos(w))/(2*Math.PI);
     note=(a>0
       ? "With the minus convention yₜ = εₜ − θεₜ₋₁, a positive θ SUPPRESSES low frequencies: at θ = 0.7 the density is proportional to 1.49 − 1.4cos ω, which is 0.09 at ω = 0 and 2.89 at ω = π."
       : a<0
       ? "A negative θ under the minus convention boosts low frequencies instead, since −2θcos ω is then positive near ω = 0."
       : "At θ = 0 the MA(1) IS white noise, so the density is flat.");
   }
   const p=plot(f,0,Math.PI,{ymin:0,pad:1.15});
   // Simpson over (0, pi), doubled by symmetry: a midpoint sum left the readout at 0.9997
   // where the exact answer is 1, which reads like a discrepancy rather than a rounding.
   const area=(()=>{const M=2000,h=Math.PI/M;let s=f(0)+f(Math.PI);
     for(let i=1;i<M;i++)s+=f(i*h)*(i%2?4:2); return 2*s*h/3;})();
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Spectral density of the selected process plotted against frequency from zero to pi">'+
     axes(p,"ω  in radians, 0 to π","f(ω)",ticks(0,Math.PI,5))+
     '<path d="'+p.d+'" class="vcurve"/>'+'</svg>';
   return {svg:svg,
     read:[["process",name],
           ["f(0)",f(0).toFixed(4)],
           ["f(π)",f(Math.PI).toFixed(4)],
           ["area over (−π, π)",area.toFixed(4)+"  = γ₀ = "+g0.toFixed(4)]],
     note:note+" The area under the density over the full range (−π, π) is always γ₀, the process variance — here "+area.toFixed(4)+" against the exact "+g0.toFixed(4)+". That is what makes the spectral density a decomposition of the variance by frequency rather than merely a curve."};
 }};

VIZ["ineq-bounds"]={
 title:"Chebyshev's bound against the truth: how much slack an inequality carries",
 init:c=>({dist:c.dist===undefined?0:c.dist, k:c.k===undefined?2:c.k}),
 controls(st){
   const D=["Normal","Exponential","Uniform","Laplace","Tight 3-point"];
   const d=Math.round(st.dist);
   return [{k:"dist",label:"distribution of X (standardised to mean 0, variance 1)",min:0,max:4,step:1,val:d,fmt:v=>D[Math.round(v)]},
           {k:"k",label:"k, measured in standard deviations",min:1,max:4,step:0.1,val:st.k,fmt:v=>v.toFixed(1)}];
 },
 draw(st){
   const d=Math.round(st.dist), kk=st.k;
   // Every distribution below is standardised: mean 0, variance 1. So the Chebyshev
   // bound is 1/k^2 for all of them and the only thing that changes is the true tail.
   let tail,name,note0;
   if(d===0){                                        // standard normal
     name="Normal(0, 1)";
     tail=k=>2*(1-nphi(k));
     note0="The normal is the case most people carry in their heads, and it is where Chebyshev is at its loosest.";
   }else if(d===1){                                  // Exponential(1) shifted to mean 0: X = E - 1, sd 1
     name="Exponential(1) − 1";
     tail=k=>{ const up=Math.exp(-(1+k));             // P(E - 1 >= k) = P(E >= 1+k)
               const lo=k<1?(1-Math.exp(-(1-k))):0;   // P(E - 1 <= -k) = P(E <= 1-k), empty once k >= 1
               return up+lo; };
     note0="Skewed and one-sided: beyond k = 1 the lower tail is empty because an exponential cannot go below 0, so the whole tail probability sits above the mean.";
   }else if(d===2){                                  // Uniform standardised: support +-sqrt(3)
     name="Uniform, standardised";
     tail=k=>k>=Math.sqrt(3)?0:(1-k/Math.sqrt(3));
     note0="A uniform has bounded support, so its tail probability hits exactly zero at k = √3 ≈ 1.732 while the bound is still 1/3.";
   }else if(d===3){                                  // Laplace with variance 1: scale b = 1/sqrt(2)
     name="Laplace, standardised";
     tail=k=>Math.exp(-Math.sqrt(2)*k);
     note0="Heavier tails than the normal, so the truth sits closer to the bound — but still well under it.";
   }else{                                            // the three-point distribution that ATTAINS the bound at k
     name="3-point at ±k (attains the bound)";
     tail=k=>1/(k*k);
     note0="This is the distribution Chebyshev's proof cannot improve on: mass 1/(2k²) at each of ±k and the rest at 0.";
   }
   const bound=k=>1/(k*k);
   const p=plot(bound,1,4,{ymin:0,ymax:1.05});
   const pt=plot(tail,1,4,{ymin:0,ymax:p.ymax});
   const tv=tail(kk), bv=bound(kk);
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Chebyshev upper bound one over k squared plotted against the true tail probability of the selected distribution, as a function of k">'+
     axes(p,"k (standard deviations)","P(|X − μ| ≥ kσ)",ticks(1,4,7))+
     '<path d="'+p.d+'" class="vcurve"/>'+
     '<path d="'+pt.d+'" class="vcurve alt"/>'+
     vline(p,kk,"vmark","k = "+kk.toFixed(1))+'</svg>';
   const ratio=bv>0?tv/bv:0;
   return {svg:svg,
     read:[["distribution",name],
           ["Chebyshev bound  1/k²",bv.toFixed(6)],
           ["true P(|X − μ| ≥ kσ)",tv.toFixed(6)],
           ["truth ÷ bound",ratio.toFixed(4)]],
     note:"The accent curve is the bound 1/k², the teal curve the real tail probability. At k = "+kk.toFixed(1)+" the bound is "+bv.toFixed(4)+
          " while the truth is "+tv.toFixed(4)+" — a ratio of "+ratio.toFixed(3)+
          (d===4?". ":", so the bound overstates the tail by a factor of "+(ratio>0?(1/ratio).toFixed(1):"∞")+". ")+
          note0+" The point of the comparison is not that Chebyshev is a bad inequality but that it is a DISTRIBUTION-FREE one: it holds for every distribution with a finite variance, so it must accommodate the worst case, and the worst case is the 3-point distribution on this list. Select that option and the two curves coincide exactly — the bound is attained, so it cannot be improved without assuming more about the distribution."};
 }};

VIZ["rank-null"]={
 title:"The exact null distribution of Spearman's ρ, from every permutation",
 init:c=>({n:c.n||6, k:c.k===undefined?0:c.k}),
 controls(st){
   const n=Math.round(st.n), mx=n*(n*n-1)/3;
   return [{k:"n",label:"n, the number of ranked pairs",min:3,max:8,step:1,val:n,fmt:v=>Math.round(v)},
           {k:"k",label:"Σd² of an observed sample (0 = perfect agreement)",min:0,max:mx,step:Math.max(2,Math.round(mx/40)*2),val:Math.min(st.k,mx),fmt:v=>Math.round(v)}];
 },
 draw(st){
   const n=Math.round(st.n);
   const mx=n*(n*n-1)/3;                             // the largest Sum d^2 can be, at reversed ranks
   const obs=Math.min(Math.round(st.k),mx);
   // Enumerate every permutation of the ranks 1..n and tabulate Sum d^2. For n <= 8 that is
   // at most 40320 permutations, which is instant, and it gives the EXACT null distribution
   // rather than an approximation — the whole point of a permutation test.
   const idx=[]; for(let i=0;i<n;i++) idx.push(i);
   const cnt={}; let total=0;
   const perm=[];
   (function rec(rem){
     if(!rem.length){
       let s=0; for(let i=0;i<n;i++){const dd=(i+1)-perm[i]; s+=dd*dd;}
       cnt[s]=(cnt[s]||0)+1; total++; return;
     }
     for(let i=0;i<rem.length;i++){
       perm.push(rem[i]);
       rec(rem.slice(0,i).concat(rem.slice(i+1)));
       perm.pop();
     }
   })(idx.map(i=>i+1));
   const keys=Object.keys(cnt).map(Number).sort((a,b)=>a-b);
   const rho=s=>1-6*s/(n*(n*n-1));
   let ymax=0; for(const s of keys){const y=cnt[s]/total; if(y>ymax)ymax=y;}
   if(!(ymax>0)) ymax=1;
   const p0=plot(()=>0,-1.08,1.08,{ymin:0,ymax:ymax*1.14});
   const X=x=>VP.l+(x+1.08)/2.16*(VW-VP.l-VP.r);
   const Y=y=>VH-VP.b-(y/(ymax*1.14))*(VH-VP.t-VP.b);
   let stems="";
   for(const s of keys){
     const x=rho(s), y=cnt[s]/total;
     stems+='<line x1="'+X(x).toFixed(1)+'" y1="'+Y(0).toFixed(1)+'" x2="'+X(x).toFixed(1)+
            '" y2="'+Y(y).toFixed(1)+'" stroke="var(--accent)" stroke-width="'+(keys.length>40?1.3:2.4)+'"/>';
   }
   // one-sided exact p-value for the observed Sum d^2: P(Sum d^2 <= obs) under the null,
   // which is the upper-tail test on rho since small Sum d^2 means large positive rho.
   let le=0; for(const s of keys) if(s<=obs) le+=cnt[s];
   const pv=le/total;
   const robs=rho(obs);
   // normal approximation: rho is asymptotically N(0, 1/(n-1))
   const sd=1/Math.sqrt(n-1);
   const nap=x=>Math.exp(-x*x/(2*sd*sd))/(Math.sqrt(2*Math.PI)*sd);
   let napmax=0; for(let i=0;i<=200;i++){const v=nap(-1.08+2.16*i/200); if(v>napmax)napmax=v;}
   let napd=""; 
   for(let i=0;i<=200;i++){
     const x=-1.08+2.16*i/200, y=nap(x)/napmax*ymax;
     napd+=(i?"L":"M")+X(x).toFixed(1)+" "+Y(y).toFixed(1)+" ";
   }
   const svg='<svg viewBox="0 0 '+VW+' '+VH+'" class="viz" role="img" aria-label="Exact null distribution of Spearman rank correlation for n ranked pairs, drawn as stems over every permutation, with a normal approximation and the observed value marked">'+
     axes(p0,"ρ","P(ρ = value)",ticks(-1,1,5))+
     '<path d="'+napd.trim()+'" class="vcurve alt"/>'+stems+
     vline(p0,robs,"vmark","observed ρ = "+robs.toFixed(3))+'</svg>';
   return {svg:svg,
     read:[["permutations enumerated",total+" = "+n+"!"],
           ["distinct values of ρ",keys.length],
           ["observed ρ  (Σd² = "+obs+")",robs.toFixed(6)],
           ["exact one-sided P(ρ ≥ observed)",pv.toFixed(6)]],
     note:"Every stem is a value ρ can take, with height equal to its probability when the two rankings are unrelated — computed by running through all "+total+
          " orderings of "+n+" ranks, not by any approximation. The distribution is symmetric about 0 and supported on ±1, with the extremes ρ = 1 (Σd² = 0) and ρ = −1 (Σd² = "+mx+
          ") each having probability 1/"+total+". The teal curve is the normal approximation ρ ≈ N(0, 1/(n−1)), scaled to the same height; at n = "+n+" its standard deviation is "+sd.toFixed(4)+
          ". The approximation is poor at these sample sizes and is the reason exact tables are used for small n — raise n to 8 and watch it improve. The exact one-sided p-value shown is P(Σd² ≤ "+obs+
          ") = "+pv.toFixed(4)+", obtained by counting permutations, which is what a permutation test is. Note also that ρ = 1 − 2(Σd²/"+mx+"), so Σd² at exactly half its maximum gives ρ = 0."};
 }};
