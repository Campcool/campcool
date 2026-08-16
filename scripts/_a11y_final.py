# 線上驗證：跑 _a11y_scan.py 並彙總到 /tmp/a11y_report5.json
import asyncio, importlib.util, json, sys
from collections import Counter

spec = importlib.util.spec_from_file_location('scan', '/home/ubuntu/audit/campcool/scripts/_a11y_scan.py')
# 直接 exec 避免 module 副作用
src = open('/home/ubuntu/audit/campcool/scripts/_a11y_scan.py').read()
src = src.replace("'/tmp/a11y_report2.json'", "'/tmp/a11y_report5.json'")
exec(compile(src, 'a11y_scan', 'exec'))
