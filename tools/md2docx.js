// md2docx.js — 將 Markdown 轉為中文排版之 Word 檔
// 用法: node md2docx.js input.md output.docx "文件標題"
const fs = require('fs');
const { marked } = require('marked');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, WidthType, AlignmentType, BorderStyle, ShadingType,
  LevelFormat, convertMillimetersToTwip,
} = require('docx');

const [,, inFile, outFile] = process.argv;
const md = fs.readFileSync(inFile, 'utf8')
  // 去除 YAML front matter
  .replace(/^---\n[\s\S]*?\n---\n/, '');

const FONT = 'Microsoft JhengHei';
const PAGE_W = 11906, MARGIN = 1080; // A4, 邊界 1.9cm
const CONTENT_W = PAGE_W - MARGIN * 2; // 9746 DXA

function inlineRuns(tokens, extra = {}) {
  const runs = [];
  const walk = (toks, style) => {
    for (const t of toks || []) {
      if (t.type === 'strong') walk(t.tokens, { ...style, bold: true });
      else if (t.type === 'em') walk(t.tokens, { ...style, italics: true });
      else if (t.type === 'del') walk(t.tokens, { ...style, strike: true });
      else if (t.type === 'codespan') runs.push(new TextRun({ text: t.text, font: 'Consolas', size: extra.size || 21, ...style }));
      else if (t.type === 'link') walk(t.tokens, { ...style, color: '1155CC' });
      else if (t.type === 'br') runs.push(new TextRun({ text: '', break: 1 }));
      else if (t.type === 'text' || t.type === 'escape') {
        if (t.tokens) { walk(t.tokens, style); continue; }
        // 表格儲存格內的 <br> 換行
        const parts = String(t.text).replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#39;/g,"'").replace(/&quot;/g,'"').split(/<br\s*\/?>/i);
        parts.forEach((p, i) => {
          if (i > 0) runs.push(new TextRun({ text: '', break: 1 }));
          if (p) runs.push(new TextRun({ text: p, font: FONT, size: extra.size || 21, ...style }));
        });
      } else if (t.type === 'html') { /* 略過原始 html 標籤 */ }
      else if (t.text) runs.push(new TextRun({ text: t.text, font: FONT, size: extra.size || 21, ...style }));
    }
  };
  walk(tokens, {});
  return runs;
}

function makeTable(tok) {
  const nCols = tok.header.length;
  let widths;
  if (nCols === 2) widths = [Math.round(CONTENT_W * 0.22), Math.round(CONTENT_W * 0.78)];
  else if (nCols === 3) widths = [Math.round(CONTENT_W * 0.12), Math.round(CONTENT_W * 0.58), Math.round(CONTENT_W * 0.30)];
  else widths = Array(nCols).fill(Math.round(CONTENT_W / nCols));
  const total = widths.reduce((a, b) => a + b, 0);
  widths[nCols - 1] += CONTENT_W - total;

  const mkCell = (cellTok, w, isHeader) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: isHeader ? { type: ShadingType.CLEAR, fill: 'E8EDF5' } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      children: inlineRuns(cellTok.tokens, { size: 20 }),
      spacing: { before: 20, after: 20 },
    })],
  });

  const rows = [new TableRow({
    tableHeader: true,
    children: tok.header.map((h, i) => {
      const c = mkCell(h, widths[i], true);
      return c;
    }),
  })];
  for (const r of tok.rows) rows.push(new TableRow({ children: r.map((c, i) => mkCell(c, widths[i], false)) }));
  return new Table({ columnWidths: widths, width: { size: CONTENT_W, type: WidthType.DXA }, rows });
}

const children = [];
const push = (el) => children.push(el);
const HL = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3, 4: HeadingLevel.HEADING_4 };

function handle(tokens, ctx = {}) {
  for (const tok of tokens) {
    if (tok.type === 'heading') {
      push(new Paragraph({ heading: HL[Math.min(tok.depth, 4)], spacing: { before: tok.depth <= 2 ? 240 : 180, after: 100 }, children: inlineRuns(tok.tokens, { size: tok.depth === 1 ? 32 : tok.depth === 2 ? 28 : 24 }) }));
    } else if (tok.type === 'paragraph') {
      push(new Paragraph({ spacing: { after: 120, line: 300 }, children: inlineRuns(tok.tokens) }));
    } else if (tok.type === 'table') {
      push(makeTable(tok));
      push(new Paragraph({ children: [], spacing: { after: 60 } }));
    } else if (tok.type === 'blockquote') {
      for (const sub of tok.tokens) {
        if (sub.type === 'paragraph') {
          push(new Paragraph({
            indent: { left: 360 },
            border: { left: { style: BorderStyle.SINGLE, size: 18, color: '8899AA', space: 8 } },
            shading: { type: ShadingType.CLEAR, fill: 'F4F6F8' },
            spacing: { after: 100, line: 300 },
            children: inlineRuns(sub.tokens),
          }));
        } else handle([sub]);
      }
    } else if (tok.type === 'list') {
      let idx = 0;
      for (const item of tok.items) {
        idx++;
        const marker = tok.ordered ? `${(tok.start || 1) + idx - 1}. ` : '';
        const first = item.tokens.find(t => t.type === 'paragraph' || t.type === 'text');
        const runs = first ? inlineRuns(first.tokens || [first]) : [];
        push(new Paragraph({
          numbering: tok.ordered ? undefined : { reference: 'bullets', level: 0 },
          indent: tok.ordered ? { left: 420, hanging: 360 } : undefined,
          spacing: { after: 60, line: 280 },
          children: tok.ordered ? [new TextRun({ text: marker, font: FONT, size: 21 }), ...runs] : runs,
        }));
        // 巢狀內容
        for (const t of item.tokens) {
          if (t !== first && (t.type === 'table' || t.type === 'list' || t.type === 'blockquote')) handle([t]);
        }
      }
    } else if (tok.type === 'hr') {
      push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '999999' } }, spacing: { before: 120, after: 160 }, children: [] }));
    } else if (tok.type === 'space') { /* skip */ }
    else if (tok.tokens) handle(tok.tokens);
  }
}

handle(marked.lexer(md));

const doc = new Document({
  numbering: {
    config: [{
      reference: 'bullets',
      levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 420, hanging: 210 } } } }],
    }],
  },
  styles: {
    default: {
      document: { run: { font: FONT, size: 21 } },
      heading1: { run: { font: FONT, size: 32, bold: true, color: '1A1A2E' } },
      heading2: { run: { font: FONT, size: 28, bold: true, color: '1F3864' } },
      heading3: { run: { font: FONT, size: 24, bold: true, color: '2E4A7A' } },
      heading4: { run: { font: FONT, size: 22, bold: true, color: '444444' } },
    },
  },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 16838 }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(outFile, buf); console.log('WROTE', outFile, buf.length, 'bytes'); });
