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

# 1 cover
slides.append(('cover',f'''<section id="cover" data-transition="fade" style="background:{D};color:{L};font-family:{B};padding:128px;display:flex;flex-direction:column;justify-content:center;gap:40px">
<img src="{IMG['tea']}" alt="時間到茶館空間意象示意圖" style="position:absolute;left:1040px;top:0px;width:880px;height:1080px;object-fit:cover">
<div style="position:absolute;left:1040px;top:0px;width:880px;height:1080px;background:linear-gradient(90deg, #1E3A2F 0%, rgba(30,58,47,0) 35%)"></div>
<p style="width:860px;font-size:28px;font-weight:700;color:#E3A48F;letter-spacing:4px">臺南市政府文化局｜評選會議簡報</p>
<h1 style="width:860px;font-family:{H};font-size:80px;font-weight:700;line-height:1.2;color:{L}">赤崁樓遊客中心2樓部分空間委外經營管理案</h1>
<p style="width:860px;font-size:40px;line-height:1.4;color:{MD}">時間到茶館｜在赤崁，喝一杯有故事的臺灣茶</p>
<div style="display:flex;flex-direction:column;gap:8px;width:860px"><p style="font-size:32px;color:{L}">投標廠商：鑫和洋行</p><p style="font-size:32px;color:{L}">計畫主持人：鄭玉屏</p><p style="font-size:24px;color:{MD}">中華民國115年10月</p></div>
<aside>各位評選委員好，我是鑫和洋行計畫主持人鄭玉屏。今天向各位報告本團隊對赤崁樓遊客中心2樓的經營規劃，主軸是「時間到茶館」——在赤崁，喝一杯有故事的臺灣茶。（右側為空間意象示意圖，實際以核定設計圖說為準。）</aside></section>'''))

# 2 errata
content('errata','簡報前說明','服務建議書勘誤',
 table(['頁次','原文','更正為','說明'],[
  ['第3頁表1','蛙聚有限公司','<b>蚨聚有限公司</b>','依附件2-2租賃契約公證書'],
  ['第3頁','計畫主持人鄭玉萍小姐','<b>計畫主持人鄭玉屏小姐</b>','姓名誤植'],
  ['第3頁','咖啡烘培師、烘培','<b>咖啡烘焙師、烘焙</b>','錯字'],
  ['第26頁','固定權利金每月新臺幣550,000元','<b>固定權利金每年新臺幣550,000元</b>','與第24頁推估、表16一致'],
 ],[16,28,32,24],fs=26)+f'<p style="font-size:28px;color:{M}">以上均屬文字誤植，不影響服務內容與財務結論。權利金以「每年」計收；變動權利金門檻540萬元與契約一致。</p>',
 '正式報告前，先向委員說明服務建議書中的幾處誤植。最重要的是第26頁：固定權利金應為「每年」55萬元，第24頁的推估與表16的試算都以每年計；變動權利金門檻540萬元與契約第4條一致，沒有錯。另外第3頁台中館的出租人是「蚨聚有限公司」，計畫主持人是鄭玉屏，烘焙兩字也一併更正。')

# 3 agenda
items=[('壹','團隊介紹與經營願景'),('貳','整體營運與服務規劃'),('參','營運管理與組織人力'),('肆','權利金與財務營運規劃'),('伍','履約執行與管理維護')]
ag='<div style="display:flex;flex-direction:column;gap:20px">'+''.join(f'<div style="display:flex;align-items:center;gap:40px;padding:24px 40px;background:#FBF8F1;border:1px solid #D9CFBC;border-radius:16px"><p style="font-family:{H};font-size:44px;font-weight:700;color:{A};width:80px">{a}</p><p style="font-size:36px;color:{D}">{b}</p></div>' for a,b in items)+'</div>'
content('agenda','簡報大綱','五個部分，依服務建議書章節',ag,'簡報依服務建議書五個章節進行，約15分鐘。')

