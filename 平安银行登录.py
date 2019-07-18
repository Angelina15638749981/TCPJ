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
from selenium.webdriver.common.alert import Alert
# 获取处理验证码
driver = webdriver.Ie("D:\IEDriver\IEDriverServer")
driver.get("https://ebank.sdb.com.cn/corporbank/logon_basic.jsp")
driver.maximize_window()
_btn1 = driver.find_element_by_id('PCLogonTip')
# 点击UKEY登录
if _btn1:
    _btn1.click()

# 获取验证码图片 certify_code.png，并识别内容
driver.save_screenshot('full_snap.png')
page_snap_obj = Image.open('full_snap.png')
img = driver.find_element_by_class_name('inputcodeM')
time.sleep(1)
location = img.location
# print(location)
size = img.size
left = location['x']
top = location['y']
right = left + size['width']
bottom = top + size['height']
image_obj = page_snap_obj.crop((left, top, right, bottom))
image_obj.save("certify_code.png")


# 获取验证码
APP_ID = '16340507'
API_KEY = '3BcdhviIZhIq1R0eW3nDO5id'
SECRECT_KEY = 'GQglG2S9KB84wArEgDCxdFMoKElSVEg2'
client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
i = open(r'C:\Users\mayn\Desktop\平安银行模拟登录\certify_code.png','rb')
img = i.read()
# message = client.basicGeneral(img)
message = client.basicAccurate(img)
for i in message.get('words_result'):
    text = i.get('words').replace(' ', '').replace('-', '')
    print(text)

try:
    # a1 = Alert(driver)
    # if a1:
    #     print(a1.text)
    # 登录
    send_usr_name = driver.find_element_by_id("userAliasText")
    if send_usr_name:
        send_usr_name.send_keys("2000856048@15")
    time.sleep(10)
    # send_pwd = driver.find_element_by_class_name("inputpswdM")
    # send_pwd = driver.find_element_by_class_name("security-suite-tip")
    # send_pwd = driver.find_element_by_id("powerpass")
    # send_pwd = driver.find_element_by_id("powerpass_UtilObject")
    # send_pwd = driver.find_element_by_xpath("//*[@id='div_ukey'']//tr[2]/td[2]")
    # if send_pwd:
    #     send_pwd.send_keys("0803kkok")
    # time.sleep(5)
    # 识别验证码，并发送 //*[@id="div_ukey"]/table/tbody/tr[2]/td[2]
    # send_certift_code = driver.find_element_by_id("checkCodeText")
    # if send_certift_code:
    #     send_certift_code.send_keys(text)

    driver.find_element_by_class_name("ukey_login_btn").click()
    # a1 = driver.switch_to.alert
    # print(a1.text)
    # a1.send_keys("12345678")
    # time.sleep(1)
    # a1.accept()

    time.sleep(5)
    # 点击付款业务
    driver.find_element_by_id("03").click()
    # 点击支付结算
    driver.find_element_by_class_name("0301").click()
    #点击 对外转账
    driver.find_element_by_class_name("030102").click()
    time.sleep(5)

except (IndexError, Exception) as e:
    print(e)
































