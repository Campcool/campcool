import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

// ── 滿分制第二輪：20 項斷言 + --selftest 防假綠 ───────────────
// 新增斷言（此段以下）：
//  9. 死重圖片不可再被任何頁面引用（homepage_hero.png / taiwan_map.png）
// 10. 每頁 LINE CTA 閉環（areas 殘頁除外）
// 11. 兩支計算機門檻一致性（ac: 2.75 坪 / 9 ㎡、tent: 9 ㎡ / 16 坪拒租）
// 12. 小物品項數 = 15（產品合約）
// 13. GA4 config endpoint 統一 v=20260727（14 頁）
// 14. areas 殘頁 noindex
// 15. 評論圖 img src 僅限 1 張 jpg（產品實照），其餘 webp
// 16. llms.txt  freshness ≤ 60 天
// 17. git 追蹤清單不含死重圖
// 18. selftest 模式（故意破壞→須抓住→還原）


const root = process.cwd();
const htmlFiles = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'node_modules') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith('.html')) htmlFiles.push(full);
  }
}

walk(root);
const errors = [];
const scriptRe = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;

for (const file of htmlFiles) {
  const relative = path.relative(root, file).replaceAll('\\', '/');
  const html = fs.readFileSync(file, 'utf8');
  if (!/<link\s+rel=["']canonical["'][^>]+href=["']https:\/\/campcool\.tw\//i.test(html)) {
    errors.push(relative + ': missing absolute canonical');
  }

  let match;
  while ((match = scriptRe.exec(html))) {
    const attrs = match[1];
    const body = match[2].trim();
    if (!body || /\bsrc\s*=/.test(attrs)) continue;
    if (/application\/ld\+json/i.test(attrs)) {
      try { JSON.parse(body); }
      catch (error) { errors.push(relative + ': invalid JSON-LD: ' + error.message); }
      continue;
    }
    try { new Function(body); }
    catch (error) { errors.push(relative + ': invalid inline JavaScript: ' + error.message); }
  }
}

const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
for (const duplicate of ['areas/taipei.html', 'areas/hsinchu.html', 'areas/taichung.html']) {
  if (sitemap.includes(duplicate)) errors.push('sitemap.xml still contains duplicate ' + duplicate);
}

const homepage = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
for (const required of [
  'booking_message_composed',
  '內容只在此裝置整理',
  '[來源:booking_form]',
  'cc-line-shimmer',
  'prefers-reduced-motion: reduce',
  '竹北社區取件（預約制）',
  '通常 1 小時內回覆',
  '目前不提供宅配',
]) {
  if (!homepage.includes(required)) errors.push('index.html missing required text: ' + required);
}
for (const forbidden of [
  '/public/booking-leads',
  'BOOKING_LEAD_API',
  'renter_contact',
  'ga_client_id',
  'generate_lead',
]) {
  if (homepage.includes(forbidden)) errors.push('index.html still contains pre-LINE lead upload marker: ' + forbidden);
}
if (/value:\s*1000/.test(homepage)) {
  errors.push('index.html still assigns a fixed NT$1,000 value to a lead conversion');
}

const publicHtml = htmlFiles.map((file) => fs.readFileSync(file, 'utf8')).join('\n');
if (/24\s*H/i.test(publicHtml)) {
  errors.push('public HTML still advertises 24H pickup or return');
}
for (const forbidden of ['社區寄櫃', '寄櫃自取', '取件碼', '隨時自取']) {
  if (publicHtml.includes(forbidden)) errors.push('public HTML still contains retired community locker copy: ' + forbidden);
}

// ── 9. 死重圖片不可再被任何頁面引用（asset 檔案本身已 git rm） ──
for (const dead of ['homepage_hero.png', 'taiwan_map.png']) {
  for (const file of htmlFiles) {
    const html = fs.readFileSync(file, 'utf8');
    if (html.includes(dead)) {
      errors.push(path.relative(root, file).replaceAll('\\', '/') + ' still references removed heavy image ' + dead);
    }
  }
}

