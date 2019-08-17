import requests
import time
import json
from lxml import etree
import re
from pymongo import MongoClient
import random
import datetime
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
import datetime
import sys
import time
import hashlib
import requests
requests.packages.urllib3.disable_warnings()


nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在


# 代码冗余问题
# def get_data_from_tcpj(pt_tradestatus, pt_bid, pageIdx_client):
# #     headers = {
# #         # "accept": "*/*",
# #         # "accept-encoding": "gzip, deflate, br",
# #         # "accept-language": "zh - CN, zh;q = 0.9",
# #         # "content-length": "307",
# #         # "content - type": "application/x-www-form-urlencoded",
# #         # "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7faa415597160258384479eca57a735df4a746d72874024353c894a; NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==",
# #         # "origin": "https://www.tcpjw.com",
# #         # "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
# #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
# #         # 'X-Requested-With': 'XMLHttpRequest'
# #     }
# #
# #     data = {
# #         # 待结单
# #         # "pt_tradestatus": "00",
# #         # 交易完成
# #         "pt_tradestatus": "%s" % pt_tradestatus,
# #         "pt_bid": "%s" % pt_bid,
# #         "pageIdx_client": "%s" % pageIdx_client,
# #         "X-Requested-With": "XMLHttpRequest",
# #
# #     }
# #
# #     print("-----------------------------------------------------------------------------------")
# #     response = requests.get("http://120.79.14.150:8888/index.html#",headers=headers, verify=False)
# #
# #     # response = requests.post("http://120.79.14.150:8888/index.html#",headers=headers, data=data, verify=False)
# #     print(response.status_code)
# #     # if pt_tradestatus=="22":
# #     #     print(response.text)
# #     # 判断请求状态 切换I
# #     print("----------------------请求成功-----------------------------------------------------------------")
# #     # time.sleep(random.random() * 3)
# #     response.encoding = "utf-8"
# #     Html = response.text
# #     html = etree.HTML(Html)


headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "origin": "http://120.79.14.150:8888",
            "referer": "http://120.79.14.150:8888/tickerHtml/credit-new.html",
            "token": "3b53170a0a1a31003413035d4e484b417547555356465258770e120c070e110524535941564d51406048515356181d142f040d1745454000300d074f465b03",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    }
response = requests.get("http://120.79.14.150:9901/cdk/priceRelation/doBankList?pageNum=1&pageSize=10&companyId=1&paperTypeId=6&bankTypeId=1&type=0&searchContent=", verify=False)

# response = requests.post("http://120.79.14.150:8888/index.html#",headers=headers, data=data, verify=False)
print(response.status_code)
print(response.text)





