# 4 statement
n=len(slides)+1
slides.append(('vision',f'''<section id="vision" data-transition="fade" style="background:{A};color:{L};font-family:{B};padding:128px 128px 160px;display:flex;flex-direction:column;justify-content:center;gap:48px">
<p style="font-size:28px;font-weight:700;letter-spacing:4px;color:#F3D9CF">經營主張</p>
<h1 style="font-family:{H};font-size:104px;font-weight:700;line-height:1.2;color:{L}">守護場域、服務遊客、<br>轉譯文化</h1>
<p style="font-size:40px;line-height:1.5;width:1500px;color:#FBEDE6">在古蹟場域經營，首要任務不是追求最大營業額，而是以穩定、可持續的營運回饋機關與地方。</p>
{foot(n,'dark')}<aside>這是我們的經營態度。赤崁樓是國定古蹟，我們把自己定位為場域的守護者與文化的轉譯者，商業營運是讓文化被看見的方法，而不是目的。</aside></section>'''))

# 5 track record
content('record','壹、團隊介紹','鑫和洋行近年業務實績',
 table(['類別','實績內容'],[
  ['公共場域進駐','宜蘭礁溪溫泉公園「時間到咖啡館－公園裡的咖啡館」，提供園區遊客餐飲服務'],
  ['跨區門市經營','台中館：承租蚨聚有限公司經營之臺中市第二市場停車場附屬空間（115/3/20租約公證），115/9/19開幕'],
  ['品牌資產','「舞荳及圖」商標註冊（第02507640號，第030類）'],
  ['產學合作','佛光大學「玩咖系列」濾掛咖啡；教育部USR國際交流活動'],
  ['產品檢測','2019年起委託金屬工業研究發展中心進行產品成分分析'],
  ['推廣教學','115/9/5 國安一期社會住宅咖啡手沖體驗課程（講師鄭玉屏）'],
 ],[20,80],fs=28),
 '鑫和洋行民國107年成立，從宜蘭礁溪溫泉公園起步，今年再到台中第二市場設立台中館，9月19日開幕，臺中市停車管理處與中區區公所都有出席。我們同時有自有商標、產學合作與產品檢測紀錄。佐證見服務建議書附件二。')

# 6 photos
ph=lambda src,alt,cap: f'<div style="flex:1;display:flex;flex-direction:column;gap:16px"><img src="{src}" alt="{alt}" style="width:536px;height:400px;object-fit:cover;border-radius:12px"><p style="font-size:26px;line-height:1.4;color:{M}">{cap}</p></div>'
content('field','壹、團隊介紹','公共場域經營，已在現場',
 '<div style="display:flex;gap:28px">'+ph(IMG['jx'],'礁溪溫泉公園時間到咖啡館','宜蘭礁溪溫泉公園<br>公園裡的咖啡館')+ph(IMG['op'],'台中館開幕手沖儀式','台中館開幕（115/9/19）<br>停車管理處、中區區公所出席')+ph(IMG['cls'],'國安社宅手沖體驗課程','國安一期社宅手沖課（115/9/5）<br>講師鄭玉屏')+'</div>',
 '三張照片分別是礁溪、台中館開幕與社宅手沖課。我們熟悉公部門場域的規範：營業時間、清潔、消防與活動報備，這些經驗會直接用在赤崁樓。')

# 7 PI
content('pi','壹、計畫主持人','鄭玉屏：把餐飲和文化變成生活產品',
 f'''<div style="display:flex;gap:56px;align-items:start"><div style="flex:1;display:flex;flex-direction:column;gap:20px">
<ul style="font-size:30px;line-height:1.6;color:{M}"><li>鑫和洋行營運長、本案主理人，咖啡烘焙師</li><li>店面SOP、菜單設計、品項開發與人員訓練</li><li>協辦宜蘭冬戀溫泉季、佛光大學文創市集</li><li>上海咖啡展、馬來西亞展售等國際交流</li></ul>
<div style="background:#FBF8F1;border-left:6px solid {A};padding:28px 36px"><p style="font-size:28px;line-height:1.6;color:{D}">「舞荳」二字為宜蘭縣書法學會陳玨霖老師題贈（2024/9/17），鄭玉屏據以發展品牌識別與文化生活商品。</p></div></div>
<img src="{IMG['cal']}" alt="陳玨霖老師題贈舞荳墨寶展出" style="width:520px;height:560px;object-fit:cover;border-radius:12px"></div>''',
 '我負責統籌本案。舞荳品牌來自陳玨霖老師的題字，我把書法放進咖啡包裝與詩文卡片，這正是本案要做的事：讓赤崁樓的歷史，變成旅客帶得走的一杯茶、一份伴手禮。')

