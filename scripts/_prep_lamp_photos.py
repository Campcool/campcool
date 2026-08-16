#!/usr/bin/env python3
"""逐露天下（逐浪天下）燈條商品照處理：覆蓋 assets/addon-lamp-5m/10m.webp。

- 5M：RHl9wNOh1mUj.webp（momo 官方 640×640）裁左半乾淨燈條特寫
- 10M：7eTMrqAzpdZA.jpg（官方 800×800 帳篷實景）裁掉頂部「全台最亮」黃標
處理：裁主體 → 置中縮放 300px 內 → 320×320 白底 webp。
"""
from PIL import Image

SRC = "/home/ubuntu/upload/search_images"
OUT_DIR = "/home/ubuntu/audit/campcool/assets"

jobs = [
    # 5M：左半直條燈條特寫（0.00-0.34 寬、0.12-0.88 高）
    (f"{SRC}/RHl9wNOh1mUj.webp", "addon-lamp-5m.webp",  (0.00, 0.31, 0.34, 0.88)),
    # 10M：帳篷實景裁掉頂部黃標（0.0-1.0 寬、0.30-1.0 高）
    (f"{SRC}/7eTMrqAzpdZA.jpg",  "addon-lamp-10m.webp", (0.00, 0.30, 1.00, 1.00)),
]

for src, out, box in jobs:
    img = Image.open(src).convert("RGB")
    w, h = img.size
    l, t, r, b = box
    crop = img.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
    canvas = Image.new("RGB", (320, 320), (255, 255, 255))
    scale = min(300 / crop.width, 300 / crop.height)
    small = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.LANCZOS)
    canvas.paste(small, ((320 - small.width) // 2, (320 - small.height) // 2))
    canvas.save(f"{OUT_DIR}/{out}", "WEBP", quality=80)
    print(f"OK {OUT_DIR}/{out} (crop {crop.size})")

print("done")
