#!/usr/bin/env node
// Postproxy 代發工具:一支指令發 IG、Google 商家檔案(未來可加 Facebook/Threads)。Node 22+,無外部套件。
//
// 金鑰:環境變數 POSTPROXY_API_KEY,或 --env-file <路徑>(KEY=value 檔,放 repo 外)。絕不寫進 repo。
//
// 用法:
//   node tools/social_post.js profiles                         # 列出已連接的帳號(profile id、平台、狀態)
//   node tools/social_post.js placements <profileId>           # Google 商家:列出該連線底下的所有分店 location_id
//   node tools/social_post.js groups                           # 列出 profile group
//   node tools/social_post.js connect instagram                # 產生 IG 授權連結(Google 商家請在 Postproxy 後台按「Connect」)
//   node tools/social_post.js post --profiles prof_xxx[,prof_yyy] --text "文案" \
//        [--media https://...jpg,https://...jpg | --file 本機圖檔] [--at 2026-09-09T03:00:00Z] \
//        [--ig-format post|reel|story] [--first-comment "..."] \
//        [--gbp-location accounts/123/locations/456] [--gbp-format standard|event|offer] [--cta LEARN_MORE|BOOK|ORDER|SHOP|SIGN_UP|CALL --cta-url https://...] \
//        [--draft] [--dry-run]
//   node tools/social_post.js get <postId>                     # 查發布狀態(每平台 published/failed/pending)
//   node tools/social_post.js posts [--status scheduled]       # 列出貼文

const fs = require('fs');
const API = 'https://api.postproxy.dev/api';

