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

nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

with open(r"C:\Users\admin\Desktop\scrapy_xici-master\xici\xici\ips_%s.txt" % nowTime) as f:
    content_list = f.readlines()
    ip_pool = [x.strip() for x in content_list]


def ip_proxy():
    proxies = {
        ip_pool[-1].split(":")[0]: ip_pool[-1]
    }
    return proxies

# 待结单
# 获取国股数据
def get_gg_daijiedan_data_from_tcpj(n):

    # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}

    try:
        for j in range(1, 4):

            response = requests.get(" https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=%s" % n,
                                     headers=headers)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)

            # response = requests.post(" https://www.tcpjw.com/OrderList/TradingCenter/",
            #                          data={"pageIdx_client": "%s" % j, "pt_tradestatus": "22"},
            #                          headers=headers)
            print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------"%j)
            print(response.status_code)
            # print(response.text)
            # 判断请求状态 切换IP
            # if response.status_code != 200:
            #     ip_pool.pop()
            #     time.sleep(1)
            #     response = requests.post("https://www.tcpjw.com/OrderList/TradingCenter?pt_bid=1",
            #                              data={"pageIdx_client": "%s" % j, "pt_tradestatus": "22"},
            #                              headers=headers)
            #     requests.adapters.DEFAULT_RETRIES = 5
            #     s = requests.session()
            #     s.keep_alive = False
            #     print("--------------------爬取第%s页数据-------------------------------------------------------------" % j)

            print("----------------------请求成功-----------------------------------------------------------------")
            time.sleep(1)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)
             # 1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
            content_below_td = html.xpath('//*[@id="tb"]/tr[1]/td[1]/a')[0].text
            print(content_below_td)
            # item_time = html.xpath('//*[@id="tb"]/tr[1]/td')[1].text
            # print(item_time)
            # 2person 5interest_every_100_thousand 7defect_spot 11operation（交易完成）
            # content_below_td_span = html.xpath('//*[@id="tb"]/tr[1]/td/span')
            # print(content_below_td_span[3].text)

            # check_time = html.xpath('//*[@id="tb"]/tr[1]/td')[0].text.strip("\n")[6:]
            # print("----------------------------系统时间--------------------------------")
            # print("系统时间:%s" % check_time)
            for i in range(15, 0, -1):
                with open('tcpjw_wancheng_data_%s.txt'%nowTime, 'a+') as f:
                        # 1 时间
                        item_time = html.xpath('//*[@id="tb"]/tr[%s]/td' % i)[0].text.strip("\n")
                        item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                        time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                        # print(time_)
                        # 2 person
                        item_person = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[0].text.strip("\n")
                        # print(item_person)
                        # 3 amount
                        item_amount = html.xpath('//*[@id="tb"]/tr[%s]/td'% i)[2].text.strip("\n")
                        # print(item_amount)
                        # amount = int(item_amount)
                        # 4 expire_date
                        expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td' % i)[3].text.replace('\n', '').replace('\t', '') .replace(' ', '')
                        if expire_date[-5] == "剩":
                            days_to_expire_date = int(expire_date[-4:-1])
                        elif expire_date[-4] == "剩":
                            days_to_expire_date = int(expire_date[-3:-1])
                        elif expire_date[-3] == "剩":
                            days_to_expire_date = int(expire_date[-2:-1])
                        # print(expire_date)

                        # print(days_to_expire_date)
                        # 5 interest_every_100_thousand
                        interest_every_100_thousand = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[1].text.strip("\n")
                        # print(interest_every_100_thousand)
                        if "竞" in interest_every_100_thousand:
                            interest_every_100_thousand = "竞价"
                        else:
                            interest_every_100_thousand = int(interest_every_100_thousand)

                        # 6 annual_interest
                        annual_interest = html.xpath('//*[@id="tb"]/tr[%s]/td' % i)[5].text.strip("\n")
                        # 7 defect_spot% i)% i)
                        defect_spot = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[2].text.strip("\n")
                        # print(defect_spot)
                        if "无" in defect_spot:
                            defect_spot = "无"
                        else:
                            defect_spot = "有"
                        # print(defect_spot)
                        # operation 待结单
                        # order_state =html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                        # print(order_state)
                        # operation 交易完成
                        order_state = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[3].text.strip("\n")
                        #
                        if "接" in order_state:
                            order_state = 1
                        else:
                            order_state = 0

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
                            print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

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

                        # 写入文件
                        f.write(
                            band_type + ',' + judgement_basis + ',' + item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                            str(interest_every_100_thousand) + ',' + annual_interest + ',' + defect_spot + ',' + str(order_state) + "\n")

                        print("---------爬取第%s行数据--------------------------------------------------------" % i)
                        print("银行类型：%s" % band_type)
                        print("判断依据：%s" % judgement_basis)
                        print("发布时间: %s" % time_)
                        print("承兑人: %s" % item_person)
                        print("金额（万元）: %s" % float(item_amount))
                        print("到期日: %s" % int(days_to_expire_date))
                        print("每十万扣息: %s" % interest_every_100_thousand)
                        print(" 年息: %s" % annual_interest)
                        print("瑕疵: %s" % defect_spot)
                        print("操作: %s" % order_state)


    except IndexError as e:
        print(e)



