from django.shortcuts import render

import requests
import sys
from subprocess import run,PIPE

from .hello import testrunning

def button(request):
    return render(request,'home.html')

def output(request):
    # data=requests.get("https://reqres.in/api/users")
    data=requests.get("https://www.google.com")
    print(data.text)
    data=data.text
    return render(request,'home.html',{'data':data})

def external(request):
    inp= request.POST.get('param')
    text = testrunning(inp)
    # out = inp
    # print(out)
    print(text)
    # return render(request, 'home.html')
    return render(request,'home.html',{'data1':text})