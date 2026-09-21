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
