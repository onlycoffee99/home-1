import sys, docx
from docx.oxml.ns import qn
from docx.oxml import parse_xml
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
SRC,OUT=sys.argv[1:3]
d=docx.Document(SRC); body=d.element.body; kids=list(body)
def t(el): return ''.join(x.text or '' for x in el.iter(qn('w:t'))).strip()
s=next(i for i,e in enumerate(kids) if e.tag==qn('w:p') and t(e)=='商品售價與營收預估')
e=next(i for i,x in enumerate(kids) if i>s and x.tag==qn('w:p') and t(x).startswith('履約執行與管理維護計畫'))
sect=body.find(qn('w:sectPr'))
for i,x in enumerate(kids):
    if not (s<=i<e) and x is not sect: body.remove(x)
fixed={'商品售價與營收預估':'三、','損益及財務可行性分析':'四、','營收預估表':'表15、','三年損益試算表':'表16、'}
for p in body.iter(qn('w:p')):
    tx=t(p)
    if tx in fixed:
        ppr=p.get_or_add_pPr()
        for old in ppr.findall(qn('w:numPr')): ppr.remove(old)
        ppr.insert(1, parse_xml(f'<w:numPr xmlns:w="{W}"><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'))
        ts=list(p.iter(qn('w:t'))); ts[0].text=fixed[tx]+ts[0].text
    for pb in p.findall('.//'+qn('w:pageBreakBefore')): pb.getparent().remove(pb)
rid=next(r.rId for r in d.part.rels.values() if r.reltype.endswith('/footer'))
if sect.find(qn('w:footerReference')) is None:
    sect.insert(0, parse_xml(f'<w:footerReference xmlns:w="{W}" xmlns:r="{R}" w:type="default" r:id="{rid}"/>'))
pn=sect.find(qn('w:pgNumType'))
if pn is None:
    pn=parse_xml(f'<w:pgNumType xmlns:w="{W}"/>'); cols=sect.find(qn('w:cols')); cols.addprevious(pn)
for a in list(pn.attrib):
    if a.endswith('fmt'): del pn.attrib[a]
pn.set(qn('w:start'),'25')
d.save(OUT)
