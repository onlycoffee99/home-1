'use strict';
const crypto=require('crypto'),fs=require('fs'),{execFileSync}=require('child_process');
const [,,cfgPath,path,dataPath,rev]=process.argv;
const cfg=JSON.parse(fs.readFileSync(cfgPath,'utf8'));
const data=JSON.parse(fs.readFileSync(dataPath,'utf8'));
function enc(o,k,iv){const c=crypto.createCipheriv('aes-128-cbc',k,iv);return Buffer.concat([c.update(encodeURIComponent(JSON.stringify(o)),'utf8'),c.final()]).toString('base64');}
function dec(b,k,iv){const d=crypto.createDecipheriv('aes-128-cbc',k,iv);return JSON.parse(decodeURIComponent(Buffer.concat([d.update(Buffer.from(b,'base64')),d.final()]).toString('utf8')));}
const hdr={Timestamp:Math.floor(Date.now()/1000)}; if(rev) hdr.Revision=rev;
const body={MerchantID:cfg.MerchantID,RqHeader:hdr,Data:enc(data,cfg.HashKey,cfg.HashIV)};
const out=execFileSync('curl',['-sS','--max-time','60','-X','POST','https://einvoice.ecpay.com.tw'+path,'-H','Content-Type: application/json','-d',JSON.stringify(body),'-w','\n%{http_code}'],{encoding:'utf8'});
const i=out.lastIndexOf('\n');const outer=JSON.parse(out.slice(0,i));
if(outer.TransCode!==1){console.log(JSON.stringify({ok:false,TransCode:outer.TransCode,TransMsg:outer.TransMsg}));process.exit(1);}
const rtn=dec(outer.Data,cfg.HashKey,cfg.HashIV);
console.log(JSON.stringify(rtn));process.exit(rtn.RtnCode===1?0:1);
