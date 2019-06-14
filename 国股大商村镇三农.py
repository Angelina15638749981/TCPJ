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


nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

# 代理IP
# _version = sys.version_info
# is_python3 = (_version[0] == 3)
#
# orderno = "ZF20179xxxxxxxxx"
# secret = "3f9c2ecac7xxxxxxxxxxxxxxxx"
# ip = "forward.xdaili.cn"
# port = "80"
#
# ip_port = ip + ":" + port
#
# timestamp = str(int(time.time()))                # 计算时间戳
# string = ""
# string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
# if is_python3:
#     string = string.encode()
# md5_string = hashlib.md5(string).hexdigest()                 # 计算sign
# sign = md5_string.upper()                              # 转换成大写
# print(sign)
# auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
# print(auth)
# proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
# headers = {"Proxy-Authorization": auth}
# with open(r"C:\Users\admin\Desktop\scrapy_xici-master\xici\xici\ips_%s.txt" % nowTime) as f:
#     content_list = f.readlines()
#     ip_pool = [x.strip() for x in content_list]


# def ip_proxy():
#     proxies = {
#         ip_pool[-1].split(":")[0]: ip_pool[-1]
#     }
#     return proxies

# 待结单
# 获取国股数据
def get_gg_daijiedan_data_from_tcpj(n):

    # 随即设置
    user_agents = ua.random
    # print(user_agents)
    headers = {
        "User-Agent": user_agents}

    try:
        for j in range(1, 4):

            response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=1", headers=headers)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)
            print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------" % j)
            print(response.status_code)
            # print(response.text)

            print("-------------------------------------------请求成功---------------------------------------------------------------")
            time.sleep(1)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)
             # 1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
            # content_below_td = html.xpath('//*[@id="tb"]/tr[15]/td[3]')[0].text
            # print(content_below_td)

            for i in range(15, 0, -1):
                with open('tcpjw_wancheng_data_%s.txt' % nowTime, 'a+') as f:
                        # 1 时间
                        item_time = html.xpath('//*[@id="tb"]/tr[%s]/td[1]' % i)[0].text.strip("\n")
                        item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                        time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                        # print(item_time)

                        # 2 person
                        item_person = html.xpath('//*[@id="tb"]/tr[%s]/td[2]/span' % i)[0].text.strip("\n")
                        # print(item_person)

                        # 3 amount
                        item_amount = html.xpath('//*[@id="tb"]/tr[%s]/td[3]' % i)[0].text.strip("\n")
                        # print(item_amount)
                        # amount = int(item_amount)

                        # 4 expire_date
                        expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '') .replace(' ', '')
                        if expire_date[-5] == "剩":
                            days_to_expire_date = int(expire_date[-4:-1])
                        elif expire_date[-4] == "剩":
                            days_to_expire_date = int(expire_date[-3:-1])
                        elif expire_date[-3] == "剩":
                            days_to_expire_date = int(expire_date[-2:-1])
                        # print(expire_date)

                        # 5 interest_every_100_thousand
                        interest_every_100_thousand = html.xpath('//*[@id="tb"]/tr[%s]/td[5]/span' % i)[0].text.strip("\n")
                        # print(interest_every_100_thousand)
                        # if "竞" in interest_every_100_thousand:
                        #     interest_every_100_thousand = "竞价"
                        # else:
                        #     interest_every_100_thousand = int(interest_every_100_thousand)

                        # 6 annual_interest
                        annual_interest = html.xpath('//*[@id="tb"]/tr[%s]/td[6]' % i)[0].text.strip("\n")
                        # print(annual_interest)

                        # 7 defect_spot% i)% i)
                        defect_spot = html.xpath('//*[@id="tb"]/tr[%s]/td[7]/span' % i)[0].text.strip("\n")
                        # print(defect_spot)
                        # if "无" in defect_spot:
                        #     defect_spot = "无"
                        # else:
                        #     defect_spot = "有"
                        # print(defect_spot)

                        # operation 待结单
                        # order_state =html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        # operation 交易完成
                        order_state = html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        #
                        # if "接" in order_state:
                        #     order_state = 1
                        # else:
                        #     order_state = 0
                        # print(order_state)

                        band_type = "guogu"
                        judgement_basis = "pt_bid_1"

                        try:

                            col.update_one({
                                "bank_type": band_type,
                                "judgement_basis": judgement_basis,
                                "person": item_person,
                                "amount": float(item_amount),
                                "expire_date": int(days_to_expire_date),
                                "interest_every_100_thousand ": int(interest_every_100_thousand),
                                "annual_interest": annual_interest,
                                " defect_spot ":  defect_spot,
                                "operation": 1}, {"$set": {'operation': 0}})
                            # print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

                        except:
                            # 向集合同城票据中插入一条文档
                            data_ = [{"band_type": band_type,
                                    "judgement_basis": judgement_basis,
                                    'publish_time': time_,
                                    'person': item_person,
                                    'amount': float(item_amount),
                                    'expire_date': int(days_to_expire_date),
                                     'interest_every_100_thousand': interest_every_100_thousand,
                                    'annual_interest': annual_interest,
                                               'defect_spot': defect_spot,
                                               "operation": order_state}]

                            for item in data_:
                                if col.update_one(item, {'$set': item}, upsert=True):
                                    print('存储成功')


                        print("---------爬取第%s行数据--------------------------------------------------------" % i)
                        print("银行类型：%s" % band_type)
                        print("判断依据：%s" % judgement_basis)
                        print("发布时间: %s" % item_time)
                        print("承兑人: %s" % item_person)
                        print("金额（万元）: %s" % float(item_amount))
                        print("到期日: %s" % expire_date)
                        print("每十万扣息: %s" % interest_every_100_thousand)
                        print(" 年息: %s" % annual_interest)
                        print("瑕疵: %s" % defect_spot)
                        print("操作: %s" % order_state)


    except IndexError as e:
        print(e)






