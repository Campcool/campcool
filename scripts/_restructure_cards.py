# 小物卡片左右兩欄佈局重排：
# 原: <span class="ad-info"><ad-brand><ad-name><ad-meta><ad-note></span><ad-price>
# 新: <span class="ad-info"><span class="ad-head"><span class="ad-title"><ad-brand><ad-name></span><ad-price></span><ad-meta><ad-note></span>
import re

P = 'index.html'
html = open(P).read()

# 匹配每張卡片: <span class="ad-info">\n(brand)(name)(meta)(note) 直到 </span>
pat = re.compile(r'<span class="ad-info">\n(\s*<span class="ad-brand">.*?</span>\n)(\s*<span class="ad-name">.*?</span>\n)(\s*<span class="ad-meta">.*?</span>\n)(\s*<span class="ad-note">.*?</span>\n)\s*</span>\n(\s*<span class="ad-price">.*?</span>\n)', re.S)

def repl(m):
    brand, name, meta, note, price = m.groups()
    head = '                <span class="ad-head">\n' + brand + name + '                  ' + price.strip() + '\n                </span>\n'
    return '<span class="ad-info">\n' + head + meta + note + '              </span>\n'

new, n = pat.subn(repl, html)
print('restructured:', n)
assert n == 16, 'expected 16 cards, got ' + str(n)
open(P, 'w').write(new)
