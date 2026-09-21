# IG 圖卡模板(1080×1350)

用 headless Chromium 把 HTML 渲染成 PNG,不需 PIL/ImageMagick。照片放同資料夾命名 `ube.jpg`(或改 HTML 內的檔名),文字直接改 HTML。

```bash
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=1080,1350 --screenshot=card.png "file://$PWD/card.html"
```

- 字型:容器內有「WenQuanYi Zen Hei」;品牌色 UBE 紫 `#3a2440`(可依主題換)。
- 上傳到 Postproxy:`upload_create` 取得 upload_url → `curl -F "file=@card.png;type=image/png" <upload_url>` → 回傳 url 放進 post 的 media。
- 版式:照片在上(700px,cover)、文字帶在下:標籤 / 品名 / 三點說明 / 店名+營業時間。

- `新品_橫式Google用.html`:1200×900,照片左、文字右;Google 商家版面用橫式。截圖指令改 `--window-size=1200,900`。
