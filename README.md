# Campcool 露涼社 — Website UI Kit

## Overview
High-fidelity recreation of the campcool.tw mobile website.  
Built with React (JSX via Babel). Source: `Campcool/campcool` repo.

## Product
Single mobile-first website with 4 sections (tabs):
- **租借資訊** — AC rental info, pricing, locations
- **知識百科** — Equipment specs, usage guides
- **預約須知** — Booking policy, cancellation terms
- **冰箱租借** — Portable fridge rental

## Components
| File | Description |
|---|---|
| `Header.jsx` | Sticky top header with logo |
| `BottomNav.jsx` | 4-tab fixed bottom navigation |
| `HeroSection.jsx` | Page hero banner (gradient bg) |
| `ProductCard.jsx` | AC/Fridge spec card |
| `NoticeCard.jsx` | Color-coded notice/alert card |
| `PricingTable.jsx` | Rental pricing display |
| `AlertBanner.jsx` | Info/warning/danger alert banners |
| `LineBanner.jsx` | LINE CTA banner |

## Usage
Open `index.html` for the full interactive prototype.
Components are exported to `window` and can be used standalone.

## Design Constraints
- Mobile-first (375px target width)
- System font stack — no custom fonts
- Tailwind CSS v4 color tokens (see `colors_and_type.css`)
