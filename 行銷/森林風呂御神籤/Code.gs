/**
 * 森林風呂御神籤:Google Apps Script 後端
 * 可放在試算表的 擴充功能 → Apps Script,或 script.google.com 新專案(兩種都可以)。
 * 網頁(Index.html)答完後呼叫 submit(),寫一列到「回覆」工作表並回傳券號。
 * 匯出(給 Claude 做評估報告):網址後加 ?export=<金鑰>,回傳全部回覆 JSON。
 *   金鑰放在「專案設定 → 指令碼屬性」EXPORT_KEY,不寫進程式碼;未設定則不開放匯出。
 * 店員兌換頁:網址後加 ?staff=1,輸入店員密碼(指令碼屬性 STAFF_PIN)後可核銷券號。
 */

var SHEET_NAME = '回覆';
// 每日咖啡券上限(台灣時間 0 點重算);0 = 不限量。額滿後仍可填答、抽籤,只是不發券號
var DAILY_LIMIT = 100;
// 券號有效天數(從抽中當天起算)
var VALID_DAYS = 30;
// 「今日無抽中」:每人約 NOWIN_RATE 機率沒抽中,每天最多 NOWIN_PER_DAY 人(由後端決定,客人無法自選)
var NOWIN_PER_DAY = 5;
var NOWIN_RATE = 0.09;
// 「森林風呂御神籤_回覆」試算表 ID(雲端硬碟「森林風呂御神籤」資料夾內)
var SPREADSHEET_ID = '1K22clZvbwZXTtxSCUmUTx1svKZBpdLILlm6Q7w6yC88';

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
  ['asked', '本次抽到的題目'],
  // 115/9/27 改 10 題版新增(接在最後,舊資料欄位不動)
  ['q00', '0 整體滿意度'],
  ['v1', '客源地'],
  ['v2', '宜蘭住宿晚數'],
  ['v3', '同行對象'],
  ['v4', '資訊來源'],
  ['v5', '宜蘭其他行程'],
  // 115/9/27 新增:選填 email(個資,匯出時排除)
  ['email', 'Email(選填,同意收優惠)'],
  // 115/9/28 新增:咖啡館核銷時間(空白=尚未兌換)
  ['redeemed', '兌換時間']
];
// 含個資的欄位:只留在試算表,?export 匯出時不提供
var PRIVATE_COLUMNS = ['email'];

