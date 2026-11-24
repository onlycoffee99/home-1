# 文39 附件插入 Word:先跑 tools/qc_letter.py 產函稿,再跑本檔
import sys
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
p, A = sys.argv[1], sys.argv[2]
d = Document(p)
def t(s, sz, b=False):
    para = d.add_paragraph(); r = para.add_run(s); r.font.size = Pt(sz); r.font.bold = b
    r.font.name = '標楷體'; r._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
t('附件　宜蘭縣政府衛生局水質檢體抽驗送驗單及採樣照片（115年11月24日）', 14, True)
for f, h in [('衛生局水質檢體抽驗送驗單_1151124.jpg', 11.5), ('衛生局採樣檢體_1151124.jpg', 12)]:
    para = d.add_paragraph(); para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run().add_picture(f'{A}/{f}', height=Cm(h))
d.save(p)