# 8 partners
content('team','壹、協力團隊','跨領域協力，由鑫和洋行單獨投標',
 table(['協力人員／單位','背景','本案分工'],[
  ['蔡錦佳老師','東華印刷局資訊科技企業社計畫主持人','印刷手作課程顧問'],
  ['黃荻昌副教授','長榮大學副教授，鐵道工程與文化資產','文化顧問；「府城交通與城市記憶」沙龍規劃'],
  ['徐鈺清','台灣瑰寶牛樟芝生物科技負責人','臺灣原生物產顧問；泡茶用水研討'],
  ['廣廓生活有限公司','Himalaya Smile 天然手作商品','文創選物規劃'],
  ['傳宇智聯有限公司','AI企業培訓及品牌行銷','社群經營與AI行銷工具'],
 ],[24,40,36],fs=28)+f'<p style="font-size:26px;color:{M}">均已簽署合作意向書（附件一）。本案由鑫和洋行單獨投標，協力人員依意向書提供專業協助。</p>',
 '協力團隊涵蓋印刷手作、文化史、原生物產與數位行銷。蔡老師與黃老師是顧問角色，負責規劃與指導，現場課程由本團隊人員帶領。本案依投標須知不允許共同投標，因此由鑫和洋行單獨投標並負全部履約責任。')

# 9 positioning
content('product','貳、整體營運','老茶新喝：臺灣茶手搖飲為主力',
 f'''<div style="display:flex;gap:48px;align-items:start"><div style="width:560px;display:flex;flex-direction:column;gap:24px">
<p style="font-size:32px;line-height:1.6;color:{D}">傳統好茶以原茶、奶茶、果茶、茶凍、茶冰沙重新詮釋；每款茶附產區與製茶故事卡。</p>
<p style="font-size:28px;line-height:1.6;color:{M}">多語菜單（中英日韓）、自備環保杯折扣、兒童杯與無咖啡因選項。</p></div>
<div style="flex:1">{table(['類別','參考售價（元）'],[['臺灣原茶','50～90'],['奶茶與茶拿鐵','65～110'],['季節果茶（在地農產）','60～120'],['茶凍與茶冰沙','60～110'],['品茶組合','150～250'],['舞荳咖啡','90～180'],['甜品與茶點','50～150'],['文創選物','150～1,200']],[62,38],fs=26)}</div></div>''',
 '我們以現點現做的臺灣茶手搖飲為主力，價格貼近一般遊客，平均客單價約115元。與周邊手搖飲的差別在於故事：每一杯茶都有產區與製茶故事卡。')

# 10 culture x revenue
content('culture','貳、整體營運','文化內容與營運互相支持',
 table(['體驗','現場做法','對應收入'],[
  ['一杯茶認識臺灣','圖文介紹茶的製作與外銷故事','單杯茶飲、品茶組合'],
  ['赤崁建築與故事','圖卡呈現普羅民遮堡、贔屭馱碑','延長停留，帶動飲品甜品'],
  ['夏季也能喝茶','同一茶款延伸為茶凍與茶冰沙','不同季節與客群銷售'],
  ['智慧供茶','多語選茶、付款與標準化出茶','提升尖峰服務效率'],
  ['故事活動','茶文化體驗、親子故事場、團體預約','活動收入與團體消費'],
 ],[24,44,32],fs=28),
 '文化不是附加活動，而是設計在每一個消費環節裡。旅客因故事多停留，也因此多消費，形成可持續的循環。')

