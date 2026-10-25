#!/usr/bin/env python3
"""HTTP browser regression. External requests are stubbed; no real messages are sent."""
import asyncio
import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'work' / 'redesign-screenshots'
PAGES = sorted(p.name for p in ROOT.glob('*.html')) + ['areas/new-taipei.html']
WIDTHS = (360, 390, 768, 1440)
MEASUREMENTS, FAILURES = [], []

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

def check(name, condition, detail=''):
    print(('PASS ' if condition else 'FAIL ') + name + (f': {detail}' if detail else ''))
    if not condition:
        FAILURES.append(name + ': ' + str(detail))

async def measure(page, label, width):
    metrics = await page.evaluate("""() => {
      const root=document.documentElement;
      return {scrollWidth:root.scrollWidth, viewport:innerWidth,
        rootFont:getComputedStyle(root).fontSize,
        headerHeight:document.querySelector('.cc-header,.cc-site-header').getBoundingClientRect().height,
        overflow:[...document.querySelectorAll('body *')].filter(e=>{
          if(!e.getClientRects().length || e.closest('[hidden]')) return false;
          const r=e.getBoundingClientRect();
          return r.width && (r.right>innerWidth+1 || r.left< -1);
        }).slice(0,8).map(e=>e.tagName+'.'+e.className),
        brokenImages:[...document.images].filter(i=>i.loading!=='lazy' &&
          (!i.complete || !i.naturalWidth)).map(i=>i.getAttribute('src'))};
    }""")
    MEASUREMENTS.append({'page':label, 'width':width, **metrics})
    check(f'{label}/{width}: no horizontal overflow', metrics['scrollWidth']<=width+1,
          json.dumps(metrics, ensure_ascii=False))
    check(f'{label}/{width}: readable root font', metrics['rootFont']=='20px')
    check(f'{label}/{width}: images loaded', not metrics['brokenImages'], metrics['brokenImages'])

