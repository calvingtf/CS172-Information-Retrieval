from django.shortcuts import render

import sys
sys.path.append("..") # Adds higher directory to python modules path.

import requests
import sys
from subprocess import run,PIPE

from .indexer import web_search

def button(request):
    return render(request,'home.html')

def output(request):
    # data=requests.get("https://reqres.in/api/users")
    data=requests.get("https://www.google.com")
    print(data.text)
    data=data.text
    return render(request,'home.html',{'data':data})

def external(request):
    input_query = request.POST.get("input_query")
    input_url = request.POST.get("input_url")
    input_pages = request.POST.get("input_pages")
    input_depth = request.POST.get("input_depth")
    text = ""
    if input_pages == "" and input_depth == "":
        text = web_search(input_url, input_query)
    elif input_depth == "":
        text = web_search(input_url, input_query, int(input_pages), 10)
    elif input_pages == "":
        text = web_search(input_url, input_query, 50, int(input_depth))
    else:
        text = web_search(input_url, input_query, int(input_pages), int(input_depth))
    # out = inp
    # print(out)
    print(text)
    # return render(request, 'home.html')
    return render(request,'home.html',{'data1':text})