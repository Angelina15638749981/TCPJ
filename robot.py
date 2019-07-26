import re
import time

import requests
import itchat
import random
KEY = '9d22f7e2a7a347b18d57743882fe7367'
from itchat.content import *
def get_response(msg):
    api_url = 'http://www.tuling123.com/openapi/api'  # 图灵机器人网址
    data = {
        'key': KEY,
        'info': msg,  # 这是我们从好友接收到的消息 然后转发给图灵机器人
        'userid': 'wechat-robot',  # 这里你想改什么都可以
    }
    try:
        r = requests.post(api_url, data=data).json()
        # 向服务器发送请求
        return r.get("text")
    except:
        return


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReplay = 'I received: ' + msg['Text']
    robots = ['I am Jarvis.May I have a message to Tony?', 'Hello,I am Jarvis.']
    reply = get_response(msg['Text'])
    # random.choice会从robots中随机选取一个元素，这个可以根据自己喜好来修改
    return reply


@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
# 用于接收群里面的对话消息
def print_content(msg):
    return get_response(msg['Text'])


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    if msg.User["NickName"] == '银燕软件部' or msg.User["NickName"] == 'YY爬虫群':
    # if msg.User["NickName"] == '发小儿' or msg.User["NickName"] == 'Data Science Group of CityU':
        # msg['FromUserName']就是发送者的ID
        present_time = time.strftime("%Y:%m:%d %H:%M:%S", time.localtime())
        print("Now is %s, the msg or pic is from %s, %s. " % (present_time, msg.User['NickName'], msg['ActualNickName']))
        receive_msg = str(msg['Text']).split("\n")

        msg_ = []
        print("-------------------------------------------------接受的消息--------------------------------------------------")
        for i in receive_msg:
            print(i)
            with open("msg_tackled_.txt", "a+") as f:

                # 匹配文本中的数字
                all = re.findall(r"\d+\.?\d*", i)
                # 匹配文本中的汉字
                font = re.findall(r'[\u4e00-\u9fa5]+', i)
                if len(all) != 0:
                    all_price = sorted([eval(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", x)) for x in all], reverse=True)
                    max_length, content = max([(len(x), x) for x in font])
                    # a = " 公司:" + content + " " + "金额:" + str(all_price[1]) + " " + "价格:" + str(all_price[0])
                    a = content + " " +str(all_price[1]) + " "+ str(all_price[0])+"\n"
                    f.write(str(a) + "\n")
                    msg_.append(a)
        print("--------------------------------------------------处理后的信息-----------------------------------------------")
        y = ""
        for x in msg_:
            # 将消息的类型和文本内容返回给发送者
            y += x
        print(y)
        itchat.send('%s \n' % y, msg['FromUserName'])



@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)    #群图片消息的处理
def download_files(msg):
    if msg.User["NickName"] == '银燕软件部' or msg.User["NickName"] == 'YY爬虫群':
    # if msg.User["NickName"] == '发小儿' or msg.User["NickName"] == 'Data Science Group of CityU':

    # print(msg.User['NickName'] + ":" + msg['Text'])     #打印哪个群给你发了什么消息
    # 传入文件名，将文件下载下来
        msg['Text'](msg['FileName'])    # 把下载好的文件再发回给发送者

    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
    
    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

    #     if msg["Content"]=="图片":
    #         pic = "mao.jpg"
    #         print(111)
    #     # print(get_response(msg['Text'])+"\n")           #打印机器人回复的消息
    #         name = msg.User["NickName"]
    #         print(name)
    #         itchat.send_image(pic, toUserName=name)
    #     else:
    #         return get_response(msg['Text'])
    # else:                                         #其他群聊直接忽略
    #     pass

# @itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE], isGroupChat=True):


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # , 保持在线，下次运行代码可自动登录  hotReload=True
    itchat.run()

