import asyncio
import time, random
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  # 设置重试次数用的
import requests
# from selenium import webdriver
import requests
import os, time, random
import asyncio
import datetime
import pymongo
from lxml import etree
from pymongo import MongoClient
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
user_agents = ua.random
requests.packages.urllib3.disable_warnings()


async def main(username, pwd, url):
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({
        'headless': False,
        'args': [
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-infobars',
            "--enable-automation"
        ],
        'dumpio': True,

    })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    await page.goto(url)  # 访问登录页面

    await page.setViewport({"width": 1920, "height": 1790})

    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator 且让
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    # 使用type选定页面元素，并修改其数值，用于输入账号密码，修改的速度仿人类操作，因为有个输入速度的检测机制
    # 因为 pyppeteer 框架需要转换为js操作，而js和python的类型定义不同，所以写法与参数要用字典，类型导入
    await page.type('#userName', username, {'delay': input_time_random() - 50})
    await page.type('#password2', pwd, {'delay': input_time_random()})

    flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
    await page.click("input[class='sub_btn']")


    #进入企企大厅
    await page.waitForNavigation()
    await page.goto("https://www.tcpjw.com/OrderList/TradingCenter")
    # await page.click("a[href='/OrderList/TradingCenter']")
    # cookie = await get_cookie(page)
    Html = await page.content()
    html = etree.HTML(Html)

    url = "https://www.tcpjw.com/orderList/VisitValid?forceValid=1&userIdOver=118.178.15.96&redirectUrl=%2fOrderList%2fTradingCenter"
    await page.goto(url)  # 访问登录页面

    await page.waitFor(5000)
    w = 960
    h = 330
    await page.mouse.move(960, 330)
    await page.mouse.down()
    while h <= 450:
        while w <= 1110:
            w += 10
            # await page.mouse.down()
            await page.mouse.move(w, h)
            await page.mouse.down()

        await page.mouse.move(960, h)
        await page.mouse.down()
        while w >= 800:
            w -= 10
            # await page.mouse.down()
            await page.mouse.move(w, h)
            await page.mouse.down()
        h += 10
    #


    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "content-length": "310",
        "content-type": "application/x-www-form-urlencoded",
        # "cookie": cookie,
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.37
        #         'x-requested-with': 'XMLHttpRequest',29.108 Safari/537.36",
        "user-agent": user_agents,

        # "Proxy-Authorization": auth
    }

    while True:
        for pageIdx_client in range(1, 11):
            data = {

                    "pt_tradestatus": "00",
                    "pt_bid": "1",
                    "pageIdx_client": "%s" % pageIdx_client,
                    "X-Requested-With": "XMLHttpRequest",

                }
            response = requests.post("https://www.tcpjw.com/OrderList/TradingCenter",
                                     headers=headers, data=data, verify=False, )
            # print(response.text)
            response.encoding = "utf-8"
            Html = response.text
            html = etree.HTML(Html)
            # item1 = html.xpath('//tr[1]/td[1]')[0].text.strip("\n")
            # print(item1)
            for i in range(1, 16):
                # 1 时间
                item_time = html.xpath('//tr[%s]/td[1]' % i)[0].text.strip("\n")

                if item_time:
                    item_time_ = "2019-" + item_time.replace('.', '-') + ":00"
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
                # if "竞" in interest_every_100_thousand:
                #     interest_every_100_thousand_ = interest_every_100_thousand
                # else:
                #     interest_every_100_thousand_ = int(interest_every_100_thousand)
                if "竞" not in interest_every_100_thousand:
                    interest_every_100_thousand_ = int(interest_every_100_thousand)
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
                # order_state =html.xpath('//tr[%s]/td[10]' % i)[0].text.strip("\n")
                # print(order_state)
                # operation 交易完成 22
                # order_state = html.xpath('//tr[%s]/td[10]/span' % i)[0].text.strip("\n")
                # #判断订单状态


                # print(band_type)

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("时间戳类型，发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand_)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                # print("操作: %s" % order_state)


    # except IndexError as e:
    # await page.goto("https://www.tcpjw.com/orderList/VisitValid?forceValid=1&userIdOver=118.178.15.96&redirectUrl=%2fOrderList%2fTradingCenter")


      # for order_state in ["00", "22"]:
            #     await page.click("a[data-values='%s']" % order_state)
            #     time.sleep(1)
            #     for person_type in ["1", "2", "3", "6", "7", "4"]:
            #         print(order_state, person_type)
            #     await page.click("a[data-values='%s']" % order_state)
            #     await page.click("a[data-values='%s']" % person_type)
    # for i in range(1, 16):
    # #     1 时间
    #     item_time = html.xpath('//tr[%s]/td[1]' % i)[0].text.strip("\n")
    #
    #     # if item_time:
    #     #     item_time_ = "2019-" + item_time.replace('.', '-') + ":00"
    #     #     print(item_time_)
    #     #     time_ = int(time.mktime(time.strptime(item_time_, '%Y-%m-%d %H:%M:%S')))
    #     # else:
    #     #     break
    #     # print(time_)
    #     # 2 person
    #     item_person = html.xpath('//tr[%s]/td[2]/span' % i)[0].text.strip("\n")
    #
    #     # print(item_person)
    #     # 3 amount
    #     item_amount = html.xpath('//tr[%s]/td[3]' % i)[0].text.strip("\n")
    #     # print(item_amount)
    #     # amount = int(item_amount)
    #     # 4 expire_date
    #     expire_date = html.xpath('//tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '').replace(' ',
    #                                                                                                        '')
    #     if expire_date[-6] == "剩":
    #         days_to_expire_date = int(expire_date[-5:-2])
    #     elif expire_date[-5] == "剩":
    #         days_to_expire_date = int(expire_date[-4:-2])
    #     elif expire_date[-4] == "剩":
    #         days_to_expire_date = int(expire_date[-3:-2])
    #     # print(expire_date)
    #     # print(days_to_expire_date)
    #     # 5 interest_every_100_thousand
    #     interest_every_100_thousand = html.xpath('//tr[%s]/td[5]/span' % i)[0].text.strip("\n")
    #     # print(type(interest_every_100_thousand))
    #     # 十万扣息 为竞价不是数字
    #     # if "竞" in interest_every_100_thousand:
    #     #     interest_every_100_thousand_ = interest_every_100_thousand
    #     # else:
    #     #     interest_every_100_thousand_ = int(interest_every_100_thousand)
    #     if "竞" not in interest_every_100_thousand:
    #         interest_every_100_thousand_ = int(interest_every_100_thousand)
    #     # print(interest_every_100_thousand)
    #     # 6 annual_interest
    #     annual_interest = html.xpath('//tr[%s]/td[6]' % i)[0].text.strip("\n")
    #     # 7 defect_spot% i)% i)
    #     defect_spot = html.xpath('//tr[%s]/td[7]/span' % i)[0].text.strip("\n")
    #     # print(defect_spot)
    #     if "无" in defect_spot:
    #         defect_spot = "无"
    #     else:
    #         defect_spot = "有"
    #     # print(defect_spot)
    #     # operation 待结单 00
    #     # order_state =html.xpath('//tr[%s]/td[10]' % i)[0].text.strip("\n")
    #     # print(order_state)
    #     # operation 交易完成 22
    #     # order_state = html.xpath('//tr[%s]/td[10]/span' % i)[0].text.strip("\n")
    #     # #判断订单状态
    #
    #
    #     # print(band_type)
    #
    #     print("---------爬取第%s行数据--------------------------------------------------------" % i)
    #     print("时间戳类型，发布时间: %s" % item_time)
    #     print("承兑人: %s" % item_person)
    #     print("金额（万元）: %s" % float(item_amount))
    #     print("到期日: %s" % int(days_to_expire_date))
    #     print("每十万扣息: %s" % interest_every_100_thousand_)
    #     print(" 年息: %s" % annual_interest)
    #     print("瑕疵: %s" % defect_spot)
    #     # print("操作: %s" % order_state)




    # await get_cookie(page)  #
    # return get_cookie(page)




# 时间
nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在
# 获取登录后cookie
async def get_cookie(page):
    # res = await page.content()
    with open("%s_cookie.txt" % nowTime, "w") as f:
        cookies_list = await page.cookies()
        # print(cookies_list)
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        print(cookies_list[0]["name"], cookies_list[0]["value"])
        print(cookies_list[1]["name"], cookies_list[1]["value"])
        print(cookies_list[2]["name"], cookies_list[0]["value"])
        cookie_full = cookies_list[0]["name"]+"="+cookies_list[0]["value"]+";"+cookies_list[1]["name"]+"="+cookies_list[1]["value"]+";"+cookies_list[2]["name"]+"="+cookies_list[2]["value"]
        print(cookie_full)
        f.write(cookie_full)
        return cookie_full



def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1__scale_text ')
        await page.mouse.down()
        await page.mouse.move(1500, 0, {'delay': random.randint(400, 500)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('#nc_1__scale_text', 'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    # 创建连接对象
    client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库
    db = client.bank
    col = db.data
    username = '18039118570'  # 用户名
    # username = '13213337315'  # 用户名
    # username = '13213242228'  # 用户名
    pwd = 'yy123456'  # 密码
    # username = '15638749981'  #
    # pwd = 'syf11140725com'  # 密码
    url = 'https://www.tcpjw.com/Account/Login?rUrl=https%3A%2F%2Fwww.tcpjw.com%2F'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop.run_until_complete(main(username, pwd, url))


