from PIL import Image
BASE = "/home/ubuntu/audit/campcool/assets"
a = Image.open(f"{BASE}/addon-lamp-5m.webp").resize((320, 320))
b = Image.open(f"{BASE}/addon-lamp-g40.webp").resize((320, 320))
g = Image.new("RGB", (650, 320), "white")
g.paste(a, (0, 0))
g.paste(b, (330, 0))
g.save("/tmp/lamp_g40_grid.png")
print("grid saved")
