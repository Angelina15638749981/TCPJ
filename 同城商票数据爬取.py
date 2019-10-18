import os
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

mkpath = r"E:\同城_商票_待接单\%s" % nowTime
if not os.path.exists(mkpath):
    os.mkdir(mkpath)

def company_search(chinaCompan):


    # 转化为机器可以识别带中文的网址，编码类型为unicode。只转换汉字部分，不能全部网址进行转换
    compan_y = urllib.parse.quote(chinaCompan)
    testUr_l = "https://www.qichacha.com/search?key=" + compan_y
    # print("visit web: " + testUr_l)

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
    print(response.status_code)
    response.encoding = "utf-8"
    Html = response.text
    # print(Html)
    html = etree.HTML(Html)


    # 获取 公司 链接
    compan_link = html.xpath('//*[@id="search-result"]/tr[1]/td[3]/a/@href')[0]
    # print("公司链接： %s，用于获取该公司详细信息" % compan_link)
    full_link = "https://www.qichacha.com" + compan_link
    print(full_link)
    try:
        # 获得网页信息
        response_by_full_link = requests.get(full_link, headers=request_header, )
        print(response.status_code)
        response_by_full_link.encoding = "utf-8"
        Html = response_by_full_link.text
        html = etree.HTML(Html)


        try:

            company_name = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[1]/h1')[0].text.replace('\n',
                                                                                                        '').replace('\t', '').replace(' ', '')
            print("公司名字： %s" % company_name)


            # 官网
            official_website = html.xpath('//*[@id="company-top"]//div[2]/div[3]/div[1]/span[3]')[0].text.replace('\n',
                                                                                                                  '').replace(
                '\t', '').replace(' ', '')
            print("官网： %s" % official_website)









        except:
            print("------------------报错--------------------------------------")

    except IndexError:

        pass
    # return stockholder, stock_ratio



