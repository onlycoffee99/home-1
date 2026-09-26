from PIL import Image, ImageDraw, ImageFont
S=2; W,H=1040*S,510*S
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
fp='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; fr='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
F=lambda s,b=True: ImageFont.truetype(fp if b else fr, s*S, index=3)
def box(x,y,w,h,fill,text,tc='white',fs=20,bold=True,r=10):
    d.rounded_rectangle([x*S,y*S,(x+w)*S,(y+h)*S],radius=r*S,fill=fill)
    lines=text.split('\n'); f=F(fs,bold); lh=fs*1.45
    ty=y+h/2-lh*len(lines)/2-fs*0.15
    for i,l in enumerate(lines):
        tw=d.textlength(l,font=f)/S
        d.text(((x+w/2-tw/2)*S,(ty+i*lh)*S),l,font=f,fill=tc)
line=lambda x1,y1,x2,y2: d.line([x1*S,y1*S,x2*S,y2*S],fill=(160,160,160),width=3*S)
GRAY=(215,215,215)
box(410,20,220,36,(84,130,53),'計畫主持人',fs=19); box(410,56,220,58,GRAY,'鄭玉屏',tc='black',fs=24)
line(520,114,520,370)
line(520,250,640,250)
box(640,120,360,34,(230,170,0),'協力人員',fs=18)
box(640,154,360,196,GRAY,'蔡錦佳老師（印刷手作課程顧問）\n黃萩昌教授（鐵道文化史）\n徐鈺清（原生特色商品）\n○○○（文創選物）\n○○○（AI行銷）',tc='black',fs=17)
line(115,370,935,370)
cols=[(115,(47,84,150),'活動推廣組'),(385,(120,150,205),'行銷組'),(655,(68,114,196),'餐飲組'),(935,(18,160,180),'行政事務組')]
subs=['文化沙龍・講座\n市集・導覽串聯','社群・LINE・Google\n文宣・異業合作','茶飲・咖啡・輕食\n食品安全・備品','財務・採購・人事\n設備・消防・考核']
for (x,c,t),s in zip(cols,subs):
    line(x,370,x,400); box(x-100,400,200,46,c,t,fs=21)
    f=F(15,False)
    for i,l in enumerate(s.split('\n')):
        tw=d.textlength(l,font=f)/S; d.text(((x-tw/2)*S,(454+i*22)*S),l,font=f,fill=(60,60,60))
im.save('orgchart.png')
