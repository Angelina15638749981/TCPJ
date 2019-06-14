import urllib

import requests
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
import datetime
import time
from lxml import etree
from pymongo import MongoClient

nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

headers_ = {

    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
# response = requests.get(" https://www.tcpjw.com/OrderList/TradingCenter?pageIdx_client=%s&pt_bid=%s "%(p_num, bid),
#                                          headers=headers)
data = {
    "pt_tradestatus": "00",
    "pt_bid": "8",

}
response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=8", headers=headers_)
print(response.status_code)
print(response.text)
# 判断请求状态 切换I
print("----------------------请求成功-----------------------------------------------------------------")

