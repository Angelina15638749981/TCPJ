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

import requests
import os, time, random
requests.packages.urllib3.disable_warnings()
import urllib.request
import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/softwares/tesseract/tesseract.exe'
import urllib.request
import time

# 时间
nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在
# 创建文件夹
# 定义要创建的目录
mkpath = r"E:\同城票据_票面照片\%s" % nowTime
if not os.path.exists(mkpath):
    os.mkdir(mkpath)

# 获取更新的cookie
# with open(r'%s_cookie.txt' % nowTime, 'r') as f:
#     cookie = f.readline()
#     print(cookie)

# def save_pic():
#     # 浏览器启动设置类
#     optons = webdriver.ChromeOptions()
#     # 浏览器启动配置
#     prefs = {
#         'profile.default_content_setting_values':
#             {
#                 'notifications': 2
#             }
#     }
#     optons.add_argument('--headless')
#     optons.add_argument('--disable-gpu')
#     optons.add_experimental_option('prefs', prefs)
#     optons.add_argument('disable-infobars')
#     optons.add_experimental_option('excludeSwitches', ['enable-automation'])
#     driver = webdriver.Chrome(executable_path=r'D:\softwares\chromedriver\chromedriver.exe', options=optons)
#
#     return driver


# def get_full_name(pic_link, item_person):
#     urllib.request.urlretrieve(pic_link, '%s.png' % item_person)
#     image = cv2.imread('%s.png' % item_person, 1)
#
#     #二值化
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
#     cv2.waitKey(0)
#
#     rows, cols = binary.shape
#     scale = 40
#     #识别横线
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(cols//scale,1))
#     eroded = cv2.erode(binary,kernel,iterations = 1)
#     # cv2.imshow("Eroded Image",eroded)
#     dilatedcol = cv2.dilate(eroded,kernel,iterations = 1)
#
#     #识别竖线
#     scale = 20
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,rows//scale))
#     eroded = cv2.erode(binary,kernel,iterations = 1)
#     dilatedrow = cv2.dilate(eroded,kernel,iterations = 1)
#
#     #标识交点
#     bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)
#
#     #标识表格
#     merge = cv2.add(dilatedcol,dilatedrow)
#     cv2.waitKey(0)
#
#     #识别黑白图中的白色点
#     ws,hs = np.where(bitwiseAnd>0)
#     mylistw=[]
#     mylisth=[]
#
#     #通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值，我只取最后一点
#     i = 0
#     myxs=np.sort(hs)
#     for i in range(len(myxs)-1):
#         if(myxs[i+1]-myxs[i]>10):
#             mylisth.append(myxs[i])
#         i=i+1
#     mylisth.append(myxs[i])
#
#
#     i = 0
#     myys = np.sort(ws)
#
#     for i in range(len(myys)-1):
#         if(myys[i+1]-myys[i]>10):
#             mylistw.append(myys[i])
#         i=i+1
#     mylistw.append(myys[i])
#     # hhhhhhhhhhhhhhhhhhh
#     print("----------H------------------")
#     print(mylistw, len(mylistw))
#     # wwwwwwwwwwwwwwwww
#     print("----------W------------------")
#     print(mylisth,len(mylisth))
#
#     # 银行承兑汇票情况1
#     if len(mylistw) ==13 and len(mylisth) ==7:
#
#         ROI = image[mylistw[0]:mylistw[4], mylisth[0]:mylisth[-1]]
#         # print(mylistw[0],mylistw[4], mylisth[0], mylisth[-1])
#         # 账号 1
#         account_num_1 = image[mylistw[0]:mylistw[1], mylisth[2]:mylisth[3]]
#         # 全称1
#         full_name_1 = image[mylistw[1]:mylistw[2], mylisth[2]:mylisth[3]]
#         # 开户行1
#         bank_name_1 = image[mylistw[2]:mylistw[3], mylisth[2]:mylisth[3]]
#         # 开户行号1
#         bank_name_num_1 = image[mylistw[3]:mylistw[4], mylisth[2]:mylisth[3]]
#
#         # 账号 2
#         account_num_2 = image[mylistw[0]:mylistw[1], mylisth[5]:mylisth[6]]
#         # 全称 2
#         full_name_2 = image[mylistw[1]:mylistw[2], mylisth[5]:mylisth[6]]
#         # 开户行 2
#         bank_name_2 = image[mylistw[2]:mylistw[3], mylisth[5]:mylisth[6]]
#         # 开户行号 2
#         bank_name_num_2 = image[mylistw[3]:mylistw[4], mylisth[5]:mylisth[6]]
#
#         # 账号 1
#         x, y = account_num_1.shape[0:2]
#         account_num_1 = cv2.resize(account_num_1, (int(2 * y), int(2 * x)))
#         # 全称1
#         x, y = full_name_1.shape[0:2]
#         full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))
#
#         # 账号 2
#         x, y = account_num_2.shape[0:2]
#         account_num_2 = cv2.resize(account_num_2, (int(2 * y), int(2 * x)))
#         # 全称2
#         x, y = full_name_2.shape[0:2]
#         full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))
#         # cv2.imshow("Cut Image", ROI)
#
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_account_num_1.png' % item_person, account_num_1)
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_full_name_1.png' % item_person, full_name_1)
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_1.png' % item_person, bank_name_1)
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_num_1.png' % item_person, bank_name_num_1)
#
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_account_num_2.png' % item_person, account_num_2)
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_full_name_2.png' % item_person, full_name_2)
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_2.png' % item_person, bank_name_2)
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_num_2.png' % item_person, bank_name_num_2)
#
#         cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s.png' % item_person, ROI, )
#         cv2.waitKey(0)
#
#     else:
#         account_num_1 = "无"
#         full_name_1 = "无"
#         account_num_2 = "无"
#         full_name_2 = "无"
#
#
#     # print("---------------------出票人信息------------------------------------------")
#     account_num_1 = pytesseract.image_to_string(account_num_1, lang='chi_sim')  #读取文字，此为默认英文
#     # print("账号1：%s" % account_num_1)
#     full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  #读取文字，此为默认英文
#     # print("全称1：%s" % full_name_1)
#
#     # print("---------------------收款人信息------------------------------------------")
#     account_num_2 = pytesseract.image_to_string(account_num_2, lang='chi_sim')  #读取文字，此为默认英文
#     # print("账号2：%s" % account_num_2)
#     full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  #读取文字，此为默认英文
#     # print("全称2：%s" % full_name_2)
#
#     return account_num_1,full_name_1,account_num_2,full_name_2


def get_pic(tradeno, msw):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-length": "31",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7fa9915676518330222517ec49a8abacc9709a8c9a7581c5a9a1716; ASP.NET_SessionId=zpzwd4wpuemwr15rlchsyamh; NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiylA9PZJ9IDe4wOFHOMNXlVzQUKfdV5u+ZuR3xRTWH0p9BELN+Xz4J6+EMZT/2KDCPS2zoiFsGuqQOjXaayxLIMqRgpNYKYyoYgJ7LbXi70U4xygYSCqZgPodjKP0aRQpkR557HG5qzHb2FmBJ4rqMAcclI16qWp5UKv+w+v0YNRWfMCxmSD4k4FsQuFMBTukx/y0VCKkx2n8dDf7QvGIvNg/0um9Noy2hFJOxWGLQRvND/3H9nFjIDAf0E/FNM+9o",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        # 搜索
        "tradeno": "%s" % tradeno,
        # 交易状态
        "msw": "%s" % msw,


    }
    try:

        response = requests.post("https://www.tcpjw.com/OrderList/GetBuyJDDetails",
                                 headers=headers, data=data, verify=False)
        # print(response.status_code)
        # if pt_tradestatus=="22":\
        # -------------------------------------------------------------------------bug--------------------------------------------
        html_ = response.text
        # print(Html)
        # html_ = eval(Html)




    except(KeyError,IndexError,Exception) as e:
        print(e)
        # pass
    return html_


