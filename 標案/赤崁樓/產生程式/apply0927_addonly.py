# -*- coding: utf-8 -*-
# 以使用者 1150927 版為底:補回修正 + 新增附件(履約實績佐證資料)
import re, sys, copy, docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.oxml import parse_xml
SRC, OUT = sys.argv[1], sys.argv[2]
d = docx.Document(SRC); body = d.element.body
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
sid = {s.style_id: s for s in d.styles}
def sty(name): return next(s for s in d.styles if s.name == name)
def ptext(el): return ''.join(t.text or '' for t in el.iter(qn('w:t')))
def add_runs(p, text):
    for i, seg in enumerate(re.split(r'【(.*?)】', text)):
        if seg:
            r = p.add_run(seg)
            if i % 2: r.font.highlight_color = 7
def mk_par(style, text):
    p = d.add_paragraph(style=style); add_runs(p, text); body.remove(p._p); return p._p
def set_cell(cell, text):
    ts = list(cell._tc.iter(qn('w:t')))
    ts[0].text = text; ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for t in ts[1:]: t.text = ''
def set_par(el, text):
    ts = list(el.iter(qn('w:t'))); ts[0].text = text
    for t in ts[1:]: t.text = ''
def mk_figure(imgs, caption, per_row):
    total = 8646
    t = d.add_table(rows=0, cols=per_row); body.remove(t._tbl)
    tp = t._tbl.tblPr
    for old in tp.findall(qn('w:tblW')) + tp.findall(qn('w:tblStyle')): tp.remove(old)
    for x in (f'<w:tblStyle xmlns:w="{W}" w:val="a9"/>', f'<w:tblW xmlns:w="{W}" w:w="{total}" w:type="dxa"/>', f'<w:jc xmlns:w="{W}" w:val="center"/>', f'<w:tblLayout xmlns:w="{W}" w:type="fixed"/>'):
        tp.append(parse_xml(x))
    order = ['tblStyle', 'tblW', 'jc', 'tblLayout', 'tblLook']
    kids = sorted(list(tp), key=lambda e: order.index(e.tag.split('}')[1]) if e.tag.split('}')[1] in order else 99)
    for k in list(tp): tp.remove(k)
    for k in kids: tp.append(k)
    cw = total // per_row
    for gc in t._tbl.tblGrid.findall(qn('w:gridCol')): gc.set(qn('w:w'), str(cw))
    for i in range(0, len(imgs), per_row):
        cells = t.add_row().cells
        for j, (path, wcm) in enumerate(imgs[i:i + per_row]):
            c = cells[j]; tcPr = c._tc.get_or_add_tcPr()
            for old in tcPr.findall(qn('w:tcW')): tcPr.remove(old)
            tcPr.append(parse_xml(f'<w:tcW xmlns:w="{W}" w:w="{cw}" w:type="dxa"/>'))
            tcPr.append(parse_xml(f'<w:vAlign xmlns:w="{W}" w:val="center"/>'))
            p = c.paragraphs[0]; p.alignment = 1; p.add_run().add_picture(path, width=Cm(wcm))
    for tr in t._tbl.findall(qn('w:tr')):
        tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit xmlns:w="{W}"/>'))
        for p in tr.iter(qn('w:p')):
            ppr = p.get_or_add_pPr(); idx = 1 if len(ppr) and ppr[0].tag == qn('w:pStyle') else 0
            ppr.insert(idx, parse_xml(f'<w:keepNext xmlns:w="{W}"/>'))
    cap = t.add_row().cells
    m = cap[0].merge(cap[-1]) if per_row > 1 else cap[0]
    p = m.paragraphs[0]; p.style = sid['a']; add_runs(p, caption)
    ppr = p._p.get_or_add_pPr(); ppr.insert(1, parse_xml(f'<w:numPr xmlns:w="{W}"><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'))
    return t._tbl

# (原文不動,只新增附件;115/9/27 老闆指示)

# ---- 3. 附件:履約實績佐證資料 ----
sect = body.find(qn('w:sectPr')); last = sect.getprevious()
els = [parse_xml(f'<w:p xmlns:w="{W}"><w:r><w:br w:type="page"/></w:r></w:p>'),
       mk_par(sty('A-01-壹'), '附件'),
       mk_par(sty('A-02-一'), '履約實績佐證資料'),
       mk_par(sty('B-02-一文'), '以下依「鑫和洋行近年業務實績一覽表」項次，檢附相關契約、公證文件及現場照片影本，以資佐證。')]
FIG = [
 ([('img/jx.jpg', 14)], '附件1-1　礁溪溫泉公園進駐合約書(甲方：輕車悠遊股份有限公司；乙方：鑫和洋行；合約期間112年2月1日至117年10月30日)', 1),
 ([('img/lease.jpg', 11)], '附件1-2　時間到咖啡館台中館租賃契約公證書(115年3月20日，臺灣臺中地方法院所屬民間公證人)', 1),
 ([('img/handover.jpg', 11)], '附件1-3　臺中市第二市場停車場附屬空間委託經營案點交簽到表(114年12月22日)', 1),
 ([('img/open1.jpg', 7.4), ('img/open2.jpg', 7.4)], '附件1-4　時間到咖啡館台中館開幕活動(2026年9月19日，臺中市停車管理處、中區區公所出席)', 2),
 ([('img/dripbag.jpg', 5.4), ('img/kumquat.jpg', 5.4), ('img/callig_pack.jpg', 3.9)], '附件1-5　自有品牌商品：舞荳掛耳咖啡、宜蘭金棗黑糖金磚、舞荳單品咖啡包裝', 3),
 ([('img/test1.jpg', 5.8), ('img/test2.jpg', 5.8)], '附件1-6　委託財團法人金屬工業研究發展中心產品成分分析報告(2019年3月)', 2),
 ([('img/course1.jpg', 7.4), ('img/course2.jpg', 7.4)], '附件1-7　國安一期社會住宅咖啡手沖體驗課程(2026年9月5日，講師鄭玉屏)', 2),
]
for imgs, cap, n in FIG:
    els.append(mk_figure(imgs, cap, n))
    els.append(mk_par(sid['af4'], '資料來源：本計畫彙整'))
for e in els:
    last.addnext(e); last = e

dps = list(body.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr'))
seen = set(); mx = max(int(x.get('id')) for x in dps)
for dp in dps:  # 只調整重複的 id,原有圖片不動
    if dp.get('id') in seen: mx += 1; dp.set('id', str(mx))
    seen.add(dp.get('id'))
d.save(OUT); print('saved')
