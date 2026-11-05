// UI regressions for the redesign: live WCAG AA contrast in both themes, the scene
// rail being present and navigable, and the sticky chrome staying put while scrolling.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const errs = [];
  for (const theme of ['light', 'dark']) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
    await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1300);
    if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }
    await p.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
    await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
    await p.evaluate(() => { S.open.inference = true; render(); }); await p.waitForTimeout(250);
    await p.evaluate(() => openTopic('inference-t5')); await p.waitForTimeout(800);

    // --- the scene rail ---
    await p.evaluate(() => gotoScene(2)); await p.waitForTimeout(400);
    const rail = await p.evaluate(() => {
      const steps = [...document.querySelectorAll('.wsnav .steprow .step')];
      const cur = document.querySelector('.wsnav .steprow.cur');
      const r = cur && cur.getBoundingClientRect(), nav = document.querySelector('.wsnav').getBoundingClientRect();
      return { n: steps.length, cur: cur ? cur.innerText.split('\n')[0] : null,
               inView: !!(r && r.top >= nav.top - 1 && r.bottom <= nav.bottom + 1),
               clickable: steps.every(s => s.hasAttribute('data-sc')),
               ticks: document.querySelectorAll('.wsnav [data-seen]').length,
               want: (S.lessons[S.learn.topicId]||{scenes:[]}).scenes.length };
    });
    if (theme === 'light')
      console.log('rail: ' + rail.n + ' steps (lesson has ' + rail.want + '), current = ' + JSON.stringify(rail.cur) +
                  ', every step clickable = ' + rail.clickable + ', per-scene ticks = ' + rail.ticks +
                  ', current scrolled into view = ' + rail.inView);
    // jumping from the rail must change the scene
    const jumped = await p.evaluate(async () => {
      document.querySelector('.wsnav .steprow .step[data-sc="8"]').click();
      await new Promise(r => setTimeout(r, 300));
      return { i: S.learn.i, title: document.querySelector('.pane h1').textContent };
    });
    if (theme === 'light') console.log('clicked step 9 in the rail -> scene index ' + jumped.i + ', ' + JSON.stringify(jumped.title));

    // --- sticky chrome survives a scroll ---
    const sticky = await p.evaluate(async () => {
      window.scrollTo(0, 1200); document.querySelector('.wscanvas').scrollTop = 1200;
      await new Promise(r => setTimeout(r, 250));
      const hd = document.querySelector('.scbar').getBoundingClientRect();
      const ft = document.querySelector('.scnav').getBoundingClientRect();
      return { headerTop: Math.round(hd.top), footerBottom: Math.round(innerHeight - ft.bottom) };
    });
    if (theme === 'light') console.log('after scrolling: header top = ' + sticky.headerTop + 'px, continue bar bottom gap = ' + sticky.footerBottom + 'px');

    // --- live contrast of every text node against its painted background ---
    const bad = await p.evaluate(() => {
      const L = c => { c /= 255; return c <= .04045 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4) };
      const rgb = s => (s.match(/[\d.]+/g) || []).map(Number);
      const lum = s => { const [r, g, bl] = rgb(s); return .2126 * L(r) + .7152 * L(g) + .0722 * L(bl) };
      const bgOf = el => { let n = el; while (n && n !== document.documentElement) {
          const c = getComputedStyle(n).backgroundColor, a = rgb(c)[3];
          if (c && c !== 'transparent' && (a === undefined || a > .5)) return c; n = n.parentElement; }
        return getComputedStyle(document.body).backgroundColor };
      const out = [];
      for (const el of document.querySelectorAll('.ws *')) {
        if (!el.offsetParent && getComputedStyle(el).position !== 'sticky') continue;
        const txt = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
        if (!txt) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || +cs.opacity < .6) continue;
        const fs = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
        const need = (fs >= 24 || (fs >= 18.66 && bold)) ? 3 : 4.5;
        const lf = lum(cs.color), lb = lum(bgOf(el));
        const cr = (Math.max(lf, lb) + .05) / (Math.min(lf, lb) + .05);
        if (cr < need) out.push({ t: txt.slice(0, 44), cls: el.className.toString().slice(0, 28), cr: +cr.toFixed(2), need, fs });
      }
      return out;
    });
    console.log(theme + ' contrast: ' + bad.length + ' failures' + (bad.length ? '\n  ' + bad.slice(0, 8).map(x => `${x.cr} (need ${x.need}) .${x.cls} "${x.t}"`).join('\n  ') : ''));
    await p.close();
  }
  console.log(errs.length ? '--- ' + errs.join('\n') : 'no runtime errors');
  await b.close();
})();
