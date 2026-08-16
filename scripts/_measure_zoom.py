# 量化 zoom：用 header「詢問·預約」綠色按鈕與截圖像素字級
# 用戶截圖區域：綠色 CTA 按鈕約 (1055, 830)-(1390, 905)（截圖 y 範圍需先找）
# 做法：找綠色像素帶（CC line 按鈕 #06C755）的高與寬，
# 再本地渲染 412px 量同元素 → 倍率 = 用戶高 / 本地高
import numpy as np
from PIL import Image

img = Image.open('/home/ubuntu/upload/1000033501.jpg').convert('RGB')
arr = np.array(img).astype(int)
h, w, _ = arr.shape
# 綠: G 高、R/B 低
green = (arr[:, :, 1] > 150) & (arr[:, :, 0] < 100) & (arr[:, :, 2] < 120)
# header 區約 y 800-1000（截圖上 header 在網址列下）
# 找 header 列綠色帶：y 830-920 範圍統計
band = green[800:960]
ys, xs = np.nonzero(band)
if len(xs):
    print('green band y: 800+{} ~ 800+{} ({} px), x: {} ~ {} ({} px)'.format(
        ys.min(), ys.max(), ys.max()-ys.min(), xs.min(), xs.max(), xs.max()-xs.min()))
    btn_h = ys.max() - ys.min()
    btn_w = xs.max() - xs.min()
else:
    print('no green band found')
    raise SystemExit

# 本地 412px 渲染量同元素
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 412, 'height': 900}, device_scale_factor=3)
        await pg.goto('https://campcool.tw/')
        await pg.wait_for_timeout(1500)
        m = await pg.evaluate("""() => {
          const btn = document.querySelector('.cc-line-btn');
          const r = btn.getBoundingClientRect();
          const logo = document.querySelector('.cc-logo img');
          const lr = logo.getBoundingClientRect();
          return {btn: {w: r.width, h: r.height, x: r.x, y: r.y}, logo: {w: lr.width, h: lr.height, x: lr.x, y: lr.y}};
        }""")
        await b.close()
        print('local 412px:', m)
        print('btn zoom ratio =', btn_w / m['btn']['w'], '(height ratio', btn_h / m['btn']['h'], ')')

asyncio.run(main())
