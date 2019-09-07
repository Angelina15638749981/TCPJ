
import datetime
import time
import math
import random
import requests
import json
requests.packages.urllib3.disable_warnings()

# userId
userId = ""
# nc_token
# # nc_token = ["FFFF00000000017EDC0B", (new Date()).getTime(), Math.random()].join(':');
t = time.time()
str1 = "FFFF00000000017EDC0B"
str2 = str(int(round(t * 1000)))
str3 = str(random.random())
nc_token = str1+"%3A"+str2+"%3A"+str3
userName = "15638749981"
passWord = "syf11140725com"

# nc_token="FFFF0N00000000006CEC%3A1566972194453%3A0.3831247839494356"
csessionid = "010B3TrWzwsdkM2Lqh18cIU1DBMJh-BmLfmZmsnJ9NPbPnm0HGgIH09_WXRYS66N3E8BPr1K8yJNxOoCnfhcGdFdILksAsi_jOiYiArUQCcwdB868MvOl8tcUwL1pP4CneUkK6Lznktfg0HrA9IRZodYo5RIua7vTpjLLqQCtCGyRakNb-mttl5VEb5I2zAEOv86kToIZFsl19mhs_mLSHIA"
sig = "05XqrtZ0EaFgmmqIQes-s-CGe24G1xxTIrr8iDy2e9mXrD-S1kBkkpOdWIAB-7epjMH9PottefDCerfMN9HCuwtrayugzpyMdV72hb2T1HRI5c61lO4c5xF4cmdomh5dU6U2Yd9F9ZRoF3GxJDvbZDf8Gotuhyu2enDPY2EOTfU_1CIkO9SXJYJ7mJrNcS--L8fLZZV-upiGuy3Gxu4oNPIXHaYKMqpUAA9JMAETY2WB6J5qhY_MrcYaNOV0HVaB0v01Ar3YahFiLVfGqfBS59zuRhH8dfu7zjXHSvkZIyX-K7Q_OZnbYj1GIsD3dN-umc3JTbp7Usk86QpibyiCwJukh4VLZvMZzpEvDs1oiAkZQxne_vxjEuB9DJKKPOAoxvNeytiSgO8xLXd3krP5xatz0ZFS1mz4z4HP5D9PkHdQS-JC3HZoAWw1ixygJNjJYqgsxcOvbWKEKlPNtpk3lJT1ZCpYJQSc0WbkEH-8et4qs"
type=1

headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh - CN, zh;q = 0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Content-Length": "844",
        "cookie": "_uab_collina=155616336304149025669944;ASP.NET_SessionId=5avphjgmiyee2nkhqmr2wayj;acw_tc=24f9419d15668913294182713e074483688c5bd059eb19f828ef4d3723",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/Account/Login?rUrl=https%3A%2F%2Fwww.tcpjw.com%2F",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'Connection': 'Keep-Alive',
        'Host': 'www.tcpjw.com',
        'x-requested-with': 'XMLHttpRequest'

}


data = {

        "userName": "%s" % userName,
        "passWord": "%s" % passWord,
        "nc_token": "%s" % nc_token,
        "csessionid": "%s" % csessionid,
        "sig": "%s" % sig,
        "type": "%s" % type,

}
# print(nc_token)
response = requests.post("https://www.tcpjw.com/Account/Login", headers=headers, data=data, verify=False)
print(response.status_code)
print(response.text)
info = str(json.loads(response.text)["msg"]).split("--")
# for x in info:
#     print(x)


