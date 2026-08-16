# 多情境驗證：價格行佈局在系統字級放大下不溢出
# 情境: 412px 標準、390px、360px、412+zoom1.15、412+zoom1.25、412+zoom1.3
import asyncio
from PIL import Image
from playwright.async_api import async_playwright

URL = 'https://campcool.tw/'

async def shot(pg, path):
    await pg.goto(URL)
    await pg.wait_for_timeout(1200)
    await pg.evaluate("""() => {
      setTab('fridge');
      document.querySelectorAll('.ad-drawer').forEach(d => d.open = true);
    }""")
    await pg.wait_for_timeout(800)
    sec = await pg.evaluate_handle("""() =>
      [...document.querySelectorAll('section')].find(s => {
        const h2 = s.querySelector('h2');
        return h2 && h2.textContent.includes('其它小物');
      })""")
    await sec.screenshot(path=path)
    print('saved', path)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        cases = [
            ('std_412', {'width': 412, 'height': 900}, None),
            ('std_390', {'width': 390, 'height': 900}, None),
            ('std_360', {'width': 360, 'height': 900}, None),
            ('zoom_412_115', {'width': 412, 'height': 900}, '1.15'),
            ('zoom_412_125', {'width': 412, 'height': 900}, '1.25'),
            ('zoom_412_13', {'width': 412, 'height': 900}, '1.3'),
        ]
        for name, vp, zoom in cases:
            pg = await b.new_page(viewport=vp, device_scale_factor=2)
            if zoom:
                await pg.goto(URL)
                await pg.wait_for_timeout(500)
                await pg.evaluate(f"() => document.documentElement.style.zoom = '{zoom}'")
                # zoom 後再截 section：reload 會還原，所以先 goto 再 zoom 再 evaluate
                await pg.evaluate("""() => {
                  setTab('fridge');
                  document.querySelectorAll('.ad-drawer').forEach(d => d.open = true);
                }""")
                await pg.wait_for_timeout(800)
                sec = await pg.evaluate_handle("""() =>
                  [...document.querySelectorAll('section')].find(s => {
                    const h2 = s.querySelector('h2');
                    return h2 && h2.textContent.includes('其它小物');
                  })""")
                await sec.screenshot(path=f'/tmp/repro_{name}.png')
                print('saved', name)
            else:
                await shot(pg, f'/tmp/repro_{name}.png')
            await pg.close()
        await b.close()

asyncio.run(main())

# 拼六張成兩組對照
pairs = [
    (['/tmp/repro_std_412.png', '/tmp/repro_std_390.png', '/tmp/repro_std_360.png'], '/tmp/repro_std_all.png'),
    (['/tmp/repro_zoom_412_115.png', '/tmp/repro_zoom_412_125.png', '/tmp/repro_zoom_412_13.png'], '/tmp/repro_zoom_all.png'),
]
for lst, out in pairs:
    imgs = [Image.open(x) for x in lst]
    w0 = max(i.width for i in imgs)
    h0 = sum(i.height for i in imgs) + 20 * len(imgs)
    canvas = Image.new('RGB', (w0, h0), 'white')
    yy = 0
    for i in imgs:
        canvas.paste(i, (0, yy)); yy += i.height + 20
    canvas.save(out)
    print('stitched', out, canvas.size)