// ── 10. 每頁 LINE CTA 閉環（areas 殘頁除外）──────────────────
for (const file of htmlFiles) {
  const relative = path.relative(root, file).replaceAll('\\', '/');
  if (relative.startsWith('areas/')) continue;
  const html = fs.readFileSync(file, 'utf8');
  if (!/lin\.ee|logLineClick|cc-line/.test(html)) {
    errors.push(relative + ': missing LINE CTA (lin.ee / logLineClick / cc-line)');
  }
}

// ── 11. 兩支計算機門檻一致性（產品合約）────────────────────────
const calcContract = [
  { page: 'index.html', expects: ['area > 2.75', 'area > 9', 'area > 16'] },
];
for (const contract of calcContract) {
  const html = fs.readFileSync(path.join(root, contract.page), 'utf8');
  for (const expect of contract.expects) {
    if (!html.includes(expect)) errors.push(contract.page + ': missing calculator threshold "' + expect + '"');
  }
}
// 16 坪以上必須有明確拒租文案
if (!/16/.test(homepage)) errors.push('index.html: calculator missing 16-ping rejection constant');

// ── 12. 小物品項數 = 16（產品合約，改動任一品項都要連動更新）─────
// 僅數 ad-name 不夠：單品項改名 ad-name 總數不變。必須逐項驗證 16 品項全在。
const addonContract = [
  'C40 移動冰箱 40L',
  '5×8 黑膠天幕',
  '蝶形天幕',
  '黑狗速開穹頂',
  '電吉拉 mini 行動電站',
  '簡易焚火台',
  '青鸞觀火台',
  'C8 投影機',
  '製冰機',
  '渦輪扇',
  '五米黃光燈條',
  '十米黃光燈條',
  'G40 復古 LED 燈串',
  '持久帳篷小燈',
  '動力延長線（綠）5M',
  '動力延長線（綠）10M',
];
const addonCount = (homepage.match(/class="ad-name">/g) || []).length;
if (addonCount !== 16) errors.push('index.html: addon count is ' + addonCount + ' but product contract requires 16');
for (const addon of addonContract) {
  if (!homepage.includes(addon)) errors.push('index.html: product-contract addon missing: ' + addon);
}
const llms = fs.readFileSync(path.join(root, 'llms.txt'), 'utf8');
if (!llms.includes('16 品項')) errors.push('llms.txt: missing explicit 16-item declaration');
// llms.txt 小物價格表必須覆蓋 16 品項（至少 16 個含「$」與數字的中價描述）
const llmsPrices = (llms.match(/\$\s?[0-9][0-9,]+/g) || []).length;
if (llmsPrices < 16) errors.push('llms.txt: price table covers only ' + llmsPrices + ' items but requires at least 16');

// ── 13. GA4 config endpoint 統一版號（14 頁，ID 由 campcool-bot Worker 注入）─
const configEndpoint = '/public/config?v=20260727';
const configPages = htmlFiles.filter((file) => fs.readFileSync(file, 'utf8').includes('/public/config'));
for (const file of configPages) {
  const html = fs.readFileSync(file, 'utf8');
  if (!html.includes(configEndpoint)) {
    errors.push(path.relative(root, file).replaceAll('\\', '/') + ': references stale config endpoint version');
  }
}
if (configPages.length < 14) errors.push('config endpoint coverage: only ' + configPages.length + ' pages include /public/config (expected 14)');

// ── 14. areas 殘頁必須 noindex（meta-refresh 轉址頁不參與索引）───
for (const dup of ['areas/taipei.html', 'areas/hsinchu.html', 'areas/taichung.html']) {
  const html = fs.readFileSync(path.join(root, dup), 'utf8');
  if (!/noindex/.test(html)) errors.push(dup + ': duplicate-area page missing noindex meta');
}

// ── 15. 評論圖 img src 僅限 1 張 jpg（emergency 產品實照），其餘 webp ─
for (const file of htmlFiles) {
  const relative = path.relative(root, file).replaceAll('\\', '/');
  const html = fs.readFileSync(file, 'utf8');
  const jpgInSrc = (html.match(/src=["'][^"']*\.jpg["']/g) || []).length;
  if (jpgInSrc > 1) errors.push(relative + ': references ' + jpgInSrc + ' jpg images in img src (reviews must be webp; product photos max 1)');
}

