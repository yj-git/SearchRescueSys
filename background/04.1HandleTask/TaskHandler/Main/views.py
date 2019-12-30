from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.


def test(request):
    s = datetime.datetime.now().__str__()
    return HttpResponse('test over now:'+s)


def test(request):
    return HttpResponse('done')
