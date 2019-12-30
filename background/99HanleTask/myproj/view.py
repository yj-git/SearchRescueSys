from django.shortcuts import render, HttpResponse
from myapp.models import Test
from datetime import datetime
from tools import sender
import json
import os


def test1(request):
    # json字符串直接发给队列，当任务参数
    try:
        body = request.body.decode()
        sender.sendtask(body)
    except:
        HttpResponse(json.dumps({'isSuccess': 'false'}))
    return HttpResponse(json.dumps({'isSuccess': 'true'}))
