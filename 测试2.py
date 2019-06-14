import requests
import time
import json
from lxml import etree
import re
from pymongo import MongoClient
import random
import datetime
from fake_useragent import UserAgent
import datetime
import sys
import time
import hashlib


# 方法1
# 实例化 UserAgent 类
ua = UserAgent()

# 方法2
user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
             ]

user_agents = random.choice(user_agents)

nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

# 选代理
# with open(r"C:\Users\admin\Desktop\scrapy_xici-master\xici\xici\ips_%s.txt" % nowTime) as f:
#     content_list = f.readlines()
#     ip_pool = [x.strip() for x in content_list]

# def ip_proxy():
#     proxies = {
#         ip_pool[-1].split(":")[0]: ip_pool[-1]
#     }
#     return proxies


# 代理IP
_version = sys.version_info
is_python3 = (_version[0] == 3)
# http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=6606fe923b0c4ba6819f9dca6b346ec7&orderno=YZ201961242327XYoay&returnType=2&count=20
orderno = "ZF20196128635R5mccH"
secret = "1e8b6d5b2e774e20b51d7af391a55e75"
ip = "forward.xdaili.cn"
port = "80"
ip_port = ip + ":" + port
timestamp = str(int(time.time()))                # 计算时间戳
string = ""
string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
if is_python3:
    string = string.encode()
md5_string = hashlib.md5(string).hexdigest()                 # 计算sign
sign = md5_string.upper()                              # 转换成大写
print(sign)
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
print(auth)
proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
headers = {"Proxy-Authorization": auth, "User-Agent": user_agents}
print(headers)


