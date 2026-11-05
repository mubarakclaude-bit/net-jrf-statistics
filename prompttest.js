// The content factory is how other chats author lessons, so the prompts must name
// every feature this app now renders, and the validators must refuse drafts without them.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1400);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(800); }
  let fails = 0; const bad = m => { fails++; console.log('   FAIL ' + m); };

  await p.click('[data-tab="admin"]'); await p.waitForTimeout(500);
  await p.selectOption('#fMod2', 'inference'); await p.waitForTimeout(250);

  console.log('--- what each prompt now insists on ---');
  const MUST = {
    blueprint: [],
    lesson: ['two or three years', 'foundation', 'flow', 'scenario', 'tricks', 'shortcuts',
             'remember', 'diff', 'decision procedure', 'Exam weight', 'obviously'],
    practice: ['two or three years', '"diff"', 'easy', 'moderate', 'hard', 'spread the keys'],
    mastery:  ['two or three years', '"diff"', '3 easy / 5 moderate / 2 hard', 'spread the keys',
               'held out', '6 easy / 10 moderate / 4 hard', 'POOL of 20'],
    validation: []
  };
  for (const stage of Object.keys(MUST)) {
    await p.selectOption('#fStage', stage); await p.waitForTimeout(300);
    if (stage === 'practice' || stage === 'mastery') { await p.selectOption('#fTop', 'inference-t7'); await p.waitForTimeout(250); }
    const t = await p.inputValue('#pBox');
    const missing = MUST[stage].filter(w => t.indexOf(w) < 0);
    console.log('  ' + stage.padEnd(11) + String(t.length).padStart(5) + ' chars' +
                (MUST[stage].length ? '  carries ' + (MUST[stage].length - missing.length) + '/' + MUST[stage].length + ' required phrases' : ''));
    if (missing.length) bad(stage + ' prompt never mentions: ' + missing.join(', '));
  }

  console.log('--- the in-app generator\'s own prompts ---');
  const gp = await p.evaluate(() => {
    const m = S.catalog.modules.filter(x => x.id === 'inference')[0];
    const t = (m.topics || []).filter(x => x.id === 'inference-t7')[0] || m.topics[0];
    return { plan: pPlan(m, t), scenes: pScenes(m, t, { title:'T', objectives:['a'], prereq:[{name:'p'}],
               scenePlan:[{kind:'foundation',title:'F',objective:'o'}] }, [{ i:0 }]),
             mastery: pQuestions(m, t, 'mastery', 20, ''), practice: pQuestions(m, t, 'practice', 15, '') };
  });
  const GMUST = {
    plan:     ['two or three years', 'foundation drill', '"flow":true', '"scenario":true', '"tricks"', '"remember"', 'Exam weight'],
    scenes:   ['foundation {', '"flow":{', '"scenario":{', 'prerequisite CHECK', 'Check every number'],
    mastery:  ['"diff"', '3 easy, 5 moderate, 2 hard', 'Spread the correct answers', 'HELD-OUT MASTERY POOL', '6 easy'],
    practice: ['"diff"', 'Spread the correct answers', '3 easy to 5 moderate to 2 hard']
  };
  for (const k of Object.keys(GMUST)) {
    const miss = GMUST[k].filter(w => gp[k].indexOf(w) < 0);
    console.log('  ' + k.padEnd(9) + String(gp[k].length).padStart(5) + ' chars  ' + (GMUST[k].length - miss.length) + '/' + GMUST[k].length);
    if (miss.length) bad('in-app ' + k + ' prompt never mentions: ' + miss.join(', '));
  }

  console.log('--- validators refuse a draft that skips the new features ---');
  const v = await p.evaluate(() => {
    const plan = { title:'t', breadcrumb:'b', estMin:40,
      objectives:['a','b','c','d'], prereq:[{id:'p1',name:'n',why:'w'}],
      refs:[{title:'r'}], traps:['x','y','z','a','b'],
      revision:{ sheet:new Array(9).fill('f'), cards:new Array(8).fill(['f','b']) },
      scenePlan:['intuition','theory','worked','recall','completion','theory','guided','trapcheck','guided','summary','quiz']
        .map((k,i)=>({id:'s'+(i+1),kind:k,title:'T'+i,objective:'o',mins:3})) };
    const planErrs = vLessonPlan(plan);
    const thin = { id:'s1', kind:'foundation', title:'Ground', mins:5, objective:'o',
      body:['one'], items:[{ask:'q',recall:'a'},{ask:'q2',recall:'a2',refresh:['too short']}] };
    const flowBad = { id:'s2', kind:'theory', title:'T', mins:4, blocks:[{t:'def',h:'h',body:'b'}],
      flow:{ nodes:[{id:'n1',r:0,c:0,label:'a'},{id:'n2',r:1,c:0,label:'b'}], edges:[{from:'n1',to:'n9'}] } };
    const qs = { source:'mastery', items:new Array(10).fill(0).map((_,i)=>({
      id:'q'+i, format:'single', topic:'x', stem:'s', options:['a','b','c','d'], answer:'A',
      explanation:'a long enough explanation to pass the length check here' })) };
    return { plan: planErrs, thin: vScene(thin,0), flow: vScene(flowBad,1), qs: vQset(qs,20) };
  });
  const want = (label, list, phrases) => {
    const missing = phrases.filter(w => !list.some(e => e.indexOf(w) >= 0));
    console.log('  ' + label.padEnd(22) + list.length + ' complaints' + (missing.length ? '' : '  ✓'));
    if (missing.length) bad(label + ' did not complain about: ' + missing.join(' / ') + '  [got: ' + list.join(' · ') + ']');
  };
  want('plan without drills', v.plan, ['first scene must be the foundation', 'no foundation scene',
      'fewer than 3 prerequisites', 'flow diagram', 'real-world scenario', 'mnemonics', 'shortcuts', 'remember nothing else']);
  want('thin foundation', v.thin, ['prerequisite checks', 'no rebuild', 'too thin to teach from']);
  want('broken flow diagram', v.flow, ['fewer than 3 nodes', 'does not exist']);
  want('under-specified pool', v.qs, ['needs "easy"', 'mastery pool is 20', 'numerical items',
      'multi-statement', 'spread the keys', 'easy items']);

  console.log('--- a complete draft passes ---');
  const ok = await p.evaluate(() => {
    const sc = { id:'s1', kind:'foundation', title:'Ground yourself', mins:6, objective:'o',
      body:['why this exists','how to use it'],
      items:[1,2,3].map(k=>({ ask:'ask '+k, recall:'recall '+k,
        refresh:['A rebuild paragraph long enough to teach the prerequisite from the base, naming the tool and then carrying every step of one small worked instance so the learner sees it move rather than being told it moves.',
                 'And a second paragraph that lands the point, with the one sanity check worth keeping.'] })) };
    const th = { id:'s2', kind:'theory', title:'T', mins:4, blocks:[{t:'def',h:'h',body:'b'}],
      flow:{ caption:'c', nodes:[{id:'a',r:0,c:0,label:'start'},{id:'b',r:1,c:0,label:'step'},{id:'c',r:2,c:0,label:'end'}],
             edges:[{from:'a',to:'b'},{from:'b',to:'c'}] },
      scenario:{ teaser:'a plant throws away 40,000 numbers', title:'Case', body:[new Array(45).fill('word').join(' '), new Array(45).fill('word').join(' ')] } };
    return { found: vScene(sc,0), theory: vScene(th,1) };
  });
  console.log('  clean foundation scene: ' + (ok.found.length ? 'REJECTED ' + ok.found.join('; ') : 'accepted'));
  console.log('  clean flow + scenario:  ' + (ok.theory.length ? 'REJECTED ' + ok.theory.join('; ') : 'accepted'));
  if (ok.found.length || ok.theory.length) bad('a valid draft was rejected');

  console.log('\nerrors: ' + (errs.length ? errs.join(' | ') : 'none'));
  console.log(fails ? 'FAILURES: ' + fails : 'content factory carries every feature');
  await b.close(); process.exit(fails || errs.length ? 1 : 0);
})();
