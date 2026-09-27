/**
 * 森林風呂御神籤:Google Apps Script 後端
 * 放在「森林風呂御神籤_回覆」試算表的 擴充功能 → Apps Script 裡。
 * 網頁(Index.html)答完後呼叫 submit(),寫一列到「回覆」工作表並回傳券號。
 */

var SHEET_NAME = '回覆';

// 欄位順序固定;id 須與 Index.html 題庫一致
var COLUMNS = [
  ['time', '填答時間'],
  ['coupon', '券號'],
  ['luck', '籤'],
  ['age', '年齡'],
  ['freq', '來訪頻率'],
  ['q01', '1 公園風景'],
  ['q02', '2 公園走道草地清潔'],
  ['q03', '3 公園廁所(含泡腳池旁)'],
  ['q04', '4 泡腳池清潔'],
  ['q05', '5 人員主動協助'],
  ['q06', '6 垃圾分類回收'],
  ['q07', '7 防蚊蟲'],
  ['q08', '8 溫泉水質'],
  ['q09', '9 湯區清潔'],
  ['q10', '10 風呂廁所'],
  ['q11', '11 櫃台人員態度'],
  ['q12', '12 櫃台等候時間'],
  ['q13', '13 園區店家服務'],
  ['q14', '14 停車方便'],
  ['q15', '15 停車場好找'],
  ['q16', '16 推薦意願'],
  ['q17', '17 對宜蘭觀光的貢獻'],
  ['q18', '18 宜蘭觀光形象'],
  ['q19', '19 在地特色'],
  ['q20', '20 活動佈置認識宜蘭'],
  ['q21', '21 觀光資訊提供'],
  ['q22', '22 公益活動/按摩小站'],
  ['q23', '23 在地免費泡湯回饋'],
  ['q24', '24 佛光大學創生商品'],
  ['f1', '趣味:泡湯時在想什麼'],
  ['f2', '趣味:最想來一杯'],
  ['f3', '趣味:森林風呂是什麼動物'],
  ['message', '想說的話'],
  ['asked', '本次抽到的題目']
];

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('森林風呂御神籤')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
  }
  if (sh.getLastRow() === 0) {
    sh.appendRow(COLUMNS.map(function (c) { return c[1]; }));
    sh.setFrozenRows(1);
  }
  return sh;
}

function submit(payload) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = getSheet_();
    var n = sh.getLastRow(); // 標題列佔 1 列,故第 n 份 = 第 n+1 列
    var coupon = ('0000' + n).slice(-4);
    var a = (payload && payload.answers) || {};
    // 截長度;開頭是 = + - @ 的文字前面加 ' ,避免被試算表當成公式
    var clip = function (s, len) {
      s = String(s == null ? '' : s).slice(0, len);
      return /^[=+\-@]/.test(s) ? "'" + s : s;
    };

    var row = COLUMNS.map(function (c) {
      var k = c[0];
      if (k === 'time') return new Date();
      if (k === 'coupon') return 'No.' + coupon;
      if (k === 'luck') return clip(payload.luck, 10);
      if (k === 'message') return clip(payload.message, 300);
      if (k === 'asked') return clip(payload.asked, 200);
      return clip(a[k], 40);
    });
    sh.appendRow(row);
    return coupon;
  } finally {
    lock.releaseLock();
  }
}
