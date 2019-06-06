# 商票数据处理
# !/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import re
from lxml import etree

import requests
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
user_agents = ua.random
headers = {
        "User-Agent": user_agents}

# chinaCompan ="贵州电网有限责任公司"
# chinaCompan ="泸州恒大南城置业有限公司"
# chinaCompan ="中国石油集团西部钻探工程有限公"
chinaCompan ="湖南航天机电设备与特种材料研究所"


testUr = "https://www.qichacha.com/search?key=" + chinaCompan
print("visit web: " + testUr)

# 转化为机器可以识别带中文的网址，编码类型为unicode。只转换汉字部分，不能全部网址进行转换
compan_y = urllib.parse.quote(chinaCompan)
testUr_l = "https://www.qichacha.com/search?key=" + compan_y
print("visit web: " + testUr_l)



response = requests.post(testUr_l, headers=headers, )
print(response.status_code)

#浏览器伪装池，将爬虫伪装成浏览器，避免被网站屏蔽
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)


# 爬取第一个页面，即搜索企业名字，获得访问企业信息的跳转链接
searchRet =urllib.request.urlopen(testUr_l).read().decode("utf-8", "ignore")
matchPat ='addSearchIndex.*?href="(.*?)" target="_blank" class="ma_h1"'
nextUrls = re.compile(matchPat, re.S).findall(searchRet)

nextUrl = "https://www.qichacha.com" + str(nextUrls[0])
print("企业详细信息可以查看下一个链接：" + nextUrl)

headers_ = {
    'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
response_ = requests.get(nextUrl, headers=headers_)
# print(response_.text)

response.encoding = "utf-8"
Html = response_.text
html = etree.HTML(Html)
# 股东（发起人）
stockholder = html.xpath('//*[@id="partnerslist"]//tr[2]/td[2]//tr/td[2]/a/h3')[0].text
print("以下是%s股东信息" % chinaCompan)
print("股东（发起人）: %s" % stockholder)
# 持股比例
stock_ratio = html.xpath('//*[@id="partnerslist"]//tr[2]/td[3]')[0].text
print("持股比例: %s" % stock_ratio)
# 关联产品/机构
# content_below_td = html.xpath('//*[@id="tb"]/tr[1]/td[10]/a')[0].text
# print(content_below_td)


