# 店內菜單(115/9 改版:無 S,只有 M/L)
def T(title, cols, rows, note=""):
    h = "".join(f'<th class="{"r" if i else ""}">{c}</th>' for i,c in enumerate(cols))
    b = "".join("<tr>"+ "".join(f'<td class="{"r" if i else ""}">{c}</td>' for i,c in enumerate(r)) +"</tr>" for r in rows)
    n = f'<p class="muted">{note}</p>' if note else ""
    return f'<h3>{title}</h3><table><tr>{h}</tr>{b}</table>{n}'

body = """
<div class="hero"><h1>Time Coffee Menu</h1><p>我們將咖啡變得不一樣了——全系列衣索比亞精品產區</p></div>
<main class="wrap">
<section>
<h2>土耳其式手選咖啡</h2>
<p class="muted">土耳其式沖泡使用精細研磨,讓好豆子充滿考驗,呈現香氣優雅、濃郁而不失特色、口感飽滿且極具異國風情的咖啡。</p>
""" + T("手選咖啡",["品項","M","L"],[
["水果鉑金(NO.3號)|Light Roast<br><span class='muted'>熱口感酸甜水果,溫口感花香,清爽果味最令人著迷</span>","140","170"],
["鉑金級(NO.4號)|Cinnamon Roast<br><span class='muted'>熱口感甘性出現,溫口感莓果酸甜,柔美雅致</span>","130","160"],
["精品級(NO.5號)|Medium Roast<br><span class='muted'>前味微苦甘香,尾韻葡萄乾與熱帶水果甘味最集中</span>","150","180"],
["焦糖野橘(NO.6號)|High Roast<br><span class='muted'>焦糖奶油溫柔香,苦甘韻味感十足</span>","150","180"],
["土耳其直火咖啡 Turkish coffee<br><span class='muted'>磨成極細粉末於爐上煮沸,第一口就品嚐咖啡果實香氣</span>","","180"],
["Espresso<br><span class='muted'>第一口的濃苦,後勁卻出現了甘香(可選豆子)</span>","","200"],
]) + """
</section>
<section>
<h2>手沖咖啡 Hand Brewed Coffee</h2>
<p class="muted">滴漏式沖煮,呈現明亮華麗的香氣與深厚豐富性。產地衣索比亞,一杯 $200,以下產地可選淺焙或中焙。</p>
<div class="grid">
<div class="card"><h3>谷吉布穀 罕布拉 G1 日曬</h3><p class="muted">Guji Buku Hambella G1 Natural——圓潤、層次豐富,水果酸香甜飽滿,冷口感呈現果汁清澈</p></div>
<div class="card"><h3>耶加雪菲 雪列圖 G1 日曬</h3><p class="muted">Yirgacheffe Chelelektu G1 Natural——花香、葡萄乾、深色莓果、熱帶水果、焦糖</p></div>
<div class="card"><h3>耶加雪菲 雪列圖 G1 水洗</h3><p class="muted">Yirgacheffe Chelelektu G1 Washed——花檸檬柑橘,伯爵茶尾韻,蜂蜜蜜桃,口感乾淨清澈</p></div>
</div>
<h3>限量季節產品精品豆</h3>
<p class="muted">不定期推出——當季遇到特別出色的精品豆,才會另外引進限量介紹,售完為止,供應以現場公告為準。近期登場:</p>
<div class="grid">
<div class="card"><h3>黃金曼特寧 AAA</h3><p class="muted">中深焙——烘焙堅果與焦糖調,醇厚沉穩、回甘悠長</p></div>
<div class="card"><h3>馬拉威藝伎</h3><p class="muted">Malawi Geisha——花香、柑橘、檸檬,尾韻蜂蜜,酸質集中</p></div>
<div class="card"><h3>衣索比亞・耶加雪菲藝伎</h3><p class="muted">Ethiopia Yirgacheffe Geisha——細緻花果香,乾淨柔和、尾韻優雅</p></div>
</div>
</section>
<section>
<h2>冰咖啡&花式咖啡</h2>
""" + T("單品冰黑咖啡 Ice Coffee",["品項","M","L"],[
["冰黑咖啡 Ice black coffee","","160"],
["青檸冰咖啡 Lime ice coffee<br><span class='muted'>檸檬與咖啡的美味激盪</span>","160","180"],
["冰滴咖啡 Ice drip coffee<br><span class='muted'>12小時直取(0.1咖啡因)</span>","200","280"],
["精品濃縮冰黑咖啡 Iced espresso","200",""],
]) + T("花式咖啡(冰/熱)|換置燕麥奶+30元",["品項","M","L"],[
["鮮奶咖啡 Latte","140","160"],["卡布其諾 Cappuccino","130","150"],
["榛果歐蕾 Hazelnut Latte","140","160"],["焦糖歐蕾 Caramel Latte","140","160"],
["黑糖歐蕾 Brown Sugar Latte","140","160"],["太妃歐蕾 Toffee Latte","140","160"],
["摩卡可可 Café Mocha","","160"],["港式鴛鴦奶茶 Coffee with Milk Tea","140","160"],
["樟芝養氣咖啡(黑咖啡)<br><span class='muted'>Coffee with Taiwan Antrodia Cinnamomea</span>","150","180"],
]) + """
</section>
<section>
<h2>茶飲系列(冰/熱)</h2>
""" + T("茶飲 Tea",["品項","M","L"],[
["原味鮮奶蓋茶 Milk Tea","120","140"],
["鮮奶蓋茶(榛果/太妃/焦糖/黑糖/香草/焦塩)","130","150"],
["日式宇治濃抹茶 Matcha Latte","150","170"],
["新鮮手作蘋果茶 Apple Tea","","160"],
["宜蘭省產金棗茶 Kumquat Tea","130","150"],
["宜蘭金磚黑糖金棗茶 Brown Sugar Kumquat Tea","130","150"],
["蜂蜜檸檬茶 Honey Lemon Tea","130","150"],
["新鮮綜合水果茶 Fruit Tea","","150"],
]) + T("舞荳頂級植物草本茶系列",["品項","M","L"],[
["樟香熟普洱","","200"],
["樟香生普洱","","200"],
["南非國寶茶+有機杭菊","","180"],
]) + """
</section>
<section>
<h2>黃金可可飲&果汁氣泡</h2>
""" + T("黃金可可飲(冰/熱)",["品項","M","L"],[
["原味香純可可 Cocoa","140","160"],["香草香可可 Vanilla Cocoa","150","170"],
["芝麻香純可可 Sesame Cocoa","150","170"],["核桃香純可可 Walnut Cocoa","150","170"],
["胡桃香純可可 Pecan Cocoa","150","170"],["鹽之花可可 Sea Salt Flower Cocoa","150","170"],
["焦糖香純可可 Caramel Cocoa","140","160"],["太妃香純可可 Toffee Cocoa","150","170"],
["摩卡可可冰沙 Mocha Cocoa Smoothie","","180"],
["莓果歐蕾可可冰沙 Berry Cocoa Smoothie","","180"],["香蕉歐蕾可可冰沙 Banana Cocoa Smoothie","","180"],
]) + T("時令果汁&特別氣泡 Juice & Soda",["品項","M","L"],[
["貓山王榴槤奶茶 Musang King Durian Milk Tea","","180"],["火龍果蘋果汁 Dragon Fruit Apple Juice","","180"],
["蘋果鳯梨汁 Apple Pineapple Juice","","180"],["香蕉木瓜牛奶 Banana Papaya Milk","","180"],
["蜂蜜蘇打 Honey Soda","","180"],["檸檬蘇打 Lemon Soda","","180"],["百香果蘇打 Passion Fruit Soda","","180"],
]) + T("餐點(以現場為主)",["品項","價格"],[
["四種起士披薩 Four Cheese Pizza","280"],
["瑪格麗特披薩 Margherita Pizza","280"],
["鄉村菇鹹派 Country Mushroom Quiche","180"],
["青森燉蘋果派 Aomori Stewed Apple Pie","180"],
["宜蘭金棗香檸派 Kumquat Lemon Pie","180"],
]) + """
</section>
</main>
"""
page("menu.html","店內菜單介紹",body,"時間到咖啡館店內菜單:土耳其式咖啡、手沖精品咖啡、花式咖啡、茶飲、黃金可可飲、果汁氣泡與時令點心。")
