const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(900);
  const audit = async label => {
    const res = await p.evaluate(() => {
      const parse = s => { const m = String(s).match(/rgba?\(([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?/); return m ? [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]] : null; };
      const lin = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
      const L = ([r, g, bb]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(bb);
      const bgOf = el => { let e = el; while (e) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c[3] > 0.5) return c; e = e.parentElement; } return [255,255,255,1]; };
      const out = [];
      document.querySelectorAll('#top *, main section.on *').forEach(el => {
        if (!el.offsetParent) return;
        const t = Array.from(el.childNodes).filter(n => n.nodeType === 3 && n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
        if (!t) return;
        const cs = getComputedStyle(el); const fg = parse(cs.color); if (!fg) return;
        const cr = (Math.max(L(fg), L(bgOf(el))) + 0.05) / (Math.min(L(fg), L(bgOf(el))) + 0.05);
        const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 600;
        const need = (px >= 24 || (px >= 18.66 && bold)) ? 3 : 4.5;
        if (cr < need - 0.05) out.push(el.tagName.toLowerCase()+'.'+String(el.className).split(' ')[0]+' "'+t.slice(0,26)+'" '+cr.toFixed(2));
      });
      return [...new Set(out)];
    });
    if (res.length) console.log('FAIL ' + label + ': ' + res.join(' | '));
  };
  for (const theme of ['light', 'dark']) {
    await p.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
    await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
    await p.evaluate(() => { S.open.inference = true; render(); }); await p.waitForTimeout(250);
    await audit(theme + '/tree');
    await p.click('[data-topic="inference-t4"]'); await p.waitForTimeout(700);
    await audit(theme + '/overview');
    for (const i of [0,1,2,3,5,7,9,10,12,13]) {
      await p.evaluate(k => gotoScene(k), i); await p.waitForTimeout(260);
      await audit(theme + '/scene' + (i+1));
    }
    await p.click('[data-tab="admin"]'); await p.waitForTimeout(400); await audit(theme + '/admin');
  }
  console.log('contrast audit complete');
  await b.close();
})();
