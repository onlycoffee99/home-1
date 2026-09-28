// HTML(A4 等 @page 紙張)→ 300 dpi 點陣 PNG + 300 dpi 點陣 PDF(給要求「300dpi 圖檔」的印刷店)。
// 用法:node tools/html2print300.js 輸入.html 輸出前綴 [dpi]
//   產出 <前綴>.png 與 <前綴>.pdf;dpi 預設 300。
// 註:html2pdf.js 產出的是向量 PDF(文字線條放大不糊,品質最好);本工具只在印刷店指定要點陣圖時使用。
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
(async () => {
  const [, , input, prefix, dpiArg] = process.argv;
  if (!input || !prefix) { console.error('用法:node tools/html2print300.js 輸入.html 輸出前綴 [dpi]'); process.exit(1); }
  const dpi = Number(dpiArg) || 300;
  const opts = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] } : {};
  const b = await chromium.launch(opts);
  // CSS 1px = 1/96 吋,所以縮放倍率 = dpi/96
  const ctx = await b.newContext({ ignoreHTTPSErrors: true, deviceScaleFactor: dpi / 96 });
  const p = await ctx.newPage();
  await p.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await p.emulateMedia({ media: 'print' });
  const box = await p.evaluate(() => { const e = document.body.firstElementChild; const r = e.getBoundingClientRect(); return { w: r.width, h: r.height }; });
  await p.setViewportSize({ width: Math.round(box.w), height: Math.round(box.h) });
  const png = prefix + '.png';
  await p.screenshot({ path: png, clip: { x: 0, y: 0, width: box.w, height: box.h } });
  // 把 PNG 以原尺寸(mm)放進 PDF,Chromium 會保留原圖像素
  const wmm = box.w * 25.4 / 96, hmm = box.h * 25.4 / 96;
  const data = fs.readFileSync(png).toString('base64');
  const q = await ctx.newPage();
  await q.setContent(`<style>@page{size:${wmm}mm ${hmm}mm;margin:0}body{margin:0}img{display:block;width:${wmm}mm;height:${hmm}mm}</style><img src="data:image/png;base64,${data}">`);
  await q.pdf({ path: prefix + '.pdf', preferCSSPageSize: true, printBackground: true });
  await b.close();
  console.log(`已產出 ${png}、${prefix}.pdf(${dpi} dpi,${Math.round(wmm)}×${Math.round(hmm)} mm)`);
})();
