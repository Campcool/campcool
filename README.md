# Campcool 露涼社 — Website

## Overview
Production website for campcool.tw — 露營冷氣・移動冰箱出租 (camping AC / portable
fridge rental), serving 新竹・竹北・台北・新北・台中.

Mobile-first, deployed via GitHub Pages (`CNAME` → campcool.tw).

AI agents and automated maintainers should read [`AI-README.md`](AI-README.md)
before changing booking privacy, LINE tracking, pickup policy, motion, or social
share metadata.

## Pages
| File | Description |
|---|---|
| `index.html` | Main site — **static HTML + vanilla JS and shared assets/site-redesign.css** (no build step, no runtime framework). Four tabbed sections with `#hash` deep-linking. |
| `btu-guide.html` | Standalone BTU 選購指南 article — static, optimized for LINE/FB share previews. |
| Product, rental, region, FAQ and review pages | Share the same brand header, reading styles and navigation. `areas/new-taipei.html` is content; the other three area aliases retain redirects. |

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
  JUZ-400 = 5100 BTU / 425W / 13kg; SAC688 = 6300 BTU / 530W / 17kg.
- The booking form only composes and copies a LINE message in the visitor's
  browser. It does not upload contact details to Campcool; the customer must
  confirm and send the message in LINE before Campcool receives it.
- LINE click tracking fires a GA4 `line_click` event. Buttons that actually open
  LINE also send a Google Ads conversion when `ADS_CONVERSION_LABEL` is set.
- Design: warm white and forest green; desktop content up to 1160px, articles
  up to 960px, fixed 20px root font. Desktop top navigation and mobile bottom
  navigation share tab state. See [DESIGN.md](DESIGN.md).
- Decorative CTA shimmer is disabled. Reduced-motion users receive instant
  scrolling and no interface animations.
- Checks: `node scripts/validate-site.mjs`, the same command with `--selftest`,
  `python3 scripts/e2e-test.py`, and `python3 scripts/redesign-e2e.py`.
  Browser tests require Playwright and Chromium. The redesign test covers
  15 content pages, four widths, navigation, equipment and plan carry-over,
  local-only booking privacy and header LINE tracking.
  CI uploads screenshots and layout measurements as an Actions artifact;
  all checks must pass before Pages deploys. Internal docs, scripts and
  `work/` are excluded from the public Pages artifact.