# print(response.text["csessionid"])
"""
userId=&
nc_token=FFFF00000000017EDC0B%3A1566973139484%3A0.588549301146895&
csessionid=03oqci1BRKevK1yQNbxHIxzOBRW3YPkOIOFALD5BISKENHTdfEBoavxTasS8jYde9OlGt-UD2HYl4aF5M9G5dUm7QoyNQVMpugJ5Frp0FEuKtgwqAU-CUmZ5ggigKi4yfSusf38M7BaU8joilXo7IvRdyh_6g-ZekXQKgUi7WQqTCQ4_8g4r00VXEGx-b8TwDpdAG_m7RJpuEkS7to9dZgz5_82RkfUlIbV8dcrkf2StE&
sig=05a1C7nT4bR5hcbZlAujcdyZopdDAhYmqcB36HSTtWsUrP_naenufpGcDv_GHxLtLz4wRPeru_zkT1jQANHbKTPf4S_PWr4ZveVc4zobBfkn2NcunTo1InRMd-u1rE_ZgtP4MnSDZUtwlhzwu1w7M7XFFDJwdaRtMjo0Jq4E5TUjsB3fTdxa3NgHUcyS5-jz9mgAplArdq55kicsDCHVvLjqPs0BCbnbeaa3w4eUHrkZZed1mCFAqTsIKTu8wKti7Tqq2BMYVMexlFdHBlFXlbS8be4gQHgwCP0IaqyNnECbWZrTV_ZakxCTeK7znsauiyB9E5RfuxiRny_e7PiFnYmbKRu8LmJfRGoPT6zkPY9KLDpfEoEHb4tYU_Z8dKKaB_NdKE_7oFTsWcFprJwG8N7y1SHS3zEH3E01wLx7hwFInLRUlrrtvdW67ydhG5j6KFEaqOep8rCbgyD1Ys5Twr7agHYfFrrmRWNmxob-fWN-NBhrHbonN2fVKehHEcHOJXuj_r0ZDUxx5o14nClKpcnA
"""
userId = ""
# nc_token = info[2].split(":")[1]
# csessionid = info[3].split(":")[1]
# sig = info[4].split(":")[1]
# print(nc_token)
# print(csessionid)
# print(sig)



# 处理验证码
headers1 = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest',
        "cookie": "Cookie: ASP.NET_SessionId=5avphjgmiyee2nkhqmr2wayj; acw_tc=24f9419d15668913294182713e074483688c5bd059eb19f828ef4d3723; NewUserCookie=x/0ZjgxwrC2CvM/xC1lDSHx6j0JZ30d337685+F+KOUlluh1GD0x/Ik9HsEkAxyMW1gDsWCom9wGnPowo1O7TpQavAo8KNVlxD+dfhPw5HCvODIMYEYS2TJ2JnoiFzf79bdj590XsN5MVlglyxiEXw==",
        "Content-Length": "863",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/orderList/VisitValid?forceValid=1&userIdOver=118.178.15.96&redirectUrl=%2fOrderList%2fTradingCenter",
        'Connection': 'Keep-Alive',
        'Host': 'www.tcpjw.com',

}


data1 = {

        "userId": "%s" % userId,
        "nc_token": "%s" % nc_token,
        "csessionid": "%s" % csessionid,
        "sig": "%s" % sig,

}
# print(nc_token)
response = requests.post("https://www.tcpjw.com/orderList/updateVisitState", headers=headers1, data=data1, verify=False)
print(response.status_code)
print(response.content)


"""
userName=15638749981&passWord=syf11140725com&
nc_token=FFFF0N00000000006CEC%3A1567389212329%3A0.18108814991969946&
csessionid=01meJRDQhjKvuhvkU5cu47-H1uENYKXmqn19h1pavY-umO0KA00XiJpptKUle1pvr0lr4kNRx113PcQSmw4CDenP0gAr0O8tIId3dMSMVprRhgj08S1T5hVVoDayX289iJTA5GTSvJxHdLoG3PGaqpeVU6u7Y_cKsgOI96i9wGvdJyhRIJZ43IgYkC9mkCNCwFym8pJ4RbNE-grJRaZ6L65Q&sig=05XqrtZ0EaFgmmqIQes-s-CP6dZm68CXEBWXIbvKyoiirD-S1kBkkpOdWIAB-7epjMQ5frzvzQhXCPpyNZ59GkYGcojBOfKZbdGyc8wzU0woFg7wEoevct_fcCivXMzeYLi0bLnaQf1K6F8JpN-hahiCxC0R14RKFrbJOZKFhyhAMigpGGR5J1rkOOcCdLpLhP07vCmVn1lxv-6rZte1Qkc0x32w8nUHnXT2fP4YQWQXePuqhHIKg-Xq1epdkhFh7mExhygtd82qIZTMnCDt79IV03WIdso6Ik7dgZumfOEy_nah0NDEHG3Fc1yZS5o6rLknZQkJmrAt2WAtEvVGHTcfN31CQWQymw0tydeNJoJ8C9gi2ugMk6yTolaC_m_ouGn_rnpvHJYCqkEeJTMvrpyR7lj5PMEC7aMIdwlPReGaktWbMUDPM7xvzQ171vRReiBXImFC6O96B74v0til_xQ75BdKtsxfcxrxuuM1aoVnk&
type=1

"""