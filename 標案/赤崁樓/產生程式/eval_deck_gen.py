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

CREATED=json.load(open(R+'/deck.json'))['createdOnFiles']
E1='評選項目一｜專業能力與績效（10分）';E2='評選項目二｜經營管理內容、創意能力及經營策略（25分）';E3='評選項目三｜權利金報價合理性（20分）';E4='評選項目四｜財務規劃（15分）';E5='評選項目五｜空間使用規劃（15分）';E6='評選項目六｜環境、建物及設備管理維護計畫（15分）'

# cover
slides.append(('cover',f'''<section id="cover" data-transition="fade" style="background:{D};color:{L};font-family:{B};padding:128px;display:flex;flex-direction:column;justify-content:center;gap:40px">
<img src="{IMG['tea']}" alt="時間到茶館空間意象示意圖" style="position:absolute;left:1040px;top:0px;width:880px;height:1080px;object-fit:cover">
<div style="position:absolute;left:1040px;top:0px;width:880px;height:1080px;background:linear-gradient(90deg, #1E3A2F 0%, rgba(30,58,47,0) 35%)"></div>
<p style="width:860px;font-size:28px;font-weight:700;color:#E3A48F;letter-spacing:4px">臺南市政府文化局｜評選會議簡報</p>
<h1 style="width:860px;font-family:{H};font-size:80px;font-weight:700;line-height:1.2;color:{L}">赤崁樓遊客中心2樓部分空間委外經營管理案</h1>
<p style="width:860px;font-size:40px;line-height:1.4;color:{MD}">時間到茶館｜在赤崁，喝一杯有故事的臺灣茶</p>
<div style="display:flex;flex-direction:column;gap:8px;width:860px"><p style="font-size:32px;color:{L}">投標廠商：鑫和洋行</p><p style="font-size:32px;color:{L}">計畫主持人：鄭玉屏</p><p style="font-size:24px;color:{MD}">中華民國115年10月</p></div>
<aside>（約10秒）各位委員好，我是鑫和洋行計畫主持人鄭玉屏，向各位報告「時間到茶館」的經營規劃。</aside></section>'''))

content('errata','簡報前說明','服務建議書勘誤',
 table(['頁次','原文','更正為','說明'],[
  ['第3頁表1','蛙聚有限公司','<b>蚨聚有限公司</b>','依附件2-2租賃契約公證書'],
  ['第3頁','計畫主持人鄭玉萍小姐','<b>計畫主持人鄭玉屏小姐</b>','姓名誤植'],
  ['第3頁','咖啡烘培師、烘培','<b>咖啡烘焙師、烘焙</b>','錯字'],
  ['第26頁','固定權利金每月新臺幣550,000元','<b>固定權利金每年新臺幣550,000元</b>','與第24頁推估、表16一致'],
 ],[16,28,32,24],fs=28)+f'<p style="font-size:28px;color:{M}">以上均屬文字誤植，不影響服務內容及財務結論。</p>',
 '（約20秒）先說明服務建議書四處誤植：第26頁固定權利金應為「每年」55萬元，與第24頁推估及表16一致；第3頁台中館出租人為蚨聚有限公司、計畫主持人為鄭玉屏，烘焙二字一併更正。')

ag=[('一','專業能力與績效','10'),('二','經營管理內容、創意能力及經營策略','25'),('三','權利金報價合理性','20'),('四','財務規劃','15'),('五','空間使用規劃','15'),('六','環境、建物及設備之管理維護計畫','15')]
agh='<div style="display:flex;flex-direction:column;gap:16px">'+''.join(f'<div style="display:flex;align-items:center;gap:36px;padding:18px 40px;background:#FBF8F1;border:1px solid #D9CFBC;border-radius:16px"><p style="font-family:{H};font-size:40px;font-weight:700;color:{A};width:60px">{a}</p><p style="flex:1;font-size:34px;color:{D}">{b}</p><p style="font-size:30px;font-weight:700;color:{M}">{c}分</p></div>' for a,b,c in ag)+'</div>'
content('agenda','簡報大綱','依評選項目順序報告',agh,'（約5秒）以下依評選須知六個評選項目的順序報告。')

