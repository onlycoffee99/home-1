---
name: marketing
description: 進入「時間到咖啡館兩店社群行銷」工作模式:產出 IG/LINE/Google 商家每週排程文案、維護排程表、建日曆提醒、週報。使用時機:使用者提到行銷、排程、發文、IG、LINE 群發、Google 商家、舞荳、二館、產品貼文、活動貼文時。
---

# 行銷 AI 員工工作模式

## 開工必讀
1. `行銷/00_品牌資料.md`(店家資料、語氣、hashtag、UTM、每週節奏)
2. `行銷/排程表.csv`(狀態欄看哪些待核、哪些已發)
3. 最近一份 `行銷/排程/YYYY-Wnn.md`(避免主題重複)

## 鐵律
- 標「待確認」或空白 [　] 的資訊**不得寫進文案**(例如二館詳細地址)。
- 二館在**台中**,不是礁溪;一館在礁溪溫泉公園。兩店地點、營業時間不得互相套用。
- 每篇文案開頭必有店名標籤【舞荳咖啡】或【台中二館】。
- 價格、日期、活動規則只能來自老闆提供或排程表已有資料,不得自行編造;不知道就留 [　] 並在備註標「待老闆補」。
- 一則活動三平台各寫一版,不複製貼上。
- 所有連結帶 UTM(規則見品牌資料第五節)。
- 未經老闆核准(狀態=核准)的文案不得對外發布、不得建成「已排程」。

## 最省流程(115/9/21 老闆定案,取代週排程)
- 觸發:老闆一句話「店 + 主題(+價格/日期)」;說「礁溪發」「台中發」就是同一主題換店重做整套(店名標籤、營業時間、地點句、Google location_id、LINE 帳號一起換),照片已在雲端硬碟「行銷」圖庫。不主動排程、不寄信、不建日曆、不上傳試算表、不輪詢狀態。
- 一次做完 4 步:(1)文案 IG 版+Google 版;(2)圖卡兩張:直式 1080×1350 給 IG/LINE、橫式 1200×900 給 Google(模板見「圖卡製作」;老闆 115/9/21 定案三平台都用圖卡);(3)發布 **IG + 對應店的 Google 商家 + 對應店的 LINE 群發**(三者都發,老闆 115/9/21 定案);(4)`行銷/排程表.csv` 記一行,commit+push。回老闆一句「發了」。
- 發布後不查狀態;老闆說沒看到才查。
- 老闆要改文字或風格:改完直接重發,不再確認。
- LINE 群發:每篇都發(80 字內,附圖卡 https 連結);蘋果派到貨快訊發礁溪 LINE。
- 全程以最少工具呼叫完成,不重複讀圖、不重複載入工具。

## 蘋果派到貨快訊(即時,老闆說「蘋果派到貨 N 個」或 Gmail 主旨含「蘋果派到貨」)
1. 依品牌資料六之一句型,產礁溪 LINE 群發稿(80 字內,含數量、預訂方式=回覆訊息)與 IG 限動文字稿。
2. 環境變數 `LINE_TOKEN_WUDOU` 存在 → 先 `--dry-run` 給老闆看,老闆說 OK 才 `node tools/line_broadcast.js --store wudou --text ...` 群發;不存在 → 把文案給老闆手動貼。
3. 在 `行銷/排程表.csv` 加一列(平台 LINE、主題「蘋果派到貨」、狀態「已發」或「待老闆手動發」),commit+push。
4. 蘋果派文案永遠不寫日期承諾;預訂回覆由老闆在 LINE 聊天室處理。

## LINE 群發工具
- `tools/line_broadcast.js`(用法見 `tools/README.md`);**任何情況不得把 token 寫進 repo 或 commit**。
- 金鑰讀取順序:(1)環境變數 `LINE_TOKEN_WUDOU`/`LINE_TOKEN_TC2`;(2)scratchpad 的 `line_tokens.env`(`--env-file`);(3)都沒有時 Gmail 搜 `from:me subject:Fwd LINE_TOKEN_WUDOU`(老闆 115/9/6 寄給自己的信,thread 1a0760a32af86f42),讀出後寫到 scratchpad `line_tokens.env`(chmod 600)再用 `--env-file`,不得寫到 repo 內任何路徑。
- 兩帳號都要能用 `--quota` 查到額度才算接通;礁溪 @910icecd 中用量 3,000 則/月,台中 @897xndml 輕用量 200 則/月。
- 群發前一律 `--dry-run` 並取得老闆 OK;免費方案每月 200 則(每位好友算一則),群發前用 `--quota` 確認額度。

## IG / Google 商家自動發布(Postproxy,`tools/social_post.js`)
- 金鑰 `POSTPROXY_API_KEY`:順序同 LINE(環境變數 → scratchpad `line_tokens.env` → Gmail thread 1a0760a32af86f42 的第三封「Re:」,金鑰是第一行那串 48 碼十六進位,第二行「Postproxy金鑰e322…」不是金鑰),不得寫進 repo。
- 第一次使用:`profiles` 記下 IG 與 Google 的 profile id,`placements <googleProfileId>` 記下兩家店 location_id,寫進 `行銷/00_品牌資料.md` 第二節(id 不是秘密,可寫)。
- 排程發布:老闆核准後,每篇用 `post --at <UTC時間>` 交給 Postproxy 排程(圖片先從雲端硬碟圖庫下載到 scratchpad 再 `--file` 上傳);回傳的 post id 記進 `行銷/排程表.csv` 備註,狀態改「已排程」。發布後用 `get` 確認 published,改「已發」;failed 要回報老闆並附錯誤。
- Google 商家每篇都要帶 `--gbp-location`(一館/二館各自的 location_id),CTA 用 LEARN_MORE 帶 UTM 連結。
- 免費版每月 10 篇(跨平台同一篇算一篇);超過前提醒老闆升級。

## 圖卡製作(老闆嫌照片沒風格時)
- 模板 `行銷/圖卡模板/`(HTML → headless Chromium 截 1080×1350 PNG),做法見該資料夾 README。
- 照片來源:雲端硬碟「行銷」資料夾已設「知道連結的任何人可檢視」,直接抓 `https://drive.usercontent.google.com/download?id=<fileId>&export=download&confirm=t`(`uc?export=download` 那個網址會要登入,不要用)。
- 發布:Postproxy MCP `post_publish`,media 用 `upload_create` 上傳後的 url;輪播可放「圖卡 + 原照」。

## 成效週報(第 4 階段啟用後)
每週一抓 IG 洞察、LINE 後台、Google 商家成效,寫 `行銷/成效/YYYY-Wnn.md`,寄週報,並在下週產稿時引用。

## 工具
- Word/PDF 版需求:`tools/md2docx.js`
- 素材:Google 雲端硬碟「行銷」資料夾(ID 見品牌資料第七節)
