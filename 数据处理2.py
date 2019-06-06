from pymongo import MongoClient
import os, time, random
from PIL import Image
from aip import AipOcr
import cv2
import re
import requests


img_url = "https://api.growingio.com/v2/bf8ca8a31e663811/web/action?stm=1559532615223"
#获取出票人全称    收票人全称
response = requests.get(img_url)
APP_ID = '16340507'
API_KEY = '3BcdhviIZhIq1R0eW3nDO5id'
SECRECT_KEY = 'GQglG2S9KB84wArEgDCxdFMoKElSVEg2'
client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
company_ls = []
message = client.basicAccurate(response.content)
# message = client.basicGeneral(response.content)
print(message)
for j in message.get('words_result')[5:20]:
    # print(j['words'])
    # if re.search("有限公司$", j['words']) or re.search("^[全,称，收]", j['words']):
    if re.search("有限公司$", j['words']) or re.search("^[全]", j['words']) or re.search("^[称]", j['words']):
        company = j['words'].strip("全").strip("称").strip("全称").strip("收全称").strip("出全称")
        company_ls.append(company)
if len(company_ls) >= 2:
    if "公司" or "有限" in company_ls[0] and company_ls[1]:
        company_1 = company_ls[0]
        if company_ls[1] != "":
            company_2 = company_ls[1]
        elif company_ls[2]:
            company_2 = company_ls[2]

    elif "已打码" in company_ls[0] or company_ls[1]:
        company_1 = "无"
        company_2 = "无"
else:
    company_1 = "无"
    company_2 = "无"

print("出票人：%s" % company_1)
print("收票人：%s" % company_2)