import sys,re,docx,pymupdf as f
from docx.oxml.ns import qn
src,pdf,out=sys.argv[1:4]
d=f.open(pdf); pages={}
body_start=None
for i,p in enumerate(d):
    lines=[re.sub(r'\s','',l) for l in p.get_text().split('\n') if l.strip()]
    if not lines: continue
    num=lines[-1]
    if not num.isdigit(): continue
    for l in lines:
        pages.setdefault(l,num)
        l2=re.sub(r'^(圖|表)\d+','',l)
        if l2!=l: pages.setdefault(l2,num)
doc=docx.Document(src); body=doc.element.body
miss=[];n=0
for p in body.iter(qn('w:p')):
    if not any('PAGEREF' in (x.text or '') for x in p.iter(qn('w:instrText'))) and not p.find('.//'+qn('w:pStyle')) is not None: continue
    instr=''.join(x.text or '' for x in p.iter(qn('w:instrText')))
    ts=list(p.iter(qn('w:t')))
    if not ts: continue
    full=re.sub(r'\s','',''.join(t.text or '' for t in ts))
    m=re.match(r'^(.*?)(\d+)$',full)
    if not m or 'PAGEREF' not in instr: continue
    key=m.group(1)
    cands=[key, re.sub(r'^(壹|貳|參|肆|伍|陸|柒|一|二|三|四|五|六)、','',key), re.sub(r'^(圖|表)\d+、','',key)]
    pg=next((pages[c] for c in cands if c in pages),None)
    if pg is None:
        # heading lines rendered as "壹、團隊..." -> try contains
        pg=next((v for k,v in pages.items() if cands[1] and k.endswith(cands[1]) and len(k)-len(cands[1])<=3),None)
    if pg is None: miss.append(key); continue
    # set last number t
    for t in reversed(ts):
        if re.fullmatch(r'\s*\d+\s*',t.text or ''): t.text=pg; n+=1; break
doc.save(out); print('updated',n,'missing',miss)
