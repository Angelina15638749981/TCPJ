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

async def main():
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.goto("https://www.tcpjw.com/OrderList/TradingCenter")





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

    # username = '13213242228'  # 淘宝用户名
    # pwd = 'yy123456'  # 密码
    # url = 'https://www.tcpjw.com/orderList/VisitValid?forceValid=1&userIdOver=118.178.15.96&redirectUrl=%2fOrderList%2fTradingCenter'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop.run_until_complete(main())  # 将协程注册到事件循环，

"""
acw_tc=3a14c4a015675769662183349e8e8865fc7aafde58c494c87f1d40ee88;
ASP.NET_SessionId=fozf1wmosuo4ugiruouywdn5;
NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiylA9PZJ9IDe4wOFHOMNXlVzQUKfdV5u+ZuR3xRTWH0p9BELN+Xz4J6+EMZT/2KDCPS2zoiFsGuqQOjXaayxLIMqRgpNYKYyoYgJ7LbXi70U4xygYSCqZgPodjKP0aRQpkR557HG5qzHb2FmBJ4rqMAcclI16qWp5UKv+w+v0YNRWfMCxmSD4k4FsQuFMBTukx/y0VCKkx2n8dDf7QvGIvNg/0um9Noy2hFJOxWGLQRvND/3H9nFjIDAf0E/FNM+9o


_uab_collina=155710764840181703453248; 
acw_tc=24f9419915668933329793630e96aed17e47a82d7338cc5dc1becd5c78;
 acw_sc__v2=5d6f6af92f373a0789dcfafaed3d388bbb2c2765; 
 acw_sc__v3=5d6f6afed25ff6270f2cd4b709fc81fd4998318b;
  NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==

"""
