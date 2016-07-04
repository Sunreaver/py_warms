# -*- coding: UTF-8 -*-

# import github.sunreaver.py_tools.Network.HttpClient as Network
import re
import base64
import time
import os
import github.sunreaver.py_tools.system as sys
from jinja2 import Template
import requests

ShadowsocksX_gfwlist_js = "/Users/theone/.ShadowsocksX/gfwlist.js"


def getNetworkGfwlist():
    # c = Network.HttpsClient(host)
    # read = c.Get(url)
    rsp = requests.get(
        "https://github.com/gfwlist/gfwlist/blob/master/gfwlist.txt")
    if rsp.status_code != requests.codes.ok:
        return []
    searchStr = r'<td id="LC[0-9]+" class="blob-code blob-code-inner js-file-line">(.*?)</td>'
    read = rsp.text
    # match = re.findall(searchStr, read.decode("utf-8"))
    match = re.findall(searchStr, read)
    gfw = base64.b64decode("".join(match)).decode("utf-8").split("\n")
    result = []
    for item in gfw:
        if item.startswith("!") or item.startswith("[") or len(item) == 0:
            continue
        r = item.replace("\\", "\\\\")
        r = r.replace("/", "\\/")
        result.append(r)
    return result


def makeJsFile(gfwlist=""):
    template = None
    with open(os.getcwd() + sys.SystemSpe() + "gfwlist.tmpl") as tmplFile:
        template = Template(tmplFile.read())
    out = template.render(List=gfwlist, Date=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), Code="Py")
    fileName = os.getcwd() + sys.SystemSpe() + \
        time.strftime("%Y_%m_%d_%H_%M_%S.js", time.localtime())
    with open(fileName, "w") as fo:
        fo.write(out)
    return fileName


gfwlist = getNetworkGfwlist()
print(len(gfwlist))
fileName = ""
if len(gfwlist) > 0:
    fileName = makeJsFile(gfwlist)
    print("OK:", fileName)
else:
    print("faile")

try:
    os.replace(fileName, ShadowsocksX_gfwlist_js)
except Exception as e:
    print("Copy Err:", e)
else:
    print("Copy OK")
