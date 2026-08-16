#!/usr/bin/env python3
"""替換 index.html 中其它小物區塊的 emoji 佔位為 320x320 webp 商品照。
依卡片內 data-name 屬性區分品項（序位匹配）。
用法：python3 scripts/_patch_addon_photos.py
"""
import re

PATH = "/home/ubuntu/audit/campcool/index.html"
html = open(PATH, encoding="utf-8").read()

order = [
    ('動力延長線（綠）5M',  'assets/addon-ext-cord-5m.webp'),
    ('動力延長線（綠）10M', 'assets/addon-ext-cord-10m.webp'),
    ('五米黃光燈條',        'assets/addon-lamp-5m.webp'),
    ('十米黃光燈條',        'assets/addon-lamp-10m.webp'),
    ('製冰機',              'assets/addon-ice-maker.webp'),
    ('渦輪扇',              'assets/addon-fan.webp'),
]

# 依序找到每張卡片：先定位 data-name，再定位之後最近的 ad-ph-ico span
pos = 0
count = 0
for name, src in order:
    dn = html.find(f'data-name="{name}"', pos)
    if dn == -1:
        raise SystemExit(f"FAIL: 找不到卡片 data-name={name}")
    ph = html.find('<span class="ad-ph-ico">', dn)
    if ph == -1 or ph > html.find('</label>', dn):
        raise SystemExit(f"FAIL: {name} 卡片內無 ad-ph-ico 佔位（卡片已結束）")
    end = html.find('</span>', ph)
    if end == -1:
        raise SystemExit(f"FAIL: {name} 佔位 span 無結尾")
    alt = name.replace('（綠）', '')
    new = f'<img src="{src}" alt="{alt}" width="320" height="320" loading="lazy">'
    html = html[:ph] + new + html[end + len('</span>'):]
    pos = dn
    count += 1
    print(f"OK {name} -> {src}")

open(PATH, "w", encoding="utf-8").write(html)
print(f"replaced {count} placeholder spans")

n_img = len(re.findall(r'assets/addon-(ext-cord|lamp|ice-maker|fan)', html))
n_ico = len(re.findall(r'class="ad-ph-ico"', html))
print(f"addon img refs: {n_img}, remaining emoji spans: {n_ico}")
assert n_img == 6 and n_ico == 0, "verification failed"
