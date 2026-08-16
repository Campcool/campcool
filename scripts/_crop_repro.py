# 裁 zoom1.3 情境截圖中的關鍵卡（延長線 5M、焚火台）局部放大檢視
from PIL import Image
img = Image.open('/tmp/repro_zoom_412_13.png')
w, h = img.size
print('size', img.size)
# 找 5M 延長線卡位置：用 OCR 不可行，直接掃描價格字
# 簡化：整張圖太高（52K），裁三個區段各 3000px 檢查卡片是否超寬
# 用溢出偵測：掃描每列最右邊非背景像素——太複雜，直接裁出三塊拼接
seg = 2500
out = []
for y in range(0, h, seg):
    out.append(img.crop((0, y, w, min(y + seg, h))))
total = sum(i.height for i in out) + 10 * len(out)
canvas = Image.new('RGB', (w, total), 'white')
yy = 0
for i in out:
    canvas.paste(i, (0, yy)); yy += i.height + 10
canvas.save('/tmp/repro_zoom13_segs.png')
print('saved repro_zoom13_segs.png', canvas.size)
