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
from selenium.webdriver.common.action_chains import ActionChains

def crack():
    # 浏览器启动设置类
    optons = webdriver.ChromeOptions()
    # 浏览器启动配置
    optons.add_argument('disable-infobars')
    driver = webdriver.Chrome(executable_path=r'D:\softwares\chromedriver\chromedriver.exe', options=optons)
    driver.get("https://www.tcpjw.com/orderList/VisitValid?forceValid=1&userIdOver=118.178.15.96&redirectUrl=%2fOrderList%2fTradingCenter")
    driver.maximize_window()
    time.sleep(1)

    ActionChains(driver).move_by_offset(810, 300).click().perform()

    time.sleep(3)



if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用同城票据数据库
    db = client.同城票据
    col = db.col
    crack()
























