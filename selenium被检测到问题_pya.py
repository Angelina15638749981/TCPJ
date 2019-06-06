import asyncio
import time, random
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  # 设置重试次数用的
import requests

async def main(username, pwd, url):
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    await page.goto(url)  # 访问登录页面
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
    await page.setViewport({"width": 1920, "height": 895})
    time.sleep(3)
    await page.type('#userphone', username, {'delay': input_time_random() - 50})
    await page.type('#password', pwd, {'delay': input_time_random()})
    await page.click(".login_btn")
    time.sleep(5)
    # body > div.homemenubox.newHomeHeaderBox.isInTop > div > div > ul > li:nth-child(3) > a
    await page.click("body > div.homemenubox.newHomeHeaderBox.isInTop > div > div > ul > li:nth-child(3) > a")
    time.sleep(3)

    # document.querySelector("#dl_bid > dd:nth-child(3) > a")
    # await page.click('document.querySelector("#dl_bid > dd:nth-child(3) > a")')
    time.sleep(3)




def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    username = '18625558886'  # 淘宝用户名
    pwd = 'yy123456'  # 密码
    url = 'https://www.jinbill.com/login/plogin.html'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop.run_until_complete(main(username, pwd, url))  # 将协程注册到事件循环，


