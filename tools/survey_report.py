#!/usr/bin/env python3
"""森林風呂御神籤問卷 → 統計報告(Markdown)。

資料來源(擇一):
  --url <網頁網址> --key <匯出金鑰>   直接向 Apps Script 匯出(金鑰也可放環境變數 OMIKUJI_EXPORT_KEY)
  --json <檔案>                        先前匯出的 JSON({columns, rows})

期間(擇一,預設全部):
  --month 2026-10                      單月
  --from 2026-10-01 --to 2026-12-31    自訂區間(含頭尾)

輸出:--out 報告.md(省略則印到螢幕);--save-json 另存原始資料
用法見 tools/README.md。只用 Python 標準函式庫。
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from collections import Counter, OrderedDict

SCALE = OrderedDict([("非常滿意", 5), ("滿意", 4), ("普通", 3), ("不滿意", 2), ("非常不滿意", 1)])
NA = {"不清楚/沒注意", "今天沒開車", "今天沒需要幫忙"}
RECOMMEND = ["一定會", "應該會", "還不確定", "應該不會"]
SMALL_N = 30  # 有效份數低於此值標註「樣本少」

SECTIONS = [
    ("♨️ 泡風呂(核心題:每位填答者必答)", ["q08", "q09"]),
    ("🌳 公園環境與服務", ["q01", "q02", "q03", "q04", "q05", "q06", "q07"]),
    ("♨️ 風呂服務", ["q10", "q11", "q12"]),
    ("☕ 店家與停車", ["q13", "q14", "q15"]),
    ("🏞️ 宜蘭好在地", ["q17", "q18", "q19", "q20", "q21", "q22", "q23", "q24"]),
]
FUN = ["f1", "f2", "f3"]
AGES = ["20 以下", "21-30 歲", "31-40 歲", "41-50 歲", "51-60 歲", "61-70 歲", "71 以上"]
FREQS = ["今天第一次來 🎉", "一年 3 次以下", "一年 3~10 次", "一年 10 次以上", "天天都來 😎"]


def roc(d):
    return f"{d.year - 1911}/{d.month}/{d.day}"


def parse_time(s):
    s = (s or "").strip()
    m = re.match(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})(?:\s+(上午|下午)?\s*(\d{1,2}):(\d{2})(?::(\d{2}))?)?", s)
    if not m:
        return None
    y, mo, d, ap, h, mi, se = m.groups()
    h = int(h or 0)
    if ap == "下午" and h < 12:
        h += 12
    if ap == "上午" and h == 12:
        h = 0
    return dt.datetime(int(y), int(mo), int(d), h, int(mi or 0), int(se or 0))


def load(args):
    if args.json:
        with open(args.json, encoding="utf-8") as f:
            data = json.load(f)
    else:
        key = args.key or os.environ.get("OMIKUJI_EXPORT_KEY")
        if not (args.url and key):
            sys.exit("需要 --url 與 --key(或環境變數 OMIKUJI_EXPORT_KEY),或改用 --json")
        with urllib.request.urlopen(args.url + "?export=" + key, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
        if data.get("error"):
            sys.exit("匯出失敗:" + data["error"] + "(金鑰錯誤,或 Apps Script 尚未設定 EXPORT_KEY / 未部署新版本)")
    if args.save_json:
        with open(args.save_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    ids = [c[0] for c in data["columns"]]
    names = {c[0]: c[1] for c in data["columns"]}
    rows = [dict(zip(ids, r)) for r in data["rows"]]
    for r in rows:
        r["_t"] = parse_time(r.get("time"))
    return rows, names


def pct(a, b):
    return f"{a / b * 100:.0f}%" if b else "—"


def sat_stats(rows, qid):
    vals = [r.get(qid, "") for r in rows]
    asked = sum(1 for r in rows if qid in (r.get("asked") or "").split(","))
    valid = [v for v in vals if v in SCALE]
    na = sum(1 for v in vals if v in NA)
    c = Counter(valid)
    n = len(valid)
    good = c["非常滿意"] + c["滿意"]
    bad = c["不滿意"] + c["非常不滿意"]
    avg = sum(SCALE[v] for v in valid) / n if n else None
    return {"asked": asked or (n + na), "n": n, "na": na, "c": c, "good": good, "bad": bad, "avg": avg}


def dist_table(rows, key, order, title):
    c = Counter(r.get(key, "") for r in rows if r.get(key))
    n = sum(c.values())
    out = [f"| {title} | 份數 | 比例 |", "|---|---:|---:|"]
    for k in order + [k for k in c if k not in order]:
        if c.get(k):
            out.append(f"| {k} | {c[k]} | {pct(c[k], n)} |")
    out.append(f"| **合計** | **{n}** | |")
    return "\n".join(out), c, n


def build(rows, names, start, end):
    lines = []
    days = (end - start).days + 1
    period = f"{roc(start)} ~ {roc(end)}"
    lines += [
        f"# 森林風呂遊客滿意度調查 統計報告",
        "",
        f"- 調查期間:{period}(共 {days} 日)",
        f"- 有效問卷:**{len(rows)} 份**(平均每日 {len(rows) / days:.1f} 份)",
        f"- 調查方式:森林風呂現場 QR code 線上填答(森林風呂御神籤),匿名、不蒐集個資;填答後贈時間到咖啡館折價券",
        f"- 產出日期:{roc(dt.date.today())}",
        "",
    ]
    if not rows:
        lines.append("本期間無填答資料。")
        return "\n".join(lines)

    core = {q: sat_stats(rows, q) for q in ["q08", "q09"]}
    lines += ["## 一、重點摘要", ""]
    for q, s in core.items():
        if s["n"]:
            lines.append(f"- {names[q]}:滿意(含非常滿意)**{pct(s['good'], s['n'])}**,平均 {s['avg']:.2f} 分(5 分制,{s['n']} 份)")
    allq = [q for _, qs in SECTIONS for q in qs]
    stats = {q: sat_stats(rows, q) for q in allq}
    ranked = sorted([q for q in allq if stats[q]["n"] >= 10], key=lambda q: -stats[q]["avg"])
    if ranked:
        lines.append(f"- 平均分數最高:{names[ranked[0]]}({stats[ranked[0]]['avg']:.2f} 分)")
        lines.append(f"- 平均分數最低:{names[ranked[-1]]}({stats[ranked[-1]]['avg']:.2f} 分)")
    watch = [q for q in allq if stats[q]["n"] >= 10 and stats[q]["bad"] / stats[q]["n"] >= 0.10]
    if watch:
        lines.append("- 不滿意(含非常不滿意)達 10% 以上:" + "、".join(f"{names[q]}({pct(stats[q]['bad'], stats[q]['n'])})" for q in watch))
    else:
        lines.append("- 各題不滿意比例均未達 10%(僅計有效份數 10 份以上之題目)")
    first = sum(1 for r in rows if r.get("freq", "").startswith("今天第一次來"))
    lines.append(f"- 首次到訪遊客占 {pct(first, len(rows))}")
    lines.append("")

    lines += ["## 二、各題滿意度", "",
              "> 說明:每位填答者答 8 題(2 題核心題固定,其餘自題庫隨機抽出),故各題有效份數不同。滿意率=(非常滿意+滿意)÷有效份數;平均分數以非常滿意 5 分至非常不滿意 1 分計;「不清楚/沒注意」「今天沒開車」「今天沒需要幫忙」列為不適用,不計入分母。"
              f"有效份數未達 {SMALL_N} 份者標註「樣本少」,僅供參考。", ""]
    for title, qs in SECTIONS:
        lines += [f"### {title}", "",
                  "| 題目 | 有效份數 | 非常滿意 | 滿意 | 普通 | 不滿意 | 非常不滿意 | 滿意率 | 平均分數 | 不適用 |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for q in qs:
            s = stats[q]
            flag = "(樣本少)" if 0 < s["n"] < SMALL_N else ""
            avg = f"{s['avg']:.2f}" if s["avg"] is not None else "—"
            c = s["c"]
            lines.append(f"| {names[q]}{flag} | {s['n']} | {c['非常滿意']} | {c['滿意']} | {c['普通']} | {c['不滿意']} | {c['非常不滿意']} | {pct(s['good'], s['n'])} | {avg} | {s['na'] or ''} |")
        lines.append("")

    t, c, n = dist_table(rows, "q16", RECOMMEND, "會推薦朋友來嗎")
    lines += ["### 推薦意願", "", t, ""]
    if n:
        lines.append(f"推薦意願(一定會+應該會):{pct(c['一定會'] + c['應該會'], n)}\n")

    lines += ["## 三、填答者背景", ""]
    t, _, _ = dist_table(rows, "age", AGES, "年齡")
    lines += [t, ""]
    t, _, _ = dist_table(rows, "freq", FREQS, "來訪頻率")
    lines += [t, ""]

    months = sorted({(r["_t"].year, r["_t"].month) for r in rows if r["_t"]})
    if len(months) > 1:
        lines += ["## 四、月別趨勢", "", "| 月份 | 份數 | 溫泉水質 滿意率 | 湯區清潔 滿意率 |", "|---|---:|---:|---:|"]
        for y, m in months:
            sub = [r for r in rows if r["_t"] and (r["_t"].year, r["_t"].month) == (y, m)]
            a, b = sat_stats(sub, "q08"), sat_stats(sub, "q09")
            lines.append(f"| {y - 1911}/{m} | {len(sub)} | {pct(a['good'], a['n'])} | {pct(b['good'], b['n'])} |")
        lines.append("")
        sec = "五"
    else:
        sec = "四"

    lines += [f"## {sec}、趣味題(遊客偏好參考)", ""]
    for q in FUN:
        c = Counter(r.get(q) for r in rows if r.get(q))
        if c:
            n = sum(c.values())
            lines += [f"**{names[q].split(':', 1)[-1]}**({n} 份)", "", "| 選項 | 份數 | 比例 |", "|---|---:|---:|"]
            lines += [f"| {k} | {v} | {pct(v, n)} |" for k, v in c.most_common()]
            lines.append("")

    msgs = [(r["_t"], r.get("message", "").lstrip("'")) for r in rows if r.get("message", "").strip()]
    nxt = "六" if sec == "五" else "五"
    lines += [f"## {nxt}、遊客留言(原文照錄,共 {len(msgs)} 則)", ""]
    for t, m in sorted(msgs, key=lambda x: x[0] or dt.datetime.min):
        lines.append(f"- {roc(t) if t else ''}:{m}")
    if not msgs:
        lines.append("本期間無留言。")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url")
    ap.add_argument("--key")
    ap.add_argument("--json")
    ap.add_argument("--save-json")
    ap.add_argument("--month")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--exclude", default="Claude 測試", help="留言含此字串的列視為測試資料排除")
    ap.add_argument("--out")
    args = ap.parse_args()

    rows, names = load(args)
    rows = [r for r in rows if not (args.exclude and args.exclude in r.get("message", ""))]
    if args.month:
        y, m = map(int, args.month.split("-"))
        start = dt.date(y, m, 1)
        end = (dt.date(y + m // 12, m % 12 + 1, 1) - dt.timedelta(days=1))
    else:
        ts = [r["_t"].date() for r in rows if r["_t"]]
        start = dt.date.fromisoformat(args.start) if args.start else (min(ts) if ts else dt.date.today())
        end = dt.date.fromisoformat(args.end) if args.end else (max(ts) if ts else dt.date.today())
    rows = [r for r in rows if r["_t"] and start <= r["_t"].date() <= end]

    md = build(rows, names, start, end)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"已產出 {args.out}({len(rows)} 份)")
    else:
        print(md)


if __name__ == "__main__":
    main()
