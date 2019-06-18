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


# 代码冗余问题
def get_data_from_tcpj(pt_tradestatus, pt_bid, pageIdx_client):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "content-length": "307",
        "content - type": "application/x-www-form-urlencoded",
        "cookie": "_uab_collina = 155710764840181703453248;acw_tc = 77a7faa415597160258384479eca57a735df4a746d72874024353c894a;ASP.NET_SessionId = een0mox0bwn2kkfynkqlnibo",
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
    try:

        response = requests.post("https://www.tcpjw.com/OrderList/TradingCenter",
                                 headers=headers, data=data)
        print(response.status_code)
        # if pt_tradestatus=="22":
        #     print(response.text)
        # 判断请求状态 切换I
        print("----------------------请求成功-----------------------------------------------------------------")
        time.sleep(random.random() * 3)
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
        # 待结单
        # item10  = html.xpath('//tr[1]/td[10]/a')[0].text.strip("\n")
        # 交易完成
        # item10 = html.xpath('//tr[1]/td[10]/span')[0].text.strip("\n")
        if pt_tradestatus == "00":
            item10 = html.xpath('//tr[1]/td[10]/a')[0].text.strip("\n")
        elif pt_tradestatus == "22":
            item10 = html.xpath('//tr[1]/td[10]/span')[0].text.strip("\n")
        # print(item1)
        # print(item2)
        # print(item3)
        # print(item4)
        # print(item5)
        # print(item6)
        # print(item10)


        for i in range(1, 16):
            with open('tcpjw_full_data_%s.txt' % nowTime, 'a+') as f:
                # 1 时间
                item_time = html.xpath('//tr[%s]/td[1]' % i)[0].text.strip("\n")
                if item_time:
                    item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                    print(item_time_)
                    time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
                else:
                    break
                # print(time_)
                # 2 person
                item_person = html.xpath('//tr[%s]/td[2]/span' % i)[0].text.strip("\n")
                # print(item_person)
                # 3 amount
                item_amount = html.xpath('//tr[%s]/td[3]' % i)[0].text.strip("\n")
                # print(item_amount)
                # amount = int(item_amount)
                # 4 expire_date
                expire_date = html.xpath('//tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '').replace(' ',
                                                                                                                   '')
                if expire_date[-5] == "剩":
                    days_to_expire_date = int(expire_date[-4:-1])
                elif expire_date[-4] == "剩":
                    days_to_expire_date = int(expire_date[-3:-1])
                elif expire_date[-3] == "剩":
                    days_to_expire_date = int(expire_date[-2:-1])
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
                if "无" in defect_spot:
                    defect_spot = "无"
                else:
                    defect_spot = "有"
                # print(defect_spot)
                # operation 待结单 00
                # order_state =html.xpath('//tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                # print(order_state)
                # operation 交易完成 22
                # order_state = html.xpath('//tr[%s]/td[10]/span' % i)[0].text.strip("\n")
                # #判断订单状态
                if pt_tradestatus == "00":
                    order_state = html.xpath('//tr[%s]/td[10]/a' % i)[0].text.strip("\n")
                elif pt_tradestatus == "22":
                    order_state = html.xpath('//tr[%s]/td[10]/span' % i)[0].text.strip("\n")
                # 1指 待接单  0 订单完成
                if "接" in order_state:
                    order_state = 1
                else:
                    order_state = 0


                # print(pt_tradestatus)
                # print(pt_bid)
                # band_type judgement_basis 赋值
                if pt_bid == "1":
                    band_type = "国股"
                    judgement_basis = pt_bid
                elif pt_bid == "2":
                    band_type = "城商"
                    judgement_basis = pt_bid
                elif pt_bid == "3":
                    band_type = "三农"
                    judgement_basis = pt_bid
                elif pt_bid == "6":
                    band_type = "村镇"
                    judgement_basis = pt_bid
                elif pt_bid == "7":
                    band_type = "外资"
                    judgement_basis = pt_bid
                # print(band_type)

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("银行类型：%s" % band_type)
                print("判断依据：%s" % judgement_basis)
                print("发布时间: %s" % time_)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % int(interest_every_100_thousand))
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % order_state)

                # try:
                #     col.update_one({
                #         "bank_type": band_type,
                #         "judgement_basis": judgement_basis,
                #         'publish_time': time_,
                #         "person": item_person,
                #         "amount": float(item_amount),
                #         "expire_date": int(days_to_expire_date),
                #         "interest_every_100_thousand ": int(interest_every_100_thousand),
                #         "annual_interest": annual_interest,
                #         " defect_spot ": defect_spot,
                #         "operation": 1}, {"$set": {'operation': 0}})
                    # print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

                # except:
                    # 向集合同城票据中插入一条文档
                data_ = [{"band_type": band_type,
                          "judgement_basis": judgement_basis,
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
                f.write(
                    item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                    interest_every_100_thousand + ',' + annual_interest + ',' + defect_spot + ',' + str(order_state) + "\n")

    except IndexError as e:
        print(e)
        # pass




if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库
    db = client.bank
    col = db.data
    while True:
        for pageIdx_client in range(5, 50):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client)

            # 国股 参数依次为 订单状态，类型，页码
            print("*************************************国股**待接单状态******************************************************************************************")
            get_data_from_tcpj("00", "1", pageIdx_client)
            print("*************************************国股**订单完成状态******************************************************************************************")
            get_data_from_tcpj("22", "1", pageIdx_client)

            # 城商
            print("*************************************城商**待接单状态******************************************************************************************")
            get_data_from_tcpj("00", "2", pageIdx_client)
            print("*************************************城商**订单完成状态******************************************************************************************")
            get_data_from_tcpj("22", "2", pageIdx_client)

            # 三农
            print("*************************************三农**待接单状态******************************************************************************************")
            get_data_from_tcpj("00", "3", pageIdx_client)
            print("*************************************三农**订单完成状态******************************************************************************************")
            get_data_from_tcpj("22", "3", pageIdx_client)

            # 村镇
            print("*************************************村镇**待接单状态******************************************************************************************")
            get_data_from_tcpj("00", "6", pageIdx_client)
            print("*************************************村镇**订单完成状态******************************************************************************************")
            get_data_from_tcpj("22", "6", pageIdx_client)

            # 外资
            print("*************************************外资**待接单状态******************************************************************************************")
            get_data_from_tcpj("00", "7", pageIdx_client)
            print("*************************************外资**订单完成状态******************************************************************************************")
            get_data_from_tcpj("22", "7", pageIdx_client)


#13213242228
# yy123456













