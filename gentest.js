// Exercises in-app authoring with a scripted Claude: clean output, broken output that must be
// repaired, and a truncated answer. Nothing may reach the store unless it passes validation.
const { chromium } = require('playwright');

const SAMPLE = `
window.__genMode = 'good';
window.__calls = [];
const KINDS = ['foundation','intuition','explore','theory','worked','recall','completion','theory','explore','guided','trapcheck','guided','summary','quiz'];
function plan(broken){
  const p = {
    title:'Test Topic', breadcrumb:'Inference → Test', estMin:35,
    objectives:['Do A','Do B','Do C','Do D','Do E'],
    prereq:[{id:'p1',name:'Prereq one',why:'because'},{id:'p2',name:'Prereq two',why:'because'},
            {id:'p3',name:'Prereq three',why:'because'}],
    refs:[{title:'Ref',where:'Lesson 1.1',site:'Somewhere',url:'https://example.org/x',type:'Course notes',free:true,why:'for scene 3'}],
    revision:{sheet:['a','b','c','d','e','f','g','h','i'],cards:[['f','b'],['f','b'],['f','b'],['f','b'],['f','b'],['f','b'],['f','b'],['f','b']],
      tricks:[{hook:'h1',why:'w1'},{hook:'h2',why:'w2'},{hook:'h3',why:'w3'}],
      shortcuts:['s1','s2','s3'],remember:['r1','r2'],traps:['t1','t2','t3']},
    traps:['t1','t2','t3','t4','t5'],
    scenePlan: KINDS.map((k,i)=>{
      const o={id:'s'+(i+1),kind:k,title:'Scene '+(i+1),objective:'obj '+(i+1),mins:4};
      if(k==='explore')o.viz={type: i<5?'exp-likelihood':'unif-likelihood', n:3, sumx:12};
      if(k==='theory')o.flow=true;
      if(k==='worked'||k==='guided')o.scenario=true;
      return o;})
  };
  if(broken){ p.scenePlan = p.scenePlan.slice(0,4); p.scenePlan[1].viz={type:'heatmap-of-doom'}; delete p.objectives; }
  return p;
}
function scene(i, broken){
  const k = KINDS[i];
  const s = {id:'s'+(i+1), kind:k, title:'Scene '+(i+1), mins:4, objective:'obj'};
  if(k==='foundation'){ s.body=['why this check exists','how to use it'];
    s.items=[1,2,3].map(j=>({ask:'prereq '+j+'?',recall:'the one-line answer for '+j,
      refresh:['A rebuild paragraph with enough length to teach the prerequisite from the base, naming the tool and then carrying one small worked instance all the way through so nothing is skipped.',
               'A second paragraph with the sanity check worth keeping.']})); }
  if(k==='intuition'){ s.body=['para one','para two']; s.aside={h:'h',body:'b'}; s.ask={q:'q',nudge:'n'}; }
  if(k==='explore'){ s.body=['para']; s.viz={type:i<5?'exp-likelihood':'unif-likelihood',n:3,sumx:12}; s.ask={q:'q',nudge:'n'}; }
  if(k==='theory'){ s.blocks=[{t:'def',h:'H',body:'B'},{t:'formula',h:'F',body:'x=1'}]; }
  if(k==='worked'){ s.problem='P'; s.steps=[{say:'s',math:'m',why:'w'},{say:'s2',math:'m2',why:'w2'}]; s.after='a'; }
  if(k==='recall'){ s.intro='i'; s.items=[{q:'q',a:'a'},{q:'q2',a:'a2'}]; }
  if(k==='completion'){ s.problem='P'; s.steps=[{say:'s',math:'m',why:'w'},
      {say:'s2',blank:{prompt:'write it',answer:'x',accept:['x','X'],hint:'a hint'},why:'w'}]; s.after='a'; }
  if(k==='guided'){ s.problem='P'; s.hints=['direction','method','next step']; s.solution=[{say:'s',math:'m'}]; s.answer='A'; s.check='c'; }
  if(k==='trapcheck'){ s.intro='i'; s.items=[{claim:'c1',tf:true,why:'w'},{claim:'c2',tf:false,why:'w'}]; }
  if(k==='summary'){ s.body=['one','two']; }
  if(k==='quiz'){ s.setId='PLACEHOLDER'; }
  if(k==='theory'&&i===3){ s.flow={caption:'c',nodes:[{id:'a',r:0,c:0,label:'start',kind:'start'},
      {id:'b',r:1,c:0,label:'step'},{id:'c',r:2,c:0,label:'end',kind:'end'}],
      edges:[{from:'a',to:'b'},{from:'b',to:'c'}]}; }
  if(k==='worked'||k==='guided'){ s.scenario={teaser:'a real situation in one line',title:'Case',
      body:[new Array(50).fill('word').join(' '),new Array(50).fill('word').join(' ')],close:'what it bought them'}; }
  if(broken){
    if(k==='foundation') s.items=[{ask:'q',recall:'a'}];
    if(k==='intuition') delete s.body;
    if(k==='explore') s.viz={type:'heatmap-of-doom'};
    if(k==='theory') delete s.blocks;
    if(k==='guided') s.hints=['only one'];
    if(k==='worked') s.steps=[{say:'s',math:'m'}];
    if(k==='completion') delete s.steps[1].blank.hint;
  }
  return s;
}
function questions(n, mastery, broken){
  const out=[];
  for(let i=0;i<n;i++){
    const fmt = mastery ? (i<4?'numeric':i<6?'multi':'single') : (i<2?'numeric':i<4?'multi':'single');
    const q={id:'gen-'+(mastery?'m':'p')+'-'+(i+1), format:fmt, topic:'inference-t1',
      stem:'Question '+(i+1)+' about something specific',
      options:['opt A','opt B','opt C','opt D'], answer:'ABCD'[i%4],
      diff: (i<6?'easy':(i<16?'moderate':'hard')),
      explanation:'This is a full explanation of why A is right and why the other three are wrong in detail.'};
    if(fmt==='numeric') q.check='Check the quantity asked.';
    if(fmt==='multi'){ q.statements=['s1','s2','s3','s4'];
      q.verdicts={A:{tf:true,why:'w'},B:{tf:false,why:'w'},C:{tf:true,why:'w'},D:{tf:false,why:'w'}}; }
    out.push(q);
  }
  if(broken){ out[0].options=['a','b']; out[1].answer='Z'; delete out[2].explanation;
    if(mastery) out[3].options=[]; }
  return out;
}
window.__mkSample = () => {
  const fn = async (prompt, opts) => {
    window.__calls.push(prompt.slice(0,40));
    const mode = window.__genMode;
    const n = window.__calls.length;
    const broken = (mode==='broken' && n===1) || (mode==='broken-scenes' && n===2);
    if(mode==='truncate' && n===1) return { text: '{"title":"cut off here', truncated:true };
    if(mode==='refuse') { const e=new Error('nope'); e.code='rate_limited'; throw e; }
    let obj;
    if(/Produce the PLAN/.test(prompt)) obj = plan(broken);
    else if(/WRITE ONLY these scenes/.test(prompt)){
      const m = prompt.match(/WRITE ONLY these scenes, in full: ([\\d, ]+)/);
      const idx = m[1].split(',').map(x=>parseInt(x.trim(),10)-1);
      obj = { scenes: idx.map(i=>scene(i, broken)) };
    }
    else if(/Write (\\d+) questions/.test(prompt)){
      const m = prompt.match(/Write (\\d+) questions/);
      obj = { items: questions(parseInt(m[1],10), /HELD-OUT MASTERY/.test(prompt), broken) };
    }
    else obj = {};
    if(opts && opts.onText) opts.onText({ text: JSON.stringify(obj) });
    return { text: JSON.stringify(obj), truncated:false };
  };
  fn.json = async (p,o) => JSON.parse((await fn(p,o)).text);
  fn.limits = async () => ({images:false});
  return fn;
};
`;

