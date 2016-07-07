# -*- coding: UTF-8 -*-

import requests
import re

m = requests.get("http://fx.cmbchina.com/hq/")
if m.status_code != requests.codes.ok:
    print("抓取失败:", m.status_code)
    exit(0)

reg = re.compile(r"""
<tr>\s*<td\s+class="fontbold">\s*(?P<name>\S+)\s*</td>\s*
<td\s+align="center">\s*\d+\s*</td>\s*
<td\s+align="center"\s+class="fontbold">\s*(?P<base>\S+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<midPrice>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<sellPrice>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<buyPrice1>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<buyPrice2>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<buyPrice3>\d+\.\d+)\s*</td>\s*
<td\s*align="center">\s*(?P<time>\d+:\d+:\d+)\s*</td>\s*
""", re.MULTILINE | re.X)

rows = reg.findall(m.text)

for v in rows:
    print(v)
