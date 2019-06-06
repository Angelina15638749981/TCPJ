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
from PIL import Image


def crack():
    # 浏览器启动设置类
    # optons = webdriver.ChromeOptions()
    # 浏览器启动配置
    # optons.add_argument('disable-infobars')
    # driver = webdriver.Chrome(executable_path=r'D:\softwares\chromedriver\chromedriver.exe', options=optons)
    # driver = webdriver.Edge("D:\softwares\edgedriver\MicrosoftWebDriver.exe")
    # action = ActionChains(driver)
    # wait = WebDriverWait(driver, 20)
    driver = webdriver.Ie("D:\softwares\IEDriver\IEDriverServer")
    driver.get("https://ebank.sdb.com.cn/corporbank/logon_basic.jsp")
    driver.maximize_window()
    # driver.refresh()
    time.sleep(3)
    _btn1 = driver.find_element_by_id('PCLogonTip')
    # 点击UKEY登录
    if _btn1:
        _btn1.click()
    time.sleep(20)

    # 处理验证码
    # img = driver.find_element_by_id("verifyImg")
    # VerifyImage?update = ' + Math.random();
    # html = driver.page_source
    # image = Image.open('img')
    # text = pytesseract.image_to_string(image)
    # print(text)

    # 用户名和密码
    # send_usr_name = driver.find_element_by_class_name("inputnameM")
    # if send_usr_name:
    #     send_usr_name.send_keys("2000856048@14")
    # time.sleep(1)
    # send_pwd = driver.find_element_by_class_name("inputpswdM")
    # if send_pwd:
    #     send_pwd.send_keys("12345678")
    # 识别验证码，并发送
    # send_certift_code = driver.find_element_by_class_name("inputcodeM")
    # if send_certift_code:
    #     send_certift_code.send_keys(text)
    driver.find_element_by_class_name("ukey_login_btn").click()







    """
    # 点击 企业大厅
    _btn = driver.find_element_by_xpath('//div[2]//div[1]//li[2]/a')
    if _btn:
        _btn.click()
    html_content = driver.page_source
    print(html_content)
    time.sleep(3)
    for j in range(3, 21):
        # 3-20页
        # 点击第一页 xpath://*[@id="page_section"]/div/a[3]
        driver.refresh()
        _btn1 = driver.find_element_by_xpath('//*[@id="page_section"]/div/a[%s]'%j)
        if _btn1:
            _btn1.click()
        for i in range(1, 16):
            # 1 发布时间
            item_time = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[1]' % i)
            # 2 承税人
            item_person = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[2]' % i)
            # 3 金额（万元）
            item_amount = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[3]' % i)
            # 4 到期日
            expire_date = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[4]' % i)
            # 5 每十万扣息
            interest_every_100_thousand = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[5]' % i)
            # 6 年息
            annual_interest = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[6]' % i)
            # 7 瑕疵
            defect_spot = driver.find_element_by_xpath('//*[@id="tb"]/tr[%s]/td[7]' % i)
            print("---------爬取第%s页，第%行数据--------------------------------------------------------" % (j, i))
            print("--------------------------------------------------------------------------------------")
            print("发布时间: %s" % item_time.text)
            print("承税人: %s" % item_person.text)
            print("金额（万元）: %s" % item_amount.text)
            print("到期日: %s" % expire_date.text)
            print("每十万扣息: %s" % interest_every_100_thousand.text)
            print(" 年息: %s" % annual_interest.text)
            print("瑕疵: %s" % defect_spot.text)
        """

crack()






















