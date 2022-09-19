from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

template = loader.get_template('login.html')
register_template = loader.get_template('register.html')

def index(request):
    return HttpResponse(template.render({}, request))
    # return HttpResponse("Willkommen bei der Megagutebank Bank!")

def register(request):
    return HttpResponse(register_template.render({}, request))