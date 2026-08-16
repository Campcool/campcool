import json
from collections import Counter

r = json.load(open('/tmp/a11y_report5.json'))
c = Counter(); per = {}
for k, vs in r.items():
    per[k] = sum(1 for v in (vs or []) if v)
    for v in (vs or []):
        if v:
            c[(v['id'], v['impact'])] += v['count']
            for t in v['target'][:3]:
                if isinstance(t, list):
                    tv = ''.join(''.join(x) if isinstance(x, list) else str(x) for x in t)
                else:
                    tv = str(t)
                print(f'   {k}: {tv[:110]}')
print('pages:', len(r))
for k, nv in sorted(per.items(), key=lambda x: -x[1]):
    print(f'{k:28s} violations={nv}')
print('--- summary ---')
for (i, imp), cnt in c.most_common():
    print(f'{cnt:4d}x {i} [{imp}]')
