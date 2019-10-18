from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  # 设置重试次数用的
import requests
import os, time, random
import asyncio
import datetime
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
user_agents = ua.random
requests.packages.urllib3.disable_warnings()


async def main(person,username, pwd, url):
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({
        'headless': False,
        # 'headless': True,

        'args': [

            '--disable-infobars',
            "--enable-automation",
            "--start-maximized"
        ],
        'dumpio': True,

    })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.setViewport({"width": 1920, "height": 895})
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


    page=await mouse_slide(page=page)  # js拉动滑块过去。
    await page.click("input[class='sub_btn']")

    try:
        #进入企企大厅
        await page.waitForNavigation()
        await page.goto("https://www.tcpjw.com/OrderList/TradingCenter")
        await page.evaluate(
            '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

        # 搜索
        # await page.waitFor(2000)

        # await page.click("span[data-type='2']")
        # await page.waitFor(3000)
        # await page.click("input[class='je_input']")
        # await page.evaluate(
        #     '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        await page.evaluate('''() => document.getElementsByClassName("centre_search1")[0].style.display="block"''')
        await page.waitFor(2000)


        person = "中国银行"
        await page.type('.je_input', person,  {'delay': input_time_random() - 50})
        await page.waitFor(3000)

        await page.click("input[id='bidchoose']")
        await page.waitFor(1000000000000000000000)

        #抢单
        await page.click("a[class='wyjy_but fl']")

        await page.screenshot({'path': 'a1.png'})
        # await page.click("input[class='n_but1 fl']")

        await page.waitFor(3000)

        await page.click("a[class='layui-layer-ico layui-layer-close layui-layer-close1']")
        await page.screenshot({'path': 'b1.png'})

        # await page.waitFor(5000)

        await browser.close()
    except (IndexError,OSError,Exception) as e:
        raise e




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
    # await asyncio.sleep(2)
    await page.waitForXPath("//*[@id='nc_1_n1z']")
    # try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
    await page.hover('#nc_1__scale_text ')
    await page.mouse.down()
    await page.mouse.move(2000, 0, {'delay': random.randint(400, 500)})
    await page.mouse.up()
    await asyncio.sleep(2)
    print("-----------------------------------------------------------------------------")
    print('第一次验证通过')

    return page


    #
    # except Exception as e:
    #     print(e, ':验证失败')
    #     return None, page
    # else:
    #     await asyncio.sleep(2)
    #     # 判断是否通过
    #     slider_again = await page.Jeval('#nc_1__scale_text', 'node => node.textContent')
    #     if slider_again != '验证通过':
    #         return None, page
    #     else:
    #         print('验证通过')
    #         return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':

    # username = '18039118570'  # 用户名
    # username = '13213337315'  # 用户名
    username = '13213242228'  # 用户名
    pwd = 'yy123456'  # 密码
    person = "中国银行"
    # username = '15638749981'  #
    # pwd = 'syf11140725com'  # 密码
    url = 'https://www.tcpjw.com/Account/Login?rUrl=https%3A%2F%2Fwww.tcpjw.com%2F'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(username, pwd, url))

    """
    document.getElementsByClassName("nc_iconfont btn_slide")[0].style.left="316px"
    document.getElementsByClassName("nc_bg")[0].style.width="316px"
    document.getElementsByClassName("nc-lang-cnt")[0].data-nc-lang="_yesTEXT"
    
    """







