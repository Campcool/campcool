#!/usr/bin/env python3
"""CX40 冰箱照處理：用戶提供的規格圖（800x800）裁留主圖+尺寸標註，去底部規格表。

輸出覆蓋 assets/addon-fridge-c40.webp（320x320 白底 webp）。
"""
from PIL import Image

src = Image.open("/home/ubuntu/upload/1000033496.avif").convert("RGB")
w, h = src.size  # 800x800

# 主圖 + CX40 標籤 + 尺寸標註約在 y 0-560（比例 0.70），規格表自 y≈585 起
crop = src.crop((0, 0, w, int(h * 0.71)))
canvas = Image.new("RGB", (320, 320), (255, 255, 255))
scale = min(310 / crop.width, 310 / crop.height)
small = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.LANCZOS)
canvas.paste(small, ((320 - small.width) // 2, (320 - small.height) // 2))
canvas.save("/home/ubuntu/audit/campcool/assets/addon-fridge-c40.webp", "WEBP", quality=82)
print("OK addon-fridge-c40.webp", crop.size, "->", canvas.size)
