---
name: ot-case
description: 進入「礁溪溫泉公園 OT 案(輕車悠遊 vs 宜蘭縣政府)」工作模式:接續公文撰擬、對照表與會議文件製作、進度追蹤。使用時機:使用者提到縣政府、縣府、輕車、OT案、履約會議、績效評估、票券、函稿、對照表、公文,或要求接續縣府案件工作時。
---

# 縣府 OT 案工作模式

## 開工順序

1. 讀 repo 根目錄 `CLAUDE.md`(案件全貌、鐵律、期限)與 `README.md`(進度總覽)。
2. 讀 `縣府案件/13_交件指引_送件順序與注意事項.md` 確認目前送件順位與現況。
3. 需要爭點攻防分析時讀 `縣府案件/10_爭點對照表_會議討論用.md`;需要查證背景時讀 `縣府案件/00_總說明_必讀.md`。

## 產出規則

- 公文/函稿一律先寫 md(放 `縣府案件/`,檔名沿用現有編號體例),再轉 Word 給使用者:

```bash
cd /tmp/claude-0/*/*/scratchpad 2>/dev/null || SCRATCH=$(mktemp -d) && cd $SCRATCH
npm init -y >/dev/null 2>&1 && npm install docx marked --no-audit --no-fund >/dev/null 2>&1
node <repo>/tools/md2docx.js <輸入.md> <輸出.docx>
```

- 產出 Word 後用 SendUserFile 傳給使用者(display: attach)。
- 每次有收發文動作,回填 `縣府案件/收發文登記簿.csv`。
- 完成即 commit + push 到 `claude/desktop-crash-issue-axgd3x` 分支。

## 文書鐵律(違反=重寫)

- 遵守 `CLAUDE.md` 第三節全部 8 條,特別是「六句話不能說」。
- 函稿【製作說明】段落僅供內部,標明「發文前刪除」。
- 空白欄位【　】未填不得標示為可發文。
- 狀態標示誠實:佐證未補=「另補送+時程」,不得寫「已補充」。

## 常用查證來源

- Google 雲端硬碟(檔案 ID 見 CLAUDE.md 第四節)
- Gmail:LINE發票、[鑫和] 提醒、iCHEF 關帳、縣府/銀行通知
- 桌機路徑對照見 `縣府案件/13_交件指引` 陸節
