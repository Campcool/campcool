# 最終驗證：多 viewport × 多 zoom 情境，檢查 16 卡所有文字元素不超卡界
import asyncio
from playwright.async_api import async_playwright

CASES = [
    ('std_412', 412, None),
    ('std_390', 390, None),
    ('std_360', 360, None),
    ('z115_412', 412, '1.15'),
    ('z125_412', 412, '1.25'),
    ('z13_412', 412, '1.3'),
    ('z14_412', 412, '1.4'),
    ('z15_360', 360, '1.5'),
]

JS = """() => {
  setTab('fridge');
  document.querySelectorAll('.ad-drawer').forEach(d => d.open = true);
  const issues = [];
  document.querySelectorAll('.ad-card').forEach(c => {
    const cr = c.getBoundingClientRect();
    ['ad-name','ad-price','ad-brand','ad-note'].forEach(cls => {
      const el = c.querySelector('.'+cls);
      if (!el) return;
      const rr = el.getBoundingClientRect();
      if (rr.right > cr.right + 0.5 || rr.left < cr.left - 0.5)
        issues.push(c.querySelector('.ad-name').textContent.slice(0,10) + ':' + cls + ' r=' + Math.round(rr.right) + ' vs card ' + Math.round(cr.right));
    });
  });
  return issues;
}"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        total = 0
        for name, w, zoom in CASES:
            pg = await b.new_page(viewport={'width': w, 'height': 900}, device_scale_factor=2)
            await pg.goto('file:///home/ubuntu/audit/campcool/index.html')
            await pg.wait_for_timeout(700)
            if zoom:
                await pg.evaluate(f"() => document.documentElement.style.zoom = '{zoom}'")
                await pg.wait_for_timeout(200)
            issues = await pg.evaluate(JS)
            total += len(issues)
            print(f"{name:12s} issues={len(issues)}", issues[:5] if issues else '')
            await pg.close()
        await b.close()
        print('TOTAL issues:', total)
        raise SystemExit(0 if total == 0 else 1)

asyncio.run(main())
