# 產生器:執行 python3 build.py 會依 pages 內容輸出各 html(共用頁首頁尾)
NAV = [("index.html","首頁"),("menu.html","店內菜單"),("beans.html","咖啡豆單"),
       ("brand.html","舞荳品牌"),("sustain.html","關於永續"),("about.html","關於我們"),
       ("contact.html","聯絡我們")]
SHOP = "https://sirshopping.cashier.ecpay.com.tw"

SKY_JS = r"""<script>
(function(){
 var themes={morning:"早晨的天空",noon:"正午的晴空",dusk:"黃昏的霞光"};
 var order=["morning","noon","dusk"];
 function pick(){var h=new Date().getHours();return h>=5&&h<10?"morning":h>=10&&h<16?"noon":"dusk";}
 var hero=document.querySelector(".hero");
 if(hero){
  order.forEach(function(m){var d=document.createElement("div");d.className="skybg "+m;hero.insertBefore(d,hero.firstChild);});
  ["c1","c2","c3"].forEach(function(c){var d=document.createElement("div");d.className="cloud "+c;hero.appendChild(d);});
  var sun=document.createElement("div");sun.className="sun";hero.appendChild(sun);
  var hz=document.createElement("div");hz.className="horizon";hero.appendChild(hz);
  var g=document.createElement("div");g.className="greet";
  var h1=hero.querySelector("h1");hero.insertBefore(g,h1);
  var sw=document.createElement("div");sw.className="skyswitch";
  [["morning","晨"],["noon","午"],["dusk","暮"]].forEach(function(p){
   var bt=document.createElement("button");bt.dataset.m=p[0];bt.textContent=p[1];
   bt.onclick=function(){apply(p[0],true)};sw.appendChild(bt);});
  hero.appendChild(sw);
 }
 function apply(m,save){
  document.documentElement.setAttribute("data-sky",m);
  if(save){try{localStorage.setItem("sky",m)}catch(e){}}
  document.querySelectorAll(".skybg").forEach(function(d){d.classList.toggle("show",d.classList.contains(m))});
  var g=document.querySelector(".hero .greet");if(g)g.textContent=themes[m];
  document.querySelectorAll(".skyswitch button").forEach(function(b){b.classList.toggle("on",b.dataset.m===m)});
 }
 var target;try{target=localStorage.getItem("sky")}catch(e){}
 if(!themes[target])target=pick();
 var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
 if(reduce||!hero){apply(target,false);return;}
 var seq=order.slice(0,order.indexOf(target)+1);
 if(seq.length===1)seq=["dusk"].concat(seq);
 apply(seq[0],false);
 var k=1;
 var t=setInterval(function(){
  if(k>=seq.length){clearInterval(t);return;}
  apply(seq[k],false);k++;
 },2600);
})();
</script>
"""

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
{SKY_JS}
</body></html>"""
    open(fname,"w",encoding="utf-8").write(html)
    print("wrote",fname)

import importlib, glob
for m in sorted(glob.glob("page_*.py")):
    src = open(m,encoding="utf-8").read()
    g = {"page":page}
    exec(src, g)
