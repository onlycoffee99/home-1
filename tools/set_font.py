#!/usr/bin/env python3
# 把 docx 內所有文字改成指定字型(預設標楷體)。用法: python3 tools/set_font.py 檔.docx [字型]
import sys, docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
f = sys.argv[1]; font = sys.argv[2] if len(sys.argv) > 2 else '標楷體'
d = docx.Document(f)
def fix(rpr_parent):
    rPr = rpr_parent.get_or_add_rPr()
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rPr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rf.set(qn(a), font)
    for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
for r in d.element.body.iter(qn('w:r')):
    fix(r)
for st in d.styles:
    try:
        st.font.name = font; st.element.rPr.rFonts.set(qn('w:eastAsia'), font)
    except Exception: pass
for sec in d.sections:
    for part in (sec.header, sec.footer):
        for r in part._element.iter(qn('w:r')): fix(r)
d.save(f); print('font ->', font, f)
