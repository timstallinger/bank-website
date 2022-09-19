from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

template = loader.get_template('login.html')

def index(request):
    return HttpResponse(template.render({}, request))
    # return HttpResponse("Willkommen bei der Megagutebank Bank!")