# tools

## md2docx.js

將 Markdown(含表格、粗體、引用)轉為中文排版 Word 檔。

```bash
npm install docx marked   # 在任意暫存目錄安裝一次
node tools/md2docx.js 輸入.md 輸出.docx
```

- 預設 A4、微軟正黑體、表格自動配欄寬
- YAML front matter 會自動去除

## line_broadcast.js

LINE 官方帳號群發(Messaging API),兩店各自一組金鑰。金鑰放環境變數 `LINE_TOKEN_WUDOU`(礁溪一館)、`LINE_TOKEN_TC2`(台中二館),**不得寫進 repo**。

```bash
node tools/line_broadcast.js --store wudou --text "【舞荳咖啡】..." --dry-run   # 先看內容
node tools/line_broadcast.js --store wudou --text "【舞荳咖啡】..." --image https://.../a.jpg
node tools/line_broadcast.js --store tc2 --text "..." --to <userId>          # 只推給一個人測試
node tools/line_broadcast.js --store wudou --quota                            # 查本月額度/已用量
node tools/line_broadcast.js --env-file /path/line_tokens.env --store wudou --quota   # 金鑰從 repo 外的檔讀
```

## social_post.js(Postproxy 代發:IG + Google 商家檔案)

金鑰放環境變數 `POSTPROXY_API_KEY` 或 `--env-file`,**不得寫進 repo**。

```bash
node tools/social_post.js profiles                                  # 已連接帳號
node tools/social_post.js placements <googleProfileId>              # 兩家店的 location_id
node tools/social_post.js post --profiles <igProfileId> --text "【舞荳咖啡】..." --file 圖.jpg --at 2026-09-09T03:00:00Z --ig-format post
node tools/social_post.js post --profiles <gbpProfileId> --text "..." --file 圖.jpg --gbp-location accounts/…/locations/… --cta LEARN_MORE --cta-url https://…
node tools/social_post.js get <postId>                              # 查每平台 published/failed
```
時間用 UTC(台灣時間減 8 小時)。IG 圖 JPG/PNG ≤8MB;Google 商家圖 ≤5MB、不支援影片、文字 ≤1,500 字。

## survey_report.py(森林風呂御神籤問卷統計報告)

只用 Python 標準函式庫。匯出金鑰在雲端硬碟「森林風呂御神籤」資料夾,**不得寫進 repo**。

```bash
python3 tools/survey_report.py --url <網頁網址> --key <金鑰> --month 2026-10 --out 報告.md
python3 tools/survey_report.py --url <網頁網址> --key <金鑰> --from 2026-10-01 --to 2026-12-31 --out 報告.md --save-json raw.json
python3 tools/survey_report.py --json raw.json --month 2026-11 --out 報告.md   # 用已下載的資料
```
- 各題:有效份數、五級分布、滿意率、平均分數(5 分制)、不適用份數;未達 30 份標「樣本少」
- 另含重點摘要、推薦意願、年齡/來訪頻率、月別趨勢(跨月時)、趣味題、留言原文
- 留言含「Claude 測試」的列自動排除(`--exclude` 可改)

## make_qr.py / html2pdf.js(印刷品:QR 立牌、贈品券)

```bash
pip install qrcode                                   # 一次
python3 tools/make_qr.py <網址> qr.svg               # 產 QR SVG,貼進立牌 HTML
node tools/html2pdf.js 立牌.html 立牌.pdf 預覽.png   # 依 CSS @page 紙張大小輸出 PDF + 預覽圖
node tools/html2print300.js 券.html 券_300dpi        # 印刷店指定 300 dpi 點陣圖時:產出 券_300dpi.png + 券_300dpi.pdf
```
- 範本:`輕車鑫和合作案/森林風呂御神籤/立牌_A5.html`、`咖啡券_A4十張.html`
- 印之前用預覽圖解碼確認網址:`pip install opencv-python-headless` 後 `python3 -c "import cv2;print(cv2.QRCodeDetector().detectAndDecode(cv2.imread('預覽.png'))[0])"`
