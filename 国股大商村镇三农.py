import pymongo
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
requests.packages.urllib3.disable_warnings()


nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在


# 代码冗余问题
def get_data_from_tcpj(pt_tradestatus, pt_bid, pageIdx_client):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "content-length": "307",
        "content - type": "application/x-www-form-urlencoded",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7faa415597160258384479eca57a735df4a746d72874024353c894a; NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==",
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
                                 headers=headers, data=data, verify=False)
        print(response.status_code)
        # if pt_tradestatus=="22":
        #     print(response.text)
        # 判断请求状态 切换I
        print("----------------------请求成功-----------------------------------------------------------------")
        # time.sleep(random.random() * 3)
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
            with open(r'同城_待接单_交易完成_%s.txt' % nowTime, 'a+') as f:

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

                # 1 时间
                item_time = html.xpath('//tr[%s]/td[1]' % i)[0].text.strip("\n")
                if item_time:
                    item_time_ = "2019-" + item_time.replace('.', '-')+":00"
                    # print(item_time_)
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
                # print(type(interest_every_100_thousand))
                # 十万扣息 为竞价不是数字
                # if "竞" in interest_every_100_thousand:
                #     interest_every_100_thousand_ = interest_every_100_thousand
                # else:
                #     interest_every_100_thousand_ = int(interest_every_100_thousand)
                if "竞" not in interest_every_100_thousand:
                    interest_every_100_thousand_ = int(interest_every_100_thousand)
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
                if "完成" in order_state:
                    print("-------------------------------查看状态，接单中搜索，如果有，更新状态位订单完成---------------------------")
                    try:
                        col.update_one({
                            # "judgement_basis": "1",
                            "judgement_basis": judgement_basis,
                            # 'publish_time': 1565160300,
                            'publish_time': time_,
                            # "person": "中国光大银行无锡分行",
                            "person": item_person,
                            # "expire_date": 330,
                            "expire_date": days_to_expire_date,
                            # "annual_interest": "2.8364 %",
                            "annual_interest": annual_interest,

                            "operation": "接单"}, {"$set": {'operation': "完成"}})
                    except (IndexError, Exception) as e:
                        print(e)


                # print(band_type)

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("银行类型：%s" % band_type)
                print("判断依据：%s" % judgement_basis)
                print("非时间戳类型，发布时间: %s" % time_)
                print("时间戳类型，发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand_)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % order_state)

                data_ = [{"band_type": band_type,
                          "judgement_basis": judgement_basis,
                          'publish_time': time_,
                          'person': item_person,
                          'amount': float(item_amount),
                          'expire_date': int(days_to_expire_date),
                          'interest_every_100_thousand': interest_every_100_thousand_,
                          'annual_interest': annual_interest,
                          'defect_spot': defect_spot,
                          "operation": order_state}]


                for item in data_:
                    if col.update_one(item, {'$set': item}, upsert=True):
                        print('存储成功')

                # 写入文件
                f.write(
                    item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                    interest_every_100_thousand+ ',' + annual_interest + ',' + defect_spot + ',' + str(order_state) + "\n")

    except (IndexError, ConnectionError, Exception) as e:
        print(e)
        # pass




if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库
    db = client.bank
    col = db.data

    while True:
        # gg 国股
        print("*************************************国股**待接单状态******************************************************************************************")
        for pageIdx_client_gg_jiedan in range(1, 5):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_gg_jiedan)
            time.sleep(1)

            # 国股 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("00", "1", pageIdx_client_gg_jiedan)

        # time.sleep(random.random() * 3)
        time.sleep(1)
        print("*************************************国股**订单完成状态******************************************************************************************")
        for pageIdx_client_gg_wancheng in range(1, 3):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_gg_wancheng)
            time.sleep(1)

            # 国股 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("22", "1", pageIdx_client_gg_wancheng)



        time.sleep(1)
        # cs 城商
        print("*************************************城商**待接单状态******************************************************************************************")
        for pageIdx_client_cs_jiedan in range(1, 5):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cs_jiedan)
            time.sleep(1)

            # 城商 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("00", "2", pageIdx_client_cs_jiedan)

        time.sleep(1)
        print("*************************************城商**订单完成状态******************************************************************************************")
        for pageIdx_client_cs_wancheng in range(1, 3):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cs_wancheng)
            time.sleep(1)

            # 城商 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("22", "2", pageIdx_client_cs_wancheng)



        time.sleep(1)
        # sn 三农ss

        print("*************************************三农**待接单状态******************************************************************************************")
        for pageIdx_client_sn_jiedan in range(1, 5):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_sn_jiedan)
            time.sleep(1)

            # 三农 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("00", "3", pageIdx_client_sn_jiedan)

        time.sleep(1)
        print("*************************************三农**订单完成状态******************************************************************************************")
        for pageIdx_client_sn_wancheng in range(1, 3):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_sn_wancheng)
            time.sleep(1)

            # 三农 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("22", "3", pageIdx_client_sn_wancheng)



        time.sleep(1)
        # cz 村镇
        print("*************************************村镇**待接单状态******************************************************************************************")
        for pageIdx_client_cz_jiedan in range(1, 5):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cz_jiedan)
            time.sleep(1)

            # 村镇 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("00", "6", pageIdx_client_cz_jiedan)

        time.sleep(1)
        print("*************************************村镇**订单完成状态******************************************************************************************")
        for pageIdx_client_cz_wancheng in range(1, 3):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cz_wancheng)
            time.sleep(1)

            # 村镇 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("22", "6", pageIdx_client_cz_wancheng)



        time.sleep(1)
        # wz 外资
        print("*************************************外资**待接单状态******************************************************************************************")
        for pageIdx_client_wz_jiedan in range(1, 5):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_wz_jiedan)
            time.sleep(1)

            # 外资 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("00", "7", pageIdx_client_wz_jiedan)

        time.sleep(1)
        print("*************************************外资**订单完成状态******************************************************************************************")
        for pageIdx_client_wz_wancheng in range(1, 3):
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_wz_wancheng)
            time.sleep(1)

            #外资 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("22", "7", pageIdx_client_wz_wancheng)





#13213242228
# yy123456













