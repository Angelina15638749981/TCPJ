# 商票数据处理
# !/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import re
from lxml import etree
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time
import datetime

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
    'X-Requested-With': 'XMLHttpRequest'
}

request_header_ = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh - CN, zh;q = 0.9",
    "Connection": "keep-alive",
    "cookie": cookie,
    "Host": "www.qichacha.com",
    "Referer": "https://www.qichacha.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}
link = "https://www.qichacha.com/#area"
# 获得网页信息
response = requests.get(link, headers=request_header, )
# print(response.status_code)
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
    response_by_province_addr_link = requests.get(full_province_addr_link, headers=request_header_, )
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
    response = requests.get(full_province_link, headers=request_header, )
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
                full_page_link = "https://www.qichacha.com/gongsi_area.html?prov=" + province_breif_name + "&" + "city=" + city_breif_name + "&" + "p=" + str(
                    p)
                print("----%s省------%s地区-------------第%s页---------------公司信息--------" % (
                province_breif_name, city_breif_name, p))
                print(full_page_link)
                # 获取公司链接
                # 进入每一页，获取公司链接和公司详细信息
                response_by_page_link = requests.get(full_page_link, headers=request_header_, )

                response_by_page_link.encoding = "utf-8"
                Html = response_by_page_link.text
                html_page = etree.HTML(Html)
                time.sleep(3)

                for y in range(1, 11):
                    print("------------------------------第%s个企业--------------------" % y)
                    company_link = html_page.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
                    full_company_link = "https://www.qichacha.com" + company_link
                    print(full_company_link)
                    # 获取公司链接和公司详细信息
                    response_by_company_link = requests.get(full_company_link, headers=request_header, )

                    response_by_company_link.encoding = "utf-8"

                    Html = response_by_company_link.text
                    html = etree.HTML(Html)

                    try:
                        # 根据风险扫描来判断 页面内容，在进行抓取
                        judgement_basis = html.xpath('//*[@id="base_title"]/h2/text()')[0]
                        if judgement_basis:
                            print(judgement_basis)
                            print(
                                "----------------------------------------属于第二种页面---------------信息丰富--------------------------------------------")

                    except IndexError as e:
                        # print(e)
                        # 详细信息
                        # 基本信息
                        # 公司名字
                        print(
                            "------------------------------------------第一种页面-------------------------信息较少------------------------------------------")
                        company_name = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[1]/h1')[0].text.replace(
                            '\n', '').replace('\t', '').replace(' ', '')

                        # 电话
                        phone_number = html.xpath('//*[@id="company-top"]//div[2]/div[3]/div[1]/span[1]/span[2]')[
                            0].text.replace('\n', '').replace('\t', '').replace(' ', '')

                        # 官网
                        official_website = html.xpath('//*[@id="company-top"]//div[2]/div[3]/div[1]/span[3]')[
                            0].text.replace('\n', '').replace('\t', '').replace(' ', '')

                        # 邮箱
                        email_addree = html.xpath('//*[@id="company-top"]//div[2]/div[3]/div[2]/span[1]/span[2]')[
                            0].text.replace('\n', '').replace('\t', '').replace(' ', '')

                        # 工商信息
                        # 经营者  有问题
                        person = html.xpath('//*[@id="Cominfo"]/table/td[1]')[0].text.replace('\n', '').replace('\t',
                                                                                                                '').replace(
                            ' ', '')
                        # 经营状态
                        running_state = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[2]')[0].text.replace('\n',
                                                                                                           '').replace(
                            '\t', '').replace(' ', '')
                        # 成立日期
                        starting_time = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[4]')[0].text.replace('\n',
                                                                                                           '').replace(
                            '\t', '').replace(' ', '')
                        # 注册号
                        register_number = html.xpath('//*[@id="Cominfo"]/table/tr[4]/td[2]')[0].text.replace('\n',
                                                                                                             '').replace(
                            '\t', '').replace(' ', '')
                        # 企业类型
                        company_type = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[2]')[0].text.replace('\n',
                                                                                                          '').replace(
                            '\t', '').replace(' ', '')
                        # 所属行业
                        belong_to = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[4]')[0].text.replace('\n',
                                                                                                       '').replace('\t',
                                                                                                                   '').replace(
                            ' ', '')

                        # 核准日期
                        check_date = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[2]')[0].text.replace('\n',
                                                                                                        '').replace(
                            '\t', '').replace(' ', '')
                        # 登记机关
                        register_institute = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[4]')[0].text.replace('\n',
                                                                                                                '').replace(
                            '\t', '').replace(' ', '')
                        # 所属地区
                        belong_to_area = html.xpath('//*[@id="Cominfo"]/table/tr[7]/td[2]')[0].text.replace('\n',
                                                                                                            '').replace(
                            '\t', '').replace(' ', '')
                        # 营业期限
                        running_date_limition = html.xpath('//*[@id="Cominfo"]/table/tr[9]/td[4]')[0].text.replace('\n',
                                                                                                                   '').replace(
                            '\t', '').replace(' ', '')
                        # 企业地址
                        company_addr = html.xpath('//*[@id="Cominfo"]/table/tr[10]/td[2]')[0].text.replace('\n',
                                                                                                           '').replace(
                            '\t', '').replace(' ', '')
                        # 经营范围
                        running_state = html.xpath('//*[@id="Cominfo"]/table/tr[11]/td[2]')[0].text.replace('\n',
                                                                                                            '').replace(
                            '\t', '').replace(' ', '')

                        # 变更记录
                        # 序号一
                        # 变更日期
                        # running_date_limition = html.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
                        # print(person)
                        # # 变更项目
                        # company_addr = html.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
                        # print(person)
                        # # 变更前
                        # running_state = html.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
                        # print(person)
                        # # 序号二
                        # # 变更日期
                        # running_date_limition = html.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
                        # print(person)
                        # # 变更项目
                        # company_addr = html.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
                        # print(person)
                        # # 变更前
                        # running_state = html.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]

                        print("公司名字： %s" % company_name)
                        print("电话： %s" % phone_number)
                        print("官网： %s" % official_website)
                        print("邮箱： %s" % email_addree)
                        print("经营者： %s" % person)
                        print("经营状态： %s" % running_state)
                        print("成立日期： %s" % starting_time)
                        print("注册号： %s" % register_number)
                        print("企业类型： %s" % company_type)
                        print("所属行业： %s" % belong_to)
                        print("核准日期： %s" % check_date)
                        print("登记机关： %s" % register_institute)
                        print("所属地区： %s" % belong_to_area)
                        print("营业期限： %s" % running_date_limition)
                        print("企业地址： %s" % company_addr)
                        print("经营范围： %s" % running_state)

                        # 向集合同城票据中插入一条文档
                        data_ = [{"company_name": company_name,
                                  " phone_number": phone_number,
                                  'official_website': official_website,
                                  'email_addree': email_addree,
                                  'person': person,
                                  'running_state': running_state,
                                  'starting_time': starting_time,
                                  'register_number': register_number,
                                  'company_type': company_type,
                                  'belong_to': belong_to,
                                  "check_date": check_date,
                                  'register_institute': register_institute,
                                  "belong_to_area": belong_to_area,
                                  'running_date_limition': running_date_limition,
                                  "company_addr": company_addr,
                                  'running_state': running_state,
                                  }]

                        # for item in data_:
                        #     col.insert_one(item)



