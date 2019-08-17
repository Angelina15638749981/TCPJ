
from pymongo import MongoClient


# 创建连接对象
client = MongoClient(host='localhost', port=27017)
# 获得数据库，此处使用 data 同城票据 数据库
db = client.bank
col = db.data

# 银行类型：国股
# 判断依据：1
# 非时间戳类型，发布时间: 1565160180
# 时间戳类型，发布时间: 08.07 14:43
# 承兑人: 广发银行潍坊分行营业部
# 金额（万元）: 10.0
# 到期日: 345
# 每十万扣息: 2650
#  年息: 2.7652 %
# 瑕疵: 无
# 操作: 1
# 存储成功
col.update_one({
    "judgement_basis": "1",
    'publish_time':1565167800,
    "person": "交通银行长沙井湾子支行",
    "expire_date": 124,
    "annual_interest": "2.5694 %",
    "operation":"接单"}, {"$set": {'operation': "完成"}})
print("----------------------------------------------状态由接单变为交易完成--------------------------------------")

# col.update_one({
#     "judgement_basis": "1",
#     'publish_time': 1565160180,
#     "person": "广发银行潍坊分行营业部",
#     "expire_date": 345,
#     "annual_interest": "2.7652 %",
#     "operation": 9}, {"$set": {'operation': 16}})
# print("----------------------------------------------状态由接单变为交易完成--------------------------------------")



#13213242228
# yy123456













