#!/bin/bash
# Lighthouse 基準測量：僅跑 Perf/SEO/BestPractices（無障礙走 axe）
# 對線上的正式站測量，輸出 JSON 摘要
set -e
cd /tmp
mkdir -p lh_out
PAGES="index taipei hsinchu taichung faq how-it-works reviews btu-guide juz-400 sac-688 pricing services areas llms.txt"
for p in $PAGES; do
  if [ "$p" = "llms.txt" ]; then continue; fi
  url="https://campcool.tw/$p.html"
  echo "== $p =="
  npx --yes lighthouse "$url" --quiet \
    --only-categories=performance,seo,best-practices \
    --chrome-flags="--headless --no-sandbox --disable-gpu" \
    --output=json --output-path="lh_out/$p.json" 2>&1 | tail -0
  python3 - <<PYEOF
import json
d = json.load(open('lh_out/$p.json'))
cats = d.get('categories', {})
row = {'page': '$p'}
for k, v in cats.items():
    row[k] = round((v.get('score') or 0) * 100)
print(row)
PYEOF
done
echo "DONE"
