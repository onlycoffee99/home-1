# -*- coding: utf-8 -*-
"""赤崁樓案 分年收支預算 3年→5年(115/10/13)
第1~3年假設與 fix_pl2.py(送件版表16)完全相同;第4、5年(115/10/13 依老闆指示平滑,稅前損益不跳升):
- 營收達成率 80%/92%/97%/98%/100%(第5年才達穩定水準260人次)
- 人事、水電年增3%持續;固定權利金55萬;變動權利金=超過540萬部分2%
- 開辦170萬依原規劃3年攤提;第4年起「二期設備更新及空間活化」再投入80萬,分2年攤提(每年40萬)
- 設備逐年老化,第4年起維護費每年增列5萬
"""
FB, RET, EVT = 9328800, 720000, 360000
RAMP = (0.8, 0.92, 0.97, 0.98, 1.0)
RENO, MAINT = 400000, 50000
PK, FIX, TH = 0.05, 550000, 5400000
rows = []
for i, r in enumerate(RAMP):
    fb, ret, evt = FB * r, RET * r, EVT * r
    rev = fb + ret + evt
    c = dict(
        mat=round(fb * 0.32) + round(fb * PK) + round(ret * 0.55),
        hr=2880000 * 1.03 ** i,
        roy=FIX + round(max(0, rev - TH) * 0.02),
        oth=round(420000 * 1.03 ** i) + round(rev * 0.03) + round(rev * 0.015) + 180000 + (MAINT if i >= 3 else 0) + round(rev * 0.02),
        amo=566667 if i < 3 else RENO,
    )
    c = {k: round(v) for k, v in c.items()}
    tot = sum(c.values())
    rows.append(dict(rev=round(rev), **c, tot=tot, pro=round(rev) - tot))
if __name__ == '__main__':
    lab = [('營業收入', 'rev'), ('原物料、包材及商品', 'mat'), ('人事費用', 'hr'), ('權利金(固定+變動)', 'roy'),
           ('水電、行銷、保險、雜支等', 'oth'), ('開辦攤提', 'amo'), ('成本及費用合計', 'tot'), ('稅前損益', 'pro')]
    for name, k in lab:
        print(name, [f'{r[k]:,}' for r in rows], f"{sum(r[k] for r in rows):,}")
    print('淨利率', [f"{r['pro']/r['rev']*100:.1f}%" for r in rows], f"{sum(r['pro'] for r in rows)/sum(r['rev'] for r in rows)*100:.1f}%")
    cum = 0
    for i, r in enumerate(rows, 1):
        cum += r['pro'] + r['amo']
        print(f'第{i}年 營運現金流(稅前損益+攤提) {r["pro"]+r["amo"]:,}  累計 {cum:,}')
