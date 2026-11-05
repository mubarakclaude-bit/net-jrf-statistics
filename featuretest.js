// Notes, the request modal with attachments, and picking a mock by time.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1500);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(900); }

  console.log('--- notes ---');
  await p.evaluate(() => openTopic('inference-t1')); await p.waitForTimeout(1000);
  await p.evaluate(() => gotoScene(2)); await p.waitForTimeout(450);
  await p.evaluate(() => document.querySelector('[data-noteopen]').click()); await p.waitForTimeout(400);
  await p.evaluate(() => { document.querySelector('#noteBox').value = 'Indicator goes INSIDE g when the support moves.'; });
  await p.evaluate(() => document.querySelector('[data-notesave]').click()); await p.waitForTimeout(1600);   // save() is debounced
  const n = await p.evaluate(() => ({ stored: Object.keys(S.notes).length,
    railFlags: document.querySelectorAll('.wsnav .noteflag').length,
    headerChip: !!document.querySelector('.railmeta .chip.ac'),
    written: !!(window.__writes || []).filter(w => /notes/.test(w[1])).length }));
  console.log('  saved=' + n.stored + '  flag in the rail=' + n.railFlags + '  count on the rail header=' + n.headerChip + '  persisted=' + n.written);
  const tree = await p.evaluate(async () => { resetLearn(null); S.open.inference = true; render();
    await new Promise(r => setTimeout(r, 300));
    const row = document.querySelector('[data-topic="inference-t1"]');
    return row ? row.innerText.replace(/\n+/g, ' | ') : 'no row'; });
  console.log('  topic row in the tree: ' + JSON.stringify(tree.slice(0, 95)));

  console.log('--- request modal ---');
  await p.evaluate(() => openTopic('inference-t1')); await p.waitForTimeout(900);
  await p.evaluate(() => gotoScene(0)); await p.waitForTimeout(400);
  console.log('  Ask button in the scene bar: ' + await p.locator('.scbar [data-reqopen]').count());
  await p.evaluate(() => document.querySelector('.scbar [data-reqopen]').click()); await p.waitForTimeout(450);
  const m = await p.evaluate(() => { const d = document.querySelector('.modal'); if (!d) return { open: false };
    return { open: true, purpose: (d.querySelector('.modalwhy') || {}).textContent.trim().slice(0, 70),
             kinds: d.querySelectorAll('[data-reqkind]').length, fileInput: !!d.querySelector('#reqFiles'),
             section: (d.querySelector('.kv b') || {}).textContent }; });
  console.log('  ' + JSON.stringify(m));
  // attach a small file through the real input
  await p.setInputFiles('#reqFiles', { name: 'assignment.txt', mimeType: 'text/plain', buffer: Buffer.from('Q3 and Q7 please') });
  await p.waitForTimeout(500);
  const f = await p.evaluate(() => (S.reqModal.files || []).map(x => x.name + ' kept=' + x.kept));
  console.log('  attachment: ' + JSON.stringify(f));
  await p.evaluate(() => { document.querySelector('#reqText').value = 'Please add a worked example on the shifted exponential.'; });
  await p.evaluate(() => document.querySelector('#reqSend').click()); await p.waitForTimeout(600);
  const r = await p.evaluate(() => ({ filed: S.reqs.length, closed: !document.querySelector('.modal'),
    last: S.reqs[S.reqs.length - 1] }));
  console.log('  filed=' + r.filed + ' modal closed=' + r.closed +
              ' against "' + r.last.scene + '" kind=' + r.last.kind + ' files=' + (r.last.files || []).length);
  const adm = await p.evaluate(async () => { go('admin'); await new Promise(x => setTimeout(x, 500));
    const rows = document.querySelectorAll('.reqrow');
    return { rows: rows.length, brief: typeof reqBrief === 'function' ? reqBrief().length : 0 }; });
  console.log('  Admin shows ' + adm.rows + ' request row(s); authoring brief is ' + adm.brief + ' chars');

  console.log('--- mock by time ---');
  await p.evaluate(() => go('mock')); await p.waitForTimeout(600);
  const mk = await p.evaluate(() => { const s = document.querySelector('#mkMins');
    return { opts: [...s.options].map(o => o.text), sel: s.value, nLocked: document.querySelector('#mkN').disabled,
             nShown: document.querySelector('#mkN').value }; });
  console.log('  options: ' + JSON.stringify(mk.opts.slice(0, 5)));
  const lbl = await p.evaluate(() => (document.querySelector('#mkCount')||{}).textContent);
  console.log('  default ' + mk.sel + ' min -> ' + JSON.stringify(lbl) + ', manual count locked = ' + mk.nLocked);
  await p.evaluate(() => { const s = document.querySelector('#mkMins'); s.value = '0'; s.onchange(); });
  await p.waitForTimeout(250);
  console.log('  "no limit" unlocks the manual count: ' + await p.evaluate(() => !document.querySelector('#mkN').disabled));
  console.log(errs.length ? errs.join('\n') : 'no runtime errors');
  await b.close();
})();
