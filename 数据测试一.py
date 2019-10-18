import asyncio
from pyppeteer import launch
import random
def input_time_random():
    return random.randint(100, 151)

async def main():
    # headless参数设为False，则变成有头模式
    browser = await launch(
        {
            'headless': True,
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

        }

    )

    page = await browser.newPage()

    # 是否启用JS，enabled设为False，则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)

    await page.goto('https://www.baidu.com/')
    await page.screenshot({'path': 'example1.png'})

    await page.type('#kw', "nba", {'delay': input_time_random()})
    await page.click("input[id='su']")
    await page.waitFor(5000)
    await page.screenshot({'path': 'example2.png'})





    # 关闭浏览器
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())