def get_guogu_data(pt_tradestatus, pt_bid, pageIdx_client):
    headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh - CN, zh;q = 0.9",
                "content-length": "310",
                "content - type": "application/x-www-form-urlencoded",
                "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7faa415650840058478851e52f63ee27400ac15372d5c7cac79d591; ASP.NET_SessionId=b55cmfzwdhkq0hitlfzfq3jj; acw_sc__v2=5d63833628380047be13bfb293864d02a6f472ca; acw_sc__v3=5d63833e88e3335fd0adcfc0b0c97940b96042fa; NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==",
                 "origin": "https://www.tcpjw.com",
                "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
                'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
    # 待结单
    # "pt_tradestatus": "00",
    # 交易完成
    "pt_tradestatus": "%s" % pt_tradestatus,
    "pt_bid": "%s" % pt_bid,
    "pageIdx_client": "%s" % pageIdx_client,
    "X-Requested-With": "XMLHttpRequest",

    }
    # response = requests.get(" https://www.tcpjw.com/OrderList/TradingCenter?pageIdx_client=%s&pt_bid=%s "%(p_num, bid),
    #                                          headers=headers)

    response = requests.post("https://www.tcpjw.com/OrderList/TradingCenter",
                            headers=headers, data=data)
    print(response.status_code)
    # print(response.text)
    # 判断请求状态 切换I
    print("----------------------请求成功-----------------------------------------------------------------")
    time.sleep(random.random()*3)
    response.encoding = "utf-8"
    Html = response.text
    html = etree.HTML(Html)
    #
    item1 = html.xpath('//tr[1]/td[1]')[0].text.strip("\n")
    #
    item2 = html.xpath('//tr[1]/td[2]/span')[0].text.strip("\n")
    #
    item3 = html.xpath('//tr[1]/td[3]')[0].text.strip("\n")
    #
    item4 = html.xpath('//tr[1]/td[4]')[0].text.strip("\n")
    #
    item5 = html.xpath('//tr[1]/td[5]/span')[0].text.strip("\n")
    #
    item6 = html.xpath('//tr[1]/td[6]')[0].text.strip("\n")
    #
    item7 = html.xpath('//tr[1]/td[7]/span')[0].text.strip("\n")
    #待结单 00
    item10  = html.xpath('//tr[1]/td[10]/a')[0].text.strip("\n")

    # 交易完成 22
    # item10 = html.xpath('//tr[1]/td[10]/span')[0].text.strip("\n")
    # print("----------------------打印数据----------------------------------")
    # print(item1)
    # print(item2)
    # print(item3)
    # print(item4)
    # print(item5)
    # print(item6)
    # print(item7)
    # print(item10)

    for i in range(1, 16):
        with open(r'E:\同城_商票_待接单\%s\商票待接单_%s.txt' % (nowTime, nowTime), 'a+') as f:
                # 1 时间
                item_time = html.xpath('//tr[%s]/td[1]' % i)[0].text.strip("\n")
                # item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                # time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                # print(time_)

                # 2 person
                item_person = html.xpath('//tr[%s]/td[2]/span' % i)[0].text.strip("\n")
                # print(item_person)
                # 3 amount
                item_amount = html.xpath('//tr[%s]/td[3]' % i)[0].text.strip("\n")
                # print(item_amount)
                # amount = int(item_amount)
                # 4 expire_date
                expire_date = html.xpath('//tr[%s]/td[4]'% i)[0].text.replace('\n', '').replace('\t', '') .replace(' ', '')
                print(expire_date)
                if expire_date[-6] == "剩":
                    days_to_expire_date = int(expire_date[-5:-2])
                elif expire_date[-5] == "剩":
                    days_to_expire_date = int(expire_date[-4:-2])
                elif expire_date[-4] == "剩":
                    days_to_expire_date = int(expire_date[-3:-2])
                # print(expire_date)

                # print(days_to_expire_date)
                # 5 interest_every_100_thousand
                interest_every_100_thousand = html.xpath('//tr[%s]/td[5]/span' % i)[0].text.strip("\n")
                # print(interest_every_100_thousand)
                # 6 annual_interest
                annual_interest = html.xpath('//tr[%s]/td[6]' % i)[0].text.strip("\n")
                # 7 defect_spot% i)% i)
                defect_spot = html.xpath('//tr[%s]/td[7]/span' % i)[0].text.strip("\n")
                # print(defect_spot)
                # if "无" in defect_spot:
                #     defect_spot = "无"
                # else:
                #     defect_spot = "有"
                # print(defect_spot)
                # operation 待结单 00
                order_state = html.xpath('//tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                # print(order_state)
                # operation 交易完成 22
                # order_state = html.xpath('//tr[%s]/td[10]/span' % i)[0].text.strip("\n")
                # #
                # if "接" in order_state:
                # order_state = 1
                # else:
                #     order_state = 0

                # # 写入文件
                # f.write(item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                #     interest_every_100_thousand + ',' + annual_interest + ',' + defect_spot + ',' + str(order_state) + "\n")

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % order_state)
                # stockholder, stock_ratio = company_search(item_person)
                # print("%s股东信息" % item_person )
                # print("股东（发起人）: %s" % stockholder, "     持股比例: %s" % stock_ratio)

                # 写入文件
                # f.write(
                #     item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                #     interest_every_100_thousand + ',' + annual_interest + ',' + defect_spot + ',' + order_state + ',' +stockholder+ ',' +stock_ratio)
                f.write(
                    item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                    interest_every_100_thousand + ',' + annual_interest + ',' + defect_spot + ',' + order_state + "\n")





if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库 syf
    db = client.bank
    col = db.data
    while True:
        # for bid in range(1, 9):
        for p_num in range(1, 150):
            # print("--------------------爬取类型---%s-----------------------------------------------------------" % bid)
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % p_num)
            # time.sleep(random.random() * 3)
            # pt_tradestatus, pt_bid, pageIdx_client
            get_guogu_data(00, 8, p_num)
    #
    # company_search("北京中电普华信息技术有限公司")

    # get_guogu_data()4000001793  602002
