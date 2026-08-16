# WCAG 2.1 AA 掃描：18 頁 × tabs（index 含 4 tabs；其它頁只掃默認 tab）
# 使用 axe-core 4.10 全規則（wcag21aa + best-practice），輸出彙總
import asyncio, json, os, sys
from playwright.async_api import async_playwright

PAGES = ['index', 'taipei', 'hsinchu', 'taichung', 'faq',
         'how-it-works', 'reviews', 'btu-guide', 'juz-400', 'sac-688',
         'camping-ac-rental', 'camping-fridge-rental', 'camping-power-guide']

# 快取於 scripts/.cache（不進 git、不部署到正式站）；不存在時自動下載
AXE_LOCAL = os.path.join(os.path.dirname(__file__), '.cache/axe-core.min.js')

TABS = {'index': ['rental', 'wiki', 'booking', 'fridge']}

JS = """async () => {
  if (!window.axe) {
    const scripts = Array.from(document.scripts).map(s => s.src);
    throw new Error('axe not injected; scripts: ' + scripts.slice(0,5).join(','));
  }
  const res = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa','wcag21aaa','best-practice'] }, iframes: false });
  return res.violations.map(v => ({ id: v.id, impact: v.impact, title: v.title || v.id, count: v.nodes.length,
    example: v.nodes[0] ? (v.nodes[0].html || '').slice(0, 200) : '',
    target: v.nodes[0] ? JSON.stringify(v.nodes[0].target) : '' }));
}"""

async def main():
    axe_src = open(AXE_LOCAL).read() if os.path.exists(AXE_LOCAL) else None
    if axe_src is None:
        import urllib.request
        url = 'https://cdn.jsdelivr.net/npm/axe-core@4.10.3/axe.min.js'
        print('downloading axe-core...', flush=True)
        axe_src = urllib.request.urlopen(url, timeout=60).read().decode()
        os.makedirs(os.path.dirname(AXE_LOCAL), exist_ok=True)
        open(AXE_LOCAL, 'w').write(axe_src)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        report = {}
        for page in PAGES:
            if page in report:  # 去重
                continue
            url = f'https://campcool.tw/{page}.html'
            for tab in TABS.get(page, [None]):
                try:
                    pg = await b.new_page(viewport={'width': 390, 'height': 800})
                    await pg.add_init_script(axe_src)
                    await pg.goto(url, timeout=45000, wait_until='domcontentloaded')
                    await pg.wait_for_timeout(1500)
                    if tab:
                        await pg.evaluate(f"setTab('{tab}')")
                        await pg.wait_for_timeout(800)
                    # 展開所有抽屜（小物 tabs）
                    await pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
                    await pg.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
                    await pg.wait_for_timeout(500)
                    violations = await pg.evaluate(JS)
                    key = f"{page}" + (f":{tab}" if tab else "")
                    report[key] = violations
                    print(f"{key:28s} violations={len(violations)}", flush=True)
                    await pg.close()
                except Exception as e:
                    print(f"{page} ERROR: {e}", flush=True)
        await b.close()
        json.dump(report, open('/tmp/a11y_report5.json', 'w'), ensure_ascii=False, indent=1)
        from collections import Counter
        c = Counter()
        for k, vs in report.items():
            for v in vs:
                c[(v['id'], v['impact'], v['title'][:60])] += v['count']
        print('\n=== VIOLATION SUMMARY (id, impact, count) ===')
        for (i, imp, t), cnt in c.most_common():
            print(f"{cnt:4d}x {i} [{imp}] {t}")

asyncio.run(main())
