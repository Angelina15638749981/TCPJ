# 商票数据处理
# !/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import re
from lxml import etree
from pymongo import MongoClient

import requests
import time
# 创建连接对象
client = MongoClient(host='localhost', port=27017)
# 获得数据库，此处使用 data
db = client.companies
col = db.data

# 模拟登录
request_header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh - CN, zh;q = 0.9",
    "Connection": "keep-alive",
    "cookie": "UM_distinctid=16b1be8a1e2c38-0f9f621b3edc7f-f353163-1fa400-16b1be8a1e3db7; _uab_collina=155954135925730288924133; zg_did=%7B%22did%22%3A%20%2216b1be8a2e6273-01efba2c0573f6-f353163-1fa400-16b1be8a2e7f8f%22%7D; acw_tc=7b060ccf15637589267313508eb99ba33cce3df44cab6b402a51448937; QCCSESSID=4d8bb00vqa4dhem1sn1tq08js2; CNZZDATA1254842228=899027629-1559535992-https%253A%252F%252Fwww.baidu.com%252F%7C1564101597; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1563867602,1563868409,1563931433,1564104705; hasShow=1; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1564105926; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201564104704853%2C%22updated%22%3A%201564105931704%2C%22info%22%3A%201563758923593%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%5C%22%24utm_source%5C%22%3A%20%5C%22baidu%5C%22%2C%5C%22%24utm_medium%5C%22%3A%20%5C%22cpc%5C%22%2C%5C%22%24utm_term%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%5C%22%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%225b15623fd0abe04dd8055a3a6c8ef54f%22%7D",
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
    "cookie": "UM_distinctid=16b1be8a1e2c38-0f9f621b3edc7f-f353163-1fa400-16b1be8a1e3db7; _uab_collina=155954135925730288924133; zg_did=%7B%22did%22%3A%20%2216b1be8a2e6273-01efba2c0573f6-f353163-1fa400-16b1be8a2e7f8f%22%7D; acw_tc=7b060ccf15637589267313508eb99ba33cce3df44cab6b402a51448937; QCCSESSID=4d8bb00vqa4dhem1sn1tq08js2; CNZZDATA1254842228=899027629-1559535992-https%253A%252F%252Fwww.baidu.com%252F%7C1564101597; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1563867602,1563868409,1563931433,1564104705; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201564104704853%2C%22updated%22%3A%201564106278614%2C%22info%22%3A%201563758923593%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%5C%22%24utm_source%5C%22%3A%20%5C%22baidu%5C%22%2C%5C%22%24utm_medium%5C%22%3A%20%5C%22cpc%5C%22%2C%5C%22%24utm_term%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%5C%22%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%225b15623fd0abe04dd8055a3a6c8ef54f%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1564106279",
    "Host": "www.qichacha.com",
    "Referer": "https://www.qichacha.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}
link = "https://www.qichacha.com/#area"
# link = "https://www.qichacha.com/g_BJ"
# 获得网页信息
response = requests.get(link, headers=request_header, )

# print(response.text)
response.encoding = "utf-8"
Html = response.text
html_area = etree.HTML(Html)