async def main(base):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        ctx=await browser.new_context(viewport={'width':390,'height':900}, reduced_motion='reduce')
        external, errors = [], []
        async def route_request(route):
            request=route.request
            if urlparse(request.url).hostname=='127.0.0.1':
                await route.continue_()
                return
            external.append({'url':request.url,'method':request.method,'body':request.post_data or ''})
            if request.resource_type=='script':
                await route.fulfill(status=200, content_type='application/javascript', body='')
            else:
                data={'ga4_measurement_id':''} if '/public/config' in request.url else {}
                await route.fulfill(status=200, content_type='application/json',
                                    headers={'Access-Control-Allow-Origin':'*'}, body=json.dumps(data))
        await ctx.route('**/*', route_request)
        await ctx.add_init_script("""window.__cspViolations=[];
          document.addEventListener('securitypolicyviolation',
            e=>window.__cspViolations.push(e.violatedDirective+':'+e.blockedURI));""")
        page=await ctx.new_page()
        page.on('pageerror', lambda error:errors.append(str(error)))
        try:
            for width in WIDTHS:
                await page.set_viewport_size({'width':width,'height':900})
                for name in PAGES:
                    await page.goto(base+'/'+name+('#rental' if name=='index.html' else ''),
                                    wait_until='networkidle')
                    await measure(page,name,width)
                    check(name+': shared design applied',
                          await page.locator('body').evaluate('e=>getComputedStyle(e).backgroundColor')
                          =='rgb(247, 245, 239)')
                    check(name+': main and skip link',
                          await page.locator('#main-content').count()==1 and
                          await page.locator('.cc-skip').count()==1)
                    await page.locator('.cc-skip').focus()
                    await page.keyboard.press('Enter')
                    main_rect=await page.locator('#main-content').bounding_box()
                    header_rect=await page.locator('.cc-header,.cc-site-header').bounding_box()
                    check(name+': skip link clears sticky header',
                          main_rect['y']>=header_rect['height']-1, str(main_rect))
                    await page.evaluate('scrollTo(0,0)')
                    check(name+': no CSP violations', not await page.evaluate('window.__cspViolations'))
                    if width in (390,1440) and name in (
                            'index.html','juz-400.html','camping-ac-rental.html','areas/new-taipei.html'):
                        await page.screenshot(path=str(OUTPUT/f'{name.replace("/","-")}-{width}.png'),
                                              full_page=True)
                await page.goto(base+'/index.html#rental',wait_until='networkidle')
                closed_height=await page.evaluate('document.documentElement.scrollHeight')
                await page.locator('.cc-more-reviews summary').click()
                check(f'{width}: more reviews reveal real content',
                      await page.locator('.cc-more-reviews .cc-review').first.is_visible() and
                      await page.evaluate('document.documentElement.scrollHeight')>closed_height+100)
                await page.locator('.cc-more-reviews summary').click()
                check(f'{width}: reviews collapse again',
                      not await page.locator('.cc-more-reviews .cc-review').first.is_visible())
                nav='.cc-top-tab' if width>=1024 else '.cc-nav-btn'
                for tab in ('wiki','fridge','booking','rental'):
                    button=page.locator(f'{nav}[data-tab="{tab}"]')
                    await button.click()
                    check(f'{width}: navigate to {tab}',
                          await page.locator(f'.cc-page[data-tab="{tab}"]').is_visible() and
                          await button.get_attribute('aria-current')=='page')
                    await measure(page,'index.html#'+tab,width)
                first=page.locator(nav).first
                await first.focus()
                await page.keyboard.press('Tab')
                check(f'{width}: keyboard focus moves',
                      not await first.evaluate('e=>e===document.activeElement'))
                await page.locator('.cc-model button').first.click()
                check(f'{width}: JUZ carries to booking',
                      await page.locator('#modelSel').input_value()=='艾比酷 JUZ-400' and
                      await page.locator('.cc-page[data-tab="booking"]').is_visible())
                await page.wait_for_function("""() => {
                  const r=document.getElementById('bookingForm').getBoundingClientRect();
                  return r.y>=75 && r.y<innerHeight;
                }""")
                rect=await page.locator('#bookingForm').bounding_box()
                header=await page.locator('.cc-header').bounding_box()
                check(f'{width}: heading clears sticky header',
                      rect['y']>=header['height'], str(rect))
                await page.evaluate('setTab("rental")')
                await page.locator('.cc-model button').nth(1).click()
                check(f'{width}: SAC carries to booking',
                      await page.locator('#modelSel').input_value()=='山水 SAC688')
                await page.evaluate('setTab("rental")')
                await page.locator('.cc-price-pick').nth(1).click()
                check(f'{width}: plan carries to booking',
                      await page.locator('#planSel').input_value()=='三天兩夜')
            await page.set_viewport_size({'width':390,'height':900})
            await page.goto(base+'/index.html#fridge',wait_until='networkidle')
            await page.locator('.ad-drawer summary').first.click()
            await page.locator('label.ad-card').first.click()
            check('C40 card toggles checkbox', await page.locator('.ad-chk').first.is_checked())
            check('C40 updates total',await page.locator('#adCartSum').inner_text()=='800')
            await page.evaluate('addonsToForm()')
            check('add-on carries to booking','C40' in await page.locator('#bkNote').input_value())
            await page.evaluate('resetBooking()')
            await page.locator('.cc-btn-primary').click()
            check('missing date blocks message',
                  await page.locator('#bkMsg').count()==0 and
                  '日期' in await page.locator('#bkRes').inner_text())
            await page.locator('#bkName').fill('Redesign Test Visitor')
            await page.locator('#bkPhone').fill('0999999999')
            await page.locator('#bkDate').fill(await page.locator('#bkDate').get_attribute('min'))
            await page.locator('#bkNote').fill('Redesign privacy fixture')
            before=len(external)
            await page.locator('.cc-btn-primary').click()
            await page.wait_for_timeout(100)
            check('message composed locally',
                  'Redesign Test Visitor' in await page.locator('#bkMsg').inner_text() and
                  '尚未上傳' in await page.locator('#bkRes').inner_text())
            check('compose makes no external request',len(external)==before)
            check('contact data stays off external requests',
                  all('0999999999' not in json.dumps(r) and
                      'Redesign Test Visitor' not in json.dumps(r) and
                      'Redesign privacy fixture' not in json.dumps(r) for r in external))
            check('LINE link opens confirmation',
                  (await page.locator('#bkLineLink').get_attribute('href')).startswith(
                      'https://line.me/R/oaMessage/'))
            events=json.loads(await page.evaluate('JSON.stringify(dataLayer.map(x=>Array.from(x)))'))
            check('compose tracking has no contact data',
                  any(e[:2]==['event','booking_message_composed'] for e in events) and
                  '0999999999' not in json.dumps(events))
            await page.screenshot(path=str(OUTPUT/'booking-390.png'),full_page=True)
            # P01: native choice cards, live summary and truthful LINE handoff.
            await page.set_viewport_size({'width':375,'height':900})
            await page.goto(base+'/index.html#booking',wait_until='networkidle')
            await page.evaluate('resetBooking()')
            radios=page.locator('input[name="ccBookingModel"]')
            check('P01: exactly three native model choices',await radios.count()==3)
            check('P01: recommendation remains the default',
                  await radios.nth(2).is_checked() and
                  await page.locator('#modelSel').input_value()=='不限／請推薦')
            await radios.nth(0).check()
            await radios.nth(0).focus()
            await page.keyboard.press('ArrowDown')
            check('P01: keyboard changes original model and summary',
                  await radios.nth(1).is_checked() and
                  await page.locator('#modelSel').input_value()=='山水 SAC688' and
                  '山水 SAC688' in await page.locator('#bkSummaryModel').inner_text())
            check('P01: keyboard focus visible on selected card',
                  await radios.nth(1).evaluate("e=>parseFloat(getComputedStyle(e.closest('label')).outlineWidth)>=3"))
            date_min=await page.locator('#bkDate').get_attribute('min')
            await page.locator('#bkDate').fill(date_min)
            await page.locator('#planSel').select_option('其他')
            await page.locator('button[onclick="adjustCounter(\'rentDays\',1,3)"]').click()
            await page.locator('button[onclick="adjustCounter(\'acQty\',1,1)"]').click()
            await page.locator('button[onclick="adjustCounter(\'fridgeQty\',1,0)"]').click()
            await page.locator('.cc-pick-btn[data-v="內湖"]').click()
            check('P01: date, custom days, pickup and quantities stay current',
                  await page.locator('#bkSummaryDate').inner_text()==date_min and
                  '4 天' in await page.locator('#bkSummaryPlan').inner_text() and
                  await page.locator('#bkSummaryPickup').inner_text()=='內湖' and
                  await page.locator('#bkSummaryQty').inner_text()=='冷氣 2 台・移動冰箱 1 台')
            await page.locator('#bkName').fill('P01 Fixture')
            await page.locator('#bkPhone').fill('0999999999')
            await page.locator('#bkNote').fill('P01 fictional inquiry note')
            await page.locator('#peopleSel').select_option('7+')
            await page.evaluate('setTab("rental")')
            await page.locator('.cc-model button').first.click()
            check('P01: home model entry preserves existing customer choices',
                  await page.locator('#bkName').input_value()=='P01 Fixture' and
                  await page.locator('#bkPhone').input_value()=='0999999999' and
                  await page.locator('#bkDate').input_value()==date_min and
                  await page.locator('#planSel').input_value()=='其他' and
                  await page.locator('#peopleSel').input_value()=='7+' and
                  'P01 fictional inquiry note' in await page.locator('#bkNote').input_value() and
                  '1-4 人' not in await page.locator('#bkNote').input_value() and
                  'JUZ-400' in await page.locator('#bkSummaryModel').inner_text())
            await page.wait_for_timeout(100)
            await page.screenshot(path=str(OUTPUT/'p01-models-375.png'))
            await page.set_viewport_size({'width':1440,'height':1000})
            await page.locator('#bookingForm').scroll_into_view_if_needed()
            await page.screenshot(path=str(OUTPUT/'p01-models-1440.png'))
            await measure(page,'P01 booking choices',1440)
            await page.set_viewport_size({'width':375,'height':900})
            await page.locator('#bkSummary').scroll_into_view_if_needed()
            await page.screenshot(path=str(OUTPUT/'p01-summary-375.png'))
            await measure(page,'P01 booking summary',375)
            await page.evaluate("""Object.defineProperty(navigator,'clipboard',{configurable:true,
              value:{writeText:()=>Promise.reject(new Error('clipboard denied fixture'))}});""")
            await page.evaluate('dataLayer.length=0')
            before=len(external)
            await page.locator('#bkComposeButton').click()
            await page.wait_for_function("document.querySelector('#bkMsg') !== null")
            check('P01: clipboard refusal retains selectable manual-copy message',
                  await page.locator('#bkMsg').get_attribute('tabindex')=='0' and
                  '手動複製' in await page.locator('#bkComposeStatus').inner_text() and
                  'P01 Fixture' in await page.locator('#bkMsg').inner_text())
            events=json.loads(await page.evaluate('JSON.stringify(dataLayer.map(x=>Array.from(x)))'))
            check('P01: composing records one event and no contact conversion or request',
                  len([e for e in events if e[:2]==['event','booking_message_composed']])==1 and
                  not any(e[:2]==['event','line_click'] or e[:2]==['event','conversion'] for e in events) and
                  len(external)==before)
            await page.locator('#bkLineLink').evaluate("e=>e.addEventListener('click',event=>event.preventDefault())")
            await page.locator('#bkLineLink').click()
            events=json.loads(await page.evaluate('JSON.stringify(dataLayer.map(x=>Array.from(x)))'))
            check('P01: actual LINE click records contact and conversion once',
                  len([e for e in events if e[:2]==['event','line_click']])==1 and
                  len([e for e in events if e[:2]==['event','conversion']])==1)
            await page.locator('#bkDate').fill('2099-05-06')
            check('P01: editing removes the outdated LINE message and link',
                  await page.locator('#bkLineLink').count()==0 and
                  await page.locator('#bkMsg').count()==0 and
                  await page.locator('#bkSummaryDate').inner_text()=='2099-05-06')
            await page.evaluate("""window.__copyCalls=0;
              Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>{
                window.__copyCalls++;return new Promise(resolve=>window.__finishCopy=resolve);
              }}});
              void submitBooking();void submitBooking();""")
            check('P01: repeated compose is locked while clipboard is pending',
                  await page.locator('#bkComposeButton').is_disabled() and
                  await page.evaluate('window.__copyCalls')==1)
            await page.locator('#bkNote').fill('P01 revised while copy pending')
            await page.evaluate('window.__finishCopy()')
            await page.wait_for_function("!document.getElementById('bkComposeButton').disabled")
            check('P01: late clipboard completion cannot restore stale LINE content',
                  await page.locator('#bkLineLink').count()==0 and
                  '重新整理' in await page.locator('#bkComposeStatus').inner_text())
            await page.evaluate("""Object.defineProperty(navigator,'clipboard',{configurable:true,
              value:{writeText:()=>Promise.resolve()}});void submitBooking();""")
            await page.wait_for_function("document.querySelector('#bkMsg') !== null")
            check('P01: retry uses the latest message',
                  'P01 revised while copy pending' in await page.locator('#bkMsg').inner_text() and
                  '2099-05-06' in await page.locator('#bkMsg').inner_text())
            await page.locator('#bkNote').fill('P01 長文字示意。'*80)
            await measure(page,'P01 long text',375)
            await page.evaluate('resetBooking()')
            check('P01: reset synchronizes model, summary, pickup and counters',
                  await radios.nth(2).is_checked() and
                  await page.locator('#bkSummaryDate').inner_text()=='待選擇' and
                  await page.locator('#bkSummaryPickup').inner_text()=='竹北' and
                  await page.locator('#bkSummaryQty').inner_text()=='冷氣 1 台' and
                  await page.locator('#bkMsg').count()==0)
            check('P01: fixture PII stays out of requests and analytics',
                  all('0999999999' not in json.dumps(r) and 'P01 Fixture' not in json.dumps(r)
                      and 'P01 fictional inquiry note' not in json.dumps(r) for r in external) and
                  '0999999999' not in await page.evaluate('JSON.stringify(dataLayer)'))

            await page.goto(base+'/juz-400.html',wait_until='networkidle')
            await page.evaluate("""document.querySelector('.cc-header-contact').addEventListener(
              'click',e=>e.preventDefault());""")
            await page.locator('.cc-header-contact').click()
            events=json.loads(await page.evaluate('JSON.stringify(dataLayer.map(x=>Array.from(x)))'))
            check('new header retains LINE click and conversion',
                  any(e[:2]==['event','line_click'] for e in events) and
                  any(e[:2]==['event','conversion'] for e in events))
            check('no uncaught JavaScript errors',not errors,errors)
        finally:
            (OUTPUT/'measurements.json').write_text(json.dumps(MEASUREMENTS,ensure_ascii=False,indent=2))
            (OUTPUT/'failures.json').write_text(json.dumps(FAILURES,ensure_ascii=False,indent=2))
            await browser.close()
    if FAILURES:
        raise AssertionError('\n'.join(FAILURES))
    print(f'Passed shared design and booking regression; {len(MEASUREMENTS)} layout measurements.')

if __name__=='__main__':
    handler=functools.partial(QuietHandler,directory=str(ROOT))
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        asyncio.run(main(f'http://127.0.0.1:{server.server_port}'))
    finally:
        server.shutdown()
        server.server_close()