def get_data_from_tcpj(pt_keywords, pt_tradestatus, pt_bid, pageIdx_client):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q =0.9",
        "content-length": "309",
        "content - type": "application/x-www-form-urlencoded",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7fa9915676518330222517ec49a8abacc9709a8c9a7581c5a9a1716; ASP.NET_SessionId=jt52bmkgb3hi3qydixsykj2m; NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiylA9PZJ9IDe4wOFHOMNXlVzQUKfdV5u+ZuR3xRTWH0p9BELN+Xz4J6+EMZT/2KDCPS2zoiFsGuqQOjXaayxLIMqRgpNYKYyoYgJ7LbXi70U4xygYSCqZgPodjKP0aRQpkR557HG5qzHb2FmBJ4rqMAcclI16qWp5UKv+w+v0YNRWfMCxmSD4k4FsQuFMBTukx/y0VCKkx2n8dDf7QvGIvNg/0um9Noy2hFJOxWGLQRvND/3H9nFjIDAf0E/FNM+9o",
        # "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7faa415597160258384479eca57a735df4a746d72874024353c894a; NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiya39OHdOgT5G1vHfmqDd6KAsR8s0OUV/thXejTQ/RJWjKGBbD3mOmVSbZ2JjHtArsX4ceeif6sxRyEr3tAVGfype4oLBq89Beavs9rNM/6NASpPxBXhd8D3m8EqNkML4piXLOwtUpH7SmtMplSwiMjxQsbBn9q/vfBLzhYoLz3vd5UuNca1WqhKkJ++rmXUZdLU3wt748v0YrBTMHSCkPymSrRkp12OEJ7OXVQh2S6zwVeqspNpPT/kwdeX5SHaL6",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        # 搜索
        "pt_keywords": "%s" % pt_keywords,
        # 交易状态
        "pt_tradestatus": "%s" % pt_tradestatus,
        # 银行类型
        "pt_bid": "%s" % pt_bid,
        # 页码
        "pageIdx_client": "%s" % pageIdx_client,
        "X-Requested-With": "XMLHttpRequest",

    }
    try:

        response = requests.post("https://www.tcpjw.com/OrderList/TradingCenter",
                                 headers=headers, data=data, verify=False)
        # print(response.status_code)
        # if pt_tradestatus=="22":
        # print(response.text)
        # 判断请求状态 切换I
        print("----------------------请求成功-----------------------------------------------------------------")
        time.sleep(random.random() * 3)
        response.encoding = "utf-8"
        Html = response.text
        # print(Html)
        html = etree.HTML(Html)
        #

        for i in range(1, 16):
            # with open(r'E:\同城票据_票面信息\同城票据_接单中_票面信息_%s.txt' % nowTime, 'a+') as f:
            with open('图片识别核对_%s.txt' % nowTime, 'a+') as f:
                # 1 时间
                item_time = html.xpath('//tr[%s]/td[1]' % i)[0].text.strip("\n")
                time_pic_needed = str(item_time[-5])+str(item_time[-4])+str(item_time[-2])+str(item_time[-1])
                # print(time_pic_needed)
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
                if "竞" in interest_every_100_thousand:
                    interest_every_100_thousand_ = interest_every_100_thousand
                else:
                    interest_every_100_thousand_= int(interest_every_100_thousand)

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
                # if pt_tradestatus == "00":
                #     order_state = html.xpath('//tr[%s]/td[10]/div/a' % i)[0].text.strip("\n")
                # elif pt_tradestatus == "22":
                #     order_state = html.xpath('//tr[%s]/td[10]/span' % i)[0].text.strip("\n")
                # 1指 待接单  0 订单完成
                # if "接" in order_state:
                #     order_state = 1
                # else:
                #     order_state = 0
                # 获取参数
                tradeno = html.xpath('//tr[%s]/td[10]/div/@id' % i)[0]
                tradeno_ = tradeno[-14:]
                # 获取interest_every_100_thousand 带四位小数
                interest_every_100_thousand_with_4_ = html.xpath('//tr[%s]/td[10]/div/a/@onclick'% i)
                if str(interest_every_100_thousand_with_4_[0][25:-1])[-4:] == "0000":
                    interest_every_100_thousand_msw = str(interest_every_100_thousand)
                elif len(str(interest_every_100_thousand_with_4_[0][25:-1])) == 8:
                    interest_every_100_thousand_msw = str(interest_every_100_thousand_with_4_[0][25:-3])
                elif len(str(interest_every_100_thousand_with_4_[0][25:-1])) == 9:
                    interest_every_100_thousand_msw = str(interest_every_100_thousand_with_4_[0][25:-3])
                elif len(str(interest_every_100_thousand_with_4_[0][25:-1])) == 10:
                    interest_every_100_thousand_msw = str(interest_every_100_thousand_with_4_[0][25:-3])

                # time.sleep(1)
                # 保存图片
                # pic_link, pic_price = get_pic(tradeno_, interest_every_100_thousand_msw)


                html_ = get_pic(tradeno_, interest_every_100_thousand_msw)
                # print(html_)
                # print(type(html_))
                if "无法接单" in html_:
                    print("无法接单在html中,无法获取照片")

                elif "t_no" in html_:
                    html_ = eval(html_)
                    pic_link_ = html_["t_face"]
                    pic_price_ = html_["t_price"]



                    # 获取全称
                    # print("--------Test2---------------")
                    urllib.request.urlretrieve(pic_link_, r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s.png' % i)
                    # print("--------Test1---------------")
                    time.sleep(3)
                    image = cv2.imread(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s.png' % i, 1)
                    # 二值化
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
                    cv2.waitKey(0)
                    rows, cols = binary.shape
                    scale = 40
                    # 识别横线
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
                    eroded = cv2.erode(binary, kernel, iterations=1)
                    # cv2.imshow("Eroded Image",eroded)
                    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
                    # 识别竖线
                    scale = 20
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
                    eroded = cv2.erode(binary, kernel, iterations=1)
                    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
                    # 标识交点
                    bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)
                    # 标识表格
                    merge = cv2.add(dilatedcol, dilatedrow)
                    cv2.waitKey(0)
                    # 识别黑白图中的白色点
                    ws, hs = np.where(bitwiseAnd > 0)
                    mylistw = []
                    mylisth = []
                    # 通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值，我只取最后一点
                    i = 0
                    myxs = np.sort(hs)
                    for i in range(len(myxs) - 1):
                        if (myxs[i + 1] - myxs[i] > 10):
                            mylisth.append(myxs[i])
                        i = i + 1
                    mylisth.append(myxs[i])

                    i = 0
                    myys = np.sort(ws)

                    for i in range(len(myys) - 1):
                        if (myys[i + 1] - myys[i] > 10):
                            mylistw.append(myys[i])
                        i = i + 1
                    mylistw.append(myys[i])
                    # hhhhhhhhhhhhhhhhhhh
                    print("----------H------------------")
                    print(mylistw, len(mylistw))
                    # wwwwwwwwwwwwwwwww
                    print("----------W------------------")
                    print(mylisth, len(mylisth))
                    # 银行承兑汇票情况1
                    if len(mylistw) == 13 and len(mylisth) == 7:
                        ROI = image[mylistw[0]:mylistw[4], mylisth[0]:mylisth[-1]]
                        # print(mylistw[0],mylistw[4], mylisth[0], mylisth[-1])
                        # 账号 1
                        account_num_1 = image[mylistw[0]:mylistw[1], mylisth[2]:mylisth[3]]
                        # 全称1
                        full_name_1 = image[mylistw[1]:mylistw[2], mylisth[2]:mylisth[3]]
                        # 开户行1
                        bank_name_1 = image[mylistw[2]:mylistw[3], mylisth[2]:mylisth[3]]
                        # 开户行号1
                        bank_name_num_1 = image[mylistw[3]:mylistw[4], mylisth[2]:mylisth[3]]

                        # 账号 2
                        account_num_2 = image[mylistw[0]:mylistw[1], mylisth[5]:mylisth[6]]
                        # 全称 2
                        full_name_2 = image[mylistw[1]:mylistw[2], mylisth[5]:mylisth[6]]
                        # 开户行 2
                        bank_name_2 = image[mylistw[2]:mylistw[3], mylisth[5]:mylisth[6]]
                        # 开户行号 2
                        bank_name_num_2 = image[mylistw[3]:mylistw[4], mylisth[5]:mylisth[6]]

                        # 账号 1
                        x, y = account_num_1.shape[0:2]
                        account_num_1 = cv2.resize(account_num_1, (int(2 * y), int(2 * x)))
                        # 全称1
                        x, y = full_name_1.shape[0:2]
                        full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))

                        # 账号 2
                        x, y = account_num_2.shape[0:2]
                        account_num_2 = cv2.resize(account_num_2, (int(2 * y), int(2 * x)))
                        # 全称2
                        x, y = full_name_2.shape[0:2]
                        full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))
                        # cv2.imshow("Cut Image", ROI)

                        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_account_num_1.png' % i,
                                    account_num_1)
                        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_full_name_1.png' % i,
                                    full_name_1)
                        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_1.png' % i,
                                    bank_name_1)
                        cv2.imwrite(
                            r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_num_1.png' % i,
                            bank_name_num_1)

                        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_account_num_2.png' % i,
                                    account_num_2)
                        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_full_name_2.png' % i,
                                    full_name_2)
                        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_2.png' % i,
                                    bank_name_2)
                        cv2.imwrite(
                            r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_num_2.png' % i,
                            bank_name_num_2)

                        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s.png' % i, ROI, )
                        cv2.waitKey(0)

                    else:
                        account_num_1 = "无"
                        full_name_1 = "无"
                        account_num_2 = "无"
                        full_name_2 = "无"

                    account_num_1 = pytesseract.image_to_string(account_num_1, lang='chi_sim')  # 读取文字，此为默认英文
                    full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  # 读取文字，此为默认英文
                    account_num_2 = pytesseract.image_to_string(account_num_2, lang='chi_sim')  # 读取文字，此为默认英文
                    full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  # 读取文字，此为默认英文

                    # urllib.request.urlretrieve(pic_link, r"E:\同城票据_票面信息\%s\%s_%s_%s_%s_%s_%s_%s.png" % (nowTime, time_pic_needed, item_person, item_amount, days_to_expire_date, interest_every_100_thousand,annual_interest,defect_spot))
                    # driver = save_pic()
                    # driver.get(pic_link)
                    # driver.save_screenshot(r"E:\同城票据_票面信息\%s\%s_%s_%s_%s_%s_%s_%s.png" % (nowTime, time_pic_needed, item_person, item_amount, days_to_expire_date, interest_every_100_thousand,annual_interest,defect_spot))



                    print("---------爬取第%s行数据--------------------------------------------------------" % i)
                    print("发布时间: %s" % item_time)
                    print("承兑人: %s" % item_person)
                    print("金额（万元）: %s" % float(item_amount))
                    print("到期日: %s" % int(days_to_expire_date))
                    print("每十万扣息: %s" % interest_every_100_thousand)
                    print(" 年息: %s" % annual_interest)
                    print("瑕疵: %s" % defect_spot)
                    # print("操作: %s" % order_state) jdclick(90619125285609,1,2858.3300) 保留2位数字
                    # get_pic参数信息
                    print("订单号是: %s" % tradeno_)
                    print("传的参数msw为: %s" % interest_every_100_thousand_msw)
                    print("图片链接： %s" % pic_link_)
                    print("票据金额： %s" % pic_price_)
                    print("账号1：%s" % account_num_1)
                    print("全称1：%s" % full_name_1)
                    print("账号2：%s" % account_num_2)
                    print("全称2：%s" % full_name_2)

                    f.write(account_num_1 + ',' + full_name_1 + ',' + account_num_2 + ',' + full_name_2+ ',' + pic_price_ + ',' +pic_link_+"\n")

    except (IndexError, UnboundLocalError, Exception) as e:
        # raise e
        print(e)




if __name__ == '__main__':

    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库 https://github.com/Angelina15638749981/TCPJ.git
    db = client.bank
    col = db.data

    while True:
        for pageIdx_client in range(1, 6):
            # pt_keywords,pt_tradestatus, pt_bid, pageIdx_client
            print("--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client)
            get_data_from_tcpj("", "00", "", pageIdx_client,)
            time.sleep(3)


#13213242228
# yy123456


#








