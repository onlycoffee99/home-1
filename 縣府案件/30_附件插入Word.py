# 文30 附件1~3 插入 Word:先跑 tools/qc_letter.py 產函稿,再跑本檔
import sys, glob
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
p, A = sys.argv[1], sys.argv[2]
d = Document(p)
def t(s, sz, b=False):
    para = d.add_paragraph(); r = para.add_run(s); r.font.size = Pt(sz); r.font.bold = b
    r.font.name = '標楷體'; r._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
def brk(): d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
def img(f, h):
    para = d.add_paragraph(); para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run().add_picture(f, height=Cm(h))
brk(); t('附件1　法務部行政執行署宜蘭分署執行扣押繳款證明影本', 16, True)
t('【待補：宜執和115罰00225189字第1150220203A號執行命令及扣款證明】', 12)
brk(); t('附件2　礁溪溫泉公園18巷停車場登記證影本（府交停字第1150141230號）', 16, True)
img(f'{A}/停車場登記證_府交停字第1150141230號.jpg', 21)
pages = sorted(glob.glob(f'{A}/充電站合作協議書_華城電能-*.jpg'))
for i, f in enumerate(pages):
    brk()
    if i == 0: t('附件3　「宜蘭縣政府停車場電動汽車充電站建置營運」合作協議書影本', 14, True)
    img(f, 22 if i else 21)
d.save(p)
