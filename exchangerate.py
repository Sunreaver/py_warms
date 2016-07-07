# -*- coding: UTF-8 -*-

import requests
import re
import pymongo

m = requests.get("http://fx.cmbchina.com/hq/")
if m.status_code != requests.codes.ok:
    print("抓取失败:", m.status_code)
    exit(0)

reg = re.compile(r"""
<tr>\s*<td\s+class="fontbold">\s*(?P<name>\S+)\s*</td>\s*
<td\s+align="center">\s*(?P<init>\d+)\s*</td>\s*
<td\s+align="center"\s+class="fontbold">\s*(?P<base>\S+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<midPrice>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<sellPrice>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<buyPrice1>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<buyPrice2>\d+\.\d+)\s*</td>\s*
<td\s*class="numberright">\s*(?P<buyPrice3>\d+\.\d+)\s*</td>\s*
<td\s*align="center">\s*(?P<time>\d+:\d+:\d+)\s*</td>\s*
""", re.MULTILINE | re.X)

rows = reg.findall(m.text)

rate = None
connection = None
try:
    connection = pymongo.MongoClient("localhost", 27017)
    connection.Stocks.authenticate("stocks", "1111", timeout=10)
    dbcl = connection.Stocks.rate
except Exception as e:
    print("mongo err:", e)
    exit(0)

dic = [{}]
for v in rows:
    dic.append({
               'name': v[0],
               'init': v[1],
               'base': v[2],
               'midPrice': v[3],
               'sellPrice': v[4],
               'time': v[8]
               })

if len(dic) > 0:
    try:
        rate.insert(dic)
    except Exception as e:
        print("mongo insert err:", e)
        raise Exception('MongoInsertErr')
    finally:
        print("OK at:", dic[0]['time'])
connection.close()
