# 嚴謹級基準彙總：Lighthouse 分數表 + axe 違規統計
import json, glob
from collections import Counter

print('=== LIGHTHOUSE SCORE TABLE ===')
rows = []
for f in sorted(glob.glob('/tmp/lh_out/*.json')):
    p = f.split('/')[-1][:-5]
    try:
        d = json.load(open(f))
    except Exception:
        continue
    row = {'page': p}
    for k, v in d.get('categories', {}).items():
        row[k] = round((v.get('score') or 0) * 100)
    rows.append(row)
    print(f"{p:22s} perf={row.get('performance'):3d} seo={row.get('seo'):3d} bp={row.get('best-practices'):3d}")

print('\n=== COMMON AUDIT FAILURES (score<0.9, count across pages) ===')
fail = Counter()
details = {}
for f in glob.glob('/tmp/lh_out/*.json'):
    p = f.split('/')[-1][:-5]
    try:
        d = json.load(open(f))
    except Exception:
        continue
    for aid, a in d.get('audits', {}).items():
        s = a.get('score')
        if s is not None and s < 0.9:
            fail[(aid, (a.get('title') or '')[:55])] += 1
            if aid not in details:
                details[aid] = (p, a.get('displayValue', ''), a.get('score'))

for (aid, title), cnt in fail.most_common(25):
    p, dv, sc = details[aid]
    print(f"{cnt:2d}x {aid} [{round((sc or 0)*100)}] {title} | e.g. [{p}] {dv}")

print('\n=== AXE VIOLATIONS (per page) ===')
report = json.load(open('/tmp/a11y_report.json'))
c = Counter()
perpage = Counter()
for k, vs in report.items():
    perpage[k] = sum(v['count'] for v in vs)
    for v in vs:
        if not v:
            continue
        c[(v['id'], v['impact'], (v.get('title') or '')[:60])] += v['count']
for k in sorted(perpage):
    print(f"{k:28s} violation-nodes={perpage[k]}")
print('\n=== AXE SUMMARY (id, impact, total nodes) ===')
for (i, imp, t), cnt in c.most_common(25):
    print(f"{cnt:4d}x {i} [{imp}] {t}")
