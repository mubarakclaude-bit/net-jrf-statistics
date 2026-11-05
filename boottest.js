// Prove the page survives every way the runtime can let it down.
const fs=require('fs'); const { chromium } = require('playwright');
const base = fs.readFileSync('/tmp/claude-0/harness.html','utf8');
const scenarios = {
  'db never answers (hangs forever)':
    `window.claude={use:(n)=>n==='db'?new Promise(()=>{}):Promise.resolve(null)};`,
  'db resolves null (not granted)':
    `window.claude={use:()=>Promise.resolve(null)};`,
  'db slow: 4s then works':
    `const real=window.claude.use;window.claude={use:(n)=>n==='db'?new Promise(r=>setTimeout(()=>r(real(n)),4000)):real(n)};`,
  'sample hangs, db fine':
    `const real=window.claude.use;window.claude={use:(n)=>n==='sample'?new Promise(()=>{}):real(n)};`,
  'reads reject (no shared read access)':
    `const real=window.claude.use;window.claude={use:async(n)=>{const v=await real(n);
       if(n==='db')return {doc:p=>({get:()=>Promise.reject({code:'invalid_argument'}),set:()=>Promise.reject({code:'invalid_argument'}),onSnapshot:()=>()=>{},collection:()=>v.collection(p)}),collection:v.collection};
       return v}};`,
  'no claude object at all':
    `delete window.claude;`
};
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  for (const [name, patch] of Object.entries(scenarios)) {
    const html = base.replace('</head>', '</head>').replace(/(<body>)/, '$1');
    const file = '/tmp/claude-0/boot-' + name.replace(/\W+/g,'_') + '.html';
    // inject the patch AFTER the stub but BEFORE the page script
    fs.writeFileSync(file, html.replace('<div id="top">', '<script>'+patch+'</script><div id="top">'));
    const p = await b.newPage({ viewport: { width: 1100, height: 800 } });
    const errs=[]; p.on('pageerror', e=>errs.push(e.message));
    await p.goto('file://'+file);
    const t0=Date.now(); let settled=null;
    for (let i=0;i<40;i++){
      const txt=(await p.innerText('#v-home').catch(()=>'')).trim();
      if (txt && !/starting up|Connecting/.test(txt)) { settled={ms:Date.now()-t0,txt:txt.replace(/\s+/g,' ').slice(0,110)}; break; }
      await p.waitForTimeout(500);
    }
    console.log('• ' + name);
    console.log('   ' + (settled ? settled.ms+'ms → '+settled.txt : 'NEVER SETTLED (still showing the startup card after 20s)'));
    if (errs.length) console.log('   errors: '+errs.join(' | '));
    await p.close();
  }
  await b.close();
})();