# 11 space
content('space','貳、空間規劃','約62坪：不破壞古蹟、可復原、動線清楚',
 f'''<div style="display:flex;gap:48px;align-items:start"><div style="width:760px;display:flex;flex-direction:column;gap:16px"><img src="{IMG['plan']}" alt="赤崁樓遊客中心2樓平面圖，紅框為委外範圍" style="width:760px;height:380px;object-fit:contain;background:#FFFFFF;border:1px solid #D9CFBC;border-radius:12px"><p style="font-size:24px;color:{M}">紅框為委外範圍（招標文件平面圖）；實際配置以點交丈量及機關核定設計圖說為準</p></div>
<div style="flex:1">{table(['分區','面積'],[['入口接待及展售區','8坪'],['手搖飲吧台及備料區','12坪'],['休憩座位區（約36席）','20坪'],['文化沙龍多功能區','14坪'],['倉儲及員工區','4坪'],['公共動線（淨寬1.2m以上）','4坪']],[72,28],fs=26)}</div></div>''',
 '委外範圍203.35平方公尺，約62坪。全部採活動式家具與模組化櫃體，不鑽孔、不變更結構；吧台一律電熱設備，不使用明火與桶裝瓦斯。設計圖說於簽約次日起30日內併同營運管理維護計畫送審。')

# 12 hours stats
st=lambda big,unit,cap: f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF8F1;padding:40px;border:1px solid #D9CFBC;border-radius:16px"><p style="font-family:{H};font-size:96px;font-weight:700;color:{A};line-height:1.1">{big}<span style="color:{D}">{unit}</span></p><p style="font-size:28px;line-height:1.5;color:{M}">{cap}</p></div>'
content('ops','貳、營運作業','營業時間優於契約要求',
 '<div style="display:flex;gap:28px">'+st('6','日','每週營業日（週二至週日）<br>契約要求不少於5日')+st('9','時','每日10:00–19:00<br>契約要求不少於8小時')+st('3','日','一般意見回覆時限')+st('24','時','重大客訴處理完畢')+'</div>'
 +f'<p style="font-size:28px;line-height:1.6;color:{M}">營業前、營業中、營業後三階段SOP，由值班主管逐項檢核簽名；國定假日與連續假期照常營業，可配合機關活動延長。</p>',
 '營業時間每週6日、每日9小時，都比契約下限多。顧客意見3日內回覆，重大客訴當日通報、24小時內處理完畢。')

# 13 seasons
content('season','參、行銷推廣','四季行銷，結合在地節慶',
 '<div style="display:flex;gap:24px">'+card('春季','春茶品飲會；兒童節親子故事場及茶點手作')+card('夏季','冷泡茶與茶冰沙；暑期學生文化體驗營；鐵道文化講座')+card('秋季','古蹟月文化沙龍：赤崁樓建築變遷與贔屭馱碑導覽')+card('冬季','年終選物市集、活版印刷賀卡手作；新春茶禮盒')+'</div>'
 +f'<p style="font-size:28px;line-height:1.6;color:{M}">IG、Facebook、LINE官方帳號、Google商家每週至少3則貼文；串聯赤嵌朋派商圈、赤嵌社區等在地組織。所有宣傳避免政治性及宗教性，並事先報機關同意。</p>',
 '行銷以四季為節奏。線上由傳宇智聯協助AI行銷與社群，線下串聯周邊商圈與社區組織，推出「古蹟參訪＋一杯故事茶」的套裝。')

# 14 royalty
roy=table(['年度','預估年營業額','超過540萬部分','變動權利金（2%）','權利金合計'],[
  ['第一年','8,327,040','2,927,040','58,541','<b>608,541</b>'],
  ['第二年','9,576,096','4,176,096','83,522','<b>633,522</b>'],
  ['第三年','10,096,536','4,696,536','93,931','<b>643,931</b>']],[14,22,22,22,20],fs=26)
