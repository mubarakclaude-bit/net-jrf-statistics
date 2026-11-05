// screenshots of each tab in both themes, plus a contrast audit of rendered text
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const W = '/home/claude/w1';

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1180, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto('file:///tmp/claude-0/harness.html');
  await page.waitForTimeout(900);
  // put some state in so the screens are not empty
  await page.evaluate(() => {
    const ids = (S.index && S.index.modules.inference) ? null : null;
    S.cfg = { exam: '2026-12-18', target: 150 };
  });
  await page.click('[data-tab="bank"]'); await page.waitForTimeout(800);
  await page.evaluate(() => {
    const l = S.bank.inference || [];
    l.forEach((q, i) => { if (i % 3) S.att[q.id] = { o: i % 4 ? 1 : 0, n: 1, t: Date.now() }; });
    S.mocks.push({ ts: Date.now() - 86400000 * 6, n: 50, c: 24, pass: 80, scope: 'P2', secs: 2100, byModule: { inference: { n: 20, c: 11 } } });
    S.mocks.push({ ts: Date.now() - 86400000 * 2, n: 50, c: 36, pass: 80, scope: 'P2', secs: 2000, byModule: { inference: { n: 22, c: 19 } } });
    S.errs = [{ qid: 'a', mid: 'inference', fmt: 'numeric', type: 'quantity', ts: Date.now(), stem: 'CRLB for lambda' },
              { qid: 'b', mid: 'inference', fmt: 'numeric', type: 'quantity', ts: Date.now(), stem: 'Fisher information' },
              { qid: 'c', mid: 'inference', fmt: 'multi', type: 'misread', ts: Date.now(), stem: 'completeness statements' },
              { qid: 'd', mid: 'inference', fmt: 'numeric', type: 'df', ts: Date.now(), stem: 'variance of UMVUE' },
              { qid: 'e', mid: 'inference', fmt: 'single', type: 'formula', ts: Date.now(), stem: 'exponential family form' },
              { qid: 'f', mid: 'inference', fmt: 'multi', type: 'gap', ts: Date.now(), stem: 'ancillary statistic' }];
    S.topics['inference-t1'] = { s: 2 }; S.topics['inference-t2'] = { s: 2 }; S.topics['inference-t3'] = { s: 1 };
    S.open.inference = true; S.notes.inference = false;
    render();
  });
  await page.waitForTimeout(300);

  const bad = [];
  function srgb(c){c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)}
  // contrast audit runs in-page
  const audit = async (label) => {
    const res = await page.evaluate(() => {
      const parse = s => { const m = String(s).match(/rgba?\(([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?/); return m ? [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]] : null; };
      const lin = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
      const L = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
      const bgOf = el => { let e = el; while (e) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c[3] > 0.5) return c; e = e.parentElement; } return [255,255,255,1]; };
      const out = [];
      document.querySelectorAll('#top *, main section.on *').forEach(el => {
        if (!el.offsetParent && el.tagName !== 'BODY') return;
        const t = Array.from(el.childNodes).filter(n => n.nodeType === 3 && n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
        if (!t) return;
        const cs = getComputedStyle(el); const fg = parse(cs.color); if (!fg) return;
        const bg = bgOf(el);
        const l1 = L(fg), l2 = L(bg);
        const cr = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
        const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 600;
        const need = (px >= 24 || (px >= 18.66 && bold)) ? 3 : 4.5;
        if (cr < need - 0.05) out.push({ sel: el.tagName.toLowerCase() + '.' + String(el.className).split(' ')[0], txt: t.slice(0, 32), cr: +cr.toFixed(2), need, px: Math.round(px) });
      });
      const seen = {}; return out.filter(o => { const k = o.sel + o.cr; if (seen[k]) return false; seen[k] = 1; return true; });
    });
    if (res.length) bad.push(label + ': ' + JSON.stringify(res));
  };

  for (const theme of ['light', 'dark']) {
    await page.evaluate(t => { document.documentElement.setAttribute('data-theme', t); }, theme);
    for (const t of ['home', 'learn', 'bank', 'mock', 'progress', 'admin']) {
      await page.click('[data-tab="' + t + '"]'); await page.waitForTimeout(t === 'bank' ? 600 : 300);
      if (t === 'bank') { await page.evaluate(() => { S.filt.mod = 'inference'; render(); }); await page.waitForTimeout(300); }
      await page.screenshot({ path: '/tmp/claude-0/shot-' + theme + '-' + t + '.png', fullPage: t === 'mock' || t === 'content' });
      await audit(theme + '/' + t);
    }
  }
  // drill screen
  await page.evaluate(() => { document.documentElement.setAttribute('data-theme', 'light'); });
  await page.click('[data-tab="bank"]'); await page.waitForTimeout(600);
  await page.locator('.qrow').nth(2).click(); await page.waitForTimeout(300);
  for (let i = 0; i < await page.locator('.vb.t').count(); i++) { await page.locator('.vb.t').nth(i).click(); await page.waitForTimeout(70); }
  await page.locator('.opt').nth(1).click(); await page.waitForTimeout(150);
  await page.click('#reveal').catch(()=>{}); await page.waitForTimeout(350);
  await page.screenshot({ path: '/tmp/claude-0/shot-light-drill.png', fullPage: true });
  await audit('light/drill');

  console.log(bad.length ? 'CONTRAST ISSUES:\n' + bad.join('\n') : 'contrast: all rendered text passes WCAG AA');
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
