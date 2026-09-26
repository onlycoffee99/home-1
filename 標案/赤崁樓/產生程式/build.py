# -*- coding: utf-8 -*-
import re, copy, sys
import docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
from content import S

SRC, OUT = sys.argv[1], sys.argv[2]
d = docx.Document(SRC)
body = d.element.body
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

STY = {'h2': 'A-02-一', 'h3': 'A-03-(一)', 'h4': 'A-04-1', 'h4c': 'A-04-1',
       'p2': 'B-02-一文', 'p3': 'B-03-(一)文', 'p4': 'B-04-1文',
       'tcap': 'C-02-表名', 'tsrc': 'D-05-資料來源', 'fsrc': '資料來源', 'cap': 'a'}
style_by_id = {s.style_id: s for s in d.styles}
def sty(name):
    for s in d.styles:
        if s.name == name: return s
    raise KeyError(name)
CELL = style_by_id['D-02-']
CAP = style_by_id['a']

# ---- numbering: new num (restart) for each h4 group ----
numbering = d.part.numbering_part.element
def new_num(start=1):
    ids = [int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))]
    nid = max(ids) + 1
    last_num = numbering.findall(qn('w:num'))[-1]
    last_num.addnext(parse_xml(
        f'<w:num xmlns:w="{W}" w:numId="{nid}"><w:abstractNumId w:val="3"/>'
        f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="{start}"/></w:lvlOverride></w:num>'))
    return nid

def add_runs(p, text):
    for i, seg in enumerate(re.split(r'【(.*?)】', text)):
        if not seg: continue
        r = p.add_run(seg)
        if i % 2:
            r.font.highlight_color = 7  # yellow

def mk_par(style, text):
    p = d.add_paragraph(style=style)
    add_runs(p, text)
    body.remove(p._p)
    return p._p

def mk_table(ratios, header, rows):
    total = 9600
    ws = [round(total * r / sum(ratios)) for r in ratios]
    t = d.add_table(rows=1 + len(rows), cols=len(ws))
    body.remove(t._tbl)
    tp = t._tbl.tblPr
    tp.append(parse_xml(f'<w:tblStyle xmlns:w="{W}" w:val="a9"/>'))
    for tag in ('w:tblW',):
        for e in tp.findall(qn(tag)): tp.remove(e)
    tp.append(parse_xml(f'<w:tblW xmlns:w="{W}" w:w="{total}" w:type="dxa"/>'))
    tp.append(parse_xml(f'<w:jc xmlns:w="{W}" w:val="center"/>'))
    # reorder tblPr children per schema: tblStyle, tblW, jc, tblLook
    order = ['tblStyle', 'tblpPr', 'tblOverlap', 'bidiVisual', 'tblStyleRowBandSize', 'tblStyleColBandSize', 'tblW', 'jc', 'tblCellSpacing', 'tblInd', 'tblBorders', 'shd', 'tblLayout', 'tblCellMar', 'tblLook']
    kids = sorted(list(tp), key=lambda e: order.index(e.tag.split('}')[1]) if e.tag.split('}')[1] in order else 99)
    for k in list(tp): tp.remove(k)
    for k in kids: tp.append(k)
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn('w:gridCol')), ws): gc.set(qn('w:w'), str(w))
    for ri, row in enumerate([header] + rows):
        tr = t.rows[ri]
        if ri == 0:
            trPr = tr._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:tblHeader xmlns:w="{W}"/>'))
        bold_row = ri > 0 and row[0].strip() in ('合計', '營業收入合計', '成本及費用合計', '稅前損益', '總投入資金', '開辦小計', '營業收入', '營業成本及費用')
        for ci, txt in enumerate(row):
            c = tr.cells[ci]
            tcPr = c._tc.get_or_add_tcPr()
            for old in tcPr.findall(qn('w:tcW')): tcPr.remove(old)
            tcPr.append(parse_xml(f'<w:tcW xmlns:w="{W}" w:w="{ws[ci]}" w:type="dxa"/>'))
            if ri == 0:
                tcPr.append(parse_xml(f'<w:shd xmlns:w="{W}" w:val="clear" w:color="auto" w:fill="D9D9D9"/>'))
            tcPr.append(parse_xml(f'<w:vAlign xmlns:w="{W}" w:val="center"/>'))
            p = c.paragraphs[0]
            p.style = CELL
            pPr = p._p.get_or_add_pPr()
            pPr.append(parse_xml(f'<w:spacing xmlns:w="{W}" w:line="380" w:lineRule="exact"/>'))
            short = len(re.sub(r'[【】]', '', txt)) <= 6 or re.fullmatch(r'[\d,.%～\-－—／/()（）元人場日次時分以上內下]+', txt or '-')
            num = re.fullmatch(r'-?\d{1,3}(,\d{3})+|[\d.]+%', txt)
            align = 'center' if ri == 0 or (short and not num) else ('right' if num else 'left')
            pPr.append(parse_xml(f'<w:jc xmlns:w="{W}" w:val="{align}"/>'))
            add_runs(p, txt)
            if bold_row or ri == 0:
                for r in p.runs: r.bold = True
    return t._tbl

