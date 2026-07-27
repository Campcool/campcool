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
  '/public/booking-leads',
  'generate_lead',
  '線索編號：',
  '通常 1 小時內回覆',
  '目前不提供宅配',
]) {
  if (!homepage.includes(required)) errors.push('index.html missing required text: ' + required);
}
if (/value:\s*1000/.test(homepage)) {
  errors.push('index.html still assigns a fixed NT$1,000 value to a lead conversion');
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log('Validated ' + htmlFiles.length + ' HTML files, inline scripts, JSON-LD, canonicals, sitemap, and booking funnel markers.');
}
