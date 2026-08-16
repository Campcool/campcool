# 視覺驗證：本地 index.html，全部 drawers 展開，直接截「其它小物」section 整段
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 390, 'height': 900}, device_scale_factor=2)
        await pg.goto('file:///home/ubuntu/audit/campcool/index.html')
        # 其它小物在 data-tab 分頁內，先切到 fridge tab 再展開 drawers
        await pg.evaluate('''() => {
          setTab('fridge');
          document.querySelectorAll('details').forEach(d => d.open = true);
        }''')
        await pg.wait_for_timeout(800)
        # 定位其它小物 section，直接 element screenshot（playwright 會自動捲動到元素）
        handle = await pg.evaluate_handle('''() => {
          const sec = [...document.querySelectorAll('section')].find(s => s.querySelector('h2') && s.querySelector('h2').textContent.includes('其它小物'));
          return sec || null;
        }''')
        if await handle.evaluate('s => s !== null'):
            await handle.screenshot(path='/tmp/addons_section.png')
            # 全頁截圖
            await pg.screenshot(path='/tmp/addons_full.png', full_page=True)
            print('section shot saved; sec found')
        else:
            print('section not found')
            await pg.screenshot(path='/tmp/addons_full.png', full_page=True)
        await b.close()

asyncio.run(main())
