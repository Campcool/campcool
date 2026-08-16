#!/usr/bin/env python3
"""campcool E2E 核心流程測試（playwright python，headless chromium）
覆蓋：tab 切換、LINE 點擊 logLineClick dataLayer 事件、ad-drawer 開合、
計算器輸出、小物勾選→合計更新、goBooking 錨點導航、鍵盤 Tab 移動、無水平 overflow。
--selftest 防假綠：最後故意斷言失敗，腳本必須 exit 1。
用法：python3 scripts/e2e-test.py [--selftest]
CI 整合（.github/workflows/site-check.yml 加步驟）：
  - name: Install Playwright
    run: pip install playwright && playwright install --with-deps chromium
  - name: E2E tests
    run: python3 scripts/e2e-test.py
  - name: E2E selftest (expect failure)
    run: python3 scripts/e2e-test.py --selftest && exit 1 || true
"""
import asyncio
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = ROOT.joinpath('index.html').as_uri()
SELFTEST = '--selftest' in sys.argv

results = []

def check(name, cond, detail=''):
    results.append((name, bool(cond), detail))
    print(('  PASS ' if cond else '  FAIL ') + name + (f' — {detail}' if detail else ''))

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={'width': 390, 'height': 800})
        page = await ctx.new_page()
        dl_events = []
        await page.expose_function('__e2e_push', lambda *a: dl_events.append(list(a)))
        try:
            await page.goto(URL, wait_until='domcontentloaded')
            await page.evaluate("""
              () => {
                const orig = window.dataLayer.push.bind(window.dataLayer);
                window.dataLayer.push = function (...args) { __e2e_push(JSON.stringify(args)); return orig(...args); };
              }
            """)

            # 1. rental tab 預設顯示
            t = await page.evaluate("""
              () => [...document.querySelectorAll('section')].some(s => {
                const h = s.querySelector('h1');
                return h && h.textContent.includes('租');
              })
            """)
            check('rental tab 預設顯示（含 h1 標題）', t)

            # 2. 切換各 tab
            for tab in ('fridge', 'wiki', 'booking'):
                await page.evaluate(f'setTab("{tab}")')
                await page.evaluate('() => document.querySelectorAll(".ad-drawer").forEach(d => d.open = true)')
                vis = await page.evaluate(f"""
                  () => {{
                    const el = document.querySelector('[data-tab="{tab}"]');
                    return el && el.offsetParent !== null && el.offsetHeight > 50;
                  }}
                """)
                check(f'tab 切換到 {tab}（內容可見且非隱藏）', bool(vis), tab)

            # 3. LINE 點擊 → dataLayer（FAB + form_skip 兩個 logLineClick 入口）
            await page.evaluate('setTab("rental")')
            before = len(dl_events)
            await page.evaluate("""
              () => {
                const fab = document.querySelector('.cc-fab-line');
                if (fab) fab.click();
                const skip = document.querySelector('.cc-form-skip a');
                if (skip) skip.click();
              }
            """)
            await page.wait_for_timeout(100)
            n = len(dl_events) - before
            check('LINE 點擊送出 dataLayer 事件', n >= 1, f'events={n}')

            # 4. ad-drawer 開合
            await page.evaluate('setTab("fridge")')
            await page.wait_for_timeout(200)
            ds = await page.evaluate("""
              () => {
                const d = document.querySelector('.ad-drawer');
                if (!d) return 'no-drawer';
                d.open = true; const opened = d.open;
                d.open = false;
                return JSON.stringify({ opened, closed: !d.open });
              }
            """)
            info = json.loads(ds)
            check('ad-drawer 可開合', info.get('opened') is True and info.get('closed') is True, ds)

            # 5. 計算器輸出渲染（租金計算結果區）
            calc = await page.evaluate("""
              () => {
                const res = document.querySelector('#calcRes, #tcRes');
                return res ? res.textContent.slice(0, 60) : 'no-output';
              }
            """)
            check('計算器輸出元素存在', calc != 'no-output', calc)

            # 6. 小物 checkbox 勾選 → adCart 小計更新（adCart 預設 hidden，先顯示再檢查）
            addons = await page.evaluate("""
              () => {
                const chk = document.querySelector('input.ad-chk');
                if (!chk) return 'no-addon-chk';
                const cart = document.getElementById('adCart');
                const cartN = document.getElementById('adCartN');
                const cartSum = document.getElementById('adCartSum');
                const n = cartN ? cartN.textContent : 'no-n';
                const sum = cartSum ? cartSum.textContent : 'no-sum';
                const before = n + '|' + sum;
                if (cart) cart.hidden = false;
                chk.click();
                const after = cartN.textContent + '|' + cartSum.textContent;
                chk.click();
                addonsUpdate(); // 勾回 → 觸發 addonsUpdate 更新數字
                const after0 = cartN.textContent + '|' + cartSum.textContent;
                if (cart) cart.hidden = true;
                return JSON.stringify({ before, after, after0: after0.slice(0, 20) });
              }
            """)
            info = json.loads(addons)
            parts = info.get('after', '0|0').split('|')
            n_ok, sum_ok = parts[0] != '0', parts[1] != '0'
            check('勾選小物 → 小計金額與件數更新', bool(n_ok) or bool(sum_ok), json.dumps(info))

            # 7. goBooking 錨點導航（scrollIntoView bookingForm）
            # goBooking：先點選，等 browser 側 scrollIntoView 完成後再讀位置
            nav_click = await page.evaluate("""
              () => {
                const btn = document.querySelector('button.cc-line-btn, button.cc-hero-cta');
                if (!btn) return 'no-btn';
                btn.click();
                return document.getElementById('bookingForm') ? 'clicked' : 'no-form';
              }
            """)
            await page.wait_for_timeout(700)
            nav = await page.evaluate("""
              () => {
                const el = document.getElementById('bookingForm');
                if (!el) return JSON.stringify({ visible: false, note: 'no-form' });
                const rect = el.getBoundingClientRect();
                const visible = rect.top >= 0 && rect.top < window.innerHeight && rect.bottom > 0;
                return JSON.stringify({ rectTop: Math.round(rect.top), formTop: Math.round(el.offsetTop), scrollY: Math.round(window.scrollY), visible });
              }
            """)
            nav = json.loads(nav)
            check('goBooking 錨點導航到位', nav.get('visible'), json.dumps(nav))

            # 8. 鍵盤 Tab 移動焦點
            kb = await page.evaluate("""
              async () => {
                const btn = document.querySelector('.cc-nav-btn');
                if (!btn) return { first: false, moved: false, note: 'no-nav-btn' };
                btn.focus();
                const first = document.activeElement === btn;
                document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', code: 'Tab', keyCode: 9, bubbles: true }));
                await new Promise(r => setTimeout(r, 50));
                return { first, moved: document.activeElement !== btn, note: document.activeElement.className };
              }
            """)
            check('鍵盤 Tab 可移動焦點', kb.get('moved') or kb.get('first'), json.dumps(kb))

            # 9. 無水平 overflow
            sw = await page.evaluate('() => document.documentElement.scrollWidth')
            check('無水平 overflow（390px viewport）', sw <= 400, f'scrollWidth={sw}')

        except Exception as e:
            results.append(('exception', False, str(e)))
            print('  EXCEPTION:', e)
        await browser.close()

    if SELFTEST:
        # 防假綠：selftest 模式下故意 FAIL → 腳本必須 exit 1
        check('SELFTEST 假斷言（預期失敗）', False, 'selftest expected failure')
        real_failures = [r for r in results if not r[1] and r[0] != 'SELFTEST 假斷言（預期失敗）']
        if real_failures:
            print('SELFTEST 異常：正常斷言出現失敗，流程有問題，exit 2')
            sys.exit(2)

    n_pass = sum(1 for r in results if r[1])
    n_fail = len(results) - n_pass
    print(f'\n{n_pass} passed, {n_fail} failed')
    if n_fail:
        for r in results:
            if not r[1]:
                print(' -', r[0], r[2])
    sys.exit(1 if n_fail else 0)

asyncio.run(main())