def get_wancheng_data_from_tcpj():
    # 对应随即设置 方法1
    # user_agents = ua.random
    # headers 设置方法1
    # headers = {"Proxy-Authorization": auth}
    # headers = {
    #     "User-Agent": headers}

    # headers设置方法2
    # headers_ = {
    #     "User-Agent": user_agents}
    # print(user_agents)
    try:
        for j in range(1, 4):
            response = requests.get(" https://www.tcpjw.com/OrderList/TradingCenter/", data={"pageIdx_client": "%s" % j,"pt_tradestatus": "22"},
                                     proxies=proxy, headers=headers, verify=False, allow_redirects=False)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)

            # response = requests.post(" https://www.tcpjw.com/OrderList/TradingCenter/",
            #                          data={"pageIdx_client": "%s" % j, "pt_tradestatus": "22"},
            #                          headers=headers)
            print("--------------------爬取-交易完成-----第%s页数据-------------------------------------------------------------"%j)
            print(response.status_code)
            print(response.text)
            # 判断请求状态 切换IP
            if response.status_code != 200:
                # ip_pool.pop()
                time.sleep(1)
                response = requests.post(" https://www.tcpjw.com/OrderList/TradingCenter/",
                                         data={"pageIdx_client": "%s" % j, "pt_tradestatus": "22"},
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
            #  1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
            # content_below_td = html.xpath('//*[@id="tb"]/tr[1]/td[10]/a')[0].text
            # print(content_below_td)
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

                        # 城商 有问题
                        bank_belongto_chengshang_list = ["农业", "中国银行", "建设", "浦发", "广发", "中信", "招商", "广大", "民生",
                                                         "华夏", "平安", "兴业", "交通",
                                                         "浙商", "渤海", "宁波", "江苏", "北京", "上海", "南京",
                                                         "农村", "农商",
                                                         "村镇",
                                                         "财务"]
                        for bank in bank_belongto_chengshang_list:
                            if bank not in item_person:
                                band_type = "城商"
                                judgement_basis = "城商"

                        # 国股
                        bank_belongto_guogu_list = ["农业", "中国银行", "建设", "浦发", "广发", "中信", "招商", "广大", "民生", "华夏", "平安",
                                                    "兴业", "交通"]
                        for bank in bank_belongto_guogu_list:
                            if bank in item_person:
                                band_type = "国股"
                                judgement_basis = bank

                        # 大商
                        bank_belongto_dashang_list = ["浙商", "渤海", "宁波", "江苏", "北京", "上海", "南京"]
                        for bank in bank_belongto_dashang_list:
                            if bank in item_person:
                                band_type = "大商"
                                judgement_basis = bank

                        # 三农
                        bank_belongto_sannong_list = ["农村", "农商"]
                        for bank in bank_belongto_sannong_list:
                            if bank in item_person:
                                band_type = "三农"
                                judgement_basis = bank

                        # 村镇
                        bank_belongto_cunzheng_list = ["村镇"]
                        for bank in bank_belongto_cunzheng_list:
                            if bank in item_person:
                                band_type = "村镇"
                                judgement_basis = bank

                        # 财务
                        bank_belongto_caiwu_list = ["财务"]
                        for bank in bank_belongto_caiwu_list:
                            if bank in item_person:
                                band_type = "财务"
                                judgement_basis = bank

                        try:
                            # result_exist = col.find(
                            #     {
                            #         "person": item_person,
                            #         "amount": float(item_amount),
                            #         "expire_date": int(days_to_expire_date),
                            #         "interest_every_100_thousand ": int(interest_every_100_thousand),
                            #         "annual_interest": annual_interest,
                            #         " defect_spot ":  defect_spot,
                            #         "operation": 1
                            #      })
                            bank.col.update_one({
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
    # 对应随即设置 方法1
    # user_agents = ua.random
    # headers 设置方法1
    # headers = {"Proxy-Authorization": auth}
    # headers = {
    #     "User-Agent": headers}

    # headers设置方法2
    # headers_ = {
    #     "Proxy-Authorization": auth,
    #     "User-Agent": user_agents}
    # print(user_agents)

    try:
        for j in range(1, 5):
            # https://www.tcpjw.com/OrderList/TradingCenter/?pageIdx_client=2
            response = requests.get("https://www.tcpjw.com/OrderList/TradingCenter/", data={"pageIdx_client": "%s" % j,"pt_tradestatus": "00"},
                                      proxies=proxy, headers=headers, verify=False, allow_redirects=False)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            time.sleep(1)
            print("--------------------爬取-待结单-----第%s页数据-------------------------------------------------------------" % j)
            print(response.status_code)
            print(response.text)
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



                    # 城商 有问题
                    bank_belongto_chengshang_list = ["农业", "中国银行", "建设", "浦发", "广发", "中信", "招商", "广大", "民生",
                                                     "华夏", "平安", "兴业", "交通",
                                                     "浙商", "渤海", "宁波", "江苏", "北京", "上海", "南京",
                                                     "农村", "农商",
                                                     "村镇",
                                                     "财务"]
                    for bank in bank_belongto_chengshang_list:
                        if bank not in item_person:
                            band_type = "城商"
                            judgement_basis = "城商"

                    # 国股
                    bank_belongto_guogu_list = ["农业", "中国银行", "建设", "浦发", "广发", "中信", "招商", "广大", "民生", "华夏", "平安",
                                                "兴业", "交通"]
                    for bank in bank_belongto_guogu_list:
                        if bank in item_person:
                            band_type = "国股"
                            judgement_basis = bank

                    # 大商
                    bank_belongto_dashang_list = ["浙商", "渤海", "宁波", "江苏", "北京", "上海", "南京"]
                    for bank in bank_belongto_dashang_list:
                        if bank in item_person:
                            band_type = "大商"
                            judgement_basis = bank

                    # 三农
                    bank_belongto_sannong_list = ["农村", "农商"]
                    for bank in bank_belongto_sannong_list:
                        if bank in item_person:
                            band_type = "三农"
                            judgement_basis = bank

                    # 村镇
                    bank_belongto_cunzheng_list = ["村镇"]
                    for bank in bank_belongto_cunzheng_list:
                        if bank in item_person:
                            band_type = "村镇"
                            judgement_basis = bank

                    # 财务
                    bank_belongto_caiwu_list = ["财务"]
                    for bank in bank_belongto_caiwu_list:
                        if bank in item_person:
                            band_type = "财务"
                            judgement_basis = bank

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
        get_full_data_from_tcpj()
        get_wancheng_data_from_tcpj()




#13213242228
# yy123456









