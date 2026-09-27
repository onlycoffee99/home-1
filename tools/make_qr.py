#!/usr/bin/env python3
"""網址 → QR code SVG(可直接嵌進 HTML 立牌),並以 OpenCV 解碼驗證(有裝才驗)。
用法:python3 tools/make_qr.py <網址> <輸出.svg>
需要:pip install qrcode(驗證另需 opencv-python-headless)"""
import re, sys
import qrcode, qrcode.image.svg

url, out = sys.argv[1], sys.argv[2]
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=1,
                  image_factory=qrcode.image.svg.SvgPathImage)
q.add_data(url)
q.make(fit=True)
q.make_image().save(out)
svg = open(out, encoding="utf-8").read()
svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
svg = re.sub(r'width="[\d.]+mm" height="[\d.]+mm"', 'width="100%" height="100%" shape-rendering="crispEdges"', svg, 1)
svg = svg.replace("<path ", '<path fill="#2b2a26" ', 1)
open(out, "w", encoding="utf-8").write(svg)
print(f"已產出 {out}(QR version {q.version})")