# 一 專業能力
content('record',E1,'鑫和洋行：公共場域經營實績',
 '<div style="display:flex;gap:40px;align-items:start"><div style="flex:1">'+table(['類別','實績內容'],[
  ['公共場域進駐','宜蘭礁溪溫泉公園「時間到咖啡館－公園裡的咖啡館」'],
  ['跨區門市','台中館：承租蚨聚有限公司經營之臺中市第二市場停車場附屬空間，115/9/19開幕'],
  ['品牌資產','「舞荳及圖」商標註冊第02507640號'],
  ['產學合作','佛光大學「玩咖系列」濾掛咖啡；USR國際交流'],
  ['產品檢測','2019年起委託金屬中心成分分析'],
  ['推廣教學','國安一期社宅咖啡手沖課（講師鄭玉屏）'],
 ],[24,76],fs=26)+f'</div><div style="width:420px;display:flex;flex-direction:column;gap:12px"><img src="{IMG["op"]}" alt="台中館開幕手沖儀式" style="width:420px;height:280px;object-fit:cover;border-radius:12px"><p style="font-size:24px;color:{M}">台中館開幕，臺中市停車管理處、中區區公所出席</p><img src="{IMG["jx"]}" alt="礁溪溫泉公園時間到咖啡館" style="width:420px;height:200px;object-fit:cover;border-radius:12px"></div></div>',
 '（約30秒）鑫和洋行民國107年成立，從礁溪溫泉公園起步，今年9月19日在台中第二市場停車場附屬空間開設台中館，臺中市停車管理處與中區區公所都有出席。我們有自有商標、產學合作與產品檢測紀錄，熟悉公部門場域的營運規範。')

content('pi',E1,'計畫主持人與承攬緣由',
 f'''<div style="display:flex;gap:56px;align-items:start"><div style="flex:1;display:flex;flex-direction:column;gap:20px">
<ul style="font-size:30px;line-height:1.6;color:{M}"><li>鄭玉屏：鑫和洋行營運長、本案主理人，咖啡烘焙師</li><li>店面SOP、菜單設計、品項開發與人員訓練</li><li>協辦宜蘭冬戀溫泉季、佛光大學文創市集</li></ul>
<div style="background:#FBF8F1;border-left:6px solid {A};padding:28px 36px"><p style="font-size:28px;line-height:1.6;color:{D}"><b>承攬緣由</b>：「舞荳」品牌源自陳玨霖老師題贈墨寶，我們一直在做「把餐飲和文化變成生活產品」；赤崁樓是最適合實踐這件事的場域。</p></div></div>
<img src="{IMG['cal']}" alt="陳玨霖老師題贈舞荳墨寶展出" style="width:480px;height:540px;object-fit:cover;border-radius:12px"></div>''',
 '（約25秒）我負責統籌本案。舞荳品牌來自陳玨霖老師的題字，我把書法用在包裝與詩文卡片。承攬本案的緣由很單純：赤崁樓的歷史，最適合變成旅客帶得走的一杯茶。')

content('team',E1,'協力團隊：由鑫和洋行單獨投標',
 table(['協力人員／單位','背景','本案分工'],[
  ['蔡錦佳老師','東華印刷局資訊科技企業社計畫主持人','印刷手作課程顧問'],
  ['黃荻昌副教授','長榮大學副教授，鐵道工程與文化資產','文化顧問、文化沙龍規劃'],
  ['徐鈺清','台灣瑰寶牛樟芝生物科技負責人','原生物產顧問、泡茶用水研討'],
  ['廣廓生活有限公司','Himalaya Smile 天然手作商品','文創選物規劃'],
  ['傳宇智聯有限公司','AI企業培訓及品牌行銷','社群經營與AI行銷'],
 ],[24,42,34],fs=28)+f'<p style="font-size:26px;color:{M}">均已簽署合作意向書（附件一）。本案依投標須知由鑫和洋行單獨投標，負全部履約責任。</p>',
 '（約15秒）協力團隊涵蓋印刷手作、文化史、原生物產與數位行銷，蔡老師與黃老師擔任顧問，負責規劃與指導。本案由鑫和洋行單獨投標，負全部履約責任。')

