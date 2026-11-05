#!/usr/bin/env python3
# 圖七 既設版橋平面圖・縱剖面圖(政達二廠,跨越梅花排水,梅山段329)
# 尺寸:渠寬約3.83 m(圖四)、版橋長約4 m(業主告知);寬度、厚度、高程依實測填寫
F = "'Microsoft JhengHei','微軟正黑體','PMingLiU',sans-serif"
o = []
def T(x, y, s, size=12, fill='#222', anchor='start', bold=False):
    w = ' font-weight="700"' if bold else ''
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{s}</text>')
def R(x, y, w, h, fill='none', stroke='#333', sw=1, rx=0, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"{d}/>')
def L(x1, y1, x2, y2, stroke='#333', sw=1, dash=None, m=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')
def P(pts, fill='none', stroke='#333', sw=1, op=1):
    o.append(f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
def dim(x1, y1, x2, y2, label, side=-8, color='#c62828', vertical=False):
    L(x1, y1, x2, y2, color, 1.2, m=' marker-start="url(#a2)" marker-end="url(#a2)"')
    if vertical:
        T(x1 + 8, (y1 + y2) / 2 + 4, label, 12, color)
    else:
        T((x1 + x2) / 2, y1 + side, label, 12, color, 'middle')

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="1123" height="794" viewBox="0 0 1123 794"><defs>'
         '<marker id="a2" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="#c62828"/></marker>'
         '<marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#1565c0"/></marker>'
         '<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#c9a227" stroke-width="2"/></pattern>'
         '<pattern id="conc" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.9" fill="#777"/></pattern>'
         '</defs>')
R(0, 0, 1123, 794, '#fff', 'none')
R(14, 14, 1095, 766, 'none', '#111', 1.5)
T(46, 44, '圖七　既設版橋平面圖・縱剖面圖', 17, '#111', bold=True)

# ---------- (一)平面圖 ----------
T(56, 80, '(一)平面圖', 14, '#111', bold=True)
X0, X1 = 70, 690
R(X0 - 10, 90, X1 - X0 + 20, 300, 'none', '#888')
# 328 農路
R(X0, 100, X1 - X0, 70, '#eceff1', '#90a4ae')
T(X0 + 10, 125, '梅山段 328(交通用地・農路)　寬約 4.65 m', 13, '#37474f', bold=True)
T(X0 + 10, 145, '公共通行道路', 11, '#607d8b')
# 329 渠道
R(X0, 170, X1 - X0, 80, '#d6ecfa', '#1565c0', 1.2)
L(X0 + 20, 228, X1 - 30, 228, '#1565c0', 3, m=' marker-end="url(#fl)"')
T(X0 + 10, 190, '梅山段 329(水利用地)', 13, '#0d47a1', bold=True)
T(X0 + 10, 207, '梅花排水(梅花大排)渠道', 12, '#0d47a1')
T(X1 - 40, 245, '流向下游', 11, '#1565c0', 'end')
# 349 廠區
R(X0, 250, X1 - X0, 130, 'url(#hatch)', '#b8860b', 1.2, op=0.35)
T(X0 + 10, 360, '梅山段 349　政達木業有限公司二廠(廠區)', 13, '#6d4c00', bold=True)
# 版橋 (spans 165..255 => 渠寬80px=3.83m, 版橋長 ~4.0m => ~90px)
BX, BW = 330, 110
R(BX, 165, BW, 90, 'url(#conc)', '#333', 2)
R(BX, 165, BW, 90, '#bdbdbd', '#333', 2, op=0.55)
T(BX + BW / 2, 205, '既設版橋', 14, '#111', 'middle', True)
T(BX + BW / 2, 223, '(鋼筋混凝土版)', 11, '#333', 'middle')
# 橋臺
R(BX, 160, BW, 10, '#757575', '#333', 1)
R(BX, 250, BW, 10, '#757575', '#333', 1)
T(BX + BW + 6, 160, '橋臺(渠岸外側)', 10.5, '#424242')
T(BX + BW + 6, 262, '橋臺(渠岸外側)', 10.5, '#424242')
# 正門口
R(BX + 10, 262, BW - 20, 16, '#5d4037', '#3e2723', 1)
T(BX + BW / 2, 274, '廠區正門口', 10.5, '#fff', 'middle')
# 尺寸
dim(BX - 22, 165, BX - 22, 255, '長約 4.0 m', vertical=True)
L(BX - 30, 165, BX, 165, '#c62828', 0.6, '3,2'); L(BX - 30, 255, BX, 255, '#c62828', 0.6, '3,2')
o[-3] = o[-3].replace(f'x="{BX - 22 + 8}"', f'x="{BX - 100}"')
dim(BX, 152, BX + BW, 152, '寬【實測】m', side=-6)
# 渠寬
dim(X1 - 15, 170, X1 - 15, 250, '', vertical=True)
T(X1 - 20, 200, '渠寬約 3.83 m', 11, '#c62828', 'end')
# 介入口(錯開版橋)
IX = 520
L(IX, 300, IX, 246, '#c62828', 2.5, '6,3')
o.append(f'<circle cx="{IX}" cy="244" r="6" fill="#c62828" stroke="#fff" stroke-width="1.5"/>')
o.append(f'<circle cx="{IX}" cy="305" r="5" fill="#e65100"/>')
T(IX + 10, 312, '放流池', 10.5, '#e65100')
T(IX + 10, 284, '放流管', 10.5, '#c62828')
T(IX + 10, 266, '介入口(與版橋錯開)', 11, '#c62828')
dim(BX + BW, 296, IX, 296, '間距【實測】', side=14)
T(X0, 384, '※ 平面示意(比例約略);版橋寬度、厚度、介入口與版橋間距依現地實測填寫。', 10.5, '#666')

# ---------- (二)縱剖面圖(垂直渠道方向,沿版橋中心線) ----------
T(56, 420, '(二)縱剖面圖(沿版橋中心線,垂直渠道方向)', 14, '#111', bold=True)
R(60, 430, 630, 290, 'none', '#888')
GY = 520  # 地面
# 地面線
L(80, GY, 255, GY, '#5d4037', 2); L(505, GY, 670, GY, '#5d4037', 2)
T(90, GY + 20, '梅山段 328 農路側', 11, '#37474f')
T(580, GY + 20, '梅山段 349 廠區側', 11, '#6d4c00')
# 渠道斷面(梯形)
P(f'255,{GY} 505,{GY} 470,{GY+130} 290,{GY+130}', '#ffffff', '#555', 1.5)
P(f'268,{GY+60} 492,{GY+60} 470,{GY+130} 290,{GY+130}', '#bbdefb', '#1565c0', 1, 0.9)
L(268, GY + 60, 492, GY + 60, '#1565c0', 1, '5,3')
T(380, GY + 55, '常水位', 11, '#1565c0', 'middle')
T(380, GY + 112, '梅花排水(梅花大排)　通水斷面不縮減', 12, '#0d47a1', 'middle', True)
# 橋臺
R(205, GY - 4, 50, 40, 'url(#conc)', '#333', 1.5); R(205, GY - 4, 50, 40, '#9e9e9e', '#333', 1.5, op=0.5)
R(505, GY - 4, 50, 40, 'url(#conc)', '#333', 1.5); R(505, GY - 4, 50, 40, '#9e9e9e', '#333', 1.5, op=0.5)
T(230, GY + 52, '橋臺', 11, '#333', 'middle'); T(530, GY + 52, '橋臺', 11, '#333', 'middle')
# 版橋版
R(205, GY - 22, 350, 18, 'url(#conc)', '#111', 2); R(205, GY - 22, 350, 18, '#bdbdbd', '#111', 2, op=0.5)
T(380, GY - 28, '既設鋼筋混凝土版橋', 12, '#111', 'middle', True)
# 尺寸
dim(205, GY - 60, 555, GY - 60, '版橋長約 4.0 m(含兩端橋臺搭接)', side=-6)
dim(255, GY + 160, 505, GY + 160, '渠寬(渠頂)約 3.83 m', side=16)
L(255, GY, 255, GY + 165, '#c62828', 0.6, '3,2'); L(505, GY, 505, GY + 165, '#c62828', 0.6, '3,2')
dim(575, GY - 22, 575, GY - 4, '', vertical=True)
T(582, GY - 8, '版厚【實測】', 10.5, '#c62828')
T(260, GY + 22, '版底不低於渠岸頂', 10.5, '#c62828')
T(80, 712, '※ 示意圖(尺寸待實測);渠道內不設橋墩,橋臺設於渠岸外側。', 10.5, '#666')

# ---------- 右側:規格表 ----------
RX = 715
R(RX, 70, 380, 300, '#fafafa', '#333', 1.2, 6)
T(RX + 12, 94, '既設版橋規格(現況)', 14, '#111', bold=True)
rows = [('位　　置', '廠區正門口,梅山段329地號'), ('跨越水路', '梅花排水(宜蘭縣管區域排水)'),
        ('連　　接', '梅山段328農路 ↔ 349廠區'), ('現　　況', '已施設完成(補辦申請)'),
        ('型　　式', '鋼筋混凝土版橋【確認】'), ('長　　度', '約 4.0 m(渠寬約 3.83 m)'),
        ('寬　　度', '【實測】m'), ('版　　厚', '【實測】cm'), ('橋臺位置', '渠岸外側,渠內無橋墩'),
        ('用　　途', '廠區人員及車輛出入通行'), ('數　　量', '一處一座'), ('施設年份', '【待補】')]
y = 118
for k, v in rows:
    T(RX + 16, y, k, 12, '#455a64'); T(RX + 110, y, v, 12, '#111')
    L(RX + 12, y + 7, RX + 368, y + 7, '#e0e0e0', 0.8)
    y += 20.5

R(RX, 380, 380, 230, '#fff5f5', '#c62828', 1.2, 6)
T(RX + 12, 404, '設置原則與承諾事項', 14, '#c62828', bold=True)
rules = ['1. 版橋長度約 4 m,在 6 m 以內,一處一座。',
         '2. 渠道內不設橋墩,橋臺設於渠岸外側,',
         '　 不縮減梅花排水通水斷面。',
         '3. 版底不低於渠岸頂,不妨礙排水及渠道維護。',
         '4. 放流管介入口與版橋錯開,不設於橋下。',
         '5. 每年防汛期前及颱風警報前清除橋下淤積、',
         '　 漂流物;災後檢查橋面與橋臺並報府。',
         '6. 維護管理由申請人負責;主管機關認有妨礙',
         '　 河防或通水時,依指示改善或自費拆除。']
y = 428
for r in rules:
    T(RX + 16, y, r, 11.5, '#333'); y += 19.5

# 圖例/註
T(RX, 630, '依據:宜蘭縣政府水利事業(跨越水道)建造物申辦規定;', 10.5, '#555')
T(RX, 646, '農業部農田水利署宜蘭管理處版橋規定(長度 6 m 以內、一處一座)。', 10.5, '#555')
# 標題欄
R(785, 690, 324, 90, '#fff', '#111', 1.2)
T(797, 712, '圖七　既設版橋平面圖・縱剖面圖', 16, '#111', bold=True)
T(797, 732, '跨越梅花排水(梅山段329地號)', 12, '#444')
L(793, 740, 1101, 740, '#999', 0.8)
T(797, 757, '案名:政達木業有限公司二廠既設版橋及生活污水搭排', 11, '#333')
T(797, 772, '示意圖(尺寸待實測)　｜　第 7 張,共 7 張', 10.5, '#333')
o.append('</svg>')
open('圖七_既設版橋平面剖面圖.svg', 'w', encoding='utf-8').write('\n'.join(o))
print('OK')
