// HTML(用 CSS @page 設定紙張大小)→ PDF,並另存第一頁 PNG 預覽。
// 用法:node tools/html2pdf.js 輸入.html 輸出.pdf [預覽.png]
// 雲端環境:Playwright 已預裝,Chromium 在 /opt/pw-browsers;Google Fonts 需經 proxy。
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
(async () => {
  const [, , input, pdf, png] = process.argv;
  if (!input || !pdf) { console.error('用法:node tools/html2pdf.js 輸入.html 輸出.pdf [預覽.png]'); process.exit(1); }
  const opts = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] } : {};
  const b = await chromium.launch(opts);
  const ctx = await b.newContext({ ignoreHTTPSErrors: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  await p.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await p.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  if (png) {
    const box = await p.evaluate(() => { const e = document.body.firstElementChild; const r = e.getBoundingClientRect(); return { w: Math.ceil(r.width), h: Math.ceil(r.height) }; });
    await p.setViewportSize({ width: box.w, height: box.h });
    await p.screenshot({ path: png });
  }
  await b.close();
  console.log('已產出 ' + pdf + (png ? '、' + png : ''));
})();