function doGet(e) {
  var key = PropertiesService.getScriptProperties().getProperty('EXPORT_KEY');
  if (e && e.parameter && e.parameter.export) {
    if (!key || e.parameter.export !== key) {
      return ContentService.createTextOutput('{"error":"forbidden"}').setMimeType(ContentService.MimeType.JSON);
    }
    var values = getSheet_().getDataRange().getDisplayValues();
    var keep = [];
    COLUMNS.forEach(function (c, i) { if (PRIVATE_COLUMNS.indexOf(c[0]) < 0) keep.push(i); });
    var cols = keep.map(function (i) { return COLUMNS[i]; });
    var rows = values.slice(1).map(function (r) { return keep.map(function (i) { return r[i] === undefined ? '' : r[i]; }); });
    return ContentService.createTextOutput(JSON.stringify({ columns: cols, rows: rows }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  if (e && e.parameter && e.parameter.staff) {
    return HtmlService.createHtmlOutput(STAFF_HTML)
      .setTitle('咖啡券兌換(店員用)')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1');
  }
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('森林風呂御神籤')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getSheet_() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
  }
  var header = COLUMNS.map(function (c) { return c[1]; });
  if (sh.getLastRow() === 0) {
    sh.appendRow(header);
    sh.setFrozenRows(1);
  } else if (sh.getLastColumn() < header.length) {
    // 新增欄位時補齊標題列(新欄位一律接在最後,既有資料不受影響)
    sh.getRange(1, 1, 1, header.length).setValues([header]);
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
    // 數今天已發出的券、已「未抽中」的人數
    var issued = 0, nowinToday = 0, nowin = false;
    if (n > 1) {
      var today = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd');
      var tc = sh.getRange(2, 1, n - 1, 2).getDisplayValues(); // A 填答時間、B 券號
      tc.forEach(function (r) {
        if (r[0].indexOf(today) !== 0) return;
        if (r[1].indexOf('No.') === 0) issued++;
        else if (r[1] === '未抽中') nowinToday++;
      });
    }
    if (DAILY_LIMIT > 0 && issued >= DAILY_LIMIT) {
      coupon = '';                                   // 今日券已送完
    } else if (nowinToday < NOWIN_PER_DAY && Math.random() < NOWIN_RATE) {
      coupon = ''; nowin = true;                     // 今日無抽中
    }
    var a = (payload && payload.answers) || {};
    // 截長度;開頭是 = + - @ 的文字前面加 ' ,避免被試算表當成公式
    var clip = function (s, len) {
      s = String(s == null ? '' : s).slice(0, len);
      return /^[=+\-@]/.test(s) ? "'" + s : s;
    };

    var row = COLUMNS.map(function (c) {
      var k = c[0];
      if (k === 'time') return Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
      if (k === 'coupon') return coupon ? 'No.' + coupon : (nowin ? '未抽中' : '今日額滿');
      if (k === 'luck') return nowin ? '今日無抽中' : clip(payload.luck, 10);
      if (k === 'message') return clip(payload.message, 300);
      if (k === 'asked') return clip(payload.asked, 200);
      if (k === 'email') {
        var m = String(payload.email || '').trim().slice(0, 100);
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(m) ? clip(m, 100) : '';
      }
      return clip(a[k], 40);
    });
    sh.appendRow(row);
    return { coupon: coupon, nowin: nowin };
  } finally {
    lock.releaseLock();
  }
}

// ===================== 店員兌換(時間到咖啡館) =====================

function checkPin_(pin) {
  var p = PropertiesService.getScriptProperties().getProperty('STAFF_PIN');
  if (!p) throw new Error('尚未設定店員密碼(指令碼屬性 STAFF_PIN)');
  if (String(pin) !== p) throw new Error('店員密碼錯誤');
}

function colIndex_(id) {
  for (var i = 0; i < COLUMNS.length; i++) if (COLUMNS[i][0] === id) return i + 1;
  return -1;
}

function staffStats_(sh) {
  var n = sh.getLastRow();
  var today = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd');
  var st = { issuedToday: 0, redeemedToday: 0, issuedAll: 0, redeemedAll: 0 };
  if (n < 2) return st;
  var rc = colIndex_('redeemed');
  var vals = sh.getRange(2, 1, n - 1, rc).getDisplayValues();
  vals.forEach(function (r) {
    if (r[1].indexOf('No.') !== 0) return;
    st.issuedAll++;
    if (r[0].indexOf(today) === 0) st.issuedToday++;
    var red = r[rc - 1];
    if (red) { st.redeemedAll++; if (red.indexOf(today) === 0) st.redeemedToday++; }
  });
  return st;
}

function staffStats(pin) {
  checkPin_(pin);
  return staffStats_(getSheet_());
}

function redeem(pin, raw) {
  checkPin_(pin);
  var digits = String(raw || '').replace(/\D/g, '');
  if (!digits) return { ok: false, msg: '請輸入券號數字' };
  var no = 'No.' + ('0000' + parseInt(digits, 10)).slice(-4);
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = getSheet_();
    var n = sh.getLastRow();
    var rc = colIndex_('redeemed');
    var vals = n > 1 ? sh.getRange(2, 1, n - 1, rc).getDisplayValues() : [];
    for (var i = 0; i < vals.length; i++) {
      if (vals[i][1] !== no) continue;
      var issued = vals[i][0].slice(0, 10), luck = vals[i][2];
      if (vals[i][rc - 1]) return { ok: false, msg: no + ' 已於 ' + vals[i][rc - 1] + ' 兌換過,不能重複使用', stats: staffStats_(sh) };
      var d = new Date(issued.replace(/-/g, '/') + ' 00:00:00');
      var days = Math.floor((new Date() - d) / 86400000);
      if (!isNaN(days) && days > VALID_DAYS) return { ok: false, msg: no + ' 已過期(' + issued + ' 抽中,有效 ' + VALID_DAYS + ' 天)', stats: staffStats_(sh) };
      var now = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
      sh.getRange(i + 2, rc).setValue(now);
      return { ok: true, msg: no + ' 可折 30 元', detail: issued + ' 抽中「' + luck + '」', stats: staffStats_(sh) };
    }
    return { ok: false, msg: '查無 ' + no + ',請再確認券號', stats: staffStats_(sh) };
  } finally {
    lock.releaseLock();
  }
}

var STAFF_HTML = [
  '<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">',
  '<style>',
  'body{margin:0;font-family:"Noto Sans TC",system-ui,sans-serif;background:#f6f0e4;color:#2b2a26}',
  '.w{max-width:420px;margin:0 auto;padding:20px 16px}',
  'h1{font-size:22px;color:#2f5d46;text-align:center;margin:6px 0 16px}',
  'input{width:100%;box-sizing:border-box;font-size:30px;text-align:center;letter-spacing:.2em;padding:12px;border:2px solid #d9cdb4;border-radius:12px}',
  'button{width:100%;margin-top:12px;padding:16px;font-size:22px;font-weight:700;border:0;border-radius:12px;background:#b8402f;color:#fff}',
  '.r{margin-top:16px;padding:16px;border-radius:12px;text-align:center;font-size:20px;font-weight:700;display:none}',
  '.ok{background:#e3ecdf;color:#2f5d46;border:2px solid #2f5d46}.ng{background:#f3ddd6;color:#b8402f;border:2px solid #b8402f}',
  '.d{font-size:14px;font-weight:400;margin-top:6px}',
  '.s{margin-top:18px;font-size:14px;color:#6b6558;text-align:center;line-height:1.8}',
  '.tip{margin-top:14px;font-size:13px;color:#6b6558;background:#fffdf7;border-radius:10px;padding:10px;line-height:1.7}',
  '</style></head><body><div class="w">',
  '<h1>☕ 咖啡券兌換(店員用)</h1>',
  '<div id="pinBox"><input id="pin" type="password" inputmode="numeric" placeholder="店員密碼"><button onclick="savePin()">登入</button></div>',
  '<div id="main" style="display:none">',
  '<input id="no" inputmode="numeric" placeholder="紙本券上的券號 例 0012">',
  '<button id="go" onclick="go()">兌換</button>',
  '<div id="r" class="r"></div>',
  '<div id="s" class="s"></div>',
  '<div class="tip">① 收下客人的紙本券,輸入券上的券號按「兌換」<br>✔ 綠色=可折 30 元,系統已記錄,請在 iCHEF 按「問卷券折 30」<br>✘ 紅色=不能折(用過、過期或查無券號),紙本券退還客人<br>收回的紙本券請保留,月底對帳</div>',
  '</div></div>',
  '<script>',
  'var PIN="";try{PIN=localStorage.getItem("fr-staff-pin")||"";}catch(e){}',
  'function el(i){return document.getElementById(i);}',
  'function stats(s){if(!s)return;el("s").innerHTML="今日:發出 "+s.issuedToday+" 張・已兌換 "+s.redeemedToday+" 張<br>累計:發出 "+s.issuedAll+" 張・已兌換 "+s.redeemedAll+" 張";}',
  'function login(){google.script.run.withSuccessHandler(function(s){el("pinBox").style.display="none";el("main").style.display="block";stats(s);el("no").focus();}).withFailureHandler(function(e){try{localStorage.removeItem("fr-staff-pin");}catch(x){}alert(e.message);}).staffStats(PIN);}',
  'function savePin(){PIN=el("pin").value.trim();try{localStorage.setItem("fr-staff-pin",PIN);}catch(e){}login();}',
  'function go(){var b=el("go");b.disabled=true;b.textContent="查詢中…";google.script.run.withSuccessHandler(function(res){b.disabled=false;b.textContent="兌換";var r=el("r");r.style.display="block";r.className="r "+(res.ok?"ok":"ng");r.innerHTML=(res.ok?"✅ ":"❌ ")+res.msg+(res.detail?"<div class=d>"+res.detail+"</div>":"");stats(res.stats);el("no").value="";el("no").focus();}).withFailureHandler(function(e){b.disabled=false;b.textContent="兌換";alert(e.message);}).redeem(PIN,el("no").value);}',
  'el("no")&&el("no").addEventListener("keydown",function(e){if(e.key==="Enter")go();});',
  'if(PIN)login();',
  '</script></body></html>'
].join('\n');
