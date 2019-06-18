import json
import urllib

import requests
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
import datetime
import time
from lxml import etree
from pymongo import MongoClient
import random
import re

# 实例化 UserAgent 类
ua = UserAgent()
user_agents = ua.random
headers = {
        "User-Agent": user_agents}


nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在





def get_guogu_data():
    headers = {
                "accept": "text/plain, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh - CN, zh;q = 0.9",
                "content-length": "44",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cookie": "_uab_collina = 155710764840181703453248;acw_tc = 77a7faa415597160258384479eca57a735df4a746d72874024353c894a;ASP.NET_SessionId = een0mox0bwn2kkfynkqlnibo",
                 "origin": "https://chat.im.alisoft.com",
                "referer": "https://chat.im.alisoft.com/proxy.htm?prefix=i30lbn9h&uid=i30lbn9h1817&toPrefix=i30lbn9h&ver=4.0.1&accessToken=khy1b5xlwh6rro9f&lpath=yw",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
                'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        # 待结单
        # "pt_tradestatus": "00",
        # 交易完成
        "at": "khy1b5xlwh6rro9f",
        "uid": "i30lbn9h1817",
        "msgId": "0",



    }

    # payloadData = {
    #     "login":{"userid": 1817,
    #                       "username": "18625558886",
    #                       "sessionKey": "UVZ5R0Z2NDM3VnRwbGtMc2NINFZQU2FsM0ozT1BVVjNZMGJ0aXBDNnRpSFZvRU9GYVpKY3VBdTd2TUl4VmFMdFRaOE9MTkY2d21vN0ljOWVXTnF1YVRveFdEMDVEUGNEL2EwYXk0ZmVlQldNbTRXbEZUNFRjdGlTM1ROUzliRDM=",
    #                         "hash": 0.8502833436194395
    #                       }
    #
    # }

    response = requests.post("https://www.jinbill.com/login/plogin.html",headers=headers, data=data,verify=False)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':

    get_guogu_data()