def mk_figure(imgs, caption, per_row):
    total = 8646
    t = d.add_table(rows=0, cols=per_row)
    body.remove(t._tbl)
    tp = t._tbl.tblPr
    for old in tp.findall(qn('w:tblW')) + tp.findall(qn('w:tblStyle')): tp.remove(old)
    tp.append(parse_xml(f'<w:tblStyle xmlns:w="{W}" w:val="a9"/>'))
    tp.append(parse_xml(f'<w:tblW xmlns:w="{W}" w:w="{total}" w:type="dxa"/>'))
    tp.append(parse_xml(f'<w:jc xmlns:w="{W}" w:val="center"/>'))
    tp.append(parse_xml(f'<w:tblLayout xmlns:w="{W}" w:type="fixed"/>'))
    order = ['tblStyle', 'tblW', 'jc', 'tblLayout', 'tblLook']
    kids = sorted(list(tp), key=lambda e: order.index(e.tag.split('}')[1]) if e.tag.split('}')[1] in order else 99)
    for k in list(tp): tp.remove(k)
    for k in kids: tp.append(k)
    cw = total // per_row
    for gc in t._tbl.tblGrid.findall(qn('w:gridCol')): gc.set(qn('w:w'), str(cw))
    for i in range(0, len(imgs), per_row):
        cells = t.add_row().cells
        for j, (path, wcm) in enumerate(imgs[i:i + per_row]):
            c = cells[j]
            tcPr = c._tc.get_or_add_tcPr()
            for old in tcPr.findall(qn('w:tcW')): tcPr.remove(old)
            tcPr.append(parse_xml(f'<w:tcW xmlns:w="{W}" w:w="{cw}" w:type="dxa"/>'))
            tcPr.append(parse_xml(f'<w:vAlign xmlns:w="{W}" w:val="center"/>'))
            p = c.paragraphs[0]
            p.alignment = 1
            p.add_run().add_picture(path, width=Cm(wcm))
    for tr in t._tbl.findall(qn('w:tr')):
        tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit xmlns:w="{W}"/>'))
        for p in tr.iter(qn('w:p')):
            ppr = p.get_or_add_pPr()
            idx = 1 if len(ppr) and ppr[0].tag == qn('w:pStyle') else 0
            ppr.insert(idx, parse_xml(f'<w:keepNext xmlns:w="{W}"/>'))
    cap = t.add_row().cells
    m = cap[0].merge(cap[-1]) if per_row > 1 else cap[0]
    p = m.paragraphs[0]
    p.style = CAP
    add_runs(p, caption)
    return t._tbl

def build(blocks):
    els, cur_num = [], None
    for b in blocks:
        k = b[0]
        if k in ('h2', 'h3'):
            cur_num = None
        if k == 'h4c':
            if cur_num is None: cur_num = new_num(3)
            k = 'h4'
        if k in ('h2', 'h3', 'p2', 'p3', 'p4', 'tcap', 'tsrc', 'fsrc'):
            els.append(mk_par(sty(STY[k]), b[1]))
        elif k == 'h4':
            if cur_num is None: cur_num = new_num()
            e = mk_par(sty(STY[k]), b[1])
            e.get_or_add_pPr().append(parse_xml(
                f'<w:numPr xmlns:w="{W}"><w:ilvl w:val="0"/><w:numId w:val="{cur_num}"/></w:numPr>'))
            # numPr must follow pStyle
            pPr = e.pPr; np_ = pPr.find(qn('w:numPr')); pPr.remove(np_); pPr.insert(1, np_)
            els.append(e)
        elif k == 'table':
            els.append(mk_table(*b[1:]))
        elif k == 'fig':
            els.append(mk_figure(*b[1:]))
        else:
            raise ValueError(k)
    return els

