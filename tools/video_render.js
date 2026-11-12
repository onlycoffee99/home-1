// usage: node tools/video_render.js page.html outDir fps duration [stillTimes...]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [page_, out, fps, dur, ...stills] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'] }).catch(()=>chromium.launch({args:['--no-sandbox']}));
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(page_));
  await p.waitForTimeout(300);
  const times = stills.length ? stills.map(Number) : [...Array(Math.round(dur*fps)).keys()].map(i=>i/fps);
  let i = 0;
  for (const t of times) {
    await p.evaluate(t => window.render(t), t);
    await p.screenshot({ path: path.join(out, String(i++).padStart(5,'0') + '.jpg'), type:'jpeg', quality: 92 });
  }
  await b.close();
})();
