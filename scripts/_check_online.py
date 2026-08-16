# 檢查正式站 CSS 指紋
import re, requests

html = requests.get('https://campcool.tw/', timeout=30).text
print('online html length:', len(html))

def show(pat, name):
    m = re.findall(pat, html)
    print(f'== {name} ({len(m)} matches) ==')
    for x in m[:3]:
        print(' ', x[:200])

show(r'\.ad-head[^}]*}', 'ad-head')
show(r'\.ad-title[^}]*}', 'ad-title')
show(r'\.ad-price[^}]*}', 'ad-price')
show(r'\.ad-card[^}]*}', 'ad-card')
# 指紋：ed3114b 修正應含 word-break:keep-all 在 .ad-name
show(r'\.ad-name[^}]*}', 'ad-name')
# 指紋：overflow:hidden 在 ad-card
print('ad-card overflow-hidden count:', len(re.findall(r'\.ad-card\s*\{[^}]*overflow:hidden', html)))
print('ad-name keep-all count:', html.count('keep-all'))
