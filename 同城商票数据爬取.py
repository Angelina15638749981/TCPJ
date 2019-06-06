import urllib

import requests
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
import datetime
import time
from lxml import etree
from pymongo import MongoClient

nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

with open(r"C:\Users\admin\Desktop\scrapy_xici-master\xici\xici\ips_%s.txt" % nowTime) as f:
    content_list = f.readlines()
    ip_pool = [x.strip() for x in content_list]


def ip_proxy():
    proxies = {
        ip_pool[-1].split(":")[0]: ip_pool[-1]
    }
    return proxies

def get_guogu_data(p_num,bid):
     # 随即设置
    user_agents = ua.random
    headers = {
        "User-Agent": user_agents}
    # response = requests.get(" https://www.tcpjw.com/OrderList/TradingCenter?pageIdx_client=%s&pt_bid=%s "%(p_num, bid),
    #                                          headers=headers, proxies=ip_proxy())
    response = requests.get(
         " https://www.tcpjw.com/OrderList/TradingCenter?pageIdx_client=%s&pt_bid=%s " % (p_num, bid),
         headers=headers,)
    print(response.status_code)
    # print(response.text)
    # 判断请求状态 切换I
    print("----------------------请求成功-----------------------------------------------------------------")
    time.sleep(1)
    response.encoding = "utf-8"
    Html = response.text
    html = etree.HTML(Html)
    #  1时间 3金额 4expire_date 6annual_interest 11operation（待结单）
    # content_below_td = html.xpath('//*[@id="tb"]/tr[1]/td[10]/a')[0].text
    # print(content_below_td)
    # item_time = html.xpath('//*[@id="tb"]/tr[1]/td[1]')[0].text
    # 2person 5interest_every_100_thousand 7defect_spot 11operation（交易完成）
    # content_below_td_span = html.xpath('//*[@id="tb"]/tr[1]/td/span')
    # print(content_below_td_span[3].text)

    # check_time = html.xpath('//*[@id="tb"]/tr[1]/td')[0].text.strip("\n")[6:]
    # print("----------------------------系统时间--------------------------------")
    # print("系统时间:%s" % check_time)
    # while True:
    for i in range(15, 0, -1):
        with open('tcpjw_wancheng_data_%s.txt' % nowTime, 'a+') as f:
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

                # order_state = html.xpath('//*[@id="tb"]/tr[%s]/td/span' % i)[3].text.strip("\n")
                # #
                # if "接" in order_state:
                order_state = 1
                # else:
                #     order_state = 0

                # 写入文件
                f.write(item_time + ',' + item_person + ',' + item_amount + ',' + expire_date + ',' +
                    interest_every_100_thousand + ',' + annual_interest + ',' + defect_spot + ',' + str(order_state) + "\n")

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                # print("发布时间: %s" % item_time)
                # print("承兑人: %s" % item_person)
                # print("金额（万元）: %s" % float(item_amount))
                # print("到期日: %s" % int(days_to_expire_date))
                # print("每十万扣息: %s" % interest_every_100_thousand)
                # print(" 年息: %s" % annual_interest)
                # print("瑕疵: %s" % defect_spot)
                # print("操作: %s" % order_state)
                chinaCompan = item_person
                testUr = "https://www.qichacha.com/search?key=" + chinaCompan
                print("visit web: " + testUr)

                # 转化为机器可以识别带中文的网址，编码类型为unicode。只转换汉字部分，不能全部网址进行转换
                compan_y = urllib.parse.quote(chinaCompan)
                print(compan_y)
                testUr_l = "https://www.qichacha.com/search?key=" + compan_y
                print("visit web: " + testUr_l)

                response = requests.post(testUr_l, headers=headers, )


                print(response.status_code)
                print("---------------------公司类别查询成功------------------------------------------")
                # print(response.text)





if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库
    db = client.bank
    col = db.data
    # while True:
    #     for bid in range(1, 9):
    #         for p_num in range(1, 5):
    #             print("--------------------爬取类型---%s-----------------------------------------------------------" % bid)
    #             print("--------------------爬取第%s页数据-----------------------------------------------------------" % p_num)
    get_guogu_data(1, 8)
