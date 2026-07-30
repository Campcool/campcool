import fs from 'node:fs';
import path from 'node:path';

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

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log('Validated ' + htmlFiles.length + ' HTML files, inline scripts, JSON-LD, canonicals, sitemap, local-only booking, and LINE funnel markers.');
}
