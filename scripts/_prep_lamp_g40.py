#!/usr/bin/env python3
"""燈條共用圖與 G40 圖處理。

燈條共用圖（用戶提供 1024x1024）：裁下半圓盤區避開中央紅字「10米燈條大全配」，
含圓盤下半弧光、網袋、調光開關與右側電源線。
G40 圖（用戶提供 800x800）：裁下半部去橘色廣告字，留圓球泡特寫主體。
輸出均為 320x320 白底 webp。
"""
from PIL import Image

BASE = "/home/ubuntu/audit/campcool/assets"

def to_webp(src_img, out_name):
    canvas = Image.new("RGB", (320, 320), (255, 255, 255))
    scale = min(310 / src_img.width, 310 / src_img.height)
    small = src_img.resize((max(1, int(src_img.width * scale)), max(1, int(src_img.height * scale))), Image.LANCZOS)
    canvas.paste(small, ((320 - small.width) // 2, (320 - small.height) // 2))
    canvas.save(f"{BASE}/{out_name}", "WEBP", quality=82)
    print("OK", out_name, src_img.size, "->", canvas.size)

# 燈條共用圖：裁 (130, 470, 830, 830) 白底圓盤下半+網袋+開關+電源線，無紅字
lamp = Image.open("/tmp/lamp10m_user.png").convert("RGB")
lamp_c = lamp.crop((130, 490, 830, 830))
to_webp(lamp_c, "addon-lamp-5m.webp")

# G40：裁 (10, 260, 790, 640) 圓球泡主體，去底部橘字（橘字自 y≈0.80 起）
g40 = Image.open("/tmp/g40_user.png").convert("RGB")
g40_c = g40.crop((10, 260, 790, 640))
to_webp(g40_c, "addon-lamp-g40.webp")