def get_full_data_from_tcpj():
    # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}

    try:
        for j in range(1, 5):
            # https://www.tcpjw.com/OrderList/TradingCenter/?pageIdx_client=2
            response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter/", data={"pageIdx_client": "%s" % j,"pt_tradestatus": "00"},
                                     headers=headers)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)
            print("--------------------爬取-待结单-----第%s页数据-------------------------------------------------------------" % j)
            print(response.status_code)
            # 判断请求状态 切换IP
            if response.status_code != 200:
                ip_pool.pop()
                time.sleep(1)
                response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter?pageIdx_client=%s" % j,
                                        headers=headers)
                requests.adapters.DEFAULT_RETRIES = 5
                s = requests.session()
                s.keep_alive = False
                print("--------------------爬取第%s页数据-------------------------------------------------------------" % j)

            print("----------------------请求成功-----------------------------------------------------------------")
            time.sleep(1)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)

            for i in range(15, 0, -1):
                with open('tcpjw_full_data_%s.txt'%nowTime, 'a+') as f:
                    # 1 时间
                    item_time = html.xpath('//*[@id="tb"]/tr[%s]/td' % i)[0].text.strip("\n")
                    item_time_ = "2019-" + item_time.replace('.', '-') + ":00"
                    time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                    # 2 person
                    item_person = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[0].text.strip("\n")
                    # print(item_person)
                    # 3 amount
                    item_amount = html.xpath('//*[@id="tb"]/tr[%s]/td' % i)[2].text.strip("\n")
                    # 4 expire_date
                    expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td' % i)[3].text.replace('\n', '').replace('\t', '').replace(' ', '')
                    if expire_date[-5] == "剩":
                        days_to_expire_date = int(expire_date[-4:-1])
                    elif expire_date[-4] == "剩":
                        days_to_expire_date = int(expire_date[-3:-1])
                    elif expire_date[-3] == "剩":
                        days_to_expire_date = int(expire_date[-2:-1])

                    # 5 interest_every_100_thousand
                    interest_every_100_thousand = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[1].text.strip("\n")
                    # print(type(interest_every_100_thousand))
                    if "竞" in interest_every_100_thousand:
                        interest_every_100_thousand = "竞价"
                    else:
                        interest_every_100_thousand = int(interest_every_100_thousand)

                    # 6 annual_interest
                    annual_interest = html.xpath('//*[@id="tb"]/tr[%s]/td' % i)[5].text.strip("\n")
                    # print(annual_interest)
                    # 7 defect_spot% i)% i)
                    defect_spot = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[2].text.strip("\n")
                    # print(type(defect_spot))
                    if "无" in defect_spot:
                        defect_spot = "无"
                    else:
                        defect_spot = "有"
                    # operation 待结单
                    order_state =html.xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)[0].text.strip("\n")

                    if "接" in order_state:
                        order_state = 1
                    else:
                        order_state = 0
                    band_type=""
                    judgement_basis=""


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

                    # 写入文件
                    f.write(
                        band_type + ',' + judgement_basis + ',' + item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                        str(interest_every_100_thousand) + ',' + annual_interest + ',' + defect_spot + ',' +  str(order_state) + "\n")

                    print("---------爬取第%s行数据--------------------------------------------------------" % i)
                    print("银行类型：%s" % band_type)
                    print("判断依据：%s" % judgement_basis)
                    print("发布时间: %s" % time_)
                    print("承兑人: %s" % item_person)
                    print("金额（万元）: %s" % float(item_amount))
                    print("到期日: %s" % int(days_to_expire_date))
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
        #
        # for n in range(1, 6):
        get_gg_daijiedan_data_from_tcpj(1)




#13213242228
# yy123456









