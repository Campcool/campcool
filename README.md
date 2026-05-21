# Campcool 露涼社 — Website

## Overview
Production website for campcool.tw — 露營冷氣・移動冰箱出租 (camping AC / portable
fridge rental), serving 新竹・竹北・台北・新北・台中.

Mobile-first, deployed via GitHub Pages (`CNAME` → campcool.tw).

## Pages
| File | Description |
|---|---|
| `index.html` | Main site — **self-contained static HTML/CSS + vanilla JS** (no build step, no runtime framework). Four tabbed sections with `#hash` deep-linking. |
| `btu-guide.html` | Standalone BTU 選購指南 article — static, optimized for LINE/FB share previews. |

### `index.html` tabs
- **租借方案** — AC rental info, pricing, locations, 露友 reviews
- **選購指南** — Equipment specs, BTU knowledge, link to full guide
- **預約方式** — Booking flow, cancellation policy
- **冰箱出租** — Portable fridge models, usage notes

## Reference components (not loaded in production)
The `*.jsx` files are the original React component source, kept for design
reference only. The live `index.html` no longer loads React/Babel — the markup
was inlined as static HTML for performance and SEO (crawler / share-bot readable
without JS).

| File | Component |
|---|---|
| `Header.jsx` | Sticky top header with logo |
| `BottomNav.jsx` | 4-tab fixed bottom navigation |
| `HeroSection.jsx` | Per-tab hero banner (gradient bg) |
| `ProductCard.jsx` | AC/Fridge spec card (+ `NoticeCard`, `AlertBanner`) |
| `PricingTable.jsx` | Rental pricing display (+ `LineBanner`) |

## Local preview
No build needed. Serve the folder and open in a browser:
```
python3 -m http.server 8000   # then visit http://localhost:8000/
```

## Notes
- Product specs (BTU / 重量 / 耗電) must stay consistent between `index.html`
  and `btu-guide.html`. Current values match manufacturer data:
  JUZ-400 = 5100 BTU / 425W / 13kg; SAC688 = 6000 BTU / 530W / 17kg.
- LINE click tracking fires a GA4 `line_click` event. To also send a Google Ads
  conversion, set `ADS_CONVERSION_LABEL` in `index.html`.
- Design: mobile-first (≤680px content width), system font stack, no custom fonts.
