from mongoengine import *
import datetime


class JobInfo(Document):
    userid = StringField()
    created=DateTimeField()
    casename = StringField()
    dir = StringField()
    file = StringField()
    fullpath = StringField()
    type = StringField()