function parseArgs(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (!k.startsWith('--')) { a._.push(k); continue; }
    const key = k.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) a[key] = true;
    else { a[key] = next; i++; }
  }
  return a;
}
function loadEnvFile(path) {
  try {
    for (const line of fs.readFileSync(path, 'utf8').split('\n')) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
      if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
    }
  } catch {}
}
async function call(key, path, method = 'GET', body, isForm = false) {
  const headers = { Authorization: `Bearer ${key}` };
  if (body && !isForm) headers['Content-Type'] = 'application/json';
  const res = await fetch(API + path, { method, headers, body: body && !isForm ? JSON.stringify(body) : body });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = text; }
  if (!res.ok) throw new Error(`Postproxy ${res.status} ${method} ${path}: ${typeof data === 'string' ? data : JSON.stringify(data)}`);
  return data;
}
const csv = v => (v ? String(v).split(',').map(s => s.trim()).filter(Boolean) : []);

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args['env-file']) loadEnvFile(args['env-file']);
  const key = process.env.POSTPROXY_API_KEY;
  const cmd = args._[0];
  if (!cmd) { console.error('缺少子指令:profiles | placements | groups | connect | post | get | posts'); process.exit(2); }
  if (!key && !args['dry-run']) { console.error('缺少環境變數 POSTPROXY_API_KEY(或用 --env-file)'); process.exit(2); }

  if (cmd === 'profiles') {
    const r = await call(key, '/profiles');
    const list = Array.isArray(r) ? r : (r.data || r.profiles || []);
    for (const p of list) console.log(`${p.id}\t${p.platform}\t${p.name || p.username || ''}\t${p.status || ''}`);
    if (!list.length) console.log(JSON.stringify(r, null, 2));
    return;
  }
  if (cmd === 'groups') { console.log(JSON.stringify(await call(key, '/profile_groups'), null, 2)); return; }
  if (cmd === 'placements') {
    const id = args._[1]; if (!id) { console.error('用法:placements <profileId>'); process.exit(2); }
    const r = await call(key, `/profiles/${id}/placements`);
    for (const pl of (r.data || [])) console.log(`${pl.id}\t${pl.name || ''}\t${pl.platform_id || pl.resource_name || ''}`);
    if (!(r.data || []).length) console.log(JSON.stringify(r, null, 2));
    return;
  }
  if (cmd === 'connect') {
    const platform = args._[1]; if (!platform) { console.error('用法:connect instagram'); process.exit(2); }
    const groups = await call(key, '/profile_groups');
    const glist = Array.isArray(groups) ? groups : (groups.data || []);
    const gid = args.group || (glist[0] && glist[0].id);
    if (!gid) throw new Error('找不到 profile group');
    const r = await call(key, `/profile_groups/${gid}/initialize_connection`, 'POST', { platform, redirect_url: args.redirect || 'https://app.postproxy.dev/' });
    console.log(r.url || JSON.stringify(r));
    return;
  }
  if (cmd === 'get') { console.log(JSON.stringify(await call(key, `/posts/${args._[1]}`), null, 2)); return; }
  if (cmd === 'posts') {
    const q = args.status ? `?status=${encodeURIComponent(args.status)}` : '';
    const r = await call(key, `/posts${q}`);
    const list = Array.isArray(r) ? r : (r.data || []);
    for (const p of list) console.log(`${p.id}\t${p.status}\t${p.scheduled_at || ''}\t${(p.body || '').slice(0, 40).replace(/\n/g, ' ')}`);
    return;
  }
  if (cmd === 'post') {
    const profiles = csv(args.profiles);
    if (!profiles.length || !args.text) { console.error('post 需要 --profiles 與 --text'); process.exit(2); }
    const post = { body: String(args.text) };
    if (args.at) post.scheduled_at = args.at;
    if (args.draft) post.draft = true;
    const platforms = {};
    if (args['ig-format'] || args['first-comment']) {
      platforms.instagram = {};
      if (args['ig-format']) platforms.instagram.format = args['ig-format'];
      if (args['first-comment']) platforms.instagram.first_comment = args['first-comment'];
    }
    if (args['gbp-location'] || args['gbp-format'] || args.cta) {
      platforms.google_business = { format: args['gbp-format'] || 'standard' };
      if (args['gbp-location']) platforms.google_business.location_id = args['gbp-location'];
      if (args.cta) { platforms.google_business.cta_action_type = args.cta; if (args['cta-url']) platforms.google_business.cta_url = args['cta-url']; }
      for (const k of ['event_title', 'event_start_date', 'event_end_date', 'offer_coupon_code', 'offer_redeem_url', 'offer_terms']) {
        const v = args[k.replace(/_/g, '-')]; if (v) platforms.google_business[k] = v;
      }
    }
    const media = csv(args.media);
    if (args['dry-run']) {
      console.log('[dry-run] 將送出:', JSON.stringify({ post, profiles, media, platforms, file: args.file || null }, null, 2));
      return;
    }
    let r;
    if (args.file) {
      const fd = new FormData();
      fd.append('post[body]', post.body);
      if (post.scheduled_at) fd.append('post[scheduled_at]', post.scheduled_at);
      if (post.draft) fd.append('post[draft]', 'true');
      for (const p of profiles) fd.append('profiles[]', p);
      for (const [plat, opts] of Object.entries(platforms)) for (const [k, v] of Object.entries(opts)) fd.append(`platforms[${plat}][${k}]`, String(v));
      for (const f of csv(args.file)) {
        const buf = fs.readFileSync(f);
        const ext = f.toLowerCase().split('.').pop();
        const type = ext === 'png' ? 'image/png' : ext === 'mp4' ? 'video/mp4' : ext === 'mov' ? 'video/quicktime' : 'image/jpeg';
        fd.append('media[]', new Blob([buf], { type }), f.split('/').pop());
      }
      r = await call(key, '/posts', 'POST', fd, true);
    } else {
      const body = { post, profiles };
      if (media.length) body.media = media;
      if (Object.keys(platforms).length) body.platforms = platforms;
      r = await call(key, '/posts', 'POST', body);
    }
    console.log(`post id=${r.id} status=${r.status} scheduled_at=${r.scheduled_at || '-'}`);
    for (const p of (r.platforms || [])) console.log(`  ${p.platform}\t${p.profile_name || p.profile_id}\t${p.status}${p.error ? '\t' + p.error : ''}`);
    return;
  }
  console.error('未知子指令'); process.exit(2);
}
main().catch(e => { console.error(e.message); process.exit(1); });