# 二 經營管理
n=len(slides)+1
slides.append(('vision',f'''<section id="vision" data-transition="fade" style="background:{A};color:{L};font-family:{B};padding:128px 128px 160px;display:flex;flex-direction:column;justify-content:center;gap:48px">
<p style="font-size:28px;font-weight:700;letter-spacing:2px;color:#F3D9CF">{E2}</p>
<h1 style="font-family:{H};font-size:104px;font-weight:700;line-height:1.2;color:{L}">守護場域、服務遊客、<br>轉譯文化</h1>
<p style="font-size:40px;line-height:1.5;width:1500px;color:#FBEDE6">經營目標：讓赤崁樓遊客中心2樓成為兼具文化深度、服務品質與營運韌性的文化複合空間。</p>
{foot(n,'dark')}<aside>（約10秒）我們的經營目標是：守護場域、服務遊客、轉譯文化。商業營運是讓文化被看見的方法，不是目的。</aside></section>'''))

content('product',E2,'經營內容：老茶新喝，臺灣茶手搖飲為主力',
 f'''<div style="display:flex;gap:48px;align-items:start"><div style="width:560px;display:flex;flex-direction:column;gap:24px">
<p style="font-size:32px;line-height:1.6;color:{D}">符合工作說明書「以輕飲食為規劃主軸」。傳統好茶以原茶、奶茶、果茶、茶凍、茶冰沙重新詮釋；每款茶附產區與製茶故事卡。</p>
<p style="font-size:28px;line-height:1.6;color:{M}">多語菜單（中英日韓）、環保杯折扣、兒童杯與無咖啡因選項。</p></div>
<div style="flex:1">{table(['收費項目','收費標準（元）'],[['臺灣原茶','50～90'],['奶茶與茶拿鐵','65～110'],['季節果茶（在地農產）','60～120'],['茶凍與茶冰沙','60～110'],['品茶組合','150～250'],['舞荳咖啡','90～180'],['甜品與茶點','50～150'],['文化體驗','免費～400／人']],[62,38],fs=26)}</div></div>''',
 '（約30秒）經營內容符合工作說明書「以輕飲食為規劃主軸」：以現點現做的臺灣茶手搖飲為主力，價格貼近一般遊客，平均客單價約115元。和周邊手搖飲的差別在故事，每一杯茶都附產區與製茶故事卡。')

content('culture',E2,'創意能力：文化內容與營運互相支持',
 table(['體驗','現場做法','對應收入'],[
  ['一杯茶認識臺灣','圖文介紹茶的製作與外銷故事','單杯茶飲、品茶組合'],
  ['赤崁建築與故事','圖卡呈現普羅民遮堡、贔屭馱碑','延長停留，帶動飲品甜品'],
  ['夏季也能喝茶','同一茶款延伸為茶凍與茶冰沙','不同季節與客群銷售'],
  ['智慧供茶','多語選茶、付款與標準化出茶','提升尖峰服務效率'],
  ['故事活動','茶文化體驗、親子故事場、團體預約','活動收入與團體消費'],
 ],[24,44,32],fs=28),
 '（約25秒）創意在於文化不是附加活動，而是設計在每個消費環節裡：旅客因為故事多停留，也因此多消費，形成可持續的循環。')

