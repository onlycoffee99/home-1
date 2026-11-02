# 文24 附件1~3 插入 Word:python3 縣府案件/24_附件插入Word.py 縣府案件/24_湯圍溝票券差別處理請釋明_函稿.docx 縣府案件/附件/24_湯圍溝票券
# (先跑 tools/qc_letter.py 產函稿,再跑本檔附加附件頁)
import sys
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
src,A=sys.argv[1],sys.argv[2]
doc=Document(src)
def p(text,size=12,bold=False,center=False):
    para=doc.add_paragraph(); r=para.add_run(text); r.font.size=Pt(size); r.font.bold=bold
    r.font.name='標楷體'; r._element.rPr.rFonts.set(qn('w:eastAsia'),'標楷體')
    para.paragraph_format.space_after=Pt(4)
    if center: para.alignment=WD_ALIGN_PARAGRAPH.CENTER
    return para
def img(path,h=None,w=None,cap=None):
    para=doc.add_paragraph(); para.alignment=WD_ALIGN_PARAGRAPH.CENTER
    para.add_run().add_picture(path,height=Cm(h) if h else None,width=Cm(w) if w else None)
    if cap: p(cap,10,center=True)
def brk():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
pages=[
 ("附件1　湯圍溝溫泉公園優待票（60元）影像",
  "票券名稱「湯圍溝公園溫泉泡湯券」，優待票每張60元，票號058602、058610，加蓋泡湯專用章。背面加蓋：「本泡湯優待券，適用於一次購買30人以上（亦即30張）之個人及團體使用，每張為60元……湯圍溝溫泉公園　TEL:03-9874882　有效日期102.12.31」。",
  [("a1_front.jpg",6.2,None,"正面（票號058602，收執聯）"),("a1_front_strip.jpg",5.2,None,"正面（票號058610，存根聯及收執聯）"),("a1_back.jpg",6.2,None,"背面加蓋使用規範及有效日期「102.12.31」")]),
 ("附件2　湯圍溝溫泉公園全票（80元）影像及105年1月29日收據",
  "全票每張80元，票號033431，加蓋泡湯專用章及有效日期「105.10.31」。收據載明：「前收到湯圍溝公園『湯圍風呂』泡湯券5000張（編號030001-035000）計50本及漁寶食品行發票（二聯式編號AZ05705726）乙張」，日期中華民國105年1月29日。",
  [("a2_ticket.jpg",8.5,None,"全票80元（票號033431），有效日期105.10.31"),("a2_receipt.jpg",10.5,None,"105年1月29日收據")]),
]
for t,d,ims in pages:
    brk(); p(t,16,True); p(d,11.5)
    for f,h,w,c in ims: img(f"{A}/{f}",h,w,c)
brk(); p("附件3　105年間臉書貼文截圖（池騰聯君帳號）",16,True)
p("貼文一載明：「該三種票卷皆為輕車悠遊公司私印或授權他人印製之票卷。本府一旦接管該公園後，一律不受理……」。貼文二標明「宜蘭縣府工旅處說明如下」，載明本公司「私自印製不法票券」，並載明票券碼033431及034638「為105年01月29日縣府舉辦『105年春節期間鼓勵民眾搭乘大眾運輸工具－幸福宜蘭福袋製作』活動，破例賣給縣府之5000張泡湯券（票券碼030001-035000）隨福袋送給民眾」。",11.5)
para=doc.add_paragraph(); para.alignment=WD_ALIGN_PARAGRAPH.CENTER
for f in ["a3_12.jpg","a3_8.jpg","a3_9.jpg"]:
    para.add_run().add_picture(f"{A}/{f}",height=Cm(9.6)); para.add_run(" ")
p("左：貼文一　中：貼文二（上）　右：貼文二（下）",10,center=True)
doc.save(src)
