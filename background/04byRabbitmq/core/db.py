from mongoengine import connect

from conf import setting

def my_connet():
    connect(db=setting._MONGODB_NAME, host=setting._MONGODB_HOST, port=setting._MONGODB_PORT)
