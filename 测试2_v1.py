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



def get_wancheng_data_from_tcpj():

    # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}

    try:
        for m in range(1, 9):
            print("---------------------------爬取银行类型----%s--------------------------------------------------------------------------" % m)
            for j in range(1, 4):

                response = requests.get(" https://www.tcpjw.com/OrderList/TradingCenter?pageIdx_client=1&pt_bid= 1" ,
                                         headers=headers, proxies=ip_proxy())
                print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------" % j)
                print(response.status_code)
                # print(response.content)
                # 判断请求状态 切换IP
                if response.status_code != 200:
                    ip_pool.pop()
                    time.sleep(1)
                    response = requests.get(
                        " https://www.tcpjw.com/OrderList/TradingCenter?pageIdx_client=%s&pt_bid=%s " % (j, m),
                        headers=headers, proxies=ip_proxy())
                    print("--------------------爬取第%s页数据-------------------------------------------------------------" % j)

                print("----------------------请求成功-----------------------------------------------------------------")
                time.sleep(1)
                response.encoding = "utf-8"
                Html = response.text
                html = etree.HTML(Html)

                for i in range(15, 0, -1):
                    with open('tcpjw_wancheng_data_%s.txt'% nowTime, 'a+') as f:
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
                            expire_date = html.xpath('//*[@id="tb"]/tr[%s]/td'% i)[3].text.replace('\n', '').replace('\t', '') .replace(' ', '')
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
                            # if "接" in order_state:
                            order_state = 1
                            # else:
                            #     order_state = 0

                            try:
                                col.update_one({
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
                                data_ = [{
                                        'publish_time': time_,
                                        'person': item_person,
                                        'amount': float(item_amount),
                                        'expire_date': int(days_to_expire_date),
                                         'interest_every_100_thousand': int(interest_every_100_thousand),
                                        'annual_interest': annual_interest,
                                                   'defect_spot': defect_spot,
                                                   "operation": order_state}]

                                for item in data_:
                                    if col.update_one(item, {'$set': item}, upsert=True):
                                        print('存储成功')

                            # 写入文件
                            f.write(item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                                interest_every_100_thousand + ',' + annual_interest + ',' + defect_spot + ',' + str(order_state) + "\n")

                            print("---------爬取第%s行数据--------------------------------------------------------" % i)
                            print("发布时间: %s" % time_)
                            print("承兑人: %s" % item_person)
                            print("金额（万元）: %s" % float(item_amount))
                            print("到期日: %s" % int(days_to_expire_date))
                            print("每十万扣息: %s" % int(interest_every_100_thousand))
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
        get_wancheng_data_from_tcpj()




#13213242228
# yy123456