# 城商
def get_cs_daijiedan_data_from_tcpj(n):

    # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}

    try:
        for j in range(1, 4):
            response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=2", headers=headers)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)
            print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------" % j)
            print(response.status_code)
            # print(response.text)

            print("-------------------------------------------请求成功---------------------------------------------------------------")
            time.sleep(1)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)
             # 1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
            # content_below_td = html.xpath('//*[@id="tb"]/tr[15]/td[3]')[0].text
            # print(content_below_td)

            for i in range(15, 0, -1):
                with open('tcpjw_wancheng_data_%s.txt' % nowTime, 'a+') as f:
                        # 1 时间
                        item_time = html.xpath('//*[@id="tb"]/tr[%s]/td[1]' % i)[0].text.strip("\n")
                        item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                        time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                        # print(item_time)

                        # 2 person
                        item_person = html.xpath('//*[@id="tb"]/tr[%s]/td[2]/span' % i)[0].text.strip("\n")
                        # print(item_person)

                        # 3 amount
                        item_amount = html.xpath('//*[@id="tb"]/tr[%s]/td[3]' % i)[0].text.strip("\n")
                        # print(item_amount)
                        # amount = int(item_amount)

                        # 4 expire_date
                        expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '') .replace(' ', '')
                        if expire_date[-5] == "剩":
                            days_to_expire_date = int(expire_date[-4:-1])
                        elif expire_date[-4] == "剩":
                            days_to_expire_date = int(expire_date[-3:-1])
                        elif expire_date[-3] == "剩":
                            days_to_expire_date = int(expire_date[-2:-1])
                        # print(expire_date)

                        # 5 interest_every_100_thousand
                        interest_every_100_thousand = html.xpath('//*[@id="tb"]/tr[%s]/td[5]/span' % i)[0].text.strip("\n")
                        # print(interest_every_100_thousand)
                        # if "竞" in interest_every_100_thousand:
                        #     interest_every_100_thousand = "竞价"
                        # else:
                        #     interest_every_100_thousand = int(interest_every_100_thousand)

                        # 6 annual_interest
                        annual_interest = html.xpath('//*[@id="tb"]/tr[%s]/td[6]' % i)[0].text.strip("\n")
                        # print(annual_interest)

                        # 7 defect_spot% i)% i)
                        defect_spot = html.xpath('//*[@id="tb"]/tr[%s]/td[7]/span' % i)[0].text.strip("\n")
                        # print(defect_spot)
                        # if "无" in defect_spot:
                        #     defect_spot = "无"
                        # else:
                        #     defect_spot = "有"
                        # print(defect_spot)

                        # operation 待结单
                        # order_state =html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        # operation 交易完成
                        order_state = html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        #
                        # if "接" in order_state:
                        #     order_state = 1
                        # else:
                        #     order_state = 0
                        # print(order_state)

                        band_type = "guogu"
                        judgement_basis = "pt_bid_1"

                        try:

                            col.update_one({
                                "bank_type": band_type,
                                "judgement_basis": judgement_basis,
                                "person": item_person,
                                "amount": float(item_amount),
                                "expire_date": int(days_to_expire_date),
                                "interest_every_100_thousand ": int(interest_every_100_thousand),
                                "annual_interest": annual_interest,
                                " defect_spot ":  defect_spot,
                                "operation": 1}, {"$set": {'operation': 0}})
                            # print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

                        except:
                            # 向集合同城票据中插入一条文档
                            data_ = [{"band_type": band_type,
                                    "judgement_basis": judgement_basis,
                                    'publish_time': time_,
                                    'person': item_person,
                                    'amount': float(item_amount),
                                    'expire_date': int(days_to_expire_date),
                                     'interest_every_100_thousand': interest_every_100_thousand,
                                    'annual_interest': annual_interest,
                                               'defect_spot': defect_spot,
                                               "operation": order_state}]

                            for item in data_:
                                if col.update_one(item, {'$set': item}, upsert=True):
                                    print('存储成功')


                        print("---------爬取第%s行数据--------------------------------------------------------" % i)
                        print("银行类型：%s" % band_type)
                        print("判断依据：%s" % judgement_basis)
                        print("发布时间: %s" % item_time)
                        print("承兑人: %s" % item_person)
                        print("金额（万元）: %s" % float(item_amount))
                        print("到期日: %s" % expire_date)
                        print("每十万扣息: %s" % interest_every_100_thousand)
                        print(" 年息: %s" % annual_interest)
                        print("瑕疵: %s" % defect_spot)
                        print("操作: %s" % order_state)


    except IndexError as e:
        print(e)






