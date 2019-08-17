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
    driver.find_element_by_xpath('//*[@id="mCSB_1_container"]/ul/li[4]/ul/li[4]/a').click()
    time.sleep(5)

    html_content = driver.page_source
    print(html_content)
    time.sleep(10)





if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用同城票据数据库
    db = client.同城票据
    col = db.col
    crack()
























