# -*- coding: utf-8 -*-
"""赤崁樓案 財務模型 v2(115/10/16,依評選委員意見修正)
- 5年損益、開辦170萬改5年攤提(每年34萬)
- 非餐飲收入逐年提高(餐飲占比 89.6%→82%)
- 三情境:樂觀(來客+10%)、基準、保守(來客-20%)
- 文化活動另計直接成本40%(講師、材料)
用法:python3 -I pl_v2.py
"""
FB = 9328800                      # 穩定水準餐飲年收入(260人次×115元×26日×12月×1.0... 依建議書表15)
RAMP = (0.80, 0.92, 0.97, 0.98, 1.00)
SHARE = [(0.896, 0.069, 0.035), (0.88, 0.075, 0.045), (0.865, 0.08, 0.055), (0.85, 0.085, 0.065), (0.84, 0.09, 0.07)]
FIX, TH = 550000, 5400000
AMO = 340000                      # 170萬/5年


def run(mult=1.0):
    rows = []
    for i, r in enumerate(RAMP):
        fb = FB * r * mult
        sf, sr, se = SHARE[i]
        tot = fb / sf
        ret, evt = tot * sr, tot * se
        rev = fb + ret + evt
        c = dict(
            food=round(fb * 0.32) + round(fb * 0.05),
            goods=round(ret * 0.55),
            event=round(evt * 0.40),
            hr=round(2880000 * 1.03 ** i),
            roy=FIX + round(max(0, rev - TH) * 0.02),
            util=round(420000 * 1.03 ** i),
            mkt=round(rev * 0.03), fee=round(rev * 0.015), misc=round(rev * 0.02),
            maint=180000 + (50000 if i >= 3 else 0),
            amo=AMO,
        )
        cost = sum(c.values())
        rows.append(dict(fb=round(fb), ret=round(ret), evt=round(evt), rev=round(rev), **c, cost=cost,
                         pro=round(rev) - cost))
    return rows


def bep_daily(row, i):
    """損益兩平每日餐飲來客數(其他收入依同年比例連動)"""
    sf, sr, se = SHARE[i]
    fixed = row['hr'] + FIX - TH * 0.02 + row['util'] + row['maint'] + row['amo']
    tot_per_fb = 1 / sf
    var = (0.37 + (sr / sf) * 0.55 + (se / sf) * 0.40) + tot_per_fb * (0.03 + 0.015 + 0.02 + 0.02)
    margin = tot_per_fb - var          # 每1元餐飲收入的邊際貢獻
    fb_needed = fixed / margin
    return fb_needed / (115 * 26 * 12)


if __name__ == '__main__':
    for name, m in (('保守(來客-20%)', 0.8), ('基準', 1.0), ('樂觀(來客+10%)', 1.1)):
        R = run(m)
        print(name, [r['pro'] for r in R], [f"{r['pro']/r['rev']*100:.1f}%" for r in R])
    R = run()
    for k in ('fb', 'ret', 'evt', 'rev', 'food', 'goods', 'event', 'hr', 'roy', 'util', 'mkt', 'fee', 'misc', 'maint', 'amo', 'cost', 'pro'):
        print(k, [r[k] for r in R])
    print('BEP', [round(bep_daily(r, i)) for i, r in enumerate(R)])
    for name, m in (('保守', 0.8),):
        cash = 300000; mn = cash
        for r in run(m):
            cash += r['pro'] + r['amo']; mn = min(mn, cash)
        print(name, '30萬週轉金下最低現金', mn)
