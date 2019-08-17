# -*- coding: utf-8 -*-
from selenium import webdriver
import os, time, random,datetime
# import pytesseract
from PIL import Image
from aip import AipOcr
import cv2
import re
import requests
import xlwt

nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在

mkpath = r"E:\票易安_票面信息\%s" % nowTime
if not os.path.exists(mkpath):
    os.mkdir(mkpath)



def txt_to_excel(txtname):
    excelname = 'pya_%s.xls' % nowTime

    fopen = open(txtname, 'r')
    lines = fopen.readlines()

    file = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 新建一个sheet
    sheet = file.add_sheet('data')

    i = 0
    for line in lines:
        line = line.strip('\n')
        line = line.split(',')
        company_num = line[0]
        date = line[1]
        baifenbi = line[2]

        sheet.write(i, 0, company_num)
        sheet.write(i, 1, date)
        sheet.write(i, 2, baifenbi)
        i = i + 1
    file.save(excelname)


def crack():

    # 浏览器启动设置类
    optons = webdriver.ChromeOptions()
    # 浏览器启动配置
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    # optons.add_argument('--headless')
    optons.add_argument('--disable-gpu')
    optons.add_experimental_option('prefs', prefs)
    optons.add_argument('disable-infobars')
    optons.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(executable_path=r'D:\softwares\chromedriver\chromedriver.exe', options=optons)
    driver.get("https://www.jinbill.com/login/plogin.html")
    driver.maximize_window()
    time.sleep(random.random()*3)
    # 发送手机号
    _btn_phone_number = driver.find_element_by_xpath('//*[@id="userphone"]')
    if _btn_phone_number:
        _btn_phone_number.send_keys("18625558886")
    # 发送密码
    _btn_passcode = driver.find_element_by_xpath('//*[@id="password"]')
    if _btn_passcode:
        _btn_passcode.send_keys("yy123456")
    time.sleep(random.random()*3)
    # 点击登录
    driver.find_element_by_xpath("//div[2]/div/div/div/div/div[1]").click()
    time.sleep(random.random()*3)
    while True:
        # 进入云库存
        btn = driver.find_element_by_xpath("//div[3]//ul/li[3]/a")
        if btn:
            btn.click()
            time.sleep(random.random() * 3)
            break
        else:
            continue
    time.sleep(2)
    print("-------------------------------------------已进入云库存---------------------------------------------")
    source = driver.page_source#
    # print(source)
    # print("---------------------------------------------------------------------")

    try:
        for i in range(2, 102):
            with open(r'E:\票易安_票面信息\%s\pya_%s.txt' % (nowTime, nowTime), 'a+') as f:

                # 类型
                type = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[1]' % i)
                # 2期限 //*[@id="tableshow"]/table/tr[1]/td[2]你
                date_limition = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[2]' % i)
                # 3承税人 //*[@id="tableshow"]/table/tr[100]/td[3]/div
                person = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[3]' % i)
                # 4票面金额
                amount = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[4]' % i)
                # 5到期日期
                expire_date = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[5]' % i)
                # 6剩余天数
                days_left = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[6]' % i)
                # 7入库时间
                time_ = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[7]' % i)
                # 8入库时间
                hundred_thousand = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[8]' % i)
                if hundred_thousand == "----":
                    hundred_thousand = "无"
                # 9张数
                number = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[9]' % i)
                # 10所属公司
                company_ = driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[10]' % i)

                # 进入操作
                # 点击票面
                driver.find_element_by_xpath('//*[@id="tableshow"]//tr[%s]/td[11]/button[1]' % i).click()
                # 获取当前窗口的句柄
                currentWin = driver.current_window_handle
                driver.switch_to.window(currentWin)
                time.sleep(random.random() * 3)
                # 保存图片
                driver.save_screenshot(r"C:\Users\admin\Desktop\TCPJW\certify_code\票易安票面照片\p_%s.png" % (i))
                # 获取图片链接
                xpath = '//*[@class="pswp__img"]'
                for element in driver.find_elements_by_xpath(xpath):
                    img_url = element.get_attribute('src')
                    if img_url:
                        print(img_url)
                        # 获取出票人全称    收票人全称
                        response = requests.get(img_url)
                        # print(response.content)
                        # APP_ID = '16340507'
                        # API_KEY = '3BcdhviIZhIq1R0eW3nDO5id'
                        # SECRECT_KEY = 'GQglG2S9KB84wArEgDCxdFMoKElSVEg2'
                        APP_ID = '16340507'
                        API_KEY = '3BcdhviIZhIq1R0eW3nDO5id'
                        SECRECT_KEY = 'GQglG2S9KB84wArEgDCxdFMoKElSVEg2'
                        client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
                        company_ls = []
                        message = client.basicAccurate(response.content)
                        # message = client.basicGeneral(response.content)
                        print(message)

                        for j in message.get('words_result')[5:20]:
                            # print(i['words'])
                            if re.search("有限公司$", j['words']) or re.search("^[全,称，收]", j['words']):
                                company = j['words'].strip("全").strip("称").strip("全称").strip("收全称").strip("出全称")
                                company_ls.append(company)


                        if len(company_ls) == 2:
                            if "公司" or "有限" in company_ls[0] and company_ls[1]:
                                company_1 = company_ls[0]
                                company_2 = company_ls[1]
                            elif "已打码" in company_ls[0] or company_ls[1]:
                                company_1 = "无"
                                company_2 = "无"

                        else:
                            company_1 = "无"
                            company_2 = "无"

                        print("---------爬取第%s行数据--------------------------------------------------------" % i)
                        print("类型: %s" % type.text)
                        print("期限: %s" % date_limition.text)
                        print("承税人: %s" % person.text)
                        print("票面金额（万元）: %s" % amount.text.strip(""))
                        print("到期日: %s" % expire_date.text)
                        print("剩余天数: %s" % days_left.text)
                        print("入库时间: %s" % time_.text.strip("今天"))
                        print("拟售价/十万: %s" % hundred_thousand)
                        print("张数: %s" % number.text)
                        print("所属公司: %s" % company_.text)
                        print("出票人：%s" % company_1)
                        print("收票人：%s" % company_2)
                        # print(img_url)



                        # 写入文件
                        f.write(type.text + ',' + date_limition.text + ',' + person.text + ',' + amount.text.strip(
                            "") + ',' + expire_date.text + ',' +
                                days_left.text + ',' + time_.text.strip(
                            "今天") + ',' +hundred_thousand + ',' + number.text + ',' + company_.text + ',' + company_1 + ',' + company_2 + "\n")
                        # f.write(date_limition.text + ',' + person.text + ',' + amount.text.strip(
                        #     "") + ',' + expire_date.text + ',' +
                        #         days_left.text + ',' + time_.text.strip(
                        #     "今天") + ',' + number.text + ',' + company_.text + ',' + img_url + "\n")

                        time.sleep(random.random() * 3)
                        driver.find_element_by_xpath('//div[5]/div[3]/div[2]/div[2]/div[1]/button[1]').click()


                    else:
                        break


    except (IndexError,Exception,TimeoutError) as e:
        print(e)

        # pass


def f1_to_f2():
    f1 = open(r'E:\票易安_票面信息\%s\pya_%s.txt' % (nowTime, nowTime), 'r')
    f2 = open(r'E:\票易安_票面信息\%s\pya_html_%s.txt' % (nowTime, nowTime), 'w')
    ls = []
    for line in f1.readlines():
        print(line.split(","))
        ls.append(line.strip("\n").split(","))
    f2.write(str(ls))


if __name__ == '__main__':
    while True:
        crack()
    # f1_to_f2()

# 18625558886
# yy123456




















