# 產生器:執行 python3 build.py 會依 pages 內容輸出各 html(共用頁首頁尾)
NAV = [("index.html","首頁"),("menu.html","店內菜單"),("beans.html","咖啡豆單"),
       ("brand.html","舞荳品牌"),("sustain.html","關於永續"),("about.html","關於我們"),
       ("contact.html","聯絡我們")]
SHOP = "https://sirshopping.cashier.ecpay.com.tw"

def page(fname, title, body, desc=""):
    nav = "".join(f'<a class="item{" on" if f==fname else ""}" href="{f}">{t}</a>' for f,t in NAV)
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}｜時間到咖啡館-公園裡的咖啡館</title>
<meta name="description" content="{desc or title+'。時間到咖啡館,宜蘭礁溪,ICO國際咖啡組織認證咖啡。'}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header><nav class="nav">
<a class="logo" href="index.html">時間到咖啡館<small>公園裡的咖啡館・我們就是ICO認証咖啡</small></a>
{nav}
<a class="shop" href="{SHOP}" target="_blank" rel="noopener">線上購物</a>
</nav></header>
{body}
<footer><div class="wrap">
<div><strong>鑫和洋行 生技</strong><br>統一編號:72941298<br>客服電話:03-936-3306<br>客服手機:0975-328-779<br>LINE ID:onlycoffee99</div>
<div><strong>線上購物</strong><br>台灣訂購:<a href="{SHOP}" target="_blank" rel="noopener">綠界 時間到咖啡館</a><br>海外訂購:<a href="https://5wudou.com" target="_blank" rel="noopener">舞荳購物網(5wudou.com)</a><br><br>© 時間到咖啡館-公園裡的咖啡館</div>
</div></footer>
</body></html>"""
    open(fname,"w",encoding="utf-8").write(html)
    print("wrote",fname)

import importlib, glob
for m in sorted(glob.glob("page_*.py")):
    src = open(m,encoding="utf-8").read()
    g = {"page":page}
    exec(src, g)
