#!/bin/bash
# 全頁面 Lighthouse 批測 + 彙總分數與主要扣分項
set -u
cd /tmp
mkdir -p lh_out
PAGES="index taipei hsinchu taichung faq how-it-works reviews btu-guide juz-400 sac-688 pricing services areas"
for p in $PAGES; do
  url="https://campcool.tw/$p.html"
  if ! [ -f "lh_out/$p.json" ]; then
    echo "== $p =="
    npx --yes lighthouse "$url" --quiet \
      --only-categories=performance,seo,best-practices \
      --chrome-flags="--headless --no-sandbox --disable-gpu" \
      --output=json --output-path="lh_out/$p.json" 2>/dev/null || echo "LH failed for $p"
  fi
done

echo "=== SCORE TABLE ==="
for p in $PAGES; do
  [ -f "lh_out/$p.json" ] && python3 - "$p" <<'PY'
import json, sys
d = json.load(open('/tmp/lh_out/' + sys.argv[1] + '.json'))
row = {'page': sys.argv[1]}
for k, v in d.get('categories', {}).items():
    row[k] = round((v.get('score') or 0) * 100)
print(row)
PY
done

echo "=== COMMON AUDIT FAILURES (score<0.9 across pages) ==="
python3 - <<'PY'
import json, glob, collections
fail = collections.Counter()
details = collections.defaultdict(list)
for f in glob.glob('/tmp/lh_out/*.json'):
    p = f.split('/')[-1][:-5]
    try:
        d = json.load(open(f))
    except Exception:
        continue
    for aid, a in d.get('audits', {}).items():
        s = a.get('score')
        if s is not None and s < 0.9:
            fail[(aid, a.get('title','')[:70])] += 1
            if len(details[aid]) < 2:
                details[aid].append((p, a.get('displayValue',''), str(a.get('details',{}))[:150]))
for (aid, title), cnt in fail.most_common(20):
    print(f"{cnt}x {aid} | {title}")
    for p, dv, dt in details[aid]:
        print(f"    [{p}] {dv} | {dt}")
PY
