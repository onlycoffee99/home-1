#!/usr/bin/env python3
# 填寫宜蘭縣政府「水利事業(跨越水道)建造物」申請表單(政達二廠搭排梅花排水)
# 用法: python3 fill_forms.py <空白表單資料夾(已轉 docx)> <輸出資料夾>
import sys, os, copy, docx
from docx.oxml.ns import qn

SRC, OUT = sys.argv[1], sys.argv[2]
APP = '政達木業有限公司二廠'
REP = '陳文政'
ADDR = '宜蘭縣冬山鄉得安村梅林路571-1號'
TEL = '(03)958-5175'
NAME = '政達木業有限公司二廠既設版橋及生活污水搭排梅花排水申請案'

def find(sub):
    return os.path.join(SRC, [f for f in os.listdir(SRC) if sub in f and f.endswith('.docx')][0])

def cells(t):
    seen = set()
    for r in t.rows:
        for c in r.cells:
            if c._tc not in seen:
                seen.add(c._tc); yield c

def append(p, text, like=None, underline=False):
    base = like or (p.runs[-1] if p.runs else None)
    r = p.add_run(text)
    if base is not None and base._r.rPr is not None:
        r._r.insert(0, copy.deepcopy(base._r.rPr))
    if underline:
        r.font.underline = True
    return r

def fill_sign_block(cell, label_map):
    for p in cell.paragraphs:
        for k, v in label_map.items():
            if p.text.strip() == k:
                append(p, v)

# 1. 封面
d = docx.Document(find('i_01'))
for r in d.tables[0].rows:
    k = r.cells[0].text.strip()
    if k in ('申請名稱：', '申請單位：'):
        p = r.cells[-1].paragraphs[0]
        append(p, NAME if k == '申請名稱：' else APP, like=r.cells[0].paragraphs[0].runs[0])
d.save(os.path.join(OUT, '01_封面_水利事業建造物申請書件_政達二廠.docx'))

# 2. 申請書
d = docx.Document(find('-02_'))
t = d.tables[0]
vals = {
    '使用行為名稱': '既設版橋(跨越梅花排水)及生活污水搭排(放流管線及介入口設置)',
    '使用內容': '一、既設版橋:廠區正門口跨越梅花排水之版橋一座(已施設完成),鋼筋混凝土版,長4.9公尺(跨越渠道方向)、寬7.6公尺,渠內無橋墩,供廠區出入通行,補辦申請。二、生活污水搭排:二廠生活污水經化糞池處理後,以放流管埋設通過梅山段329地號(水利用地),於梅花排水護岸設置介入口排放;日最大排放量2.25立方公尺,年排放量821.25立方公尺(年365日)。',
    '水道名稱': '梅花排水(宜蘭縣管區域排水)',
    '申請人土地': '冬山　鄉(鎮)市　梅山　段　－　小段　349　地號',
    '設置位置': '冬山　鄉(鎮)市　梅山　段　－　小段　329　地號(廠區正門口前,詳設計圖說)',
    '使用水道面積': '版橋約37.24平方公尺(長4.9公尺×寬7.6公尺);放流管約0.38平方公尺(PVC管徑0.1公尺×通過長度約3.83公尺)',
    '預定施工期間': '版橋已施設完成(既設);搭排管線於核准後擇期施工,工期約5至10個工作天(避開防汛期,詳施工計畫書)',
    '申請使用期限': '自核准之日起至119年12月31日止(配合農業部農田水利署115年10月28日農水宜字第1158104356號函許可期間)',
    '經費來源': '申請人自籌',
}
for r in t.rows:
    key = r.cells[0].text.replace(' ', '').replace('　', '').strip()
    if key in vals:
        c = r.cells[1]
        p = c.paragraphs[0]
        like = r.cells[0].paragraphs[0].runs[0] if r.cells[0].paragraphs[0].runs else None
        for x in list(p.runs): x._r.getparent().remove(x._r)
        append(p, vals[key], like=like)
for c in cells(t):
    fill_sign_block(c, {'申請人：': APP, '代表人：': REP, '住址：': ADDR, '電話：': TEL})
d.save(os.path.join(OUT, '02_水利事業建造物申請書_政達二廠.docx'))

# 3. 切結書
d = docx.Document(find('i_03'))
blanks = [APP, '冬山', '梅山', '－', '329', '梅花排水(區域排水)', '既設版橋及生活污水放流管線、介入口']
for c in cells(d.tables[0]):
    for p in c.paragraphs:
        if p.text.startswith('立切結書人為'):
            i = 0
            for r in p.runs:
                if '____' in r.text:
                    pre = r.text.split('_')[0]
                    r.text = pre + '　' + blanks[i] + '　'
                    r.font.underline = True
                    if pre:  # e.g. ')____' 保留括號不加底線
                        r.text = '　' + blanks[i] + '　'
                        r._r.addprevious(copy.deepcopy(r._r)); prev = r._r.getprevious()
                        for tt in prev.iter(qn('w:t')): tt.text = pre
                        for u in prev.iter(qn('w:u')): u.getparent().remove(u)
                    i += 1
    fill_sign_block(c, {'具切結書人：': APP, '代表人：': REP, '住址：': ADDR, '電話：': TEL})
d.save(os.path.join(OUT, '03_使用河川地切結書_政達二廠.docx'))
print('OK')
