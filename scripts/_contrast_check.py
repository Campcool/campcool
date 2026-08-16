# 對比度計算：確認各違規組合是否真的不及格，驗證修正後的顏色
def lum(hex6):
    hex6 = hex6.lstrip('#')
    r, g, b = [int(hex6[i:i+2], 16)/255 for i in (0, 2, 4)]
    def f(c): return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)

def ratio(fg, bg):
    l1, l2 = lum(fg), lum(bg)
    if l2 > l1: l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

cases = [
    # (name, fg, bg, required) — 只驗修後值
    ('.logo .s #047857/白', '#047857', '#ffffff', 4.5),
    ('.review-date #6b7280/白', '#6b7280', '#ffffff', 4.5),
    ('camping-ac .btn 白字/#047857', '#ffffff', '#047857', 4.5),
    ('camping-fridge .btn 白字/#075985', '#ffffff', '#075985', 4.5),
    ('camping-power .btn 白字/#c2410c', '#ffffff', '#c2410c', 4.5),
    ('sac-688 .btn 白字/#047857', '#ffffff', '#047857', 4.5),
    ('btu .line-btn/.btn-line 白字/#047857', '#ffffff', '#047857', 4.5),
    ('btu .btn-site #047857/白', '#047857', '#ffffff', 4.5),
    ('index .cc-logo-sub #047857/白', '#047857', '#ffffff', 4.5),
    ('index .tag 白字/#047857', '#ffffff', '#047857', 4.5),
    ('how-it-works .cta-block a #047857/白', '#047857', '#ffffff', 4.5),
    ('reviews .google-review-cta a #047857/白', '#047857', '#ffffff', 4.5),
    ('reviews .invite .s #059669/白(font 13px+)', '#059669', '#ffffff', 4.5),
    ('index .cc-price td.price #059669/白(font 17.6px+)', '#059669', '#ffffff', 4.5),
    ('index .cc-price td.desc #6b7280/白', '#6b7280', '#ffffff', 4.5),
    ('index .cc-price tr.hl td.price #047857/#dcfce7', '#047857', '#dcfce7', 4.5),
    ('index .cc-ann-dot::before 白/#34d399（裝飾，非文字，axe 未報）', '#ffffff', '#34d399', 3.0),
]
for name, fg, bg, req in cases:
    r = ratio(fg, bg)
    status = 'PASS' if r >= req else 'FAIL'
    print(f"{status:5s} {r:5.2f}:1 {name}")