def ptext(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t')))

def is_blank(el):
    return el.tag == qn('w:p') and not ptext(el).strip() and not el.findall('.//' + qn('w:br')) \
        and not el.findall('.//' + qn('w:drawing')) and el.find('.//' + qn('w:sectPr')) is None

def find_par(pred):
    for el in body.iterchildren(qn('w:p')):
        if pred(ptext(el)): return el
    raise LookupError

def insert_after(anchor, els, drop_blank=True):
    if drop_blank:
        nxt = anchor.getnext()
        while nxt is not None and is_blank(nxt):
            n2 = nxt.getnext(); body.remove(nxt); nxt = n2
    for e in els:
        anchor.addnext(e); anchor = e
    return anchor

def set_text(el, new):
    ts = list(el.iter(qn('w:t')))
    ts[0].text = new
    ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for t in ts[1:]: t.text = ''

# ---------- 1. 文字修正 ----------
TAG = re.compile(r'[(（](淑湄|鄭姊|鄭姐|袁小姐、鄭小姐)[)）]')
for el in body.iter(qn('w:p')):
    s = ptext(el)
    ns = TAG.sub('', s).replace('159房屋交易網', '591房屋交易網').replace('赤嵌樓', '赤崁樓').replace('停\t留', '停留')
    if ns != s:
        if TAG.search(s) and '目錄' not in s:
            # 目錄列(含頁碼)只改文字 run,避免動到欄位碼
            for t in el.iter(qn('w:t')):
                t.text = TAG.sub('', t.text or '')
            if ptext(el) != ns:  # 標籤被拆在多個 run
                txt = ptext(el)
                set_text(el, ns) if el.find('.//' + qn('w:fldChar')) is None else None
        if ptext(el) != ns and el.find('.//' + qn('w:fldChar')) is None:
            # 以逐 run 取代為先,不行才整段合併
            for t in el.iter(qn('w:t')):
                t.text = (t.text or '').replace('159房屋交易網', '591房屋交易網').replace('赤嵌樓', '赤崁樓')
            if ptext(el) != ns:
                set_text(el, ns)
# 目錄內若標籤跨 run
for el in body.iter(qn('w:p')):
    s = ptext(el)
    if TAG.search(s):
        ts = list(el.iter(qn('w:t')))
        joined = ''.join(t.text or '' for t in ts)
        m = TAG.search(joined)
        # 刪除跨 run 的字元
        pos, a, b = 0, m.start(), m.end()
        for t in ts:
            tx = t.text or ''
            s0, s1 = pos, pos + len(tx)
            keep = ''.join(ch for i, ch in enumerate(tx) if not (a <= s0 + i < b))
            t.text = keep; pos = s1

# ---------- 2. 各章節插入 ----------
H = lambda key: (lambda s: s.strip() == key)
insert_after(find_par(H('前言')), build(S['前言']))
insert_after(find_par(lambda s: s.startswith('鑫和洋行營運長鄭玉屏小姐')), build(S['舞荳品牌']), drop_blank=False)

ph = find_par(lambda s: s.startswith('履約實績(待鄭姐提供)'))
insert_after(ph, build(S['履約實績']), drop_blank=False)
body.remove(ph)

h_co = find_par(lambda s: s.strip() == '協力廠商')
set_text(h_co, '協力人員')
nx = h_co.getnext()
while ptext(nx).strip() != '經營目標及預期效益':
    n2 = nx.getnext(); body.remove(nx); nx = n2
insert_after(h_co, build(S['協力人員']), drop_blank=False)
for el in body.iter(qn('w:p')):
    for t in el.iter(qn('w:t')):
        if t.text and '協力廠商' in t.text: t.text = t.text.replace('協力廠商', '協力人員')

for key, head in [('經營構想', '經營構想'), ('商品與服務內容', '商品與服務內容'), ('營運作業流程', '營運作業流程'),
                  ('室內空間說明', '室內空間說明'), ('行銷推廣計畫', '行銷推廣計畫'),
                  ('組織架構與人力配置', '組織架構與人力配置'), ('營運與服務品質管理', '營運與服務品質管理'),
                  ('經費來源', '經費來源'), ('商品售價與營收預估', '商品售價與營收預估'),
                  ('損益及財務可行性分析', '損益及財務可行性分析'), ('設備管理維護計畫', '設備管理維護計畫'),
                  ('消防、防災與防盜計畫', '消防、防災與防盜計畫'), ('營運風險管理', '營運風險管理'),
                  ('履約承諾與績效追蹤', '履約承諾與績效追蹤')]:
    heads = [el for el in body.iterchildren(qn('w:p')) if ptext(el).strip() == head]
    assert len(heads) == 1, (head, len(heads))
    insert_after(heads[0], build(S[key]))

# 附件:文件最後
sect = body.find(qn('w:sectPr'))
last = sect.getprevious()
pb = parse_xml(f'<w:p xmlns:w="{W}"><w:r><w:br w:type="page"/></w:r></w:p>')
h1 = mk_par(sty('A-01-壹'), '附件')
last = insert_after(last, [pb, h1], drop_blank=False)
insert_after(last, build(S['附件']), drop_blank=False)

# ---------- 2b. 獨立分頁段落 → 下一段「段落前分頁」,避免頁面剛好滿版時多出空白頁 ----------
for el in list(body.iterchildren(qn('w:p'))):
    brs = el.findall('.//' + qn('w:br'))
    if brs and all(b.get(qn('w:type')) == 'page' for b in brs) and not ptext(el).strip() \
            and el.find('.//' + qn('w:sectPr')) is None and el.find('.//' + qn('w:drawing')) is None:
        nx = el.getnext()
        while nx is not None and is_blank(nx):
            n2 = nx.getnext(); body.remove(nx); nx = n2
        if nx is not None and nx.tag == qn('w:p'):
            ppr = nx.get_or_add_pPr()
            ppr.insert(1, parse_xml('<w:pageBreakBefore xmlns:w="%s"/>' % W))
            body.remove(el)

# ---------- 3. 組織圖換新 ----------
import shutil
for rel in d.part.rels.values():
    if rel.reltype.endswith('/image') and rel.target_ref == 'media/image5.png':
        rel.target_part._blob = open('orgchart.png', 'rb').read()
for ext in body.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent'):
    if ext.get('cx') == '6188710' and ext.get('cy') == '3136265':
        ext.set('cy', str(round(6188710 * 510 / 1040)))
        for a in body.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}ext'):
            if a.get('cx') == '6188710' and a.get('cy') == '3136265':
                a.set('cy', str(round(6188710 * 510 / 1040)))

