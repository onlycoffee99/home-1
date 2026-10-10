import json,os,datetime
R='/tmp/claude-0/-home-user-home-1/c0e478eb-8463-5374-8afd-baba07237450/scratchpad/eval/deck/project'
D='#1E3A2F';L='#F7F3EA';L2='#ECE4D3';A='#A8432A';M='#4D4A42';MD='#C9D6CC'
H="'Noto Serif TC', Georgia, serif";B="'Noto Sans TC', Arial, sans-serif"
IMG=dict(plan='/_blob/62f67fdbab19ff0a86164a988f1b2119',tea='/_blob/c566d56169e054e78ed5921264eebaab',jx='/_blob/e0dd7440253af3226f5b3b6a5c663a1d',tc='/_blob/a933bb57c14fc10bb68ea30cd17ca8b3',op='/_blob/6d9d8f2ce0556a9090e66940cd15a3f9',op2='/_blob/e9a01c2af5f8fc2538071ec35e6d9ff9',cal='/_blob/9d873bfa768c387b39279aaf37305151',kq='/_blob/017a16c6d40922851828e25cd23152c8',drip='/_blob/6730f75861a7d898b329bb9a94069799',cls='/_blob/e6ba1ea277a29171b21ba6bb09dd8e1a',map='/_blob/43f19846c81d1e93d662ce667162ee5b')
slides=[]
def foot(n,bg='light'):
    c=M if bg=='light' else MD
    return (f'<p style="position:absolute;left:128px;bottom:64px;width:1200px;font-size:24px;color:{c}">鑫和洋行｜赤崁樓遊客中心2樓部分空間委外經營管理案</p>'
            f'<p style="position:absolute;right:128px;bottom:64px;width:120px;text-align:right;font-size:24px;color:{c}">{n:02d}</p>')
def content(id,eyebrow,title,body,notes,bg=L,n=None):
    n=len(slides)+1
    s=(f'<section id="{id}" data-transition="fade" style="background:{bg};color:{D};font-family:{B};padding:128px 128px 160px;display:flex;flex-direction:column;gap:40px">'
       f'<div style="display:flex;flex-direction:column;gap:12px"><p style="font-size:24px;font-weight:700;color:{A};letter-spacing:2px">{eyebrow}</p>'
       f'<h2 style="font-family:{H};font-size:64px;font-weight:700;line-height:1.15;color:{D}">{title}</h2></div>'
       f'{body}{foot(n)}<aside>{notes}</aside></section>')
    slides.append((id,s))
def table(head,rows,widths,fs=28,align=None):
    t=f'<table style="font-size:{fs}px;color:{D};font-family:{B};padding:14px 20px"><tr style="background:{D}">'
    for h,w in zip(head,widths): t+=f'<th style="width:{w}%;color:{L};text-align:left">{h}</th>'
    t+='</tr>'
    for i,r in enumerate(rows):
        bg=L2 if i%2 else '#FBF8F1'
        t+=f'<tr style="background:{bg}">'+''.join(f'<td>{c}</td>' for c in r)+'</tr>'
    return t+'</table>'
def card(title,text,bg='#FBF8F1',extra=''):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:{bg};padding:40px;border:1px solid #D9CFBC;border-radius:16px{extra}">'
            f'<h3 style="font-family:{H};font-size:40px;font-weight:700;color:{D}">{title}</h3><p style="font-size:28px;line-height:1.55;color:{M}">{text}</p></div>')

