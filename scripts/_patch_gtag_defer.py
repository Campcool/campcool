# 把其餘頁面的 gtag.js <script async src=...> 改為延遲載入模式（與 index.html 同模式）
import re, glob

SRC_TAG = '<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18167565264"></script>'

DEFER_BLOCK = """<script>
  (function () {
    var loaded = false;
    function loadGtag() {
      if (loaded) return;
      loaded = true;
      var s = document.createElement('script');
      s.src = 'https://www.googletagmanager.com/gtag/js?id=AW-18167565264';
      s.async = true;
      document.head.appendChild(s);
    }
    var timer = setTimeout(loadGtag, 2500);
    var onFirst = function () {
      clearTimeout(timer);
      loadGtag();
      document.removeEventListener('pointerdown', onFirst);
      document.removeEventListener('keydown', onFirst);
      document.removeEventListener('scroll', onFirst);
    };
    document.addEventListener('pointerdown', onFirst, { passive: true });
    document.addEventListener('keydown', onFirst, { passive: true });
    document.addEventListener('scroll', onFirst, { passive: true });
  })();
</script>"""

changed = 0
for f in sorted(glob.glob('*.html')):
    html = open(f, encoding='utf-8').read()
    if SRC_TAG not in html:
        continue
    # 只在其他頁做（index 已手改）
    if f == 'index.html':
        if SRC_TAG in html:
            print(f, 'STILL HAS SRC TAG - check manually')
        continue
    html = html.replace(SRC_TAG, DEFER_BLOCK)
    open(f, 'w', encoding='utf-8').write(html)
    changed += 1
    print('patched', f)
print('total patched:', changed)
