import urllib

import requests
from fake_useragent import UserAgent
# 实例化 UserAgent 类
ua = UserAgent()
import datetime
import time
from lxml import etree
from pymongo import MongoClient
import random
import re

# 实例化 UserAgent 类
ua = UserAgent()
user_agents = ua.random
headers = {
        "User-Agent": user_agents}


nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在



def get_guogu_data(address, id_, query,page):
    position = urllib.parse.quote(query)
    url_ = "https://www.zhipin.com/job_detail/?query=%s&city=%s&industry=&position=" % (position, id_)
    print(url_)
    url = "https://www.zhipin.com/c%s/?query=%s&page=%s&ka=page-%s" % (id_,position, page, page)
    print(url)
    headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh - CN, zh;q = 0.9",
                "content - type": "application/x-www-form-urlencoded",
                "cookie": "_uab_collina=155790767424549257071252; lastCity=101020100; __c=1561343137; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DUoL10b23BUKODOyeVOZ0OBfVYi3kuBOpB7UJlOPkVVGpGN4b-hMKd6g3GCF8a_Sf%26wd%3D%26eqid%3Defd8384c000019ce000000025d10349d; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1560827190,1561017900,1561018442,1561343137; t=2P1UnjpX9hJ0WXWs; wt=2P1UnjpX9hJ0WXWs; __a=53316894.1557907674.1561017900.1561343137.115.6.37.115; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1561349665",
                 "token": "9GTGE1p0kqy91Gj",
                "referer": url_,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
                'X-Requested-With': 'XMLHttpRequest'
    }

    data = {

    "sceneStr": "cf06b97c45114cf18706c88d1f92903d",
    "filter": '{"city":{"desc":"%s","value":"%s"},"query":"%s"}' % (address, id_, query),

    }

    # print(url)
    try:
        response = requests.post(url, headers=headers, data=data)
        # print(response.status_code)
        # print(response.text)
        # 判断请求状态 切换I
        # print("----------------------请求成功-----------------------------------------------------------------")
        time.sleep(random.random()*3)
        response.encoding = "utf-8"
        Html = response.text
        html = etree.HTML(Html)

        print("-----%s地区-----------%s职位所有招聘的数据信息--------------------------------------" % (address, query))
        print("---------爬取第%s页数据--------------------------------------------------------" % page)

        for i in range(1, 31):
            with open('杭州地区UI职位信息_%s.txt' % query, 'a+') as f:
                # 1 position
                position = html.xpath('//*[@id="main"]//li[%s]/div/div[1]/h3/a/div[1]' % i)[0].text.strip("\n")
                print(position)
                # 2 salary
                salary = html.xpath('//*[@id="main"]//ul/li[%s]//h3/a/span' % i)[0].text.strip("\n")
                print(salary)
                # 3 company
                company_name = html.xpath('//*[@id="main"]//ul/li[%s]/div/div[2]/div/h3/a' % i)[0].text.strip("\n")
                print(company_name)

                # 4working place
                company_place = html.xpath('//*[@id="main"]//ul/li[%s]/div/div[1]/p/text()[1]' % i)[0].strip("\n")
                print(company_place)
                # 5working-experience
                experience = html.xpath('//*[@id="main"]//ul/li[%s]/div/div[1]/p/text()[2]' % i)[0].strip("\n")
                print(experience)
                # 6学历要求
                requirement = html.xpath('//*[@id="main"]//ul/li[%s]/div/div[1]/p/text()[3]' % i)[0].strip("\n")
                print(requirement)

                # 7公司类型
                company_type = html.xpath('//*[@id="main"]//ul/li[%s]/div/div[2]/div/p/text()[1]' % i)[0].strip("\n")
                print(company_type)
                # 8公司规模
                company_scale =html.xpath('//*[@id="main"]//ul/li[%s]/div/div[2]/div/p/text()[2]' % i)[0].strip("\n")
                print(company_scale)
                # 9发布时间
                publish_time = html.xpath('//*[@id="main"]//ul/li[%s]/div/div[3]/p' % i)[0].text.strip("\n")
                print(publish_time)

                print("---------第%s行数据--------------------------------------------------------" % i)

                print("职位名称: %s" % position)
                print("薪资: %s" % salary)
                print("公司名称: %s" % company_name)
                print("公司地点: %s" % company_place)
                print("工作经验要求: %s" % experience)
                print("学历要求: %s" % requirement)
                print("公司类型: %s" % company_type)
                print("公司规模: %s" % company_scale)
                print("发布时间: %s" % publish_time)
                # 写入文件
                f.write(
                    position + ',' + salary+ ',' + company_name + ',' + company_place + ',' +
                    experience + ',' + requirement + ',' + company_type + ',' + company_scale + ',' + publish_time + "\n")
    except IndexError as e:
        print(e)







if __name__ == '__main__':

    # filter: {"city":{"desc":"北京","value":"101010100"},"query":"英语翻译"}
    #filter: {"city":{"desc":"上海","value":"101020100"},"query":"护士"}
    #filter: {"city":{"desc":"深圳","value":"101280600"},"query":"护士"}
    #filter: {"city":{"desc":"杭州","value":"101210100"},"query":"ui 设计"}
    # filter: {"city": {"desc": "郑州", "value": "101180100"}, "query": "ui 设计"}

    for page in range(1, 40):
        # get_guogu_data("郑州", "101180100", "销售", page)
        get_guogu_data("杭州", "101210100", "python爬虫", page)