content('royalty','肆、權利金','固定保底，營收超過目標值再分享',
 f'''<div style="display:flex;gap:28px">
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{D};padding:36px 40px;border-radius:16px"><p style="font-size:26px;color:{MD}">固定權利金（外加5%營業稅）</p><p style="font-family:{H};font-size:64px;font-weight:700;color:{L}">每年55萬元</p><p style="font-size:26px;line-height:1.5;color:{MD}">高於契約底價每年54萬元；依周邊租金推估 (683+62)元×12月×61.51坪 ≈ 549,899元</p></div>
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF8F1;padding:36px 40px;border:1px solid #D9CFBC;border-radius:16px"><p style="font-size:26px;color:{M}">變動權利金（外加5%營業稅）</p><p style="font-family:{H};font-size:64px;font-weight:700;color:{A}">超過540萬部分×2%</p><p style="font-size:26px;line-height:1.5;color:{M}">契約第4條：未達540萬元免繳；依401申報書計算</p></div></div>
{roy}<p style="font-size:24px;color:{M}">單位：新臺幣元（未稅）；營業額依服務建議書表15。契約期5年，固定權利金五年合計275萬元。</p>''',
 '權利金分兩層。固定權利金每年55萬元，高於契約底價54萬元，是依周邊租金行情推估的合理水準，不論營運好壞都照繳。變動權利金依契約第4條：當年度稅前營業收入超過目標值540萬元的部分收2%，不是全部營業額乘2%；未達540萬免繳，第一年依實際履約日數折算目標值，以401申報書為依據。依預估營收，前三年每年繳給市府約61萬到64萬元，外加營業稅。')

# 15 finance
content('finance','肆、財務可行性','保守估算：以來客數達基本面為前提',
 f'''<div style="display:flex;gap:40px;align-items:start"><div style="flex:1">{table(['項目','第一年','第二年','第三年'],[['營收爬坡（穩定水準）','80%','92%','97%'],['年營業收入','832.7萬','957.6萬','1,009.7萬'],['稅前損益','約損益兩平','約64萬','約82萬'],['稅前淨利率','—','6.6%','8.1%']],[37,21,21,21],fs=28)}</div>
<div style="width:520px;display:flex;flex-direction:column;gap:12px;background:{A};padding:40px;border-radius:16px"><p style="font-size:26px;color:#F3D9CF">損益兩平</p><p style="font-family:{H};font-size:88px;font-weight:700;color:{L};line-height:1.1">207人次</p><p style="font-size:26px;line-height:1.5;color:#FBEDE6">每日平均來客；穩定水準估每日260人次、客單價115元</p></div></div>
<p style="font-size:28px;line-height:1.6;color:{M}">開辦170萬元＋週轉金30萬元，自有資金70%、金融機構貸款30%；每年自盈餘提撥營業額1%作為設備汰換準備金。契約期5年，自點交次日起算。</p>''',
 '財務採保守估算。第一年是導入期，只估穩定水準的八成，約損益兩平；第二、三年稅前淨利率約6.6%與8.1%。這些數字以來客數達到基本面為前提：每日平均要約207人次才能損益兩平。開辦資金200萬元，七成自有資金。契約規定的地價稅、房屋稅由廠商負擔，已列在表16「耗材及雜支」項目內，每年編列營業額2%，約17萬到20萬元。')

# 16 maintenance
content('manage','伍、履約管理','安全與維護，寫進每天的流程',
 '<div style="display:flex;gap:24px">'+card('設備維護','點交時建立財產及設備清冊並拍照；依表定頻率保養並登記建檔；POS、監視等聯網設備不使用中國品牌')+card('消防防災','設置防火管理人；吧台電熱、不用明火；每半年至少1次防災實地演練並邀請機關參與')+card('風險管理','遊客量、食安、古蹟損害、人力、財務、輿情六類風險，各有預防及因應措施；投保公共意外、火災及產品責任險')+'</div>',
 '我們把安全放在營運之前：不使用明火、不變更結構、每日巡檢，發生任何損害立即通報機關並負責修復。')

