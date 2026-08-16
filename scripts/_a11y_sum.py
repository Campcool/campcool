import json
from collections import Counter

r = json.load(open('/tmp/a11y_report5.json'))
c = Counter(); per = {}
for k, vs in r.items():
    per[k] = sum(1 for v in (vs or []) if v)
    for v in (vs or []):
        if v:
            c[(v['id'], v['impact'])] += v['count']
            for t in v['target'][:2]:
                c[('src', v['id'], k, t[:60])] += 0  # placeholder
print('pages:', len(r))
for k, nv in sorted(per.items(), key=lambda x: -x[1]):
    print(f'{k:28s} violations={nv}')
print('--- summary ---')
for (i, imp), cnt in c.most_common():
    print(f'{cnt:4d}x {i} [{imp}]')