# ---------- 4. 目錄加「陸、附件」列 ----------
sdt = body.find(qn('w:sdt'))
toc_rows = [el for el in sdt.iter(qn('w:p')) if el.find('.//' + qn('w:pStyle')) is not None
            and el.find('.//' + qn('w:pStyle')).get(qn('w:val')) in ('11', '21')]
l1 = [el for el in toc_rows if el.find('.//' + qn('w:pStyle')).get(qn('w:val')) == '11']
new = copy.deepcopy(l1[-1])
for r in list(new.iter(qn('w:r'))):
    if r.find(qn('w:fldChar')) is not None or r.find(qn('w:instrText')) is not None:
        r.getparent().remove(r)
for h in new.iter(qn('w:hyperlink')):
    h.attrib.pop(qn('w:anchor'), None)
ts = [t for t in new.iter(qn('w:t'))]
ts[0].text = '陸、'
for t in ts[1:-1]:
    if (t.text or '').strip(): t.text = ''
[t for t in ts[1:-1] if t.text == ''][0].text = '附件'
ts[-1].text = 'PAGE_ATTACH'
toc_rows[-1].addnext(new)
# 目錄後多一個空白段會把分頁擠到下一頁
nxt = sdt.getnext()
if is_blank(nxt): body.remove(nxt)
sp = sdt.getnext()  # 帶 sectPr 的段落:分節本身即換頁,去掉多餘的分頁符號
if sp.find('.//' + qn('w:sectPr')) is not None:
    for r in list(sp.findall(qn('w:r'))):
        if r.find(qn('w:br')) is not None: sp.remove(r)
    ppr = sp.find(qn('w:pPr'))
    wc = ppr.find(qn('w:widowControl'))
    pos = list(ppr).index(wc) + 1 if wc is not None else 0
    ppr.insert(pos, parse_xml('<w:spacing xmlns:w="%s" w:before="0" w:after="0" w:line="20" w:lineRule="exact"/>' % W))
    ppr.insert(pos, parse_xml('<w:snapToGrid xmlns:w="%s" w:val="0"/>' % W))
    ppr.insert(len(ppr) - 1, parse_xml('<w:rPr xmlns:w="%s"><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr>' % W))

# 目錄第一層段前距縮小,容納新增的「陸、附件」列
sp1 = style_by_id['11'].element.pPr.find(qn('w:spacing'))
sp1.set(qn('w:beforeLines'), '25'); sp1.set(qn('w:before'), '90')

# 開啟時提示更新欄位(目錄頁碼)
settings = d.settings.element
if False:
    settings.append(parse_xml(f'<w:updateFields xmlns:w="{W}" w:val="true"/>'))

# 圖片 docPr id 重新編號,避免重複造成 Word 無法開啟
for i, dp in enumerate(body.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr'), 1):
    dp.set('id', str(i))
d.save(OUT)
print('saved', OUT)