content('season',E2,'行銷推廣：四季主題，串聯在地',
 '<div style="display:flex;gap:24px">'+card('春季','春茶品飲會；兒童節親子故事場及茶點手作')+card('夏季','冷泡茶與茶冰沙；暑期學生文化體驗營；鐵道文化講座')+card('秋季','古蹟月文化沙龍：赤崁樓建築變遷與贔屭馱碑導覽')+card('冬季','年終選物市集、活版印刷賀卡手作；新春茶禮盒')+'</div>'
 +f'<p style="font-size:28px;line-height:1.6;color:{M}">IG、Facebook、LINE官方帳號、Google商家每週至少3則貼文；串聯赤嵌朋派商圈、赤嵌社區等在地組織；宣傳內容事先報機關同意。</p>',
 '（約25秒）行銷以四季為節奏，線上每週至少3則貼文，線下串聯周邊商圈與社區組織，推出「古蹟參訪＋一杯故事茶」套裝。所有宣傳避免政治及宗教內容，並事先報機關同意。')

content('staff',E2,'組織與人力：平日3人、假日5人在場',
 '<div style="display:flex;gap:40px;align-items:start"><div style="flex:1">'+table(['職稱','人數','工作職掌'],[
  ['計畫主持人','1','鄭玉屏，統籌履約與機關聯繫'],['店長','1','現場管理、食安及消防安全管理人'],['茶飲調製人員','3','茶飲及咖啡製作、商品解說'],['外場服務人員','1','接待點餐、環境整理、遊客諮詢'],['兼職人員','2～3','假日及活動支援，優先聘在地居民'],['行政及會計','1（兼）','帳務、採購、報表、保險']],[26,14,60],fs=26)+'</div>'
 +card('教育訓練','職前訓練16小時（古蹟規範、食安、消防、赤崁樓導覽）；每年食品衛生講習8小時；每季服務及茶飲專業訓練',extra=';flex:none;width:520px')+'</div>',
 '（約20秒）現場人力平日至少3人、假日至少5人，由計畫主持人統籌督導。新進人員職前訓練16小時，內容包括古蹟場域規範與赤崁樓導覽。')

content('review',E2,'執行能力：對應年度考核五大項目',
 table(['考核項目（權重）','本團隊做法'],[
  ['營運計畫執行（含財務）25%','依核定計畫營運；會計獨立、每月損益檢討、營運月報'],
  ['設備維修及環境清潔 25%','設備保養表定執行並建檔；每2小時巡檢公共區域'],
  ['歷史、文化及藝術教育推廣 25%','每年24場以上文化沙龍及體驗；茶款附故事卡'],
  ['與文化局配合度 15%','機關借用場地優先無償提供；宣傳事先報准；主持人親自出席考核'],
  ['顧客滿意度或投訴率 10%','每半年滿意度調查，目標85%以上；意見3日內回覆'],
 ],[36,64],fs=28)+f'<p style="font-size:28px;color:{M}">自我評估目標：年度考核85分以上（75分通過），作為後續擴充3年之依據。</p>',
 '（約20秒）執行能力的部分，我們把文化局年度考核的五個項目，逐項對應到具體做法，以85分為目標，高於75分的通過標準。')

# 三 權利金
content('basis',E3,'固定權利金：依周邊租金行情推估',
 f'''<div style="display:flex;gap:40px;align-items:start"><div style="flex:1">{table(['周邊租金熱點','一樓每坪月租金（元）'],[['中正路、國華街三段','2,100～3,273'],['中山路、西門路二段','889～3,375'],['民族路二段（參考基準）','1,200～1,472'],['民生路一段','596～833']],[58,42],fs=28)}<p style="font-size:24px;color:{M}">資料來源：591房屋交易網，本團隊彙整分析</p></div>
<div style="width:640px;display:flex;flex-direction:column;gap:16px;background:{D};padding:40px;border-radius:16px">
<p style="font-size:28px;line-height:1.6;color:{MD}">1,300元 × 70%（商圈繁榮度）× 75%（二樓樓層效用）＝ 683元</p>
<p style="font-size:28px;line-height:1.6;color:{MD}">（683 ＋ 管理費62元）× 12月 × 61.51坪</p>
<p style="font-family:{H};font-size:56px;font-weight:700;color:{L}">≈ 549,899元／年</p>
<p style="font-size:28px;color:#E3A48F">報價：每年55萬元，高於契約底價54萬元</p></div></div>''',
 '（約30秒）固定權利金不是隨意加價，而是依市場行情推估。以民族路二段一樓每坪1,300元為基準，考量赤崁樓商圈繁榮度與二樓樓層效用，加上管理費，推估每年約55萬元，高於契約底價54萬元，是我們有能力長期穩定繳納的合理金額。')

