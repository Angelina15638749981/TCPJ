# -*- coding: utf-8 -*-
import asyncio
import time, random
from pyppeteer.launcher import launch
from retrying import retry  # 设置重试次数用的
#import requests
import os, time, random
import asyncio
import datetime
import pymongo
from lxml import etree
from pymongo import MongoClient
#from fake_useragent import UserAgent
# 实例化 UserAgent 类
#ua = UserAgent()
#user_agents = ua.random
#requests.packages.urllib3.disable_warnings()
async def main(username, pwd, url):
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({
        'headless': False,
        'args': [
            # '--disable-extensions',
            # '--hide-scrollbars',
            # '--disable-bundled-ppapi-flash',
            # '--mute-audio',
            # '--no-sandbox',
            # '--disable-setuid-sandbox',
            # '--disable-gpu',
            '--disable-infobars',
            "--enable-automation",
            "--start-maximized"
        ],
        'dumpio': True,

    })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面
   # print('123345')
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.setViewport({"width": 1920, "height": 895})
    # await page.press('F5')
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.goto(url)  # 访问登录页面
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    # 使用type选定页面元素，并修改其数值，用于输入账号密码，修改的速度仿人类操作，因为有个输入速度的检测机制
    # 因为 pyppeteer 框架需要转换为js操作，而js和python的类型定义不同，所以写法与参数要用字典，类型导入
    await page.type('#userName', username, {'delay': input_time_random() - 50})
    await page.type('#password2', pwd, {'delay': input_time_random()})
   # await page.waitFor(5000)


    flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
    await page.click("input[class='sub_btn']")

    # cookie = await page.cookies()
    # print(cookie)

    #进入企企大厅
    await page.waitForNavigation()
    await page.goto("https://www.tcpjw.com/OrderList/TradingCenter")
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    # Html = await page.content()
    # html = etree.HTML(Html)

    url = "https://www.tcpjw.com/orderList/VisitValid?forceValid=1&userIdOver=118.178.15.96&redirectUrl=%2fOrderList%2fTradingCenter"

    await page.goto(url)  # 访问登录页面
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    #
    w = 960
    h = 330
    await page.mouse.move(960, 330)
    await page.mouse.down()
    while h <= 430:
        while w <= 1110:
            w += 10
            await page.mouse.down()
            await page.mouse.move(w, h)
            await page.mouse.down()

        await page.mouse.move(960, h)
        await page.mouse.down()
        while w >= 800:
            w -= 10
            await page.mouse.down()
            await page.mouse.move(w, h)
            await page.mouse.down()
        h += 10

    await page.waitFor(1000)
    # cookie = await page.cookies()
    # print(cookie)
    await browser.close()





# 时间
nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1__scale_text ')
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(400, 500)})
        await page.mouse.up()

    except Exception as e:
        # print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('#nc_1__scale_text', 'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            # print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    # 创建连接对象
   # client = MongoClient(host='localhost', port=27017)
    # 获得数据库，此处使用 data 同城票据 数据库
   # db = client.bank
   # col = db.data

    # username = '18039118570'  # 用户名
    # username = '13213337315'  # 用户名
    username = '13213242228'  # 用户名
    pwd = 'yy123456'  # 密码
    # username = '15638749981'  #
    # pwd = 'syf11140725com'  # 密码
    url = 'https://www.tcpjw.com/Account/Login?rUrl=https%3A%2F%2Fwww.tcpjw.com%2F'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(username, pwd, url))







