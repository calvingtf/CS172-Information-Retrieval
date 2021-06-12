from django.shortcuts import render

import requests
import sys
from subprocess import run,PIPE

def button(request):
    return render(request,'home.html')

def output(request):
    data=requests.get("https://reqres.in/api/users")
    print(data.text)
    data=data.text
    return render(request,'home.html',{'data':data})

def external(request):
    # inp= request.POST.get('param')
    # # out= run([sys.executable,'//mnt//e//work//django_testing//test.py',inp],shell=False, stdout=PIPE)
    # out = inp
    # print(out)
    inp = request.POST
    print(inp)
    return render(request, 'home.html')
    # return render(request,'home.html',{'data1':out.stdout})