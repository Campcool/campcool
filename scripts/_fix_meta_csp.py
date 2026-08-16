#!/usr/bin/env python3
"""為每頁 head 加 meta CSP（GitHub Pages 無法設 HTTP 標頭，用 meta http-equiv 補防）。
policy: default-src 'self'; img-src 'self' https: data:; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; style-src 'self' 'unsafe-inline'; font-src 'self' data:; connect-src 'self' https://campcool-line-bot.a0920077473.workers.dev https://www.google-analytics.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self';
等 pages build 完成後執行：python3 scripts/_fix_meta_csp.py --apply
"""
import sys
import glob
import re

POLICY = "default-src 'self'; img-src 'self' https: data:; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; style-src 'self' 'unsafe-inline'; font-src 'self' data:; connect-src 'self' https://campcool-line-bot.a0920077473.workers.dev https://www.google-analytics.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self';"

def fix(path, apply=False):
    html = open(path, encoding='utf-8').read()
    if 'http-equiv="Content-Security-Policy"' in html:
        return path, 'skip', html
    tag = f'\n<meta http-equiv="Content-Security-Policy" content="{POLICY}">'
    if '<head>' in html:
        new = html.replace('<head>', '<head>' + tag, 1)
    else:
        m = re.search(r'<head\s[^>]*>', html)
        new = html[:m.end()] + tag + html[m.end():]
    changed = new != html
    if apply and changed:
        open(path, 'w', encoding='utf-8').write(new)
    return path, ('patched' if changed and apply else ('would-patch' if changed else 'skip')), new

if __name__ == '__main__':
    apply = '--apply' in sys.argv
    pages = sorted(glob.glob('*.html'), key=lambda p: p)
    cnt = 0
    for p in pages:
        path, status, _ = fix(p, apply)
        print(f'{status:12s} {path}')
        if status != 'skip':
            cnt += 1
    print('total affected:', cnt)
