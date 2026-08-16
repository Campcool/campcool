# 診斷 Lighthouse 首頁扣分細節
import json

d = json.load(open('/tmp/lh_out/index.json'))

print('== server-response-time ==')
a = d['audits'].get('server-response-time')
if a:
    print('  value:', a.get('displayValue'), 'score:', a.get('score'))
    for item in a.get('details', {}).get('items', [])[:3]:
        print('  item:', {k: v for k, v in item.items() if k in ('url','responseTime')})

print('== deprecations ==')
a = d['audits'].get('deprecations')
if a:
    print('  score:', a.get('score'), 'count:', len(a.get('details', {}).get('items', [])))
    for item in a.get('details', {}).get('items', []):
        print('  -', item.get('value', {}).get('text', '') or item.get('sourceLocation', {}).get('url', ''), '|', str(item)[:120])

print('== third-party-summary ==')
a = d['audits'].get('third-party-summary')
if a:
    items = a.get('details', {}).get('items', [])
    for item in items:
        e = item.get('entity', {})
        print('  -', e.get('name'), '| blocking:', round((item.get('mainThreadBlockingTime') or 0)/1000, 2), 's | transfer:', item.get('transferSize'), 'bytes')

print('== LCP ==')
a = d['audits'].get('largest-contentful-paint')
if a:
    print('  LCP:', a.get('displayValue'))

print('== lighthouse-version / metrics summary ==')
le = d.get('audits', {}).get('le-maximum-latency')
print('perf version:', d.get('lighthouseVersion'))
