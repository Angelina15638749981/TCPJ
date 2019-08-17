# 商票数据处理
# !/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import re
from lxml import etree
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()
import time
import datetime
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
user_agent=ua.random
# 创建连接对象
client = MongoClient(host='localhost', port=27017)
# 获得数据库，此处使用 data
db = client.companies
col = db.data
# 时间
nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

# 获取更新的cookie
with open(r'%s_cookie.txt' % nowTime, 'r') as f:
    cookie = f.readline()
    print(cookie)

# 模拟登录
request_header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh - CN, zh;q = 0.9",
    "Connection": "keep-alive",
    "cookie": cookie,
    "Host": "www.qichacha.com",
    "Referer": "https://www.qichacha.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    # "User-Agent": user_agent,
    'X-Requested-With': 'XMLHttpRequest'
}

request_header_ = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN",
    "Connection": "keep-alive",
    "cookie": cookie,
    "Host": "www.qichacha.com",
    "Referer": "https://www.qichacha.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",

    # "User-Agent": user_agent,
    'X-Requested-With': 'XMLHttpRequest'
}
link = "https://www.qichacha.com/#area"
# 获得网页信息
response = requests.get(link, headers=request_header,verify=False )
print(response.status_code)

# print(response.text)
response.encoding = "utf-8"
Html = response.text
html_area = etree.HTML(Html)

# 获取省份链接和对应的市级链接
for i in range(1, 2):
    # 获取省级 地址链接
    province_addr_link = html_area.xpath('//*[@id="area"]//div[1]/div[%s]/a/@href' % i)[0]
    # /g_BJ
    if len(province_addr_link) == 5:
        addr_ = province_addr_link[-2:]
    else:
        addr_ = province_addr_link[-2:]
    # https://www.qichacha.com/g_BJ
    full_province_addr_link = "https://www.qichacha.com" + province_addr_link
    # 请求上边的链接
    response_by_province_addr_link = requests.get(full_province_addr_link, headers=request_header_,verify=False)
    # print(response_by_province_addr_link.text)
    response_by_province_addr_link.encoding = "utf-8"
    Html = response_by_province_addr_link.text
    html_province = etree.HTML(Html)

    soup = BeautifulSoup(response_by_province_addr_link.text, 'html.parser')
    list = soup.findAll(class_='pills-item')
    # print(list) 0-31 provinces  32-end districts
    # /html/body/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/a[31]  Z - 浙江
    province_ls = []
    for x in range(len(list)):
        text = list[x]
        soup2 = BeautifulSoup(str(text), 'lxml')
        link_ = soup2.find('a').attrs['href']
        if "110" not in link_:
            # print(link_)
            province_ls.append(link_)



for province in province_ls:
    if len(province) == 10:
        province_breif_name = province[3:5]
    elif len(province) == 11:
        province_breif_name = province[3:6]
    elif len(province) == 12:
        province_breif_name = province[3:7]
    full_province_link = "https://www.qichacha.com" + province
    # print(full_province_link)
    # print("--------------------------------------%s------------------------------------" % province)
    # 获取市级link
    response = requests.get(full_province_link, headers=request_header,verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    list = soup.findAll(class_='pills-item')
    # print(list) 0-31 provinces  32-end districts
    # /html/body/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/a[31]  Z - 浙江
    city_ls = []
    for y in range(len(list)):
        text = list[y]
        soup2 = BeautifulSoup(str(text), 'lxml')
        link_city = soup2.find('a').attrs['href']
        if len(link_city) > 12:
            city_breif_name = link_city[-11:-5]
            # city_ls.append(link_city)

            for p in range(1, 501):
                # https://www.qichacha.com/gongsi_area.html?prov=AH&city=340100&p=1
                full_page_link = "https://www.qichacha.com/gongsi_area.html?prov="+province_breif_name+"&"+"city="+city_breif_name+"&"+"p="+str(p)
                print("----%s省------%s地区-------------第%s页---------------公司信息--------" % (province_breif_name, city_breif_name,p))
                print(full_page_link)
                # 获取公司链接
                # 进入每一页，获取公司链接和公司详细信息
                response_by_page_link = requests.get(full_page_link, headers=request_header_, verify=False )

                response_by_page_link.encoding = "utf-8"
                Html = response_by_page_link.text
                html_page = etree.HTML(Html)
                time.sleep(3)

                for y in range(1, 11):
                    print("------------------------------第%s个企业--------------------" % y )
                    company_link = html_page.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
                    full_company_link = "https://www.qichacha.com" + company_link
                    # print(full_company_link)
                    # 获取公司链接和公司详细信息
                    response_by_company_link = requests.get(full_company_link, headers=request_header,verify=False )
                    soup_comp = BeautifulSoup(response_by_company_link.text, 'xml')
                    # soup_comp.find_all(class_="content")
                    # 基本信息获取
                    # if
                    # print(soup_comp.find_all(class_="row title"))
                    #       row title jk-tip
                    # print(soup_comp.find_all(class_=" row title jk-tip"))

                    print("-----------------------------------------------------")


                    # 基本信息 h1 
                    company_name = soup_comp.find_all("div", {"class": "content"})[0].find("h1").text
                    print(company_name)
                    # 电话
                    phone_number = soup_comp.find_all("div", {"class": "content"})[0].select('span .cvlu')[0].text
                    print(phone_number)
                    # 官网
                    official_website =soup_comp.find_all("div", {"class": "content"})[0].select('span .cvlu')[1].text
                    print(official_website)

                    # 邮箱
                    email_addree =soup_comp.find_all("div", {"class": "content"})[0].select('span .cvlu')[2].text
                    print(email_addree)

                    # 地址
                    address=soup_comp.find_all("div", {"class": "content"})[0].select('span .cvlu')[2].text
                    print(address)

                    """


                    # 工商信息
                    # 法定代表人
                    person =
                    #注册资本
                    register_asset=
                    # 实缴资本
                    paid_in_capital=
                    # 经营状态
                    running_state =
                    # 成立日期
                    starting_time =
                    # 统一社会信用代码
                    unified_social_credit_code=
                    # 纳税人识别号
                    ditinguish_number=
                    # 注册号
                    register_number =
                    # 组织机构代码
                    organization_code=
                    # 企业类型
                    company_type =
                    # 所属行业
                    belong_to =
                    # 核准日期
                    check_date =
                    # 登记机关
                    register_institute =
                    # 所属地区
                    belong_to_area =
                    # 英文名
                    # English_name=
                    # 曾用名
                    used_name=
                    # 参保人数
                    numbers_of_insurance=
                    # 人员规模
                    staff_size=
                    # 营业期限
                    running_date_limition =
                    # 企业地址
                    company_addr =
                    # 经营范围
                    running_state =



                    #股东信息
                    #股东1及出资信息
                    #
                    # 持股比例
                    #
                    #认缴出资额(万元)
                    #
                    # 认缴出资日期
                    #
                    # 关联产品/机构
                    #

                    # 股东2及出资信息
                    #
                    # 持股比例
                    #
                    # 认缴出资额(万元)
                    #
                    # 认缴出资日期
                    #
                    # 关联产品/机构
                    #



                    # 主要人员
                    # 姓名1
                    #
                    # 职务
                    #
                    # 姓名2
                    #
                    # 职务
                    #
                    # 姓名3
                    #
                    # 职务
                    #
"""

















