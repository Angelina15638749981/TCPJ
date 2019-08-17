# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from io import BytesIO
import time
import requests
import random
import pytesseract
from pytesseract import *
from PIL import Image
from aip import AipOcr
import threading

# 获取处理验证码
driver = webdriver.Ie("D:\softwares\IEDriver\IEDriverServer")
driver.get("https://ebank.sdb.com.cn/corporbank/logon_basic.jsp")
driver.maximize_window()
driver.refresh()
time.sleep(3)
_btn1 = driver.find_element_by_id('PCLogonTip')
# 点击UKEY登录
if _btn1:
    _btn1.click()
time.sleep(2)

# 获取验证码图片 certify_code.png，并识别内容
# driver.save_screenshot('full_snap.png')
# page_snap_obj = Image.open('full_snap.png')
# img = driver.find_element_by_class_name('inputcodeM')
# time.sleep(2)
# location = img.location
# # print(location)
# size = img.size
# left = location['x']
# top = location['y']
# right = left + size['width']
# bottom = top + size['height']
# image_obj = page_snap_obj.crop((left, top, right, bottom))
# image_obj.save("certify_code.png")


# 获取验证码
def get_cerfity_code():
    APP_ID = '16340507'
    API_KEY = '3BcdhviIZhIq1R0eW3nDO5id'
    SECRECT_KEY = 'GQglG2S9KB84wArEgDCxdFMoKElSVEg2'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    i = open(r'C:\Users\admin\Desktop\TCPJW\certify_code\certify_code.png','rb')
    img = i.read()
    # message = client.basicGeneral(img)
    message = client.basicAccurate(img)
    for i in message.get('words_result'):
        text = i.get('words').replace(' ', '')
        print(text)
    return text

# 登录
# def enter_into():
    # text = get_cerfity_code()
send_usr_name = driver.find_element_by_class_name("inputnameM")
if send_usr_name:
    send_usr_name.send_keys("    ")
time.sleep(1)
send_pwd = driver.find_element_by_class_name("inputpswdM")
if send_pwd:
    send_pwd.send_keys("0803kkok")
time.sleep(1)
# 识别验证码，并发送
send_certift_code = driver.find_element_by_class_name("inputcodeM")
if send_certift_code:
    send_certift_code.send_keys("0000")

driver.find_element_by_class_name("ukey_login_btn").click()
time.sleep(5)


# enter_into()































