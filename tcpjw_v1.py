# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from io import BytesIO
import requests
from pymongo import MongoClient
from multiprocessing import Pool
import os, time, random
import asyncio

def crack():
    # 浏览器启动设置类
    optons = webdriver.ChromeOptions()
    # 浏览器启动配置
    optons.add_argument('disable-infobars')
    driver = webdriver.Chrome(executable_path=r'D:\softwares\chromedriver\chromedriver.exe', options=optons)
    driver.get("http://120.79.14.150:8888/login.html")
    driver.maximize_window()
    time.sleep(1)

    driver.find_element_by_id("exampleInputEmail1").send_keys("test02")
    driver.find_element_by_id("exampleInputPassword1").send_keys("123456")
    time.sleep(3)

    driver.find_element_by_class_name("gradient").click()
    time.sleep(3)
    #点击 利率设置
    driver.find_element_by_xpath('//*[@id="mCSB_1_container"]/ul/li[2]/a').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="mCSB_1_container"]/ul/li[4]/a').click()

    time.sleep(3)
    #点击 授信表
    driver.find_element_by_class_name("nav-link").click()
    time.sleep(1)
    # item_time = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[1]')
    # print

    html_content = driver.page_source
    print(html_content)
    # while True:
    #     for i in range(15, 0, -1):
    #         with open('tcpjw_v1_by_selenium_0523.txt', 'a+') as f:
    #             # 新需求   +图片 10+承税人.png          河南，陕西 单独保存
    #             # 1 发布时间
    #             item_time = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[1]' % i)
    #             item_time_ = "2019-" + item_time.text.replace('.', '-') + ":00"
    #             time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
    #             # print(time_)
    #             # 2 承税人
    #             item_person = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[2]' % i)
    #             # 3 金额（万元）
    #             item_amount = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[3]' % i)
    #             # 4 到期日
    #             expire_date = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[4]' % i)
    #             if expire_date.text[-5] == "剩":
    #                 days_to_expire_date = int(expire_date.text[-4:-1])
    #             elif expire_date.text[-4] == "剩":
    #                 days_to_expire_date = int(expire_date.text[-3:-1])
    #             elif expire_date.text[-3] == "剩":
    #                 days_to_expire_date = int(expire_date.text[-2:-1])
    #             # print(expire_date.text)
    #             days_to_expire_date = expire_date.text[-4:-1] if expire_date.text[-4] != "剩" else expire_date.text[-3:-1]
    #             # print(days_to_expire_date)
    #             # 5 每十万扣息
    #             interest_every_100_thousand = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[5]' % i)
    #             # 6 年息
    #             annual_interest = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[6]' % i)
    #             # 7 瑕疵
    #             defect_spot = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[7]' % i)
    #             # 操作
    #             order_state = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[10]/a' % i)
    #             # print(order_state.text)
    #
    #             # 城商 有问题
    #             bank_belongto_chengshang_list = ["农业", "中国银行", "建设", "浦发", "广发", "中信", "招商", "广大", "民生",
    #                                              "华夏", "平安", "兴业", "交通",
    #                                              "浙商", "渤海", "宁波", "江苏", "北京", "上海", "南京",
    #                                              "农村", "农商",
    #                                              "村镇",
    #                                              "财务"]
    #             for bank in bank_belongto_chengshang_list:
    #                 if bank not in item_person.text:
    #                     band_type = "城商"
    #                     judgement_basis = "城商"
    #
    #             # 国股
    #             bank_belongto_guogu_list = ["农业", "中国银行", "建设", "浦发", "广发", "中信", "招商", "广大", "民生", "华夏", "平安",
    #                                         "兴业", "交通"]
    #             for bank in bank_belongto_guogu_list:
    #                 if bank in item_person.text:
    #                     band_type = "国股"
    #                     judgement_basis = bank
    #
    #             # 大商
    #             bank_belongto_dashang_list = ["浙商", "渤海", "宁波", "江苏", "北京", "上海", "南京"]
    #             for bank in bank_belongto_dashang_list:
    #                 if bank in item_person.text:
    #                     band_type = "大商"
    #                     judgement_basis = bank
    #
    #             # 三农
    #             bank_belongto_sannong_list = ["农村", "农商"]
    #             for bank in bank_belongto_sannong_list:
    #                 if bank in item_person.text:
    #                     band_type = "三农"
    #                     judgement_basis = bank
    #
    #             # 村镇
    #             bank_belongto_cunzheng_list = ["村镇"]
    #             for bank in bank_belongto_cunzheng_list:
    #                 if bank in item_person.text:
    #                     band_type = "村镇"
    #                     judgement_basis = bank
    #
    #             # 财务
    #             bank_belongto_caiwu_list = ["财务"]
    #             for bank in bank_belongto_caiwu_list:
    #                 if bank in item_person.text:
    #                     band_type = "财务"
    #                     judgement_basis = bank
    #
    #             # 向集合同城票据中插入一条文档
    #             data = [{"band_type": band_type,
    #                      "judgement_basis": judgement_basis,
    #                      'publish_time': time_,
    #                      'person': item_person.text,
    #                      'amount': float(item_amount.text),
    #                      'expire_date': days_to_expire_date,
    #                      'interest_every_100_thousand': int(interest_every_100_thousand.text),
    #                      'annual_interest': annual_interest.text,
    #                      'defect_spot': defect_spot.text,
    #                      "operation": order_state.text}]
    #
    #             for item in data:
    #                 if col.update_one(item, {'$set': item}, upsert=True):
    #                     print('存储成功')
    #
    #
    #
    #             # 写入文件
    #             f.write(item_time.text + ',' + item_person.text + ',' + item_amount.text + ',' + expire_date.text + ',' +
    #                     interest_every_100_thousand.text + ',' + annual_interest.text + ',' + defect_spot.text + "\n")
    #             print("---------爬取第%s行数据--------------------------------------------------------" % i)
    #             print("发布时间: %s" % item_time.text)
    #             print("承税人: %s" % item_person.text)
    #             print("金额（万元）: %s" % float(item_amount.text))
    #             print("到期日: %s" % days_to_expire_date)
    #             print("每十万扣息: %s" % int(interest_every_100_thousand.text))
    #             print(" 年息: %s" % annual_interest.text)
    #             print("瑕疵: %s" % defect_spot.text)
    #             print("操作: %s" % order_state.text)
    #             # driver.save_screenshot("tcpj_data_check_%s.png" % i)
    #     driver.refresh()
    #     # time.sleep(3)

if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用同城票据数据库
    db = client.同城票据
    col = db.col
    crack()
























