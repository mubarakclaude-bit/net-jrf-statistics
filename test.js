// Headless test of app.html against an in-memory stand-in for the artifact db,
// loaded from the real seed documents.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const W = __dirname;                      // repo root, so a clone works anywhere
const CACHE = path.join(W, '.cache');
fs.mkdirSync(CACHE, { recursive: true });
const SEED = path.join(W, 'seed');

function seedDocs() {
  const J = f => JSON.parse(fs.readFileSync(path.join(SEED, f + '.json'), 'utf8'));
  const docs = {};
  docs['meta/catalog'] = J('catalog');
  for (const f of ['inference_multi_1', 'inference_numeric_1', 'inference_concept_1', 'pyq_j26_full',
                   'inference_t4_practice', 'inference_t4_mastery', 'inference_t1_mastery', 'inference_t2_mastery', 'inference_t3_mastery', 'inference_t6_mastery', 'inference_t5_mastery', 'inference_t9_mastery', 'inference_t7_mastery', 'inference_t8_mastery', 'inference_t12_mastery', 'inference_t10_mastery', 'inference_t13_mastery', 'inference_t17_mastery', 'inference_t15_mastery', 'inference_t14_mastery', 'inference_t16_mastery', 'inference_t11_mastery', 'timeseries_t3_mastery', 'timeseries_t5_mastery', 'official_t1_mastery', 'official_t2_mastery', 'official_t3_mastery', 'official_t4_mastery', 'official_t5_mastery', 'probability_t7_mastery', 'nonparam_t4_mastery', 'timeseries_t11_mastery', 'timeseries_t10_mastery', 'timeseries_t9_mastery', 'timeseries_t8_mastery', 'timeseries_t4_mastery', 'timeseries_t2_mastery', 'timeseries_t1_mastery', 'timeseries_t7_mastery', 'timeseries_t6_mastery', 'probability_t10_mastery', 'probability_t8_mastery', 'maths_t4_mastery', 'maths_t2_mastery', 'maths_t3_mastery', 'maths_t5_mastery', 'maths_t6_mastery', 'maths_t7_mastery', 'probability_t5_mastery', 'maths_t1_mastery', 'probability_t1_mastery', 'probability_t13_mastery', 'probability_t3_mastery',
                   'inference_pyq_variants','maths_pyq_variants','probability_pyq_variants',
                   'timeseries_pyq_variants','rprog_pyq_variants','regression_pyq_variants',
                   'multivariate_pyq_variants','nonparam_pyq_variants','official_pyq_variants', 'stochastic_t1_mastery']) docs['qsets/' + f] = J(f);
  docs['lessons/mle'] = J('lesson_mle');
  docs['lessons/inferencet1'] = J('lesson_t1');
  docs['lessons/inferencet2'] = J('lesson_t2');
  docs['lessons/inferencet3'] = J('lesson_t3');
  docs['lessons/inferencet6'] = J('lesson_t6');
  docs['lessons/inferencet5'] = J('lesson_t5');
  docs['lessons/inferencet9'] = J('lesson_t9');
  docs['lessons/inferencet7'] = J('lesson_t7');
  docs['lessons/inferencet8'] = J('lesson_t8');
  docs['lessons/inferencet12'] = J('lesson_t12');
  docs['lessons/inferencet10'] = J('lesson_t10');
  docs['lessons/inferencet13'] = J('lesson_t13');
  docs['lessons/inferencet17'] = J('lesson_t17');
  docs['lessons/inferencet15'] = J('lesson_t15');
  docs['lessons/inferencet14'] = J('lesson_t14');
  docs['lessons/inferencet16'] = J('lesson_t16');
  docs['lessons/inferencet11'] = J('lesson_t11');
  docs['lessons/timeseriest3'] = J('lesson_ts3');
  docs['lessons/timeseriest5'] = J('lesson_ts5');
  docs['lessons/officialt1'] = J('lesson_10a1');
  docs['lessons/officialt2'] = J('lesson_10a2');
  docs['lessons/officialt3'] = J('lesson_10a3');
  docs['lessons/officialt4'] = J('lesson_10a4');
  docs['lessons/officialt5'] = J('lesson_10a5');
  docs['lessons/probabilityt3'] = J('lesson_pr3');
  docs['lessons/probabilityt13'] = J('lesson_pr13');
  docs['lessons/probabilityt1'] = J('lesson_pr1');
  docs['lessons/mathst1'] = J('lesson_ma1');
  docs['lessons/mathst2'] = J('lesson_ma2');
  docs['lessons/mathst3'] = J('lesson_ma3');
  docs['lessons/mathst5'] = J('lesson_ma5');
  docs['lessons/mathst6'] = J('lesson_ma6');
  docs['lessons/mathst7'] = J('lesson_ma7');
  docs['lessons/probabilityt5'] = J('lesson_pr5');
  docs['lessons/mathst4'] = J('lesson_ma4');
  docs['lessons/probabilityt8'] = J('lesson_pr8');
  docs['lessons/probabilityt10'] = J('lesson_pr10');
  docs['lessons/timeseriest6'] = J('lesson_ts6');
  docs['lessons/timeseriest7'] = J('lesson_ts7');
  docs['lessons/timeseriest1'] = J('lesson_ts1');
  docs['lessons/timeseriest2'] = J('lesson_ts2');
  docs['lessons/timeseriest4'] = J('lesson_ts4');
  docs['lessons/timeseriest8'] = J('lesson_ts8');
  docs['lessons/timeseriest9'] = J('lesson_ts9');
  docs['lessons/timeseriest10'] = J('lesson_ts10');
  docs['lessons/timeseriest11'] = J('lesson_ts11');
  docs['lessons/nonparamt4'] = J('lesson_np4');
  docs['lessons/probabilityt7'] = J('lesson_pr7');
  docs['lessons/stochastict1'] = J('lesson_stochastic_t1');
  docs['meta/lessons'] = J('meta_lessons');
  docs['meta/users'] = J('meta_users');
  docs['meta/syllabus'] = J('meta_syllabus');
  docs['meta/app'] = { url: 'https://claude.ai/artifact/TEST', title: 'NET JRF Statistics', v: 4 };
  return docs;
}

