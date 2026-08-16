# 定位 report5 的 color-contrast 與 region 違規具體來源
import json
from collections import defaultdict

r = json.load(open('/tmp/a11y_report5.json'))
cc = defaultdict(list); rg = defaultdict(list)
for k, vs in r.items():
    for v in (vs or []):
        if not v:
            continue
        if v['id'] == 'color-contrast':
            cc[k].append((v['target'][:70], (v['example'] or '')[:70].replace('\n', ' ')))
        elif v['id'] == 'region':
            rg[k].append(v['target'][:70])

print('=== color-contrast ===')
seen = set()
for k, ts in cc.items():
    for t, ex in ts:
        key = (t, ex[:25])
        if key in seen:
            continue
        seen.add(key)
        print(f'{k:18s} {t} | {ex}')
print()
print('=== region ===')
seen = set()
for k, ts in rg.items():
    for t in ts:
        if t in seen:
            continue
        seen.add(t)
        print(f'{k:18s} {t}')