# 三农
def get_sn_daijiedan_data_from_tcpj(n):

    # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}

    try:
        for j in range(1, 4):

            response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=3", headers=headers)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)
            print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------" % j)
            print(response.status_code)
            # print(response.text)

            print("-------------------------------------------请求成功---------------------------------------------------------------")
            time.sleep(1)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)
             # 1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
            # content_below_td = html.xpath('//*[@id="tb"]/tr[15]/td[3]')[0].text
            # print(content_below_td)

            for i in range(15, 0, -1):
                with open('tcpjw_wancheng_data_%s.txt' % nowTime, 'a+') as f:
                        # 1 时间
                        item_time = html.xpath('//*[@id="tb"]/tr[%s]/td[1]' % i)[0].text.strip("\n")
                        item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                        time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                        # print(item_time)

                        # 2 person
                        item_person = html.xpath('//*[@id="tb"]/tr[%s]/td[2]/span' % i)[0].text.strip("\n")
                        # print(item_person)

                        # 3 amount
                        item_amount = html.xpath('//*[@id="tb"]/tr[%s]/td[3]' % i)[0].text.strip("\n")
                        # print(item_amount)
                        # amount = int(item_amount)

                        # 4 expire_date
                        expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '') .replace(' ', '')
                        if expire_date[-5] == "剩":
                            days_to_expire_date = int(expire_date[-4:-1])
                        elif expire_date[-4] == "剩":
                            days_to_expire_date = int(expire_date[-3:-1])
                        elif expire_date[-3] == "剩":
                            days_to_expire_date = int(expire_date[-2:-1])
                        # print(expire_date)

                        # 5 interest_every_100_thousand
                        interest_every_100_thousand = html.xpath('//*[@id="tb"]/tr[%s]/td[5]/span' % i)[0].text.strip("\n")
                        # print(interest_every_100_thousand)
                        # if "竞" in interest_every_100_thousand:
                        #     interest_every_100_thousand = "竞价"
                        # else:
                        #     interest_every_100_thousand = int(interest_every_100_thousand)

                        # 6 annual_interest
                        annual_interest = html.xpath('//*[@id="tb"]/tr[%s]/td[6]' % i)[0].text.strip("\n")
                        # print(annual_interest)

                        # 7 defect_spot% i)% i)
                        defect_spot = html.xpath('//*[@id="tb"]/tr[%s]/td[7]/span' % i)[0].text.strip("\n")
                        # print(defect_spot)
                        # if "无" in defect_spot:
                        #     defect_spot = "无"
                        # else:
                        #     defect_spot = "有"
                        # print(defect_spot)

                        # operation 待结单
                        # order_state =html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        # operation 交易完成
                        order_state = html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        #
                        # if "接" in order_state:
                        #     order_state = 1
                        # else:
                        #     order_state = 0
                        # print(order_state)

                        band_type = "guogu"
                        judgement_basis = "pt_bid_1"

                        try:

                            col.update_one({
                                "bank_type": band_type,
                                "judgement_basis": judgement_basis,
                                "person": item_person,
                                "amount": float(item_amount),
                                "expire_date": int(days_to_expire_date),
                                "interest_every_100_thousand ": int(interest_every_100_thousand),
                                "annual_interest": annual_interest,
                                " defect_spot ":  defect_spot,
                                "operation": 1}, {"$set": {'operation': 0}})
                            # print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

                        except:
                            # 向集合同城票据中插入一条文档
                            data_ = [{"band_type": band_type,
                                    "judgement_basis": judgement_basis,
                                    'publish_time': time_,
                                    'person': item_person,
                                    'amount': float(item_amount),
                                    'expire_date': int(days_to_expire_date),
                                     'interest_every_100_thousand': interest_every_100_thousand,
                                    'annual_interest': annual_interest,
                                               'defect_spot': defect_spot,
                                               "operation": order_state}]

                            for item in data_:
                                if col.update_one(item, {'$set': item}, upsert=True):
                                    print('存储成功')


                        print("---------爬取第%s行数据--------------------------------------------------------" % i)
                        print("银行类型：%s" % band_type)
                        print("判断依据：%s" % judgement_basis)
                        print("发布时间: %s" % item_time)
                        print("承兑人: %s" % item_person)
                        print("金额（万元）: %s" % float(item_amount))
                        print("到期日: %s" % expire_date)
                        print("每十万扣息: %s" % interest_every_100_thousand)
                        print(" 年息: %s" % annual_interest)
                        print("瑕疵: %s" % defect_spot)
                        print("操作: %s" % order_state)


    except IndexError as e:
        print(e)






