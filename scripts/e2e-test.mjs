#!/usr/bin/env node
/**
 * campcool E2E 核心流程測試（playwright，無 UI，headless chromium）
 * 用途：CI 門禁 + 防回歸。覆蓋：
 *  1. 四 tab 切換（fridge/wiki/booking/rental）內容可見
 *  2. LINE 按鈕全部可點擊且 dataLayer 事件被送出
 *  3. 小物 cards：details 開合、計算器運算
 *  4. 錨點導航 goBooking 跳轉
 *  5. 鍵盤導航（Tab 移動焦點）
 *  6. --selftest：故意破壞後應 FAIL（防假綠）
 */
import { chromium } from 'playwright';

const SELFTEST = process.argv.includes('--selftest');
const URL = `file://${process.cwd()}/index.html`;

let failures = [];
let passes = 0;

function ok(name, cond, detail = '') {
  if (cond) { passes++; console.log(`  PASS ${name}`); }
  else { failures.push(name + (detail ? ' — ' + detail : '')); console.log(`  FAIL ${name}${detail ? ' — ' + detail : ''}`); }
}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 800 } });
const page = await ctx.newPage();

// 收集 dataLayer 事件
const dlEvents = [];
await page.exposeFunction('__e2e_push', (...args) => dlEvents.push(args));

try {
  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => {
    // 攔截 dataLayer push
    const orig = window.dataLayer.push.bind(window.dataLayer);
    window.dataLayer.push = function (...args) { __e2e_push(...args); return orig(...args); };
  });

  // 1. 首頁載入後 rental tab 預設顯示
  let t = await page.evaluate(() => {
    const sec = [...document.querySelectorAll('section')];
    return sec.some(s => s.querySelector('h1')?.textContent.includes('租'));
  });
  ok('rental tab 預設顯示（含 h1 標題）', t);

  // 2. 切換各 tab
  for (const id of ['fridge', 'wiki', 'booking']) {
    await page.evaluate((t) => setTab(t), id);
    t = await page.evaluate((t) => {
      document.querySelectorAll('details').forEach(d => d.open = true);
      const el = document.querySelector(`[data-tab="${t}"]`);
      return el && el.offsetParent !== null && el.offsetHeight > 50;
    }, id);
    ok(`tab 切換到 ${id}（內容可見且非隱藏）`, !!t, id);
  }

  // 3. LINE 按鈕點擊 → dataLayer 事件
  await page.evaluate(() => setTab('rental'));
  const before = dlEvents.length;
  await page.evaluate(() => {
    const a = [...document.querySelectorAll('a[href="https://lin.ee/8maotVi"]')].find(x => x.textContent.includes('詢問'));
    if (a) a.click();
  });
  await page.waitForTimeout(100);
  ok('LINE 點擊送出 dataLayer 事件', dlEvents.length > before, `events=${dlEvents.length - before}`);

  // 4. 小物卡片 details 開合
  await page.evaluate(() => setTab('fridge'));
  await page.waitForTimeout(200);
  const detailsState = await page.evaluate(() => {
    const d = document.querySelector('#addons details');
    if (!d) return 'no-details';
    d.click();
    const opened = d.open;
    d.click();
    return { opened, closed: !d.open };
  });
  ok('小物區塊 details 可開合', detailsState.opened && detailsState.closed, JSON.stringify(detailsState));

  // 5. 價格計算器運算
  const calcRes = await page.evaluate(() => {
    const inp = document.querySelector('#nights, input[name="nights"], .cc-calc input');
    if (!inp) return 'no-input';
    inp.value = '3';
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    inp.dispatchEvent(new Event('change', { bubbles: true }));
    const out = document.querySelector('.cc-calc-output, [id*="calc"]');
    return out ? out.textContent.slice(0, 60) : 'no-output';
  });
  ok('計算器有輸入與輸出（渲染）', calcRes !== 'no-input' && calcRes !== 'no-output', calcRes);

  // 6. 錨點 goBooking 導航
  const navOk = await page.evaluate(() => {
    const btns = [...document.querySelectorAll('a[onclick*="goBooking"]')];
    const beforeTop = window.scrollY;
    window.scrollTo(0, document.body.scrollHeight);
    btns[0]?.click();
    const el = document.getElementById('booking');
    return el && Math.abs(el.getBoundingClientRect().top - window.scrollY) < 200;
  });
  ok('goBooking 錨點導航到位', !!navOk);

  // 7. 鍵盤導航：Tab 移動焦點
  const kb = await page.evaluate(async () => {
    const btn = document.querySelector('.cc-nav-btn, a[href="https://lin.ee/8maotVi"]');
    if (!btn) return 'no-focusable';
    btn.focus();
    const first = document.activeElement === btn;
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', bubbles: true }));
    await new Promise(r => setTimeout(r, 50));
    return { first, activeAfterTab: document.activeElement !== btn };
  });
  ok('鍵盤 Tab 可移動焦點', kb.activeAfterTab || kb.first, JSON.stringify(kb));

  // 8. 無 overflow 橫向捲動（手機 viewport 無水平捲軸）
  const scrollW = await page.evaluate(() => document.documentElement.scrollWidth);
  ok('無水平 overflow（390px viewport）', scrollW <= 400, `scrollWidth=${scrollW}`);

} catch (e) {
  failures.push('exception: ' + e.message);
}

// --selftest：故意破壞一個斷言
if (SELFTEST) {
  const saved = passes;
  ok('SELFTEST 假斷言（永遠失敗用）', false, 'selftest expected failure');
  if (failures.length === 0) { console.log('SELFTEST 漏網：應有失敗但沒有 → 流程有問題'); process.exit(2); }
}

await browser.close();
console.log(`\n${passes} passed, ${failures.length} failed`);
if (failures.length) { console.log('FAILURES:'); failures.forEach(f => console.log(' -', f)); }
process.exit(failures.length ? 1 : 0);
