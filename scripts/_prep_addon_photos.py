#!/usr/bin/env python3
"""其它小物商品照處理：裁行銷字 -> 置中方形補白 -> 320x320 webp。
用法：python3 scripts/_prep_addon_photos.py
"""
from PIL import Image
import os

SRC = "/home/ubuntu/upload/search_images"
DST = "/home/ubuntu/audit/campcool/assets"
SIZE = 320
Q = 82

def crop_marketing_box(img, box=None):
    """box = (left, top, right, bottom) 比例，None 則不裁"""
    if box:
        w, h = img.size
        img = img.crop((int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h)))
    return img

def to_square_webp(img, out):
    # 置中補白到正方形
    w, h = img.size
    side = max(w, h)
    canvas = Image.new("RGB", (side, side), (255, 255, 255))
    canvas.paste(img, ((side - w) // 2, (side - h) // 2))
    canvas = canvas.resize((SIZE, SIZE), Image.LANCZOS)
    canvas.save(out, "WEBP", quality=Q, method=6)
    kb = os.path.getsize(out) // 1024
    print(f"OK {out} ({SIZE}x{SIZE}, {kb}KB)")

jobs = [
    # (src, out, marketing_crop_box)
    (f"{SRC}/5WlyZSBh6Tgu.jpeg",   "addon-ext-cord-5m.webp",   None),
    (f"{SRC}/ZdfWBuLoB6oa.jpg",    "addon-ext-cord-10m.webp",  (0.02, 0.345, 0.515, 0.825)),  # 軍綠線盤主體
    (f"{SRC}/kKRBEQXk9BL3.jpg",    "addon-lamp-5m.webp",       None),
    (f"{SRC}/062bvymWmlZE.jpg",    "addon-lamp-10m.webp",      (0.0, 0.0, 1.0, 0.72)),  # 裁底部 28%（移除「客廳帳使用 12米燈條」標籤）
    (f"{SRC}/8XDRok0sMKBA.jpg",    "addon-ice-maker.webp",     None),
    (f"{SRC}/GHqlAnRij6jC.jpg",    "addon-fan.webp",           None),
]

for src, out, box in jobs:
    img = Image.open(src).convert("RGB")
    img = crop_marketing_box(img, box)
    to_square_webp(img, os.path.join(DST, out))

print("done")
