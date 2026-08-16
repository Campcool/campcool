# 把其它小物 section 全長截圖裁成 6 段並拼兩組對照
from PIL import Image

img = Image.open('/tmp/addons_section.png')
w, h = img.size  # 780 x 12210
print('size:', img.size)
seg = 2000
parts = []
for y in range(0, h, seg):
    box = (0, y, w, min(y + seg, h))
    parts.append(img.crop(box))

# 存六段
for i, part in enumerate(parts):
    part.save(f'/tmp/seg_{i}.png')

# 拼前 3 段與後 3 段成兩張對照
def stitch(lst, name):
    w0 = max(p.width for p in lst)
    h0 = sum(p.height for p in lst) + 10 * len(lst)
    out = Image.new('RGB', (w0, h0), 'white')
    yy = 0
    for p in lst:
        out.paste(p, (0, yy)); yy += p.height + 10
    out.save(name)
    return out

stitch(parts[:3], '/tmp/seg_top.png')
stitch(parts[3:], '/tmp/seg_bot.png')
print('done')
