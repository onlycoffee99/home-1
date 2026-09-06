#!/usr/bin/env node
// LINE 官方帳號群發工具(Messaging API)。Node 22+,無外部套件。
//
// 用法:
//   node tools/line_broadcast.js --store wudou --text "【舞荳咖啡】今天蘋果派到貨..." [--image https://...jpg] [--dry-run]
//   node tools/line_broadcast.js --store tc2   --text "..." --to <userId>      # 只推給一個人(測試用)
//   node tools/line_broadcast.js --store wudou --quota                          # 查本月免費額度與已用量
//
// 金鑰放環境變數,絕不寫進 repo:
//   LINE_TOKEN_WUDOU  = 礁溪一館 @910icecd 的 Channel access token (long-lived)
//   LINE_TOKEN_TC2    = 台中二館 @897xndml 的 Channel access token (long-lived)

const STORES = {
  wudou: { env: 'LINE_TOKEN_WUDOU', name: '舞荳咖啡(礁溪一館 @910icecd)' },
  tc2:   { env: 'LINE_TOKEN_TC2',   name: '台中二館(@897xndml)' },
};
const API = 'https://api.line.me/v2/bot';

function parseArgs(argv) {
  const a = {};
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (!k.startsWith('--')) continue;
    const key = k.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) a[key] = true;
    else { a[key] = next; i++; }
  }
  return a;
}

async function call(token, path, method = 'GET', body) {
  const res = await fetch(API + path, {
    method,
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`LINE API ${res.status} ${path}: ${text}`);
  return text ? JSON.parse(text) : {};
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const store = STORES[args.store];
  if (!store) { console.error('請指定 --store wudou 或 --store tc2'); process.exit(2); }
  const token = process.env[store.env];
  if (!token && !args['dry-run']) { console.error(`缺少環境變數 ${store.env}(${store.name})`); process.exit(2); }

  if (args.quota) {
    const q = await call(token, '/message/quota');
    const c = await call(token, '/message/quota/consumption');
    console.log(`${store.name} 本月額度:${q.type === 'limited' ? q.value : '無上限'},已用:${c.totalUsage}`);
    return;
  }

  if (!args.text) { console.error('缺少 --text'); process.exit(2); }
  const messages = [{ type: 'text', text: String(args.text) }];
  if (args.image) {
    if (!/^https:\/\//.test(args.image)) { console.error('--image 必須是 https 連結'); process.exit(2); }
    messages.push({ type: 'image', originalContentUrl: args.image, previewImageUrl: args.image });
  }

  if (args['dry-run']) {
    console.log(`[dry-run] ${store.name} 將發送:\n${JSON.stringify(messages, null, 2)}`);
    return;
  }
  if (args.to) {
    await call(token, '/message/push', 'POST', { to: args.to, messages });
    console.log(`${store.name} 已推播給 ${args.to}`);
  } else {
    await call(token, '/message/broadcast', 'POST', { messages });
    console.log(`${store.name} 已群發給全部好友`);
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });
