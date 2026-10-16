# Pinkoi 館:舞荳 Wudou|時間到咖啡館 Time Coffee

- `上架稿.md`:館介紹+各商品逐欄文字([　]待老闆補,補齊才上架)
- `主圖模板.html`:1200×1200 主圖。商品照片放同資料夾命名 `photo.jpg`,改品名/副標後出圖:

```bash
chrome=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
$chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=1200,1400 --screenshot=out.png "file://$PWD/主圖模板.html"
python3 -c "from PIL import Image;Image.open('out.png').crop((0,0,1200,1200)).save('out.png')"
```
(headless 視窗會吃掉約 90px,所以開 1400 高再裁成 1200。)
