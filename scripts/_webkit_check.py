#!/usr/bin/env python3
"""webkit（Safari 引擎）跨瀏覽器驗證 — campcool index.html 關鍵行為檢查
檢查：tab 切換、小物勾選→合計、無水平 overflow、h1 存在、截圖。
依賴：python3 -m playwright install webkit && playwright install-deps webkit
輸出截圖 /tmp/webkit_index.png
"""
import asyncio
from playwright.async_api import async_playwright

URL = 'file:///home/ubuntu/audit/campcool/index.html'

async def main():
    async with async_playwright() as p:
        b = await p.webkit.launch()
        c = await b.new_context(viewport={'width': 390, 'height': 800})
        pg = await c.new_page()
        await pg.goto(URL, wait_until='domcontentloaded')
        await pg.wait_for_timeout(1500)
        r = await pg.evaluate("""() => {
          const issues = [];
          document.querySelectorAll('.ad-drawer').forEach(d => d.open = true);
          document.querySelectorAll('input.ad-chk').forEach(x => x.click());
          addonsUpdate();
          const cart = document.getElementById('adCart');
          if (!cart || cart.hidden) issues.push('adCart hidden');
          const sum = document.getElementById('adCartSum');
          if (!sum || sum.textContent === '0') issues.push('sum=0');
          setTab('fridge');
          const el = document.querySelector('[data-tab="fridge"]');
          if (!el || el.offsetParent === null) issues.push('fridge hidden');
          const sw = document.documentElement.scrollWidth;
          if (sw > 400) issues.push('overflow ' + sw);
          const h1 = document.querySelector('h1');
          if (!h1) issues.push('no h1');
          setTab('booking');
          const bk = document.querySelector('[data-tab="booking"]');
          if (!bk || bk.offsetParent === null) issues.push('booking hidden');
          return JSON.stringify(issues);
        }""")
        await pg.screenshot(path='/tmp/webkit_index.png')
        print('webkit issues:', r)
        await b.close()

asyncio.run(main())
