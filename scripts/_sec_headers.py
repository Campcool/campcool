# 檢查正式站安全標頭現狀
import requests

h = requests.head('https://campcool.tw/', timeout=30).headers
h2 = requests.get('https://campcool.tw/', timeout=30).headers
print('== HEAD headers ==')
for k in ['strict-transport-security', 'x-content-type-options', 'x-frame-options',
          'content-security-policy', 'referrer-policy', 'permissions-policy',
          'x-xss-protection', 'cross-origin-opener-policy', 'cross-origin-resource-policy']:
    print(f"{k:42s} {h.get(k, '(missing)')}")
print('\n== GET server ==', h2.get('server'), '| via:', h2.get('via'), '| cache:', h2.get('cache-control'))
