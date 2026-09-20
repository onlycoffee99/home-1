# NEW 咖啡豆單
def bean(name, en, price, lines):
    li = "".join(f"<p class='muted'>{l}</p>" for l in lines)
    return f"<div class='card'><h3>{name}</h3><p class='muted'>{en}</p>{li}<p><strong>半磅 {price}</strong></p></div>"

body = """
<div class="hero"><h1>NEW 咖啡豆單</h1><p>我們將咖啡變得不一樣了</p></div>
<main class="wrap">
<section>
<h2>經典配方豆</h2>
<div class="grid">
""" + bean("水果鉑金(NO.3號)","Light Roast 淺焙・黑咖啡","600",["熱口感:酸甜水果香氣奔放;溫口感:花香輕柔優雅","整體印象:清爽果味,明亮層次,最適合喜愛輕盈口感的你"]) \
+ bean("鉑金級(NO.4號)","Cinnamon Roast 肉桂焙(淺中焙)・黑咖啡","600",["熱口感:甘性風味浮現;溫口感:莓果酸甜細膩;冷口感:清爽亮麗不失層次","整體印象:柔美雅致,如水果般圓潤細緻的優雅表現"]) \
+ bean("精品級(NO.5號)","Medium Roast 中焙・黑咖啡","600",["前味:微苦甘香柔和展現;尾韻:葡萄乾與熱帶水果香甜收尾","整體印象:甜感集中,風味圓潤,為經典中焙款代表作"]) \
+ bean("焦糖野橘(NO.6號)","High Roast 中深焙・黑咖啡","600",["香氣:焦糖與奶油的溫柔香氣;口感:苦甘交織,韻味濃厚","整體印象:口感厚實,香醇中帶層次,風味深沉卻不沉重"]) + """
</div>
</section>
<section>
<h2>衣索比亞精品單品豆</h2>
<div class="grid">
""" + bean("古吉布穀・罕布拉 G1 日曬","Guji Buku Hambella G1 Natural","800",["口感:圓潤飽滿、層次豐富;亮點:水果酸香甜明顯,冷卻後如果汁般清澈透亮","經典日曬豆款中的佳作|遊玩角色:果園裡的徒步旅人"]) \
+ bean("西達瑪・卡拉莫 日曬","Bombe Bensa Sidama G1 Natural","800",["口感:花香清新,乾淨透亮;亮點:柑橘、檸檬調性、甘蔗、黃肉李子","適合喜愛清爽果感甜與自然花果調的飲者|遊玩角色:清晨花市裡的尋香者"]) \
+ bean("西達摩・聖塔瓦納 G1 日曬","Sidamo Nigusse Gemeda Shantawene G1 Natural","800",["口感:果香鮮明濃郁;亮點:藍莓果醬、香檳白酒韻味","甜感與酒香兼具的精品豆|遊玩角色:黃昏酒館裡的靈魂旅行家"]) \
+ bean("耶加雪菲・雪列圖 G1 水洗","Yirgacheffe Chelelektu G1 Washed","700",["口感:乾淨清爽,質地透亮;亮點:花檸檬、柑橘、伯爵茶、蜂蜜蜜桃","如清晨陽光般細緻,水洗愛好者首選|遊玩角色:晨光下的山城漫遊者"]) \
+ bean("耶加雪菲・雪列圖 G1 日曬","Yirgacheffe Chelelektu G1 Natural","700",["口感:花香與熱帶果香交融;亮點:葡萄乾、莓果、焦糖尾韻","甜感與酸質平衡,適合喜歡熱帶果韻的你|遊玩角色:熱帶果園的探路者"]) + """
</div>
</section>
<section>
<h2>新品上市</h2>
""" + bean("馬拉威藝伎|水洗","Malawi Geisha Washed・高海拔火山土壤、日夜溫差大・Geisha 品種,非洲風土×藝伎","900",["口感:花香、柑橘、檸檬表現;亮點:柑橘檸檬尾韻蜂蜜","酸質集中,適合喜歡熱帶果韻的你"]) + """
<div class="note">選購與客製化掛耳需求,歡迎至 <a href="https://sirshopping.cashier.ecpay.com.tw" target="_blank" rel="noopener">線上購物(綠界)</a> 或以 LINE(ID:onlycoffee99)聯繫我們。</div>
</section>
</main>
"""
page("beans.html","NEW 咖啡豆單",body,"時間到咖啡館咖啡豆單:NO.3~6號配方豆、衣索比亞精品單品豆(谷吉、西達摩、耶加雪菲)、新品馬拉威藝伎。")
