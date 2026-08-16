# 彙總 axe 掃描結果：每頁違規數 + 違規類型分佈
import json, os, sys
from collections import Counter

for name in ('/tmp/a11y_report.json', '/tmp/a11y_report2.json', '/tmp/a11y_report3.json'):
    if not os.path.exists(name):
        print(f'{name}: 不存在（跳過）'); continue
    r = json.load(open(name))
    print(f'\n===== {name} ({len(r)} pages) =====')
    c = Counter()
    per_page = {}
    for k, vs in r.items():
        nv = sum(1 for v in (vs or []) if v)
        per_page[k] = nv
        for v in (vs or []):
            if v:
                c[(v['id'], v['impact'])] += v['count']
    print('--- per page ---')
    for k, nv in per_page.items():
        print(f'{k:28s} violations={nv}')
    print('--- summary ---')
    for (i, imp), cnt in c.most_common():
        print(f'{cnt:4d}x {i} [{imp}]')