roy=table(['年度','預估年營業額','超過540萬部分','變動權利金（2%）','權利金合計'],[
  ['第一年','8,327,040','2,927,040','58,541','<b>608,541</b>'],
  ['第二年','9,576,096','4,176,096','83,522','<b>633,522</b>'],
  ['第三年','10,096,536','4,696,536','93,931','<b>643,931</b>']],[14,22,22,22,20],fs=26)
content('royalty',E3,'固定保底，營收超過目標值再分享',
 f'''<div style="display:flex;gap:28px">
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{D};padding:36px 40px;border-radius:16px"><p style="font-size:26px;color:{MD}">固定權利金（外加5%營業稅）</p><p style="font-family:{H};font-size:64px;font-weight:700;color:{L}">每年55萬元</p><p style="font-size:26px;line-height:1.5;color:{MD}">不論營運好壞照繳；五年合計275萬元</p></div>
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF8F1;padding:36px 40px;border:1px solid #D9CFBC;border-radius:16px"><p style="font-size:26px;color:{M}">變動權利金（外加5%營業稅）</p><p style="font-family:{H};font-size:64px;font-weight:700;color:{A}">超過540萬部分×2%</p><p style="font-size:26px;line-height:1.5;color:{M}">契約第4條：未達540萬元免繳；依401申報書計算</p></div></div>
{roy}<p style="font-size:24px;color:{M}">單位：新臺幣元（未稅）；營業額依服務建議書表15。</p>''',
 '（約30秒）變動權利金依契約第4條：當年度營業收入超過目標值540萬元的部分收2%，以401申報書計算。依我們的營收預估，前三年每年繳給市府約61萬到64萬元。固定保底、成長共享，市府的收入有保障，我們也能長期穩定經營。')

# 四 財務
content('invest',E4,'投資金額與經費來源',
 f'''<div style="display:flex;gap:40px;align-items:start"><div style="flex:1">{table(['項目','金額（元）'],[['可復原式室內裝修及木作','800,000'],['吧台及餐飲設備','550,000'],['家具及陳設','250,000'],['資訊及安全設備','100,000'],['<b>開辦小計</b>','<b>1,700,000</b>'],['營運週轉金（約3個月）','300,000'],['<b>總投入資金</b>','<b>2,000,000</b>']],[64,36],fs=28)}</div>
<div style="width:560px;display:flex;flex-direction:column;gap:24px">
<div style="display:flex;flex-direction:column;gap:8px;background:{D};padding:36px 40px;border-radius:16px"><p style="font-size:26px;color:{MD}">自有資金</p><p style="font-family:{H};font-size:64px;font-weight:700;color:{L}">140萬元（70%）</p></div>
<div style="display:flex;flex-direction:column;gap:8px;background:#FBF8F1;padding:36px 40px;border:1px solid #D9CFBC;border-radius:16px"><p style="font-size:26px;color:{M}">金融機構貸款</p><p style="font-family:{H};font-size:64px;font-weight:700;color:{A}">60萬元（30%）</p></div>
<p style="font-size:26px;line-height:1.5;color:{M}">開辦費用分3年攤提；每年另自盈餘提撥營業額1%為設備汰換準備金</p></div></div>''',
 '（約20秒）總投入資金200萬元，其中開辦170萬元、週轉金30萬元。七成是自有資金，三成向金融機構貸款。開辦費用分3年攤提，另外每年提撥營業額1%作為設備汰換準備金。')

