#!/usr/bin/env node
// 綠界電子發票開立工具(B2C Issue API,支援買受人統編)
// 用法:
//   node issue.js --config <金鑰檔.json> --data <發票資料.json> [--stage]
//
// 金鑰檔格式(勿放進 repo,由 Google 雲端硬碟或環境變數提供):
//   { "MerchantID": "3099012", "HashKey": "...", "HashIV": "..." }
//
// 發票資料檔格式(金額一律「含稅」整數):
//   {
//     "RelateNumber": "自訂單號(可省略,自動產生)",
//     "CustomerIdentifier": "買受人統編(個人戶留空)",
//     "CustomerName": "買受人名稱",
//     "CustomerEmail": "客人email(發票通知寄送)",
//     "Print": "0",            // 有統編建議 "1"(紙本);個人戶 "0"
//     "Donation": "0",
//     "CarrierType": "",       // 個人戶可 "3"=手機條碼,搭配 CarrierNum
//     "CarrierNum": "",
//     "TaxType": "1",
//     "SalesAmount": 125,
//     "InvoiceRemark": "備註(可放廠商訂單編號)",
//     "Items": [ { "ItemName": "停車費", "ItemCount": 1, "ItemWord": "式",
//                  "ItemPrice": 125, "ItemAmount": 125 } ]
//   }
//
// 成功時輸出 JSON:{ ok: true, InvoiceNo, InvoiceDate, RandomNumber, RelateNumber }
// 失敗時輸出 JSON:{ ok: false, ... } 並以非零碼結束。

'use strict';
const crypto = require('crypto');
const fs = require('fs');
const { execFileSync } = require('child_process');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--stage') args.stage = true;
    else if (argv[i].startsWith('--')) args[argv[i].slice(2)] = argv[++i];
  }
  return args;
}

// 綠界規格:JSON → URL encode → AES-128-CBC(PKCS7) → base64
function ecpayEncrypt(obj, key, iv) {
  const cipher = crypto.createCipheriv('aes-128-cbc', key, iv);
  const urlEncoded = encodeURIComponent(JSON.stringify(obj));
  return Buffer.concat([cipher.update(urlEncoded, 'utf8'), cipher.final()]).toString('base64');
}

function ecpayDecrypt(b64, key, iv) {
  const decipher = crypto.createDecipheriv('aes-128-cbc', key, iv);
  const urlEncoded = Buffer.concat([
    decipher.update(Buffer.from(b64, 'base64')),
    decipher.final(),
  ]).toString('utf8');
  return JSON.parse(decodeURIComponent(urlEncoded));
}

// 走 curl 發送:雲端環境的對外連線須經代理(HTTPS_PROXY),Node https 不會自動走代理
function post(url, body) {
  const out = execFileSync('curl', [
    '-sS', '--max-time', '60',
    '-X', 'POST', url,
    '-H', 'Content-Type: application/json',
    '-d', JSON.stringify(body),
    '-w', '\n%{http_code}',
  ], { encoding: 'utf8' });
  const idx = out.lastIndexOf('\n');
  return Promise.resolve({ status: Number(out.slice(idx + 1)), body: out.slice(0, idx) });
}

function fail(msg, extra) {
  console.log(JSON.stringify({ ok: false, error: msg, ...extra }, null, 2));
  process.exit(1);
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.config || !args.data) fail('用法:node issue.js --config 金鑰檔 --data 發票資料檔 [--stage]');

  const cfg = JSON.parse(fs.readFileSync(args.config, 'utf8'));
  const inv = JSON.parse(fs.readFileSync(args.data, 'utf8'));
  for (const k of ['MerchantID', 'HashKey', 'HashIV']) if (!cfg[k]) fail(`金鑰檔缺 ${k}`);

  // 基本檢核:品項金額加總須等於 SalesAmount(全含稅)
  if (!Array.isArray(inv.Items) || inv.Items.length === 0) fail('Items 不可為空');
  const sum = inv.Items.reduce((s, it) => s + Number(it.ItemAmount || 0), 0);
  if (sum !== Number(inv.SalesAmount)) fail(`品項合計 ${sum} 不等於 SalesAmount ${inv.SalesAmount}`);
  if (inv.CustomerIdentifier && !/^\d{8}$/.test(inv.CustomerIdentifier)) fail('買受人統編須為 8 碼數字');
  if (inv.CustomerIdentifier && inv.CarrierType) fail('有統編不可同時使用載具');

  const data = {
    RelateNumber: inv.RelateNumber || 'AI' + new Date().toISOString().replace(/\D/g, '').slice(0, 14),
    CustomerIdentifier: inv.CustomerIdentifier || '',
    CustomerName: inv.CustomerName || '',
    CustomerAddr: inv.CustomerAddr || '',
    CustomerPhone: inv.CustomerPhone || '',
    CustomerEmail: inv.CustomerEmail || '',
    ClearanceMark: '',
    Print: inv.Print || (inv.CustomerIdentifier ? '1' : '0'),
    Donation: inv.Donation || '0',
    LoveCode: inv.LoveCode || '',
    CarrierType: inv.CarrierType || '',
    CarrierNum: inv.CarrierNum || '',
    TaxType: inv.TaxType || '1',
    SalesAmount: Number(inv.SalesAmount),
    InvoiceRemark: inv.InvoiceRemark || '',
    Items: inv.Items.map((it, i) => ({
      ItemSeq: i + 1,
      ItemName: String(it.ItemName),
      ItemCount: Number(it.ItemCount || 1),
      ItemWord: it.ItemWord || '式',
      ItemPrice: Number(it.ItemPrice),
      ItemTaxType: it.ItemTaxType || '1',
      ItemAmount: Number(it.ItemAmount),
      ItemRemark: it.ItemRemark || '',
    })),
    InvType: '07',
    vat: '1',
  };

  const host = args.stage ? 'https://einvoice-stage.ecpay.com.tw' : 'https://einvoice.ecpay.com.tw';
  const body = {
    MerchantID: cfg.MerchantID,
    RqHeader: { Timestamp: Math.floor(Date.now() / 1000), Revision: '3.0.0' },
    Data: ecpayEncrypt(data, cfg.HashKey, cfg.HashIV),
  };

  const res = await post(host + '/B2CInvoice/Issue', body);
  let outer;
  try { outer = JSON.parse(res.body); } catch { fail('回應非 JSON', { http: res.status, raw: res.body.slice(0, 500) }); }
  if (outer.TransCode !== 1) fail('傳輸層失敗', { TransCode: outer.TransCode, TransMsg: outer.TransMsg });

  const rtn = ecpayDecrypt(outer.Data, cfg.HashKey, cfg.HashIV);
  if (rtn.RtnCode !== 1) fail('開立失敗', { RtnCode: rtn.RtnCode, RtnMsg: rtn.RtnMsg, RelateNumber: data.RelateNumber });

  console.log(JSON.stringify({
    ok: true,
    InvoiceNo: rtn.InvoiceNo,
    InvoiceDate: rtn.InvoiceDate,
    RandomNumber: rtn.RandomNumber,
    RelateNumber: data.RelateNumber,
    SalesAmount: data.SalesAmount,
  }, null, 2));
}

main().catch((e) => fail(e.message));
