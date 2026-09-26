import sys,re,docx,pymupdf as f
from docx.oxml.ns import qn
src,pdf,out=sys.argv[1:4]
d=f.open(pdf)
pages={}
for i,p in enumerate(d):
    lines=[l.strip() for l in p.get_text().split('\n') if l.strip()]
    if i==0: continue
    num=lines[-1]
    for l in lines: pages.setdefault(re.sub(r'\s','',l),num)
doc=docx.Document(src); body=doc.element.body
sdt=body.find(qn('w:sdt'))
miss=[]
for p in sdt.iter(qn('w:p')):
    ts=list(p.iter(qn('w:t')))
    txt=re.sub(r'\s','',''.join(t.text or '' for t in ts[:-1]))
    if not txt or txt=='目錄' : continue
    if txt in pages: ts[-1].text=pages[txt]
    else: miss.append(txt)
doc.save(out); print('missing',miss)