(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(()=>chromium.launch());
  const p = await b.newPage({ viewport:{width:1300,height:950} });
  const errs=[]; p.on('pageerror', e=>errs.push(e.message));
  await p.addInitScript(SAMPLE);
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1500);
  await p.click('[data-login="me"]'); await p.waitForTimeout(700);
  await p.evaluate(()=>{ S.sampleFn = window.__mkSample(); });
  await p.click('[data-tab="admin"]'); await p.waitForTimeout(500);

  const run = async (stage, mode, topic) => {
    await p.evaluate(([s,mo,t])=>{ window.__genMode=mo; window.__calls=[]; S.gen=null;
      S.stage=s; S.pickMod='inference'; S.pickTopic=t; render(); }, [stage,mode,topic||'inference-t1']);
    await p.waitForTimeout(300);
    await p.click('#genRun');
    for (let i=0;i<60;i++){ if(!await p.evaluate(()=>S.gen&&S.gen.running)) break; await p.waitForTimeout(250); }
    return await p.evaluate(()=>({ calls: window.__calls.length, out: !!(S.gen&&S.gen.out),
      path: S.gen&&S.gen.out?S.gen.out.path:null, errs: S.gen?S.gen.errs.length:-1,
      summary: S.gen&&S.gen.out?S.gen.out.summary:null,
      log: S.gen?S.gen.log.map(l=>l.state[0]+':'+l.msg.slice(0,110)):[] }));
  };

  console.log('=== lesson, clean run ===');
  let r = await run('lesson','good');
  console.log('calls=' + r.calls + '  draft=' + r.out + '  path=' + r.path + '  warnings=' + r.errs);
  console.log('  ' + r.summary);
  r.log.forEach(l=>console.log('  ' + l));
  console.log('  nothing written yet: ' + await p.evaluate(()=>!window.__docs['lessons/inferencet1x'] && !(S.gen.saved)));
  const scenes = await p.evaluate(()=>S.gen.out.body.scenes.length);
  const quiz = await p.evaluate(()=>S.gen.out.body.scenes.filter(s=>s.kind==='quiz')[0].setId);
  const refs = await p.evaluate(()=>S.gen.out.body.refs.map(x=>x.unverified));
  console.log('  scenes=' + scenes + '  quiz setId rewritten to=' + quiz + '  refs flagged unverified=' + JSON.stringify(refs));

  console.log('\\n=== lesson, broken plan must be repaired ===');
  r = await run('lesson','broken');
  console.log('calls=' + r.calls + ' (extra call = the repair)  draft=' + r.out + '  warnings=' + r.errs);
  console.log('  ' + (r.log.find(l=>l.startsWith('w')) || 'NO WARNING LOGGED'));

  console.log('\\n=== scenes come back malformed ===');
  r = await run('lesson','broken-scenes');
  console.log('draft=' + r.out + '  warnings=' + r.errs);
  console.log('  ' + (r.log.find(l=>/retrying/.test(l)) || 'NO RETRY LOGGED'));

  console.log('\\n=== answer truncated ===');
  r = await run('lesson','truncate');
  console.log('draft produced=' + r.out + ' (must be false)');
  console.log('  ' + (r.log.find(l=>l.startsWith('b')) || 'NO FAILURE LOGGED'));

  console.log('\\n=== Claude refuses ===');
  r = await run('lesson','refuse');
  console.log('draft produced=' + r.out + ' (must be false)');
  console.log('  ' + (r.log.find(l=>l.startsWith('b')) || 'NO FAILURE LOGGED'));

  console.log('\\n=== mastery set, clean ===');
  r = await run('mastery','good');
  console.log('path=' + r.path + '  warnings=' + r.errs + '  ' + r.summary);
  if (r.errs) console.log('  warnings: ' + JSON.stringify(await p.evaluate(()=>S.gen.errs)));

  console.log('\\n=== mastery set with a write-in and bad keys ===');
  r = await run('mastery','broken');
  console.log('warnings after repair=' + r.errs);
  console.log('  ' + (r.log.find(l=>l.startsWith('w')) || 'no repair logged'));

  console.log('\\n=== practice set ===');
  r = await run('practice','good');
  console.log('path=' + r.path + '  warnings=' + r.errs + '  ' + r.summary);

  console.log('\\n=== commit the practice set ===');
  await p.click('#genSave'); await p.waitForTimeout(1800);
  const after = await p.evaluate(()=>({
    saved: !!S.gen.saved,
    wrote: window.__writes.filter(w=>/qsets\//.test(w[1])).map(w=>w[1]),
    indexed: !!(S.index && S.index.modules.inference),
    log: S.gen.log.slice(-2).map(l=>l.msg) }));
  console.log('saved=' + after.saved + '  wrote=' + JSON.stringify([...new Set(after.wrote)].slice(-2)));
  console.log('  ' + after.log.join('\\n  '));

  console.log('\\n=== the JSON preview ===');
  await p.click('#genPreview'); await p.waitForTimeout(400);
  console.log('textarea shown: ' + (await p.locator('.genbox textarea').count() > 0));
  await p.click('#genDrop'); await p.waitForTimeout(300);
  console.log('discard clears the panel: ' + (await p.evaluate(()=>S.gen===null)));

  await p.setViewportSize({width:393,height:852}); await p.waitForTimeout(400);
  await p.evaluate(()=>{S.stage='mastery';S.pickMod='inference';S.pickTopic='inference-t1';window.__genMode='good';render()});
  await p.waitForTimeout(300); await p.click('#genRun');
  for (let i=0;i<40;i++){ if(!await p.evaluate(()=>S.gen&&S.gen.running)) break; await p.waitForTimeout(250); }
  const ov = await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));
  console.log('\\nphone: overflow=' + (ov.sw-ov.cw));
  await p.screenshot({path:'/tmp/claude-0/gen-phone.png'});
  console.log(errs.length ? 'ERRORS: '+errs.join(' | ') : 'no runtime errors');
  await b.close();
})();