content('finance',E4,'分年收支預算：以來客數達基本面為前提',
 f'''<div style="display:flex;gap:40px;align-items:start"><div style="flex:1">{table(['項目（元）','第一年','第二年','第三年'],[['營業收入','8,327,040','9,576,096','10,096,536'],['原物料、包材及商品','3,078,125','3,539,844','3,732,227'],['人事費用','2,880,000','2,966,400','3,055,392'],['權利金（固定＋變動）','608,541','633,522','643,931'],['水電、行銷、保險、雜支等','1,141,258','1,235,046','1,281,853'],['開辦攤提','566,667','566,667','566,667'],['<b>稅前損益</b>','<b>52,449</b>','<b>634,617</b>','<b>816,466</b>']],[37,21,21,21],fs=24)}</div>
<div style="width:400px;display:flex;flex-direction:column;gap:12px;background:{A};padding:36px;border-radius:16px"><p style="font-size:26px;color:#F3D9CF">損益兩平</p><p style="font-family:{H};font-size:80px;font-weight:700;color:{L};line-height:1.1">207人次</p><p style="font-size:26px;line-height:1.5;color:#FBEDE6">每日平均來客；穩定水準估260人次、客單價115元</p></div></div>
<p style="font-size:26px;line-height:1.5;color:{M}">營收爬坡80%／92%／97%；稅前淨利率0.6%／6.6%／8.1%。地價稅、房屋稅列於雜支。</p>''',
 '（約30秒）財務採保守估算。第一年只估穩定水準的八成，約損益兩平；第二、三年稅前淨利率約6.6%與8.1%。前提是來客數達到基本面：每日平均約207人次才能損益兩平。契約規定的地價稅、房屋稅由廠商負擔，已列在雜支項目內。')

# 五 空間
content('space',E5,'空間使用規劃：約62坪，動線清楚',
 f'''<div style="display:flex;gap:48px;align-items:start"><div style="width:760px;display:flex;flex-direction:column;gap:16px"><img src="{IMG['plan']}" alt="赤崁樓遊客中心2樓平面圖，紅框為委外範圍" style="width:760px;height:380px;object-fit:contain;background:#FFFFFF;border:1px solid #D9CFBC;border-radius:12px"><p style="font-size:24px;color:{M}">紅框為委外範圍（招標文件平面圖）</p></div>
<div style="flex:1">{table(['分區','面積'],[['入口接待及展售區','8坪'],['手搖飲吧台及備料區','12坪'],['休憩座位區（約36席）','20坪'],['文化沙龍多功能區（約30人）','14坪'],['倉儲及員工區','4坪'],['公共動線（淨寬1.2m以上）','4坪']],[74,26],fs=26)}</div></div>''',
 '（約20秒）委外範圍203.35平方公尺、約62坪，分為六區。吧台與洗滌設備靠北側，鄰近既有給排水；文化沙龍區平日為座位，活動時轉為講座空間，可容納約30人。')

content('design',E5,'裝修設計：不破壞古蹟、可復原',
 f'''<div style="display:flex;gap:48px;align-items:start"><img src="{IMG['tea']}" alt="時間到茶館空間意象示意圖" style="width:820px;height:520px;object-fit:cover;border-radius:12px">
<ul style="flex:1;font-size:28px;line-height:1.6;color:{M}"><li>活動式家具與模組化櫃體，不鑽孔、不變更結構</li><li>吧台全部電熱設備，不用明火及桶裝瓦斯</li><li>茶葉綠、原木與暖光；照明避免直射古蹟視野</li><li>無障礙座位與通道</li><li>設計圖說於簽約次日起30日內送審，核定後施作</li></ul></div>
<p style="font-size:24px;color:{M}">空間意象示意圖，實際以機關核定設計圖說為準</p>''',
 '（約20秒）裝修以可復原為原則：活動式家具、不鑽孔、不變更結構；吧台全部電熱，不用明火。設計圖說在簽約次日起30日內送審，核定後才施作。')

