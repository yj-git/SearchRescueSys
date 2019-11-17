import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.pythondb
db = client['test']
collection = db.python_collection
collection = db['rbmqlog']

# state=0正在进行，state=1完成,state=-1异常或失败


def insertLog(msg, state, detail=''):
    logdic = {
        'taskMessage': msg,
        'state': state,
        'detail': detail,
        'createtime': datetime.datetime.now()
    }
    mid = collection.insert_one(logdic).inserted_id
    return mid
