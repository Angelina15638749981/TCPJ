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
    driver.get("http://www.sdpjw.cn/#/register?status=1")
    driver.maximize_window()
    time.sleep(1)

    driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div/div[2]/div[2]/form/div[1]/div/div/input").send_keys("15638749981")
    driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div/div[2]/div[2]/form/div[2]/div/div/input").send_keys("syf11140725com")
    time.sleep(1)

    driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div/div[2]/div[2]/form/div[3]/div/div/button/span").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='app']/div[2]/div[2]/div/ul/li[2]").click()
    time.sleep(3)
    # 国股
    driver.find_element_by_xpath("//*[@id='app']/div[2]/div[3]/div[3]/div[2]/div/div[1]/div[2]/div/label[2]/span[2]").click()
    driver.find_element_by_xpath("//*[@id='app']/div[2]/div[3]/div[3]/div[2]/div/div[4]/div[2]/div[1]/label[3]/span[2]").click()

    for i in range(1, 11):
        person = driver.find_element_by_xpath("//*[@id='paylist']/div/div[1]/div[2]/table/tbody/tr[%s]/td[2]/div/div"% i)
        print(person.text)
    # 城商
    driver.find_element_by_xpath("//*[@id='app']/div[2]/div[2]/div/ul/li[2]").click()

    for i in range(1, 11):
        person = driver.find_element_by_xpath("//*[@id='paylist']/div/div[1]/div[2]/table/tbody/tr[%s]/td[2]/div/div"% i)
        print(person.text)




    time.sleep(10)




if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用同城票据数据库
    db = client.同城票据
    col = db.col
    crack()
























