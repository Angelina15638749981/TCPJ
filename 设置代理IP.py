import requests
import sys
import time
import hashlib
import logging
import json
# -*- coding: UTF-8 –*-
import requests
requests.packages.urllib3.disable_warnings()
headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "content-length": "310",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=24f9419915668933329793630e96aed17e47a82d7338cc5dc1becd5c78; ASP.NET_SessionId=egmo0ba3q4tr2j11fjcglm5v; acw_sc__v2=5d68e4403da2bed01d2ac7b4f8bfd4c4495ddcb8; acw_sc__v3=5d68e446882a46d054e03aa724b36d3c7fdbe8f3; NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'x-requested-with': 'XMLHttpRequest',
        # "Proxy-Authorization": auth
    }

data = {
    # 待结单
    # "pt_tradestatus": "00",
    # 交易完成
    # "00", "1", pageIdx_client_gg_jiedan
    "pt_tradestatus": "00",
    "pt_bid": "1",
    "pageIdx_client": "1" ,
    "X-Requested-With": "XMLHttpRequest",

}

proxy_server = '183.129.244.16'


# { “code”: 100, “left_ip”: 4914, “left_time”: 1876270, “number”: 2, “domain”: “ip.feiyiproxy.com”, “port”: [ 14343, 14344 ] }
api_url = "http://183.129.244.16:88/open?user_name=syf11140725ap2&timestamp=1567148049&md5=887BB8E7A0BB9B392C7685BACED412F2&pattern=json&number=1"
res = requests.get(api_url)
result = str(res.content, encoding='utf8')
json_obj = json.loads(result)
print(json_obj)
auth_port = json_obj["port"][0]
left_time_start = json_obj["left_time"]
# 2590506
# 2590396
# 2590338
# 2590021
print(left_time_start)
proxies = {'http': "http://" + proxy_server + ':' + str(auth_port),
           'https': 'http://' + proxy_server + ':' + str(auth_port), }
time.sleep(3)
from lxml import etree

while True:
#     print(int(left_time_start)-int(json_obj["left_time"]))
#     if int(left_time_start)-int(json_obj["left_time"]) >= 180:
    s = requests.Session()
    s.proxies.update(proxies)
    print(proxies)
    ret = s.post("https://www.tcpjw.com/OrderList/TradingCenter", headers=headers, data=data, verify=False, timeout=5)
    print(ret.status_code)
    ret.encoding = "utf-8"
    Html = ret.text
    print(Html)
    # if "html" in Html:
        # print(Html)

    # html = etree.HTML(Html)
    # item_time = html.xpath('//tr[1]]/td[1]')
    # print(item_time)



