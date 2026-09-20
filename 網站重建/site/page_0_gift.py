# 中秋禮盒新品頁
def flavor(name, en, notes, quote):
    return f"<div class='card'><h3>{name}</h3><p class='muted'>{en}</p><p>{notes}</p><p class='muted'>{quote}</p></div>"

body = """
<div class="hero"><h1>中秋精品咖啡禮盒</h1><p>五款精品掛耳、五段天色——把一整天的天空,裝進一盒祝福裡。</p>
<p style="position:relative;z-index:2;font-size:1.3rem;font-weight:700;margin-top:6px">一盒五入 NT$250</p>
<a class="cta" href="https://sirshopping.cashier.ecpay.com.tw" target="_blank" rel="noopener">綠界線上訂購</a>
</div>
<main class="wrap">
<section>
<h2>新品上市|一盒五入,五段天色</h2>
<div class="card photo-card"><img src="assets/gift.jpg" alt="Time Coffee 中秋五入精品咖啡禮盒,五款掛耳包以天空漸層設計" loading="lazy">
<p class="muted">每一包掛耳,都是一片天空——從深夜的星藍、破曉的霞紫,到清晨的粉藍與原野的青綠。五款精品咖啡各自獨立包裝,拼起來,就是完整的一天。</p></div>
</section>
<section>
<h2>五款風味</h2>
<div class="grid">
""" + flavor("耶加雪菲","Yirgacheffe Sheleto","花香、柑橘、茉莉,甜美水質——彩色莓果與熱帶水果,風味明亮輕盈。","Hope is everything possible.") \
+ flavor("西達瑪","Aleta Wondo Sidama G","柑橘、熱帶水果,甜感平衡——檸檬與花香交織,清新有層次。","You become a conduit of light.") \
+ flavor("谷吉布穀","Guji Buku Hambella G","莓果、桃香、茶感,甜感細緻——葡萄、柑橘與蜜桃香氣,甜感飽滿。","If you can't live long, live deep.") \
+ flavor("藝伎","Geisha","花香、柑橘、蜂蜜、霜蜜,果感細緻——乾淨柔和、尾韻優雅。","The essence of creation is a good life, not perfection.") \
+ flavor("黃金曼特寧","Golden Mandheling","烘焙堅果、黑糖,濃厚醇香——焦糖調醇厚沉穩,回甘悠長。","The distance to a good will is the evolution.") + """
</div>
</section>
<section>
<h2>訂購方式</h2>
<div class="grid">
<div class="card"><h3>少量訂購</h3><p><strong>每盒 NT$250</strong>(五入)。直接透過綠界線上付款,台灣本島宅配。</p><p><a class="cta" style="display:inline-block;background:var(--accent);color:#fff;padding:10px 26px;border-radius:22px;font-weight:700" href="https://sirshopping.cashier.ecpay.com.tw" target="_blank" rel="noopener">前往綠界訂購</a></p></div>
<div class="card"><h3>企業/團體訂購</h3><p>中秋送禮大宗採購、企業客製(加印 LOGO、賀卡),請以 LINE 或電話聯繫,確認價格與交期後再付款。</p><p>LINE ID:onlycoffee99<br>電話:03-936-3306/0975-328-779</p></div>
</div>
<div class="note">海外訂購請至 <a href="https://5wudou.com" target="_blank" rel="noopener">舞荳購物網(5wudou.com)</a>;更多禮盒介紹也可參考 <a href="https://time-coffee-midautumn-gift.onlycoffee99.chatgpt.site" target="_blank" rel="noopener">禮盒介紹頁</a>。</div>
</section>
</main>
"""
page("gift.html","中秋精品咖啡禮盒",body,"Time Coffee 中秋五入精品咖啡禮盒:耶加雪菲、西達瑪、谷吉布穀、藝伎、黃金曼特寧,天空漸層包裝,綠界線上訂購。")
