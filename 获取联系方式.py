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
import os
import time
import hashlib
import requests
from selenium import webdriver
import asyncio
import time, random
import requests
from selenium import webdriver
import requests
import os, time, random
requests.packages.urllib3.disable_warnings()
import urllib.request
import cv2
import numpy as np
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = 'D:/softwares/tesseract/tesseract.exe'
import urllib.request
import time
from 抢单 import main

# 时间
nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

def fetch_company():
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q =0.9",
        "content-length": "309",
        "content - type": "application/x-www-form-urlencoded",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7fa9915676518330222517ec49a8abacc9709a8c9a7581c5a9a1716; ASP.NET_SessionId=zpzwd4wpuemwr15rlchsyamh; NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiylA9PZJ9IDe4wOFHOMNXlVzQUKfdV5u+ZuR3xRTWH0p9BELN+Xz4J6+EMZT/2KDCPS2zoiFsGuqQOjXaayxLIMqRgpNYKYyoYgJ7LbXi70U4xygYSCqZgPodjKP0aRQpkR557HG5qzHb2FmBJ4rqMAcclI16qWp5UKv+w+v0YNRWfMCxmSD4k4FsQuFMBTukx/y0VCKkx2n8dDf7QvGIvNg/0um9Noy2hFJOxWGLQRvND/3H9nFjIDAf0E/FNM+9o",
        # "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7faa415597160258384479eca57a735df4a746d72874024353c894a; NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiya39OHdOgT5G1vHfmqDd6KAsR8s0OUV/thXejTQ/RJWjKGBbD3mOmVSbZ2JjHtArsX4ceeif6sxRyEr3tAVGfype4oLBq89Beavs9rNM/6NASpPxBXhd8D3m8EqNkML4piXLOwtUpH7SmtMplSwiMjxQsbBn9q/vfBLzhYoLz3vd5UuNca1WqhKkJ++rmXUZdLU3wt748v0YrBTMHSCkPymSrRkp12OEJ7OXVQh2S6zwVeqspNpPT/kwdeX5SHaL6",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest'
    }


    for page in range(2115, 7056):
        print("-----------------------第%s页-------------------" % page)
        response = requests.get("https://www.dlzb.com/charts/?page=%s" % page,
                                 verify=False)
        print(response.status_code)
        response.encoding = "utf-8"
        Html = response.text
        html = etree.HTML(Html)
        for i in range(2, 22):
            with open('companies_2.txt', 'a+',encoding='utf-8') as f:

                company_name = html.xpath('//div[10]//tr[%s]/td[1]/a' % i)[0]
                print(company_name.text)
                # get_phone_number_by_company(company_name.text)
                f.write(company_name.text+"\n")



def get_phone_number_by_company(chinaCompan):
    # 转化为机器可以识别带中文的网址，编码类型为unicode。只转换汉字部分，不能全部网址进行转换
    compan_y = urllib.parse.quote(chinaCompan)
    testUr_l = "https://www.qichacha.com/search?key=" + compan_y


    # 模拟登录
    request_header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh - CN, zh;q = 0.9",
        "Connection": "keep-alive",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=24f9419915668933329793630e96aed17e47a82d7338cc5dc1becd5c78; acw_sc__v2=5d6f6af92f373a0789dcfafaed3d388bbb2c2765; acw_sc__v3=5d6f6afed25ff6270f2cd4b709fc81fd4998318b; NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==",
        "Referer": "https://www.qichacha.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.get(testUr_l, headers=request_header, )
    # print(response.status_code)
    response.encoding = "utf-8"
    Html = response.text
    print(Html)
    html = etree.HTML(Html)
    # print(html) //*[@id="search-result"]/tr[1]/td[3]/p[2]/span/text()
    phone_num = html.xpath('//*[@id="search-result"]/tr[1]/td[3]/p[2]/span/text()')[0]
    # print(phone_num)


if __name__ == '__main__':

    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库 https://github.com/Angelina15638749981/TCPJ.git
    db = client.bank
    col = db.data
    fetch_company()