st=lambda big,unit,cap: f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF8F1;padding:40px;border:1px solid #D9CFBC;border-radius:16px"><p style="font-family:{H};font-size:96px;font-weight:700;color:{A};line-height:1.1">{big}<span style="color:{D}">{unit}</span></p><p style="font-size:28px;line-height:1.5;color:{M}">{cap}</p></div>'
content('ops',E5,'開放時間：優於契約要求',
 '<div style="display:flex;gap:28px">'+st('6','日','每週營業（週二至週日）<br>契約要求不少於5日')+st('9','時','每日10:00–19:00<br>契約要求不少於8小時')+st('假日','照常','國定假日、連續假期<br>照常營業')+'</div>'
 +f'<p style="font-size:28px;line-height:1.6;color:{M}">週一為公休及設備保養日；開放時間於現場明顯處設告示牌；配合機關活動可延長；調整均事先取得機關書面同意。</p>',
 '（約15秒）開放時間每週6日、每日9小時，都優於契約下限；國定假日與連續假期照常營業，週一公休做設備保養。')

# 六 管理維護
content('manage',E6,'環境、建物及設備管理維護',
 '<div style="display:flex;gap:24px">'+card('清潔與設備','每日開閉店清潔、每2小時巡檢；空調、給排水、冷藏冷凍等依表定保養並登記建檔；聯網設備不用中國品牌')+card('防災與防盜','設防火管理人；每半年至少1次防災演練並邀機關參與；監視錄影與夜間保全；現金每日存入銀行')+card('保險','依契約額度投保公共意外責任險、火災險（250萬元以上）及產品責任險，保單送機關備查')+'</div>'
 +f'<p style="font-size:28px;line-height:1.6;color:{M}">點交時建立財產及設備清冊並拍照存檔；損壞即時通報機關並負責修復；期滿15日內點交返還。</p>',
 '（約30秒）管理維護從點交開始：建立財產及設備清冊並拍照，設備依表定保養並建檔。防災方面設防火管理人，每半年至少一次演練；保險依契約額度投保。任何損壞即時通報機關並負責修復。')

n=len(slides)+1
slides.append(('closing',f'''<section id="closing" data-transition="fade" style="background:{D};color:{L};font-family:{B};padding:128px 128px 160px;display:flex;flex-direction:column;justify-content:center;gap:48px">
<h1 style="font-family:{H};font-size:88px;font-weight:700;line-height:1.3;color:{L};width:1500px">讓赤崁樓的故事，<br>留在旅客手中的一杯茶裡</h1>
<p style="font-size:40px;color:{MD}">鑫和洋行　敬請指教</p>
{foot(n,'dark')}<aside>（約5秒）以上報告，謝謝各位委員，敬請指教。</aside></section>'''))

os.makedirs(R+'/slides',exist_ok=True)
for id,s in slides: open(f'{R}/slides/{id}.html','w').write(s)
deck={"v":4,"createdOnFiles":CREATED,"title":"赤崁樓評選簡報","order":[i for i,_ in slides],
 "sections":{"s0":{"description":"開場、勘誤與大綱","start":"cover"},"s1":{"description":"專業能力與績效（10分）","start":"record"},"s2":{"description":"經營管理內容、創意能力及經營策略（25分）","start":"vision"},"s3":{"description":"權利金報價合理性（20分）","start":"basis"},"s4":{"description":"財務規劃（15分）","start":"invest"},"s5":{"description":"空間使用規劃（15分）","start":"space"},"s6":{"description":"環境、建物及設備管理維護（15分）","start":"manage"}},
 "faces":{"noto-serif-tc":{"family":"Noto Serif TC","href":"https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&display=swap"},"noto-sans-tc":{"family":"Noto Sans TC","href":"https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap"}},"designSystems":[]}
json.dump(deck,open(R+'/deck.json','w'),ensure_ascii=False,indent=1)
print(len(slides),[i for i,_ in slides])
import re
tot=sum(len(re.sub('（約\d+秒）','',re.search(r'<aside>(.*?)</aside>',s,re.S).group(1))) for _,s in slides);print('note chars',tot)
