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



# headers = {
#             "accept": "application/json, text/javascript, */*; q=0.01",
#             "origin": "http://120.79.14.150:8888",
#             "referer": "http://120.79.14.150:8888/tickerHtml/credit-new.html",
#             "token": "3b53170a0a1a31003413035d4e484b417547555356465258770e120c070e110524535941564d51406048515356181d142f040d1745454000300d074f465b03",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
#     }
response = requests.get("https://www.weiyoubot.cn/mainpage.html?action=complaint&gid=5d56494202152224d413d663", verify=False)

print(response.status_code)
print(response.content)





























