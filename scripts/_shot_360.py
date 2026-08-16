# 360px viewport 驗證：其它小物 section 截圖，產出 /tmp/addons_section_360.png 與 seg 兩段
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 360, 'height': 800}, device_scale_factor=2)
        await pg.goto('file:///home/ubuntu/audit/campcool/index.html')
        await pg.evaluate("""() => {
          setTab('fridge');
          document.querySelectorAll('.ad-drawer').forEach(d => d.open = true);
        }""")
        await pg.wait_for_timeout(800)
        sec = await pg.evaluate_handle("""() => {
          return [...document.querySelectorAll('section')].find(s => {
            const h2 = s.querySelector('h2');
            return h2 && h2.textContent.includes('其它小物');
          });
        }""")
        await sec.screenshot(path='/tmp/addons_section_360.png')
        await b.close()

asyncio.run(main())
print('360 shot saved')

# 裁段
from PIL import Image
img = Image.open('/tmp/addons_section_360.png')
w, h = img.size
seg = 2000
parts = []
for y in range(0, h, seg):
    parts.append(img.crop((0, y, w, min(y + seg, h))))

def stitch(lst, name):
    w0 = max(p.width for p in lst)
    h0 = sum(p.height for p in lst) + 10 * len(lst)
    out = Image.new('RGB', (w0, h0), 'white')
    yy = 0
    for p in lst:
        out.paste(p, (0, yy)); yy += p.height + 10
    out.save(name)

stitch(parts[:3], '/tmp/seg_top_360.png')
stitch(parts[3:], '/tmp/seg_bot_360.png')
print('seg saved', img.size)
