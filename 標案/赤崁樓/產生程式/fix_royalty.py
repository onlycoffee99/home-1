import sys, docx
from docx.oxml.ns import qn
SRC, OUT = sys.argv[1:3]
d = docx.Document(SRC)
rev=[8327040,10408800,10929240]; fb=[7463040,9328800,9795240]; ret=[576000,720000,756000]; evt=[288000,360000,378000]
FIX=550000; TH=5400000; RATE=0.02
n=lambda x: f'{round(x):,}'
var=[round((r-TH)*RATE) for r in rev]
def set_text(el, text):
    ts=list(el.iter(qn('w:t'))); ts[0].text=text
    ts[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    for t in ts[1:]: t.text=''
tb=next(t for t in d.tables if any('固定權利金' in c.text for r in t.rows for c in r.cells))
rows={r.cells[0].text.strip():r for r in tb.rows}
def setrow(key, vals):
    r=rows[key]; cells=[]
    for c in r.cells[1:]:
        if c._tc not in [x._tc for x in cells]: cells.append(c)
    assert len(cells)==3, (key,len(cells))
    for c,v in zip(cells,vals): set_text(c._tc, v)
# 固定權利金列可能三格合併,先拆成三格顯示
r=rows['固定權利金']
uniq=[]
for c in r.cells[1:]:
    if c._tc not in uniq: uniq.append(c._tc)
if len(uniq)==1:
    set_text(uniq[0], n(FIX))
else:
    setrow('固定權利金',[n(FIX)]*3)
k=next(k for k in rows if k.startswith('變動權利金'))
set_text(rows[k].cells[0]._tc, '　變動權利金(年營業額超過540萬元部分之2%)')
setrow(k,[n(v) for v in var])
# 成本合計、稅前損益、淨利率
def num(s): return int(s.replace(',',''))
tot=[]; 
for i in range(3):
    s=0
    for kk,rr in rows.items():
        if kk.startswith(('餐飲原物料','商品進貨','人事','固定權利金','變動權利金','水電','行銷','保險','耗材','開辦')):
            cells=[];
            for c in rr.cells[1:]:
                if c._tc not in [x._tc for x in cells]: cells.append(c)
            v = cells[i].text if len(cells)==3 else cells[0].text
            s+=num(v)
    tot.append(s)
setrow('成本及費用合計',[n(x) for x in tot])
pro=[rev[i]-tot[i] for i in range(3)]
setrow('稅前損益',[n(x) for x in pro])
setrow('稅前淨利率',[f'{pro[i]/rev[i]*100:.1f}%' for i in range(3)])
# 損益兩平
F=2880000+FIX+420000+180000+566667 - TH*RATE   # 變動權利金 = 2%R - 108,000
vr=(fb[1]*0.32+ret[1]*0.55)/rev[1]+0.03+0.02+RATE
BEP=F/(1-vr); BEPM=BEP/12; cust=(BEPM-(ret[1]+evt[1])/12)/26/115
for p in d.paragraphs:
    if '固定權利金每月新臺幣40,000元' in p.text:
        set_text(p._p, p.text.replace('「固定權利金每月新臺幣40,000元，另按年營業額1%計收變動權利金」','「固定權利金每年新臺幣550,000元，另就年營業額超過新臺幣540萬元之部分，按2%計收變動權利金」'))
    if p.text.startswith('經試算，本案年固定成本約'):
        set_text(p._p, f'經試算，本案年固定成本約{n(F)}元(已扣除變動權利金起算門檻之影響)，變動成本率約{vr*100:.1f}%，損益兩平年營業額約{n(BEP)}元(每月約{n(BEPM)}元)，換算每日來客數約{cust:.0f}人次即可達損益兩平，低於預估之平均每日260人次，具備相當之安全邊際。第一年稅前淨利約{n(pro[0])}元，第二年起約{n(pro[1])}元以上，財務具可行性；本團隊並將每年提撥營業額之1%作為設備汰換及空間維護準備金，確保長期營運品質。')
d.save(OUT)
print('var',var,'royalty total',[FIX+v for v in var]); print('cost',tot); print('profit',pro); print('BEP',round(BEP),round(cust))
