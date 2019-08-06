
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  # 设置重试次数用的
import os, time, random
import asyncio
import datetime

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
    await page.click('#normalLogin',)
    time.sleep(3)
    await page.type('#nameNormal', username, {'delay': input_time_random() - 50})
    await page.type('#pwdNormal', pwd, {'delay': input_time_random()})

    flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
    time.sleep(5)

    await page.click("button[class='btn btn-primary btn-block m-t-md login-btn']")
    time.sleep(2)

    # 进入企业大厅
    # await page.click("> div> div > div> div > ul > li:nth-child(2)> a")
    # time.sleep(5)
    await get_cookie(page)  #
    time.sleep(5)





# 时间
nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在
# 获取登录后cookie
async def get_cookie(page):
    # res = await page.content()
    with open("%s_cookie_qichacha.txt" % nowTime, "w") as f:
        cookies_list = await page.cookies()
        print(len(cookies_list))
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        print(cookies_list[0]["name"], cookies_list[0]["value"])
        print(cookies_list[1]["name"], cookies_list[1]["value"])
        print(cookies_list[2]["name"], cookies_list[0]["value"])
        print(cookies_list[3]["name"], cookies_list[3]["value"])
        print(cookies_list[4]["name"], cookies_list[4]["value"])
        print(cookies_list[5]["name"], cookies_list[5]["value"])
        print(cookies_list[6]["name"], cookies_list[6]["value"])
        print(cookies_list[7]["name"], cookies_list[7]["value"])
        print(cookies_list[7]["name"], cookies_list[8]["value"])
        cookie_full = cookies_list[0]["name"]+"="+cookies_list[0]["value"]+";"+cookies_list[1]["name"]+"="+cookies_list[1]["value"]+";"\
                      +cookies_list[2]["name"]+"="+cookies_list[2]["value"]+";" + cookies_list[3]["name"] + "=" + cookies_list[3]["value"] + ";" \
                      + cookies_list[4]["name"] + "=" + cookies_list[4]["value"] + ";"+cookies_list[5]["name"]+"="+cookies_list[5]["value"]+";"\
                      +cookies_list[6]["name"]+"="+cookies_list[6]["value"]+";" + cookies_list[7]["name"] + "=" + cookies_list[7]["value"] + ";" \
                      + cookies_list[8]["name"] + "=" + cookies_list[8]["value"]

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
        await page.hover('#nc_1_n1z')
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
    username = '15638749981'  # 淘宝用户名
    pwd = 'syf11140725com'  # 密码
    url = 'https://www.qichacha.com/user_login?back=%2F'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop.run_until_complete(main(username, pwd, url))  # 将协程注册到事件循环，


