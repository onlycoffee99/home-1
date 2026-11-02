#!/usr/bin/env python3
# 土地使用同意書(梅山段349,所有權人陳文政 → 政達木業有限公司二廠),供縣府水利事業建造物申請
import docx, sys
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
KAI='標楷體'
d=docx.Document(); s=d.sections[0]
s.page_height,s.page_width=Cm(29.7),Cm(21.0)
s.top_margin=s.bottom_margin=Cm(2.0); s.left_margin=s.right_margin=Cm(2.5)
def P(t,size=13,bold=False,align=None,before=0,after=4,line=22,indent=None):
    p=d.add_paragraph(); f=p.paragraph_format
    f.space_before,f.space_after,f.line_spacing=Pt(before),Pt(after),Pt(line)
    if align is not None: f.alignment=align
    if indent is not None: f.first_line_indent=Cm(indent)
    r=p.add_run(t); r.font.name=KAI; r.font.size=Pt(size); r.font.bold=bold
    r._element.rPr.rFonts.set(qn('w:eastAsia'),KAI); return p
P('土地使用同意書',22,True,WD_ALIGN_PARAGRAPH.CENTER,after=18)
P('本人陳文政為下列土地之所有權人,茲同意政達木業有限公司二廠(統一編號89497279)於本人所有之下列土地,施設跨越梅花排水之出入版橋(既設)及生活污水放流管線,並將生活污水排入宜蘭縣政府管理之區域排水「梅花排水」,作為申請宜蘭縣政府水利事業(跨越水道)建造物(縣管河川、區域排水及野溪搭排水專用)許可之用。',indent=1.0)
t=d.add_table(rows=1,cols=6); t.style='Table Grid'
hdr=['鄉鎮市','地段','小段','地號','面積(㎡)','權利範圍']
row=['冬山鄉','梅山段','－','349','2,602.16','全部']
for i,h in enumerate(hdr): t.rows[0].cells[i].text=h
c=t.add_row().cells
for i,v in enumerate(row): c[i].text=v
for r in t.rows:
    for cell in r.cells:
        for p in cell.paragraphs:
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name=KAI; run.font.size=Pt(13); run._element.rPr.rFonts.set(qn('w:eastAsia'),KAI)
P('',after=4)
for x in ['一、使用範圍:(一)廠區正門口既設版橋之橋臺銜接範圍;(二)放流管線自廠內化糞池、放流池經廠區正門口至梅山段329地號介入口之管線埋設範圍(詳申請書件設計圖說)。',
          '二、使用期間:自宜蘭縣政府核准之日起至中華民國119年12月31日止;期滿如經許可展延,同意期間隨同延長。',
          '三、本同意書僅供上開申請使用,不作其他用途。']:
    P(x,indent=None)
P('此致',before=12)
P('宜蘭縣政府')
for x in ['立同意書人(土地所有權人):陳文政　　　　　　(簽名蓋章)',
          '身分證統一編號:G120582948',
          '住址:宜蘭縣冬山鄉梅林路571之1號',
          '電話:0932-164882',
          '',
          '被同意人(申請人):政達木業有限公司二廠　　(蓋公司大小章)',
          '代表人:陳文政',
          '住址:宜蘭縣冬山鄉得安村梅林路571-1號']:
    P(x,before=2 if x else 0)
P('中　華　民　國　　　年　　　月　　　日',align=WD_ALIGN_PARAGRAPH.CENTER,before=14)
d.save(sys.argv[1]); print('OK')
