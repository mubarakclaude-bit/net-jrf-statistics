// Two things must hold: the owner sees questions and requests from every learner, and a
// learner sees no Admin tab and cannot reach the route by hash either.
const { chromium } = require('playwright');
const fs = require('fs');

function harness(owner, docs) {
  const STUB = fs.readFileSync('/home/claude/w1/test.js', 'utf8').match(/const STUB = `([\s\S]*?)`;/)[1]
    .replace("isOwner: () => true", "isOwner: () => " + (owner ? "true" : "false"))
    .replace("canEdit: () => true", "canEdit: () => " + (owner ? "true" : "false"));
  const html = '<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;font:14px sans-serif}</style><script>'
    + STUB.replace('__SEED__', JSON.stringify(docs)) + '</script></head><body>'
    + fs.readFileSync('/home/claude/w1/app.html', 'utf8') + '</body></html>';
  const f = '/tmp/claude-0/role-' + (owner ? 'owner' : 'learner') + '.html';
  fs.writeFileSync(f, html); return f;
}

(async () => {
  let fails = 0; const bad = m => { fails++; console.log('   FAIL ' + m); };
  const base = JSON.parse(fs.readFileSync('/tmp/claude-0/seeddocs.json', 'utf8'));
  // three learners have already asked things and filed requests
  base['feedback/u-test']   = { uid:'u-test', name:'Mubaraka', label:'me',
    asks:[{ts:1,topicId:'inference-t1',topic:'Sufficiency',scene:'Theory',intent:'define',sel:'minimal sufficient',a:'...',helpful:null}],
    reqs:[{ts:1,kind:'detail',topic:'Sufficiency',scene:'Theory',text:'more on factorisation'}] };
  base['feedback/u-asha']   = { uid:'u-asha', name:'Asha', label:'learner',
    asks:[{ts:2,topicId:'inference-t7',topic:'Bayesian',scene:'Theory',intent:'basics',sel:'conjugate',a:'...',helpful:false},
          {ts:3,topicId:'inference-t7',topic:'Bayesian',scene:'Theory',intent:'define',sel:'posterior',a:'...',helpful:null}],
    reqs:[{ts:2,kind:'example',topic:'Bayesian',scene:'Theory',text:'a worked Gamma-Poisson'}] };
  base['feedback/u-ravi']   = { uid:'u-ravi', name:'Ravi', label:'learner',
    asks:[{ts:4,topicId:'inference-t8',topic:'Decision theory',scene:'Theory',intent:'elaborate',sel:'admissible',a:'...',helpful:false}],
    reqs:[] };

  for (const owner of [true, false]) {
    const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
    const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + harness(owner, base)); await p.waitForTimeout(1600);
    if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(1200); }
    const role = owner ? 'OWNER  ' : 'LEARNER';
    const isAdmin = await p.evaluate(() => S.isAdmin);
    const tabs = await p.evaluate(() => Array.from(document.querySelectorAll('#nav button')).map(b => b.dataset.tab));
    console.log(role + ' isAdmin=' + isAdmin + '  tabs: ' + tabs.join(', '));

    if (owner) {
      if (!isAdmin) bad('owner not recognised as admin');
      if (tabs.indexOf('admin') < 0) bad('owner has no Admin tab');
      await p.click('[data-tab="admin"]'); await p.waitForTimeout(900);
      const n = await p.evaluate(() => ({ asks: fbRows('asks').length, reqs: fbRows('reqs').length,
        learners: fbLearners('asks') }));
      console.log('   admin sees ' + n.asks + ' asks and ' + n.reqs + ' requests from ' + n.learners + ' learners');
      if (n.asks !== 4) bad('expected 4 asks across learners, got ' + n.asks);
      if (n.reqs !== 2) bad('expected 2 requests across learners, got ' + n.reqs);
      if (n.learners !== 3) bad('expected 3 learners, got ' + n.learners);
      const txt = await p.evaluate(() => document.querySelector('#v-admin').innerText);
      ['Asha', 'Ravi', 'Mubaraka'].forEach(w => { if (txt.indexOf(w) < 0) bad('admin page does not name ' + w); });
      console.log('   names shown on rows: ' + ['Asha','Ravi','Mubaraka'].filter(w => txt.indexOf(w) >= 0).join(', '));
      const brief = await p.evaluate(() => askBrief());
      console.log('   brief covers ' + (brief.match(/^## /gm) || []).length + ' topics');
    } else {
      if (isAdmin) bad('learner was treated as admin');
      if (tabs.indexOf('admin') >= 0) bad('learner can see the Admin tab');
      // and cannot get there by hash
      await p.evaluate(() => { location.hash = 'admin'; go('admin'); }); await p.waitForTimeout(600);
      const route = await p.evaluate(() => S.route);
      console.log('   forcing the admin route lands on: ' + route);
      if (route === 'admin') bad('learner reached the admin route by hash');
      const adminVisible = await p.evaluate(() => {
        const v = document.querySelector('#v-admin'); return !!(v && v.offsetParent !== null); });
      if (adminVisible) bad('the admin view is visible to a learner');
      // a learner still has their own learning surfaces
      ['home','learn','bank','mock','progress'].forEach(t => { if (tabs.indexOf(t) < 0) bad('learner is missing the ' + t + ' tab'); });
    }
    console.log('   errors: ' + (errs.join(' | ') || 'none'));
    if (errs.length) fails++;
    await b.close();
  }
  console.log(fails ? '\nFAILURES: ' + fails : '\nowner sees every learner; a learner cannot reach Admin');
  process.exit(fails ? 1 : 0);
})();
