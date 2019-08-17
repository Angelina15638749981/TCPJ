#！/usr/bin/env python
#-*- coding:utf-8 -*-
#author : Only  time:2019/8/3 0002


import requests
from lxml import etree #xpath
from wordcloud import WordCloud
import PIL.Image as image  #引入读取图片的工具
import numpy as np
import jieba   # 分词


#获取html源代码
def getPage(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64)"
                     " AppleWebKit/537.36 (KHTML, like Gecko)"
                     " Chrome/63.0.3239.132 Safari/537.36"
    }
    response = requests.get(url,headers = headers).text
    return response


#获得所有页面
def all_page():
    # 26849758  长安十二时辰
    base_url = "https://movie.douban.com/subject/26946624/comments?start="
    #列表存放所有的网页，共10页
    urllist = []
    for page in range(0, 200, 20):
        allurl = base_url+str(page)
        urllist.append(allurl)
    return urllist


#解析网页
def parse():
    #列表存放所有的短评
    all_comment = []
    number = 1
    for url in all_page():
        #初始化
        html = etree.HTML(getPage(url))
        #短评
        comment = html.xpath('//div[@class="comment"]//p/span/text()')
        print(comment)
        all_comment.append(comment)
        print('第'+str(number)+'页解析并保存成功')
        number += 1
    return all_comment


#保存为txt
def save_to_txt():
    result = parse()
    for i in range(len(result)):
        with open('小欢喜评论集.txt','a+',encoding='utf-8') as f:
            f.write(str(result[i])+'\n')  #按行存储每一页的数据
            f.close()


#将爬取的文档进行分词
def trans_CN(text):
    word_list = jieba.cut(text)
    #分词后在单独个体之间加上空格
    result = " ".join(word_list)
    return result


# 制作词云
def getWordCloud():
    path_txt = "小欢喜评论集.txt"
    path_jpg = "1.jpg"
    path_font = "C:\\Windows\\Fonts\\msyh.ttc"

    text = open(path_txt, encoding='utf-8').read()

    #剔除无关字
    text = text.replace("真的", " ")
    text = text.replace("什么", " ")
    text = text.replace("但是", " ")
    text = text.replace("而且", " ")
    text = text.replace("那么", " ")
    text = text.replace("就是", " ")
    text = text.replace("可以", " ")
    text = text.replace("不是", " ")
    text = text.replace("演员", " ")
    text = text.replace("剧情", " ")



    text = trans_CN(text)
    mask = np.array(image.open(path_jpg))  #词云背景图案
    wordcloud = WordCloud(
        background_color='black',
        mask=mask,
        scale=15,
        max_font_size=80,
        font_path=path_font
    ).generate(text)
    wordcloud.to_file('小欢喜评论词云.jpg')


#主函数
if __name__ == '__main__':



    save_to_txt()
    print('所有页面保存成功')
    getWordCloud()
    print('词云制作成功')