// the stub runs inside the page; it mimics the db/user/sample/downloads surfaces we use
const STUB = `
window.__writes = [];
window.__docs = __SEED__;
function mkDoc(p){
  return {
    id: p.split('/').pop(), path: p,
    get: async () => { await new Promise(r=>setTimeout(r,(window.__SLOW_LESSON&&p.indexOf('lessons/')===0)?window.__SLOW_LESSON:180)); const d = window.__docs[p];
      return { id: p.split('/').pop(), exists: d !== undefined, data: () => d, metadata:{fromCache:false,hasPendingWrites:false} }; },
    set: async (b) => { window.__docs[p] = JSON.parse(JSON.stringify(b)); window.__writes.push(['set', p]); },
    update: async (b) => { Object.assign(window.__docs[p] || (window.__docs[p] = {}), b); window.__writes.push(['update', p]); },
    delete: async () => { delete window.__docs[p]; window.__writes.push(['delete', p]); },
    onSnapshot: (next) => { const fire=()=>next({ id: p.split('/').pop(), exists: window.__docs[p] !== undefined,
      data: () => window.__docs[p], metadata:{fromCache:false,hasPendingWrites:false} });
      setTimeout(fire, 400); const iv=setInterval(fire, 1500); return () => clearInterval(iv); },
    collection: (sub) => mkColl(p + '/' + sub)
  };
}
function mkColl(cp, filters){
  filters = filters || [];
  const q = {
    path: cp,
    doc: (id) => mkDoc(cp + '/' + (id || ('auto' + Math.random().toString(36).slice(2, 9)))),
    add: async (d) => { const r = q.doc(); await r.set(d); return r; },
    where: (f, op, v) => mkColl(cp, filters.concat([[f, op, v]])),
    orderBy: () => q, limit: () => q,
    get: async () => {
      await new Promise(r=>setTimeout(r,220));
      const out = [];
      Object.keys(window.__docs).forEach(p => {
        const parts = p.split('/');
        if (parts.slice(0, -1).join('/') !== cp) return;
        const d = window.__docs[p];
        if (!filters.every(([f, op, v]) => op === '==' ? d[f] === v : true)) return;
        out.push({ id: parts[parts.length-1], exists: true, data: () => d, metadata:{fromCache:false,hasPendingWrites:false} });
      });
      out.sort((a,b)=>a.id<b.id?-1:1);
      return { docs: out, size: out.length, empty: !out.length, docChanges: () => [], metadata:{fromCache:false,hasPendingWrites:false} };
    },
    onSnapshot: (next) => { q.get().then(next); return () => {}; }
  };
  return q;
}
window.claude = { use: async (n) => {
  if (n === 'db') return { doc: mkDoc, collection: (p) => mkColl(p) };
  if (n === 'user') return { me: async () => ({ id:'u-test', name:'Mubaraka' }), id: async () => 'u-test', isOwner: () => true, canEdit: () => true, can: () => true, me: async()=>({id:'u-test'}) };
  if (n === 'downloads') return { save: async (r) => { window.__saved = { filename: r.filename, size: String(r.data).length }; return { status: 'saved' }; } };
  if (n === 'sample') return async (input, opts) => { window.__asked = input; if (opts && opts.onText) opts.onText({ text: 'stub answer' }); return { text: 'stub answer' }; };
  return null;
} };
`;

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1180, height: 950 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });

  const body = fs.readFileSync(path.join(W, 'app.html'), 'utf8');
  const stub = STUB.replace('__SEED__', JSON.stringify(seedDocs()));
  // mirror the real artifact wrapper, viewport meta and safe-area padding included
  const html = '<!doctype html><html><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' +
    '<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}' +
    'body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff}img{max-width:100%}[hidden]{display:none!important}</style>' +
    '<script>' + stub + '</script></head><body>' + body + '</body></html>';
  fs.writeFileSync(path.join(CACHE, 'harness.html'), html);
  await page.goto('file://' + path.join(CACHE, 'harness.html'));
  await page.waitForTimeout(900);
  // the front door now stands in front of the app
  if (await page.locator('[data-login="me"]').count()) { await page.click('[data-login="me"]'); await page.waitForTimeout(700); }

  const out = [];
  const say = s => { out.push(s); console.log(s); };

  // ---- boot
  say('ready=' + await page.evaluate(() => S.ready) + ' modules=' + await page.evaluate(() => (S.catalog && S.catalog.modules || []).length) +
      ' indexBuilt=' + await page.evaluate(() => !!S.index));
  say('index totals=' + JSON.stringify(await page.evaluate(() => {
    const m = S.index.modules; const o = {}; Object.keys(m).forEach(k => o[k] = m[k].total); return o; })));

  // ---- home numbers
  say('hdScore="' + (await page.textContent('#hdScore')) + '"');
  const hm = await page.evaluate(() => { const o = overall(2); return { proj: Math.round(o.proj), base: Math.round(o.base), marks: o.marks, target: o.target }; });
  say('home: projected=' + hm.proj + '/200  baseline=' + hm.base + '  marks=' + hm.marks + '  targetQ=' + hm.target);
  say('strip blocks=' + await page.locator('.strip button').count() + '  stat cards=' + await page.locator('#v-home .g4 .card').count());

  // ---- every tab renders
  for (const t of ['learn', 'bank', 'mock', 'progress', 'admin']) {
    await page.click('[data-tab="' + t + '"]');
    await page.waitForTimeout(t === 'bank' ? 700 : 260);
    const n = (await page.innerHTML('#v-' + t)).length;
    say('tab ' + t.padEnd(9) + ' html=' + String(n).padStart(6) + '  visible=' + await page.isVisible('#v-' + t));
  }

  // ---- learning tree (walked in detail by learn-test.js)
  await page.click('[data-tab="learn"]'); await page.waitForTimeout(300);
  await page.click('.navmh[data-mod="inference"]'); await page.waitForTimeout(250);
  say('learn tree: topics=' + await page.locator('.navt').count() + '  modes=' + await page.locator('[data-mode]').count());

  // ---- bank filters
  await page.click('[data-tab="bank"]'); await page.waitForTimeout(800);
  say('bank rows=' + await page.locator('#v-bank .qrow').count() + '  (expect 106)');
  await page.selectOption('#fFmt', 'multi'); await page.waitForTimeout(400);
  say('filter multi -> ' + await page.locator('#v-bank .qrow').count() + ' (expect 35+pyq multi)');
  await page.selectOption('#fSrc', 'pyq'); await page.waitForTimeout(400);
  say('filter multi+pyq -> ' + await page.locator('#v-bank .qrow').count());
  await page.selectOption('#fFmt', ''); await page.selectOption('#fSrc', 'pyq'); await page.waitForTimeout(400);
  say('filter pyq -> ' + await page.locator('#v-bank .qrow').count() + ' (expect 6)');

  // ---- drill a multi item: gating must hold
  await page.selectOption('#fSrc', ''); await page.selectOption('#fFmt', 'multi'); await page.waitForTimeout(400);
  await page.locator('#v-bank .qrow').first().click(); await page.waitForTimeout(350);
  say('drill open: locked=' + await page.locator('.locked').count() + '  reveal disabled=' + await page.locator('#reveal').isDisabled());
  const vb = page.locator('.vb.t');
  const nst = await vb.count();
  for (let i = 0; i < nst; i++) { await page.locator('.vb.t').nth(i).click(); await page.waitForTimeout(90); }
  say('after ' + nst + ' verdicts: locked=' + await page.locator('.locked').count() + '  reveal disabled=' + await page.locator('#reveal').isDisabled());
  await page.locator('.opt').first().click(); await page.waitForTimeout(150);
  say('after picking: reveal disabled=' + await page.locator('#reveal').isDisabled());
  await page.click('#reveal'); await page.waitForTimeout(300);
  say('revealed: explanation=' + await page.locator('.expl').count() + '  per-statement verdicts=' + await page.locator('.vitem').count() +
      '  errBtns=' + await page.locator('[data-err]').count() + '  attempts=' + JSON.stringify(await page.evaluate(() => Object.keys(S.att).length)));
  if (await page.locator('[data-err]').count()) { await page.locator('[data-err]').first().click(); await page.waitForTimeout(250);
    say('error logged=' + JSON.stringify(await page.evaluate(() => S.errs.length))); }
  await page.locator('#v-bank [data-ask]').first().click(); await page.waitForTimeout(300);
  say('ask fired, prompt starts: "' + String(await page.evaluate(() => window.__asked || '')).slice(0, 72) + '…"');
  await page.locator('[data-nav="1"]').click(); await page.waitForTimeout(300);
  say('next question: shown=' + await page.evaluate(() => S.drill.shown) + ' locked=' + await page.locator('.locked').count());

  // ---- write-in numericals
  await page.click('[data-exit="1"]'); await page.waitForTimeout(250);
  await page.selectOption('#fFmt', 'free'); await page.waitForTimeout(450);
  say('write-in filter -> ' + await page.locator('#v-bank .qrow').count() + ' rows (expect 25)');
  await page.locator('#v-bank .qrow').first().click(); await page.waitForTimeout(300);
  say('write-in: answer box=' + await page.locator('#freeAns').count() + '  options=' + await page.locator('.opt').count() +
      '  toggles=' + await page.locator('[data-w="1"],[data-c="1"]').count() + '  locked=' + await page.locator('.locked').count() +
      '  reveal disabled=' + await page.locator('#reveal').isDisabled());
  await page.fill('#freeAns', 'p-hat = 0.3');
  await page.locator('[data-w="1"]').click(); await page.waitForTimeout(140);
  say('  one toggle: locked=' + await page.locator('.locked').count() + '  text kept=' + JSON.stringify(await page.inputValue('#freeAns')));
  await page.locator('[data-c="1"]').click(); await page.waitForTimeout(140);
  say('  both toggles: locked=' + await page.locator('.locked').count() + '  reveal disabled=' + await page.locator('#reveal').isDisabled());
  await page.click('#reveal'); await page.waitForTimeout(300);
  const attBefore = await page.evaluate(() => Object.keys(S.att).length);
  say('  revealed: answer shown=' + /class="expl/.test(await page.innerHTML('#v-bank')) +
      '  terminal check=' + /Terminal check/.test(await page.innerHTML('#v-bank')) +
      '  self-mark buttons=' + await page.locator('[data-self]').count() + '  recorded yet=' + attBefore);
  await page.locator('[data-self="0"]').click(); await page.waitForTimeout(300);
  say('  marked wrong: attempts=' + await page.evaluate(() => Object.keys(S.att).length) +
      '  errBtns=' + await page.locator('[data-err]').count() +
      '  status=' + await page.evaluate(() => statusOf(S.drill.list[S.drill.i].id)));
  await page.click('[data-exit="1"]'); await page.waitForTimeout(200);
  await page.selectOption('#fFmt', ''); await page.waitForTimeout(400);

  // ---- mock
  await page.click('[data-tab="mock"]'); await page.waitForTimeout(300);
  say('mock gaps banner=' + /no content yet/.test(await page.innerHTML('#v-mock')));
  // the length now follows the time you say you have; "no limit" hands the count back
  // The mock view re-renders whenever a watched store doc arrives, and a re-render rebuilds
  // #mkMins at its default, which re-disables #mkN and discards a select made just before.
  // With 27 lessons the snapshots land later, so this grew from flaky to reliable failure.
  // Wait for the view to stop changing, THEN set the value, then confirm it stuck.
  await page.waitForFunction(() => {
    const v = document.querySelector('#v-mock'); if (!v) return false;
    const len = v.innerHTML.length;
    if (window.__mkLen === len) { return (window.__mkStable = (window.__mkStable || 0) + 1) >= 3; }
    window.__mkLen = len; window.__mkStable = 0; return false;
  }, null, { timeout: 20000, polling: 300 });
  for (let i = 0; i < 20; i++) {
    await page.selectOption('#mkMins', '0');
    await page.waitForTimeout(150);
    if (await page.evaluate(() => {
      const m = document.querySelector('#mkMins'), n = document.querySelector('#mkN');
      return !!(m && n && m.value === '0' && !n.disabled);
    })) break;
    await page.waitForTimeout(250);
  }
  await page.waitForFunction(() => { const n = document.querySelector('#mkN'); return n && !n.disabled; }, null, { timeout: 15000 });
  await page.selectOption('#mkN', '25'); await page.selectOption('#mkScope', '2'); await page.selectOption('#mkTimer', '1');
  await page.click('#mkStart'); await page.waitForTimeout(1200);
  const mk = await page.evaluate(() => S.mock ? { n: S.mock.list.length, fmts: S.mock.list.reduce((a, q) => (a[q.format] = (a[q.format] || 0) + 1, a), {}), mods: Object.keys(S.mock.list.reduce((a, q) => (a[q.moduleId] = 1, a), {})) } : null);
  say('mock built: ' + JSON.stringify(mk));
  say('mock has no write-in items=' + await page.evaluate(() => S.mock.list.every(q => (q.options||[]).length === 4)));
  say('clock=' + (await page.textContent('#mkClock').catch(() => 'none')) + '  palette=' + await page.locator('[data-mgo]').count());
  for (let i = 0; i < (mk ? mk.n : 0); i++) { await page.locator('.opt').first().click(); await page.waitForTimeout(45); }
  await page.waitForTimeout(200);
  const btn = await page.locator('#mkSubmit2').count() ? '#mkSubmit2' : '#mkSubmit';
  await page.click(btn); await page.waitForTimeout(600);
  say('mock submitted: done=' + await page.evaluate(() => !!(S.mock && S.mock.done)) +
      '  stored=' + await page.evaluate(() => S.mocks.length) +
      '  byModule=' + JSON.stringify(await page.evaluate(() => S.mock && S.mock.byModule)));
  say('result page: review items=' + await page.locator('#v-mock details.sp').count() + '  format table=' + /By format/.test(await page.innerHTML('#v-mock')));
  await page.click('#mkExit'); await page.waitForTimeout(300);
  say('history table rows=' + await page.locator('#v-mock .tbl tbody tr').count());

  // ---- progress
  await page.click('[data-tab="progress"]'); await page.waitForTimeout(300);
  await page.click('#loadAllBtn'); await page.waitForTimeout(1200);
  say('progress: module bars=' + await page.locator('#v-progress .bar').count() + '  table rows=' + await page.locator('#v-progress .tbl tbody tr').count());
  say('format stats=' + JSON.stringify(await page.evaluate(() => fmtStats())));
  say('inference stat=' + JSON.stringify(await page.evaluate(() => { const x = mstat(modById('inference')); return { att: x.att, cor: x.cor, acc: +x.acc.toFixed(3), loaded: x.loaded, need: x.need, mock: x.mock, st: x.st, proj: +x.proj.toFixed(1) }; })));

  // ---- content
  await page.click('[data-tab="admin"]'); await page.waitForTimeout(300);
  say('content: table rows=' + await page.locator('#v-admin .tbl tbody tr').count() + '  promptBox=' + await page.locator('#pBox').count());
  const p = await page.inputValue('#pBox');
  say('prompt length=' + p.length + '  mentions artifact url=' + /claude.ai\/artifact\/TEST/.test(p));
  await page.selectOption('#fMod2', 'timeseries'); await page.waitForTimeout(350);
  say('switched prompt module -> ' + /Time series|timeseries/.test(await page.inputValue('#pBox')));
  await page.click('#exGo').catch(() => {}); await page.waitForTimeout(900);
  say('export attempted, saved=' + JSON.stringify(await page.evaluate(() => window.__saved || null)));
  await page.selectOption('#exWhat', 'all'); await page.waitForTimeout(150);
  await page.click('#exGo'); await page.waitForTimeout(1200);
  say('export all, saved=' + JSON.stringify(await page.evaluate(() => window.__saved || null)));
  await page.click('#rescan'); await page.waitForTimeout(700);
  say('rescan wrote meta/index=' + await page.evaluate(() => window.__writes.filter(w => w[1] === 'meta/index').length));

  // ---- settings + theme
  await page.click('[data-tab="home"]'); await page.waitForTimeout(250);
  await page.fill('#cfgExam', '2026-12-18'); await page.fill('#cfgTarget', '150'); await page.click('#cfgSave'); await page.waitForTimeout(400);
  say('exam chip="' + await page.textContent('#hdDays') + '"');
  await page.click('#themeBtn'); await page.waitForTimeout(200);
  say('theme=' + await page.evaluate(() => document.documentElement.getAttribute('data-theme')));

  // ---- mobile width: no horizontal scroll
  for (const w of [390, 360]) {
    await page.setViewportSize({ width: w, height: 844 }); await page.waitForTimeout(400);
    for (const t of ['home', 'learn', 'bank', 'mock', 'progress', 'admin']) {
      await page.click('[data-tab="' + t + '"]'); await page.waitForTimeout(t === 'bank' ? 500 : 220);
      const r = await page.evaluate(() => {
        const d = document.documentElement; const off = [];
        if (d.scrollWidth > d.clientWidth + 1) document.querySelectorAll('*').forEach(e => {
          const b = e.getBoundingClientRect();
          if (b.right > d.clientWidth + 1 && b.width > 0) off.push(e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : '') + '#' + (e.id||'') + '@' + Math.round(b.right));
        });
        return { sw: d.scrollWidth, cw: d.clientWidth, off: off.slice(0, 5) };
      });
      say(w + 'px ' + t.padEnd(9) + ' scrollWidth=' + r.sw + ' client=' + r.cw + (r.sw > r.cw + 1 ? '  <-- OVERFLOW ' + r.off.join(' | ') : '  ok'));
    }
    // also open a drill at phone width
    if (w === 390) { await page.click('[data-tab="bank"]'); await page.waitForTimeout(500);
      await page.locator('#v-bank .qrow').first().click(); await page.waitForTimeout(350);
      const r2 = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
      say('390px drill     scrollWidth=' + r2.sw + ' client=' + r2.cw + (r2.sw > r2.cw + 1 ? '  <-- OVERFLOW' : '  ok'));
      await page.click('[data-exit="1"]'); await page.waitForTimeout(200); }
  }

  say('--- errors: ' + (errs.length ? '\n' + errs.join('\n') : 'none'));
  await browser.close();
  fs.writeFileSync(path.join(CACHE, 'test-out.txt'), out.join('\n'));
})().catch(e => { console.error('HARNESS FAILED', e); process.exit(1); });
