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

# with open(r"C:\Users\admin\Desktop\scrapy_xici-master\xici\xici\ips_%s.txt" % nowTime) as f:
#     content_list = f.readlines()
#     ip_pool = [x.strip() for x in content_list]


# def ip_proxy():
#     proxies = {
#         ip_pool[-1].split(":")[0]: ip_pool[-1]
#     }
#     return proxies

# def get_guogu_data(p_num,bid):
def company_search(chinaCompan):
    # 实例化 UserAgent 类
    ua = UserAgent()
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}
    # chinaCompan ="贵州电网有限责任公司"
    # chinaCompan ="泸州恒大南城置业有限公司"
    # chinaCompan ="中国石油集团西部钻探工程有限公"

    testUr = "https://www.qichacha.com/search?key=" + chinaCompan
    # print("visit web: " + testUr)

    # 转化为机器可以识别带中文的网址，编码类型为unicode。只转换汉字部分，不能全部网址进行转换
    compan_y = urllib.parse.quote(chinaCompan)
    testUr_l = "https://www.qichacha.com/search?key=" + compan_y
    print("visit web: " + testUr_l)

    response = requests.post(testUr_l, headers=headers, )
    print(response.status_code)

    # 浏览器伪装池，将爬虫伪装成浏览器，避免被网站屏蔽
    headers = ("User-Agent",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)

    # 爬取第一个页面，即搜索企业名字，获得访问企业信息的跳转链接
    searchRet = urllib.request.urlopen(testUr_l).read().decode("utf-8", "ignore")
    matchPat = 'addSearchIndex.*?href="(.*?)" target="_blank" class="ma_h1"'
    nextUrls = re.compile(matchPat, re.S).findall(searchRet)
    try:
        nextUrl = "https://www.qichacha.com" + str(nextUrls[0])
        print("企业详细信息可以查看下一个链接：" + nextUrl)

        headers_ = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        response_ = requests.get(nextUrl, headers=headers_)
        # print(response_.text)

        response.encoding = "utf-8"
        Html = response_.text
        html = etree.HTML(Html)
        time.sleep(random.random() * 3)
        try:
            # 股东（发起人）
            stockholder = html.xpath('//*[@id="partnerslist"]//a/h3')[0].text.strip("\n")
            # 持股比例
            stock_ratio = html.xpath('//*[@id="partnerslist"]//tr[2]/td[3]')[0].text.strip("\n")
            print("以下是%s股东信息" % chinaCompan)
            print("股东（发起人）: %s" % stockholder)
            print("持股比例: %s" % stock_ratio)
        except:
            print("------------------该公司股东信息不存在--------------------------------------")

    except IndexError:
        pass



def get_guogu_data(pt_tradestatus, pt_bid, pageIdx_client):
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
        with open('tcpjw_shangpiao_daijiedan_%s.txt' % nowTime, 'a+') as f:
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
                # 写入文件
                f.write(
                    item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                    interest_every_100_thousand + ',' + annual_interest + ',' + defect_spot + ',' + order_state + "\n")


                # company_search(item_person)




if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库
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

    # get_guogu_data()