# 村镇
def get_cz_daijiedan_data_from_tcpj(n):

    # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}

    try:
        for j in range(1, 4):

            response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=6", headers=headers)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)
            print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------" % j)
            print(response.status_code)
            # print(response.text)

            print("-------------------------------------------请求成功---------------------------------------------------------------")
            time.sleep(1)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)
             # 1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
            # content_below_td = html.xpath('//*[@id="tb"]/tr[15]/td[3]')[0].text
            # print(content_below_td)

            for i in range(15, 0, -1):
                with open('tcpjw_wancheng_data_%s.txt' % nowTime, 'a+') as f:
                        # 1 时间
                        item_time = html.xpath('//*[@id="tb"]/tr[%s]/td[1]' % i)[0].text.strip("\n")
                        item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                        time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                        # print(item_time)

                        # 2 person
                        item_person = html.xpath('//*[@id="tb"]/tr[%s]/td[2]/span' % i)[0].text.strip("\n")
                        # print(item_person)

                        # 3 amount
                        item_amount = html.xpath('//*[@id="tb"]/tr[%s]/td[3]' % i)[0].text.strip("\n")
                        # print(item_amount)
                        # amount = int(item_amount)

                        # 4 expire_date
                        expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '') .replace(' ', '')
                        if expire_date[-5] == "剩":
                            days_to_expire_date = int(expire_date[-4:-1])
                        elif expire_date[-4] == "剩":
                            days_to_expire_date = int(expire_date[-3:-1])
                        elif expire_date[-3] == "剩":
                            days_to_expire_date = int(expire_date[-2:-1])
                        # print(expire_date)

                        # 5 interest_every_100_thousand
                        interest_every_100_thousand = html.xpath('//*[@id="tb"]/tr[%s]/td[5]/span' % i)[0].text.strip("\n")
                        # print(interest_every_100_thousand)
                        # if "竞" in interest_every_100_thousand:
                        #     interest_every_100_thousand = "竞价"
                        # else:
                        #     interest_every_100_thousand = int(interest_every_100_thousand)

                        # 6 annual_interest
                        annual_interest = html.xpath('//*[@id="tb"]/tr[%s]/td[6]' % i)[0].text.strip("\n")
                        # print(annual_interest)

                        # 7 defect_spot% i)% i)
                        defect_spot = html.xpath('//*[@id="tb"]/tr[%s]/td[7]/span' % i)[0].text.strip("\n")
                        # print(defect_spot)
                        # if "无" in defect_spot:
                        #     defect_spot = "无"
                        # else:
                        #     defect_spot = "有"
                        # print(defect_spot)

                        # operation 待结单
                        # order_state =html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        # operation 交易完成
                        order_state = html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        #
                        # if "接" in order_state:
                        #     order_state = 1
                        # else:
                        #     order_state = 0
                        # print(order_state)

                        band_type = "guogu"
                        judgement_basis = "pt_bid_1"

                        try:

                            col.update_one({
                                "bank_type": band_type,
                                "judgement_basis": judgement_basis,
                                "person": item_person,
                                "amount": float(item_amount),
                                "expire_date": int(days_to_expire_date),
                                "interest_every_100_thousand ": int(interest_every_100_thousand),
                                "annual_interest": annual_interest,
                                " defect_spot ":  defect_spot,
                                "operation": 1}, {"$set": {'operation': 0}})
                            # print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

                        except:
                            # 向集合同城票据中插入一条文档
                            data_ = [{"band_type": band_type,
                                    "judgement_basis": judgement_basis,
                                    'publish_time': time_,
                                    'person': item_person,
                                    'amount': float(item_amount),
                                    'expire_date': int(days_to_expire_date),
                                     'interest_every_100_thousand': interest_every_100_thousand,
                                    'annual_interest': annual_interest,
                                               'defect_spot': defect_spot,
                                               "operation": order_state}]

                            for item in data_:
                                if col.update_one(item, {'$set': item}, upsert=True):
                                    print('存储成功')


                        print("---------爬取第%s行数据--------------------------------------------------------" % i)
                        print("银行类型：%s" % band_type)
                        print("判断依据：%s" % judgement_basis)
                        print("发布时间: %s" % item_time)
                        print("承兑人: %s" % item_person)
                        print("金额（万元）: %s" % float(item_amount))
                        print("到期日: %s" % expire_date)
                        print("每十万扣息: %s" % interest_every_100_thousand)
                        print(" 年息: %s" % annual_interest)
                        print("瑕疵: %s" % defect_spot)
                        print("操作: %s" % order_state)


    except IndexError as e:
        print(e)