# 二级城市  安徽，福建，广东，甘肃,广西，贵州 其他
for i in range(15, 16):
    # 获取地址链接
    # addr_link = html.xpath('//*[@id="area"]//div[%s]/div[1]/a/@href' % j)[0]
    # 获取省级 地址链接
    province_addr_link = html_area.xpath('//*[@id="area"]//div[%s]/div[1]/a/@href' % i)[0]
    # /g_BJ
    if len(province_addr_link) == 5:
        addr_ = province_addr_link[-2:]
    else:
        addr_ = province_addr_link[-2:]
    # https://www.qichacha.com/g_BJ
    full_province_addr_link = "https://www.qichacha.com" + province_addr_link
    print("--------------------------------------------------------省级地址链接-----------------------------------------")
    print(full_province_addr_link)


    for x in range(73, 501):
        # <a class="pills-item " href="/g_JS_320600.html">南通市</a>
        full_page_link = "https://www.qichacha.com/g_JS_320600.html"
        print("----------%s地区-------------第%s页---------------公司信息--------" % (addr_, x))
        print(full_page_link)
        # 获取公司链接
        # 进入每一页，获取公司链接和公司详细信息
        response_by_page_link = requests.get(full_page_link, headers=request_header_, )

        response_by_page_link.encoding = "utf-8"
        Html = response_by_page_link.text
        html_page = etree.HTML(Html)
        time.sleep(3)

        for y in range(1, 6):
            print("------------------------------第%s个企业--------------------" % y )
            company_link = html_page.xpath('//*[@id="searchlist"]//tr[%s]/td[2]/a/@href' % y)[0]
            full_company_link = "https://www.qichacha.com" + company_link

            print(full_company_link)
            # 获取公司链接和公司详细信息
            response_by_company_link = requests.get(full_company_link, headers=request_header, )
            # print(response_by_company_link.status_code)
            # if str(response_by_company_link.status_code) == "200":
            #     print("----------------------第3次requests请求成功------------获取企业详细信息-------------------")
            # else:
            #     print("----------------------第3次requests请求失败-------------获取企业详细信息------------------")
            response_by_company_link.encoding = "utf-8"
            Html = response_by_company_link.text
            html = etree.HTML(Html)


            try:
                # 根据风险扫描来判断 页面内容，在进行抓取
                # judgement_basis = html.xpath('//*[@id="base_title"]/h2/text()')[0]
                if html.xpath('//*[@id="base_title"]/h2/text()')[0]:
                    # print(judgement_basis)
                    print("----------------------------------------属于第二种页面---------------信息丰富--------------------------------------------")

            except IndexError as e:
                pass
                # print(e)
                # 详细信息
                # 基本信息
                # 公司名字
                print("------------------------------------------第一种页面-------------------------信息较少------------------------------------------")
                company_name = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[1]/h1')[0].text.replace('\n', '').replace('\t','').replace(' ','')

                # 电话
                phone_number = html.xpath('//*[@id="company-top"]//div[2]/div[3]/div[1]/span[1]/span[2]')[0].text.replace('\n', '').replace('\t','').replace(' ','')

                # 官网
                official_website = html.xpath('//*[@id="company-top"]//div[2]/div[3]/div[1]/span[3]')[0].text.replace('\n', '').replace('\t','').replace(' ','')

                # 邮箱
                email_addree = html.xpath('//*[@id="company-top"]//div[2]/div[3]/div[2]/span[1]/span[2]')[0].text.replace('\n', '').replace('\t','').replace(' ','')



                # 工商信息
                # 经营者  有问题
                person = html.xpath('//*[@id="Cominfo"]/table/td[1]')[0].text.replace('\n', '').replace('\t', '').replace(' ', '')
                # 经营状态
                running_state = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[2]')[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 成立日期
                starting_time = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[4]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 注册号
                register_number = html.xpath('//*[@id="Cominfo"]/table/tr[4]/td[2]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 企业类型
                company_type = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[2]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 所属行业
                belong_to = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[4]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')

                # 核准日期
                check_date = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[2]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 登记机关
                register_institute = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[4]' )[0].text.replace('\n', '').replace('\t', '').replace(' ','')
                # 所属地区
                belong_to_area = html.xpath('//*[@id="Cominfo"]/table/tr[7]/td[2]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 营业期限
                running_date_limition = html.xpath('//*[@id="Cominfo"]/table/tr[9]/td[4]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 企业地址
                company_addr = html.xpath('//*[@id="Cominfo"]/table/tr[10]/td[2]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')
                # 经营范围
                running_state = html.xpath('//*[@id="Cominfo"]/table/tr[11]/td[2]' )[0].text.replace('\n', '').replace('\t','').replace(' ','')


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



# 1508