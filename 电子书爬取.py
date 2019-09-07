import requests

# 导入协程模块
import asyncio
import aiohttp
import requests
requests.packages.urllib3.disable_warnings()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
           "Host": "www.ireadweek.com",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

async def get_content(url):
    print("正在操作:{}".format(url))
    # 创建一个session 去获取数据
    async with requests.get(url, headers=headers, timeout=3,verify=False) as res:
        if res.status == 200:
            source = await res.text()  # 等待获取文本
            print(source)




if __name__ == '__main__':
    url_format = "http://www.ireadweek.com/index.php/bookInfo/{}.html"
    full_urllist = [url_format.format(i) for i in range(1,11394)]  # 11394
    loop = asyncio.get_event_loop()
    tasks = [get_content(url) for url in full_urllist]
    results = loop.run_until_complete(asyncio.wait(tasks))