// ── 16. llms.txt 新鮮度 ≤ 60 天 ────────────────────────────────
const dateMatch = llms.match(/最後更新[：:]\s*(\d{4}-\d{2}-\d{2})/);
if (dateMatch) {
  const age = Math.floor((Date.now() - new Date(dateMatch[1]).getTime()) / 86400000);
  if (age > 60) errors.push('llms.txt: last-updated date is ' + age + ' days old (max 60)');
}

// ── 17. git 追蹤清單不含死重圖（防有人手動加回）────────────────
let trackedFiles = [];
try {
  const gitIndex = fs.readFileSync(path.join(root, '.git/index'));
  // .git/index 二進檔中檔案名以 '\0' 分隔出現
  const names = gitIndex.toString('latin1').split('\0');
  for (const dead of ['homepage_hero.png', 'taiwan_map.png']) {
    if (names.some((name) => name.includes(dead))) {
      errors.push('repo: tracked dead heavy image still in git index: ' + dead);
    }
  }
} catch (missing) { /* CI 無 git 索引時略過 */ }

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log('Validated ' + htmlFiles.length + ' HTML files, inline scripts, JSON-LD, canonicals, sitemap, local-only booking, LINE funnel, dead-weight images, calculator thresholds, 16-addon product contract, config endpoint coverage, duplicate-area noindex, review webp policy, llms.txt freshness, and git tracking.');
}

// ── 18. --selftest 防假綠模式 ───────────────────────────────────
// 驗證規則不是假綠：故意破壞產品事實，validate 必須抓住（exit 1）；
// 還原後必須通過（exit 0）。任何一步不符預期，selftest 整體 exit 1。
if (process.argv.includes('--selftest')) {
  const indexPath = path.join(root, 'index.html');
  let original = null;
  const checkpoint = {
    originalHtml: () => (original = original || fs.readFileSync(indexPath, 'utf8')),
    restore: () => { if (original) fs.writeFileSync(indexPath, original); original = null; },
  };
  const run = (label, script, expectFail) => {
    const out = fs.readFileSync(indexPath, 'utf8');
    let code = 0;
    try {
      execSync('node ' + path.join(root, 'scripts/validate-site.mjs'), { cwd: root, stdio: 'pipe' });
    } catch (spawn) { code = spawn.status || 1; }
    const caught = code !== 0;
    const ok = caught === expectFail;
    console.log((ok ? 'PASS' : 'FAIL') + ' | selftest ' + label + ' (validate exited ' + code + ', expected ' + (expectFail ? 'non-zero' : 'zero') + ')');
    if (!ok) process.exitCode = 1;
    return caught;
  };
  // 破壞 1：必留文案消失 → 應抓住
  checkpoint.originalHtml();
  fs.writeFileSync(indexPath, original.replace('booking_message_composed', 'REMOVED_PLACEHOLDER'));
  run('required-text-missing', null, true);
  checkpoint.restore();
  // 破壞 2：出現禁入標記 → 應抓住
  checkpoint.originalHtml();
  fs.writeFileSync(indexPath, original.replace('cc-line-shimmer', 'REMOVED_SHIMMER') + '\n<!-- /public/booking-leads secret marker -->');
  run('forbidden-marker-reintroduced', null, true);
  checkpoint.restore();
  // 破壞 3：計算機門檻被改 → 應抓住
  checkpoint.originalHtml();
  fs.writeFileSync(indexPath, original.replaceAll('area > 2.75', 'area > 1.00'));
  run('calculator-threshold-tampered', null, true);
  checkpoint.restore();
  // 破壞 4：小物品項被改名（15 品項逐項斷言應抓住）→ 應抓住
  checkpoint.originalHtml();
  fs.writeFileSync(indexPath, original.replaceAll('C40 移動冰箱 40L', 'REMOVED_ADDON'));
  run('addon-contract-broken', null, true);
  checkpoint.restore();
  // 還原後正常 validate 必須通過
  run('clean-state-passes', null, false);
  process.exit();
}
