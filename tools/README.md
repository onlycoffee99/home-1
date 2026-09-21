# tools

## md2docx.js

將 Markdown(含表格、粗體、引用)轉為中文排版 Word 檔。

```bash
npm install docx marked   # 在任意暫存目錄安裝一次
node tools/md2docx.js 輸入.md 輸出.docx
```

- 預設 A4、微軟正黑體、表格自動配欄寬
- YAML front matter 會自動去除