# 外资
def get_wz_daijiedan_data_from_tcpj(n):

    # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}

    try:
        for j in range(1, 4):

            response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=4", headers=headers)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)
            print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------" % j)
            print(response.status_code)
            # print(response.text)

            print("-------------------------------------------请求成功---------------------------------------------------------------")
            time.sleep(1)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)
             # 1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
            # content_below_td = html.xpath('//*[@id="tb"]/tr[15]/td[3]')[0].text
            # print(content_below_td)

            for i in range(15, 0, -1):
                with open('tcpjw_wancheng_data_%s.txt' % nowTime, 'a+') as f:
                        # 1 时间
                        item_time = html.xpath('//*[@id="tb"]/tr[%s]/td[1]' % i)[0].text.strip("\n")
                        item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                        time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                        # print(item_time)

                        # 2 person
                        item_person = html.xpath('//*[@id="tb"]/tr[%s]/td[2]/span' % i)[0].text.strip("\n")
                        # print(item_person)

                        # 3 amount
                        item_amount = html.xpath('//*[@id="tb"]/tr[%s]/td[3]' % i)[0].text.strip("\n")
                        # print(item_amount)
                        # amount = int(item_amount)

                        # 4 expire_date
                        expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '') .replace(' ', '')
                        if expire_date[-5] == "剩":
                            days_to_expire_date = int(expire_date[-4:-1])
                        elif expire_date[-4] == "剩":
                            days_to_expire_date = int(expire_date[-3:-1])
                        elif expire_date[-3] == "剩":
                            days_to_expire_date = int(expire_date[-2:-1])
                        # print(expire_date)

                        # 5 interest_every_100_thousand
                        interest_every_100_thousand = html.xpath('//*[@id="tb"]/tr[%s]/td[5]/span' % i)[0].text.strip("\n")
                        # print(interest_every_100_thousand)
                        # if "竞" in interest_every_100_thousand:
                        #     interest_every_100_thousand = "竞价"
                        # else:
                        #     interest_every_100_thousand = int(interest_every_100_thousand)

                        # 6 annual_interest
                        annual_interest = html.xpath('//*[@id="tb"]/tr[%s]/td[6]' % i)[0].text.strip("\n")
                        # print(annual_interest)

                        # 7 defect_spot% i)% i)
                        defect_spot = html.xpath('//*[@id="tb"]/tr[%s]/td[7]/span' % i)[0].text.strip("\n")
                        # print(defect_spot)
                        # if "无" in defect_spot:
                        #     defect_spot = "无"
                        # else:
                        #     defect_spot = "有"
                        # print(defect_spot)

                        # operation 待结单
                        # order_state =html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        # operation 交易完成
                        order_state = html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        #
                        # if "接" in order_state:
                        #     order_state = 1
                        # else:
                        #     order_state = 0
                        # print(order_state)

                        band_type = "guogu"
                        judgement_basis = "pt_bid_1"

                        try:

                            col.update_one({
                                "bank_type": band_type,
                                "judgement_basis": judgement_basis,
                                "person": item_person,
                                "amount": float(item_amount),
                                "expire_date": int(days_to_expire_date),
                                "interest_every_100_thousand ": int(interest_every_100_thousand),
                                "annual_interest": annual_interest,
                                " defect_spot ":  defect_spot,
                                "operation": 1}, {"$set": {'operation': 0}})
                            # print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

                        except:
                            # 向集合同城票据中插入一条文档
                            data_ = [{"band_type": band_type,
                                    "judgement_basis": judgement_basis,
                                    'publish_time': time_,
                                    'person': item_person,
                                    'amount': float(item_amount),
                                    'expire_date': int(days_to_expire_date),
                                     'interest_every_100_thousand': interest_every_100_thousand,
                                    'annual_interest': annual_interest,
                                               'defect_spot': defect_spot,
                                               "operation": order_state}]

                            for item in data_:
                                if col.update_one(item, {'$set': item}, upsert=True):
                                    print('存储成功')


                        print("---------爬取第%s行数据--------------------------------------------------------" % i)
                        print("银行类型：%s" % band_type)
                        print("判断依据：%s" % judgement_basis)
                        print("发布时间: %s" % item_time)
                        print("承兑人: %s" % item_person)
                        print("金额（万元）: %s" % float(item_amount))
                        print("到期日: %s" % expire_date)
                        print("每十万扣息: %s" % interest_every_100_thousand)
                        print(" 年息: %s" % annual_interest)
                        print("瑕疵: %s" % defect_spot)
                        print("操作: %s" % order_state)


    except IndexError as e:
        print(e)






if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库
    db = client.bank
    col = db.data
    while True:
        # get_full_data_from_tcpj()
        # 国股
        print("*************************************国股********************************************************************************************")
        get_gg_daijiedan_data_from_tcpj(1)
        # 城商
        print("*************************************城商*******************************************************************************************")
        get_cs_daijiedan_data_from_tcpj(1)
        # 三农
        print("*************************************三农******************************************************************************************")
        get_sn_daijiedan_data_from_tcpj(1)
        # 村镇
        print("*************************************村镇*****************************************************************************************")
        get_cz_daijiedan_data_from_tcpj(1)
        # 外资
        print("*************************************外资*****************************************************************************************")
        get_wz_daijiedan_data_from_tcpj(1)






#13213242228
# yy123456