# 17 KPI
content('kpi','伍、履約承諾','以量化指標自我追蹤',
 table(['面向','績效指標','目標值'],[
  ['營業執行','每週營業日數／每日營業時數','6日／9小時'],
  ['遊客服務','遊客滿意度調查','85%以上'],
  ['文化推廣','文化沙龍及體驗活動','每年24場以上'],
  ['在地合作','合作之臺南在地品牌及創作者','每年10家以上'],
  ['行銷推廣','社群貼文','每週3則以上'],
  ['安全管理','防災實地演練','每半年1次以上'],
  ['機關考核','年度經營管理考核成績','85分以上（及格75分）'],
 ],[20,48,32],fs=28),
 '最後是我們的承諾，全部可量化、可查核。年度考核我們以85分為目標，高於75分的通過標準。')

# 17b review
content('review','伍、年度考核','對應文化局年度考核五大項目',
 table(['考核項目（權重）','本團隊做法'],[
  ['營運計畫執行（含財務）25%','依核定計畫營運；會計獨立、每月損益檢討、營運月報'],
  ['設備維修及環境清潔 25%','設備保養表定執行並建檔；每2小時巡檢公共區域'],
  ['歷史、文化及藝術教育推廣 25%','每年24場以上文化沙龍及體驗；茶款附故事卡'],
  ['與文化局配合度 15%','機關借用場地優先無償提供；宣傳事先報准；主持人親自出席考核'],
  ['顧客滿意度或投訴率 10%','每半年滿意度調查，目標85%以上；意見3日內回覆'],
 ],[36,64],fs=28)+f'<p style="font-size:28px;color:{M}">考核75分通過，本團隊以85分為目標；考核成績亦為後續擴充3年之參考依據。</p>',
 '文化局每年考核五個項目，我們把每一項都對應到具體做法。其中文化教育推廣占25%，所以我們把文化沙龍和故事卡當成日常營運的一部分，不是偶爾辦活動。考核成績也是後續擴充3年的依據，我們以85分為目標。')

# 18 closing
n=len(slides)+1
slides.append(('closing',f'''<section id="closing" data-transition="fade" style="background:{D};color:{L};font-family:{B};padding:128px 128px 160px;display:flex;flex-direction:column;justify-content:center;gap:48px">
<h1 style="font-family:{H};font-size:88px;font-weight:700;line-height:1.3;color:{L};width:1500px">讓赤崁樓的故事，<br>留在旅客手中的一杯茶裡</h1>
<p style="font-size:40px;color:{MD}">鑫和洋行　敬請指教</p>
{foot(n,'dark')}<aside>以上報告，謝謝各位委員，敬請指教。</aside></section>'''))

os.makedirs(R+'/slides',exist_ok=True)
for id,s in slides: open(f'{R}/slides/{id}.html','w').write(s)
deck={"v":4,"createdOnFiles":{"v":1,"at":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')},"lists":"css","title":"赤崁樓評選簡報","order":[i for i,_ in slides],
 "sections":{"s1":{"description":"開場與勘誤","start":"cover"},"s2":{"description":"團隊介紹與經營願景","start":"vision"},"s3":{"description":"整體營運與服務規劃","start":"product"},"s4":{"description":"行銷推廣","start":"season"},"s5":{"description":"權利金與財務","start":"royalty"},"s6":{"description":"履約管理與承諾","start":"manage"}},
 "faces":{"noto-serif-tc":{"family":"Noto Serif TC","href":"https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&display=swap"},"noto-sans-tc":{"family":"Noto Sans TC","href":"https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap"}},"designSystems":[]}
json.dump(deck,open(R+'/deck.json','w'),ensure_ascii=False,indent=1)
print(len(slides),[i for i,_ in slides])
