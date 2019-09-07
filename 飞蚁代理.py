import requests
import sys
import time
import hashlib
import logging
import json
# -*- coding: UTF-8 –*-
import requests
requests.packages.urllib3.disable_warnings()

#  http://proxy.360pdown.com:88/open?user_name=syf11140725ap1&timestamp=15889653664&md5=00112233445566778899AABBCCDDEEFF&pattern=json&number=2&province=510000&city=510100
headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "content-length": "310",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=24f9419915668933329793630e96aed17e47a82d7338cc5dc1becd5c78; ASP.NET_SessionId=h1kjrhbx4hkj4qnao4e15q4d; NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'x-requested-with': 'XMLHttpRequest',
        # "Proxy-Authorization": auth
    }

data = {
    # 待结单
    # "pt_tradestatus": "00",
    # 交易完成
    # "00", "1", pageIdx_client_gg_jiedan
    "pt_tradestatus": "00",
    "pt_bid": "1",
    "pageIdx_client": "1" ,
    "X-Requested-With": "XMLHttpRequest",

}
proxy_username = 'syf11140725ap1'
proxy_passwd = '24447312'
proxy_server = '183.129.244.16'
proxy_port = '88'
pattern = 'json'
num = 20  #获取端口数量
key_name = 'user_name='
key_timestamp = 'timestamp='
key_md5 = 'md5='
key_pattern = 'pattern='
key_num = 'number='
key_port = 'port='


def get_timestamp():
    timestamp = round(time.time() * 1000)
    # print(timestamp)
    return timestamp


def get_md5_str(s):
    return hashlib.md5(bytes(s, encoding='utf8')).hexdigest()


def get_open_url():
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + proxy_port + '/open?' + key_name + proxy_username +\
           '&' + key_timestamp + str(time_stamp) +\
           '&' + key_md5 + md5_str + \
           '&' + key_pattern + pattern +\
           '&' + key_num + str(num)


def get_close_url(auth_port):
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + proxy_port + '/close?' + key_name + proxy_username +\
           '&' + key_timestamp + str(time_stamp) +\
           '&' + key_md5 + md5_str + \
           '&' + key_pattern + pattern + \
           '&' + key_port + auth_port


def get_reset_url():
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + proxy_port + '/reset_ip?' + key_name + proxy_username + \
           '&' + key_timestamp + str(time_stamp) +\
           '&' + key_md5 + md5_str +\
           '&' + key_pattern + pattern


def testing(url, auth_port):
    proxies = {'http': "http://" + proxy_server + ':' + auth_port,
               'https': 'http://' + proxy_server + ':' + auth_port, }
    try:
        s = requests.Session()
        s.proxies.update(proxies)
        ret = s.post(url,  headers=headers, data=data, verify=False, timeout=5)
        print(ret.text)
        msg = str(ret.status_code)

    except requests.exceptions.SSLError as e:
        msg = repr(e)

        # testing(url, auth_port)
    except Exception as e:
        msg = repr(e)

    return msg


# def get_proxy():
#     api_url = "http://proxy.360pdown.com:88/open?user_name=lt_test_1&timestamp=15889653664&md5=00112233445566778899AABBCCDDEEFF&pattern=json&number=2&province=510000&city=510100"
#     res = requests.get(api_url).content
#     print(res)
#     if len(res) == 0:
#         print('no data')
#     elif 'bad' in str(res):
#         print('bad request')
#     else:
#         print("get all proxies")
#     proxies = []
#     for line in str(res).split():
#         proxies.append(line.strip().split(":"))
#     print(proxies)


# get_proxy()
if __name__ == '__main__':
    count = 0
    port = ''
    start = time.time()
    print(start)
    # now = time.time()
    # print(now)
    while True:
        open_url = get_open_url()
        r = requests.get(open_url, timeout=3)
        result = str(r.content, encoding='utf8')
        json_obj = json.loads(result)
        code = json_obj['code']
        # left_ip = json_obj['left_ip']
        # print(left_ip)
        if json_obj['code'] == 108:
            reset_url = get_reset_url()
            r = requests.get(reset_url, timeout=3)
        elif json_obj['code'] == 100:
            port = str(json_obj['port'][0])
        if time.time()-start >= 10:
            tmp = testing('https://www.tcpjw.com/OrderList/TradingCenter', port)
            time.sleep(1)
            print(tmp)
            print("----------------------2----------------------------------------")
        else:
            close_url = get_close_url(port)
            r = requests.get(close_url, timeout=3)
            result = str(r.content, encoding='utf8')





